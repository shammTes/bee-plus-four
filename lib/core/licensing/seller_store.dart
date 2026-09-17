import 'package:hive_flutter/hive_flutter.dart';
import 'package:uuid/uuid.dart';

import 'device_id.dart';
import 'qr_payload.dart';

/// Local offline state for Bee Seller: quota remaining + history.
class SellerStore {
  SellerStore._();
  static final SellerStore instance = SellerStore._();

  static const _boxName = 'bee_seller';
  static const _quotaKey = 'quota_remaining';
  static const _wholesaleKey = 'is_wholesale';
  static const _historyKey = 'issue_history';
  static const _usedNoncesKey = 'used_nonces';

  Box? _box;

  Future<void> init() async {
    await Hive.initFlutter();
    _box = await Hive.openBox(_boxName);
  }

  Future<String> deviceId() => DeviceIdService.instance.getOrCreate();

  int get quotaRemaining => (_box?.get(_quotaKey) as int?) ?? 0;

  bool get isWholesale => (_box?.get(_wholesaleKey) as bool?) ?? false;

  bool get canIssueStudent => quotaRemaining > 0;

  bool get canIssueSeller => isWholesale && quotaRemaining > 0;

  List<Map<String, dynamic>> get history {
    final raw = _box?.get(_historyKey);
    if (raw is List) {
      return raw
          .map((e) => Map<String, dynamic>.from(e as Map))
          .toList()
          .reversed
          .toList();
    }
    return [];
  }

  Set<String> get _usedNonces {
    final raw = _box?.get(_usedNoncesKey);
    if (raw is List) return raw.map((e) => '$e').toSet();
    return {};
  }

  Future<void> _markNonce(String n) async {
    final s = _usedNonces..add(n);
    await _box?.put(_usedNoncesKey, s.toList());
  }

  /// Redeem Master wholesale code OR another seller's SELLER grant.
  Future<String> redeemAuthCode(String raw) async {
    final p = QrPayload.tryParse(raw.trim());
    if (p == null) return 'Invalid code format.';
    if (!p.isSignatureValid) return 'Invalid signature.';
    final id = await deviceId();
    if (!p.matchesDevice(id)) {
      return 'Code is bound to another seller device.\nThis device: $id';
    }
    if (_usedNonces.contains(p.nonce)) return 'This code was already used.';
    final q = p.quota;
    if (q == null || q < 1) return 'Invalid quota on code.';

    if (p.isWholesale) {
      await _box?.put(_quotaKey, quotaRemaining + q);
      await _box?.put(_wholesaleKey, true);
      await _markNonce(p.nonce);
      return 'Wholesale activated. +$q unlocks. You can issue student QR and seller codes.';
    }
    if (p.isSellerGrant) {
      await _box?.put(_quotaKey, quotaRemaining + q);
      // sub-sellers do not automatically get wholesale privilege
      await _markNonce(p.nonce);
      return 'Seller credit added. +$q student unlocks.';
    }
    return 'Not a wholesale or seller code.';
  }

  /// Issue student unlock QR for a student device id. Consumes 1 quota.
  Future<({String? code, String? error})> issueStudentUnlock(
      String studentDeviceId) async {
    final sid = studentDeviceId.trim();
    if (sid.isEmpty) return (code: null, error: 'Enter student Device ID.');
    if (quotaRemaining < 1) {
      return (code: null, error: 'No quota left. Redeem a wholesale/seller code.');
    }
    final nonce = const Uuid().v4().replaceAll('-', '').substring(0, 12);
    final payload = QrPayload.issue(
      packageCode: 'HIGHSCHOOL',
      deviceId: sid,
      nonce: nonce,
    );
    await _box?.put(_quotaKey, quotaRemaining - 1);
    await _appendHistory({
      'type': 'STUDENT',
      'target': sid,
      'at': DateTime.now().toIso8601String(),
      'code': payload.encode(),
    });
    return (code: payload.encode(), error: null);
  }

  /// Wholesale seller issues SELLER:quota for another seller device.
  Future<({String? code, String? error})> issueSellerCode({
    required String targetSellerDeviceId,
    required int grantQuota,
  }) async {
    if (!isWholesale) {
      return (code: null, error: 'Only wholesale sellers can grant seller codes.');
    }
    final tid = targetSellerDeviceId.trim();
    if (tid.isEmpty) return (code: null, error: 'Enter target seller Device ID.');
    final q = grantQuota.clamp(1, 10000);
    if (quotaRemaining < q) {
      return (code: null, error: 'Not enough quota (have $quotaRemaining).');
    }
    final nonce = const Uuid().v4().replaceAll('-', '').substring(0, 12);
    final payload = QrPayload.issueSeller(
      sellerDeviceId: tid,
      quota: q,
      nonce: nonce,
    );
    await _box?.put(_quotaKey, quotaRemaining - q);
    await _appendHistory({
      'type': 'SELLER',
      'target': tid,
      'quota': q,
      'at': DateTime.now().toIso8601String(),
      'code': payload.encode(),
    });
    return (code: payload.encode(), error: null);
  }

  Future<void> _appendHistory(Map<String, dynamic> row) async {
    final list = List<Map<String, dynamic>>.from(
      (_box?.get(_historyKey) as List? ?? []).map(
        (e) => Map<String, dynamic>.from(e as Map),
      ),
    );
    list.add(row);
    await _box?.put(_historyKey, list);
  }
}

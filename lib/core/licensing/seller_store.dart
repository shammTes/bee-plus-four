import 'package:hive_flutter/hive_flutter.dart';
import 'package:uuid/uuid.dart';

import 'device_id.dart';
import 'qr_payload.dart';

class IssueResult {
  const IssueResult.ok(this.code) : error = null;
  const IssueResult.fail(this.error) : code = null;
  final String? code;
  final String? error;
}

/// Offline quota + code history for Bee Seller app.
class SellerStore {
  SellerStore._();
  static final SellerStore instance = SellerStore._();

  static const _boxName = 'seller_store_v1';
  static const _quotaKey = 'remaining_quota';
  static const _historyKey = 'history';
  static const _usedNoncesKey = 'used_nonces';

  Box? _box;

  Future<void> init() async {
    _box = await Hive.openBox(_boxName);
  }

  int get quota => (_box?.get(_quotaKey) as int?) ?? 0;
  int get remainingQuota => quota;

  Future<String> deviceId() => DeviceIdProvider.getId();

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
    if (raw is List) return raw.map((e) => e.toString()).toSet();
    return {};
  }

  Future<void> _saveUsedNonces(Set<String> nonces) async {
    await _box?.put(_usedNoncesKey, nonces.toList());
  }

  Future<String> redeemAuthCode(String raw) async {
    final payload = QrPayload.tryParse(raw);
    if (payload == null || !payload.isSignatureValid) {
      return 'Invalid grant code.';
    }
    final type = payload.packageCode;
    if (!type.startsWith('WHOLESALE:') && !type.startsWith('SELLER:')) {
      return 'Not a seller grant.';
    }
    final myId = await DeviceIdProvider.getId();
    if (!payload.matchesDevice(myId)) return 'Grant is for another seller device.';
    final nonces = _usedNonces;
    if (nonces.contains(payload.nonce)) return 'Grant already used.';
    final q = payload.quota ?? 0;
    if (q <= 0) return 'Grant quota is 0.';
    nonces.add(payload.nonce);
    await _saveUsedNonces(nonces);
    await _box?.put(_quotaKey, quota + q);
    await _hist('redeem', type);
    return 'Added $q unlocks. Quota now ${quota}.';
  }

  Future<IssueResult> issueStudentUnlock(
    String studentDeviceId, {
    String packageCode = 'HIGHSCHOOL',
  }) async {
    final id = studentDeviceId.trim();
    if (id.isEmpty) return const IssueResult.fail('Enter or scan a device ID.');
    if (quota < 1) return const IssueResult.fail('No quota left.');
    final nonce = const Uuid().v4().replaceAll('-', '').substring(0, 12);
    final payload = QrPayload.issue(
      packageCode: packageCode.toUpperCase(),
      deviceId: id,
      nonce: nonce,
    );
    await _box?.put(_quotaKey, quota - 1);
    await _hist('student:$packageCode', id);
    return IssueResult.ok(payload.encode());
  }

  Future<IssueResult> issueSellerCode({
    required String targetSellerDeviceId,
    required int grantQuota,
  }) async {
    if (grantQuota <= 0 || quota < grantQuota) {
      return const IssueResult.fail('Not enough quota.');
    }
    final nonce = const Uuid().v4().replaceAll('-', '').substring(0, 12);
    final payload = QrPayload.issue(
      packageCode: 'SELLER:$grantQuota',
      deviceId: targetSellerDeviceId.trim(),
      nonce: nonce,
    );
    await _box?.put(_quotaKey, quota - grantQuota);
    await _hist('sub_seller', targetSellerDeviceId);
    return IssueResult.ok(payload.encode());
  }

  Future<void> _hist(String type, String target) async {
    final hist = List<Map<String, dynamic>>.from(
      (_box?.get(_historyKey) as List?)
              ?.map((e) => Map<String, dynamic>.from(e as Map)) ??
          [],
    );
    hist.add({
      'type': type,
      'target': target,
      'at': DateTime.now().toIso8601String(),
    });
    await _box?.put(_historyKey, hist);
  }
}

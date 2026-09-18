import 'package:hive_flutter/hive_flutter.dart';
import 'package:uuid/uuid.dart';

import 'device_id.dart';
import 'qr_payload.dart';

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

  int get remainingQuota => (_box?.get(_quotaKey) as int?) ?? 0;

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

  Future<bool> redeemAuthCode(String raw) async {
    final payload = QrPayload.tryParse(raw);
    if (payload == null || !payload.isSignatureValid) return false;

    final type = payload.packageCode;
    if (!type.startsWith('WHOLESALE:') && !type.startsWith('SELLER:')) {
      return false;
    }

    final myId = await DeviceIdProvider.getId();
    if (!payload.matchesDevice(myId)) return false;

    final nonces = _usedNonces;
    if (nonces.contains(payload.nonce)) return false;

    final quota = payload.quota ?? 0;
    if (quota <= 0) return false;

    nonces.add(payload.nonce);
    await _saveUsedNonces(nonces);

    final current = remainingQuota;
    await _box?.put(_quotaKey, current + quota);

    final hist = List<Map<String, dynamic>>.from(
      (_box?.get(_historyKey) as List?)
              ?.map((e) => Map<String, dynamic>.from(e as Map)) ??
          [],
    );
    hist.add({
      'type': 'redeem',
      'code': type,
      'quota': quota,
      'at': DateTime.now().toIso8601String(),
    });
    await _box?.put(_historyKey, hist);
    return true;
  }

  Future<String?> issueStudentUnlock(String studentDeviceId) async {
    if (remainingQuota < 1) return null;
    final nonce = const Uuid().v4().replaceAll('-', '').substring(0, 12);
    final payload = QrPayload.issue(
      packageCode: 'HIGHSCHOOL',
      deviceId: studentDeviceId,
      nonce: nonce,
    );
    await _box?.put(_quotaKey, remainingQuota - 1);

    final hist = List<Map<String, dynamic>>.from(
      (_box?.get(_historyKey) as List?)
              ?.map((e) => Map<String, dynamic>.from(e as Map)) ??
          [],
    );
    hist.add({
      'type': 'student',
      'target': studentDeviceId,
      'at': DateTime.now().toIso8601String(),
    });
    await _box?.put(_historyKey, hist);
    return payload.encode();
  }

  Future<String?> issueSellerCode(String subSellerDeviceId, int quota) async {
    if (quota <= 0 || remainingQuota < quota) return null;
    final nonce = const Uuid().v4().replaceAll('-', '').substring(0, 12);
    final payload = QrPayload.issue(
      packageCode: 'SELLER:$quota',
      deviceId: subSellerDeviceId,
      nonce: nonce,
    );
    await _box?.put(_quotaKey, remainingQuota - quota);

    final hist = List<Map<String, dynamic>>.from(
      (_box?.get(_historyKey) as List?)
              ?.map((e) => Map<String, dynamic>.from(e as Map)) ??
          [],
    );
    hist.add({
      'type': 'sub_seller',
      'target': subSellerDeviceId,
      'quota': quota,
      'at': DateTime.now().toIso8601String(),
    });
    await _box?.put(_historyKey, hist);
    return payload.encode();
  }
}

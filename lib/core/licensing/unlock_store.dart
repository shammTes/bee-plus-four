import 'package:hive_flutter/hive_flutter.dart';
import 'device_id.dart';
import 'qr_payload.dart';

class UnlockStore {
  UnlockStore._();
  static final instance = UnlockStore._();
  static const _boxName = 'four_unlock_v1';
  static const _packagesKey = 'packages';
  static const _noncesKey = 'used_nonces';
  late Box _box;
  Future<void> init() async { _box = await Hive.openBox(_boxName); }
  Set<String> get unlockedPackages {
    final list = (_box.get(_packagesKey) as List?)?.cast<String>() ?? [];
    return list.toSet();
  }
  Set<String> get _usedNonces {
    final list = (_box.get(_noncesKey) as List?)?.cast<String>() ?? [];
    return list.toSet();
  }
  Future<void> _markNonce(String nonce) async {
    final set = _usedNonces..add(nonce);
    await _box.put(_noncesKey, set.toList());
  }
  Future<void> _addPackage(String code) async {
    final set = unlockedPackages..add(code);
    await _box.put(_packagesKey, set.toList());
  }
  Future<Result<String>> applyPayload(String raw) async {
    final payload = QrPayload.tryParse(raw);
    if (payload == null) return Result.err('Invalid QR format');
    if (!payload.isSignatureValid) return Result.err('Invalid or tampered signature');
    final deviceId = await DeviceIdProvider.getId();
    if (!payload.matchesDevice(deviceId)) return Result.err('QR is bound to another device');
    if (_usedNonces.contains(payload.nonce)) return Result.err('This QR was already used (single-use only)');
    final pkg = UnlockPackageX.fromCode(payload.packageCode);
    if (pkg == null) return Result.err('Unknown package');
    // App 4 is highschool-focused; still accept valid packages but surface HIGHSCHOOL primarily.
    await _markNonce(payload.nonce);
    await _addPackage(pkg.code);
    return Result.ok('${pkg.code} unlocked permanently on this device');
  }
}

class Result<T> {
  final T? value;
  final String? error;
  bool get isOk => error == null;
  Result.ok(this.value) : error = null;
  Result.err(this.error) : value = null;
}

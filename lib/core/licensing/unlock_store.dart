import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:hive_flutter/hive_flutter.dart';
import 'package:uuid/uuid.dart';

import 'device_id.dart';
import 'qr_payload.dart';

/// Simple result type for unlock attempts.
class UnlockResult {
  const UnlockResult.ok(this.value) : error = null;
  const UnlockResult.fail(this.error) : value = null;
  final String? value;
  final String? error;
  bool get isOk => error == null;
}

/// Offline licensing + permanent device identity for Bee Seller QR unlock.
class UnlockStore {
  UnlockStore._();
  static final instance = UnlockStore._();

  static const _boxName = 'unlock';
  static const _deviceKey = 'device_id';
  static const _seenOnboardKey = 'seen_onboarding';
  static const _packagesKey = 'unlocked_packages';
  static const _usedNoncesKey = 'used_nonces';
  static const _secure = FlutterSecureStorage();

  Box? _box;
  String? _deviceId;

  Future<void> init() async {
    _box = await Hive.openBox(_boxName);
    await deviceId();
  }

  /// Stable unique ID generated once on first install.
  Future<String> deviceId() async {
    if (_deviceId != null) return _deviceId!;
    // Align with DeviceIdProvider when available
    try {
      final id = await DeviceIdProvider.getId();
      _deviceId = id;
      await _box?.put(_deviceKey, id);
      return id;
    } catch (_) {}
    String? id = await _secure.read(key: _deviceKey);
    id ??= _box?.get(_deviceKey) as String?;
    if (id == null || id.isEmpty) {
      id = const Uuid().v4().replaceAll('-', '').substring(0, 12).toUpperCase();
      await _secure.write(key: _deviceKey, value: id);
      await _box?.put(_deviceKey, id);
    } else {
      await _secure.write(key: _deviceKey, value: id);
      await _box?.put(_deviceKey, id);
    }
    _deviceId = id;
    return id;
  }

  bool get isUnlocked =>
      unlockedPackages.contains('HIGHSCHOOL') ||
      ((_box?.get('unlocked') as bool?) ?? false);

  Future<void> setUnlocked(bool v) async => _box?.put('unlocked', v);

  bool get seenOnboarding => (_box?.get(_seenOnboardKey) as bool?) ?? false;

  Future<void> markOnboardingSeen() async =>
      _box?.put(_seenOnboardKey, true);

  Set<String> get unlockedPackages {
    final raw = _box?.get(_packagesKey);
    if (raw is List) {
      return raw.map((e) => '$e').toSet();
    }
    if (isUnlocked) return {'HIGHSCHOOL'};
    return {};
  }

  Future<void> _savePackages(Set<String> pkgs) async {
    await _box?.put(_packagesKey, pkgs.toList());
    if (pkgs.contains('HIGHSCHOOL')) {
      await _box?.put('unlocked', true);
    }
  }

  Set<String> get _usedNonces {
    final raw = _box?.get(_usedNoncesKey);
    if (raw is List) return raw.map((e) => '$e').toSet();
    return {};
  }

  Future<void> _markNonce(String nonce) async {
    final s = _usedNonces..add(nonce);
    await _box?.put(_usedNoncesKey, s.toList());
  }

  /// Apply Bee Seller QR / pasted payload. Device-bound, single-use, permanent.
  Future<UnlockResult> applyPayload(String raw) async {
    final text = raw.trim();
    if (text.isEmpty) {
      return const UnlockResult.fail('Paste the unlock code from Bee Seller.');
    }
    final payload = QrPayload.tryParse(text);
    if (payload == null) {
      return const UnlockResult.fail('Invalid code format.');
    }
    if (!payload.isSignatureValid) {
      return const UnlockResult.fail('Invalid signature.');
    }
    final currentId = await deviceId();
    if (!payload.matchesDevice(currentId)) {
      return UnlockResult.fail(
          'Code is for another device. This device: $currentId');
    }
    if (_usedNonces.contains(payload.nonce)) {
      return const UnlockResult.fail('This code was already used.');
    }
    final pkg = UnlockPackageX.fromCode(payload.packageCode);
    if (pkg == null) {
      return const UnlockResult.fail('Unknown package.');
    }
    final pkgs = unlockedPackages..add(pkg.code);
    await _savePackages(pkgs);
    await _markNonce(payload.nonce);
    return UnlockResult.ok('Unlocked ${pkg.code}. Permanent on this device.');
  }
}

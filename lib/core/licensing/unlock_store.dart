import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:hive_flutter/hive_flutter.dart';
import 'package:uuid/uuid.dart';

/// Offline licensing + permanent device identity for Bee Seller QR unlock.
class UnlockStore {
  UnlockStore._();
  static final instance = UnlockStore._();

  static const _boxName = 'unlock';
  static const _deviceKey = 'device_id';
  static const _seenOnboardKey = 'seen_onboarding';
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
    // Prefer secure storage, fall back to Hive
    String? id = await _secure.read(key: _deviceKey);
    id ??= _box?.get(_deviceKey) as String?;
    if (id == null || id.isEmpty) {
      id = const Uuid().v4().replaceAll('-', '').substring(0, 12).toUpperCase();
      await _secure.write(key: _deviceKey, value: id);
      await _box?.put(_deviceKey, id);
    } else {
      // mirror into both stores
      await _secure.write(key: _deviceKey, value: id);
      await _box?.put(_deviceKey, id);
    }
    _deviceId = id;
    return id;
  }

  bool get isUnlocked => (_box?.get('unlocked') as bool?) ?? false;

  Future<void> setUnlocked(bool v) async => _box?.put('unlocked', v);

  bool get seenOnboarding => (_box?.get(_seenOnboardKey) as bool?) ?? false;

  Future<void> markOnboardingSeen() async =>
      _box?.put(_seenOnboardKey, true);
}

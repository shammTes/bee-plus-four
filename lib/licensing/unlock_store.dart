import 'dart:math';

import 'package:shared_preferences/shared_preferences.dart';

import 'qr_payload.dart';

/// Why a code was refused — lets the lock screen tell "camera read nothing" apart from
/// "code read but refused (reason)".
enum UnlockFail { empty, notBeeCode, badSignature, otherPhone, notHighschool, alreadyUsed }

class UnlockResult {
  const UnlockResult.ok(this.value)
      : error = null,
        reason = null,
        codeDeviceId = null;
  const UnlockResult.fail(this.error, {this.reason, this.codeDeviceId}) : value = null;
  final String? value;
  final String? error;
  final UnlockFail? reason;

  /// Device id written inside a refused code (for "this code is for another phone").
  final String? codeDeviceId;
  bool get isOk => error == null;
}

/// Permanent HIGHSCHOOL unlock, device-bound, nonce single-use. Matches Bee Seller.
class UnlockStore {
  static const _idKey = 'four_device_id_v1';
  static const _flagKey = 'four_highschool_unlocked';
  static const _nonceKey = 'four_used_nonces';

  SharedPreferences? _prefs;
  String? _deviceId;

  Future<void> init() async {
    _prefs = await SharedPreferences.getInstance();
    await deviceId();
  }

  bool get isUnlocked => _prefs?.getBool(_flagKey) ?? false;

  Future<String> deviceId() async {
    if (_deviceId != null) return _deviceId!;
    final prefs = _prefs!;
    var id = prefs.getString(_idKey);
    if (id == null || id.isEmpty) {
      id = _mint();
      await prefs.setString(_idKey, id);
    }
    _deviceId = id;
    return id;
  }

  Future<UnlockResult> applyPayload(String raw) async {
    final text = raw.trim();
    if (text.isEmpty) {
      return const UnlockResult.fail('Paste or scan the code from Bee Seller.', reason: UnlockFail.empty);
    }
    final payload = QrPayload.tryParse(text);
    if (payload == null) {
      return const UnlockResult.fail(
        'That is not a Bee Seller unlock code (it must start with BEE1|).',
        reason: UnlockFail.notBeeCode,
      );
    }
    if (!payload.signatureOk) {
      return const UnlockResult.fail(
        'The code is damaged or mistyped (signature check failed). Check every letter, or scan it again.',
        reason: UnlockFail.badSignature,
      );
    }
    final current = await deviceId();
    if (!payload.matchesDevice(current)) {
      return UnlockResult.fail(
        'This code is for another phone (${payload.deviceId}). This phone is $current — ask Bee Seller to make a code for $current.',
        reason: UnlockFail.otherPhone,
        codeDeviceId: payload.deviceId,
      );
    }
    if (!payload.isHighschool) {
      return UnlockResult.fail(
        'This code is for another Bee app (package ${payload.packageCode}), not 4. In Bee Seller tick Highschool (H).',
        reason: UnlockFail.notHighschool,
      );
    }
    final prefs = _prefs!;
    final used = prefs.getStringList(_nonceKey) ?? const <String>[];
    if (used.contains(payload.nonce)) {
      return const UnlockResult.fail('This code was already used on this phone.', reason: UnlockFail.alreadyUsed);
    }
    await prefs.setBool(_flagKey, true);
    await prefs.setStringList(_nonceKey, [...used, payload.nonce]);
    return const UnlockResult.ok('4 is unlocked on this phone.');
  }

  static String _mint() {
    const alphabet = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789';
    final r = Random.secure();
    return List.generate(12, (_) => alphabet[r.nextInt(alphabet.length)]).join();
  }
}

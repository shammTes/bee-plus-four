import 'dart:convert';
import 'dart:math';
import 'dart:typed_data';

import 'package:cryptography/cryptography.dart';

import 'format.dart';

/// Key hierarchy:
///   master key MK (per mkVersion, baked into the app / kept in the Mac Keychain)
///     └ wraps batch key BK (one per encrypt batch)          AAD "4RES-BK|batchId"
///         └ wraps content key CK (one per file)              AAD fileId
///             └ encrypts header, thumbnail and chunks; HKDF(CK) → footer HMAC key
abstract final class FourKeys {
  static final aes = AesGcm.with256bits();
  static final _rng = Random.secure();

  static Uint8List random(int n) => Uint8List.fromList(List.generate(n, (_) => _rng.nextInt(256)));

  /// Development master key (mkVersion 1). Release builds should pass their own MK
  /// (app: `--dart-define=FOUR_MK=<base64>`, CLI: `--mk`, Mac: Keychain).
  static Future<Uint8List> devMasterKey() async {
    final h = await Sha256().hash(utf8.encode('4RES-DEV-MASTER-KEY-v1-CHANGE-IN-RELEASE'));
    return Uint8List.fromList(h.bytes);
  }

  static Future<Uint8List> wrap(List<int> kek, List<int> key, List<int> aad) async {
    final box = await aes.encrypt(key, secretKey: SecretKey(kek), nonce: random(FourFormat.nonceLen), aad: aad);
    return box.concatenation();
  }

  static Future<Uint8List> unwrap(List<int> kek, List<int> wrapped, List<int> aad) async {
    try {
      final box = SecretBox.fromConcatenation(wrapped, nonceLength: FourFormat.nonceLen, macLength: FourFormat.tagLen, copy: false);
      return Uint8List.fromList(await aes.decrypt(box, secretKey: SecretKey(kek), aad: aad));
    } on SecretBoxAuthenticationError {
      throw const FourKeyException('wrong key');
    }
  }

  static List<int> batchAad(String batchId) => utf8.encode('4RES-BK|$batchId');

  static Future<Uint8List> footerKey(List<int> ck) async {
    final k = await Hkdf(hmac: Hmac.sha256(), outputLength: 32).deriveKey(secretKey: SecretKey(ck), info: utf8.encode('4RES-footer-v1'), nonce: const []);
    return Uint8List.fromList(await k.extractBytes());
  }

  /// HKDF-SHA256 helper used by the app for device keys.
  static Future<Uint8List> hkdf(List<int> ikm, List<int> salt, String info) async {
    final k = await Hkdf(hmac: Hmac.sha256(), outputLength: 32).deriveKey(secretKey: SecretKey(ikm), info: utf8.encode(info), nonce: salt);
    return Uint8List.fromList(await k.extractBytes());
  }
}

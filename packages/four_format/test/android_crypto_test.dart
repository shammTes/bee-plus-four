// Regression: on Android, cryptography_flutter routes HMAC to javax.crypto, whose SecretKeySpec throws
// "IllegalArgumentException: Empty key" for a zero-length key. HKDF-Extract with an empty salt used to hit
// exactly that (footer key), so every encrypt failed on phones. Simulate the strict platform here.
import 'dart:typed_data';

import 'package:cryptography/cryptography.dart';
import 'package:cryptography/dart.dart';
import 'package:four_format/four_format.dart';
import 'package:test/test.dart';

/// Mirrors cryptography_flutter's FlutterHmac on Android: one native call per MAC, empty key rejected.
class _StrictHmac extends Hmac {
  _StrictHmac(this.hashAlgorithm) : super.constructor();
  @override
  final HashAlgorithm hashAlgorithm;
  @override
  Future<Mac> calculateMac(List<int> bytes, {required SecretKey secretKey, List<int> nonce = const [], List<int> aad = const []}) async {
    final k = await secretKey.extractBytes();
    if (k.isEmpty) throw ArgumentError('Empty key (javax.crypto.spec.SecretKeySpec)');
    return DartHmac(hashAlgorithm).calculateMac(bytes, secretKey: SecretKey(k));
  }

  @override
  DartHmac toSync() => DartHmac(hashAlgorithm);
}

class _AndroidLike extends DartCryptography {
  @override
  Hmac hmac(HashAlgorithm hashAlgorithm) => _StrictHmac(hashAlgorithm);
}

String hex(List<int> b) => b.map((x) => x.toRadixString(16).padLeft(2, '0')).join();

void main() {
  test('platform HMAC that rejects empty keys: encrypt + decrypt + footer still work', () async {
    final saved = Cryptography.instance;
    Cryptography.instance = _AndroidLike();
    addTearDown(() => Cryptography.instance = saved);
    // sanity: the simulated platform really rejects what the old code did
    expect(() => Hkdf(hmac: Hmac.sha256(), outputLength: 32).deriveKey(secretKey: SecretKey(List.filled(32, 1)), nonce: const []), throwsArgumentError);

    final mk = await FourKeys.devMasterKey();
    final d = Uint8List.fromList(List.generate(700000, (i) => i * 13 & 0xff));
    final enc = await FourWriter.encryptBytes(d, meta: FourMeta(title: 'v', subject: 'biology', grade: 11, unit: '1', type: FourType.video, mime: 'video/mp4'), masterKey: mk, batch: FourBatch.create('b'));
    final r = await FourReader.open(BytesSource(enc), (_) async => mk, verify: true);
    expect(await r.readAll(), d);
  });

  test('HKDF with empty salt = RFC 5869 (zero salt), so older files keep verifying', () async {
    // RFC 5869 test case 3: IKM = 22 × 0x0b, salt = empty, info = empty, L = 42
    final k = await DartHkdf(hmac: DartHmac.sha256(), outputLength: 42).deriveKey(secretKey: SecretKey(List.filled(22, 0x0b)), nonce: const []);
    expect(hex(await k.extractBytes()), '8da4e775a563c18f715f802a063c5a31b8a11f5c5ee1879ec3454e5f3c738d2d9d201395faa4b61a96c8');
    final ck = List.generate(32, (i) => i);
    final zeroSalt = await DartHkdf(hmac: DartHmac.sha256(), outputLength: 32).deriveKey(secretKey: SecretKey(ck), info: 'x4RES-footer-v1'.substring(1).codeUnits, nonce: List.filled(32, 0));
    expect(await FourKeys.footerKey(ck), await zeroSalt.extractBytes());
  });

  test('wrong-size keys fail with a clear message', () async {
    final batch = FourBatch.create('b');
    for (final bad in [<int>[], List.filled(16, 1), List.filled(33, 1)]) {
      expect(
        () => FourWriter.encryptBytes(Uint8List.fromList([1, 2, 3]), meta: FourMeta(title: 't', subject: 'biology', grade: 11, unit: '1', type: FourType.pdf, mime: 'application/pdf'), masterKey: bad, batch: batch),
        throwsA(isA<FourKeyException>().having((e) => e.message, 'message', contains('master key must be 32 bytes'))),
      );
    }
    expect(() => FourKeys.footerKey([]), throwsA(isA<FourKeyException>()));
  });
}

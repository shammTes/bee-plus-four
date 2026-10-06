import 'package:flutter_test/flutter_test.dart';
import 'package:high/licensing/qr_payload.dart';
import 'package:high/licensing/unlock_store.dart';
import 'package:shared_preferences/shared_preferences.dart';

// Real payloads made with the sellers' own generator logic (tool/unlock_samples.py):
//  Kotlin Bee Seller  BEE1|dev|pkg|nonce8|tsMs|HMAC-SHA256(SHARED_SECRET)[0..12] hex
//  Flutter Bee Seller BEE1|HIGHSCHOOL|dev|nonce|HMAC-SHA256 hex
const _dev = 'QWE234RTY567';
const _kH = 'BEE1|QWE234RTY567|H|5e1f0c2a|1759741234567|bf495ccc3de2d37f7a177f9e';
const _kHK = 'BEE1|QWE234RTY567|HK|5e1f0c2b|1759741234568|daa7b9977cdcd92ab57919a5';
const _kK = 'BEE1|QWE234RTY567|K|5e1f0c2c|1759741234569|e3389e11c6249059b228604a';
const _kLower = 'BEE1|qwe234rty567|H|5e1f0c2d|1759741234570|dfa75cc5accd9ae06b1d7f9b';
const _kJH = 'BEE1|QWE234RTY567|JH|5e1f0c2e|1759741234571|d8aca40e0c1852e760d8d309';
const _f5 =
    'BEE1|HIGHSCHOOL|ABC234DEF567|0123456789ab|e55e3d2def0a3eb4d977598de639f0d48c02645f37c4226bcb84d0d24b9793d4';

void main() {
  group('QrPayload', () {
    test('parses Flutter HIGHSCHOOL payload', () {
      const raw =
          'BEE1|HIGHSCHOOL|ABC234DEF567|a1b2c3d4|b738972831c289eec5d8c64b6dce559fce371882f604adbf018ea1de5339b897';
      final p = QrPayload.tryParse(raw)!;
      expect(p.packageCode, 'HIGHSCHOOL');
      expect(p.deviceId, 'ABC234DEF567');
      expect(p.sellerLayout, isFalse);
      expect(p.isHighschool, isTrue);
      expect(p.isSignatureValid, isTrue);
      expect(p.signatureOk, isTrue);
      expect(QrPayload.tryParse(_f5)!.signatureOk, isTrue);
    });

    test('parses Kotlin Bee Seller payloads (H, HK, JH)', () {
      for (final raw in [_kH, _kHK, _kJH]) {
        final p = QrPayload.tryParse(raw)!;
        expect(p.sellerLayout, isTrue, reason: raw);
        expect(p.deviceId, _dev);
        expect(p.signatureOk, isTrue, reason: raw);
        expect(p.sellerSignatureValid(raw), isTrue);
        expect(p.isHighschool, isTrue, reason: raw);
        expect(p.encoded, raw);
      }
      const old = 'BEE1|ABC234DEF567|H|a1b2c3d4|1696000000000|4bab47f28ff8495ea2321e99';
      expect(QrPayload.tryParse(old)!.signatureOk, isTrue);
    });

    test('Junior-only / Kids-only seller codes are not highschool', () {
      const j = 'BEE1|ABC234DEF567|J|a1b2c3d4|1696000000000|f28397633d0ab515b9c19c40';
      expect(QrPayload.tryParse(j)!.isHighschool, isFalse);
      expect(QrPayload.tryParse(j)!.signatureOk, isTrue);
      expect(QrPayload.tryParse(_kK)!.isHighschool, isFalse);
      expect(QrPayload.tryParse(_kK)!.signatureOk, isTrue);
    });

    test('tolerates what real scans / pastes carry', () {
      final variants = [
        'Give this payload to the student (or encode as QR):\n$_kH\nCopy',
        '  $_kH\n',
        _kH.replaceAll('|', '%7C'),
        _kH.replaceAll('|', '｜'),
        'BEE1|QWE234RTY567|H|5e1f0c2a|17597412\n34567|bf495ccc3de2d37f7a177f9e', // wrapped line
        _kH.replaceFirst('bf495ccc3de2d37f7a177f9e', 'BF495CCC3DE2D37F7A177F9E'), // upper-case hex
        'bee1|QWE234RTY567|H|5e1f0c2a|1759741234567|bf495ccc3de2d37f7a177f9e',
        '${_kH}Copy',
      ];
      for (final v in variants) {
        final p = QrPayload.tryParse(v);
        expect(p, isNotNull, reason: v);
        expect(p!.signatureOk, isTrue, reason: v);
        expect(p.encoded, _kH, reason: v);
      }
    });

    test('device match ignores case and separators but nothing else', () {
      final p = QrPayload.tryParse(_kLower)!;
      expect(p.signatureOk, isTrue);
      expect(p.matchesDevice(_dev), isTrue);
      expect(QrPayload.tryParse(_kH)!.matchesDevice('QWE2-34RT-Y567'), isTrue);
      expect(QrPayload.tryParse(_kH)!.matchesDevice('QWE234RTY568'), isFalse);
      expect(QrPayload.tryParse(_kH)!.matchesDevice(''), isFalse);
    });

    test('rejects garbage and tampering', () {
      expect(QrPayload.tryParse('hello'), isNull);
      expect(QrPayload.tryParse('BEE1|too|short'), isNull);
      expect(QrPayload.tryParse(_kH.replaceFirst('|H|', '|J|'))!.signatureOk, isFalse);
      expect(QrPayload.tryParse(_kH.replaceFirst('QWE234', 'QWE235'))!.signatureOk, isFalse);
      expect(QrPayload.tryParse(_kH.replaceFirst('1759741234567', '1759741234568'))!.signatureOk, isFalse);
      // Old 5-field quota codes are never a student unlock.
      expect(const QrPayload(packageCode: 'WHOLESALE:5', deviceId: 'x', nonce: 'n', signature: 's').isHighschool, isFalse);
    });
  });

  group('UnlockStore', () {
    Future<UnlockStore> store(String id) async {
      SharedPreferences.setMockInitialValues({'four_device_id_v1': id});
      final s = UnlockStore();
      await s.init();
      return s;
    }

    test('unlocks with a Kotlin seller code, then refuses reuse', () async {
      final s = await store(_dev);
      expect(s.isUnlocked, isFalse);
      final r = await s.applyPayload('Give this payload to the student:\n$_kH');
      expect(r.isOk, isTrue, reason: r.error);
      expect(s.isUnlocked, isTrue);
      final again = await s.applyPayload(_kH);
      expect(again.reason, UnlockFail.alreadyUsed);
    });

    test('unlocks with a Flutter seller code', () async {
      final s = await store('ABC234DEF567');
      final r = await s.applyPayload(_f5);
      expect(r.isOk, isTrue, reason: r.error);
    });

    test('lower-case device id typed in the seller still unlocks', () async {
      final s = await store(_dev);
      expect((await s.applyPayload(_kLower)).isOk, isTrue);
    });

    test('explains each refusal', () async {
      final s = await store('ZZZ234ZZZ567');
      final other = await s.applyPayload(_kH);
      expect(other.reason, UnlockFail.otherPhone);
      expect(other.codeDeviceId, _dev);
      expect(other.error, contains('ZZZ234ZZZ567'));
      expect((await s.applyPayload('hello')).reason, UnlockFail.notBeeCode);
      expect((await s.applyPayload(_kH.replaceFirst('|H|', '|J|'))).reason, UnlockFail.badSignature);
      final s2 = await store(_dev);
      expect((await s2.applyPayload(_kK)).reason, UnlockFail.notHighschool);
      expect((await s2.applyPayload('')).reason, UnlockFail.empty);
      expect(s2.isUnlocked, isFalse);
    });
  });
}

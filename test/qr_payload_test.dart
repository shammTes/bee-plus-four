import 'package:flutter_test/flutter_test.dart';
import 'package:high/licensing/qr_payload.dart';

void main() {
  test('parses Flutter HIGHSCHOOL payload', () {
    const raw =
        'BEE1|HIGHSCHOOL|ABC234DEF567|a1b2c3d4|b738972831c289eec5d8c64b6dce559fce371882f604adbf018ea1de5339b897';
    final p = QrPayload.tryParse(raw);
    expect(p, isNotNull);
    expect(p!.packageCode, 'HIGHSCHOOL');
    expect(p.deviceId, 'ABC234DEF567');
    expect(p.sellerLayout, isFalse);
    expect(p.isHighschool, isTrue);
    expect(p.isSignatureValid, isTrue);
  });

  test('parses Kotlin Bee Seller H payload', () {
    const raw = 'BEE1|ABC234DEF567|H|a1b2c3d4|1696000000000|4bab47f28ff8495ea2321e99';
    final p = QrPayload.tryParse(raw);
    expect(p, isNotNull);
    expect(p!.packageCode, 'H');
    expect(p.deviceId, 'ABC234DEF567');
    expect(p.sellerLayout, isTrue);
    expect(p.isHighschool, isTrue);
    expect(p.sellerSignatureValid(raw), isTrue);
  });

  test('Junior-only seller code is not highschool', () {
    const raw = 'BEE1|ABC234DEF567|J|a1b2c3d4|1696000000000|f28397633d0ab515b9c19c40';
    final p = QrPayload.tryParse(raw);
    expect(p, isNotNull);
    expect(p!.isHighschool, isFalse);
    expect(p.sellerSignatureValid(raw), isTrue);
  });

  test('rejects garbage', () {
    expect(QrPayload.tryParse('hello'), isNull);
    expect(QrPayload.tryParse('BEE1|too|short'), isNull);
  });
}

// Small rolling log file (app-private) that the user can copy or share when something fails.
import 'dart:io';

import 'package:cryptography/cryptography.dart';
import 'package:cryptography/dart.dart';

import 'package:flutter/services.dart';
import 'package:four_format/four_format.dart';

const _ch = MethodChannel('four.encryptor/io');

class AppLog {
  static File? _f;
  static final _early = <String>[];
  static String device = '';

  static Future<void> init() async {
    try {
      _f = File((await _ch.invokeMethod<String>('logPath'))!);
      device = await _ch.invokeMethod<String>('deviceInfo') ?? '';
      if (await _f!.exists() && await _f!.length() > 256 * 1024) {
        final keep = (await _f!.readAsString()).split('\n');
        await _f!.writeAsString(keep.sublist(keep.length ~/ 2).join('\n'));
      }
      for (final l in _early) {
        _f!.writeAsStringSync('$l\n', mode: FileMode.append);
      }
      _early.clear();
    } catch (_) {}
  }

  static void log(String msg) {
    final line = '${DateTime.now().toIso8601String().substring(0, 19)} $msg';
    // ignore: avoid_print
    print('4enc: $line');
    final f = _f;
    if (f == null) {
      _early.add(line);
      return;
    }
    try {
      f.writeAsStringSync('$line\n', mode: FileMode.append);
    } catch (_) {}
  }

  static Future<String> read() async {
    try {
      final f = _f;
      if (f == null || !await f.exists()) return '';
      final s = await f.readAsString();
      return s.length > 60000 ? s.substring(s.length - 60000) : s;
    } catch (e) {
      return 'log unreadable: $e';
    }
  }

  static Future<void> share() async => _ch.invokeMethod('shareText', {'text': '4 Encryptor log\n$device\n\n${await read()}'});
}

/// Checks that native AES-GCM (cryptography_flutter → javax.crypto) gives exactly the pure-Dart result, incl. AAD,
/// on a 256 KiB chunk. If the plugin is missing, throws, or differs, everything switches to pure Dart (slower, correct).
/// Must run before four_format's FourKeys.aes is first used.
Future<String> cryptoSelfTest() async {
  final key = SecretKey(List.generate(32, (i) => i * 7 & 0xff));
  final nonce = List.generate(12, (i) => i + 1);
  final aad = List.generate(21, (i) => 255 - i);
  final data = List.generate(256 * 1024, (i) => i * 31 & 0xff);
  try {
    final sw = Stopwatch()..start();
    final a = await AesGcm.with256bits().encrypt(data, secretKey: key, nonce: nonce, aad: aad);
    final ms = sw.elapsedMilliseconds;
    final b = await DartAesGcm.with256bits().encrypt(data, secretKey: key, nonce: nonce, aad: aad);
    var same = a.mac.bytes.length == 16 && _eq(a.mac.bytes, b.mac.bytes) && _eq(a.cipherText, b.cipherText);
    if (same) {
      final back = await AesGcm.with256bits().decrypt(a, secretKey: key, aad: aad);
      same = _eq(back, data);
    }
    if (!same) {
      Cryptography.instance = DartCryptography.defaultInstance;
      return 'AES-GCM: native result differs from reference → using pure Dart (${Cryptography.instance.runtimeType})';
    }
    return 'AES-GCM: native OK (${AesGcm.with256bits().runtimeType}, 256 KiB in $ms ms)';
  } catch (e) {
    Cryptography.instance = DartCryptography.defaultInstance;
    return 'AES-GCM: native failed ($e) → using pure Dart';
  }
}

bool _eq(List<int> a, List<int> b) {
  if (a.length != b.length) return false;
  for (var i = 0; i < a.length; i++) {
    if (a[i] != b[i]) return false;
  }
  return true;
}

/// Set when the on-device self-test fails; the home screen shows it so nobody wastes time on a broken build.
String? selfTestError;

/// Release-mode check on the real device: encrypt 600 KB with the real master key through the exact
/// production path (native AES-GCM, HKDF/HMAC, key wrap), then decrypt and verify the footer.
Future<String> fourSelfTest(List<int> masterKey) async {
  final sw = Stopwatch()..start();
  try {
    final d = Uint8List.fromList(List.generate(600 * 1024, (i) => i * 29 & 0xff));
    final enc = await FourWriter.encryptBytes(d, meta: FourMeta(title: 'self-test', subject: 'other', grade: 0, unit: '', type: FourType.video, mime: 'video/mp4'), masterKey: masterKey, batch: FourBatch.create('selftest'));
    final r = await FourReader.open(BytesSource(enc), (_) async => masterKey, verify: true);
    final back = await r.readAll();
    if (!_eq(back, d)) throw StateError('decrypted bytes differ');
    return 'self-test OK (encrypt+decrypt 600 KB in ${sw.elapsedMilliseconds} ms)';
  } catch (e, st) {
    selfTestError = 'Self-test failed: $e';
    return 'self-test FAILED: $e\n${st.toString().split('\n').take(6).join('\n')}';
  }
}

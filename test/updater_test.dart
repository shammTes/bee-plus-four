import 'dart:convert';
import 'dart:io';

import 'package:crypto/crypto.dart';
import 'package:flutter/services.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:high/update/updater.dart';
import 'package:shared_preferences/shared_preferences.dart';

/// Local HTTP server with Range support stands in for GitHub Releases; the Android side is mocked.
void main() {
  TestWidgetsFlutterBinding.ensureInitialized();
  late HttpServer server;
  late List<int> apk;
  final ranges = <String?>[];
  var apkInfo = <String, Object?>{'package': 'com.four.student', 'versionCode': 5, 'versionName': '1.1.0', 'cert': 'aa11'};

  setUpAll(() async {
    HttpOverrides.global = null; // flutter_test fakes HttpClient with 400s; use the real one against localhost
    apk = List.generate(700000, (i) => i * 7 & 0xff);
    server = await HttpServer.bind(InternetAddress.loopbackIPv4, 0);
    server.listen((req) async {
      final r = req.response;
      if (req.uri.path == '/four-update.json') {
        r.write(jsonEncode({
          'versionCode': 5,
          'versionName': '1.1.0',
          'apk': 'http://127.0.0.1:${server.port}/universal.apk',
          'sha256': sha256.convert(apk).toString(),
          'size': apk.length,
          'cert': 'AA:11',
          'notes': 'Videos',
          'abis': {
            'arm64-v8a': {'apk': 'http://127.0.0.1:${server.port}/arm64.apk', 'sha256': sha256.convert(apk).toString(), 'size': apk.length},
          },
        }));
      } else {
        final range = req.headers.value(HttpHeaders.rangeHeader);
        ranges.add(range);
        var start = 0;
        if (range != null) {
          start = int.parse(RegExp(r'bytes=(\d+)-').firstMatch(range)!.group(1)!);
          r.statusCode = 206;
        }
        final body = apk.sublist(start);
        r.add(body);
      }
      await r.close();
    });
  });
  tearDownAll(() => server.close(force: true));

  setUp(() {
    SharedPreferences.setMockInitialValues({});
    TestDefaultBinaryMessengerBinding.instance.defaultBinaryMessenger.setMockMethodCallHandler(const MethodChannel('com.warsay.high/update'), (c) async {
      switch (c.method) {
        case 'info':
          return {'package': 'com.four.student', 'versionCode': 3, 'versionName': '1.0.2', 'cert': 'aa11', 'network': 'wifi', 'abis': ['arm64-v8a', 'armeabi-v7a']};
        case 'inspectApk':
          return apkInfo;
        case 'install':
          return 'started';
      }
      return null;
    });
  });

  Future<Updater> fresh() async {
    final u = Updater.instance
      ..available = null
      ..readyPath = null
      ..local = null
      ..step = UpdateStep.idle
      ..info = const {}
      ..urlOverride = 'http://127.0.0.1:${server.port}/four-update.json'
      ..dirOverride = await Directory.systemTemp.createTemp('upd');
    return u;
  }

  test('finds a newer version and picks this phone\'s ABI APK', () async {
    final u = await fresh();
    final m = await u.check();
    expect(m!.versionCode, 5);
    expect(m.apk, endsWith('/arm64.apk'));
    expect(m.cert, 'aa11');
  });

  test('download resumes with Range after a drop, verifies, becomes installable', () async {
    final u = await fresh();
    await u.check();
    ranges.clear();
    // an earlier attempt stopped after 300 000 bytes
    File('${u.dirOverride!.path}/four-5.apk.part').writeAsBytesSync(apk.sublist(0, 300000));
    await u.download();
    expect(u.step, UpdateStep.ready, reason: u.message);
    expect(ranges.last, startsWith('bytes='));
    expect(ranges.last, 'bytes=300000-');
    expect(File(u.readyPath!).readAsBytesSync(), apk);
    expect(await u.install(), 'started');
  });

  test('rejects an APK signed with another key', () async {
    final u = await fresh();
    apkInfo = {...apkInfo, 'cert': 'bb22'};
    await u.check();
    await u.download();
    expect(u.step, UpdateStep.failed);
    expect(u.message, contains('different key'));
    apkInfo = {...apkInfo, 'cert': 'aa11'};
  });

  test('older or same version is not offered', () async {
    final u = await fresh();
    TestDefaultBinaryMessengerBinding.instance.defaultBinaryMessenger.setMockMethodCallHandler(const MethodChannel('com.warsay.high/update'), (c) async => c.method == 'info' ? {'package': 'com.four.student', 'versionCode': 9, 'versionName': '2.0', 'cert': 'aa11', 'network': 'wifi'} : null);
    expect(await u.check(), isNull);
    expect(u.message, contains('up to date'));
  });
}

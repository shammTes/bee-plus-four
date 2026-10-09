import 'dart:io';

import 'package:flutter/services.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:high/update/update_ui.dart' show folderLabel;
import 'package:high/update/updater.dart';
import 'package:shared_preferences/shared_preferences.dart';

/// Updates come only as a file. The Android side (SAF folders, PackageManager, installer) is mocked:
/// a "document" is a uri → APK identity; importFile writes the uri into the copy so inspectApk can look it up.
void main() {
  TestWidgetsFlutterBinding.ensureInitialized();
  final messenger = TestDefaultBinaryMessengerBinding.instance.defaultBinaryMessenger;
  const upd = MethodChannel('com.warsay.high/update'), res = MethodChannel('com.warsay.high/resources');
  const resTree = 'content://com.android.externalstorage.documents/tree/primary%3AFour';
  const updTree = 'content://com.android.externalstorage.documents/tree/primary%3ASHAREit%2Fapps';

  late Map<String, Map<String, Object?>> docs; // uri → {package, versionCode, versionName, cert, tree}
  late List<String> imported, installed;
  late List<Map<Object?, Object?>> findCalls;
  late Map<String, Object?> info;
  String? picked;
  var installAnswer = 'started';

  Map<String, Object?> apk(String tree, int code, {String pkg = 'com.four.student', String cert = 'aa11'}) => {'package': pkg, 'versionCode': code, 'versionName': '1.$code', 'cert': cert, 'tree': tree};

  setUp(() async {
    SharedPreferences.setMockInitialValues({Updater.resFolderKey: resTree});
    docs = {};
    imported = [];
    installed = [];
    findCalls = [];
    picked = null;
    installAnswer = 'started';
    info = {'package': 'com.four.student', 'versionCode': 3, 'versionName': '1.3', 'cert': 'aa11', 'canInstall': true};
    final u = Updater.instance..resetForTest();
    u.dirOverride = await Directory.systemTemp.createTemp('upd');
    u.now = DateTime.now;
    messenger.setMockMethodCallHandler(upd, (c) async {
      final a = (c.arguments as Map?) ?? const {};
      switch (c.method) {
        case 'info':
          return info;
        case 'findApks': // manifest-only filter like UpdateChannel.findApks
          findCalls.add(a);
          final trees = (a['trees'] as List).cast<String>(), skip = (a['skip'] as List).cast<String>();
          return [
            for (final e in docs.entries)
              if (trees.contains(e.value['tree']) && !skip.contains('${e.key}|1000|1'))
                if (e.value['package'] != a['package'] || (e.value['versionCode'] as int) <= (a['above'] as int))
                  {'key': '${e.key}|1000|1', 'other': true, 'name': e.key}
                else
                  {'key': '${e.key}|1000|1', 'uri': e.key, 'name': e.key, 'size': 1000, 'modified': 1, 'versionCode': e.value['versionCode'], 'versionName': e.value['versionName']},
          ];
        case 'inspectApk':
          final f = File(a['path'] as String);
          if (!f.existsSync()) return null;
          final d = docs[f.readAsStringSync().trim()];
          return d == null ? null : ({...d}..remove('tree'));
        case 'pickApk':
          return picked;
        case 'install':
          installed.add(a['path'] as String);
          return installAnswer;
        case 'shareSelf':
          return {'files': 1, 'splits': 0, 'bytes': 1000, 'name': '4-1.3-3.apk'};
      }
      return null;
    });
    messenger.setMockMethodCallHandler(res, (c) async {
      final a = (c.arguments as Map?) ?? const {};
      switch (c.method) {
        case 'hasFolder':
          return a['uri'] == resTree || a['uri'] == updTree;
        case 'importFile':
          imported.add(a['uri'] as String);
          File(a['dest'] as String).writeAsStringSync((a['uri'] as String).padRight(1000));
          return 1000;
        case 'pickFolder':
          return updTree;
      }
      return null;
    });
  });

  group('verdict (package, higher versionCode, same signing cert)', () {
    final inst = {'package': 'com.four.student', 'versionCode': 3, 'cert': 'aa11'};
    test('newer 4 with the same key passes', () => expect(Updater.verdict({'package': 'com.four.student', 'versionCode': 4, 'cert': 'aa11'}, inst), isNull));
    test('another app', () => expect(Updater.verdict({'package': 'com.other', 'versionCode': 9, 'cert': 'aa11'}, inst), contains('not 4')));
    test('same or older version', () {
      expect(Updater.verdict({'package': 'com.four.student', 'versionCode': 3, 'cert': 'aa11'}, inst), contains('not newer'));
      expect(Updater.verdict({'package': 'com.four.student', 'versionCode': 1, 'cert': 'aa11'}, inst), contains('not newer'));
    });
    test('different or missing key', () {
      expect(Updater.verdict({'package': 'com.four.student', 'versionCode': 4, 'cert': 'bb22'}, inst), contains('different key'));
      expect(Updater.verdict({'package': 'com.four.student', 'versionCode': 4}, inst), contains('different key'));
    });
    test('unreadable file', () => expect(Updater.verdict(null, inst), contains('Not a valid APK')));
  });

  test('start: finds the newest valid 4 in the resources folder, copies only 4 candidates', () async {
    docs['$resTree/doc/game.apk'] = apk(resTree, 50, pkg: 'com.game');
    docs['$resTree/doc/four-old.apk'] = apk(resTree, 2);
    docs['$resTree/doc/four-5.apk'] = apk(resTree, 5);
    docs['$resTree/doc/four-7.apk'] = apk(resTree, 7);
    final u = Updater.instance;
    expect(await u.autoScan(), isTrue);
    expect(u.local!.versionCode, 7);
    expect(u.local!.from, 'your resources folder');
    expect(imported, ['$resTree/doc/four-7.apk']); // newest first; the game and older 4 are never copied
    expect(File(u.local!.path).existsSync(), isTrue);
    expect(await u.install(), 'started');
    expect(installed.single, u.local!.path);
  });

  test('wrong signing key is refused, explained, and not copied again', () async {
    docs['$resTree/doc/four-ci.apk'] = apk(resTree, 9, cert: 'ffff');
    final u = Updater.instance;
    expect(await u.autoScan(), isFalse);
    expect(u.local, isNull);
    expect(u.message, contains('different key'));
    expect(imported, hasLength(1));
    await u.autoScan(force: true);
    expect(imported, hasLength(1), reason: 'remembered by uri|size|modified');
    expect((findCalls.last['skip'] as List), contains('$resTree/doc/four-ci.apk|1000|1'));
  });

  test('other apps are remembered and skipped on the next scan', () async {
    docs['$resTree/doc/game.apk'] = apk(resTree, 50, pkg: 'com.game');
    final u = Updater.instance;
    await u.autoScan();
    await u.autoScan(force: true);
    expect((findCalls.last['skip'] as List), contains('$resTree/doc/game.apk|1000|1'));
  });

  test('start/resume scans are debounced', () async {
    final u = Updater.instance;
    var t = DateTime(2026, 10, 8, 12);
    u.now = () => t;
    await u.autoScan();
    await u.autoScan();
    expect(findCalls, hasLength(1));
    t = t.add(Updater.debounce + const Duration(seconds: 1));
    await u.autoScan();
    expect(findCalls, hasLength(2));
  });

  test('no folder chosen: nothing is listed', () async {
    SharedPreferences.setMockInitialValues({});
    expect(await Updater.instance.autoScan(), isFalse);
    expect(findCalls, isEmpty);
  });

  test('update folder (e.g. SHAREit/apps) is watched too', () async {
    docs['$updTree/doc/4.apk'] = apk(updTree, 6);
    final u = Updater.instance;
    expect(await u.pickUpdateFolder(), isTrue);
    expect(u.updateFolder, updTree);
    expect((findCalls.last['trees'] as List), [resTree, updTree]);
    expect(u.local!.versionCode, 6);
    expect(u.local!.from, 'your update folder');
  });

  test('a copy from an earlier start is re-checked, not copied again', () async {
    docs['$resTree/doc/four-5.apk'] = apk(resTree, 5);
    final u = Updater.instance;
    await u.autoScan();
    expect(imported, hasLength(1));
    u.local = null; // new process
    await u.autoScan(force: true);
    expect(u.local!.versionCode, 5);
    expect(imported, hasLength(1));
  });

  test('after the update is installed the old copy is deleted', () async {
    docs['$resTree/doc/four-5.apk'] = apk(resTree, 5);
    final u = Updater.instance;
    await u.autoScan();
    final copy = u.local!.path;
    info = {...info, 'versionCode': 5, 'versionName': '1.5'};
    await u.autoScan(force: true);
    expect(u.local, isNull);
    expect(File(copy).existsSync(), isFalse);
  });

  test('"Find update file" picker: accepts a valid file, refuses others', () async {
    final u = Updater.instance;
    expect(await u.pickFile(), ''); // cancelled
    picked = 'content://downloads/doc/1';
    docs[picked!] = apk('', 8);
    expect(await u.pickFile(), contains('Found 4 1.8'));
    expect(u.local!.from, 'the file you picked');
    u.local = null;
    picked = 'content://downloads/doc/2';
    docs[picked!] = apk('', 8, pkg: 'com.other');
    expect(await u.pickFile(), contains('not 4'));
    expect(u.local, isNull);
  });

  test('install waits for "Install unknown apps", then continues on resume', () async {
    docs['$resTree/doc/four-5.apk'] = apk(resTree, 5);
    final u = Updater.instance;
    await u.autoScan();
    installAnswer = 'permission';
    expect(await u.install(), 'permission');
    expect(u.message, contains('Install unknown apps'));
    installAnswer = 'started';
    await u.autoScan(); // resume right after Settings: not debounced
    await Future<void>.delayed(Duration.zero);
    expect(installed, hasLength(2));
  });

  test('send 4 to a friend opens the share sheet', () async {
    expect(await Updater.instance.shareSelf(), '');
  });

  test('folder labels', () {
    expect(folderLabel(updTree), 'SHAREit/apps');
    expect(folderLabel('content://com.android.externalstorage.documents/tree/primary%3A'), 'Phone storage');
  });

  test('no network: the updater has no HTTP code and release builds have no INTERNET permission', () {
    final src = File('lib/update/updater.dart').readAsStringSync();
    expect(src, isNot(contains('HttpClient')));
    expect(src, isNot(contains('http://')));
    expect(src, isNot(contains('https://')));
    expect(File('android/app/src/main/AndroidManifest.xml').readAsStringSync(), isNot(contains('android.permission.INTERNET')));
    final rel = File('android/app/src/release/AndroidManifest.xml').readAsStringSync();
    expect(rel, contains('<uses-permission android:name="android.permission.INTERNET" tools:node="remove"/>'));
  });
}

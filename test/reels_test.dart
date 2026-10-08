import 'dart:io';

import 'package:flutter/services.dart';
import 'package:flutter/widgets.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:four_format/four_format.dart';
import 'package:high/licensing/unlock_store.dart';
import 'package:high/resources/gate.dart';
import 'package:high/resources/library.dart';
import 'package:high/resources/reels_page.dart';
import 'package:shared_preferences/shared_preferences.dart';

/// The feed keeps at most 3 native players (prev / current / next) and disposes the rest.
void main() {
  TestWidgetsFlutterBinding.ensureInitialized();
  final live = <int>{};
  final calls = <String>[];
  var nextId = 1;

  testWidgets('only prev/current/next players are alive; only current plays', (tester) async {
    TestDefaultBinaryMessengerBinding.instance.defaultBinaryMessenger.setMockMethodCallHandler(const MethodChannel('com.warsay.high/video'), (c) async {
      final id = ((c.arguments as Map)['id'] as num?)?.toInt();
      calls.add('${c.method}:${id ?? ''}');
      switch (c.method) {
        case 'create':
          final n = nextId++;
          live.add(n);
          return {'id': n};
        case 'dispose':
          live.remove(id);
          return null;
        case 'state':
          return {'pos': 0, 'dur': 15000, 'playing': false, 'w': 720, 'h': 1280};
      }
      return null;
    });
    SharedPreferences.setMockInitialValues({'four_device_id_v1': 'ABC234DEF567', 'four_highschool_unlocked': true});
    FlutterSecureStorage.setMockInitialValues({});
    final reels = <ResEntry>[];
    await tester.runAsync(() async {
      final u = UnlockStore();
      await u.init();
      ResourceGate.install(u);
      final mk = await FourKeys.devMasterKey();
      final dir = await Directory.systemTemp.createTemp('reels');
      for (var i = 0; i < 5; i++) {
        final meta = FourMeta(title: 'Reel $i', subject: 'biology', grade: 11, unit: '1', type: FourType.reel, mime: 'video/mp4');
        final enc = await FourWriter.encryptBytes(Uint8List(1000), meta: meta, masterKey: mk, batch: FourBatch.create('r'));
        final f = File('${dir.path}/$i.4res')..writeAsBytesSync(enc);
        reels.add(ResEntry(id: '$i', path: f.path, meta: meta, size: 1000));
      }
    });
    await tester.pumpWidget(Directionality(textDirection: TextDirection.ltr, child: MediaQuery(data: const MediaQueryData(size: Size(400, 800)), child: ReelsPage(reels: reels))));
    Future<void> settle() async {
      for (var i = 0; i < 20; i++) {
        await tester.runAsync(() => Future<void>.delayed(const Duration(milliseconds: 30)));
        await tester.pump(const Duration(milliseconds: 50));
      }
    }

    await settle();
    expect(live.length, 2, reason: 'first page: current + next');
    await tester.drag(find.byType(PageView), const Offset(0, -600));
    await tester.pumpAndSettle(const Duration(milliseconds: 100));
    await settle();
    await tester.drag(find.byType(PageView), const Offset(0, -600));
    await tester.pumpAndSettle(const Duration(milliseconds: 100));
    await settle();
    expect(live.length, 3, reason: 'page 2: reels 1,2,3 alive, 0 disposed');
    expect(calls.where((c) => c.startsWith('dispose')).length, greaterThanOrEqualTo(1));
    expect(calls.where((c) => c.startsWith('loop')).length, greaterThanOrEqualTo(4));
    await tester.pumpWidget(const SizedBox());
    await settle();
    expect(live, isEmpty, reason: 'leaving the feed releases every player');
    ResourceLibrary.instance.toString();
  });
}

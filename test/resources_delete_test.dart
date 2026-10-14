// Delete for imported Extra resources: file removed from app storage, index entry dropped, list refreshed;
// bundled items never deleted; multi-select delete; confirm dialog wording.
import 'dart:convert';
import 'dart:io';

import 'package:flutter/widgets.dart';

import 'package:flutter/services.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:four_format/four_format.dart';
import 'package:high/high/app.dart';
import 'package:high/high/data/repository.dart';
import 'package:high/high/notes/jr/data/repository.dart';
import 'package:high/high/state/app_state.dart';
import 'package:high/high/widgets/page.dart';
import 'package:high/licensing/unlock_store.dart';
import 'package:high/resources/gate.dart';
import 'package:high/resources/library.dart';
import 'package:high/resources/resources_ui.dart';
import 'package:shared_preferences/shared_preferences.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();
  late Directory support;

  setUp(() async {
    support = await Directory.systemTemp.createTemp('4del');
    TestDefaultBinaryMessengerBinding.instance.defaultBinaryMessenger.setMockMethodCallHandler(
      const MethodChannel('plugins.flutter.io/path_provider'),
      (c) async => support.path,
    );
    SharedPreferences.setMockInitialValues({'four_device_id_v1': 'ABC234DEF567', 'four_highschool_unlocked': true, HighState.key: jsonEncode({'v': 2, 'name': 'Hana', 'theme': 'light', 'tourDone': true})});
    FlutterSecureStorage.setMockInitialValues({});
    final u = UnlockStore();
    await u.init();
    ResourceGate.install(u);
  });

  Future<File> addFile(String title, FourType type) async {
    final dir = Directory('${support.path}/resources')..createSync(recursive: true);
    final tmp = File('${dir.path}/$title.tmp');
    final sink = tmp.openWrite();
    await FourWriter.write(
      input: BytesSource(Uint8List.fromList(List.generate(5000, (i) => i & 0xff))),
      add: (b) => sink.add(b),
      meta: FourMeta(title: title, subject: 'biology', grade: 11, unit: '1', type: type, mime: type == FourType.pdf ? 'application/pdf' : 'video/mp4'),
      masterKey: await FourKeys.devMasterKey(),
      batch: FourBatch.create('t'),
    );
    await sink.close();
    final head = await tmp.openRead(0, 24).first;
    final id = head.sublist(8, 24).map((b) => b.toRadixString(16).padLeft(2, '0')).join();
    return tmp.rename('${dir.path}/$id.4res');
  }

  test('deleting removes the stored file and its index entry, and survives reload', () async {
    final a = await addFile('notes', FourType.pdf), b = await addFile('clip', FourType.video), c = await addFile('reel', FourType.reel);
    final lib = ResourceLibrary.instance;
    await lib.reload();
    expect(lib.entries, hasLength(3));
    var notified = 0;
    void l() => notified++;
    lib.addListener(l);
    final e = lib.entries.firstWhere((x) => x.meta.title == 'clip');
    expect(e.deletable, isTrue);
    await lib.remove(e);
    lib.removeListener(l);
    expect(notified, greaterThan(0));
    expect(b.existsSync(), isFalse);
    expect(a.existsSync() && c.existsSync(), isTrue);
    expect(lib.entries.map((x) => x.meta.title), unorderedEquals(['notes', 'reel']));
    await lib.reload(); // sealed index rewritten, not rebuilt with the deleted item
    expect(lib.entries.map((x) => x.meta.title), unorderedEquals(['notes', 'reel']));
  });

  test('select several: removeMany deletes all chosen in one go', () async {
    await addFile('p1', FourType.pdf);
    await addFile('p2', FourType.pdf);
    await addFile('keep', FourType.video);
    final lib = ResourceLibrary.instance;
    await lib.reload();
    final n = await lib.removeMany(lib.entries.where((x) => x.meta.title.startsWith('p')));
    expect(n, 2);
    expect(lib.entries.single.meta.title, 'keep');
    expect(Directory('${support.path}/resources').listSync().where((f) => f.path.endsWith('.4res')), hasLength(1));
  });

  test('bundled items and files outside app storage are never deleted', () async {
    final outside = File('${support.path}/outside.4res')..writeAsStringSync('x');
    final lib = ResourceLibrary.instance;
    await lib.reload();
    final meta = FourMeta(title: 'b', subject: '', grade: 0, unit: '', type: FourType.pdf, mime: 'application/pdf');
    final bundled = ResEntry(id: 'b', path: 'assets/resources/b.4pdf', meta: meta, size: 1);
    expect(bundled.deletable, isFalse);
    expect(await lib.removeMany([bundled, ResEntry(id: 'o', path: outside.path, meta: meta, size: 1)]), 0);
    expect(outside.existsSync(), isTrue);
  });

  testWidgets('trash icon → plain confirm → file gone and list refreshed; Cancel keeps it', (t) async {
    HighState.tickStudy = false;
    t.view.physicalSize = const Size(800, 1400);
    t.view.devicePixelRatio = 1;
    addTearDown(t.view.reset);
    final lib = ResourceLibrary.instance;
    final repo = ExamRepo(useIsolate: false), notes = NotesRepo(useIsolate: false);
    late HighState s;
    await t.runAsync(() async {
      await addFile('one', FourType.pdf);
      await addFile('two', FourType.video);
      await lib.reload();
      await repo.init();
      await notes.init();
      s = HighState(repo, await SharedPreferences.getInstance(), notes);
      await s.load();
    });
    await t.pumpWidget(HighApp(state: s));
    await t.pumpAndSettle();
    HighNav.of(t.element(find.byType(PageShell).first)).push(const ResourcesPage());
    await t.pumpAndSettle();
    expect(find.text('2 files'), findsOneWidget);
    final del = find.byKey(ValueKey('delete-${lib.entries.first.id}'));
    expect(find.bySemanticsLabel('Delete'), findsNWidgets(2));

    await t.tap(del);
    await t.pumpAndSettle();
    expect(find.text('Delete this file?'), findsOneWidget);
    await t.tap(find.text('Cancel'));
    await t.pumpAndSettle();
    expect(lib.entries, hasLength(2));

    final gone = lib.entries.first;
    await t.tap(del);
    await t.pumpAndSettle();
    await t.tap(find.byKey(const ValueKey('confirm-delete')));
    for (var i = 0; i < 40 && find.text('1 file').evaluate().isEmpty; i++) {
      await t.pump(const Duration(milliseconds: 50));
      await t.runAsync(() => Future<void>.delayed(const Duration(milliseconds: 50)));
    }
    await t.pumpAndSettle();
    expect(File(gone.path).existsSync(), isFalse);
    expect(find.text('1 file'), findsOneWidget);
    await t.pump(const Duration(seconds: 5));
  });
}

// TEMP (not committed): sample 360 px shots of Agriculture cards: every table renders on a narrow low-end phone (320 logical px wide) without
// overflow, cells are plain text (no $$ display maths, no garbled "%%"), every row has one cell per column.
//   flutter test test/geo_tables_test.dart
//   GEO_SHOTS=/workspace/shots/geo flutter test test/geo_tables_test.dart   # also writes one PNG per table
import 'dart:convert';
import 'dart:io';
import 'dart:ui' as ui;

import 'package:flutter/rendering.dart';
import 'package:flutter/widgets.dart';
import 'package:flutter/services.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:high/high/notes/jr/notes/svg_prep.dart';
import 'package:high/high/app.dart';
import 'package:high/high/data/repository.dart';
import 'package:high/high/notes/jr/data/notes_models.dart';
import 'package:high/high/notes/jr/data/repository.dart';
import 'package:high/high/notes/jr/notes/cards.dart';
import 'package:high/high/state/app_state.dart';
import 'package:high/high/widgets/page.dart';
import 'package:shared_preferences/shared_preferences.dart';

import 'helpers.dart';

final _shot = GlobalKey();

class _One extends StatelessWidget {
  const _One(this.ctx, this.card);
  final UnitCtx ctx;
  final NoteCard card;
  @override
  Widget build(BuildContext context) => PageShell(
    top: TopBar(title: 'Notes', onBack: HighNav.of(context).back, tab: false),
    body: SingleChildScrollView(
      padding: const EdgeInsets.all(12),
      child: RepaintBoundary(
        key: _shot,
        child: NoteCardView(key: const ValueKey('card'), ctx: ctx, card: card, ckey: 'agri-shot', compact: true),
      ),
    ),
  );
}

void main() {
  HighState.tickStudy = false;
  highDecorAnimations = false;
  highNow = () => DateTime(2026, 9, 29, 10);
  final repo = ExamRepo(useIsolate: false), notes = NotesRepo(useIsolate: false);
  final dir = Platform.environment['AGRI_SHOTS'] ?? '/workspace/shots/agri';
  final want = (Platform.environment['AGRI_IDS'] ?? '').split(',').where((s) => s.isNotEmpty).toSet();
  final grade = Platform.environment['AGRI_GRADE'] ?? '11';
  setUpAll(() async {
    await loadFonts();
    await repo.init();
    await notes.init();
    final svgs = [for (final f in Directory('assets/high/notes/notes/svg').listSync(recursive: true)) if (f.path.endsWith('.svg') && f.path.contains('agri_')) f.path.substring('assets/high/notes/notes/'.length)];
    await SvgStore.preload(rootBundle, [for (final v in svgs) '${NotesRepo.base}/$v']);
  });
  testWidgets('agri shots', (t) async {
    final raw = jsonDecode(File('assets/high/notes/notes/agriculture_$grade.json').readAsStringSync()) as Map<String, dynamic>;
    final book = NotesBook.fromJson(raw, 'agriculture_$grade.json');
    t.view.physicalSize = const Size(720, 3200);
    t.view.devicePixelRatio = 2;
    addTearDown(t.view.reset);
    SharedPreferences.setMockInitialValues({HighState.key: jsonEncode({'v': 2, 'name': 'Hana', 'theme': 'light'})});
    final s = HighState(repo, await SharedPreferences.getInstance(), notes);
    await s.load();
    await t.pumpWidget(HighApp(state: s));
    await t.pumpAndSettle();
    final nav = HighNav.of(t.element(find.byType(PageShell).first));
    var n = 0;
    for (final (ui_, u) in book.units.indexed) {
      for (final (li, l) in u.lessons.indexed) {
        for (final (ci, c) in l.cards.indexed) {
          final id = (((raw['units'] as List)[ui_]['lessons'] as List)[li]['cards'] as List)[ci]['id'] as String;
          if (!want.contains(id)) continue;
          n++;
          nav.push(_One(UnitCtx(u, 'test', (svg) => '${NotesRepo.base}/$svg'), c));
          for (var i = 0; i < 30; i++) {
            await t.runAsync(() => Future<void>.delayed(const Duration(milliseconds: 80)));
            await t.pump(const Duration(milliseconds: 100));
          }
          await t.pumpAndSettle();
          expect(t.takeException(), isNull, reason: id);
          final ro = t.renderObject<RenderRepaintBoundary>(find.byKey(_shot));
          await t.runAsync(() async {
            final img = await ro.toImage(pixelRatio: 2);
            final bd = await img.toByteData(format: ui.ImageByteFormat.png);
            Directory(dir).createSync(recursive: true);
            File('$dir/$id.png').writeAsBytesSync(bd!.buffer.asUint8List());
          });
          nav.back();
          await t.pumpAndSettle();
        }
      }
    }
    expect(n, want.length);
  });
}

// Geography table cards: every table renders on a narrow low-end phone (320 logical px wide) without
// overflow, cells are plain text (no $$ display maths, no garbled "%%"), every row has one cell per column.
//   flutter test test/geo_tables_test.dart
//   GEO_SHOTS=/workspace/shots/geo flutter test test/geo_tables_test.dart   # also writes one PNG per table
import 'dart:convert';
import 'dart:io';
import 'dart:ui' as ui;

import 'package:flutter/rendering.dart';
import 'package:flutter/widgets.dart';
import 'package:flutter_test/flutter_test.dart';
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
        child: NoteCardView(key: const ValueKey('card'), ctx: ctx, card: card, ckey: 'geo-table', compact: true),
      ),
    ),
  );
}

void main() {
  HighState.tickStudy = false;
  highDecorAnimations = false;
  highNow = () => DateTime(2026, 9, 29, 10);
  final repo = ExamRepo(useIsolate: false), notes = NotesRepo(useIsolate: false);
  final shots = Platform.environment['GEO_SHOTS'];
  setUpAll(() async {
    await loadFonts();
    await repo.init();
    await notes.init();
  });

  final books = {
    for (final g in [9, 10, 11, 12])
      g: NotesBook.fromJson(
        jsonDecode(File('assets/high/notes/notes/geography_$g.json').readAsStringSync()),
        'geography_$g.json',
      ),
  };

  test('geography table cells are well-formed plain text', () {
    for (final b in books.values) {
      for (final u in b.units) {
        for (final l in u.lessons) {
          for (final c in l.cards.whereType<TableCard>()) {
            expect(c.head, isNotEmpty, reason: '${l.id} ${c.title}');
            for (final h in c.head) {
              expect(h.contains(r'$$'), isFalse, reason: '${l.id} head "$h"');
            }
            for (final r in c.rows) {
              expect(r.length, c.head.length, reason: '${l.id} ${c.title} row $r');
              for (final x in r) {
                expect(x.trim(), isNotEmpty, reason: '${l.id} ${c.title} empty cell in $r');
                expect(x.contains(r'$$'), isFalse, reason: '${l.id} ${c.title} cell "$x"');
                expect(x.contains('%%'), isFalse, reason: '${l.id} ${c.title} cell "$x"');
              }
            }
          }
        }
      }
    }
  });

  // renders every Geography table card at [width] logical px; with [dir] set, writes one PNG per table
  Future<int> renderAll(WidgetTester t, double width, String? dir) async {
    t.view.physicalSize = Size(width * 2, 2400);
    t.view.devicePixelRatio = 2;
    addTearDown(t.view.reset);
    SharedPreferences.setMockInitialValues({
      HighState.key: jsonEncode({'v': 2, 'name': 'Hana', 'theme': 'light'}),
    });
    final s = HighState(repo, await SharedPreferences.getInstance(), notes);
    await s.load();
    await t.pumpWidget(HighApp(state: s));
    await t.pumpAndSettle();
    final nav = HighNav.of(t.element(find.byType(PageShell).first));
    var n = 0;
    for (final b in books.values) {
      for (final u in b.units) {
        for (final l in u.lessons) {
          for (final (k, c) in l.cards.whereType<TableCard>().indexed) {
            n++;
            nav.push(_One(UnitCtx(u, 'test', (svg) => '${NotesRepo.base}/$svg'), c));
            await t.pumpAndSettle();
            expect(t.takeException(), isNull, reason: '${l.id} ${c.title}');
            if (dir != null) {
              final ro = t.renderObject<RenderRepaintBoundary>(find.byKey(_shot));
              await t.runAsync(() async {
                final img = await ro.toImage(pixelRatio: 2);
                final bd = await img.toByteData(format: ui.ImageByteFormat.png);
                Directory(dir).createSync(recursive: true);
                File('$dir/${l.id}_table${k + 1}.png').writeAsBytesSync(bd!.buffer.asUint8List());
              });
            }
            nav.back();
            await t.pumpAndSettle();
          }
        }
      }
    }
    return n;
  }

  // a narrow low-end phone: wide tables must scroll sideways, never overflow
  testWidgets('every geography table renders at 320 px without overflow', (t) async {
    expect(await renderAll(t, 320, shots), greaterThan(20));
  });

  testWidgets('every geography table renders at 720 px (tablet / landscape) without overflow', (t) async {
    expect(await renderAll(t, 720, shots == null ? null : '$shots/wide'), greaterThan(20));
  });
}

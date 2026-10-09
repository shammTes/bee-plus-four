// Notes table cards on narrow phones (320–360 logical px): nothing overflows, wide tables scroll sideways with the first
// column frozen, and the accounting layouts (journal, ledger, statement, T-account) render.
//   flutter test test/notes_table_test.dart
//   BIZ_SHOTS=/workspace/shots/biz flutter test test/notes_table_test.dart   # also writes the PNG renders
import 'dart:convert';
import 'dart:io';
import 'dart:ui' as ui;

import 'package:flutter/rendering.dart';
import 'package:flutter/widgets.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:high/high/app.dart';
import 'package:high/high/data/repository.dart';
import 'package:high/high/notes/jr/data/json_util.dart';
import 'package:high/high/notes/jr/data/notes_models.dart';
import 'package:high/high/notes/jr/data/repository.dart';
import 'package:high/high/notes/jr/notes/cards.dart';
import 'package:high/high/notes/jr/notes/ntable.dart';
import 'package:high/high/state/app_state.dart';
import 'package:high/high/widgets/page.dart';
import 'package:shared_preferences/shared_preferences.dart';

import 'helpers.dart';

final _shot = GlobalKey();

class _Cards extends StatelessWidget {
  const _Cards(this.ctx, this.cards);
  final UnitCtx ctx;
  final List<NoteCard> cards;
  @override
  Widget build(BuildContext context) => PageShell(
    top: TopBar(title: 'Notes', onBack: HighNav.of(context).back, tab: false),
    body: SingleChildScrollView(
      padding: const EdgeInsets.all(12),
      child: RepaintBoundary(
        key: _shot,
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            for (final (i, c) in cards.indexed)
              Padding(
                padding: const EdgeInsets.only(bottom: 14),
                child: NoteCardView(key: ValueKey('card$i'), ctx: ctx, card: c, ckey: 'table-test-$i', compact: true),
              ),
          ],
        ),
      ),
    ),
  );
}

NoteCard _card(Map<String, dynamic> m) => NoteCard.fromJ(J({'type': 'table', 'page': 1, 'title': 'T', ...m}, 't'));

void main() {
  HighState.tickStudy = false;
  highDecorAnimations = false;
  highNow = () => DateTime(2026, 9, 29, 10);
  final repo = ExamRepo(useIsolate: false), notes = NotesRepo(useIsolate: false);
  final shots = Platform.environment['BIZ_SHOTS'];
  setUpAll(() async {
    await loadFonts();
    await repo.init();
    await notes.init();
  });

  final books = <String, NotesBook>{
    for (final f in Directory('assets/high/notes/notes').listSync().whereType<File>())
      if (f.path.endsWith('.json') && !f.path.contains('index') && !f.path.split('/').last.startsWith('unit_'))
        f.path.split('/').last.replaceAll('.json', ''): NotesBook.fromJson(jsonDecode(f.readAsStringSync()), f.path),
  };
  final anyUnit = books['business_economics_10']!.units.first;
  UnitCtx ctxOf(Unit u) => UnitCtx(u, 'test', (svg) => '${NotesRepo.base}/$svg');

  Future<HighNav> open(WidgetTester t, double width, {bool dark = false, double height = 2400}) async {
    t.view.physicalSize = Size(width * 2, height * 2);
    t.view.devicePixelRatio = 2;
    addTearDown(t.view.reset);
    SharedPreferences.setMockInitialValues({
      HighState.key: jsonEncode({'v': 2, 'name': 'Hana', 'theme': dark ? 'dark' : 'light'}),
    });
    final s = HighState(repo, await SharedPreferences.getInstance(), notes);
    await s.load();
    s.skipTour();
    await t.pumpWidget(HighApp(state: s));
    await t.pumpAndSettle();
    return HighNav.of(t.element(find.byType(PageShell).first));
  }

  Future<void> save(WidgetTester t, String name) async {
    if (shots == null) return;
    final ro = t.renderObject<RenderRepaintBoundary>(find.byKey(_shot));
    await t.runAsync(() async {
      final img = await ro.toImage(pixelRatio: 2.5);
      final bd = await img.toByteData(format: ui.ImageByteFormat.png);
      Directory(shots).createSync(recursive: true);
      File('$shots/$name.png').writeAsBytesSync(bd!.buffer.asUint8List());
    });
  }

  final wide = _card({
    'title': 'Wide',
    'head': ['Country', 'Capital city', 'Main exports', 'Population (millions)', 'Area (km²)', 'Climate'],
    'rows': [
      for (var i = 0; i < 6; i++)
        ['**Warm-Season Grains $i**', 'Asmara', 'Gold, copper, zinc and livestock', '${3 + i}.6', '117,600', 'Hot desert along the coast, cooler highlands'],
    ],
  });

  for (final w in [320.0, 360.0]) {
    testWidgets('a wide table at $w px scrolls sideways with the first column frozen', (t) async {
      final nav = await open(t, w);
      nav.push(_Cards(ctxOf(anyUnit), [wide]));
      await t.pumpAndSettle();
      expect(t.takeException(), isNull);
      final grid = find.byType(GridView2);
      expect(grid, findsOneWidget);
      final scroller = find.ancestor(of: grid, matching: find.byType(Scrollable)).first;
      expect(scroller, findsOneWidget, reason: 'too wide for $w px, so it must scroll');
      final gridBox = t.renderObject<RenderNoteGrid>(grid);
      final card = t.getRect(find.byKey(const ValueKey('card0')));
      expect(t.getRect(grid).right, lessThanOrEqualTo(card.right + .5), reason: 'the grid stays inside the card');
      expect(gridBox.maxScroll, greaterThan(0));

      await save(t, '_wide_$w');
      Offset at(String s) => t.getTopLeft(find.textContaining(s, findRichText: true).first);
      final frozen0 = at('Warm-Season'), climate0 = at('Climate');
      await t.drag(scroller, const Offset(-2000, 0));
      await t.pumpAndSettle();
      expect(t.takeException(), isNull);
      expect(at('Warm-Season'), frozen0, reason: 'first column is frozen');
      expect(at('Climate').dx, lessThan(climate0.dx - 50), reason: 'the rest scrolled');
      expect(gridBox.scroll, closeTo(gridBox.maxScroll, .5));
      // the last column is now fully visible inside the grid
      expect(t.getRect(find.textContaining('Climate', findRichText: true).first).right, lessThanOrEqualTo(t.getRect(grid).right + .5));
      // bold words are never broken mid-word (each **key word** is one box: one line high)
      final word = find.text('Warm-Season').first;
      final lineH = t.getSize(find.text('Asmara').first).height;
      expect(t.getSize(word).height, lessThanOrEqualTo(lineH + 1));
    });
  }

  testWidgets('header cells render **bold** and \$maths\$ (no raw markup)', (t) async {
    final nav = await open(t, 360);
    nav.push(
      _Cards(ctxOf(anyUnit), [
        _card({
          'head': ['**Gas**', r'Formula $\mathrm{CO_2}$'],
          'rows': [
            ['Carbon dioxide', r'$\mathrm{CO_2}$'],
          ],
        }),
      ]),
    );
    await t.pumpAndSettle();
    expect(t.takeException(), isNull);
    expect(find.textContaining('**', findRichText: true), findsNothing);
    expect(find.textContaining(r'$', findRichText: true), findsNothing);
  });

  testWidgets('money columns are right-aligned, grouped, with total rules', (t) async {
    final nav = await open(t, 340);
    nav.push(
      _Cards(ctxOf(anyUnit), [
        _card({
          'kind': 'statement',
          'head': ['Account Title', 'Debit', 'Credit'],
          'rows': [
            ['Cash', '1105000.00', ''],
            ['Capital', '', '1,105,000.00'],
            ['Total', '1,105,000.00', '1,105,000.00'],
          ],
        }),
      ]),
    );
    await t.pumpAndSettle();
    expect(t.takeException(), isNull);
    expect(find.text('1,105,000.00'), findsNWidgets(4)); // the ungrouped figure is grouped
    final grid = t.getRect(find.byType(GridView2));
    final a = t.getRect(find.text('1,105,000.00').first);
    expect(grid.contains(a.topLeft) && grid.contains(a.bottomRight - const Offset(.1, .1)), isTrue);
    expect(t.getRect(find.byType(GridView2)).width, lessThanOrEqualTo(340));
  });

  testWidgets('T-account: Dr left, Cr right, totals on both sides', (t) async {
    final nav = await open(t, 320);
    nav.push(
      _Cards(ctxOf(anyUnit), [
        _card({
          'kind': 't_account',
          'head': ['Date', 'Particulars', 'Nfa', 'Date', 'Particulars', 'Nfa'],
          'rows': [
            ['Cash', '11', '', '', '', ''],
            ['Sept. 1', 'Balance b/d', '145,000', 'Sept. 5', 'Office Equipment', '45,000'],
            ['Sept. 2', 'Capital', '900,000', 'Sept. 30', 'Balance c/d', '1,000,000'],
            ['', '', '1,045,000', '', '', '1,045,000'],
            ['Oct. 1', 'Balance b/d', '1,000,000', '', '', ''],
          ],
          'marks': ['head', '', '', 'final', ''],
        }),
      ]),
    );
    await t.pumpAndSettle();
    expect(t.takeException(), isNull);
    final dr = t.getCenter(find.text('Dr')), cr = t.getCenter(find.text('Cr'));
    expect(dr.dx, lessThan(cr.dx));
    expect(t.getCenter(find.textContaining('Office Equipment', findRichText: true)).dx, greaterThan(t.getCenter(find.text('145,000')).dx));
    expect(find.text('1,045,000'), findsNWidgets(2));
    expect(t.getTopLeft(find.text('1,045,000').first).dy, t.getTopLeft(find.text('1,045,000').last).dy);
  });

  // every table card of every subject, at the narrowest phone width
  testWidgets('every notes table renders at 320 px without overflow', (t) async {
    final nav = await open(t, 320);
    var n = 0;
    for (final b in books.values) {
      for (final u in b.units) {
        final cards = [for (final l in u.lessons) ...l.cards.whereType<TableCard>()];
        for (var i = 0; i < cards.length; i += 12) {
          final chunk = cards.sublist(i, (i + 12).clamp(0, cards.length));
          n += chunk.length;
          nav.push(_Cards(ctxOf(u), chunk));
          await t.pumpAndSettle();
          final ex = t.takeException();
          if (ex != null) debugPrint('EXC $ex ${ex is Error ? ex.stackTrace : ''}');
          expect(ex, isNull, reason: '${u.id} tables ${i + 1}..');
          // every grid stays inside its card (wide ones scroll)
          for (final g in t.renderObjectList<RenderNoteGrid>(find.byType(GridView2))) {
            expect(g.size.width, lessThanOrEqualTo(320), reason: u.id);
          }
          nav.back();
          await t.pumpAndSettle();
        }
      }
    }
    expect(n, greaterThan(500));
  });
}

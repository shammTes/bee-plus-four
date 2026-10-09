// Business tables (G10–G12) on a 360 px phone: how many still need sideways scrolling, and before/after renders.
//   flutter test test/biz_tables_test.dart
//   BIZ2_SHOTS=/workspace/shots/biz2 BIZ2_PREFIX=after_ flutter test test/biz_tables_test.dart   # PNG renders
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
                child: NoteCardView(key: ValueKey('card$i'), ctx: ctx, card: c, ckey: 'biz-test-$i', compact: true),
              ),
          ],
        ),
      ),
    ),
  );
}

void main() {
  HighState.tickStudy = false;
  highDecorAnimations = false;
  highNow = () => DateTime(2026, 9, 29, 10);
  final repo = ExamRepo(useIsolate: false), notes = NotesRepo(useIsolate: false);
  final shots = Platform.environment['BIZ2_SHOTS'];
  final prefix = Platform.environment['BIZ2_PREFIX'] ?? '';
  setUpAll(() async {
    await loadFonts();
    await repo.init();
    await notes.init();
  });

  // every Business table card, with its id
  final raw = <(String, Map<String, dynamic>)>[];
  for (final g in ['10', '11', '12']) {
    final d = jsonDecode(File('assets/high/notes/notes/business_economics_$g.json').readAsStringSync()) as Map<String, dynamic>;
    for (final u in d['units'] as List) {
      for (final l in u['lessons'] as List) {
        for (final c in l['cards'] as List) {
          if (c['type'] == 'table') raw.add((c['id'] as String, c as Map<String, dynamic>));
        }
      }
    }
  }
  final byId = {for (final (id, m) in raw) id: m};
  NoteCard card(String id) => NoteCard.fromJ(J(byId[id]!, id));
  final book = NotesBook.fromJson(jsonDecode(File('assets/high/notes/notes/business_economics_10.json').readAsStringSync()), 'be10');
  UnitCtx ctx() => UnitCtx(book.units.first, 'test', (svg) => '${NotesRepo.base}/$svg');

  Future<HighNav> open(WidgetTester t, double width, {bool dark = false}) async {
    t.view.physicalSize = Size(width * 2, 2400 * 2);
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
      File('$shots/$prefix$name.png').writeAsBytesSync(bd!.buffer.asUint8List());
    });
  }

  const sample = <(String, String, bool)>[
    ('be10-u1-tbo1', 'comparison_forms', false),
    ('be11-u2-tblE1', 'comparison_journals', false),
    ('be10-u1-tbo2', 'adv_disadv', false),
    ('be10-u2-tblE1', 'term_list', false),
    ('be10-u3-bk024', 'journal', false),
    ('be10-u3-bk046', 'cash_journal', false),
    ('be10-u3-bk081', 't_account', false),
    ('be11-u2-bk061', 'statement', false),
    ('be10-u3-bk073', 'worksheet', false),
    ('be10-u1-tbo1', 'comparison_forms_dark', true),
    ('be10-u3-bk028', 'ledger', false),
    ('be11-u2-bk058', 'worksheet_partial', false),
    ('be10-u3-bk064', 'trial_balance_dark', true),
    ('be10-u3-tb12-t1', 'cards', false),
  ];
  for (final (id, name, dark) in sample) {
    testWidgets('render $name ($id) at 360 px', (t) async {
      if (!byId.containsKey(id)) return;
      final nav = await open(t, 360, dark: dark);
      nav.push(_Cards(ctx(), [card(id)]));
      await t.pumpAndSettle();
      expect(t.takeException(), isNull);
      await save(t, name);
    });
  }

  testWidgets('worksheet sections: the toggle switches column groups', (t) async {
    final nav = await open(t, 360);
    nav.push(_Cards(ctx(), [card('be10-u3-bk073')]));
    await t.pumpAndSettle();
    expect(find.text('Adjustments'), findsOneWidget);
    expect(find.text('17,833'), findsNothing);
    await t.tap(find.text('Adjustments'));
    await t.pumpAndSettle();
    expect(t.takeException(), isNull);
    expect(find.text('17,833'), findsNWidgets(2));
    await t.tap(find.text('All'));
    await t.pumpAndSettle();
    expect(t.renderObject<RenderNoteGrid>(find.byType(GridView2)).maxScroll, greaterThan(0), reason: '"All" keeps the full worksheet (scrolls)');
  });

  testWidgets('compare / pros-cons / entries layouts render their parts', (t) async {
    final nav = await open(t, 360);
    nav.push(_Cards(ctx(), [card('be10-u1-tbo1'), card('be10-u1-tbo2'), card('be10-u3-bk046')]));
    await t.pumpAndSettle();
    expect(t.takeException(), isNull);
    expect(find.byType(GridView2), findsNothing);
    // compare: one card per form with the row labels as mini-headings
    expect(find.textContaining('Life span', findRichText: true), findsNWidgets(3));
    // pros / cons: 10 advantages and 10 disadvantages, each with its painted mark
    expect(find.textContaining('Limited growth', findRichText: true), findsOneWidget);
    expect(find.byWidgetPredicate((w) => w is CustomPaint && w.painter.runtimeType.toString() == '_MarkPainter'), findsNWidgets(20));
    // entries: the cash journal's figures as labelled chips
    expect(find.text('Fares Earned Cr'), findsNWidgets(2));
    expect(find.text('1,105,000.00'), findsOneWidget);
  });

  // which Business tables still need sideways scrolling at 360 px
  testWidgets('Business tables at 360 px: no sideways scrolling for text tables', (t) async {
    final nav = await open(t, 360);
    final scrolls = <String>[];
    final layouts = <String, int>{};
    final alt = <String>[];
    var n = 0;
    for (var i = 0; i < raw.length; i += 10) {
      final chunk = raw.sublist(i, (i + 10).clamp(0, raw.length));
      nav.push(_Cards(ctx(), [for (final (id, _) in chunk) card(id)]));
      await t.pumpAndSettle();
      expect(t.takeException(), isNull);
      for (final (k, (id, _)) in chunk.indexed) {
        final grids = t.renderObjectList<RenderNoteGrid>(find.descendant(of: find.byKey(ValueKey('card$k')), matching: find.byType(GridView2)));
        if (grids.any((g) => g.maxScroll > .5)) scrolls.add(id);
        const names = {'_TAccounts': 't_account', '_ProsCons': 'proscons', '_Compare': 'compare', '_RowCards': 'cards', '_Terms': 'terms', '_Sections': 'sections', '_Entries': 'entries'};
        final found = find
            .descendant(of: find.byKey(ValueKey('card$k')), matching: find.byWidgetPredicate((w) => names.containsKey(w.runtimeType.toString())))
            .evaluate()
            .map((e) => names[e.widget.runtimeType.toString()]!)
            .firstOrNull;
        final kind = byId[id]!['kind'] as String? ?? 'table';
        final lay = found ?? (kind == 'table' ? 'grid' : '$kind grid');
        layouts[lay] = (layouts[lay] ?? 0) + 1;
        if (lay == 'entries' || lay == 'sections') alt.add('$lay:$id');
      }
      n += chunk.length;
      nav.back();
      await t.pumpAndSettle();
    }
    bool isText(String id) {
      final k = byId[id]!['kind'] as String?;
      return k == null || k == 'table';
    }

    final text = scrolls.where(isText).toList(), nums = scrolls.where((s) => !isText(s)).toList();
    debugPrint('BIZ360 tables=$n scroll=${scrolls.length} text=${text.length} number=${nums.length}');
    debugPrint('BIZ360 text: ${text.join(' ')}');
    debugPrint('BIZ360 layouts: $layouts');
    debugPrint('BIZ360 alt: ${alt.join(' ')}');
    debugPrint('BIZ360 number: ${nums.join(' ')}');
    File('build/biz360.json').writeAsStringSync(jsonEncode({'tables': n, 'text': text, 'number': nums, 'layouts': layouts}));
    expect(text, isEmpty, reason: 'text tables must not scroll sideways at 360 px');
  });
}

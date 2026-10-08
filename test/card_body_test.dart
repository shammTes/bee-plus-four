// Table and step-by-step (steps) cards show their `body` note under the table / figure, like text cards do.
import 'dart:convert';
import 'dart:io';

import 'package:flutter/widgets.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:high/high/app.dart';
import 'package:high/high/data/repository.dart';
import 'package:high/high/notes/jr/data/json_util.dart';
import 'package:high/high/notes/jr/data/notes_models.dart';
import 'package:high/high/notes/jr/data/repository.dart';
import 'package:high/high/notes/jr/notes/cards.dart';
import 'package:high/high/notes/jr/notes/rich.dart';
import 'package:high/high/state/app_state.dart';
import 'package:high/high/widgets/page.dart';
import 'package:shared_preferences/shared_preferences.dart';

import 'helpers.dart';

class _Cards extends StatelessWidget {
  const _Cards(this.ctx, this.cards);
  final UnitCtx ctx;
  final List<NoteCard> cards;
  @override
  Widget build(BuildContext context) => PageShell(
    top: TopBar(title: 'Cards', onBack: HighNav.of(context).back, tab: false),
    // a plain column (not a lazy list) so every card is built and can be checked
    body: SingleChildScrollView(
      padding: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          for (final (i, c) in cards.indexed)
            Padding(
              padding: const EdgeInsets.only(bottom: 16),
              child: NoteCardView(key: ValueKey('card$i'), ctx: ctx, card: c, ckey: 'body-test-$i', compact: true),
            ),
        ],
      ),
    ),
  );
}

void main() {
  HighState.tickStudy = false;
  highDecorAnimations = false;
  highNow = () => DateTime(2026, 9, 29, 10);
  final repo = ExamRepo(useIsolate: false), notes = NotesRepo(useIsolate: false);
  setUpAll(() async {
    await loadFonts();
    await repo.init();
    await notes.init();
  });

  // every notes book on disk (unit_<id>.json files replace a unit, as in the app)
  final dir = Directory('assets/high/notes/notes');
  final books = <String, NotesBook>{
    for (final f in dir.listSync().whereType<File>())
      if (f.path.endsWith('.json') && !f.path.contains('index') && !f.path.split('/').last.startsWith('unit_'))
        f.path.split('/').last.replaceAll('.json', ''): NotesBook.fromJson(jsonDecode(f.readAsStringSync()), f.path),
  };
  final bio9 = books['biology_9']!.unit('bio9-u2')!;
  UnitCtx ctxOf(Unit u) => UnitCtx(u, 'test', (svg) => '${NotesRepo.base}/$svg');

  Future<HighNav> open(WidgetTester t) async {
    t.view.physicalSize = const Size(800, 1400);
    t.view.devicePixelRatio = 1;
    addTearDown(t.view.reset);
    SharedPreferences.setMockInitialValues({
      HighState.key: jsonEncode({'v': 2, 'name': 'Hana', 'theme': 'light'}),
    });
    final s = HighState(repo, await SharedPreferences.getInstance(), notes);
    await s.load();
    await t.pumpWidget(HighApp(state: s));
    await t.pumpAndSettle();
    return HighNav.of(t.element(find.byType(PageShell).first));
  }

  Finder inCard(int i, Finder f) => find.descendant(of: find.byKey(ValueKey('card$i')), matching: f);

  testWidgets('table and steps cards render their body under the table / figure; no body adds nothing', (t) async {
    final nav = await open(t);
    final dk = bio9.diagrams.keys.first;
    final cards = [
      NoteCard.fromJ(
        J({
          'type': 'table',
          'page': 3,
          'title': 'T',
          'head': ['A', 'B'],
          'rows': [
            ['a1', 'b1'],
          ],
          'body': ['Table note under the rows'],
        }, 't0'),
      ),
      NoteCard.fromJ(
        J({
          'type': 'table',
          'page': 3,
          'title': 'T2',
          'head': ['A', 'B'],
          'rows': [
            ['a2', 'b2'],
          ],
        }, 't1'),
      ),
      NoteCard.fromJ(
        J({
          'type': 'steps',
          'page': 4,
          'title': 'S',
          'diagram': dk,
          'steps': [
            {'text': 'First step'},
            {'text': 'Second step'},
          ],
          'body': ['Steps note under the figure'],
        }, 't2'),
      ),
      NoteCard.fromJ(
        J({
          'type': 'diagram',
          'page': 5,
          'title': 'D',
          'diagram': dk,
          'mode': 'plain',
          'body': ['Diagram note'],
        }, 't3'),
      ),
    ];
    nav.push(_Cards(ctxOf(bio9), cards));
    await t.pumpAndSettle();
    expect(t.takeException(), isNull);

    expect(inCard(0, find.textContaining('Table note under the rows', findRichText: true)), findsOneWidget);
    expect(inCard(1, find.byType(RichParas)), findsNothing);
    expect(inCard(2, find.textContaining('Steps note under the figure', findRichText: true)), findsOneWidget);
    expect(inCard(3, find.textContaining('Diagram note', findRichText: true)), findsOneWidget);

    // the note sits below the table and below the step text
    double y(Finder f) => t.getTopLeft(f).dy;
    expect(y(inCard(0, find.textContaining('Table note', findRichText: true))), greaterThan(y(inCard(0, find.textContaining('b1', findRichText: true)))));
    expect(y(inCard(2, find.textContaining('Steps note', findRichText: true))), greaterThan(y(inCard(2, find.textContaining('First step', findRichText: true)))));

    // moving through the steps keeps the note
    await t.tap(inCard(2, find.textContaining('2', findRichText: true)).first, warnIfMissed: false);
    await t.pumpAndSettle();
    expect(inCard(2, find.textContaining('Steps note under the figure', findRichText: true)), findsOneWidget);
  });

  testWidgets('every real table / steps card with a body shows it', (t) async {
    final nav = await open(t);
    var n = 0;
    for (final b in books.values) {
      for (final u in b.units) {
        final cards = [
          for (final l in u.lessons)
            for (final c in l.cards)
              if ((c is TableCard || c is StepsCard) && c.body.any((x) => x.trim().isNotEmpty)) c,
        ];
        if (cards.isEmpty) continue;
        n += cards.length;
        nav.push(_Cards(ctxOf(u), cards));
        await t.pumpAndSettle();
        expect(t.takeException(), isNull, reason: u.id);
        for (var i = 0; i < cards.length; i++) {
          expect(inCard(i, find.byType(RichParas)), findsWidgets, reason: '${u.id} card $i');
        }
        nav.back();
        await t.pumpAndSettle();
      }
    }
    expect(n, greaterThan(0));
  });
}

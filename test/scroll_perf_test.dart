// Scrolling paths built lazily for low-end phones: the notes unit page (sliver list + jump bar + throttled progress)
// and the exam practice list (lazy ListView that still opens at a question far down the exam).
import 'dart:convert';

import 'package:flutter/widgets.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:high/high/app.dart';
import 'package:high/high/data/repository.dart';
import 'package:high/high/exam/cards.dart' as ec;
import 'package:high/high/exam/pages.dart';
import 'package:high/high/notes/jr/data/repository.dart';
import 'package:high/high/notes/jr/screens/unit_page.dart';
import 'package:high/high/screens/notes_home.dart';
import 'package:high/high/state/app_state.dart';
import 'package:high/high/theme/perf.dart';
import 'package:high/high/widgets/page.dart';
import 'package:shared_preferences/shared_preferences.dart';

import 'helpers.dart';

void main() {
  HighState.tickStudy = false;
  highDecorAnimations = false;
  final repo = ExamRepo(useIsolate: false), notes = NotesRepo(useIsolate: false);
  setUpAll(() async {
    await loadFonts();
    await repo.init();
    await notes.init();
  });

  Future<HighState> open(WidgetTester t) async {
    t.view.physicalSize = const Size(720, 1520);
    t.view.devicePixelRatio = 2;
    addTearDown(t.view.reset);
    SharedPreferences.setMockInitialValues({
      HighState.key: jsonEncode({'v': 2, 'name': 'Hana', 'theme': 'light', 'tourDone': true}),
    });
    final s = HighState(repo, await SharedPreferences.getInstance(), notes);
    await s.load();
    await t.pumpWidget(HighApp(state: s, initialTab: HighTab.notes));
    await t.pumpAndSettle();
    return s;
  }

  Future<void> settle(WidgetTester t) async {
    for (var i = 0; i < 4; i++) {
      await t.runAsync(() => Future<void>.delayed(const Duration(milliseconds: 150)));
      await t.pumpAndSettle();
    }
  }

  testWidgets('Lite is on by default and stored with the profile', (t) async {
    final s = await open(t);
    expect(s.lite, isTrue);
    expect(Perf.lite, isTrue);
    expect(s.toJson()['lite'], isTrue);
    s.fromJson({...s.toJson(), 'lite': false});
    expect(Perf.lite, isFalse);
    s.fromJson({...s.toJson(), 'lite': true});
    expect(Perf.lite, isTrue);
  });

  testWidgets('notes unit page scrolls, jumps and tracks progress', (t) async {
    final s = await open(t);
    final b = notes.grade(9).firstWhere((b) => b.subject == 'biology'), u = b.units.first;
    await t.runAsync(() => notes.book(b.id));
    HighNav.of(t.element(find.byType(NotesHomePage))).push(UnitPage(bookId: b.id, unitId: u.id));
    await settle(t);
    expect(find.byType(UnitPage), findsOneWidget);
    final list = find.descendant(of: find.byType(UnitPage), matching: find.byType(CustomScrollView));
    expect(list, findsOneWidget);
    // a long fling through the notes: lazily built, no exceptions, progress recorded without rebuilding the page
    for (var i = 0; i < 6; i++) {
      await t.fling(list, const Offset(0, -900), 2500);
      await t.pumpAndSettle();
    }
    await t.pump(const Duration(milliseconds: 500));
    expect(t.takeException(), isNull);
    final read = (s.notes['read'] as Map).values.fold<num>(0, (a, v) => a + (v as num));
    expect(read, greaterThan(0));
    // jump bar: Quiz scrolls to the unit quiz section
    await t.tap(find.text('Quiz').first);
    await t.pumpAndSettle();
    await t.pump(const Duration(milliseconds: 200));
    expect(find.text('Unit quiz').hitTestable(), findsOneWidget);
    // and back up to the first section, which the lazy list has long disposed
    await t.tap(find.text('Notes').first);
    await t.pumpAndSettle();
    await t.pump(const Duration(milliseconds: 200));
    final page = t.state<UnitPageState>(find.byType(UnitPage));
    final first = page.unit!.lessons.first;
    expect(find.text(first.title).hitTestable(), findsOneWidget);
    expect(t.takeException(), isNull);
    await t.pump(const Duration(seconds: 3)); // let the idle progress save fire
  });

  testWidgets('practice list is lazy and still opens at a question far down', (t) async {
    await open(t);
    final e = repo.exams.reduce((a, b) => a.questions.length >= b.questions.length ? a : b);
    expect(e.questions.length, greaterThan(30));
    final target = e.questions.lastWhere((q) => !q.isMatch);
    HighNav.of(t.element(find.byType(NotesHomePage))).push(PracticePage(examId: e.id, focus: target.id));
    await t.pump();
    for (var i = 0; i < 20; i++) {
      await t.pump(const Duration(milliseconds: 16));
    }
    await t.pumpAndSettle();
    // only a screenful of cards is built, not the whole exam
    expect(find.byType(ec.QCard).evaluate().length, lessThan(e.questions.length));
    final card = find.byWidgetPredicate((w) => w is ec.QCard && w.q.id == target.id);
    expect(card, findsOneWidget);
    final top = t.getTopLeft(card).dy;
    expect(top, inInclusiveRange(0, 760));
    expect(t.takeException(), isNull);
  });
}

// unit -> exercises -> back, unit -> matric -> back, and cross links pop back instead of piling up
import 'dart:convert';

import 'package:flutter/widgets.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:high/high/app.dart';
import 'package:high/high/data/repository.dart';
import 'package:high/high/exam/pages.dart';
import 'package:high/high/notes/jr/data/repository.dart';
import 'package:high/high/notes/jr/screens/unit_page.dart';
import 'package:high/high/screens/notes_home.dart';
import 'package:high/high/state/app_state.dart';
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

  testWidgets('unit links navigate and come back', (t) async {
    t.view.physicalSize = const Size(780, 1688);
    t.view.devicePixelRatio = 2;
    addTearDown(t.view.reset);
    SharedPreferences.setMockInitialValues({HighState.key: jsonEncode({'v': 2, 'name': 'Hana', 'theme': 'light'})});
    final s = HighState(repo, await SharedPreferences.getInstance(), notes);
    await s.load();
    await t.pumpWidget(HighApp(state: s, initialTab: HighTab.notes));
    await t.pumpAndSettle();
    final b = notes.grade(9).firstWhere((b) => b.subject == 'biology'), u = b.units.first;
    expect(s.links.exercisesFor(u.id), isNotEmpty);
    expect(s.links.matricFor(u.id), isNotEmpty);

    Future<void> go(Future<void> Function() f) async {
      await f();
      await t.pumpAndSettle();
      await t.runAsync(() => notes.book(b.id));
      await t.pumpAndSettle();
    }

    final nav = HighNav.of(t.element(find.byType(NotesHomePage)));
    await go(() async => nav.open('book:${b.id}', () => NotesSubjectPage(bookId: b.id)));
    await t.tap(find.text(u.title).first);
    await go(() async {});
    expect(find.byType(UnitPage), findsOneWidget);
    expect(find.textContaining('Exercises ('), findsOneWidget);
    expect(find.textContaining('Matric questions ('), findsWidgets);

    // unit -> exercises -> back
    await go(() => t.tap(find.textContaining('Exercises (').first));
    expect(find.byType(QuizPage), findsOneWidget);
    expect(t.widget<QuizPage>(find.byType(QuizPage)).kind, 'exercise');
    await go(() async => nav.back());
    expect(find.byType(UnitPage), findsOneWidget);

    // unit -> matric -> back
    await go(() => t.tap(find.textContaining('Matric questions (').first));
    expect(t.widget<QuizPage>(find.byType(QuizPage)).kind, 'unit');
    await go(() async => nav.back());
    expect(find.byType(UnitPage), findsOneWidget);

    // unit -> exercises -> "Read the notes" pops back to the same unit page (no second copy), then back -> subject page
    await go(() => t.tap(find.textContaining('Exercises (').first));
    nav.open('unit:${u.id}', () => UnitPage(bookId: b.id, unitId: u.id));
    await go(() async {});
    expect(find.byType(UnitPage), findsOneWidget);
    await go(() async => nav.back());
    expect(find.byType(NotesSubjectPage), findsOneWidget);
    // tab state: the Notes tab page is still the same element after a detour through another tab
    await go(() async => nav.back());
    final before = t.state(find.byType(NotesHomePage));
    await go(() async => nav.tab(HighTab.exercise));
    await go(() async => nav.tab(HighTab.notes));
    expect(identical(t.state(find.byType(NotesHomePage)), before), isTrue);
    await t.pump(const Duration(seconds: 5));
  });
}

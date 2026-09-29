// Light-mode screenshots of the Exercise tab: unit list + a question -> compare/exercise_*.png
//   flutter test test/exercise_shots_test.dart
import 'dart:convert';
import 'dart:io';
import 'dart:ui' as ui;

import 'package:flutter/rendering.dart';
import 'package:flutter/widgets.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:high/high/app.dart';
import 'package:high/high/data/repository.dart';
import 'package:high/high/notes/jr/data/repository.dart';
import 'package:high/high/exam/pages.dart';
import 'package:high/high/notes/jr/screens/unit_page.dart';
import 'package:high/high/screens/exercise.dart';
import 'package:high/high/state/app_state.dart';
import 'package:high/high/widgets/page.dart';
import 'package:shared_preferences/shared_preferences.dart';

import 'helpers.dart';

void main() {
  HighState.tickStudy = false;
  highDecorAnimations = false;
  highNow = () => DateTime(2026, 9, 29, 10);
  final repo = ExamRepo(useIsolate: false), notes = NotesRepo(useIsolate: false);
  final key = GlobalKey();
  setUpAll(() async {
    await loadFonts();
    await repo.init();
    await notes.init();
  });

  Future<void> save(WidgetTester t, String name) async {
    for (var i = 0; i < 4; i++) {
      await t.runAsync(() => Future<void>.delayed(const Duration(milliseconds: 60)));
      await t.pump(const Duration(milliseconds: 100));
    }
    await t.pumpAndSettle();
    final ro = t.renderObject<RenderRepaintBoundary>(find.byKey(key));
    await t.runAsync(() async {
      final img = await ro.toImage(pixelRatio: 2);
      final bd = await img.toByteData(format: ui.ImageByteFormat.png);
      File('compare/$name.png').writeAsBytesSync(bd!.buffer.asUint8List());
    });
  }

  testWidgets('exercise shots', (t) async {
    t.view.physicalSize = const Size(780, 1688);
    t.view.devicePixelRatio = 2;
    addTearDown(t.view.reset);
    SharedPreferences.setMockInitialValues({HighState.key: jsonEncode({'v': 2, 'name': 'Hana', 'theme': 'light'})});
    final s = HighState(repo, await SharedPreferences.getInstance(), notes);
    await s.load();
    await t.pumpWidget(RepaintBoundary(key: key, child: HighApp(state: s, initialTab: HighTab.exercise)));
    await t.pumpAndSettle();
    final nav = HighNav.of(t.element(find.byType(ExercisePage)));
    nav.push(const ExerciseSubjectPage(grade: 9, subject: 'biology'));
    await save(t, 'exercise_units');
    final u = notes.grade(9).firstWhere((b) => b.subject == 'biology').units.first;
    openExercises(t.element(find.byType(ExerciseSubjectPage)), grade: 9, subject: 'biology', unitId: u.id, title: 'Unit ${u.number} · ${u.title}');
    await t.pumpAndSettle();
    final q = repo.byId[t.widget<QuizPage>(find.byType(QuizPage)).ids.first]!;
    await t.tap(find.textContaining(q.options![q.answer]!, findRichText: true).first);
    await save(t, 'exercise_question');
    await t.pump(const Duration(seconds: 5));
  });

  testWidgets('unit links shot', (t) async {
    t.view.physicalSize = const Size(780, 1688);
    t.view.devicePixelRatio = 2;
    addTearDown(t.view.reset);
    SharedPreferences.setMockInitialValues({HighState.key: jsonEncode({'v': 2, 'name': 'Hana', 'theme': 'light'})});
    final s = HighState(repo, await SharedPreferences.getInstance(), notes);
    await s.load();
    await t.pumpWidget(RepaintBoundary(key: key, child: HighApp(state: s, initialTab: HighTab.notes)));
    await t.pumpAndSettle();
    final b = notes.grade(9).firstWhere((b) => b.subject == 'biology');
    HighNav.of(t.element(find.byType(PageShell).first)).push(UnitPage(bookId: b.id, unitId: b.units.first.id));
    await t.runAsync(() => notes.book(b.id));
    await t.pumpAndSettle();
    await save(t, 'unit_links');
    await t.pump(const Duration(seconds: 5));
  });
}

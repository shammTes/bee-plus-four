// M2/M3 smoke: new nav tabs, Home grade tiles -> Grade page -> notes unit, exam practice, quiz, tutor, mistakes.
import 'package:flutter/widgets.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:high/high/app.dart';
import 'package:high/high/data/repository.dart';
import 'package:high/high/exam/pages.dart';
import 'package:high/high/notes/jr/data/repository.dart';
import 'package:high/high/notes/jr/screens/unit_page.dart';
import 'package:high/high/screens/exercise.dart';
import 'package:high/high/screens/notes_home.dart';
import 'package:high/high/screens/tutor.dart';
import 'package:high/high/state/app_state.dart';
import 'package:high/high/widgets/page.dart';
import 'package:shared_preferences/shared_preferences.dart';

import 'helpers.dart';

void main() {
  HighState.tickStudy = false;
  highDecorAnimations = false;
  final repo = ExamRepo(useIsolate: false);
  final notes = NotesRepo(useIsolate: false);
  setUpAll(loadFonts);

  Future<HighState> boot(WidgetTester t) async {
    t.view.physicalSize = const Size(780, 1688);
    t.view.devicePixelRatio = 2;
    addTearDown(t.view.reset);
    await t.runAsync(() async {
      await repo.init();
      await notes.init();
    });
    SharedPreferences.setMockInitialValues({'high:v1': '{"name":"Abel"}'});
    final s = HighState(repo, await SharedPreferences.getInstance(), notes);
    await s.load();
    await t.pumpWidget(HighApp(state: s));
    await t.pumpAndSettle();
    return s;
  }

  testWidgets('tabs, grade tiles, practice, quiz, tutor', (t) async {
    final s = await boot(t);
    expect(find.text('Grade'), findsNWidgets(4));
    for (final l in ['Notes', 'Exercise', 'Matric', 'Tutor', 'Home']) {
      await t.tap(find.text(l).last);
      await t.pumpAndSettle();
      expect(t.takeException(), isNull, reason: l);
    }
    await t.tap(find.text('12').first);
    await t.pumpAndSettle();
    expect(find.byType(GradePage), findsOneWidget);
    HighNav.of(t.element(find.byType(GradePage))).back();
    await t.pumpAndSettle();

    final e = repo.exams.first;
    final nav = HighNav.of(t.element(find.byType(PageShell).first));
    nav.push(PracticePage(examId: e.id));
    await t.pumpAndSettle();
    expect(t.takeException(), isNull);
    nav.back();
    await t.pumpAndSettle();
    nav.push(QuizPage(ids: [for (final q in e.scored.take(5)) q.id], title: 'Q'));
    await t.pumpAndSettle();
    expect(t.takeException(), isNull);
    nav.back();
    await t.pumpAndSettle();
    nav.push(const MistakesPage());
    await t.pumpAndSettle();
    nav.back();
    nav.push(const WeakPage());
    await t.pumpAndSettle();
    nav.back();
    nav.push(ExamSubjectPage(subject: e.subject));
    await t.pumpAndSettle();
    expect(t.takeException(), isNull);
    nav.back();
    await t.pumpAndSettle();
    expect(s.name, 'Abel');
    final b = notes.books.first;
    nav.push(NotesSubjectPage(bookId: b.id));
    await t.pumpAndSettle();
    nav.push(UnitPage(bookId: b.id, unitId: b.units.first.id));
    await t.runAsync(() => notes.book(b.id));
    await t.pumpAndSettle();
    expect(t.takeException(), isNull);
    await t.drag(find.byType(Scrollable).first, const Offset(0, -3000));
    await t.pumpAndSettle();
    expect(t.takeException(), isNull);
    nav.back();
    await t.pumpAndSettle();
    nav.back();
    final b12 = notes.grade(12).first;
    nav.push(ExerciseUnitPage(grade: 12, subject: b12.subject, unitId: b12.units.first.id, title: 'U'));
    await t.pumpAndSettle();
    expect(find.text('Exercises coming soon'), findsOneWidget);
    nav.back();
    await t.pumpAndSettle();

    await t.tap(find.text('Tutor').last);
    await t.pumpAndSettle();
    expect(find.byType(TutorPage), findsOneWidget);
    await t.enterText(find.byType(EditableText), 'photosynthesis');
    await t.testTextInput.receiveAction(TextInputAction.done);
    await t.pumpAndSettle();
    expect(t.takeException(), isNull);
  });

  testWidgets('exercise tab: grade -> subject -> unit opens the quiz and records answers', (t) async {
    final s = await boot(t);
    await t.tap(find.text('Exercise').last);
    await t.pumpAndSettle();
    await t.tap(find.descendant(of: find.byType(ExercisePage), matching: find.text('Grade 9')).first);
    await t.pumpAndSettle();
    await t.tap(find.descendant(of: find.byType(ExercisePage), matching: find.text('Biology')).first);
    await t.pumpAndSettle();
    expect(find.byType(ExerciseSubjectPage), findsOneWidget, reason: '${find.byType(ExercisePage).evaluate().length} exercise pages');
    final ids = repo.exerciseIds(grade: 9, subject: 'biology', unitId: notes.grade(9).firstWhere((b) => b.subject == 'biology').units.first.id);
    expect(ids, isNotEmpty);
    await t.tap(find.descendant(of: find.byType(ExerciseSubjectPage), matching: find.textContaining('questions')).first);
    await t.pumpAndSettle();
    expect(find.byType(QuizPage), findsOneWidget);
    final q = repo.byId[t.widget<QuizPage>(find.byType(QuizPage)).ids.first]!;
    final wrong = q.options!.keys.firstWhere((l) => l != q.answer);
    await t.tap(find.textContaining(q.options![wrong]!, findRichText: true).first);
    await t.pumpAndSettle();
    expect(t.takeException(), isNull);
    expect(s.answered(q.id), isTrue);
    expect(s.mistakes, contains(q.id));
    expect(s.recent.any((r) => r['id'] == q.exam.id), isFalse);
    await t.pump(const Duration(seconds: 5)); // save debounce
  });
}

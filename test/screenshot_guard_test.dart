// Screenshot block: reference counting (Notes/Matric sections + resource viewers share one FLAG_SECURE) and
// the route-aware shell (flag on while a Notes / Matric page is on top, off elsewhere).
import 'dart:convert';

import 'package:flutter/services.dart';
import 'package:flutter/widgets.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:high/high/app.dart';
import 'package:high/high/data/repository.dart';
import 'package:high/high/exam/pages.dart';
import 'package:high/high/notes/jr/data/repository.dart';
import 'package:high/high/notes/jr/screens/unit_page.dart';
import 'package:high/high/screens/exams.dart';
import 'package:high/high/screens/home.dart';
import 'package:high/high/screens/exercise.dart';
import 'package:high/high/screens/notes_home.dart';
import 'package:high/high/screens/settings.dart';
import 'package:high/high/state/app_state.dart';
import 'package:high/high/widgets/page.dart';
import 'package:high/licensing/screenshot.dart';
import 'package:high/resources/library.dart';
import 'package:shared_preferences/shared_preferences.dart';

import 'helpers.dart';

void main() {
  group('SecureFlag ref counting', () {
    late List<bool> sent;
    late SecureFlag f;
    setUp(() {
      sent = [];
      f = SecureFlag((on) async => sent.add(on));
    });

    test('on with the first holder, off only after the last', () {
      f.acquire('sections');
      expect(sent, [true]);
      f.acquire('resources'); // video opened over a notes page
      expect(sent, [true], reason: 'no extra platform call while already on');
      f.release('resources'); // video closed: notes page still visible
      expect(f.isOn, isTrue);
      expect(sent, [true]);
      f.release('sections');
      expect(f.isOn, isFalse);
      expect(sent, [true, false]);
    });

    test('the other order: the section leaves first, the video keeps the flag', () {
      f.acquire('resources');
      f.acquire('sections');
      f.release('sections');
      expect(f.isOn, isTrue);
      f.release('resources');
      expect(sent, [true, false]);
    });

    test('nested holds of one owner (reels -> video) count separately', () {
      f.acquire('resources');
      f.acquire('resources');
      expect(f.holds('resources'), 2);
      f.release('resources');
      expect(f.isOn, isTrue);
      f.release('resources');
      expect(f.isOn, isFalse);
    });

    test('unbalanced release never clears another owner', () {
      f.acquire('sections');
      f.release('resources');
      f.release('resources');
      expect(f.isOn, isTrue);
      expect(f.count, 1);
      expect(sent, [true]);
    });

    test('releaseAll drops one owner only; reapply re-sends the state', () async {
      f.acquire('resources');
      f.acquire('resources');
      f.acquire('sections');
      f.releaseAll('resources');
      expect(f.isOn, isTrue);
      await f.reapply();
      expect(sent, [true, true]);
      f.releaseAll('sections');
      expect(sent.last, isFalse);
    });
  });

  test('section classifier: Notes and Matric pages only', () {
    bool p(Widget w) => HighShellState.isSecurePage(KeyedSubtree(key: const ValueKey(1), child: w));
    expect(p(const NotesHomePage()), isTrue);
    expect(p(const NotesSubjectPage(bookId: 'chemistry_9')), isTrue);
    expect(p(const GradePage(grade: 9)), isTrue);
    expect(p(const UnitPage(bookId: 'chemistry_9', unitId: 'u')), isTrue);
    expect(p(const ExamsPage()), isTrue);
    expect(p(const ExamSubjectPage(subject: 'Chemistry')), isTrue);
    expect(p(const PracticePage(examId: 'x')), isTrue);
    expect(p(const QuizPage(ids: [], title: 'm', kind: 'unit')), isTrue);
    expect(p(const QuizPage(ids: [], title: 't')), isTrue); // topic quiz (matric questions)
    expect(p(const QuizPage(ids: [], title: 'e', kind: 'exercise')), isFalse);
    expect(p(const QuizPage(ids: [], title: 'd', kind: 'daily')), isFalse);
    expect(p(const ExercisePage()), isFalse);
    expect(p(const SettingsPage()), isFalse);
    expect(HighShellState.isSecureTab(HighTab.notes), isTrue);
    expect(HighShellState.isSecureTab(HighTab.matric), isTrue);
    expect(HighShellState.isSecureTab(HighTab.home), isFalse);
    expect(HighShellState.isSecureTab(HighTab.exercise), isFalse);
    expect(HighShellState.isSecureTab(HighTab.tutor), isFalse);
  });

  group('shell', () {
    HighState.tickStudy = false;
    highDecorAnimations = false;
    final repo = ExamRepo(useIsolate: false), notes = NotesRepo(useIsolate: false);
    setUpAll(() async {
      await loadFonts();
      await repo.init();
      await notes.init();
    });

    testWidgets('flag follows the visible page; a video over notes does not clear it', (t) async {
      final calls = <bool>[];
      t.binding.defaultBinaryMessenger.setMockMethodCallHandler(const MethodChannel('com.warsay.high/resources'), (c) async {
        if (c.method == 'setSecure') calls.add((c.arguments as Map)['on'] as bool);
        return null;
      });
      ScreenshotGuard.reset();
      t.view.physicalSize = const Size(720, 1560);
      t.view.devicePixelRatio = 2;
      addTearDown(t.view.reset);
      SharedPreferences.setMockInitialValues({HighState.key: jsonEncode({'v': 2, 'name': 'Hana', 'theme': 'light'})});
      final s = HighState(repo, await SharedPreferences.getInstance(), notes);
      await s.load();
      await t.pumpWidget(HighApp(state: s, initialTab: HighTab.home));
      await t.pumpAndSettle();
      expect(ScreenshotGuard.isOn, isFalse);
      expect(calls, isEmpty);

      final nav = HighNav.of(t.element(find.byType(HomePage)));
      nav.tab(HighTab.notes);
      await t.pumpAndSettle();
      expect(ScreenshotGuard.isOn, isTrue, reason: 'notes tab');

      final b = notes.grade(9).firstWhere((b) => b.subject == 'chemistry');
      nav.open('book:${b.id}', () => NotesSubjectPage(bookId: b.id)); // nested notes route
      await t.pumpAndSettle();
      expect(ScreenshotGuard.isOn, isTrue);
      expect(calls, [true], reason: 'staying inside Notes sends nothing new');

      // a resource viewer over the notes page takes its own hold
      ResourceLibrary.setSecure(true);
      nav.push(const SettingsPage()); // a non-notes page on top: the section hold is dropped
      await t.pumpAndSettle();
      expect(ScreenshotGuard.flag.holds('sections'), 0);
      expect(ScreenshotGuard.isOn, isTrue, reason: 'resource still holds it');
      ResourceLibrary.setSecure(false);
      expect(ScreenshotGuard.isOn, isFalse);

      nav.back(); // back to the notes page
      await t.pumpAndSettle();
      expect(ScreenshotGuard.isOn, isTrue);

      nav.tab(HighTab.exercise);
      await t.pumpAndSettle();
      expect(ScreenshotGuard.isOn, isFalse, reason: 'Exercises is not protected');

      nav.tab(HighTab.matric);
      await t.pumpAndSettle();
      expect(ScreenshotGuard.isOn, isTrue, reason: 'matric tab');

      nav.back(); // system back from a tab goes home
      await t.pumpAndSettle();
      expect(ScreenshotGuard.isOn, isFalse);
      expect(calls, [true, false, true, false, true, false]);

      // app resumed: the current state is sent again
      calls.clear();
      for (final st in [AppLifecycleState.inactive, AppLifecycleState.hidden, AppLifecycleState.paused, AppLifecycleState.hidden, AppLifecycleState.inactive, AppLifecycleState.resumed]) {
        t.binding.handleAppLifecycleStateChanged(st);
      }
      await t.pump();
      expect(calls, [false]);
    });
  });
}

// Matric GPA calculator: letter bands, Maths + English + best 3, the estimate from recent answers, and the GPA page
// (off by default; On + manual marks show the GPA).
//   flutter test test/gpa_test.dart
import 'dart:convert';

import 'package:flutter/widgets.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:high/high/app.dart';
import 'package:high/high/data/repository.dart';
import 'package:high/high/gpa/gpa.dart';
import 'package:high/high/gpa/gpa_config.dart';
import 'package:high/high/gpa/gpa_ui.dart';
import 'package:high/high/notes/jr/data/repository.dart';
import 'package:high/high/state/app_state.dart';
import 'package:high/high/widgets/page.dart';
import 'package:shared_preferences/shared_preferences.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();

  test('letter bands', () {
    expect(bandFor(100).letter, 'A');
    expect(bandFor(75).letter, 'A');
    expect(bandFor(74.9).letter, 'B');
    expect(bandFor(65).points, 3);
    expect(bandFor(50).letter, 'C');
    expect(bandFor(40).letter, 'D');
    expect(bandFor(39.9).letter, 'F');
    expect(bandFor(0).points, 0);
  });

  test('GPA = Maths + English + best 3 of the stream', () {
    final r = computeGpa({'Mathematics': 80, 'English': 66, 'Physics': 90, 'Chemistry': 55, 'Biology': 45, 'Agriculture': 70, 'History': 100}, 'natural');
    expect(r.used.map((g) => g.subject), ['Mathematics', 'English', 'Physics', 'Agriculture', 'Chemistry']);
    expect(r.gpa, closeTo((4 + 3 + 4 + 3 + 2) / 5, 1e-9));
    expect(r.complete, isTrue);
    expect(computeGpa({'Mathematics': 99, 'English': 99, 'Geography': 99, 'History': 80, 'Business and Economics': 76}, 'social').gpa, 4.0);
  });

  test('partial GPA says what is missing', () {
    final r = computeGpa({'Mathematics': 60, 'Physics': 80}, 'natural');
    expect(r.gpa, closeTo(3.0, 1e-9));
    expect(r.complete, isFalse);
    expect(r.missing, contains('English'));
    expect(computeGpa({}, 'natural').gpa, isNull);
  });

  test('estimate uses the newest answer per question and needs enough answers', () {
    final ev = <List<dynamic>>[
      for (var i = 0; i < 20; i++) [i, 'm$i', i < 15 ? 1 : 0, 'exam'],
      [99, 'm0', 0, 'exam'], // newer wrong answer to m0
      for (var i = 0; i < 5; i++) [100 + i, 'e$i', 1, 'exam'],
      [200, 'x1', 1, 'exercise'],
    ];
    final r = estimateFromAnswers(ev, (id) => id.startsWith('m') ? 'Mathematics' : id.startsWith('e') ? 'English' : null);
    expect(r.n['Mathematics'], 20);
    expect(r.pct['Mathematics'], closeTo(100 * 14 / 20, 1e-9));
    expect(r.pct.containsKey('English'), isFalse, reason: 'only 5 answers < ${GpaConfig.minAnswers}');
  });

  testWidgets('GPA page: off by default; On + my own marks show the GPA; saved', (t) async {
    HighState.tickStudy = false;
    t.view.physicalSize = const Size(800, 1400);
    t.view.devicePixelRatio = 1;
    addTearDown(t.view.reset);
    SharedPreferences.setMockInitialValues({'four_highschool_unlocked': true, HighState.key: jsonEncode({'v': 2, 'name': 'Hana', 'theme': 'light', 'tourDone': true})});
    final repo = ExamRepo(useIsolate: false), notes = NotesRepo(useIsolate: false);
    late HighState s;
    await t.runAsync(() async {
      await repo.init();
      await notes.init();
      s = HighState(repo, await SharedPreferences.getInstance(), notes);
      await s.load();
    });
    expect(s.gpaOn, isFalse);
    await t.pumpWidget(HighApp(state: s));
    await t.pumpAndSettle();
    HighNav.of(t.element(find.byType(PageShell).first)).push(const GpaPage());
    await t.pumpAndSettle();
    expect(find.byKey(const ValueKey('gpa-big')), findsNothing);
    s.gpaSet('on', true);
    s.gpaSet('manual', true);
    for (final e in {'Mathematics': 80.0, 'English': 70.0, 'Physics': 90.0, 'Chemistry': 60.0, 'Biology': 50.0}.entries) {
      s.gpaMark(e.key, e.value);
    }
    await t.pumpAndSettle();
    expect(find.text('${fmtGpa((4 + 3 + 4 + 2 + 2) / 5)} / 4.0'), findsOneWidget);
    expect((s.toJson()['gpa'] as Map)['on'], isTrue);
    await t.pumpWidget(const SizedBox());
    await t.pump(const Duration(seconds: 3));
  });
}

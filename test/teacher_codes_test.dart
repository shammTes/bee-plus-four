// Board codes: unique + decodable, set codes round-trip, homework sheet shows no answers / explanations.
import 'dart:convert';
import 'dart:math';

import 'package:flutter/widgets.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:high/high/app.dart';
import 'package:high/high/data/repository.dart';
import 'package:high/high/notes/jr/data/repository.dart';
import 'package:high/high/state/app_state.dart';
import 'package:high/high/teacher/codes.dart';
import 'package:high/high/teacher/teacher.dart';
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

  test('every question has exactly one valid code', () {
    final cd = repo.codes!;
    final ok = RegExp('^[$kCodeAlphabet]{5}\$');
    expect(cd.codes.toSet().length, cd.codes.length);
    for (final id in repo.byId.keys) {
      final c = cd.codeOf(id);
      expect(c, isNotNull, reason: id);
      expect(ok.hasMatch(c!), isTrue, reason: c);
      expect(cd.idOf(c), id);
      expect(cd.parse(c.toLowerCase()).ids, [id]);
    }
  });

  test('set codes round-trip and reject typos', () {
    final cd = repo.codes!, rnd = Random(4), n = cd.order.length;
    var maxLen = 0;
    for (var t = 0; t < 400; t++) {
      final k = 1 + rnd.nextInt(t < 200 ? 12 : 40);
      final start = rnd.nextInt(n);
      final ids = {for (var i = 0; i < k; i++) cd.order[t.isEven ? (start + rnd.nextInt(60)) % n : rnd.nextInt(n)]}.toList();
      final code = cd.setCode(ids);
      expect(code.length, isNot(5));
      expect(cd.decodeSet(code), cd.canonical(ids), reason: code);
      expect(cd.parse(code).ids, cd.canonical(ids));
      // one changed character is caught by the checksum (almost always)
      final bad = code.substring(0, code.length - 1) + (code.endsWith('2') ? '3' : '2');
      expect(cd.decodeSet(bad), isNull, reason: bad);
      if (k <= 10 && t.isEven) maxLen = max(maxLen, code.length);
    }
    // 10 nearby questions (same exam) fit a short code
    final e = repo.exams.first;
    final ten = cd.setCode(e.questions.take(10).map((q) => q.id));
    expect(ten.length, lessThanOrEqualTo(15), reason: ten);
    expect(cd.decodeSet('ZZZZZZZZ'), isNull);
  });

  testWidgets('homework sheet: questions only, no answers or explanations', (t) async {
    t.view.physicalSize = const Size(780, 1688);
    t.view.devicePixelRatio = 2;
    addTearDown(t.view.reset);
    SharedPreferences.setMockInitialValues({HighState.key: jsonEncode({'v': 2, 'name': 'Hana', 'theme': 'light'})});
    final s = HighState(repo, await SharedPreferences.getInstance(), notes);
    await s.load();
    await t.pumpWidget(HighApp(state: s));
    await t.pumpAndSettle();
    // a mix: exercise MCQs with explanations + matric questions with steps (MCQ and written)
    final ex = repo.exerciseExams['9|biology']!.questions.take(3).toList();
    final mt = [for (final e in repo.exams) ...e.questions].where((q) => q.steps.isNotEmpty).take(4).toList();
    final qs = [...ex, ...mt];
    final code = repo.codes!.setCode(qs.map((q) => q.id));
    final nav = HighNav.of(t.element(find.byType(PageShell).first));
    nav.open('classcode', () => const EnterCodePage());
    await t.pumpAndSettle();
    await t.enterText(find.byKey(const ValueKey('classCode')), code.toLowerCase());
    await t.tap(find.text('Open homework'));
    await t.pumpAndSettle();
    expect(find.byType(HomeworkPage), findsOneWidget);
    expect(s.homework.first['code'], code);
    final texts = <String>[];
    for (var i = 0; i < 30; i++) {
      texts.addAll(t.widgetList<RichText>(find.byType(RichText)).map((w) => w.text.toPlainText()));
      await t.drag(find.byType(Scrollable).first, const Offset(0, -500));
      await t.pumpAndSettle();
    }
    final all = texts.join('\n');
    expect(all, contains('Question 1'));
    expect(all, contains('Question ${qs.length}'));
    for (final q in qs) {
      for (final st in q.steps) {
        if (st.length > 25 && !q.stem.contains(st)) expect(all.contains(st), isFalse, reason: 'explanation leaked: $st');
      }
    }
    for (final w in ['Correct', 'Answer:', 'Step-by-step', 'Explanation', 'Model answer', 'Show answer', 'Check']) {
      expect(all.contains(w), isFalse, reason: w);
    }
    await t.pump(const Duration(seconds: 5));
  });
}

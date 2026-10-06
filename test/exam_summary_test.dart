// The exam packs are not read at start-up any more: ExamRepo(lazyExams: true) builds question stubs from
// assets/high/exams/summary.json (tool/exam_summary.py) and reads a pack only when its questions are shown. Everything
// the stubs feed (Home / Matric / Mistakes counts, topics, progress) must match a full load, and so must the questions
// once read. If this fails after an exam pack or topic index changed: python3 tool/exam_summary.py

import 'package:flutter_test/flutter_test.dart';
import 'package:high/high/data/models.dart';
import 'package:high/high/data/repository.dart';

String _q(Question q) => [q.id, q.exam.id, q.isMCQ, q.isMatch, q.isScored, q.reviewFlag != null, q.topics].toString();

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();

  late ExamRepo eager, lazy;
  setUpAll(() async {
    eager = ExamRepo(lazyExercises: true, deferCodes: true);
    await eager.init();
    lazy = ExamRepo(lazyExercises: true, lazyExams: true, deferCodes: true);
    await lazy.init();
  });

  const fix = 'summary.json is out of date: run python3 tool/exam_summary.py';

  test('start-up reads the summary, not the packs', () {
    expect(lazy.fromSummary, isTrue, reason: 'summary missing or does not match index.json: $fix');
    expect(eager.fromSummary, isFalse);
    expect(lazy.exams.every((e) => !e.full), isTrue);
    expect(lazy.allExamsLoaded, isFalse);
    expect(lazy.conceptsLoaded, isFalse);
    expect(lazy.concepts, isEmpty);
  });

  test('stubs give the same exams, questions, flags and topics as a full load', () {
    expect([for (final e in lazy.exams) '${e.id} ${e.file} ${e.j}'], [for (final e in eager.exams) '${e.id} ${e.file} ${e.j}'], reason: fix);
    final bad = <String>[];
    for (final (i, e) in eager.exams.indexed) {
      final l = lazy.exams[i];
      final a = [for (final q in e.questions) _q(q)], b = [for (final q in l.questions) _q(q)];
      if (a.toString() != b.toString()) bad.add(e.id);
      if (e.scored.length != l.scored.length || e.mcqs.length != l.mcqs.length || e.matches.length != l.matches.length) bad.add('${e.id} counts');
    }
    expect(bad, isEmpty, reason: fix);
    expect(lazy.byId.keys.toSet(), eager.byId.keys.toSet());
    expect(lazy.byId.values.every((q) => q.isStub), isTrue);
  });

  test('subjects and topic maps match', () {
    expect(lazy.subjects, eager.subjects);
    expect(lazy.topicQs, eager.topicQs, reason: fix);
    expect(lazy.topicParent, eager.topicParent, reason: fix);
    expect(lazy.topicTitleMap, eager.topicTitleMap, reason: fix);
  });

  test('one pack on demand: full questions replace the stubs', () async {
    final e = lazy.exams[lazy.exams.length ~/ 2], ee = eager.exam[e.id]!;
    final v = lazy.examVersion;
    await Future.wait([lazy.ensureExam(e.id), lazy.ensureExam(e.id)]);
    expect(lazy.examVersion, v + 1, reason: 'read once');
    expect(e.full, isTrue);
    expect([for (final q in e.questions) q.j], [for (final q in ee.questions) q.j]);
    for (final q in e.questions) {
      expect(identical(lazy.byId[q.id], q), isTrue);
      expect(q.isStub, isFalse);
    }
    // the others are still stubs
    expect(lazy.exams.where((x) => !x.full).length, lazy.exams.length - 1);
  });

  test('ensureExamsFor reads only the packs of the given ids', () async {
    final e = lazy.exams.firstWhere((x) => !x.full);
    await lazy.ensureExamsFor([e.questions.first.id, 'no-such-id']);
    expect(e.full, isTrue);
  });

  test('everything + concepts (tutor) equals a full load', () async {
    await Future.wait([lazy.ensureAllExams(), lazy.ensureAllExams(), lazy.ensureConcepts()]);
    expect(lazy.allExamsLoaded, isTrue);
    expect(lazy.conceptsLoaded, isTrue);
    expect(lazy.byId.values.any((q) => q.isStub), isFalse);
    for (final (i, e) in eager.exams.indexed) {
      final l = lazy.exams[i];
      expect([for (final q in l.questions) q.j], [for (final q in e.questions) q.j], reason: e.id);
      expect([for (final q in l.questions) _q(q)].toString(), [for (final q in e.questions) _q(q)].toString(), reason: e.id);
      expect(l.matchLists.keys, e.matchLists.keys);
      expect(l.passages.keys, e.passages.keys);
    }
    expect([for (final c in lazy.concepts) '${c.subject} ${c.sub['id']} ${c.sub['title']}'], [for (final c in eager.concepts) '${c.subject} ${c.sub['id']} ${c.sub['title']}']);
    expect(lazy.topicQs, eager.topicQs);
  });
}

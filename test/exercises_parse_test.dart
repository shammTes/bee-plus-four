// the bundled exercise bank (assets/high/exercises, tools/clean_exercises.py) is well-formed and loads into ExamRepo
import 'dart:convert';
import 'dart:io';

import 'package:flutter_test/flutter_test.dart';
import 'package:high/high/data/repository.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();
  test('exercise files match the index and the notes units', () {
    final idx = jsonDecode(File('assets/high/exercises/index.json').readAsStringSync()) as Map<String, dynamic>;
    final notes = jsonDecode(File('assets/high/notes/notes/index.json').readAsStringSync()) as Map<String, dynamic>;
    final unitIds = {
      for (final g in (notes['grades'] as Map).values)
        for (final b in (g as Map).values) for (final u in (b as Map)['units'] as List) (u as Map)['id'],
    };
    final ids = <String>{};
    var total = 0;
    (idx['grades'] as Map).forEach((g, subs) {
      (subs as Map).forEach((subj, e) {
        final d = jsonDecode(File('assets/high/exercises/${e['file']}').readAsStringSync()) as Map<String, dynamic>;
        final qs = (d['questions'] as List).cast<Map<String, dynamic>>();
        expect(qs.length, e['count'], reason: e['file']);
        for (final q in qs) {
          expect(ids.add(q['id'] as String), isTrue, reason: 'duplicate id ${q['id']}');
          final o = q['options'] as List;
          expect(o.length, inInclusiveRange(3, 5));
          expect(q['answer'], inInclusiveRange(0, o.length - 1));
          expect((q['prompt'] as String).startsWith('['), isFalse, reason: q['id']);
          expect(o.any((x) => RegExp(r'^[A-E][).]\s').hasMatch(x as String)) && o.every((x) => RegExp(r'^[A-E][).]\s').hasMatch(x as String)), isFalse, reason: q['id']);
          expect(q['unit'] == null || unitIds.contains(q['unit']), isTrue, reason: '${q['id']} -> ${q['unit']}');
          // explanation/trusted: tools/clean_exercises.py; reviewed: tools/fill_exercises.py (keys checked by hand,
          // see tool/exercises_fill/fixes.json); drive_*: items synced from the Drive bank
          expect(['explanation', 'trusted', 'reviewed', 'drive_practice', 'drive_chapter'], contains(q['verified']));
        }
        total += qs.length;
      });
    });
    expect(total, idx['total']);
  });

  test('ExamRepo registers the bank as exercise exams', () async {
    final r = ExamRepo(useIsolate: false);
    await r.init();
    expect(r.exerciseExams, isNotEmpty);
    final e = r.exerciseExams['9|biology']!;
    expect(e.isExercise, isTrue);
    expect(r.exams.contains(e), isFalse); // not listed with matric/model exams
    expect(e.questions.every((q) => q.isScored && q.options!.containsKey(q.answer)), isTrue);
  });
}

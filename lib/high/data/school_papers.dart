import 'dart:convert';
import 'off_thread.dart';

import 'package:flutter/services.dart';

import 'models.dart';
import 'repository.dart';

/// Loads assets/high/exercises/school and appends those MCQs onto the Exercise bank.
Future<void> loadSchoolPapers(ExamRepo repo, AssetBundle bundle, {required bool useIsolate}) async {
  const pack = 'assets/high/exercises/school';
  final String raw;
  try {
    raw = await bundle.loadString('$pack/index.json');
  } catch (_) {
    return;
  }
  final idx = jsonDecode(raw) as Map<String, dynamic>;
  final files = [
    for (final g in (idx['grades'] as Map).values)
      for (final e in (g as Map).values) (e as Map)['file'] as String,
  ];
  final raws = await Future.wait(files.map((f) => bundle.loadString('$pack/$f', cache: false)));
  final parsed = useIsolate ? await offThread(decodeJsonList, raws) : decodeJsonList(raws);
  for (final d in parsed.cast<Map<String, dynamic>>()) {
    final subj = d['subject'] as String, g = (d['grade'] as num).toInt();
    final key = '$g|$subj';
    var e = repo.exerciseExams[key];
    if (e == null) {
      final label = exerciseSubjectLabel(subj);
      e = Exam({'id': 'exercise_${subj}_$g', 'subject': label, 'year': 'Grade $g', 'type': 'exercise', 'title': '$label exercises', 'school': 'Exercise bank'}, '$pack/${subj}_$g.json');
      e.questions = [];
      repo.exam[e.id] = e;
      repo.exerciseExams[key] = e;
    }
    var n = e.questions.length;
    for (final q in (d['questions'] as List).cast<Map<String, dynamic>>()) {
      final id = '${q['id']}';
      if (repo.byId.containsKey(id)) continue;
      final question = Question({
        'id': id,
        'type': 'mcq',
        'number': ++n,
        'stem': q['prompt'],
        'options': {for (final (i, o) in (q['options'] as List).indexed) 'ABCDE'[i]: o},
        'answer': 'ABCDE'[(q['answer'] as num).toInt()],
        'explanation_steps': [if ((q['explanation'] as String? ?? '').isNotEmpty) q['explanation']],
        'unit': q['unit'],
      }, e);
      e.questions.add(question);
      repo.byId[id] = question;
      (repo.exerciseUnits[(q['unit'] as String?) ?? 'general|$g|$subj'] ??= []).add(id);
    }
  }
}

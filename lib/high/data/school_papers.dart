import 'models.dart';
import 'repository.dart';

/// Appends one school-paper file (`assets/high/exercises/school/<subject>_<grade>.json`, already decoded) onto the
/// Exercise bank's set for that grade + subject. Called by ExamRepo when the set is loaded (lazily in the app).
void addSchoolPaperQuestions(ExamRepo repo, Map<String, dynamic> d, String pack) {
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

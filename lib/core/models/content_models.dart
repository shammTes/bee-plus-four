class UnitNote {
  final String grade, subject, title, summary;
  final int unitNumber;
  final List<String> keyTerms;
  const UnitNote({required this.grade, required this.subject, required this.unitNumber, required this.title, required this.summary, this.keyTerms = const []});
  factory UnitNote.fromJson(Map<String, dynamic> j) => UnitNote(
    grade: j['grade'] as String, subject: j['subject'] as String, unitNumber: j['unit_number'] as int,
    title: j['title'] as String, summary: j['summary'] as String? ?? '',
    keyTerms: (j['key_terms'] as List?)?.cast<String>() ?? const [],
  );
}

class PracticeQuestion {
  final String id, grade, subject, prompt, explanation;
  final List<String> options;
  final int correctIndex;
  const PracticeQuestion({required this.id, required this.grade, required this.subject, required this.prompt, required this.options, required this.correctIndex, required this.explanation});
  factory PracticeQuestion.fromJson(Map<String, dynamic> j) => PracticeQuestion(
    id: j['id'] as String, grade: j['grade'] as String, subject: j['subject'] as String,
    prompt: j['prompt'] as String, options: (j['options'] as List).cast<String>(),
    correctIndex: j['correct_index'] as int,
    explanation: j['explanation'] as String? ?? ((j['explanation_steps'] as List?)?.cast<String>().join('\n') ?? ''),
  );
}

class IllustratedSlide {
  final int index; final String title, body;
  const IllustratedSlide({required this.index, required this.title, required this.body});
  factory IllustratedSlide.fromJson(Map<String, dynamic> j) => IllustratedSlide(index: j['index'] as int, title: j['title'] as String, body: j['body'] as String);
}

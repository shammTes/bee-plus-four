class UnitNote {
  final String grade;
  final String subject;
  final int unitNumber;
  final String title;
  final String summary;
  final List<String> keyTerms;

  const UnitNote({
    required this.grade,
    required this.subject,
    required this.unitNumber,
    required this.title,
    required this.summary,
    this.keyTerms = const [],
  });

  factory UnitNote.fromJson(Map<String, dynamic> j) => UnitNote(
        grade: j['grade'] as String? ?? 'G10',
        subject: j['subject'] as String? ?? 'MATH',
        unitNumber: (j['unit_number'] as num?)?.toInt() ?? 0,
        title: j['title'] as String? ?? 'Unit',
        summary: j['summary'] as String? ?? '',
        keyTerms: (j['key_terms'] as List?)?.map((e) => '$e').toList() ??
            const [],
      );
}

class PracticeQuestion {
  final String id;
  final String grade;
  final String subject;
  final int unitNumber;
  final String prompt;
  final List<String> options;
  final int correctIndex;
  final String explanation;

  const PracticeQuestion({
    required this.id,
    required this.grade,
    required this.subject,
    this.unitNumber = 0,
    required this.prompt,
    required this.options,
    required this.correctIndex,
    required this.explanation,
  });

  factory PracticeQuestion.fromJson(Map<String, dynamic> j) => PracticeQuestion(
        id: '${j['id'] ?? ''}',
        grade: j['grade'] as String? ?? 'G10',
        subject: j['subject'] as String? ?? 'MATH',
        unitNumber: (j['unit_number'] as num?)?.toInt() ??
            (j['unit'] as num?)?.toInt() ??
            0,
        prompt: j['prompt'] as String? ?? j['question'] as String? ?? '',
        options: ((j['options'] as List?) ?? const [])
            .map((e) => '$e')
            .toList(),
        correctIndex: (j['correct_index'] as num?)?.toInt() ?? 0,
        explanation: j['explanation'] as String? ??
            ((j['explanation_steps'] as List?)?.map((e) => '$e').join('\n') ??
                ''),
      );
}

class IllustratedSlide {
  final int index;
  final String title;
  final String body;

  const IllustratedSlide({
    required this.index,
    required this.title,
    required this.body,
  });

  factory IllustratedSlide.fromJson(Map<String, dynamic> j) => IllustratedSlide(
        index: (j['index'] as num?)?.toInt() ?? 0,
        title: j['title'] as String? ?? '',
        body: j['body'] as String? ?? '',
      );
}

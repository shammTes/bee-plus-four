/// Matric / model extracted questions (no ExamCatalog — lives in content_models).
class MatricQuestion {
  final String id;
  final String paperId;
  final int year;
  final String subject;
  final String examType;
  final String section;
  final int number;
  final String prompt;
  final List<String> options;
  final int correctIndex;
  final List<String> explanationSteps;
  final String correctAnswerText;
  final List<UnitLink> unitLinks;
  final List<String> topics;
  final List<SimilarQuestion> similarQuestions;

  const MatricQuestion({
    required this.id,
    required this.paperId,
    required this.year,
    required this.subject,
    required this.examType,
    required this.section,
    required this.number,
    required this.prompt,
    required this.options,
    required this.correctIndex,
    required this.explanationSteps,
    required this.correctAnswerText,
    required this.unitLinks,
    required this.topics,
    required this.similarQuestions,
  });

  factory MatricQuestion.fromJson(Map<String, dynamic> j) {
    final steps = j['explanation_steps'];
    List<String> exp = const [];
    if (steps is List) {
      exp = steps.map((e) => '$e').toList();
    } else if (j['explanation'] is String) {
      final s = (j['explanation'] as String).trim();
      if (s.isNotEmpty) exp = [s];
    }
    final opts = ((j['options'] as List?) ?? const []).map((e) => '$e').toList();
    var ci = (j['correct_index'] as num?)?.toInt() ?? -1;
    if (ci < 0 || (opts.isNotEmpty && ci >= opts.length)) {
      if (ci < 0) ci = -1;
      else ci = 0;
    }
    if (exp.isEmpty && ci >= 0 && opts.isNotEmpty) {
      exp = [
        'Correct option is (${String.fromCharCode(65 + ci)}) ${opts[ci]}.',
        'Review the related unit notes for this topic.',
      ];
    }
    return MatricQuestion(
      id: '${j['id'] ?? ''}',
      paperId: j['paper_id'] as String? ?? '',
      year: (j['year'] as num?)?.toInt() ?? 0,
      subject: (j['subject'] as String? ?? 'MATH').toUpperCase(),
      examType: j['exam_type'] as String? ?? 'matriculation',
      section: j['section'] as String? ?? '',
      number: (j['number'] as num?)?.toInt() ?? 0,
      prompt: j['prompt'] as String? ?? j['question'] as String? ?? '',
      options: opts,
      correctIndex: ci,
      explanationSteps: exp,
      correctAnswerText: j['correct_answer_text'] as String? ??
          (ci >= 0 && opts.isNotEmpty ? opts[ci] : ''),
      unitLinks: ((j['unit_links'] as List?) ?? const [])
          .whereType<Map>()
          .map((e) => UnitLink.fromJson(Map<String, dynamic>.from(e)))
          .toList(),
      topics: ((j['topics'] as List?) ?? const []).map((e) => '$e').toList(),
      similarQuestions: ((j['similar_questions'] as List?) ?? const [])
          .whereType<Map>()
          .map((e) => SimilarQuestion.fromJson(Map<String, dynamic>.from(e)))
          .toList(),
    );
  }

  String get explanationJoined => explanationSteps.isEmpty
      ? correctAnswerText
      : explanationSteps
          .asMap()
          .entries
          .map((e) => '${e.key + 1}. ${e.value}')
          .join('\n');
}

class UnitLink {
  final String grade;
  final String subject;
  final int unitNumber;
  final String unitTitleHint;

  const UnitLink({
    required this.grade,
    required this.subject,
    required this.unitNumber,
    required this.unitTitleHint,
  });

  factory UnitLink.fromJson(Map<String, dynamic> j) => UnitLink(
        grade: j['grade'] as String? ?? '',
        subject: j['subject'] as String? ?? '',
        unitNumber: (j['unit_number'] as num?)?.toInt() ?? 0,
        unitTitleHint: j['unit_title_hint'] as String? ?? '',
      );

  String get key => '$grade|$subject|$unitNumber';
}

class SimilarQuestion {
  final String id;
  final String prompt;
  final List<String> options;
  final int correctIndex;
  final String explanation;
  final String topic;

  const SimilarQuestion({
    required this.id,
    required this.prompt,
    required this.options,
    required this.correctIndex,
    required this.explanation,
    required this.topic,
  });

  factory SimilarQuestion.fromJson(Map<String, dynamic> j) => SimilarQuestion(
        id: '${j['id'] ?? ''}',
        prompt: j['prompt'] as String? ?? '',
        options: ((j['options'] as List?) ?? const []).map((e) => '$e').toList(),
        correctIndex: (j['correct_index'] as num?)?.toInt() ?? 0,
        explanation: j['explanation'] as String? ?? '',
        topic: j['topic'] as String? ?? '',
      );
}

class MatricBundle {
  final String accuracyPolicy;
  final List<MatricQuestion> questions;
  final Map<String, List<String>> unitIndex;

  const MatricBundle({
    required this.accuracyPolicy,
    required this.questions,
    required this.unitIndex,
  });

  factory MatricBundle.fromJson(dynamic raw) {
    if (raw is List) {
      return MatricBundle(
        accuracyPolicy: 'list_bank',
        questions: raw
            .whereType<Map>()
            .map((e) => MatricQuestion.fromJson(Map<String, dynamic>.from(e)))
            .toList(),
        unitIndex: const {},
      );
    }
    final j = Map<String, dynamic>.from(raw as Map);
    final idx = <String, List<String>>{};
    final unitRaw = j['unit_index'] as Map<String, dynamic>? ?? {};
    unitRaw.forEach((k, v) {
      idx[k] = (v as List).map((e) => '$e').toList();
    });
    return MatricBundle(
      accuracyPolicy: j['accuracy_policy'] as String? ?? '',
      questions: ((j['questions'] as List?) ?? const [])
          .whereType<Map>()
          .map((e) => MatricQuestion.fromJson(Map<String, dynamic>.from(e)))
          .toList(),
      unitIndex: idx,
    );
  }
}

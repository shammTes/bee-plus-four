/// Matric / model extracted question with explanations, unit links, similars.
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

  factory MatricQuestion.fromJson(Map<String, dynamic> j) => MatricQuestion(
        id: j['id'] as String,
        paperId: j['paper_id'] as String? ?? '',
        year: j['year'] as int? ?? 0,
        subject: j['subject'] as String,
        examType: j['exam_type'] as String? ?? 'matriculation',
        section: j['section'] as String? ?? '',
        number: j['number'] as int? ?? 0,
        prompt: j['prompt'] as String,
        options: (j['options'] as List).cast<String>(),
        correctIndex: j['correct_index'] as int,
        explanationSteps: (j['explanation_steps'] as List?)?.cast<String>() ?? const [],
        correctAnswerText: j['correct_answer_text'] as String? ?? '',
        unitLinks: ((j['unit_links'] as List?) ?? const [])
            .map((e) => UnitLink.fromJson(e as Map<String, dynamic>))
            .toList(),
        topics: (j['topics'] as List?)?.cast<String>() ?? const [],
        similarQuestions: ((j['similar_questions'] as List?) ?? const [])
            .map((e) => SimilarQuestion.fromJson(e as Map<String, dynamic>))
            .toList(),
      );

  String get explanationJoined => explanationSteps.isEmpty
      ? correctAnswerText
      : explanationSteps.asMap().entries.map((e) => '${e.key + 1}. ${e.value}').join('\n');
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
        grade: j['grade'] as String,
        subject: j['subject'] as String,
        unitNumber: j['unit_number'] as int,
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
        id: j['id'] as String,
        prompt: j['prompt'] as String,
        options: (j['options'] as List).cast<String>(),
        correctIndex: j['correct_index'] as int,
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

  factory MatricBundle.fromJson(Map<String, dynamic> j) {
    final idx = <String, List<String>>{};
    final raw = j['unit_index'] as Map<String, dynamic>? ?? {};
    raw.forEach((k, v) {
      idx[k] = (v as List).cast<String>();
    });
    return MatricBundle(
      accuracyPolicy: j['accuracy_policy'] as String? ?? '',
      questions: ((j['questions'] as List?) ?? const [])
          .map((e) => MatricQuestion.fromJson(e as Map<String, dynamic>))
          .toList(),
      unitIndex: idx,
    );
  }
}

/// Matric / model / school extracted questions.
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

  String get displayTitle {
    final s = subject.replaceAll('_', ' ');
    final pretty = s.isEmpty
        ? subject
        : s
            .split(' ')
            .map((w) => w.isEmpty
                ? w
                : '${w[0].toUpperCase()}${w.substring(1).toLowerCase()}')
            .join(' ');
    return '$pretty $year';
  }

  factory MatricQuestion.fromJson(Map<String, dynamic> j) {
    final steps = j['explanation_steps'];
    List<String> exp = const [];
    if (steps is List) {
      exp = steps.map((e) => '$e').toList();
    } else if (j['explanation'] is String) {
      exp = [j['explanation'] as String];
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
      options: ((j['options'] as List?) ?? const []).map((e) => '$e').toList(),
      correctIndex: (j['correct_index'] as num?)?.toInt() ?? -1,
      explanationSteps: exp,
      correctAnswerText: j['correct_answer_text'] as String? ?? '',
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

class ExamPaper {
  final String id;
  final String type;
  final String subject;
  final int year;
  final String title;
  final String driveFileId;
  final String source;
  final bool interactive;
  final String mappedSubject;
  final int questionCount;

  const ExamPaper({
    required this.id,
    required this.type,
    required this.subject,
    required this.year,
    required this.title,
    required this.driveFileId,
    required this.source,
    required this.interactive,
    required this.mappedSubject,
    required this.questionCount,
  });

  String get shortTitle {
    final s = subject.replaceAll('_', ' ');
    final pretty = s
        .split(' ')
        .map((w) => w.isEmpty
            ? w
            : '${w[0].toUpperCase()}${w.substring(1).toLowerCase()}')
        .join(' ');
    final base = '$pretty $year';
    if (type == 'model') return '$base (Model)';
    if (type == 'school') return '$base (School)';
    return base;
  }

  factory ExamPaper.fromJson(Map<String, dynamic> j) => ExamPaper(
        id: j['id'] as String? ?? '',
        type: j['type'] as String? ?? 'matriculation',
        subject: j['subject'] as String? ?? '',
        year: (j['year'] as num?)?.toInt() ?? 0,
        title: j['title'] as String? ?? '',
        driveFileId: j['drive_file_id'] as String? ?? '',
        source: j['source'] as String? ?? '',
        interactive: j['interactive'] as bool? ?? true,
        mappedSubject:
            j['mapped_subject'] as String? ?? j['subject'] as String? ?? '',
        questionCount: (j['question_count'] as num?)?.toInt() ?? 0,
      );
}

class ModelExamYear {
  final String label;
  final String folderId;
  final String type;

  const ModelExamYear({
    required this.label,
    required this.folderId,
    this.type = 'model',
  });

  factory ModelExamYear.fromJson(dynamic j) {
    if (j is num || j is String) {
      return ModelExamYear(label: '$j', folderId: '', type: 'model');
    }
    final m = Map<String, dynamic>.from(j as Map);
    return ModelExamYear(
      label: m['label'] as String? ?? '${m['year'] ?? ''}',
      folderId: m['folder_id'] as String? ?? '',
      type: m['type'] as String? ?? 'model',
    );
  }
}

class ExamCatalog {
  final String accuracyNote;
  final List<ExamPaper> matriculation;
  final List<ExamPaper> model;
  final List<ExamPaper> school;
  final List<ModelExamYear> modelYears;
  final int defaultQuestionCount;
  final int secondsPerQuestion;
  final List<String> gradesPriority;

  const ExamCatalog({
    required this.accuracyNote,
    required this.matriculation,
    this.model = const [],
    this.school = const [],
    required this.modelYears,
    this.defaultQuestionCount = 20,
    this.secondsPerQuestion = 90,
    this.gradesPriority = const ['G11', 'G10', 'G9'],
  });

  factory ExamCatalog.fromJson(Map<String, dynamic> j) {
    final defaults = j['adaptive_defaults'] as Map<String, dynamic>? ?? {};
    return ExamCatalog(
      accuracyNote: j['accuracy_note'] as String? ?? '',
      matriculation: ((j['matriculation'] as List?) ?? const [])
          .whereType<Map>()
          .map((e) => ExamPaper.fromJson(Map<String, dynamic>.from(e)))
          .toList(),
      model: ((j['model'] as List?) ?? const [])
          .whereType<Map>()
          .map((e) => ExamPaper.fromJson(Map<String, dynamic>.from(e)))
          .toList(),
      school: ((j['school'] as List?) ?? const [])
          .whereType<Map>()
          .map((e) => ExamPaper.fromJson(Map<String, dynamic>.from(e)))
          .toList(),
      modelYears: ((j['model_exam_years'] as List?) ?? const [])
          .map((e) => ModelExamYear.fromJson(e))
          .toList(),
      defaultQuestionCount:
          (defaults['question_count'] as num?)?.toInt() ?? 20,
      secondsPerQuestion:
          (defaults['seconds_per_question'] as num?)?.toInt() ?? 90,
      gradesPriority:
          ((j['grades_priority'] as List?) ?? const ['G11', 'G10', 'G9'])
              .map((e) => '$e')
              .toList(),
    );
  }
}

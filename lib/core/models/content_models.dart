class UnitNote {
  final String grade;
  final String subject;
  final int unitNumber;
  final String title;
  final String summary;
  final List<String> keyTerms;
  final List<String> keyIdeas;
  final List<NoteSection> sections;
  final List<NoteExample> examples;
  final List<NoteExercise> exercises;

  const UnitNote({
    required this.grade,
    required this.subject,
    required this.unitNumber,
    required this.title,
    required this.summary,
    this.keyTerms = const [],
    this.keyIdeas = const [],
    this.sections = const [],
    this.examples = const [],
    this.exercises = const [],
  });

  factory UnitNote.fromJson(Map<String, dynamic> j) => UnitNote(
        grade: '${j['grade'] ?? ''}',
        subject: '${j['subject'] ?? ''}',
        unitNumber: (j['unit_number'] as num?)?.toInt() ?? 0,
        title: '${j['title'] ?? ''}',
        summary: j['summary'] as String? ?? '',
        keyTerms: (j['key_terms'] as List?)?.map((e) => '$e').toList() ?? const [],
        keyIdeas: (j['key_ideas'] as List?)?.map((e) => '$e').toList() ?? const [],
        sections: ((j['sections'] as List?) ?? const [])
            .map((e) => NoteSection.fromJson(e as Map<String, dynamic>))
            .toList(),
        examples: ((j['examples'] as List?) ?? const [])
            .map((e) => NoteExample.fromJson(e as Map<String, dynamic>))
            .toList(),
        exercises: ((j['exercises'] as List?) ?? const [])
            .map((e) => NoteExercise.fromJson(e as Map<String, dynamic>))
            .toList(),
      );
}

class NoteSection {
  final String heading;
  final String explanation;
  const NoteSection({required this.heading, required this.explanation});
  factory NoteSection.fromJson(Map<String, dynamic> j) => NoteSection(
        heading: '${j['heading'] ?? ''}',
        explanation: '${j['explanation'] ?? ''}',
      );
}

class NoteExample {
  final String id;
  final String prompt;
  final String solution;
  const NoteExample({required this.id, required this.prompt, required this.solution});
  factory NoteExample.fromJson(Map<String, dynamic> j) => NoteExample(
        id: '${j['id'] ?? ''}',
        prompt: '${j['prompt'] ?? ''}',
        solution: '${j['solution'] ?? ''}',
      );
}

class NoteExercise {
  final String id;
  final String type;
  final String prompt;
  final String answer;
  final String explanation;
  const NoteExercise({
    required this.id,
    required this.type,
    required this.prompt,
    required this.answer,
    required this.explanation,
  });
  factory NoteExercise.fromJson(Map<String, dynamic> j) => NoteExercise(
        id: '${j['id'] ?? ''}',
        type: '${j['type'] ?? 'practice'}',
        prompt: '${j['prompt'] ?? ''}',
        answer: '${j['answer'] ?? ''}',
        explanation: '${j['explanation'] ?? ''}',
      );
}

class PracticeQuestion {
  final String id;
  final String grade;
  final String subject;
  final String prompt;
  final List<String> options;
  final int correctIndex;
  final String explanation;

  const PracticeQuestion({
    required this.id,
    required this.grade,
    required this.subject,
    required this.prompt,
    required this.options,
    required this.correctIndex,
    required this.explanation,
  });

  factory PracticeQuestion.fromJson(Map<String, dynamic> j) {
    final opts = (j['options'] as List?)?.map((e) => '$e').toList() ?? const <String>[];
    var ci = 0;
    final rawCi = j['correct_index'];
    if (rawCi is int) {
      ci = rawCi;
    } else if (rawCi is num) {
      ci = rawCi.toInt();
    }
    if (ci < 0 || (opts.isNotEmpty && ci >= opts.length)) ci = 0;
    return PracticeQuestion(
      id: '${j['id'] ?? j['question_id'] ?? 'q_${j.hashCode}'}',
      grade: '${j['grade'] ?? 'G10'}',
      subject: '${j['subject'] ?? 'MATH'}',
      prompt: '${j['prompt'] ?? j['question'] ?? ''}',
      options: opts,
      correctIndex: ci,
      explanation: j['explanation'] as String? ??
          ((j['explanation_steps'] as List?)?.map((e) => '$e').join('\n') ?? ''),
    );
  }
}

class IllustratedSlide {
  final int index;
  final String title;
  final String body;
  final String? image;

  const IllustratedSlide({
    required this.index,
    required this.title,
    required this.body,
    this.image,
  });

  factory IllustratedSlide.fromJson(Map<String, dynamic> j) => IllustratedSlide(
        index: j['index'] as int? ?? 0,
        title: j['title'] as String? ?? '',
        body: j['body'] as String? ?? '',
        image: j['image'] as String?,
      );
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
  });

  factory ExamPaper.fromJson(Map<String, dynamic> j) => ExamPaper(
        id: j['id'] as String,
        type: j['type'] as String? ?? 'matriculation',
        subject: j['subject'] as String,
        year: j['year'] as int,
        title: j['title'] as String,
        driveFileId: j['drive_file_id'] as String? ?? '',
        source: j['source'] as String? ?? '',
        interactive: j['interactive'] as bool? ?? true,
        mappedSubject: j['mapped_subject'] as String? ?? j['subject'] as String,
      );
}

class ModelExamYear {
  final String label;
  final String folderId;

  const ModelExamYear({required this.label, required this.folderId});

  factory ModelExamYear.fromJson(Map<String, dynamic> j) => ModelExamYear(
        label: j['label'] as String,
        folderId: j['folder_id'] as String? ?? '',
      );
}

class ExamCatalog {
  final String accuracyNote;
  final List<ExamPaper> matriculation;
  final List<ModelExamYear> modelYears;
  final int defaultQuestionCount;
  final int secondsPerQuestion;
  final List<String> gradesPriority;

  const ExamCatalog({
    required this.accuracyNote,
    required this.matriculation,
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
          .map((e) => ExamPaper.fromJson(e as Map<String, dynamic>))
          .toList(),
      modelYears: ((j['model_exam_years'] as List?) ?? const [])
          .map((e) => ModelExamYear.fromJson(e as Map<String, dynamic>))
          .toList(),
      defaultQuestionCount: defaults['question_count'] as int? ?? 20,
      secondsPerQuestion: defaults['seconds_per_question'] as int? ?? 90,
      gradesPriority:
          (defaults['grades_priority'] as List?)?.cast<String>() ??
              const ['G11', 'G10', 'G9'],
    );
  }
}

class TextbookBook {
  TextbookBook({
    required this.id,
    required this.grade,
    required this.subject,
    required this.title,
    required this.pdfAsset,
    this.sizeBytes = 0,
  });

  final String id;
  final String grade;
  final String subject;
  final String title;
  final String pdfAsset;
  final int sizeBytes;

  factory TextbookBook.fromJson(Map<String, dynamic> j) => TextbookBook(
        id: '${j['id'] ?? ''}',
        grade: '${j['grade'] ?? ''}',
        subject: '${j['subject'] ?? ''}',
        title: '${j['title'] ?? j['id'] ?? 'Textbook'}',
        pdfAsset: '${j['pdf_asset'] ?? ''}',
        sizeBytes: (j['size_bytes'] as num?)?.toInt() ?? 0,
      );
}

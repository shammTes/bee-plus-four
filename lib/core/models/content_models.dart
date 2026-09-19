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
        grade: j['grade'] as String,
        subject: j['subject'] as String,
        unitNumber: j['unit_number'] as int,
        title: j['title'] as String,
        summary: j['summary'] as String? ?? '',
        keyTerms: (j['key_terms'] as List?)?.cast<String>() ?? const [],
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

/// Official paper index entry (matriculation / model). Verified against Drive files.
class ExamPaper {
  final String id;
  final String type; // matriculation | model | semester
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

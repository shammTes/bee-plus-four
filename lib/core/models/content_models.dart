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
            .map((e) => NoteSection.fromJson(Map<String, dynamic>.from(e as Map)))
            .toList(),
        examples: ((j['examples'] as List?) ?? const [])
            .map((e) => NoteExample.fromJson(Map<String, dynamic>.from(e as Map)))
            .toList(),
        exercises: ((j['exercises'] as List?) ?? const [])
            .map((e) => NoteExercise.fromJson(Map<String, dynamic>.from(e as Map)))
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
      unitNumber: (j['unit_number'] as num?)?.toInt() ?? 0,
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

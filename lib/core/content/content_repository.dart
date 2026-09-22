import 'dart:convert';
import 'dart:math';

import 'package:flutter/services.dart';

import '../models/content_models.dart';
import '../models/exam_models.dart';

/// Loads curriculum + exam catalogue. Fail-soft + session cache.
class ContentRepository {
  ContentRepository._();
  static final instance = ContentRepository._();

  List<UnitNote>? _notes;
  List<PracticeQuestion>? _questions;
  Map<String, List<IllustratedSlide>>? _slides;
  ExamCatalog? _exams;
  MatricBundle? _matric;
  List<Map<String, dynamic>>? _flashcards;
  final _rng = Random();

  Future<void> preload() async {
    await Future.wait([
      notes(),
      questions(),
      allSlides(),
      examCatalog(),
      matricBundle(),
      flashcards(),
    ]);
  }

  Future<List<UnitNote>> notes() async {
    if (_notes != null) return _notes!;
    final byKey = <String, UnitNote>{};

    Future<void> ingest(String path) async {
      final list = await _loadList(path, (e) => UnitNote.fromJson(e));
      for (final n in list) {
        final k = '${n.grade}|${n.subject}|${n.unitNumber}';
        final prev = byKey[k];
        if (prev == null || n.summary.length > prev.summary.length) {
          byKey[k] = n;
        }
      }
    }

    await ingest('assets/content/unit_notes.json');
    for (final pack in [
      'assets/content/unit_notes_g12.json',
      'assets/content/unit_notes_g9_english.json',
      'assets/content/unit_notes_extra.json',
      'assets/content/unit_notes_rich.json',
    ]) {
      try {
        await ingest(pack);
      } catch (_) {}
    }

    _notes = byKey.values.toList()
      ..sort((a, b) {
        final g = a.grade.compareTo(b.grade);
        if (g != 0) return g;
        final s = a.subject.compareTo(b.subject);
        if (s != 0) return s;
        return a.unitNumber.compareTo(b.unitNumber);
      });
    return _notes!;
  }

  Future<List<Map<String, dynamic>>> flashcards() async {
    if (_flashcards != null) return _flashcards!;
    try {
      final raw =
          await rootBundle.loadString('assets/content/flashcards.json');
      final decoded = jsonDecode(raw);
      if (decoded is List) {
        _flashcards = decoded
            .whereType<Map>()
            .map((e) => Map<String, dynamic>.from(e))
            .toList();
      } else {
        _flashcards = [];
      }
    } catch (_) {
      _flashcards = [];
    }
    return _flashcards!;
  }

  Future<List<Map<String, dynamic>>> flashcardsFor(
      String grade, String subject) async {
    final all = await flashcards();
    return all
        .where((c) => c['grade'] == grade && c['subject'] == subject)
        .toList();
  }

  Future<List<PracticeQuestion>> questions() async {
    if (_questions != null) return _questions!;
    try {
      final idxRaw =
          await rootBundle.loadString('assets/content/practice_index.json');
      final idx = jsonDecode(idxRaw) as Map<String, dynamic>;
      final files = ((idx['files'] as List?) ?? const []).map((e) => '$e');
      final all = <PracticeQuestion>[];
      for (final f in files) {
        final path = f.startsWith('assets/') ? f : 'assets/content/$f';
        all.addAll(await _loadList(path, (e) => PracticeQuestion.fromJson(e)));
      }
      if (all.isNotEmpty) {
        _questions = all;
        return _questions!;
      }
    } catch (_) {}
    _questions = await _loadList(
      'assets/content/practice_questions.json',
      (e) => PracticeQuestion.fromJson(e),
    );
    if (_questions!.isEmpty) {
      _questions = await _loadList(
        'assets/content/practice_lite.json',
        (e) => PracticeQuestion.fromJson(e),
      );
    }
    return _questions!;
  }

  Future<List<PracticeQuestion>> questionsForUnit({
    required String grade,
    required String subject,
    required int unitNumber,
  }) async {
    final byId = <String, PracticeQuestion>{};
    final practice = await questions();
    for (final q in practice) {
      if (q.subject != subject) continue;
      if (q.grade == grade &&
          (q.unitNumber == unitNumber || q.unitNumber == 0)) {
        byId[q.id] = q;
      }
    }
    if (byId.length < 5) {
      for (final q in practice) {
        if (q.subject == subject &&
            (q.unitNumber == unitNumber || q.unitNumber == 0)) {
          byId.putIfAbsent(q.id, () => q);
        }
      }
    }

    final matric = await matricBundle();
    final subj = subject.toUpperCase();
    for (final m in matric.questions) {
      if (m.subject != subj) continue;
      if (m.options.length < 3) continue;
      final linked = m.unitLinks.any((u) =>
          u.unitNumber == unitNumber &&
          (u.grade.isEmpty || u.grade == grade || u.subject == subj));
      final linkedLoose = m.unitLinks.any((u) => u.unitNumber == unitNumber);
      if (!linked && !linkedLoose) continue;
      final exp = m.explanationJoined;
      byId.putIfAbsent(
        m.id,
        () => PracticeQuestion(
          id: m.id,
          grade: grade,
          subject: subject,
          unitNumber: unitNumber,
          prompt: m.prompt,
          options: m.options,
          correctIndex: m.correctIndex < 0 ? 0 : m.correctIndex,
          explanation: exp.isEmpty
              ? (m.correctIndex < 0
                  ? 'Answer key not verified yet.'
                  : '')
              : exp,
        ),
      );
    }
    final list = byId.values.toList()..shuffle(_rng);
    return list;
  }

  Future<Map<String, List<IllustratedSlide>>> allSlides() async {
    if (_slides != null) return _slides!;
    try {
      final raw =
          await rootBundle.loadString('assets/content/illustrated_slides.json');
      final map = jsonDecode(raw) as Map<String, dynamic>;
      _slides = map.map((k, v) => MapEntry(
            k,
            ((v as List?) ?? const [])
                .whereType<Map>()
                .map((e) =>
                    IllustratedSlide.fromJson(Map<String, dynamic>.from(e)))
                .toList(),
          ));
    } catch (_) {
      _slides = {};
    }
    return _slides!;
  }

  Future<ExamCatalog> examCatalog() async {
    if (_exams != null) return _exams!;
    try {
      final raw =
          await rootBundle.loadString('assets/content/exam_catalog.json');
      _exams = ExamCatalog.fromJson(jsonDecode(raw) as Map<String, dynamic>);
    } catch (_) {
      _exams = const ExamCatalog(
        accuracyNote: '',
        matriculation: [],
        model: [],
        modelYears: [],
      );
    }
    return _exams!;
  }

  Future<MatricBundle> matricBundle() async {
    if (_matric != null) return _matric!;
    final byId = <String, MatricQuestion>{};

    Future<void> ingest(dynamic decoded) async {
      final b = MatricBundle.fromJson(decoded);
      for (final q in b.questions) {
        final prev = byId[q.id];
        if (prev == null) {
          byId[q.id] = q;
        } else if (prev.correctIndex < 0 && q.correctIndex >= 0) {
          byId[q.id] = q;
        }
      }
    }

    try {
      final raw =
          await rootBundle.loadString('assets/content/matric_questions.json');
      await ingest(jsonDecode(raw));
    } catch (_) {}

    const packs = [
      'matric_biology.json',
      'matric_chemistry.json',
      'matric_chemistry_2000.json',
      'matric_chemistry_2001.json',
      'matric_chemistry_2002.json',
      'matric_math.json',
      'matric_math_2000.json',
      'matric_math_2001.json',
      'matric_math_2002.json',
      'matric_math_2018.json',
      'matric_math_2023.json',
      'matric_physics.json',
      'matric_physics_2000.json',
      'matric_physics_2002.json',
      'matric_physics_2009.json',
      'matric_physics_2010.json',
      'matric_english.json',
      'matric_geography.json',
      'matric_history.json',
      'matric_business_economics.json',
    ];
    for (final name in packs) {
      try {
        final raw = await rootBundle.loadString('assets/content/$name');
        await ingest(jsonDecode(raw));
      } catch (_) {}
    }

    final list = byId.values.toList()
      ..sort((a, b) {
        final y = b.year.compareTo(a.year);
        if (y != 0) return y;
        final s = a.subject.compareTo(b.subject);
        if (s != 0) return s;
        return a.number.compareTo(b.number);
      });

    _matric = MatricBundle(
      accuracyPolicy: 'merged_bank',
      questions: list,
      unitIndex: const {},
    );
    return _matric!;
  }

  Future<List<MatricQuestion>> matricForSubject(String subject) async {
    final b = await matricBundle();
    final s = subject.toUpperCase();
    return b.questions.where((q) => q.subject == s).toList();
  }

  Future<List<MatricQuestion>> matricForPaper(String subject, int year) async {
    final b = await matricBundle();
    final s = subject.toUpperCase();
    return b.questions
        .where((q) => q.subject == s && q.year == year)
        .toList();
  }

  Future<List<MatricQuestion>> matricForUnit(
      String grade, String subject, int unitNumber) async {
    final b = await matricBundle();
    return b.questions
        .where((q) =>
            q.subject == subject.toUpperCase() &&
            q.unitLinks.any((u) =>
                u.unitNumber == unitNumber &&
                (u.grade.isEmpty || u.grade == grade)))
        .toList();
  }

  Future<List<UnitNote>> notesFor(String grade, String subject) async {
    final all = await notes();
    return all
        .where((n) => n.grade == grade && n.subject == subject)
        .toList()
      ..sort((a, b) => a.unitNumber.compareTo(b.unitNumber));
  }

  Future<List<PracticeQuestion>> questionsFor(
      String grade, String subject) async {
    final all = await questions();
    return all
        .where((q) => q.grade == grade && q.subject == subject)
        .toList();
  }

  Future<List<PracticeQuestion>> adaptiveExamQuestions({
    required String subject,
    int count = 20,
    List<String> gradesPriority = const ['G11', 'G10', 'G9'],
  }) async {
    final all = await questions();
    final pool = all.where((q) => q.subject == subject).toList()..shuffle(_rng);
    return pool.take(count).toList();
  }

  Future<List<IllustratedSlide>> slidesFor(String id) async {
    final all = await allSlides();
    return all[id] ?? const [];
  }

  Future<List<T>> _loadList<T>(
    String assetPath,
    T Function(Map<String, dynamic>) map,
  ) async {
    try {
      final raw = await rootBundle.loadString(assetPath);
      final decoded = jsonDecode(raw);
      if (decoded is List) {
        return decoded
            .whereType<Map>()
            .map((e) => map(Map<String, dynamic>.from(e)))
            .toList();
      }
      if (decoded is Map && decoded['items'] is List) {
        return (decoded['items'] as List)
            .whereType<Map>()
            .map((e) => map(Map<String, dynamic>.from(e)))
            .toList();
      }
      if (decoded is Map && decoded['questions'] is List) {
        return (decoded['questions'] as List)
            .whereType<Map>()
            .map((e) => map(Map<String, dynamic>.from(e)))
            .toList();
      }
    } catch (_) {}
    return [];
  }
}

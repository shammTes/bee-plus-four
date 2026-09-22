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
      'assets/content/notes_ALL_BOOKS_v2_polished.json',
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
    final g = grade.toUpperCase();
    final s = subject.toUpperCase();
    return all
        .where((c) =>
            '${c['grade']}'.toUpperCase() == g &&
            '${c['subject']}'.toUpperCase() == s)
        .toList();
  }

  Future<List<PracticeQuestion>> questions() async {
    if (_questions != null) return _questions!;
    final out = <PracticeQuestion>[];
    try {
      final idxRaw =
          await rootBundle.loadString('assets/content/practice_index.json');
      final idx = jsonDecode(idxRaw) as Map<String, dynamic>;
      final files = (idx['files'] as List? ?? []).map((e) => '$e').toList();
      for (final f in files) {
        out.addAll(await _loadList(
            'assets/content/$f', (e) => PracticeQuestion.fromJson(e)));
      }
    } catch (_) {}
    for (final name in [
      'assets/content/practice_questions.json',
      'assets/content/practice_lite.json',
      'assets/content/practice_from_notes.json',
    ]) {
      try {
        out.addAll(
            await _loadList(name, (e) => PracticeQuestion.fromJson(e)));
      } catch (_) {}
    }
    _questions = out;
    return _questions!;
  }

  Future<List<PracticeQuestion>> questionsForUnit({
    required String grade,
    required String subject,
    required int unitNumber,
  }) async {
    final all = await questions();
    final g = grade.toUpperCase();
    final s = subject.toUpperCase();
    return all
        .where((q) =>
            q.grade.toUpperCase() == g &&
            q.subject.toUpperCase() == s &&
            q.unitNumber == unitNumber)
        .toList();
  }

  Future<Map<String, List<IllustratedSlide>>> allSlides() async {
    if (_slides != null) return _slides!;
    try {
      final raw =
          await rootBundle.loadString('assets/content/illustrated_slides.json');
      final map = jsonDecode(raw) as Map<String, dynamic>;
      final out = <String, List<IllustratedSlide>>{};
      map.forEach((k, v) {
        if (v is List) {
          out[k] = v
              .whereType<Map>()
              .map((e) => IllustratedSlide.fromJson(Map<String, dynamic>.from(e)))
              .toList();
        }
      });
      _slides = out;
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
      _exams = ExamCatalog(
        accuracyNote: '',
        matriculation: const [],
        model: const [],
        modelExamYears: const [],
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
        .where((q) => q.unitLinks.any((u) =>
            u.grade.toUpperCase() == grade.toUpperCase() &&
            u.subject.toUpperCase() == subject.toUpperCase() &&
            u.unitNumber == unitNumber))
        .toList();
  }

  Future<List<UnitNote>> notesFor(String grade, String subject) async {
    final all = await notes();
    final g = grade.toUpperCase();
    final s = subject.toUpperCase();
    return all
        .where((n) => n.grade.toUpperCase() == g && n.subject.toUpperCase() == s)
        .toList();
  }

  Future<List<PracticeQuestion>> questionsFor(
      String grade, String subject) async {
    final all = await questions();
    final g = grade.toUpperCase();
    final s = subject.toUpperCase();
    return all
        .where((q) => q.grade.toUpperCase() == g && q.subject.toUpperCase() == s)
        .toList();
  }

  Future<List<PracticeQuestion>> adaptiveExamQuestions({
    required String grade,
    required String subject,
    int limit = 20,
  }) async {
    final list = await questionsFor(grade, subject);
    list.shuffle(_rng);
    return list.take(limit).toList();
  }

  Future<List<IllustratedSlide>> slidesFor(String id) async {
    final all = await allSlides();
    return all[id] ?? const [];
  }

  Future<List<T>> _loadList<T>(
    String path,
    T Function(Map<String, dynamic>) map,
  ) async {
    try {
      final raw = await rootBundle.loadString(path);
      final decoded = jsonDecode(raw);
      final list = decoded is List
          ? decoded
          : (decoded is Map
              ? (decoded['questions'] as List? ??
                  decoded['notes'] as List? ??
                  decoded['items'] as List? ??
                  const [])
              : const []);
      return list
          .whereType<Map>()
          .map((e) => map(Map<String, dynamic>.from(e)))
          .toList();
    } catch (_) {
      return [];
    }
  }
}

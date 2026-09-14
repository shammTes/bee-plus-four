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
  final _rng = Random();

  Future<void> preload() async {
    await Future.wait([
      notes(),
      questions(),
      allSlides(),
      examCatalog(),
      matricBundle(),
    ]);
  }

  Future<List<UnitNote>> notes() async {
    if (_notes != null) return _notes!;
    _notes = await _loadList(
      'assets/content/unit_notes.json',
      (e) => UnitNote.fromJson(e),
    );
    return _notes!;
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
        // Prefer entries with verified keys over no-key duplicates
        final prev = byId[q.id];
        if (prev == null) {
          byId[q.id] = q;
        } else if (prev.correctIndex < 0 && q.correctIndex >= 0) {
          byId[q.id] = q;
        }
      }
    }

    // Primary unified bank (from CI pack or repo)
    try {
      final raw =
          await rootBundle.loadString('assets/content/matric_questions.json');
      await ingest(jsonDecode(raw));
    } catch (_) {}

    // Subject + year packs (accuracy-first incremental parses)
    const packs = [
      'matric_biology.json',
      'matric_chemistry.json',
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
      accuracyPolicy:
          'merged_bank_accuracy_first: verified keys preferred; -1 = awaiting key',
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
    } catch (_) {}
    return [];
  }
}

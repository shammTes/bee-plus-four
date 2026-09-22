import 'dart:convert';

import 'package:flutter/services.dart';

import '../models/content_models.dart';
import '../models/exam_models.dart';

class ContentRepository {
  ContentRepository._();
  static final ContentRepository instance = ContentRepository._();

  List<UnitNote>? _notes;
  MatricBundle? _matric;
  ExamCatalog? _exams;
  List<PracticeQuestion>? _practice;
  Map<String, dynamic>? _illustratedSlides;

  Future<void> warmUp() async {
    await notes();
    await practiceQuestions();
    await matricBundle();
    await examCatalog();
  }

  Future<List<UnitNote>> notes() async {
    if (_notes != null) return _notes!;
    final byKey = <String, UnitNote>{};

    Future<void> ingest(String asset) async {
      try {
        final raw = await rootBundle.loadString(asset);
        final decoded = jsonDecode(raw);
        final list = decoded is List ? decoded : (decoded['notes'] as List? ?? []);
        for (final e in list) {
          if (e is! Map) continue;
          final n = UnitNote.fromJson(Map<String, dynamic>.from(e));
          final k = '${n.grade}|${n.subject}|${n.unitNumber}';
          final prev = byKey[k];
          if (prev == null ||
              n.sections.length > prev.sections.length ||
              n.summary.length > prev.summary.length) {
            byKey[k] = n;
          }
        }
      } catch (_) {}
    }

    await ingest('assets/content/unit_notes.json');
    for (final extra in [
      'assets/content/unit_notes_g12.json',
      'assets/content/unit_notes_g9_english.json',
      'assets/content/unit_notes_extra.json',
      'assets/content/unit_notes_rich.json',
    ]) {
      await ingest(extra);
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

  Future<List<UnitNote>> notesFor(String grade, String subject) async {
    final all = await notes();
    final g = grade.toUpperCase();
    final s = subject.toUpperCase();
    return all
        .where((n) => n.grade.toUpperCase() == g && n.subject.toUpperCase() == s)
        .toList();
  }

  Future<List<PracticeQuestion>> practiceQuestions() async {
    if (_practice != null) return _practice!;
    final out = <PracticeQuestion>[];
    try {
      final idxRaw =
          await rootBundle.loadString('assets/content/practice_index.json');
      final idx = jsonDecode(idxRaw) as Map<String, dynamic>;
      final files = (idx['files'] as List? ?? []).map((e) => '$e').toList();
      for (final f in files) {
        try {
          final raw = await rootBundle.loadString('assets/content/$f');
          final decoded = jsonDecode(raw);
          final list = decoded is List
              ? decoded
              : (decoded['questions'] as List? ?? []);
          for (final e in list) {
            if (e is Map) {
              out.add(PracticeQuestion.fromJson(Map<String, dynamic>.from(e)));
            }
          }
        } catch (_) {}
      }
    } catch (_) {}
    for (final name in [
      'assets/content/practice_questions.json',
      'assets/content/practice_lite.json',
      'assets/content/practice_from_notes.json',
    ]) {
      try {
        final raw = await rootBundle.loadString(name);
        final decoded = jsonDecode(raw);
        final list =
            decoded is List ? decoded : (decoded['questions'] as List? ?? []);
        for (final e in list) {
          if (e is Map) {
            out.add(PracticeQuestion.fromJson(Map<String, dynamic>.from(e)));
          }
        }
      } catch (_) {}
    }
    _practice = out;
    return _practice!;
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

  Future<ExamCatalog> examCatalog() async {
    if (_exams != null) return _exams!;
    try {
      final raw =
          await rootBundle.loadString('assets/content/exam_catalog.json');
      _exams = ExamCatalog.fromJson(jsonDecode(raw) as Map<String, dynamic>);
    } catch (_) {
      _exams = ExamCatalog(
        accuracyNote: '',
        matriculation: [],
        model: [],
        modelExamYears: [],
      );
    }
    return _exams!;
  }
}

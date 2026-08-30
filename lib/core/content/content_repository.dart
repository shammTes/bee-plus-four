import 'dart:convert';
import 'dart:math';

import 'package:flutter/services.dart';

import '../models/content_models.dart';

/// Loads curriculum + exam catalogue. Fail-soft + session cache.
class ContentRepository {
  ContentRepository._();
  static final instance = ContentRepository._();

  List<UnitNote>? _notes;
  List<PracticeQuestion>? _questions;
  Map<String, List<IllustratedSlide>>? _slides;
  ExamCatalog? _exams;
  final _rng = Random();

  Future<void> preload() async {
    await Future.wait([notes(), questions(), allSlides(), examCatalog()]);
  }

  Future<List<UnitNote>> notes() async {
    if (_notes != null) return _notes!;
    _notes = await _loadList('assets/content/unit_notes.json', UnitNote.fromJson);
    return _notes!;
  }

  Future<List<PracticeQuestion>> questions() async {
    if (_questions != null) return _questions!;
    final all = <PracticeQuestion>[];
    try {
      final raw = await rootBundle.loadString('assets/content/practice_index.json');
      final map = jsonDecode(raw) as Map<String, dynamic>;
      final files = (map['files'] as List?)?.cast<String>() ?? const [];
      for (final f in files) {
        all.addAll(await _loadList('assets/content/$f', PracticeQuestion.fromJson));
      }
      if (all.isEmpty && map['lite'] is String) {
        all.addAll(await _loadList('assets/content/${map['lite']}', PracticeQuestion.fromJson));
      }
    } catch (_) {
      all.addAll(await _loadList('assets/content/practice_lite.json', PracticeQuestion.fromJson));
      if (all.isEmpty) {
        all.addAll(await _loadList('assets/content/practice_questions.json', PracticeQuestion.fromJson));
      }
    }
    _questions = all;
    return _questions!;
  }

  Future<Map<String, List<IllustratedSlide>>> allSlides() async {
    if (_slides != null) return _slides!;
    try {
      final raw = await rootBundle.loadString('assets/content/illustrated_slides.json');
      final map = jsonDecode(raw) as Map<String, dynamic>;
      _slides = map.map((k, v) => MapEntry(
            k,
            (v as List).map((e) => IllustratedSlide.fromJson(e as Map<String, dynamic>)).toList(),
          ));
    } catch (_) {
      _slides = {};
    }
    return _slides!;
  }

  Future<ExamCatalog> examCatalog() async {
    if (_exams != null) return _exams!;
    try {
      final raw = await rootBundle.loadString('assets/content/exam_catalog.json');
      _exams = ExamCatalog.fromJson(jsonDecode(raw) as Map<String, dynamic>);
    } catch (_) {
      _exams = const ExamCatalog(
        accuracyNote: 'Exam catalogue not loaded.',
        matriculation: [],
        modelYears: [],
      );
    }
    return _exams!;
  }

  Future<List<UnitNote>> notesFor(String grade, String subject) async {
    final all = await notes();
    return all.where((n) => n.grade == grade && n.subject == subject).toList()
      ..sort((a, b) => a.unitNumber.compareTo(b.unitNumber));
  }

  Future<List<PracticeQuestion>> questionsFor(String grade, String subject) async {
    final all = await questions();
    final filtered = all.where((q) => q.grade == grade && q.subject == subject).toList();
    if (filtered.isNotEmpty) return filtered;
    return all.where((q) => q.grade == grade).toList();
  }

  /// Adaptive exam set: prioritizes higher grades for subject, shuffles, size-limited.
  /// Accuracy: only real curriculum MCQs — never invents paper items.
  Future<List<PracticeQuestion>> adaptiveExamQuestions({
    required String subject,
    int count = 20,
    List<String> gradesPriority = const ['G11', 'G10', 'G9'],
  }) async {
    final all = await questions();
    final pool = all.where((q) => q.subject == subject).toList();
    if (pool.isEmpty) {
      final any = List<PracticeQuestion>.from(all)..shuffle(_rng);
      return any.take(count).toList();
    }
    pool.sort((a, b) {
      final ai = gradesPriority.indexOf(a.grade);
      final bi = gradesPriority.indexOf(b.grade);
      final aa = ai < 0 ? 99 : ai;
      final bb = bi < 0 ? 99 : bi;
      return aa.compareTo(bb);
    });
    final selected = <PracticeQuestion>[];
    final used = <String>{};
    for (final g in gradesPriority) {
      final slice = pool.where((q) => q.grade == g && !used.contains(q.id)).toList()
        ..shuffle(_rng);
      final need = (count - selected.length).clamp(0, count);
      final take = (slice.length < need) ? slice.length : (need > 0 ? (need * 0.5).ceil().clamp(1, need) : 0);
      for (final q in slice.take(take)) {
        selected.add(q);
        used.add(q.id);
        if (selected.length >= count) break;
      }
      if (selected.length >= count) break;
    }
    if (selected.length < count) {
      final rest = pool.where((q) => !used.contains(q.id)).toList()..shuffle(_rng);
      for (final q in rest) {
        selected.add(q);
        if (selected.length >= count) break;
      }
    }
    selected.shuffle(_rng);
    return selected.take(count).toList();
  }

  Future<List<IllustratedSlide>> slidesFor(String id) async =>
      (await allSlides())[id] ?? const [];

  Future<List<T>> _loadList<T>(
    String asset,
    T Function(Map<String, dynamic>) fromJson,
  ) async {
    try {
      final raw = await rootBundle.loadString(asset);
      final list = jsonDecode(raw) as List;
      return list.map((e) => fromJson(e as Map<String, dynamic>)).toList(growable: false);
    } catch (_) {
      return const [];
    }
  }
}

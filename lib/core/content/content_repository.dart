import 'dart:convert';

import 'package:flutter/services.dart';

import '../models/content_models.dart';

class ContentRepository {
  ContentRepository._();
  static final instance = ContentRepository._();

  List<UnitNote>? _notes;
  List<PracticeQuestion>? _questions;
  Map<String, List<IllustratedSlide>>? _slides;

  Future<void> preload() async {
    await Future.wait([notes(), questions(), allSlides()]);
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

  Future<List<IllustratedSlide>> slidesFor(String id) async => (await allSlides())[id] ?? const [];

  Future<List<T>> _loadList<T>(String asset, T Function(Map<String, dynamic>) fromJson) async {
    try {
      final raw = await rootBundle.loadString(asset);
      final list = jsonDecode(raw) as List;
      return list.map((e) => fromJson(e as Map<String, dynamic>)).toList(growable: false);
    } catch (_) {
      return const [];
    }
  }
}

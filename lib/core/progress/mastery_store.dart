import 'package:hive_flutter/hive_flutter.dart';

/// Tracks per-unit practice mastery for adaptive exam prep.
class MasteryStore {
  MasteryStore._();
  static final instance = MasteryStore._();

  static const _boxName = 'mastery';
  Box? _box;

  Future<void> init() async {
    _box = await Hive.openBox(_boxName);
  }

  String _key(String grade, String subject, int unit) =>
      '${grade}_${subject}_$unit';

  Map<String, dynamic> stats(String grade, String subject, int unit) {
    final raw = _box?.get(_key(grade, subject, unit));
    if (raw is Map) {
      return Map<String, dynamic>.from(raw);
    }
    return {'correct': 0, 'wrong': 0, 'seen': 0};
  }

  Future<void> record(
    String grade,
    String subject,
    int unit, {
    required bool correct,
  }) async {
    final s = stats(grade, subject, unit);
    s['seen'] = (s['seen'] as int? ?? 0) + 1;
    if (correct) {
      s['correct'] = (s['correct'] as int? ?? 0) + 1;
    } else {
      s['wrong'] = (s['wrong'] as int? ?? 0) + 1;
    }
    await _box?.put(_key(grade, subject, unit), s);
  }

  /// 0.0 – 1.0 mastery score (Bayesian-ish simple ratio with floor).
  double mastery(String grade, String subject, int unit) {
    final s = stats(grade, subject, unit);
    final c = s['correct'] as int? ?? 0;
    final w = s['wrong'] as int? ?? 0;
    final total = c + w;
    if (total == 0) return 0;
    return (c + 1) / (total + 2);
  }

  String levelLabel(String grade, String subject, int unit) {
    final m = mastery(grade, subject, unit);
    final s = stats(grade, subject, unit);
    final seen = s['seen'] as int? ?? 0;
    if (seen == 0) return 'New';
    if (m < 0.4) return 'Weak';
    if (m < 0.7) return 'Building';
    if (m < 0.9) return 'Strong';
    return 'Mastered';
  }

  List<Map<String, dynamic>> weakUnits({
    required String grade,
    required String subject,
    required List<int> units,
  }) {
    final list = <Map<String, dynamic>>[];
    for (final u in units) {
      list.add({
        'unit': u,
        'mastery': mastery(grade, subject, u),
        'label': levelLabel(grade, subject, u),
        'stats': stats(grade, subject, u),
      });
    }
    list.sort((a, b) =>
        (a['mastery'] as double).compareTo(b['mastery'] as double));
    return list;
  }
}

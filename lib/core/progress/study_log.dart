import 'package:hive_flutter/hive_flutter.dart';

/// Daily study log for calendar / streaks.
class StudyLog {
  StudyLog._();
  static final instance = StudyLog._();

  static const _boxName = 'study_log';
  Box? _box;

  Future<void> init() async {
    _box = await Hive.openBox(_boxName);
  }

  String _dayKey([DateTime? d]) {
    final x = d ?? DateTime.now();
    return '${x.year}-${x.month.toString().padLeft(2, '0')}-${x.day.toString().padLeft(2, '0')}';
  }

  Future<void> markStudied({int minutes = 1}) async {
    final k = _dayKey();
    final prev = (_box?.get(k) as int?) ?? 0;
    await _box?.put(k, prev + minutes);
  }

  int minutesOn(DateTime d) => (_box?.get(_dayKey(d)) as int?) ?? 0;

  bool studiedOn(DateTime d) => minutesOn(d) > 0;

  int currentStreak() {
    var streak = 0;
    var day = DateTime.now();
    for (var i = 0; i < 60; i++) {
      if (studiedOn(day)) {
        streak++;
        day = day.subtract(const Duration(days: 1));
      } else if (i == 0) {
        // allow today empty — check yesterday start
        day = day.subtract(const Duration(days: 1));
        continue;
      } else {
        break;
      }
    }
    return streak;
  }

  /// Last 35 days for heat map (oldest → newest).
  List<({DateTime day, int minutes})> lastWeeks({int days = 35}) {
    final out = <({DateTime day, int minutes})>[];
    final today = DateTime.now();
    for (var i = days - 1; i >= 0; i--) {
      final d = DateTime(today.year, today.month, today.day)
          .subtract(Duration(days: i));
      out.add((day: d, minutes: minutesOn(d)));
    }
    return out;
  }
}

// Pure GPA maths (no Flutter): letter for a %, the 5-subject GPA, and the estimate from recent matric answers.
import 'gpa_config.dart';

GpaBand bandFor(double pct) => GpaConfig.bands.firstWhere((b) => pct >= b.minPct, orElse: () => GpaConfig.bands.last);

class SubjectGrade {
  const SubjectGrade(this.subject, this.pct, {this.answers = 0});
  final String subject;
  final double pct;
  final int answers; // 0 = entered by the student
  GpaBand get band => bandFor(pct);
}

class GpaResult {
  const GpaResult(this.gpa, this.used, this.missing);

  /// null until at least one counted subject has a grade
  final double? gpa;
  final List<SubjectGrade> used;

  /// compulsory subjects with no grade yet, and the 'best other' places still empty
  final List<String> missing;
  bool get complete => missing.isEmpty;
}

/// Mathematics + English + the best other subjects of [stream] (GpaConfig.counted in total). Until all five are known
/// the GPA is the average of the subjects that have a grade (a partial GPA; [GpaResult.missing] says what is left).
GpaResult computeGpa(Map<String, double> pctBySubject, String stream, {Map<String, int> answers = const {}}) {
  final used = <SubjectGrade>[], missing = <String>[];
  for (final c in GpaConfig.compulsory) {
    final v = pctBySubject[c];
    v == null ? missing.add(c) : used.add(SubjectGrade(c, v, answers: answers[c] ?? 0));
  }
  final others = [
    for (final s in GpaConfig.streams[stream] ?? const <String>[])
      if (pctBySubject[s] != null) SubjectGrade(s, pctBySubject[s]!, answers: answers[s] ?? 0),
  ]..sort((a, b) => b.band.points != a.band.points ? b.band.points.compareTo(a.band.points) : b.pct.compareTo(a.pct));
  final room = GpaConfig.counted - GpaConfig.compulsory.length;
  used.addAll(others.take(room));
  for (var i = others.length; i < room; i++) {
    missing.add('another ${GpaConfig.streamNames[stream] ?? ''} subject');
  }
  if (used.isEmpty) return GpaResult(null, used, missing);
  final sum = used.fold<int>(0, (a, g) => a + g.band.points);
  return GpaResult(sum / used.length, used, missing);
}

/// % right per subject from the newest answers. [events] = HighState.ev rows [t, questionId, ok 0/1, mode];
/// [subjectOf] maps a question id to its exam subject, or null to skip it (exercises, unknown ids).
({Map<String, double> pct, Map<String, int> n}) estimateFromAnswers(List<List<dynamic>> events, String? Function(String id) subjectOf) {
  final right = <String, int>{}, n = <String, int>{}, seen = <String>{};
  for (var i = events.length - 1; i >= 0; i--) {
    final e = events[i];
    if (e.length < 3) continue;
    final id = e[1];
    if (id is! String || !seen.add(id)) continue; // the newest answer to each question only
    final s = subjectOf(id);
    if (s == null || (n[s] ?? 0) >= GpaConfig.recentAnswers) continue;
    n[s] = (n[s] ?? 0) + 1;
    if (e[2] == 1 || e[2] == true) right[s] = (right[s] ?? 0) + 1;
  }
  final pct = <String, double>{}, counts = <String, int>{};
  n.forEach((s, c) {
    if (c >= GpaConfig.minAnswers) {
      pct[s] = 100 * (right[s] ?? 0) / c;
      counts[s] = c;
    }
  });
  return (pct: pct, n: counts);
}

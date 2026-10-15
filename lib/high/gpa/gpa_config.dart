// Eritrean matric (ESSCE / ESECE) GPA rules used by the 'Track my GPA' calculator. Sources: docs/gpa.md.
//
// VERIFIED:
//  - letter grades convert A = 4, B = 3, C = 2, D = 1, F = 0 (NOKUT country briefing Eritrea 2017; NOKUT recognition
//    report 2013);
//  - the GPA is the average of FIVE subjects: Mathematics, English and the three other subjects with the highest
//    results (same NOKUT sources); 2.0 is the minimum GPA for higher education.
//
// EDITABLE / NOT FULLY VERIFIED (change here if the Ministry's current rules differ):
//  - the % band for each letter: Scholaro's ESSCE table (A 75-100, B 65-74.99, C 50-64.99, D 40-49.99, F 0-39.99).
//    The NCAA guide lists A 75, B 65, C 50 and no D, so the D band is the uncertain part. Real ESSCE results may also
//    be scaled by the Ministry, so a prediction from practice scores is only a guide;
//  - which subjects belong to each stream (below).

class GpaBand {
  const GpaBand(this.letter, this.minPct, this.points);
  final String letter;
  final double minPct;
  final int points;
}

abstract final class GpaConfig {
  /// highest band first
  static const bands = [GpaBand('A', 75, 4), GpaBand('B', 65, 3), GpaBand('C', 50, 2), GpaBand('D', 40, 1), GpaBand('F', 0, 0)];

  /// always counted
  static const compulsory = ['Mathematics', 'English'];

  /// how many subjects make the GPA (compulsory + best of the rest)
  static const counted = 5;

  /// minimum GPA for higher education
  static const passGpa = 2.0;

  /// stream -> its other exam subjects (names used by the exam packs). NOT verified: edit if needed.
  static const streams = <String, List<String>>{
    'natural': ['Physics', 'Chemistry', 'Biology', 'Agriculture', 'General Science'],
    'social': ['Geography', 'History', 'Business and Economics', 'Social Studies', 'General Knowledge'],
  };

  static const streamNames = {'natural': 'Natural Science', 'social': 'Social Science'};

  /// recent answers used to estimate a subject's % (newest first), and the fewest that give an estimate
  static const recentAnswers = 60;
  static const minAnswers = 10;
}

/// Eritrean high-school streams (G11–G12) and subject availability.
/// Accuracy-first: Agriculture is Science stream only from G11.
class CurriculumStreams {
  CurriculumStreams._();

  static const science = 'SCIENCE';
  static const arts = 'ARTS';

  /// Common subjects every stream takes (also common on matric).
  static const common = ['ENGLISH', 'MATH'];

  /// Matric also includes general knowledge for all.
  static const matricCommon = ['ENGLISH', 'MATH', 'GENERAL_KNOWLEDGE'];

  static const scienceSubjects = [
    'ENGLISH',
    'MATH',
    'PHYSICS',
    'CHEMISTRY',
    'BIOLOGY',
    'AGRICULTURE',
  ];

  static const artsSubjects = [
    'ENGLISH',
    'MATH',
    'GEOGRAPHY',
    'HISTORY',
    'BUSINESS_ECONOMICS',
  ];

  /// G9–G10 core subjects (before stream split).
  static const juniorCore = [
    'ENGLISH',
    'MATH',
    'PHYSICS',
    'CHEMISTRY',
    'BIOLOGY',
    'GEOGRAPHY',
    'HISTORY',
    'BUSINESS_ECONOMICS',
  ];

  /// Subjects offered for a grade + stream.
  static List<String> subjectsFor(String grade, {String stream = science}) {
    final g = grade.toUpperCase();
    if (g == 'G9' || g == 'G10') {
      // No Agriculture in G9/G10
      return List<String>.from(juniorCore);
    }
    if (g == 'G11' || g == 'G12') {
      return stream == arts
          ? List<String>.from(artsSubjects)
          : List<String>.from(scienceSubjects);
    }
    return List<String>.from(juniorCore);
  }

  static String label(String code) {
    switch (code) {
      case 'BUSINESS_ECONOMICS':
        return 'Business';
      case 'GENERAL_KNOWLEDGE':
        return 'General knowledge';
      default:
        if (code.isEmpty) return code;
        return code[0] + code.substring(1).toLowerCase();
    }
  }
}

// Reads grade / subject / chapter from a folder path such as
// "Winner handouts_encrypted/Grade 8/Science/Chapter 01 - Living things". Pure Dart (shared by the
// 4 Encryptor and Winner; keep both copies the same).

/// What a folder path says about a file. Empty / 0 when the path does not say it.
class ResPath {
  const ResPath({this.grade = 0, this.subject = '', this.subjectLabel = '', this.unit = '', this.chapter = '', this.folder = ''});
  final int grade;

  /// notes subject id (`science`, `mathematics`, `social_studies`…) or a cleaned id of an unknown name
  final String subject;

  /// subject folder name as the user wrote it ("Social Studies")
  final String subjectLabel;

  /// chapter / unit number as text ("1"), empty when the chapter folder has no number
  final String unit;

  /// chapter folder name as written ("Chapter 01 - Living things")
  final String chapter;

  /// cleaned full path (no "_encrypted" suffixes, no empty parts)
  final String folder;
}

const _subjectAliases = <String, String>{
  'math': 'mathematics', 'maths': 'mathematics', 'mathematics': 'mathematics', 'ሒሳብ': 'mathematics', 'ሕሳብ': 'mathematics',
  'science': 'science', 'general_science': 'science', 'sciences': 'science', 'ሳይንስ': 'science',
  'english': 'english', 'english_language': 'english', 'እንግሊዝኛ': 'english',
  'social_studies': 'social_studies', 'social_study': 'social_studies', 'social_science': 'social_studies', 'socials': 'social_studies', 'ማሕበራዊ_ትምህርቲ': 'social_studies',
  'citizenship': 'citizenship', 'citizenship_education': 'citizenship', 'civics': 'civics',
  'ict': 'ict', 'computer': 'ict', 'life_skills': 'life_skills', 'lifeskills': 'life_skills', 'tigrinya': 'tigrinya', 'ትግርኛ': 'tigrinya',
  'biology': 'biology', 'chemistry': 'chemistry', 'physics': 'physics', 'geography': 'geography', 'history': 'history',
  'agriculture': 'agriculture', 'business': 'business_economics', 'business_economics': 'business_economics', 'general': 'general',
};

final _gradeRe = RegExp(r'^(?:grade|grd|gr|class|g|ክፍሊ)\s*[-_.]?\s*(\d{1,2})(?!\d)', caseSensitive: false);
final _unitRe = RegExp(r'^(?:chapter|chap|ch|unit|u|lesson|topic|ምዕራፍ|ክፍል)\s*[-_.]?\s*(\d{1,3})(?!\d)', caseSensitive: false);
final _leadNumRe = RegExp(r'^(\d{1,3})(?:\s|[-_.)]|$)');

bool _chapterLike(String s) => _unitRe.hasMatch(s) || _leadNumRe.hasMatch(s);

String _clean(String s) => s.replaceAll(RegExp(r'_encrypted$', caseSensitive: false), '').trim();

/// Subject id for a folder name: known aliases first, else a cleaned lowercase id.
String subjectIdFor(String name) {
  final id = name.trim().toLowerCase().replaceAll('&', 'and').replaceAll(RegExp(r'[^\p{L}\p{N}]+', unicode: true), '_').replaceAll(RegExp(r'^_+|_+$'), '');
  return _subjectAliases[id] ?? id;
}

bool isKnownSubject(String name) => _subjectAliases.containsKey(subjectIdFor(name)) || _subjectAliases.containsValue(subjectIdFor(name));

ResPath parseResPath(String path) {
  final parts = [for (final p in path.split(RegExp(r'[\\/]'))) if (_clean(p).isNotEmpty) _clean(p)];
  final folder = parts.join('/');
  var gi = -1, grade = 0;
  for (var i = 0; i < parts.length; i++) {
    final m = _gradeRe.firstMatch(parts[i]);
    if (m != null) {
      gi = i;
      grade = int.parse(m.group(1)!);
    }
  }
  // subject: the last folder with a known subject name, else the folder right after the grade (if not a chapter)
  var si = -1;
  for (var i = parts.length - 1; i >= 0; i--) {
    if (i != gi && isKnownSubject(parts[i])) {
      si = i;
      break;
    }
  }
  if (si < 0 && gi >= 0 && gi + 1 < parts.length && !_chapterLike(parts[gi + 1])) si = gi + 1;
  // chapter: first folder after the subject (or after the grade) that is not the subject itself
  final from = si >= 0 || gi >= 0 ? (si > gi ? si : gi) + 1 : parts.length;
  var chapter = '', unit = '';
  if (from < parts.length) {
    chapter = parts[from];
    final m = _unitRe.firstMatch(chapter) ?? _leadNumRe.firstMatch(chapter);
    if (m != null) unit = '${int.parse(m.group(1)!)}';
  } else {
    // no chapter folder: a "Chapter 3" name anywhere still counts
    for (final p in parts) {
      final m = _unitRe.firstMatch(p);
      if (m != null) {
        chapter = p;
        unit = '${int.parse(m.group(1)!)}';
      }
    }
  }
  return ResPath(
    grade: grade,
    subject: si >= 0 ? subjectIdFor(parts[si]) : '',
    subjectLabel: si >= 0 ? parts[si] : '',
    unit: unit,
    chapter: chapter,
    folder: folder,
  );
}

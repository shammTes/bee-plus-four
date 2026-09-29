// Exam content (content/*.json, schema v1.0) as thin typed views over the unchanged JSON maps.
// Mirrors the web app's data section: isMCQ / isMatch / isScored, optsOf, matchPrompt, isCorrect, answerText.
typedef Json = Map<String, dynamic>;

List<String> strs(Object? v) => v is List ? [for (final x in v) if (x != null) x.toString()] : const [];
String str(Object? v) => v == null ? '' : v.toString();

class MatchList {
  MatchList(this.j);
  final Json j;
  String get id => str(j['id']);
  String get instructions => str(j['instructions']);
  late final Map<String, String> choices = {for (final e in ((j['choices'] as Map?) ?? const {}).entries) e.key.toString(): str(e.value)};
  late final List<Json> prompts = [for (final x in (j['prompts'] as List? ?? const [])) if (x is Map) Json.from(x)];
}

class SimilarQ {
  SimilarQ(this.j);
  final Json j;
  String get stem => str(j['stem']);
  Map<String, String>? get options => j['options'] is Map ? {for (final e in (j['options'] as Map).entries) e.key.toString(): str(e.value)} : null;
  String get answer => str(j['answer']);
  List<String> get steps => strs(j['explanation_steps']);
  String? get image => j['image'] as String?;
  String? get imageAlt => j['image_alt'] as String?;
}

class Question {
  Question(this.j, this.exam);
  final Json j;
  final Exam exam;
  String get id => j['id'] as String;
  int get part => (j['part'] as num?)?.toInt() ?? 1;
  int get number => (j['number'] as num?)?.toInt() ?? 0;
  String get type => str(j['type']);
  Object? get marks => j['marks'];
  String get stem => str(j['stem']);
  String? get stemTex => j['stem_tex'] as String?;
  late final Map<String, String>? options = j['options'] is Map ? {for (final e in (j['options'] as Map).entries) e.key.toString(): str(e.value)} : null;
  String get answer => str(j['answer']);
  List<String> get accepted => strs(j['accepted_answers']);
  late final List<String> steps = strs(j['explanation_steps']);
  late final List<String> tips = strs(j['tips']);
  late final List<SimilarQ> similar = [for (final x in (j['similar_questions'] as List? ?? const [])) if (x is Map) SimilarQ(Json.from(x))];
  late final List<String> topics = strs(j['topics']);
  late final List<String> keywords = strs(j['keywords']);
  Json? get textbookRef => j['textbook_ref'] is Map ? Json.from(j['textbook_ref'] as Map) : null;
  String? get confidence => j['confidence'] as String?;
  String? get reviewFlag => j['review_flag'] as String?;
  String? get image => j['image'] as String?;
  String? get imageAlt => j['image_alt'] as String?;
  String? get matchListId => j['match_list_id'] as String?;
  String? get matchAnswer => j['match_answer'] as String?;
  String? get passageId => j['passage_id'] as String?;
  List<Json> get subparts => [for (final x in (j['subparts'] as List? ?? const [])) if (x is Map) Json.from(x)];
  List<String> get markingPoints => strs(j['marking_points']);

  bool get isMCQ => type == 'mcq' && options != null && options!.length > 1;
  MatchList? get matchList => matchListId == null ? null : exam.matchLists[matchListId];
  bool get isMatch => matchAnswer != null && matchList != null && matchList!.choices.containsKey(matchAnswer);
  bool get isScored => isMCQ || isMatch;
  Map<String, String> get opts => isMCQ ? options! : isMatch ? matchList!.choices : const {};
  String get matchPrompt {
    final ml = matchList;
    if (ml == null) return stem;
    for (final p in ml.prompts) {
      if ((p['number'] as num?)?.toInt() == number) return str(p['text']);
    }
    return stem;
  }

  bool isCorrect(String l) => isMatch ? l == matchAnswer : (accepted.isNotEmpty ? accepted : [answer]).contains(l);
  String get answerText => isMatch ? '$matchAnswer – ${matchList!.choices[matchAnswer]}' : answer;

  /// qLabel: Q12 / II·3
  String get label => (part > 1 ? '${const ['', 'I', 'II', 'III', 'IV'][part.clamp(0, 4)]}·' : 'Q') + number.toString();
}

class Exam {
  Exam(this.j, this.file);
  final Json j; // the "exam" object
  final String file;
  String get id => j['id'] as String;
  String get subject => str(j['subject']);
  String get year => str(j['year']);
  String get type => str(j['type']);
  int? get semester => (j['semester'] as num?)?.toInt();
  String get title => str(j['title']);
  String get school => str(j['school']);
  String? get duration => j['duration'] as String?;
  bool get isMatric => type == 'matriculation';

  /// synthetic exam holding one grade+subject of the Exercise bank (assets/high/exercises)
  bool get isExercise => type == 'exercise';
  String get cat => isExercise ? 'exercise' : (isMatric ? 'matric' : 'model');
  final Map<String, MatchList> matchLists = {};
  final Map<String, Json> passages = {};
  List<Question> questions = [];
  late final List<Question> mcqs = questions.where((q) => q.isMCQ).toList();
  late final List<Question> matches = questions.where((q) => q.isMatch).toList();
  late final List<Question> scored = questions.where((q) => q.isScored).toList();
  List<Question> get timedQs => scored;

  String get short => isExercise ? 'Exercise' : '${isMatric ? 'Matric' : 'Model'}${semester != null ? ' · Sem $semester' : ''}';
  String get name => isExercise ? title : '$subject ${isMatric ? 'Matric' : 'Model'}${semester != null ? ' S$semester' : ''}';
}

/// "2018/2019" -> "2018/19"
String yearShort(String y) {
  final m = RegExp(r'^(\d{4})\s*[/–-]\s*(\d{2,4})$').firstMatch(y.trim());
  return m != null ? '${m[1]}/${m[2]!.substring(m[2]!.length - 2)}' : (y.isEmpty ? '—' : y);
}

int yearKey(String y) => int.tryParse(RegExp(r'^\s*(\d+)').firstMatch(y)?.group(1) ?? '') ?? 0;

String scoredLabel(List<Question> l) {
  final m = l.where((q) => q.isMatch).length, c = l.length - m;
  return m > 0 ? '$c MCQ + $m matching' : '$c MCQs';
}

/// `(1234).toLocaleString('en')`
String thousands(int n) {
  final s = n.abs().toString(), b = StringBuffer(n < 0 ? '-' : '');
  for (var i = 0; i < s.length; i++) {
    if (i > 0 && (s.length - i) % 3 == 0) b.write(',');
    b.write(s[i]);
  }
  return b.toString();
}

// ---- categories (Matriculation | Model)
class Cat {
  const Cat(this.id, this.label, this.long, this.tone, this.icon, this.blurb);
  final String id, label, long, tone, icon, blurb;
}

const kCats = [
  Cat('matric', 'Matriculation', 'Matriculation Exams', 'sage', 'trophy', 'National ESECE papers'),
  Cat('model', 'Model', 'Model Exams', 'peach', 'pen', 'Warsay Yikealo model exams'),
];
Cat catById(String id) => kCats.firstWhere((c) => c.id == id, orElse: () => kCats.first);

// ---- subject look (tone + icon)
const _tones = ['sage', 'peach', 'butter', 'blue', 'lilac', 'rose', 'mint'];
final _looks = <(RegExp, String, String)>[
  (RegExp('chem'), 'lilac', 'flask'),
  (RegExp('bio'), 'sage', 'leaf'),
  (RegExp('agri'), 'butter', 'sprout'),
  (RegExp('geo'), 'blue', 'globe'),
  (RegExp('busi|econ|account'), 'peach', 'chart'),
  (RegExp('engl|lang|tigr|arab'), 'rose', 'book'),
  (RegExp('phys'), 'mint', 'atom'),
  (RegExp('math'), 'blue', 'math'),
  (RegExp('hist'), 'butter', 'landmark'),
  (RegExp('civic|citizen'), 'peach', 'landmark'),
  (RegExp('ict|comput'), 'mint', 'monitor'),
];
final _lookCache = <String, ({String tone, String icon})>{};
({String tone, String icon}) look(String subject) => _lookCache[subject] ??= () {
  final s = subject.toLowerCase();
  for (final (re, t, i) in _looks) {
    if (re.hasMatch(s)) return (tone: t, icon: i);
  }
  var h = 0;
  for (final c in s.codeUnits) {
    h = (h * 31 + c) & 0xFFFFFFFF;
  }
  return (tone: _tones[h % _tones.length], icon: 'book');
}();

int subjOrder(String s) {
  const order = ['english', 'biology', 'chemistry', 'physics', 'mathematics', 'agriculture', 'geography', 'business', 'economics', 'history'];
  final l = s.toLowerCase();
  final i = order.indexWhere((k) => l.contains(k));
  return i < 0 ? 99 : i;
}

String shortTitle(String t) => t.split(RegExp(r'[;(]'))[0].split(RegExp(r',\s'))[0].trim();
String prettyId(String id) {
  final s = id.replaceAll(RegExp(r'[-_]+'), ' ');
  return s.isEmpty ? s : s[0].toUpperCase() + s.substring(1);
}

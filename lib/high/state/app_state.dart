// App state persisted as ONE JSON value under SharedPreferences key 'high:v1'.
import 'dart:async';
import 'dart:convert';
import 'dart:math' as math;

import 'package:flutter/widgets.dart';
import 'package:shared_preferences/shared_preferences.dart';

import '../data/models.dart';
import '../data/repository.dart';
import 'links.dart';
import 'page_gate.dart';
import '../theme/perf.dart';
import '../notes/jr/data/repository.dart' show NotesRepo;

DateTime Function() highNow = DateTime.now;
int nowMs() => highNow().millisecondsSinceEpoch;
const kDay = 86400000;

String dayKey(int t) {
  final d = DateTime.fromMillisecondsSinceEpoch(t);
  return '${d.year}-${d.month.toString().padLeft(2, '0')}-${d.day.toString().padLeft(2, '0')}';
}

DateTime _parseDay(String k, int h, [int m = 0]) {
  final p = k.split('-').map(int.parse).toList();
  return DateTime(p[0], p[1], p[2], h, m);
}

String fmtDur(int s) => s < 60
    ? '${s > 0 ? '<1' : '0'}m'
    : s < 3600
    ? '${(s / 60).round()}m'
    : '${(s / 3600).toStringAsFixed(s < 36000 ? 1 : 0)}h';

String ago(int? t) {
  if (t == null || t == 0) return 'earlier';
  final m = (nowMs() - t) / 6e4;
  if (m < 1) return 'just now';
  if (m < 60) return '${m.round()} min ago';
  if (m < 1440) return '${(m / 60).round()} h ago';
  return (m / 1440).round() == 1 ? 'yesterday' : '${(m / 1440).round()} days ago';
}

int jsRound(num x) => (x + .5).floor();

class Stats {
  Stats({
    required this.answered,
    required this.correct,
    required this.acc,
    required this.newW,
    required this.accW,
    required this.accP,
    required this.nW,
    required this.nP,
    required this.studyAll,
    required this.studyW,
    required this.cur,
    required this.best,
    required this.days,
    required this.fresh,
  });
  final int answered, correct, newW, nW, nP, studyAll, studyW, cur, best;
  final int? acc, accW, accP;
  final List<({String k, int t, String label, int n, bool today})> days;
  final bool fresh;
}

class Progress {
  const Progress(this.done, this.right, this.total, this.pct, this.acc);
  final int done, right, total, pct;
  final int? acc;
}

class HighState extends ChangeNotifier {
  HighState(this.repo, [this._prefs, NotesRepo? notes]) : notesRepo = notes ?? NotesRepo(useIsolate: false);
  final ExamRepo repo;
  final NotesRepo notesRepo;
  SharedPreferences? _prefs;
  static const key = 'high:v1';
  static bool tickStudy = true;

  String? name;
  String? theme;

  /// Flat look (solid soft colours, no blurred shadows): on unless the user picked "Clay" in Settings > Look.
  /// Stored as 'flat' (the old 'lite' switch is not carried over: flat is the new default for everyone).
  bool flat = true;
  String cat = 'matric';
  String lang = 'en';
  Map<String, dynamic> answers = {};
  List<String> bookmarks = [], mistakes = [];
  List<List<dynamic>> ev = [];
  Map<String, dynamic> study = {};
  List<Map<String, dynamic>> recent = [];
  List<Map<String, dynamic>> attempts = [];
  Map<String, dynamic> daily = {};
  Map<String, dynamic> notes = {};

  /// -1 = How to use / Skip chooser, 0+ = step, null = done.
  int? tourStep;
  static const tourActs = ['name', 'grade9', 'subject', 'back', 'back', 'notes', 'exercise', 'matric', 'tutor', 'home', 'settings', 'finish'];
  bool tourWants(String act) => tourStep != null && tourStep! >= 0 && tourStep! < tourActs.length && tourActs[tourStep!] == act;
  bool get tourActive => tourStep != null && tourStep! >= 0;

  void tourAct(String act) {
    if (!tourWants(act)) return;
    final next = tourStep! + 1;
    tourStep = next >= tourActs.length ? null : next;
    changed();
  }

  void startTour() {
    tourStep = 0;
    changed();
  }

  void skipTour() {
    tourStep = null;
    changed();
  }

  void replayTour() {
    tourStep = -1;
    changed();
  }

  void setLang(String code) {
    lang = code == 'ti' ? 'ti' : 'en';
    changed();
  }

  bool teacher = false;
  List<String> basket = [];
  List<Map<String, dynamic>> homework = [];

  void setTeacher(bool v) {
    teacher = v;
    changed();
  }

  void toggleBasket(String id) {
    basket = basket.contains(id) ? (basket.where((x) => x != id).toList()) : [...basket, id];
    changed();
  }

  void clearBasket() {
    basket = [];
    changed();
  }

  void saveHomework(String code, List<String> ids) {
    homework = [{'code': code, 'ids': ids, 't': nowMs()}, ...homework.where((h) => h['code'] != code)].take(12).toList();
    changed();
  }

  Map<String, dynamic> game = {};
  int get xp => (game['xp'] as num?)?.toInt() ?? 0;
  int starsOf(String unitId) => ((game['stars'] as Map?)?[unitId] as num?)?.toInt() ?? 0;
  int get totalStars => ((game['stars'] as Map?)?.values ?? const []).fold(0, (a, b) => a + (b as num).toInt());
  int count(String kind) => ((game['cnt'] as Map?)?[kind] as num?)?.toInt() ?? 0;
  int get level => 1 + (math.sqrt(xp / 25)).floor();

  int award(String key, int pts, {String? unit, int stars = 0, String? kind, int? t}) {
    final done = (game['done'] as Map?)?.cast<String, dynamic>() ?? <String, dynamic>{};
    final st = (game['stars'] as Map?)?.cast<String, dynamic>() ?? <String, dynamic>{};
    var gave = 0;
    if (!done.containsKey(key)) {
      done[key] = 1;
      gave = pts;
      final days = (game['days'] as Map?)?.cast<String, dynamic>() ?? <String, dynamic>{};
      final dk = dayKey(t ?? nowMs());
      days[dk] = ((days[dk] as num?) ?? 0) + pts;
      game['days'] = days;
      game['xp'] = xp + pts;
      if (kind != null) game['cnt'] = {...?(game['cnt'] as Map?)?.cast<String, dynamic>(), kind: count(kind) + 1};
    }
    if (unit != null && stars > starsOf(unit)) st[unit] = stars.clamp(0, 3);
    game['done'] = done;
    game['stars'] = st;
    changed();
    return gave;
  }

  Set<String> get badges {
    final st = streak();
    return {
      if (xp >= 10) 'first',
      if (xp >= 100) 'xp100',
      if (xp >= 500) 'xp500',
      if (xp >= 1500) 'xp1500',
      if (st.best >= 3) 'streak3',
      if (st.best >= 7) 'streak7',
      if (st.best >= 30) 'streak30',
      if (count('label') >= 5) 'labeler',
      if (count('match') >= 5) 'matcher',
      if (count('sim') >= 10) 'explorer',
      if (count('quick') >= 10) 'checker',
      if (totalStars >= 15) 'stars15',
    };
  }

  bool systemDark = false;

  /// more content arrived in the background (an exercise set, unit_questions.json, board codes): rebuild the link index
  /// and the screens that count questions
  void contentChanged() {
    _links = null;
    notifyListeners();
  }

  /// Load the exercise sets the saved profile refers to (answers, mistakes, bookmarks, homework, the teacher's basket,
  /// today's quiz), so stats and lists include them. Started after the first frame; the rest of the bank stays unread
  /// until a subject is opened.
  Future<void> restoreExerciseRefs() async {
    final ids = <String>{
      ...answers.keys,
      ...mistakes,
      ...bookmarks,
      ...basket,
      for (final h in homework) ...[for (final x in (h['ids'] as List? ?? const [])) '$x'],
      for (final d in daily.values)
        if (d is Map) ...[for (final x in (d['ids'] as List? ?? const [])) '$x'],
    }.where((id) => !repo.byId.containsKey(id)).toList();
    if (ids.isEmpty) return;
    final v = repo.exerciseVersion;
    await repo.ensureExercisesForIds(ids);
    if (repo.exerciseVersion != v) contentChanged();
  }

  /// [ids] (a quiz, homework …) may hold exercise questions that are not read in yet: load them, then rebuild
  Future<void> needQuestions(Iterable<String> ids) async {
    final v = repo.exerciseVersion;
    await repo.ensureExercisesForIds(ids);
    if (repo.exerciseVersion != v) contentChanged();
  }

  /// load one grade + subject of the Exercise bank (first open of that subject), then rebuild
  Future<void> needExercises(int grade, String subject) async {
    if (repo.exercisesLoaded(grade, subject)) return;
    await repo.ensureExercises(grade, subject);
    contentChanged();
  }

  UnitLinks? _links;
  UnitLinks get links {
    final l = _links;
    if (l != null && l.size == notesRepo.books.length) return l;
    return _links = UnitLinks(repo, notesRepo);
  }

  int notesPct() {
    final read = (notes['read'] as Map?) ?? const {};
    var n = 0, r = 0;
    for (final b in notesRepo.books) {
      for (final u in b.units) {
        for (final t in u.topics) {
          n += t.cards.length;
          r += (((read[t.id] as num?) ?? 0).toInt()).clamp(0, t.cards.length);
        }
      }
    }
    return n == 0 ? 0 : jsRound(100 * r / n).clamp(0, 100);
  }

  bool get dark => theme == 'dark';

  Future<void> load() async {
    _prefs ??= await SharedPreferences.getInstance();
    // write a pending save as soon as the app is hidden / paused (saves are debounced)
    _life ??= AppLifecycleListener(
      onStateChange: (st) {
        if (st != AppLifecycleState.resumed && _saveT != null) save();
      },
    );
    final raw = _prefs!.getString(key);
    if (raw != null) {
      try {
        fromJson(jsonDecode(raw) as Map<String, dynamic>);
      } catch (_) {
        tourStep = -1;
        theme ??= 'light';
        lang = 'ti';
      }
    } else {
      tourStep = -1;
      theme = 'light';
      lang = 'ti';
    }
  }

  void fromJson(Map<String, dynamic> o) {
    name = o['name'] as String?;
    theme = (o['theme'] as String?) ?? 'light';
    flat = o['flat'] != false;
    Perf.flat = flat;
    lang = (o['lang'] as String?) == 'en' ? 'en' : 'ti';
    cat = (o['cat'] as String?) ?? 'matric';
    answers = Map<String, dynamic>.from(o['answers'] as Map? ?? {});
    bookmarks = strs(o['bookmarks']);
    mistakes = strs(o['mistakes']);
    ev = [for (final e in (o['ev'] as List? ?? const [])) if (e is List) List<dynamic>.from(e)];
    study = Map<String, dynamic>.from(o['study'] as Map? ?? {});
    recent = [for (final r in (o['recent'] as List? ?? const [])) if (r is Map) Map<String, dynamic>.from(r)];
    attempts = [for (final r in (o['attempts'] as List? ?? const [])) if (r is Map) Map<String, dynamic>.from(r)];
    daily = Map<String, dynamic>.from(o['daily'] as Map? ?? {});
    notes = Map<String, dynamic>.from(o['notes'] as Map? ?? {});
    teacher = o['teacher'] == true;
    basket = strs(o['basket']);
    homework = [for (final r in (o['homework'] as List? ?? const [])) if (r is Map) Map<String, dynamic>.from(r)];
    game = Map<String, dynamic>.from(o['game'] as Map? ?? {});
    tourStep = o['tourDone'] == true ? null : ((o['tourStep'] as num?)?.toInt() ?? -1);
    if (!kCats.any((c) => c.id == cat) || (repo.loaded && repo.catExams(cat).isEmpty)) cat = 'matric';
  }

  Map<String, dynamic> toJson() => {
    'v': 2,
    'name': name,
    'theme': theme,
    'flat': flat,
    'lang': lang,
    'cat': cat,
    'answers': answers,
    'bookmarks': bookmarks,
    'mistakes': mistakes,
    'ev': ev,
    'study': study,
    'recent': recent,
    'attempts': attempts,
    'daily': daily,
    'notes': notes,
    'teacher': teacher,
    'basket': basket,
    'homework': homework,
    'game': game,
    'tourDone': tourStep == null,
    'tourStep': tourStep,
  };

  Timer? _saveT;
  void changed() {
    notifyListeners();
    saveLater();
  }

  void saveLater() {
    _saveT?.cancel();
    _saveT = Timer(const Duration(milliseconds: 250), save);
  }

  /// low-priority save (notes reading progress, marked while scrolling): waits until the user pauses, so encoding the
  /// whole record (up to 20k answer events) does not land in the middle of a fling. Flushed when the app is backgrounded.
  void saveIdle() {
    _saveT?.cancel();
    _saveT = Timer(const Duration(milliseconds: 2500), save);
  }

  AppLifecycleListener? _life;

  Future<void> save() async {
    _saveT?.cancel();
    _saveT = null;
    await _prefs?.setString(key, jsonEncode(toJson()));
  }

  void setTheme(String? t) {
    theme = t;
    changed();
  }

  void setFlat(bool v) {
    flat = v;
    Perf.setFlat(v);
    changed();
  }

  void toggleTheme() => setTheme(dark ? 'light' : 'dark');

  void setName(String n) {
    final s = n.trim();
    name = s.isEmpty ? 'Student' : (s.length > 24 ? s.substring(0, 24) : s);
    changed();
  }

  void setCat(String c) {
    cat = c;
    changed();
  }

  void resetProgress() {
    answers = {};
    bookmarks = [];
    mistakes = [];
    ev = [];
    study = {};
    recent = [];
    attempts = [];
    daily = {};
    notes = {};
    changed();
  }

  int lastInteract = 0;
  bool visible = true;
  Timer? _tick;
  void startTicker() {
    if (!tickStudy || _tick != null) return;
    _tick = Timer.periodic(const Duration(seconds: 5), (_) {
      if (visible && nowMs() - lastInteract < 90000 && name != null) {
        final k = dayKey(nowMs());
        final v = ((study[k] as num?) ?? 0).toInt() + 5;
        study[k] = v;
        if ((v ~/ 5) % 6 == 0) save();
      }
    });
  }

  void stopTicker() {
    _tick?.cancel();
    _tick = null;
  }

  void touchRecent(String examId, [int? t]) {
    recent = [
      {'id': examId, 't': t ?? nowMs()},
      ...recent.where((r) => r['id'] != examId),
    ].take(12).toList();
  }

  ({bool ok, int streakUp}) record(Question q, String choice, String mode, [int? t]) {
    t ??= nowMs();
    final ok = q.isCorrect(choice), before = streak(t).cur;
    answers[q.id] = {'c': choice, 'ok': ok, 't': t};
    ev.add([t, q.id, ok ? 1 : 0, mode]);
    if (ev.length > 20000) ev.removeRange(0, ev.length - 20000);
    mistakes = mistakes.where((x) => x != q.id).toList();
    if (!ok) mistakes.add(q.id);
    if (!q.exam.isExercise) touchRecent(q.exam.id, t);
    changed();
    final after = streak(t).cur;
    if (ok) award('q:${q.id}', 2, t: t);
    return (ok: ok, streakUp: after > before && after >= 2 ? after : 0);
  }

  Map<String, dynamic>? ans(String id) => answers[id] as Map<String, dynamic>?;
  bool answered(String id) => answers.containsKey(id);
  bool ansOk(String id) => (answers[id] as Map?)?['ok'] == true;

  void toggleBookmark(String id) {
    bookmarks.contains(id) ? bookmarks.remove(id) : bookmarks.add(id);
    changed();
  }

  ({int cur, int best}) streak([int? now]) {
    now ??= nowMs();
    final days = {for (final e in ev) dayKey((e[0] as num).toInt()), ...?(game['days'] as Map?)?.keys.cast<String>()};
    var cur = 0, d = now;
    if (!days.contains(dayKey(d))) d -= kDay;
    while (days.contains(dayKey(d))) {
      cur++;
      d -= kDay;
    }
    var best = 0, run = 0;
    int? prev;
    for (final k in days.toList()..sort()) {
      final t = _parseDay(k, 12).millisecondsSinceEpoch;
      run = prev != null && jsRound((t - prev) / kDay) == 1 ? run + 1 : 1;
      best = math.max(best, run);
      prev = t;
    }
    return (cur: cur, best: math.max(best, cur));
  }

  Stats stats() {
    final now = nowMs(), w0 = now - 7 * kDay, p0 = now - 14 * kDay;
    final ans = answers.values.cast<Map>();
    final answered = ans.length, correct = ans.where((a) => a['ok'] == true).length;
    final evW = ev.where((e) => (e[0] as num) >= w0).toList(), evP = ev.where((e) => (e[0] as num) >= p0 && (e[0] as num) < w0).toList();
    int? accOf(List<List<dynamic>> l) => l.isEmpty ? null : jsRound(100 * l.where((e) => e[2] == 1 || e[2] == true).length / l.length);
    final newW = {for (final e in evW) e[1]}.length;
    var studyAll = 0, studyW = 0;
    study.forEach((k, v) {
      final s = (v as num).toInt();
      studyAll += s;
      if (_parseDay(k, 23, 59).millisecondsSinceEpoch >= w0) studyW += s;
    });
    const wd = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
    final days = <({String k, int t, String label, int n, bool today})>[];
    for (var i = 6; i >= 0; i--) {
      final t = now - i * kDay, k = dayKey(t);
      days.add((k: k, t: t, label: wd[DateTime.fromMillisecondsSinceEpoch(t).weekday - 1], n: ev.where((e) => dayKey((e[0] as num).toInt()) == k).length, today: i == 0));
    }
    final st = streak(now);
    return Stats(
      answered: answered,
      correct: correct,
      acc: answered > 0 ? jsRound(100 * correct / answered) : null,
      newW: newW,
      accW: accOf(evW),
      accP: accOf(evP),
      nW: evW.length,
      nP: evP.length,
      studyAll: studyAll,
      studyW: studyW,
      cur: st.cur,
      best: st.best,
      days: days,
      fresh: answered == 0 && ev.isEmpty,
    );
  }

  Progress _prog(Iterable<Question> qs) {
    final l = qs.toList();
    final done = l.where((q) => answered(q.id)).toList(), right = done.where((q) => ansOk(q.id)).length;
    return Progress(done.length, right, l.length, l.isEmpty ? 0 : jsRound(100 * done.length / l.length), done.isEmpty ? null : jsRound(100 * right / done.length));
  }

  Progress examProgress(Exam e) => _prog(e.scored);
  Progress subjectProgress(String subj, String? year, String cat) =>
      _prog(repo.exams.where((e) => e.subject == subj && (year == null || e.year == year) && (cat == 'all' || e.cat == cat)).expand((e) => e.scored));

  ({int questions, int exams, int subjects, String years, Progress p}) catProgress(String c) {
    final l = repo.catExams(c);
    return (questions: l.fold(0, (a, e) => a + e.questions.length), exams: l.length, subjects: {for (final e in l) e.subject}.length, years: repo.catYears(l), p: _prog(l.expand((e) => e.scored)));
  }

  static int hashStr(String s) {
    var h = 2166136261;
    for (final c in s.runes) {
      h = _imul(h ^ c, 16777619);
    }
    return h & 0xFFFFFFFF;
  }

  static int _imul(int a, int b) {
    a &= 0xFFFFFFFF;
    b &= 0xFFFFFFFF;
    final ah = (a >> 16) & 0xFFFF, al = a & 0xFFFF;
    return ((al * b) + (((ah * b) & 0xFFFF) << 16)) & 0xFFFFFFFF;
  }

  static int _i32(int x) => (x & 0xFFFFFFFF) >= 0x80000000 ? (x & 0xFFFFFFFF) - 0x100000000 : x & 0xFFFFFFFF;

  static double Function() rng(int seed) {
    var s = _i32(seed);
    return () {
      s = _i32(s + 0x6D2B79F5);
      var t = _imul(s ^ ((s & 0xFFFFFFFF) >> 15), 1 | s);
      t = _i32(_i32(t + _imul(t ^ ((t & 0xFFFFFFFF) >> 7), 61 | t)) ^ t);
      return ((t ^ ((t & 0xFFFFFFFF) >> 14)) & 0xFFFFFFFF) / 4294967296;
    };
  }

  Map<String, dynamic> dailyQuiz() {
    final k = dayKey(nowMs());
    final cur = daily[k] as Map?;
    // ids of exercise sets that are not read in yet still count (they load when the quiz opens)
    if (cur != null && (cur['ids'] as List).isNotEmpty && (cur['ids'] as List).every((id) => repo.byId.containsKey(id) || repo.mayBePendingExercise('$id'))) {
      if (cur is! Map<String, dynamic> || cur['res'] is! Map<String, dynamic>) {
        daily[k] = {'ids': List<String>.from(cur['ids'] as List), 'res': Map<String, dynamic>.from((cur['res'] as Map?) ?? {})};
      }
      return daily[k] as Map<String, dynamic>;
    }
    final r = rng(hashStr(k));
    List<T> shuf<T>(List<T> a) {
      final z = [for (final x in a) (r(), x)];
      z.sort((p, q) => p.$1.compareTo(q.$1));
      return [for (final x in z) x.$2];
    }

    final mis = shuf(mistakes.where((id) => repo.byId[id]?.isMCQ ?? false).toList()).take(3).toList();
    final all = repo.allMcq;
    final groups = <String, List<String>>{};
    for (final q in shuf(all.where((q) => !answered(q.id)).toList())) {
      (groups[q.exam.subject] ??= []).add(q.id);
    }
    final inter = <String>[];
    final g = groups.values.toList();
    for (var i = 0; g.any((x) => x.length > i); i++) {
      for (final x in g) {
        if (i < x.length) inter.add(x[i]);
      }
    }
    final ids = <String>{...mis, ...inter, ...shuf([for (final q in all) q.id])}.take(10).toList();
    daily = {k: {'ids': ids, 'res': <String, dynamic>{}}};
    saveLater();
    return daily[k] as Map<String, dynamic>;
  }

  List<({String subject, String id, int n, int right, int acc})> weakTopics() {
    final m = <String, ({String subject, String id, int n, int right})>{};
    answers.forEach((id, a) {
      final q = repo.byId[id];
      if (q == null || !q.isScored) return;
      final s = q.exam.subject;
      for (final t in q.topics) {
        final k = '$s|$t', o = m[k] ?? (subject: s, id: t, n: 0, right: 0);
        m[k] = (subject: s, id: t, n: o.n + 1, right: o.right + ((a as Map)['ok'] == true ? 1 : 0));
      }
    });
    final l = [for (final o in m.values) (subject: o.subject, id: o.id, n: o.n, right: o.right, acc: jsRound(100 * o.right / o.n))];
    l.sort((a, b) => a.acc != b.acc ? a.acc - b.acc : b.n - a.n);
    return l;
  }
}

class HighScope extends InheritedNotifier<HighState> {
  const HighScope({super.key, required HighState state, required super.child}) : super(notifier: state);
  /// the state, rebuilding [c] when it changes. Inside a page ([PageGate]) only while that page is on screen.
  static HighState of(BuildContext c) => PageGateScope.depend(c) ? read(c) : c.dependOnInheritedWidgetOfExactType<HighScope>()!.notifier!;
  static HighState read(BuildContext c) => c.getInheritedWidgetOfExactType<HighScope>()!.notifier!;
}

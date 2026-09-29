// Loads the exam packs (assets/high/exams, copied unchanged from the web app) and builds the same indexes as the web:
// EXAMS (web order), EXAM, byId, SUBJECTS, YEARS, TOPIC_TITLE / TOPIC_PARENT / TOPIC_QS, CONCEPTS.
import 'dart:convert';
import 'dart:isolate';

import 'package:flutter/services.dart';

import 'models.dart';
import '../teacher/codes.dart';

String exerciseSubjectLabel(String key) => const {
  'mathematics': 'Mathematics', 'business_economics': 'Business & Economics', 'biology': 'Biology', 'chemistry': 'Chemistry',
  'physics': 'Physics', 'geography': 'Geography', 'history': 'History', 'agriculture': 'Agriculture', 'english': 'English',
}[key] ?? key;

class Concept {
  Concept(this.subject, this.topic, this.sub);
  final String subject;
  final Json topic, sub;
}

class ExamRepo {
  ExamRepo({this.useIsolate = false, AssetBundle? bundle}) : _bundle = bundle ?? rootBundle;
  final bool useIsolate;
  final AssetBundle _bundle;
  static const root = 'assets/high/exams';

  final List<Exam> exams = [];
  final Map<String, Exam> exam = {};
  final Map<String, Question> byId = {};
  final List<String> subjects = [];
  final Map<String, String> topicTitleMap = {}, topicParent = {};
  final Map<String, List<String>> topicQs = {};
  final List<Concept> concepts = [];

  /// board codes (assets/high/codes.json); null if not bundled
  QCodes? codes;
  List<String> media = [];
  bool loaded = false;

  Future<void>? _init;
  Future<void> init() => _init ??= _load();

  Future<void> _load() async {
    final idx = jsonDecode(await _bundle.loadString('$root/index.json')) as Map<String, dynamic>;
    media = strs(idx['media']);
    final files = [...strs(idx['exams']), ...strs(idx['topics'])];
    final raws = await Future.wait(files.map((f) => _bundle.loadString('$root/$f', cache: false)));
    List<Object?> parse(List<String> l) => [for (final s in l) jsonDecode(s)];
    final parsed = useIsolate ? await Isolate.run(() => parse(raws)) : parse(raws);
    final nEx = strs(idx['exams']).length;
    for (var i = 0; i < nEx; i++) {
      final d = parsed[i] as Map<String, dynamic>;
      final e = Exam(Map<String, dynamic>.from(d['exam'] as Map), files[i]);
      if (exam.containsKey(e.id)) continue;
      for (final ml in (d['match_lists'] as List? ?? const [])) {
        if (ml is Map && ml['id'] != null && ml['choices'] != null) e.matchLists[ml['id'] as String] = MatchList(Map<String, dynamic>.from(ml));
      }
      for (final ps in (d['passages'] as List? ?? const [])) {
        if (ps is Map && ps['id'] != null) e.passages[ps['id'] as String] = Map<String, dynamic>.from(ps);
      }
      e.questions = [
        for (final q in (d['questions'] as List? ?? const []))
          if (q is Map && q['id'] != null) Question(Map<String, dynamic>.from(q), e),
      ];
      for (final q in e.questions) {
        byId[q.id] = q;
      }
      exams.add(e);
      exam[e.id] = e;
    }
    final subs = {for (final e in exams) e.subject}.toList()..sort((a, b) => subjOrder(a) != subjOrder(b) ? subjOrder(a) - subjOrder(b) : a.compareTo(b));
    subjects.addAll(subs);
    // topics: attach each index file to a subject (exam_ids -> subject, explicit "subject", or the filename prefix)
    for (var i = nEx; i < files.length; i++) {
      final ix = parsed[i] as Map<String, dynamic>;
      String? subj;
      for (final id in strs(ix['exam_ids'])) {
        if (exam[id] != null) {
          subj = exam[id]!.subject;
          break;
        }
      }
      subj ??= ix['subject'] as String?;
      if (subj == null) {
        final pre = files[i].split(RegExp(r'[_.]'))[0].toLowerCase();
        final pp = pre.replaceAll(RegExp('[^a-z]'), '');
        for (final s in subjects) {
          final sl = s.toLowerCase();
          if (sl.replaceAll(RegExp('[^a-z]'), '').startsWith(pp) || pre.startsWith(sl.substring(0, sl.length < 4 ? sl.length : 4))) {
            subj = s;
            break;
          }
        }
      }
      subj ??= 'General';
      final seen = {for (final c in concepts) if (c.subject == subj) c.sub['id']};
      for (final t in (ix['topics'] as List? ?? const [])) {
        if (t is! Map) continue;
        final tt = Map<String, dynamic>.from(t);
        if (tt['id'] != null) topicParent.putIfAbsent('$subj|${tt['id']}', () => shortTitle(str(tt['title'])));
        for (final s in (tt['subtopics'] as List? ?? const [])) {
          if (s is! Map || s['id'] == null) continue;
          final ss = Map<String, dynamic>.from(s);
          topicParent.putIfAbsent('$subj|${ss['id']}', () => shortTitle(str(tt['title'])));
          topicTitleMap.putIfAbsent('$subj|${ss['id']}', () => shortTitle(str(ss['title'])));
          if (seen.add(ss['id'])) concepts.add(Concept(subj, tt, ss));
        }
      }
    }
    for (final e in exams) {
      for (final q in e.questions) {
        for (final t in q.topics) {
          (topicQs['${e.subject}|$t'] ??= []).add(q.id);
        }
      }
    }
    await _loadExercises();
    codes = await QCodes.load(_bundle);
    loaded = true;
  }

  // ---------------------------------------------------------------- Exercise bank (tools/clean_exercises.py)
  static const exRoot = 'assets/high/exercises';

  /// "grade|subject" -> exercise exam; unit id (or "general|grade|subject") -> question ids
  final Map<String, Exam> exerciseExams = {};
  final Map<String, List<String>> exerciseUnits = {};
  List<String> exerciseIds({required int grade, required String subject, String? unitId}) =>
      exerciseUnits[unitId ?? 'general|$grade|$subject'] ?? const [];

  Future<void> _loadExercises() async {
    final String idxRaw;
    try {
      idxRaw = await _bundle.loadString('$exRoot/index.json');
    } catch (_) {
      return; // bank not bundled
    }
    final idx = jsonDecode(idxRaw) as Map<String, dynamic>;
    final files = [
      for (final g in (idx['grades'] as Map).values)
        for (final e in (g as Map).values) (e as Map)['file'] as String,
    ];
    final raws = await Future.wait(files.map((f) => _bundle.loadString('$exRoot/$f', cache: false)));
    List<Object?> parse(List<String> l) => [for (final s in l) jsonDecode(s)];
    final parsed = useIsolate ? await Isolate.run(() => parse(raws)) : parse(raws);
    for (final d in parsed.cast<Map<String, dynamic>>()) {
      final subj = d['subject'] as String, g = (d['grade'] as num).toInt();
      final label = exerciseSubjectLabel(subj);
      final e = Exam({'id': 'exercise_${subj}_$g', 'subject': label, 'year': 'Grade $g', 'type': 'exercise', 'title': '$label exercises', 'school': 'Exercise bank'}, '$exRoot/${subj}_$g.json');
      var n = 0;
      e.questions = [
        for (final q in (d['questions'] as List).cast<Map<String, dynamic>>())
          Question({
            'id': q['id'],
            'type': 'mcq',
            'number': ++n,
            'stem': q['prompt'],
            'options': {for (final (i, o) in (q['options'] as List).indexed) 'ABCDE'[i]: o},
            'answer': 'ABCDE'[(q['answer'] as num).toInt()],
            'explanation_steps': [if ((q['explanation'] as String? ?? '').isNotEmpty) q['explanation']],
            'unit': q['unit'],
          }, e),
      ];
      for (final q in e.questions) {
        byId[q.id] = q;
        (exerciseUnits[(q.j['unit'] as String?) ?? 'general|$g|$subj'] ??= []).add(q.id);
      }
      exam[e.id] = e;
      exerciseExams['$g|$subj'] = e;
    }
  }

  String topicTitle(String subject, String id) => topicTitleMap['$subject|$id'] ?? prettyId(id);

  String? primaryTopic(Question q) {
    if (q.topics.isEmpty) return null;
    final s = q.exam.subject;
    final l = [...q.topics]..sort((a, b) => (topicQs['$s|$a']?.length ?? 0) - (topicQs['$s|$b']?.length ?? 0));
    return l.first;
  }

  List<Exam> catExams(String c) => exams.where((e) => c == 'all' || e.cat == c).toList();
  List<Question> get allMcq => [for (final e in exams) ...e.mcqs];

  String catYears(List<Exam> l) {
    final ys = {for (final e in l) e.year}.toList()..sort((a, b) => yearKey(a) - yearKey(b));
    if (ys.isEmpty) return '';
    if (ys.length == 1) return yearShort(ys.first);
    return '${ys.first.substring(0, 4)}–${ys.last.substring(0, 4)}';
  }

  /// asset path of a content media file ("media/x.png")
  String mediaAsset(String path) => '$root/${path.replaceFirst(RegExp(r'^\.?/'), '')}';
  bool hasMedia(String path) => media.contains(path.replaceFirst(RegExp(r'^\.?/'), '').replaceFirst('media/', ''));
}

/// byYear sort used in lists
int byYear(Exam a, Exam b) {
  final k = yearKey(b.year) - yearKey(a.year);
  if (k != 0) return k;
  final s = b.year.compareTo(a.year);
  if (s != 0) return s;
  final m = (a.semester ?? 0) - (b.semester ?? 0);
  if (m != 0) return m;
  return a.id.compareTo(b.id);
}

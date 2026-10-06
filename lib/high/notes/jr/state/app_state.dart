// High: the Junior notes renderer's AppState, backed by HighState. Notes progress lives in HighState.notes
// ({read, games, ex, last, mist}) and is saved with the rest of High's record (prefs key 'high:v1').
import 'package:flutter/widgets.dart';

import '../../../state/app_state.dart' show HighState, nowMs;
import '../../../state/page_gate.dart' show PageGateScope;
import '../data/notes_models.dart';
import '../data/repository.dart';
import '../l10n/labels.dart';

class AppState extends ChangeNotifier {
  AppState(this.high, this.repo) {
    high.addListener(notifyListeners);
    for (final k in ['read', 'games', 'ex', 'mist']) {
      high.notes[k] = Map<String, dynamic>.from((high.notes[k] as Map?) ?? {});
    }
  }
  final HighState high;
  final NotesRepo repo;
  String lang = 'en';
  bool get dark => high.dark;
  Map<String, dynamic> get notes => high.notes;

  void _changed() => high.changed();
  void _quiet() => high.saveIdle(); // reading progress: saved when the user pauses, not mid-scroll

  // ---- labels (English; missing keys show the key itself, used for subject names)
  String t(String k, [Map<String, Object>? vars]) {
    var s = kLabels['en']![k] ?? k;
    if (vars != null) s = s.replaceAllMapped(RegExp(r'\{(\w+)\}'), (m) => vars[m[1]]?.toString() ?? m[0]!);
    return s;
  }

  String en(String k) => kLabels['en']![k] ?? k;
  String nQ(int n) => n == 1 ? t('oneQuestion') : t('nQuestions', {'n': n});
  void setLang(String l) {}

  Map<String, dynamic> get _read => notes['read'] as Map<String, dynamic>;
  Map<String, dynamic> get _games => notes['games'] as Map<String, dynamic>;
  Map<String, dynamic> get _ex => notes['ex'] as Map<String, dynamic>;
  Map<String, dynamic> get notesMist => notes['mist'] as Map<String, dynamic>;

  double lessonPct(Lesson l) => l.cards.isEmpty ? 1 : (((_read[l.id] as num?) ?? 0) / l.cards.length).clamp(0, 1).toDouble();

  /// lessons 60 %, games 20 %, exercise 20 %
  int unitPct(Unit u) {
    final L = u.lessons.isEmpty ? 0.0 : u.lessons.fold<double>(0, (a, l) => a + lessonPct(l)) / u.lessons.length;
    final G = u.games.isEmpty ? 1.0 : u.games.where((g) => _games[g.id] != null).length / u.games.length;
    return (100 * (0.6 * L + 0.2 * G + 0.2 * (_ex[u.id] != null ? 1 : 0))).round();
  }

  /// unit progress from the index only (no book parse): cards read of the unit's topics
  int unitPctIdx(IndexUnit u) {
    var n = 0, r = 0;
    for (final t in u.topics) {
      n += t.cards.length;
      r += (((_read[t.id] as num?) ?? 0).toInt()).clamp(0, t.cards.length);
    }
    final L = n == 0 ? 0.0 : r / n;
    final gs = _games.keys.where((g) => g.startsWith('${u.id}-')).length;
    return (100 * (0.6 * L + 0.2 * (gs > 0 ? 1 : 0) + 0.2 * (_ex[u.id] != null ? 1 : 0))).round().clamp(0, 100);
  }

  ({String book, String unit})? get lastUnit {
    final l = notes['last'];
    if (l is Map && l['book'] is String && l['unit'] is String) return (book: l['book'] as String, unit: l['unit'] as String);
    return null;
  }

  void setLast(String book, String unit) {
    final l = notes['last'];
    final keep = l is Map && l['unit'] == unit ? Map<String, dynamic>.from(l) : <String, dynamic>{};
    keep
      ..['book'] = book
      ..['unit'] = unit
      ..['t'] = nowMs()
      ..remove('lesson');
    notes['last'] = keep;
    _quiet();
  }

  String? get lastCard {
    final l = notes['last'];
    return l is Map && l['card'] is String ? l['card'] as String : null;
  }

  bool markRead(String unitId, String lessonId, int i) {
    var dirty = false;
    if (((_read[lessonId] as num?) ?? 0) < i + 1) {
      _read[lessonId] = i + 1;
      dirty = true;
    }
    final l = notes['last'];
    if (l is Map && l['unit'] == unitId && l['card'] != '$lessonId~$i') {
      l['card'] = '$lessonId~$i';
      dirty = true;
    }
    if (dirty) _quiet();
    return dirty;
  }

  int? gameBest(String gid) => (_games[gid] as num?)?.toInt();
  void gameDone(String gid, int stars) {
    _games[gid] = stars > (gameBest(gid) ?? 0) ? stars : (gameBest(gid) ?? stars);
    _changed();
  }

  Map<String, dynamic>? exResult(String uid) => _ex[uid] as Map<String, dynamic>?;
  void exDone(String uid, int stars, int right, int of) {
    final b = (_ex[uid] as Map?)?['stars'] as num? ?? 0;
    _ex[uid] = {'stars': stars > b ? stars : b.toInt(), 'right': right, 'of': of};
    _changed();
  }

  void nmMark(String bid, String uid, String qid, bool ok) {
    final k = '$bid|$qid';
    if (ok) {
      notesMist.remove(k);
    } else {
      notesMist[k] = {'b': bid, 'u': uid, 'q': qid, 't': nowMs()};
    }
    _changed();
  }

  @override
  void dispose() {
    high.removeListener(notifyListeners);
    super.dispose();
  }
}

class AppScope extends InheritedNotifier<AppState> {
  const AppScope({super.key, required AppState state, required super.child}) : super(notifier: state);
  /// inside a page ([PageGate]) this rebuilds [c] only while the page is on screen
  static AppState of(BuildContext c) => PageGateScope.depend(c) ? read(c) : c.dependOnInheritedWidgetOfExactType<AppScope>()!.notifier!;
  static AppState read(BuildContext c) => c.getInheritedWidgetOfExactType<AppScope>()!.notifier!;
}

// One cross-link index (built once, lazily, from the loaded content): notes unit <-> exercise set <-> matric questions.
// Everything that shows "Exercises (N)" / "Matric questions (N)" / "Study this unit" reads counts from here.
import '../data/repository.dart';
import '../notes/jr/data/repository.dart';

class UnitLinks {
  UnitLinks(ExamRepo r, NotesRepo n) : _r = r {
    for (final e in n.unitQuestions.entries) {
      final seen = <String>{};
      final l = [
        for (final m in e.value)
          if (r.byId.containsKey(m['id']) && seen.add(m['id'] as String)) m['id'] as String,
      ];
      int rank(String id) => r.byId[id]!.isScored ? 0 : 1;
      final sorted = [for (final id in l) if (rank(id) == 0) id, for (final id in l) if (rank(id) == 1) id];
      if (sorted.isNotEmpty) matric[e.key] = sorted;
      for (final m in e.value) {
        final id = m['id'] as String?;
        if (id == null || !r.byId.containsKey(id)) continue;
        final c = _conf(m['confidence']);
        if (c > (_best[id] ?? -1)) {
          _best[id] = c;
          unitOf[id] = e.key;
        }
      }
    }
    for (final e in r.exerciseUnits.entries) {
      if (e.key.startsWith('general|')) continue;
      exercises[e.key] = e.value;
      for (final id in e.value) {
        unitOf[id] = e.key;
      }
    }
    for (final b in n.books) {
      final m = <String>{};
      var ex = 0;
      for (final u in b.units) {
        m.addAll(matric[u.id] ?? const []);
      }
      ex = r.exerciseCount(b.grade, b.subject);
      bookMatric[b.id] = m.toList();
      bookExercises[b.id] = ex;
    }
    size = n.books.length;
  }

  static double _conf(Object? c) => c is num ? c.toDouble() : const {'high': 3.0, 'medium': 2.0, 'low': 1.0}[c] ?? 0.5;

  /// unit id -> matric/model question ids (auto-marked first)
  final Map<String, List<String>> matric = {};

  /// unit id -> bundled exercise question ids
  final Map<String, List<String>> exercises = {};

  /// question id (matric or exercise) -> its notes unit
  final Map<String, String> unitOf = {};
  final Map<String, double> _best = {};

  /// book id -> matric ids over all its units / number of bundled exercises for the book's grade+subject
  final Map<String, List<String>> bookMatric = {};
  final Map<String, int> bookExercises = {};
  int size = 0;

  List<String> matricFor(String unitId) => matric[unitId] ?? const [];
  List<String> exercisesFor(String unitId) => exercises[unitId] ?? const [];

  final ExamRepo _r;

  /// bundled exercises of a unit: exact once its set is read in, the bank index's count before (sets load lazily)
  int exerciseCountFor(String unitId) => _r.exerciseUnitCount(unitId);
}

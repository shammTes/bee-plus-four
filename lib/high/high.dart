// Public API of the High module. Import this file from a host app:
//   import 'package:<your_app>/high/high.dart';
//   await High.init();            // optional pre-warm (content + saved progress)
//   Navigator.push(context, PageRouteBuilder(pageBuilder: (_, _, _) => const HighScreen()));
import 'data/repository.dart';
import 'notes/jr/data/repository.dart';
import 'notes/jr/notes/svg_prep.dart' show SvgStore;
export 'exercise/source.dart';
import 'state/app_state.dart';

export 'app.dart' show HighApp, HighScreen;
export 'state/app_state.dart' show HighState;
export 'widgets/page.dart' show HighTab;

abstract final class High {
  static Future<HighState>? _f;

  /// Loads all exam packs (assets/high/exams) and the saved state (SharedPreferences key 'high:v1').
  /// Safe to call many times; the same state is shared by every HighScreen.
  static Future<HighState> init({bool useIsolate = true}) => _f ??= () async {
    // Exercise bank, board codes, unit_questions.json and media placements are not read before the first screen:
    // exercise sets load per grade + subject when needed, the rest right after start in the background.
    final repo = ExamRepo(useIsolate: useIsolate, lazyExercises: true, deferCodes: true);
    final notes = NotesRepo(useIsolate: useIsolate, deferExtras: true);
    SvgStore.useIsolate = useIsolate;
    await Future.wait([repo.init(), notes.init()]);
    final s = HighState(repo, null, notes);
    await s.load();
    repo.codesReady.then((_) => s.contentChanged(), onError: (Object _) {});
    notes.extrasReady.then((_) => s.contentChanged(), onError: (Object _) {});
    if (HighState.tickStudy) s.startTicker();
    return s;
  }();

  /// test hook: forget the shared instance
  static void reset() => _f = null;
}

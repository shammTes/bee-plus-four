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
    final repo = ExamRepo(useIsolate: useIsolate);
    await repo.init();
    final notes = NotesRepo(useIsolate: useIsolate);
    SvgStore.useIsolate = useIsolate;
    await notes.init();
    final s = HighState(repo, null, notes);
    await s.load();
    if (HighState.tickStudy) s.startTicker();
    return s;
  }();

  /// test hook: forget the shared instance
  static void reset() => _f = null;
}

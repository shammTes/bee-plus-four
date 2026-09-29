// Entry widgets: HighApp (standalone app) and HighScreen (embeddable in any host app).
import 'package:flutter/widgets.dart';

import 'screens/exams.dart';
import 'screens/home.dart';
import 'screens/exercise.dart';
import 'screens/tutor.dart';
import 'notes/jr/state/app_state.dart' as jr;
import 'screens/notes_home.dart';
import 'screens/tour.dart';
import 'state/app_state.dart';
import 'theme/tokens.dart';
import 'widgets/art.dart';
import 'widgets/kit.dart';
import 'widgets/page.dart';
import 'high.dart';

/// Standalone app (use in main.dart). Loads content + state, then shows [HighScreen].
class HighApp extends StatelessWidget {
  const HighApp({super.key, this.state, this.initialTab = HighTab.home});
  final HighState? state;
  final HighTab initialTab;
  @override
  Widget build(BuildContext context) => WidgetsApp(
    title: '4',
    color: const Color(0xFFE88A6E),
    debugShowCheckedModeBanner: false,
    pageRouteBuilder: <T>(RouteSettings s, WidgetBuilder b) => PageRouteBuilder<T>(settings: s, pageBuilder: (c, _, _) => b(c)),
    home: HighScreen(state: state, initialTab: initialTab),
  );
}

/// Embeddable High UI. Works inside a MaterialApp/CupertinoApp/WidgetsApp route; creates its own state
/// via [High.init] unless one is passed in.
class HighScreen extends StatefulWidget {
  const HighScreen({super.key, this.state, this.initialTab = HighTab.home});
  final HighState? state;
  final HighTab initialTab;
  @override
  State<HighScreen> createState() => _HighScreenState();
}

class _HighScreenState extends State<HighScreen> {
  HighState? _s;
  jr.AppState? _notes;
  Object? _err;
  @override
  void initState() {
    super.initState();
    if (widget.state != null) {
      _s = widget.state;
    } else {
      High.init().then((s) => mounted ? setState(() => _s = s) : null, onError: (Object e) => mounted ? setState(() => _err = e) : null);
    }
  }

  @override
  Widget build(BuildContext context) {
    final s = _s;
    if (s == null) {
      return ColoredBox(
        color: Palette.light.bg,
        child: Center(child: _err != null ? Text('Could not open 4\n$_err', textDirection: TextDirection.ltr) : const Text('Opening 4…', textDirection: TextDirection.ltr)),
      );
    }
    final dark = MediaQuery.maybePlatformBrightnessOf(context) == Brightness.dark;
    if (s.systemDark != dark) s.systemDark = dark;
    return HighScope(
      state: s,
      child: jr.AppScope(
        state: _notes ??= jr.AppState(s, s.notesRepo),
        child: Builder(
        builder: (context) {
          final p = Kit.of(context).p;
          return Directionality(
            textDirection: TextDirection.ltr,
            child: DefaultTextStyle(
              style: ts(15, w600, p.ink),
              child: ColoredBox(color: p.bg, child: SafeArea(top: true, bottom: false, child: BigScreen(child: HighShell(initialTab: widget.initialTab)))),
            ),
          );
        },
      ),
      ),
    );
  }
}

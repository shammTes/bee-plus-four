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
import '../licensing/screenshot.dart';

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
  void dispose() {
    _s?.stopTicker();
    _notes?.dispose();
    super.dispose();
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

/// the phone: page stack per tab + floating nav bar + sheet layer
class HighShell extends StatefulWidget {
  const HighShell({super.key, this.initialTab = HighTab.home});
  final HighTab initialTab;
  @override
  State<HighShell> createState() => HighShellState();
}

class HighShellState extends State<HighShell> implements HighNav {
  late HighTab _tab = widget.initialTab;
  final List<Widget> _stack = [];
  final List<({Key key, Widget child, bool lock, bool bare})> _sheets = [];
  int _gen = 0;

  @override
  HighTab get current => _tab;

  /// tabs visited so far: their pages stay mounted (offstage) so scroll / filters survive tab switches
  final Set<HighTab> _visited = {};

  @override
  void tab(HighTab t) {
    final s = HighScope.read(context);
    if (s.tourStep != null && !s.tourWants(t.name)) return;
    setState(() {
      if (t == _tab && _stack.isEmpty) _tabGen[t] = (_tabGen[t] ?? 0) + 1;
      _stack.clear();
      _tab = t;
    });
    s.tourAct(t.name);
  }
  final Map<HighTab, int> _tabGen = {};

  @override
  void push(Widget page) => setState(() {
    _stack.add(KeyedSubtree(key: ValueKey(++_gen), child: page));
  });

  @override
  void open(String key, Widget Function() build) => setState(() {
    final k = ValueKey('r:$key'), i = _stack.indexWhere((w) => w.key == k);
    if (i >= 0) {
      _stack.removeRange(i + 1, _stack.length); // already open below: go back to it instead of stacking a copy
    } else {
      _stack.add(KeyedSubtree(key: k, child: build()));
    }
  });

  @override
  void back() {
    final s = HighScope.read(context);
    if (s.tourStep != null && !s.tourWants('back')) return;
    setState(() {
      if (_sheets.isNotEmpty) {
        _sheets.removeLast();
      } else if (_stack.isNotEmpty) {
        _stack.removeLast();
      } else if (_tab != HighTab.home) {
        _tab = HighTab.home;
      }
    });
    s.tourAct('back');
  }

  /// shows a bottom sheet (web `sheet()`); returns a close function
  VoidCallback sheet(Widget child, {bool lock = false, bool bare = false}) {
    final k = UniqueKey();
    setState(() => _sheets.add((key: k, child: child, lock: lock, bare: bare)));
    return () => mounted ? setState(() => _sheets.removeWhere((e) => e.key == k)) : null;
  }

  bool get canPop => _sheets.isEmpty && _stack.isEmpty && _tab == HighTab.home;

  static const _protected = {
    'NotesHomePage',
    'NotesSubjectPage',
    'GradePage',
    'UnitPage',
    'ExercisePage',
    'ExerciseSubjectPage',
    'ExerciseUnitPage',
    'ExamsPage',
    'ExamSubjectPage',
    'PracticePage',
  };
  bool _secureOn = false;

  bool _isProtected(Widget w) {
    if (w is KeyedSubtree) return _isProtected(w.child);
    final name = w.runtimeType.toString();
    if (name == 'QuizPage') {
      final kind = (w as dynamic).kind;
      return kind == 'exercise' || kind == 'unit' || kind == 'topic';
    }
    return _protected.contains(name);
  }

  void _syncSecure() {
    final tabProtected = _tab == HighTab.notes || _tab == HighTab.exercise || _tab == HighTab.matric;
    final stackProtected = _stack.isNotEmpty && _isProtected(_stack.last);
    final on = stackProtected || (tabProtected && _stack.isEmpty);
    if (on == _secureOn) return;
    _secureOn = on;
    ScreenshotGuard.set(on);
  }

  @override
  void dispose() {
    try {
      HighScope.read(context).stopTicker();
    } catch (_) {}
    ScreenshotGuard.set(false);
    super.dispose();
  }

  Widget _tabPage(HighTab t) => switch (t) {
    HighTab.home => const HomePage(),
    HighTab.notes => const NotesHomePage(),
    HighTab.exercise => const ExercisePage(),
    HighTab.matric => const ExamsPage(),
    HighTab.tutor => const TutorPage(),
  };

  @override
  Widget build(BuildContext context) {
    HighScope.of(context);
    _visited.add(_tab);
    final tabs = [for (final t in HighTab.values) if (_visited.contains(t)) KeyedSubtree(key: ValueKey('tab:${t.name}:${_tabGen[t] ?? 0}'), child: _tabPage(t))];
    final pages = [...tabs, ..._stack];
    final top = _stack.isNotEmpty ? _stack.last : tabs.firstWhere((w) => w.key == ValueKey('tab:${_tab.name}:${_tabGen[_tab] ?? 0}'));
    final showNav = _stack.isEmpty || (_stack.last is KeyedSubtree && (_stack.last as KeyedSubtree).child is! NoNav);
    _syncSecure();
    return PopScope(
      canPop: canPop,
      onPopInvokedWithResult: (did, _) {
        if (!did && !(_sheets.isNotEmpty && _sheets.last.lock)) back();
      },
      child: KeyboardInset(
        child: Builder(
          builder: (context) => Stack(
            children: [
              for (final pg in pages)
                Positioned.fill(
                  key: pg.key,
                  child: Offstage(
                    offstage: !identical(pg, top),
                    child: TickerMode(enabled: identical(pg, top), child: Enter(child: pg)),
                  ),
                ),
              // The floating nav hides while typing so the input and keyboard get the room.
              if (showNav && !KeyboardInset.isOpen(context))
                Positioned(left: 14, right: 14, bottom: 14 + MediaQuery.paddingOf(context).bottom, child: NavBar(current: _tab, onTap: tab)),
              for (final s in _sheets) Positioned.fill(key: s.key, child: SheetLayer(lock: s.lock, bare: s.bare, onClose: back, child: s.child)),
              const Positioned(left: 14, right: 14, bottom: 0, child: TourCard()),
            ],
          ),
        ),
      ),
    );
  }
}


/// `.enter` page entrance (.42s cubic-bezier(.2,.8,.2,1): fade + translateY 12px)
class Enter extends StatefulWidget {
  const Enter({super.key, required this.child});
  final Widget child;
  @override
  State<Enter> createState() => _EnterState();
}

const enterCurve = Cubic(.2, .8, .2, 1);

class _EnterState extends State<Enter> with SingleTickerProviderStateMixin {
  late final AnimationController _c = AnimationController(vsync: this, duration: const Duration(milliseconds: 420))..value = 1;
  @override
  void dispose() {
    _c.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) => AnimatedBuilder(
    animation: _c,
    child: widget.child,
    builder: (_, child) {
      final t = enterCurve.transform(_c.value);
      return Opacity(opacity: t, child: Transform.translate(offset: Offset(0, 12 * (1 - t)), child: child));
    },
  );
}

/// floating raised nav bar: keys raised, current key pressed in (sage)
class NavBar extends StatelessWidget {
  const NavBar({super.key, required this.current, required this.onTap});
  final HighTab current;
  final ValueChanged<HighTab> onTap;
  static const items = [
    (HighTab.home, 'home', 'Home'),
    (HighTab.notes, 'book', 'Notes'),
    (HighTab.exercise, 'pen', 'Exercise'),
    (HighTab.matric, 'trophy', 'Matric'),
    (HighTab.tutor, 'chat', 'Tutor'),
  ];
  @override
  Widget build(BuildContext context) {
    final k = Kit.of(context), p = k.p;
    return SizedBox(
      height: 76,
      child: DecoratedBox(
        decoration: k.d.nav(),
        child: Padding(
          padding: const EdgeInsets.fromLTRB(8, 0, 8, 4),
          child: Row(
            spacing: 6,
            children: [
              for (final (t, icon, label) in items)
                Expanded(
                  flex: t == current ? 125 : 100,
                  child: Press(
                    key: ValueKey(t),
                    label: label,
                    onTap: () => onTap(t),
                    selected: t == current,
                    deco: k.d.navKey(),
                    pressedDeco: t == current ? k.d.navKeyOn() : k.d.navKey().copyWith(shadows: k.d.navKeyOn().shadows),
                    dy: 4,
                    child: SizedBox(
                      height: 56,
                      child: DecoratedBox(
                        decoration: BoxDecoration(
                          borderRadius: BorderRadius.circular(16),
                          border: Kit.of(context).s.tourWants(t.name) ? Border.all(color: p.coral, width: 2.5) : null,
                        ),
                        child: Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        spacing: 3,
                        children: [
                          Transform.translate(
                            offset: Offset(0, t == current ? -1 : 0),
                            child: Transform.scale(scale: t == current ? 1.06 : 1, child: Ic(icon, size: 22, color: t == current ? p.sage.deep : p.ink3)),
                          ),
                          Text(label, style: ts(11, w800, t == current ? p.sage.deep : p.ink3), maxLines: 1, softWrap: false, overflow: TextOverflow.clip),
                        ],
                        ),
                      ),
                    ),
                  ),
                ),
            ],
          ),
        ),
      ),
    );
  }
}

/// `.scrim` + `.sheet` (slides up with the spring; tap outside closes unless locked)
class SheetLayer extends StatefulWidget {
  const SheetLayer({super.key, required this.child, required this.onClose, this.lock = false, this.bare = false});
  final Widget child;
  final VoidCallback onClose;
  final bool lock, bare;
  @override
  State<SheetLayer> createState() => _SheetLayerState();
}

class _SheetLayerState extends State<SheetLayer> with SingleTickerProviderStateMixin {
  late final AnimationController _c = AnimationController(vsync: this, duration: const Duration(milliseconds: 500))..forward();
  @override
  void dispose() {
    _c.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final k = Kit.of(context);
    final mq = MediaQuery.of(context);
    return AnimatedBuilder(
      animation: _c,
      builder: (context, child) {
        final o = (_c.value / .6).clamp(0.0, 1.0), y = 1 - springCurve.transform(_c.value);
        return Stack(
          children: [
            Positioned.fill(
              child: GestureDetector(
                onTap: widget.lock ? null : widget.onClose,
                child: ColoredBox(color: Color.fromRGBO(40, 28, 20, .35 * o)),
              ),
            ),
            Align(
              alignment: Alignment.bottomCenter,
              child: FractionalTranslation(translation: Offset(0, y.clamp(-.05, 1.0)), child: child),
            ),
          ],
        );
      },
      child: widget.bare
          ? ConstrainedBox(constraints: BoxConstraints(maxHeight: mq.size.height * .92, maxWidth: 760), child: SingleChildScrollView(child: widget.child))
          : ConstrainedBox(
        constraints: BoxConstraints(maxHeight: mq.size.height * .92, maxWidth: 760),
        child: DecoratedBox(
          decoration: k.d.sheet(),
          child: SingleChildScrollView(
            padding: EdgeInsets.fromLTRB(20, 10, 20, 26 + mq.viewInsets.bottom + mq.padding.bottom),
            child: Column(
              mainAxisSize: MainAxisSize.min,
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                Center(
                  child: Container(
                    width: 44,
                    height: 5,
                    margin: const EdgeInsets.only(bottom: 12),
                    decoration: BoxDecoration(color: withA(k.p.ink3, .35), borderRadius: BorderRadius.circular(9)),
                  ),
                ),
                widget.child,
              ],
            ),
          ),
        ),
      ),
    );
  }
}

/// access to the shell's sheet API
VoidCallback showSheet(BuildContext context, Widget child, {bool lock = false, bool bare = false}) => context.findAncestorStateOfType<HighShellState>()!.sheet(child, lock: lock, bare: bare);

/// Tablets / TVs (e.g. 1920×1080 Smart View): lay the UI out on a smaller logical canvas and scale it up, so type,
/// clay and images grow with the screen instead of stretching thin. Phones are untouched.
class BigScreen extends StatelessWidget {
  const BigScreen({super.key, required this.child});
  final Widget child;

  /// scale for a logical screen size (1 on phones; ~1.4 on a 1920×1080 TV at dpr 1)
  static double scaleFor(Size s) => s.shortestSide < 700 ? 1 : (s.shortestSide / 760).clamp(1.0, 2.0);

  @override
  Widget build(BuildContext context) {
    final mq = MediaQuery.of(context), f = scaleFor(mq.size);
    if (f == 1) return child;
    final sz = mq.size / f;
    return FittedBox(
      fit: BoxFit.fill,
      alignment: Alignment.topLeft,
      child: SizedBox(
        width: sz.width,
        height: sz.height,
        child: MediaQuery(data: mq.copyWith(size: sz, padding: mq.padding / f, viewPadding: mq.viewPadding / f, viewInsets: mq.viewInsets / f), child: child),
      ),
    );
  }
}

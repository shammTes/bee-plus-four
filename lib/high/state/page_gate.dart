// Keeps hidden pages from rebuilding on every state change.
//
// Every widget that reads the state (Kit.of / HighScope.of / the notes AppScope.of) depends on it, so each
// notifyListeners() (an answer, a bookmark, a notes card marked read, a set finishing loading …) used to rebuild every
// page that is mounted: the visited tabs and the whole page stack, although only the top page is on screen. HighShell
// wraps each page in a PageGate. While the page is hidden the gate only notes that something changed; when it comes
// back on top it rebuilds the page's readers once. The visible page updates exactly as before.
import 'package:flutter/widgets.dart';

import '../notes/jr/state/app_state.dart' as jr show AppScope;
import 'app_state.dart';

class PageGate extends StatefulWidget {
  const PageGate({super.key, required this.active, required this.child});

  /// the page is on screen (top of the stack / current tab)
  final bool active;
  final Widget child;

  @override
  State<PageGate> createState() => _PageGateState();
}

class _PageGateState extends State<PageGate> {
  Listenable? _src;
  int _rev = 0;
  bool _stale = false;

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
    // the notes AppState forwards every HighState change, so it covers both
    final src = context.getInheritedWidgetOfExactType<jr.AppScope>()?.notifier ?? context.getInheritedWidgetOfExactType<HighScope>()?.notifier;
    if (!identical(src, _src)) {
      _src?.removeListener(_changed);
      _src = src?..addListener(_changed);
    }
  }

  void _changed() {
    if (!mounted) return;
    if (widget.active) {
      setState(() => _rev++);
    } else {
      _stale = true;
    }
  }

  @override
  void didUpdateWidget(covariant PageGate old) {
    super.didUpdateWidget(old);
    if (widget.active && !old.active && _stale) {
      _stale = false;
      _rev++;
    }
  }

  @override
  void dispose() {
    _src?.removeListener(_changed);
    super.dispose();
  }

  @override
  Widget build(BuildContext context) => PageGateScope._(_rev, widget.child);
}

/// what the page's state readers depend on instead of the state itself (see [HighScope.of])
class PageGateScope extends InheritedWidget {
  const PageGateScope._(this.rev, Widget child) : super(child: child);
  final int rev;
  @override
  bool updateShouldNotify(PageGateScope old) => old.rev != rev;

  /// depends on the nearest gate, if any; true when there is one
  static bool depend(BuildContext c) => c.dependOnInheritedWidgetOfExactType<PageGateScope>() != null;
}

// Page scaffold. Lists build only visible rows so low-end phones stay smooth.
import 'package:flutter/widgets.dart';

import '../theme/tokens.dart';
import 'art.dart';
import 'kit.dart';
import '../theme/perf.dart';
import '../screens/settings.dart' show SettingsPage;

const kScreenBottom = 116.0;

/// Bottom space a screen keeps free: room for the floating nav bar, or just a small gap while the
/// keyboard is open (the nav bar is hidden then and [KeyboardInset] already lifted the page).
double screenBottom(BuildContext context, [double base = kScreenBottom]) =>
    KeyboardInset.isOpen(context) ? 12 : base + MediaQuery.paddingOf(context).bottom;

/// The app uses WidgetsApp (no Material Scaffold), so nothing moved content above the soft keyboard
/// and inputs ended up underneath it. This does what `Scaffold.resizeToAvoidBottomInset` does: the
/// child is laid out above the keyboard (so scroll views shrink and the focused field can scroll
/// into view), the bottom inset / safe-area padding is consumed, and [isOpen] tells descendants.
class KeyboardInset extends StatelessWidget {
  const KeyboardInset({super.key, required this.child});
  final Widget child;

  static bool isOpen(BuildContext context) => context.dependOnInheritedWidgetOfExactType<_KeyboardScope>()?.open ?? false;

  @override
  Widget build(BuildContext context) {
    final mq = MediaQuery.of(context);
    final kb = mq.viewInsets.bottom;
    final open = kb > 0;
    return _KeyboardScope(
      open: open,
      child: Padding(
        padding: EdgeInsets.only(bottom: kb),
        child: MediaQuery(
          data: mq.copyWith(
            viewInsets: mq.viewInsets.copyWith(bottom: 0),
            padding: open ? mq.padding.copyWith(bottom: 0) : mq.padding,
          ),
          child: child,
        ),
      ),
    );
  }
}

class _KeyboardScope extends InheritedWidget {
  const _KeyboardScope({required this.open, required super.child});
  final bool open;
  @override
  bool updateShouldNotify(_KeyboardScope old) => old.open != open;
}

/// Scrolls the widget at [context] into view once the keyboard has opened (call after focus).
void revealAboveKeyboard(BuildContext context) {
  if (!context.mounted || Scrollable.maybeOf(context) == null) return;
  Scrollable.ensureVisible(
    context,
    alignment: .5,
    alignmentPolicy: ScrollPositionAlignmentPolicy.keepVisibleAtEnd,
    duration: const Duration(milliseconds: 180),
    curve: Curves.easeOut,
  );
}

/// Idle float/pulse. Off by default so weak GPUs are not repainting off-screen.
bool highDecorAnimations = false;

class TopBar extends StatelessWidget {
  const TopBar({super.key, required this.title, this.sub, this.onBack, this.actions = const [], this.tab = true, this.coachKey});
  /// set on exactly one mounted TopBar (Home) so the coach marks can spotlight the Settings avatar
  final GlobalKey? coachKey;
  final String title;
  final String? sub;
  final VoidCallback? onBack;
  final List<Widget> actions;
  final bool tab;
  @override
  Widget build(BuildContext context) {
    final k = Kit.of(context), p = k.p;
    final status = MediaQuery.paddingOf(context).top;
    return ConstrainedBox(
      constraints: const BoxConstraints(minHeight: 66),
      child: Padding(
        padding: EdgeInsets.fromLTRB(18, 10 + status, 18, 8),
        child: Row(
          spacing: 10,
          children: [
            if (onBack != null) CBtn('back', onTap: onBack!, label: 'Back'),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                mainAxisSize: MainAxisSize.min,
                children: [
                  Tx(title, style: ts(20, w900, p.ink, height: 1.15, spacing: -.2), ellipsis: true),
                  if (sub != null) Tx(sub!, style: ts(12.5, w700, p.ink3, height: 1.15), ellipsis: true),
                ],
              ),
            ),
            ...actions,
            CBtn(p.dark ? 'sun' : 'moon', onTap: k.s.toggleTheme, label: 'Toggle dark mode'),
            if (tab) KeyedSubtree(key: coachKey, child: Avatar(onTap: () => HighNav.of(context).push(const SettingsPage()))),
          ],
        ),
      ),
    );
  }
}

enum HighTab { home, notes, exercise, matric, tutor }

mixin NoNav on Widget {}

abstract class HighNav {
  static HighNav of(BuildContext c) {
    HighNav? n;
    c.visitAncestorElements((e) {
      if (e is StatefulElement && e.state is HighNav) {
        n = e.state as HighNav;
        return false;
      }
      return true;
    });
    return n!;
  }

  void tab(HighTab t);
  void push(Widget page);
  void open(String key, Widget Function() build);
  void back();
  HighTab get current;
}

abstract interface class Spaced {
  EdgeInsets get blockMargin;
}

class _Bare extends InheritedWidget {
  const _Bare({required this.target, required super.child});
  final Widget target;
  @override
  bool updateShouldNotify(_Bare old) => false;
}

EdgeInsets bareM(BuildContext c, Widget w, EdgeInsets m) => isBare(c, w) ? EdgeInsets.zero : m;
bool isBare(BuildContext c, Widget w) => identical(c.getInheritedWidgetOfExactType<_Bare>()?.target, w);
Widget _target(Widget w) => w is Delegating ? _target((w as Delegating).inner) : w;

abstract interface class Delegating {
  Widget get inner;
}

EdgeInsets marginOf(Widget w) {
  final t = _target(w);
  return t is Spaced ? (t as Spaced).blockMargin : EdgeInsets.zero;
}

double _gap(double a, double b) {
  if (a >= 0 && b >= 0) return a > b ? a : b;
  if (a < 0 && b < 0) return a < b ? a : b;
  return a + b;
}

List<Widget> collapse(List<Widget> children, {bool leading = true, bool trailing = true}) {
  final out = <Widget>[];
  double prev = 0;
  for (var i = 0; i < children.length; i++) {
    final c = children[i], m = marginOf(c);
    final g = i == 0 ? (leading ? m.top : 0.0) : _gap(prev, m.top);
    Widget w = _Bare(target: _target(c), child: c);
    if (g != 0) w = g > 0 ? Padding(padding: EdgeInsets.only(top: g), child: w) : Transform.translate(offset: Offset(0, g), child: w);
    if (m.left != 0 || m.right != 0) w = Padding(padding: EdgeInsets.only(left: m.left, right: m.right), child: w);
    out.add(w);
    prev = m.bottom;
  }
  if (trailing && prev > 0) out.add(SizedBox(height: prev));
  return out;
}

class Blocks extends StatelessWidget {
  const Blocks({super.key, required this.children});
  final List<Widget> children;
  @override
  Widget build(BuildContext context) => Column(crossAxisAlignment: CrossAxisAlignment.stretch, children: collapse(children));
}

class ScreenList extends StatelessWidget {
  const ScreenList({super.key, required this.children, this.controller, this.bottom = kScreenBottom, this.top = 4});
  final List<Widget> children;
  final ScrollController? controller;
  final double bottom, top;
  @override
  Widget build(BuildContext context) {
    final items = collapse(children);
    final cache = Perf.cacheExtent(context);
    return ScrollConfiguration(
      behavior: const NoGlow(),
      child: ListView.builder(
        controller: controller,
        padding: EdgeInsets.fromLTRB(16, top, 16, screenBottom(context, bottom)),
        cacheExtent: cache,
        addAutomaticKeepAlives: false,
        addRepaintBoundaries: true,
        physics: const ClampingScrollPhysics(),
        itemCount: items.length,
        itemBuilder: (context, i) => items[i],
      ),
    );
  }
}

class NoGlow extends ScrollBehavior {
  const NoGlow();
  @override
  Widget buildScrollbar(BuildContext context, Widget child, ScrollableDetails details) => child;
  @override
  ScrollPhysics getScrollPhysics(BuildContext context) => const ClampingScrollPhysics();
}

class PageShell extends StatelessWidget {
  const PageShell({super.key, required this.top, required this.body});
  final Widget top, body;
  static const maxWidth = 860.0;
  @override
  Widget build(BuildContext context) {
    final col = Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [top, Expanded(child: body)],
    );
    return MediaQuery.sizeOf(context).width <= maxWidth ? col : Center(child: SizedBox(width: maxWidth, child: col));
  }
}

class CardHead extends StatelessWidget {
  const CardHead(this.title, {super.key, this.small, this.trailing});
  final String title;
  final String? small;
  final Widget? trailing;
  @override
  Widget build(BuildContext context) {
    final p = Kit.of(context).p;
    return Padding(
      padding: const EdgeInsets.only(bottom: 12),
      child: Row(
        spacing: 8,
        children: [
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(title, style: ts(16.5, w900, p.ink, spacing: -.165)),
                if (small != null) Text(small!, style: ts(12, w700, p.ink3)),
              ],
            ),
          ),
          ?trailing,
        ],
      ),
    );
  }
}

class Float extends StatefulWidget {
  const Float({super.key, required this.child});
  final Widget child;
  @override
  State<Float> createState() => _FloatState();
}

class _FloatState extends State<Float> with SingleTickerProviderStateMixin {
  late final AnimationController _c = AnimationController(vsync: this, duration: const Duration(milliseconds: 3200));
  @override
  void initState() {
    super.initState();
    if (highDecorAnimations) _c.repeat();
  }

  @override
  void dispose() {
    _c.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    if (!highDecorAnimations || !TickerMode.valuesOf(context).enabled) return widget.child;
    return AnimatedBuilder(
      animation: _c,
      child: widget.child,
      builder: (_, child) {
        final x = _c.value < .5 ? _c.value * 2 : (1 - _c.value) * 2;
        final e = Curves.easeInOut.transform(x);
        return Transform.translate(offset: Offset(0, -4 * e), child: Transform.rotate(angle: -3 * e * 3.14159265 / 180, child: child));
      },
    );
  }
}

class Kokob extends StatelessWidget {
  const Kokob({super.key, this.width = 62, this.float = true});
  final double width;
  final bool float;
  @override
  Widget build(BuildContext context) {
    final a = SizedBox(width: width, height: width, child: Art('kokob', palette: Kit.of(context).p, width: width, height: width));
    return float && highDecorAnimations ? Float(child: a) : a;
  }
}

class Blk extends StatelessWidget implements Spaced {
  const Blk({super.key, required this.margin, required this.child});
  final EdgeInsets margin;
  final Widget child;
  @override
  EdgeInsets get blockMargin => margin;
  @override
  Widget build(BuildContext context) => Padding(padding: bareM(context, this, margin), child: child);
}

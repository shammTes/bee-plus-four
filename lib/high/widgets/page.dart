// Page scaffold matching the web layout: fixed `.topbar` (padding 16 18 8, min-height 66, gap 10) above the scrolling
// `.screen` (padding 4 16 116; the nav floats over the bottom).
import 'package:flutter/widgets.dart';

import '../theme/tokens.dart';
import 'art.dart';
import 'kit.dart';
import '../screens/settings.dart' show SettingsPage;

/// bottom padding of `.screen` (the floating nav bar covers it)
const kScreenBottom = 116.0;

/// global switch for decorative infinite animations (float, pulse); tests turn it off so frames settle
bool highDecorAnimations = true;

class TopBar extends StatelessWidget {
  const TopBar({super.key, required this.title, this.sub, this.onBack, this.actions = const [], this.tab = true});
  final String title;
  final String? sub;
  final VoidCallback? onBack;
  final List<Widget> actions;

  /// tab pages show theme + avatar; pushed pages show back + theme
  final bool tab;
  @override
  Widget build(BuildContext context) {
    final k = Kit.of(context), p = k.p;
    return ConstrainedBox(
      constraints: const BoxConstraints(minHeight: 66),
      child: Padding(
        padding: const EdgeInsets.fromLTRB(18, 16, 18, 8),
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
            if (tab) Avatar(onTap: () => HighNav.of(context).push(const SettingsPage())),
          ],
        ),
      ),
    );
  }
}

enum HighTab { home, notes, exercise, matric, tutor }

/// marker for pushed pages that hide the bottom nav (notes unit page)
mixin NoNav on Widget {}

/// navigation API of the shell (web `go()` / `back()` / nav tabs)
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

  /// push a page identified by [key]; if that page is already on the stack, pop back to it instead (no pile-up)
  void open(String key, Widget Function() build);
  void back();
  HighTab get current;
}

/// A block with CSS vertical margins. Siblings laid out by [collapse] get collapsed margins
/// (gap = max(prev.bottom, next.top), negative margins added), like normal block flow in the browser.
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

/// true when [w]'s vertical margin is already applied by an enclosing [collapse]
bool isBare(BuildContext c, Widget w) => identical(c.getInheritedWidgetOfExactType<_Bare>()?.target, w);

Widget _target(Widget w) => w is Delegating ? _target((w as Delegating).inner) : w;

/// wrapper widgets (entrance animations) that pass their child's margins through
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

/// lays out [children] as CSS blocks with collapsing vertical margins; [trailing] keeps the last bottom margin
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

/// a Column of CSS blocks (margins collapsed)
class Blocks extends StatelessWidget {
  const Blocks({super.key, required this.children});
  final List<Widget> children;
  @override
  Widget build(BuildContext context) => Column(crossAxisAlignment: CrossAxisAlignment.stretch, children: collapse(children));
}

/// scrolling `.screen`
class ScreenList extends StatelessWidget {
  const ScreenList({super.key, required this.children, this.controller, this.bottom = kScreenBottom, this.top = 4});
  final List<Widget> children;
  final ScrollController? controller;
  final double bottom, top;
  @override
  Widget build(BuildContext context) => ScrollConfiguration(
    behavior: const NoGlow(),
    child: ListView(
      controller: controller,
      padding: EdgeInsets.fromLTRB(16, top, 16, bottom + MediaQuery.paddingOf(context).bottom),
      children: collapse(children),
    ),
  );
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
  @override
  Widget build(BuildContext context) => Column(
    crossAxisAlignment: CrossAxisAlignment.stretch,
    children: [
      top,
      Expanded(child: body),
    ],
  );
}

/// `.hd` card header: h3 (16.5/900) + small, trailing widget
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

/// `.kokob-float`: 3.2 s ease-in-out translateY(-4px) rotate(-3deg) at 50%
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
  Widget build(BuildContext context) => AnimatedBuilder(
    animation: _c,
    child: widget.child,
    builder: (_, child) {
      final x = _c.value < .5 ? _c.value * 2 : (1 - _c.value) * 2;
      final e = Curves.easeInOut.transform(x);
      return Transform.translate(offset: Offset(0, -4 * e), child: Transform.rotate(angle: -3 * e * 3.14159265 / 180, child: child));
    },
  );
}

/// the Kokob mascot (ART.kokob) at [width]
class Kokob extends StatelessWidget {
  const Kokob({super.key, this.width = 62, this.float = true});
  final double width;
  final bool float;
  @override
  Widget build(BuildContext context) {
    final a = SizedBox(width: width, height: width, child: Art('kokob', palette: Kit.of(context).p, width: width, height: width));
    return float ? Float(child: a) : a;
  }
}

/// any widget with CSS block margins
class Blk extends StatelessWidget implements Spaced {
  const Blk({super.key, required this.margin, required this.child});
  final EdgeInsets margin;
  final Widget child;
  @override
  EdgeInsets get blockMargin => margin;
  @override
  Widget build(BuildContext context) => Padding(padding: bareM(context, this, margin), child: child);
}

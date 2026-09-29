// Sheets and large-screen scale.
import 'package:flutter/widgets.dart';

import 'state/app_state.dart';
import 'theme/tokens.dart';
import 'widgets/kit.dart';
import 'widgets/page.dart';
import 'shell_nav.dart';

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

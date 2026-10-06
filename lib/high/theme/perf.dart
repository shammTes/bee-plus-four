// Performance switches shared by High and the notes renderer.
//
// The FLAT look is ON by default (Settings > Look): every clay decoration is painted as a solid soft colour with a 1px
// border, plus one hard offset ledge under keys and buttons (see theme/clay.dart). No blur, gradient shader, clip or
// offscreen layer is drawn for a card, so long lists scroll at 60 fps on 1-2 GB phones with old Mali / Adreno GPUs.
// Decorative animations (entrance fades, count-ups, floating art, pulses) are gone in both looks.
//
// "Clay" (opt-in) brings back the soft shadows: blurred outer shadows (drawn analytically, fairly cheap) and inset
// shadows painted as gradient bands at the edges instead of a Gaussian mask blur over a card-sized offscreen layer.
import 'dart:math' as math;
import 'dart:ui' as ui;

import 'package:flutter/widgets.dart';

class Perf {
  Perf._();

  /// flat look (default). Settings > Look > Clay turns it off.
  static bool flat = true;

  /// decorative looping animations (pulsing pins …): off. They kept the GPU busy at 60 fps while the student reads.
  static bool animations = false;

  /// read-ahead for long lists, in logical px: enough for one fling, not so much that off-screen cards are laid out early
  static double cacheExtent(BuildContext context) => (MediaQuery.sizeOf(context).height * .4).clamp(250.0, 400.0);

  /// switch Flat on / off at runtime and repaint everything (decorations compare equal, so a plain rebuild would not
  /// repaint them)
  static void setFlat(bool v) {
    if (flat == v) return;
    flat = v;
    WidgetsBinding.instance.reassembleApplication();
  }
}

// ---------------------------------------------------------------- cheap inset shadow

/// 1 - Φ(t): share of a Gaussian (σ = 1) beyond t; coverage of a blurred edge t σ inside the shadow
double _tail(double t) {
  // Abramowitz–Stegun 7.1.26 erf approximation (|error| < 1.5e-7)
  final x = t.abs() / math.sqrt2;
  final k = 1 / (1 + .3275911 * x);
  final erf = 1 - (((((1.061405429 * k - 1.453152027) * k) + 1.421413741) * k - .284496736) * k + .254829592) * k * math.exp(-x * x);
  return t >= 0 ? .5 * (1 - erf) : .5 * (1 + erf);
}

const _ts = [-2.0, -1.0, 0.0, 1.0, 2.0];

/// Paints a CSS `box-shadow: inset dx dy blur spread color` inside [rr] (already clipped by the caller) as up to four
/// edge gradient bands. Each band follows the blurred edge of the shadow "hole" (the box shrunk by spread and moved by
/// dx/dy) with a Gaussian falloff, so it looks like the mask-blurred version without any offscreen blur pass.
void paintInsetBands(Canvas canvas, RRect rr, double dx, double dy, double blur, double spread, Color color) {
  final r = rr.outerRect;
  final sigma = math.max(blur / 2, .5);
  // distance from each edge to the hole's edge (where the shadow is at 50 %)
  final edges = [
    (spread + dy, 0), // top
    (spread - dy, 1), // bottom
    (spread + dx, 2), // left
    (spread - dx, 3), // right
  ];
  final a0 = color.a;
  for (final (e, side) in edges) {
    final ext = e + 2 * sigma; // beyond this the shadow is < 2.3 %
    if (ext <= .5) continue;
    final vertical = side < 2;
    final len = math.min(ext, vertical ? r.height : r.width);
    final stops = <double>[0];
    final cols = <Color>[color.withValues(alpha: a0 * _tail(-e / sigma))];
    for (final t in _ts) {
      final x = e + t * sigma;
      if (x <= 0 || x >= len) continue;
      stops.add(x / len);
      cols.add(color.withValues(alpha: a0 * _tail(t)));
    }
    if (stops.last < 1) {
      stops.add(1);
      cols.add(color.withValues(alpha: a0 * _tail((len - e) / sigma)));
    }
    final (Rect band, Offset from, Offset to) = switch (side) {
      0 => (Rect.fromLTWH(r.left, r.top, r.width, len), r.topLeft, Offset(r.left, r.top + len)),
      1 => (Rect.fromLTWH(r.left, r.bottom - len, r.width, len), r.bottomLeft, Offset(r.left, r.bottom - len)),
      2 => (Rect.fromLTWH(r.left, r.top, len, r.height), r.topLeft, Offset(r.left + len, r.top)),
      _ => (Rect.fromLTWH(r.right - len, r.top, len, r.height), r.topRight, Offset(r.right - len, r.top)),
    };
    canvas.drawRect(band, Paint()..shader = ui.Gradient.linear(from, to, cols, stops));
  }
}

// ---------------------------------------------------------------- cheap dimming

/// Dims [child] like `Opacity(opacity)` without an offscreen layer: in the flat look a translucent veil of the colour
/// behind the child ([over], usually the card surface) is painted on top, which on a solid background looks the same.
/// An Opacity layer per dimmed option was a saveLayer per answered question while scrolling.
bool get flatNow => Perf.flat;

class Dim extends StatelessWidget {
  const Dim({super.key, required this.opacity, required this.over, required this.child, this.radius});
  final double opacity;
  final Color over;
  final BorderRadius? radius;
  final Widget child;
  @override
  Widget build(BuildContext context) {
    if (opacity >= 1) return child;
    if (!flatNow) return Opacity(opacity: opacity, child: child);
    return DecoratedBox(
      position: DecorationPosition.foreground,
      decoration: BoxDecoration(color: over.withValues(alpha: (1 - opacity).clamp(0.0, 1.0)), borderRadius: radius),
      child: child,
    );
  }
}

// Copied from Junior (junior_flutter/lib/junior/theme/clay.dart) + AngleFill for CSS linear-gradient(<angle>).
// The notes renderer (notes/jr/theme/clay.dart) re-exports this file, so there is one painter for the whole app.
//
// Decorations are still described like the CSS (layered backgrounds + outer AND inset box-shadows), but by default
// ([Perf.flat]) they are painted FLAT: one solid soft colour, a 1px border, at most one hard (non-blurred) offset "ledge"
// under keys and buttons, and a solid ring for selected keys. No mask blur, no gradient shaders, no clip, no offscreen
// layer: a card costs 2-3 rrect draws, which old Mali / Adreno GPUs handle at 60 fps. The pressed look still changes:
// the ledge shrinks and a top inner shadow ("pushed in") darkens the fill. Settings > Look > Clay brings the soft clay
// shadows back (blurred outer shadows + cheap gradient bands for the inset ones).
import 'dart:math' as math;
import 'dart:ui' as ui;

import 'package:flutter/widgets.dart';

import 'tokens.dart';
import 'perf.dart';

/// One CSS box-shadow.
@immutable
class Shadow3 {
  final double dx, dy, blur, spread;
  final Color color;
  final bool inset;
  const Shadow3(this.dx, this.dy, this.blur, this.spread, this.color, {this.inset = false});
  const Shadow3.inset(this.dx, this.dy, this.blur, this.spread, this.color) : inset = true;

  Shadow3 scaleAlpha(double f) => Shadow3(dx, dy, blur, spread, withA(color, color.a * f), inset: inset);
  static Shadow3 lerp(Shadow3 a, Shadow3 b, double t) => Shadow3(
    ui.lerpDouble(a.dx, b.dx, t)!,
    ui.lerpDouble(a.dy, b.dy, t)!,
    ui.lerpDouble(a.blur, b.blur, t)!,
    ui.lerpDouble(a.spread, b.spread, t)!,
    Color.lerp(a.color, b.color, t)!,
    inset: b.inset,
  );

  @override
  bool operator ==(Object o) => o is Shadow3 && o.dx == dx && o.dy == dy && o.blur == blur && o.spread == spread && o.color == color && o.inset == inset;
  @override
  int get hashCode => Object.hash(dx, dy, blur, spread, color, inset);
}

/// One CSS background layer.
@immutable
sealed class Fill {
  const Fill();
  Paint paint(Rect r);
  Fill lerpTo(Fill other, double t) => t < .5 ? this : other;

  /// the one solid colour this layer becomes in the flat look; null = drop it. [overlay]: something is painted under
  /// this layer, so a gradient fading to transparent is a decorative sheen / glow and is dropped.
  Color? flatColor(bool overlay);
}

/// colour of a gradient at [t] (0..1)
Color _gradAt(List<Color> colors, List<double> stops, double t) {
  if (colors.isEmpty) return const Color(0x00000000);
  if (t <= stops.first || colors.length == 1) return colors.first;
  for (var i = 1; i < colors.length && i < stops.length; i++) {
    if (t <= stops[i]) {
      final span = stops[i] - stops[i - 1];
      return Color.lerp(colors[i - 1], colors[i], span <= 0 ? 1 : (t - stops[i - 1]) / span)!;
    }
  }
  return colors.last;
}

Color? _flatGrad(List<Color> colors, List<double> stops, bool overlay, double t) {
  if (overlay && colors.any((c) => c.a < .05)) return null;
  return _gradAt(colors, stops, t);
}

class SolidFill extends Fill {
  final Color color;
  const SolidFill(this.color);
  @override
  Paint paint(Rect r) => Paint()..color = color;
  @override
  Color? flatColor(bool overlay) => color;
  @override
  Fill lerpTo(Fill other, double t) => other is SolidFill
      ? SolidFill(Color.lerp(color, other.color, t)!)
      : other is LinearFill && !other.horizontal
      ? LinearFill.vertical([for (final _ in other.colors) color], other.stops).lerpTo(other, t)
      : super.lerpTo(other, t);
  @override
  bool operator ==(Object o) => o is SolidFill && o.color == color;
  @override
  int get hashCode => color.hashCode;
}

/// linear-gradient(180deg, …) (top to bottom) or 90deg (left to right)
class LinearFill extends Fill {
  final List<Color> colors;
  final List<double> stops;
  final bool horizontal;
  const LinearFill.vertical(this.colors, this.stops) : horizontal = false;
  const LinearFill.horizontal(this.colors, this.stops) : horizontal = true;
  @override
  Paint paint(Rect r) =>
      Paint()..shader = ui.Gradient.linear(horizontal ? r.centerLeft : r.topCenter, horizontal ? r.centerRight : r.bottomCenter, colors, stops);
  @override
  Color? flatColor(bool overlay) => _flatGrad(colors, stops, overlay, .5);
  @override
  Fill lerpTo(Fill other, double t) {
    if (other is SolidFill) return lerpTo(LinearFill.vertical([for (final _ in colors) other.color], stops), t);
    if (other is LinearFill && other.colors.length == colors.length && other.horizontal == horizontal) {
      return LinearFill._(
        [for (var i = 0; i < colors.length; i++) Color.lerp(colors[i], other.colors[i], t)!],
        [for (var i = 0; i < stops.length; i++) ui.lerpDouble(stops[i], other.stops[i], t)!],
        horizontal,
      );
    }
    return super.lerpTo(other, t);
  }

  const LinearFill._(this.colors, this.stops, this.horizontal);
  @override
  bool operator ==(Object o) => o is LinearFill && _listEq(o.colors, colors) && _listEq(o.stops, stops) && o.horizontal == horizontal;
  @override
  int get hashCode => Object.hash(Object.hashAll(colors), Object.hashAll(stops), horizontal);
}

/// `linear-gradient(<deg>, …)`: CSS angle (0deg = to top, clockwise); the gradient line spans |w·sin a| + |h·cos a| like the browser.
class AngleFill extends Fill {
  final double deg;
  final List<Color> colors;
  final List<double> stops;
  const AngleFill(this.deg, this.colors, this.stops);
  @override
  Paint paint(Rect r) {
    final a = deg * math.pi / 180;
    final dir = Offset(math.sin(a), -math.cos(a));
    final len = (r.width * math.sin(a)).abs() + (r.height * math.cos(a)).abs();
    final c = r.center;
    return Paint()..shader = ui.Gradient.linear(c - dir * (len / 2), c + dir * (len / 2), colors, stops);
  }

  @override
  Color? flatColor(bool overlay) => _flatGrad(colors, stops, overlay, .5);

  @override
  bool operator ==(Object o) => o is AngleFill && o.deg == deg && _listEq(o.colors, colors) && _listEq(o.stops, stops);
  @override
  int get hashCode => Object.hash(deg, Object.hashAll(colors), Object.hashAll(stops));
}

/// radial-gradient(circle at X% Y%, …) (farthest-corner) or radial-gradient(RX% RY% at X% Y%, …) (ellipse, sizes relative to the box)
class RadialFill extends Fill {
  final double cx, cy; // fractions of the box
  final double? rx, ry; // ellipse radii as fractions of width / height; null = circle to the farthest corner
  final List<Color> colors;
  final List<double> stops;
  const RadialFill.circle(this.cx, this.cy, this.colors, this.stops) : rx = null, ry = null;
  const RadialFill.ellipse(this.rx, this.ry, this.cx, this.cy, this.colors, this.stops);
  @override
  Paint paint(Rect r) {
    final c = Offset(r.left + cx * r.width, r.top + cy * r.height);
    if (rx == null) {
      final d = [r.topLeft, r.topRight, r.bottomLeft, r.bottomRight].map((p) => (p - c).distance).reduce(math.max);
      return Paint()..shader = ui.Gradient.radial(c, d, colors, stops);
    }
    final ex = rx! * r.width, ey = ry! * r.height;
    final m = Matrix4.identity()
      ..translateByDouble(c.dx, c.dy, 0, 1)
      ..scaleByDouble(1, ey / ex, 1, 1)
      ..translateByDouble(-c.dx, -c.dy, 0, 1);
    return Paint()..shader = ui.Gradient.radial(c, ex, colors, stops, TileMode.clamp, m.storage);
  }

  /// most of a radial knob is near its outer colour
  @override
  Color? flatColor(bool overlay) => _flatGrad(colors, stops, overlay, .6);

  @override
  Fill lerpTo(Fill other, double t) {
    if (other is RadialFill && other.colors.length == colors.length && other.rx == rx) {
      return rx == null
          ? RadialFill.circle(cx, cy, [for (var i = 0; i < colors.length; i++) Color.lerp(colors[i], other.colors[i], t)!], stops)
          : RadialFill.ellipse(rx, ry, cx, cy, [for (var i = 0; i < colors.length; i++) Color.lerp(colors[i], other.colors[i], t)!], stops);
    }
    return super.lerpTo(other, t);
  }

  @override
  bool operator ==(Object o) => o is RadialFill && o.cx == cx && o.cy == cy && o.rx == rx && o.ry == ry && _listEq(o.colors, colors) && _listEq(o.stops, stops);
  @override
  int get hashCode => Object.hash(cx, cy, rx, ry, Object.hashAll(colors), Object.hashAll(stops));
}

bool _listEq<T>(List<T> a, List<T> b) {
  if (a.length != b.length) return false;
  for (var i = 0; i < a.length; i++) {
    if (a[i] != b[i]) return false;
  }
  return true;
}

/// A box painted like the CSS: `background: layer1, layer2…; box-shadow: s1, s2…; border-radius`.
/// Layers and shadows are given in CSS order (the first is on top).
@immutable
class ClayDecoration extends Decoration {
  final List<Fill> fills;
  final List<Shadow3> shadows;
  final BorderRadius radius;

  /// a solid inner ring (CSS `inset 0 0 0 Npx color`) is just a shadow; kept in [shadows].
  const ClayDecoration({this.fills = const [], this.shadows = const [], this.radius = BorderRadius.zero});

  ClayDecoration copyWith({List<Fill>? fills, List<Shadow3>? shadows, BorderRadius? radius}) =>
      ClayDecoration(fills: fills ?? this.fills, shadows: shadows ?? this.shadows, radius: radius ?? this.radius);

  @override
  EdgeInsetsGeometry get padding => EdgeInsets.zero;

  @override
  bool hitTest(Size size, Offset position, {TextDirection? textDirection}) => radius.toRRect(Offset.zero & size).contains(position);

  @override
  Path getClipPath(Rect rect, TextDirection textDirection) => Path()..addRRect(radius.resolve(textDirection).toRRect(rect));

  @override
  ClayDecoration? lerpFrom(Decoration? a, double t) => a is ClayDecoration ? ClayDecoration.lerp(a, this, t) : null;
  @override
  ClayDecoration? lerpTo(Decoration? b, double t) => b is ClayDecoration ? ClayDecoration.lerp(this, b, t) : null;

  /// CSS-like interpolation: shadow lists are padded with transparent copies so geometry and colour both animate.
  static ClayDecoration lerp(ClayDecoration a, ClayDecoration b, double t) {
    if (t <= 0) return a;
    if (t >= 1) return b;
    final n = math.max(a.shadows.length, b.shadows.length);
    Shadow3 at(List<Shadow3> l, List<Shadow3> o, int i) => i < l.length ? l[i] : o[i].scaleAlpha(0);
    final sh = <Shadow3>[];
    for (var i = 0; i < n; i++) {
      final x = at(a.shadows, b.shadows, i), y = at(b.shadows, a.shadows, i);
      if (x.inset == y.inset) {
        sh.add(Shadow3.lerp(x, y, t));
      } else {
        sh
          ..add(x.scaleAlpha(1 - t))
          ..add(y.scaleAlpha(t));
      }
    }
    final fills = a.fills.length == b.fills.length ? [for (var i = 0; i < a.fills.length; i++) a.fills[i].lerpTo(b.fills[i], t)] : (t < .5 ? a.fills : b.fills);
    return ClayDecoration(fills: fills, shadows: sh, radius: BorderRadius.lerp(a.radius, b.radius, t)!);
  }

  @override
  BoxPainter createBoxPainter([VoidCallback? onChanged]) => _ClayPainter(this);

  @override
  bool operator ==(Object o) => o is ClayDecoration && _listEq(o.fills, fills) && _listEq(o.shadows, shadows) && o.radius == radius;
  @override
  int get hashCode => Object.hash(Object.hashAll(fills), Object.hashAll(shadows), radius);
}

extension ClayPress on ClayDecoration {
  /// flat look: a key held down [t] (0..1) also darkens a little (the pressed decoration shrinks its ledge as well), so
  /// every tap shows a pushed-in colour change without any shadow blur
  ClayDecoration pressedBy(double t) =>
      !Perf.flat || t <= 0 ? this : copyWith(shadows: [...shadows, Shadow3.inset(0, 1, 1, 0, Color.fromRGBO(0, 0, 0, .16 * math.min(t, 1)))]);
}

class _ClayPainter extends BoxPainter {
  _ClayPainter(this.d);
  final ClayDecoration d;
  _FlatLook? _flat;

  static RRect _spread(RRect r, double s) {
    Radius adj(Radius x) => Radius.elliptical(math.max(0, x.x + s), math.max(0, x.y + s));
    return RRect.fromLTRBAndCorners(
      r.left - s,
      r.top - s,
      r.right + s,
      r.bottom + s,
      topLeft: adj(r.tlRadius),
      topRight: adj(r.trRadius),
      bottomLeft: adj(r.blRadius),
      bottomRight: adj(r.brRadius),
    );
  }

  @override
  void paint(Canvas canvas, Offset offset, ImageConfiguration cfg) {
    final size = cfg.size!;
    final rect = offset & size;
    final rr = d.radius.resolve(TextDirection.ltr).toRRect(rect).scaleRadii();
    if (Perf.flat) return (_flat ??= _FlatLook.of(d)).paint(canvas, rr);
    // Clay (opt-in): outer shadows, bottom-most (last in CSS) first. A blurred rounded rect is drawn analytically by
    // both Skia and Impeller.
    for (final s in d.shadows.reversed) {
      if (s.inset || s.color.a == 0) continue;
      final p = Paint()..color = s.color;
      if (s.blur > 0) p.maskFilter = MaskFilter.blur(BlurStyle.normal, s.blur / 2);
      canvas.drawRRect(_spread(rr, s.spread).shift(Offset(s.dx, s.dy)), p);
    }
    // backgrounds, bottom-most first
    for (final f in d.fills.reversed) {
      canvas.drawRRect(rr, f.paint(rect));
    }
    // inset shadows, clipped to the box
    final insets = d.shadows.reversed.where((s) => s.inset && s.color.a > 0).toList();
    if (insets.isEmpty) return;
    canvas.save();
    canvas.clipRRect(rr);
    for (final s in insets) {
      if (s.blur > 0) {
        // gradient bands instead of a mask blur over a card-sized offscreen layer (see theme/perf.dart)
        paintInsetBands(canvas, rr, s.dx, s.dy, s.blur, s.spread, s.color);
        continue;
      }
      final hole = _spread(rr, -s.spread).shift(Offset(s.dx, s.dy));
      final pad = s.spread.abs() + s.dx.abs() + s.dy.abs() + 4;
      final path = Path()
        ..fillType = PathFillType.evenOdd
        ..addRect(rect.inflate(pad))
        ..addRRect(hole);
      canvas.drawPath(path, Paint()..color = s.color);
    }
    canvas.restore();
  }
}

/// The flat version of a [ClayDecoration] (see the top of this file). Worked out once per decoration.
class _FlatLook {
  _FlatLook(this.fill, this.halo, this.ledge, this.ring, this.border);
  final Color? fill;

  /// solid outer ring (CSS `0 0 0 5px`): highlighted pins / keys
  final Shadow3? halo;

  /// hard offset shadow under a key / button (CSS `0 5px 0 edge`): the only shadow kept
  final Shadow3? ledge;

  /// solid inner ring (CSS `inset 0 0 0 2px`): selected keys
  final Shadow3? ring;

  /// 1px hairline that replaces the soft shadows of raised panels and sunk tracks
  final Color? border;

  static bool _darkish(Color c) => .2126 * c.r + .7152 * c.g + .0722 * c.b < .5;

  factory _FlatLook.of(ClayDecoration d) {
    Color? fill;
    for (var i = d.fills.length - 1; i >= 0; i--) {
      final c = d.fills[i].flatColor(fill != null);
      if (c == null || c.a == 0) continue;
      fill = fill == null ? c : Color.alphaBlend(c, fill);
    }
    Shadow3? halo, ledge, ring;
    Color? soft, sunk;
    var press = 0.0;
    Color? pressC;
    for (final s in d.shadows) {
      if (s.color.a == 0) continue;
      if (!s.inset) {
        if (s.blur == 0 && (s.dy > 0 || s.dx != 0) && s.spread >= 0) {
          ledge ??= s;
        } else if (s.blur == 0 && s.dx == 0 && s.dy == 0 && s.spread > 0) {
          halo ??= s;
        } else if (s.blur > 0) {
          soft ??= s.color;
        }
      } else if (s.blur == 0 && s.dx == 0 && s.dy == 0 && s.spread > 0) {
        ring ??= s;
      } else if (s.dy > 0 && _darkish(s.color)) {
        // a dark inner shadow along the top edge = pushed in: darken the fill a little instead
        sunk ??= s.color;
        if (s.color.a > press) {
          press = s.color.a;
          pressC = s.color;
        }
      }
    }
    if (fill != null && pressC != null) fill = Color.alphaBlend(withA(pressC, (press * .5).clamp(0.0, .3)), fill);
    Color? border;
    final b = soft ?? sunk;
    if (ledge == null && ring == null && halo == null && b != null) border = withA(b, (b.a * .6).clamp(.10, .28));
    return _FlatLook(fill, halo, ledge, ring, border);
  }

  void paint(Canvas canvas, RRect rr) {
    final h = halo;
    if (h != null) canvas.drawRRect(_ClayPainter._spread(rr, h.spread), Paint()..color = h.color);
    final l = ledge;
    if (l != null) canvas.drawRRect(_ClayPainter._spread(rr, l.spread).shift(Offset(l.dx, l.dy)), Paint()..color = l.color);
    final f = fill;
    if (f != null) canvas.drawRRect(rr, Paint()..color = f);
    final r = ring;
    if (r != null) {
      canvas.drawRRect(
        _ClayPainter._spread(rr, -r.spread / 2),
        Paint()
          ..color = r.color
          ..style = PaintingStyle.stroke
          ..strokeWidth = r.spread,
      );
    } else if (border != null && rr.width > 2 && rr.height > 2) {
      canvas.drawRRect(
        _ClayPainter._spread(rr, -.5),
        Paint()
          ..color = border!
          ..style = PaintingStyle.stroke
          ..strokeWidth = 1,
      );
    }
  }
}

// Interactive native sims for the notes: CustomPainter + clay sliders. One [SimSpec] per sim type, looked up by name
// from a media card {"kind":"sim","sim":"projectile","p":{...}}. Sims live in sims_*.dart.
import 'dart:math' as math;

import 'package:flutter/scheduler.dart';
import 'package:flutter/widgets.dart';

import '../notes/jr/notes/cards.dart' show ClaySlider;
import '../notes/jr/theme/notes_styles.dart';
import '../notes/jr/theme/tokens.dart';
import '../notes/jr/widgets/clay_widgets.dart';
import '../state/app_state.dart';
import '../widgets/page.dart' show highDecorAnimations;
import 'lab_kit.dart';
import 'lab_sims.dart';
import 'mesh3d.dart';
import 'sims_bio_geo.dart';
import 'sims_chem.dart';
import 'sims_math_econ.dart';
import 'sims_phys.dart';

typedef V = Map<String, double>;

class Prm {
  const Prm(this.name, this.label, this.min, this.max, this.def, {this.step = 1, this.unit = '', this.fmt});
  final String name, label, unit;
  final double min, max, def, step;
  final String Function(double v)? fmt;
  String show(double v) => fmt?.call(v) ?? '${v == v.roundToDouble() && step >= 1 ? v.toInt() : v.toStringAsFixed(step < .1 ? 2 : 1)}${unit.isEmpty ? '' : ' $unit'}';
}

class SimSpec {
  const SimSpec({required this.params, required this.paint, required this.out, this.animated = false, this.height = 260, this.ballStick});
  final List<Prm> params;
  final void Function(Canvas c, Size s, V v, double t, Palette p) paint;
  final List<(String, String)> Function(V v) out;
  final bool animated;
  final double height;

  /// 3D ball-and-stick scene instead of a flat painter (drag to turn)
  final BallStickPainter Function(V v, double yaw, double pitch, double zoom)? ballStick;
}

final Map<String, SimSpec Function(Map<String, dynamic> p)> kSims = {...physSims, ...chemSims, ...bioGeoSims, ...mathEconSims, ...labSims};

class SimBox extends StatefulWidget {
  const SimBox({super.key, required this.sim, required this.p, required this.gameKey, required this.unitId});
  final String sim, gameKey, unitId;
  final Map<String, dynamic> p;
  @override
  State<SimBox> createState() => _SimBoxState();
}

class _SimBoxState extends State<SimBox> with SingleTickerProviderStateMixin {
  late final SimSpec? spec = kSims[widget.sim]?.call(widget.p);
  late final V v = {for (final x in spec?.params ?? const <Prm>[]) x.name: (widget.p[x.name] as num?)?.toDouble() ?? x.def};
  double t = .8;
  Ticker? _tk;
  bool _touched = false;
  @override
  void initState() {
    super.initState();
    if ((spec?.animated ?? false) && highDecorAnimations) {
      _tk = createTicker((e) => setState(() => t = e.inMicroseconds / 1e6))..start();
    }
  }

  @override
  void dispose() {
    _tk?.dispose();
    super.dispose();
  }

  void _set(String k, double x) {
    setState(() => v[k] = x);
    if (!_touched) {
      _touched = true;
      HighScope.read(context).award('sim:${widget.gameKey}', 3, kind: 'sim');
    }
  }

  @override
  Widget build(BuildContext context) {
    final k = Kit.of(context), p = k.p, s = spec;
    if (s == null) return Text('(unknown sim ${widget.sim})', style: ts(14, FontWeight.w600, p.ink2));
    if (s is LabSpec) return LabView(spec: s, p: widget.p, gameKey: widget.gameKey);
    final outs = s.out(v);
    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        if (s.ballStick != null)
          MeshView(height: s.height, painter: (y, pi, z) => s.ballStick!(v, y, pi, z))
        else
          DecoratedBox(
            decoration: k.c.sunk(p.surface2, radius: 20),
            child: SizedBox(
              height: s.height,
              child: ClipRRect(
                borderRadius: BorderRadius.circular(20),
                child: CustomPaint(painter: _SimPainter(s, v, t, p, v.values.fold(0.0, (a, b) => a * 31 + b))),
              ),
            ),
          ),
        const SizedBox(height: 10),
        Wrap(
          spacing: 8,
          runSpacing: 8,
          children: [
            for (final (a, b) in outs)
              DecoratedBox(
                decoration: k.c.flat(p.butter.tile, radius: 14),
                child: Padding(
                  padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 7),
                  child: Text.rich(
                    TextSpan(
                      children: [
                        TextSpan(text: a.isEmpty ? '' : '$a  ', style: ts(14, FontWeight.w700, p.ink2)),
                        TextSpan(text: b, style: ts(16, FontWeight.w900, p.ink)),
                      ],
                    ),
                  ),
                ),
              ),
          ],
        ),
        for (final x in s.params) ...[
          Padding(
            padding: const EdgeInsets.only(top: 10),
            child: Row(
              children: [
                Expanded(child: Text(x.label, style: ts(15.5, FontWeight.w800, p.ink2))),
                Text(x.show(v[x.name]!), style: ts(16, FontWeight.w900, p.blue.deep)),
              ],
            ),
          ),
          ClaySlider(value: ((v[x.name]! - x.min) / x.step).round(), max: ((x.max - x.min) / x.step).round(), onChanged: (i) => _set(x.name, x.min + i * x.step)),
        ],
      ],
    );
  }
}

class _SimPainter extends CustomPainter {
  _SimPainter(this.s, this.v, this.t, this.p, this.sig);
  final SimSpec s;
  final V v;
  final double t, sig;
  final Palette p;
  @override
  void paint(Canvas canvas, Size size) => s.paint(canvas, size, v, t, p);
  @override
  bool shouldRepaint(_SimPainter o) => o.t != t || o.sig != sig || o.p != p;
}

// ---- drawing helpers shared by the sims
Paint st(Color c, [double w = 2]) => Paint()
  ..color = c
  ..style = PaintingStyle.stroke
  ..strokeWidth = w
  ..strokeCap = StrokeCap.round
  ..strokeJoin = StrokeJoin.round;
Paint fl(Color c) => Paint()..color = c;

void txt(Canvas c, String s, Offset o, Color col, {double size = 13, bool center = false, bool right = false, FontWeight w = FontWeight.w800}) {
  final tp = TextPainter(
    text: TextSpan(text: s, style: ts(size, w, col, height: 1.1)),
    textDirection: TextDirection.ltr,
  )..layout();
  tp.paint(c, o - Offset(center ? tp.width / 2 : (right ? tp.width : 0), center ? tp.height / 2 : 0));
}

void arrow(Canvas c, Offset a, Offset b, Color col, [double w = 2.5]) {
  c.drawLine(a, b, st(col, w));
  final d = b - a;
  if (d.distance < 1) return;
  final u = d / d.distance, n = Offset(-u.dy, u.dx), h = math.min(10.0, d.distance * .4);
  c.drawPath(
    Path()
      ..moveTo(b.dx, b.dy)
      ..lineTo(b.dx - u.dx * h + n.dx * h * .5, b.dy - u.dy * h + n.dy * h * .5)
      ..lineTo(b.dx - u.dx * h - n.dx * h * .5, b.dy - u.dy * h - n.dy * h * .5)
      ..close(),
    fl(col),
  );
}

void dashed(Canvas c, Offset a, Offset b, Paint pt, [double dash = 6]) {
  final d = b - a, n = (d.distance / dash).floor();
  for (var i = 0; i < n; i += 2) {
    c.drawLine(a + d * (i / n), a + d * ((i + 1) / n), pt);
  }
}

/// a plot area with axes; returns a mapper (x, y) -> screen
class Plot {
  Plot(
    this.c,
    Size s,
    this.x0,
    this.x1,
    this.y0,
    this.y1,
    this.p, {
    String xl = '',
    String yl = '',
    double left = 44,
    double bottom = 30,
    double top = 14,
    double right = 14,
    int? xt,
    int? yt,
  }) : r = Rect.fromLTRB(left, top, s.width - right, s.height - bottom) {
    c.drawLine(r.bottomLeft, r.bottomRight, st(p.ink2, 1.5));
    c.drawLine(r.bottomLeft, r.topLeft, st(p.ink2, 1.5));
    for (var i = 0; i <= (xt ?? 5); i++) {
      final x = x0 + (x1 - x0) * i / (xt ?? 5);
      txt(c, _n(x), at(x, y0) + const Offset(0, 5), p.ink2, size: 11, center: false);
    }
    for (var i = 0; i <= (yt ?? 4); i++) {
      final y = y0 + (y1 - y0) * i / (yt ?? 4);
      txt(c, _n(y), at(x0, y) - const Offset(6, 6), p.ink2, size: 11, right: true);
      if (i > 0) c.drawLine(at(x0, y), at(x1, y), st(p.line, .8));
    }
    txt(c, xl, r.bottomRight + const Offset(0, 16), p.ink2, size: 11.5, right: true);
    txt(c, yl, r.topLeft + const Offset(4, 0), p.ink2, size: 11.5);
  }
  final Canvas c;
  final Rect r;
  final double x0, x1, y0, y1;
  final Palette p;
  static String _n(double v) =>
      v.abs() >= 1000 ? '${(v / 1000).toStringAsFixed(v % 1000 == 0 ? 0 : 1)}k' : (v == v.roundToDouble() ? '${v.toInt()}' : v.toStringAsFixed(1));
  Offset at(double x, double y) => Offset(r.left + (x - x0) / (x1 - x0) * r.width, r.bottom - (y - y0) / (y1 - y0) * r.height);
  void curve(double Function(double x) f, Color col, {double w = 3, int n = 120, double? from, double? to}) {
    final a = from ?? x0, b = to ?? x1, path = Path();
    for (var i = 0; i <= n; i++) {
      final x = a + (b - a) * i / n, y = f(x).clamp(y0 - (y1 - y0), y1 + (y1 - y0)), o = at(x, y);
      i == 0 ? path.moveTo(o.dx, o.dy) : path.lineTo(o.dx, o.dy);
    }
    c.save();
    c.clipRect(r.inflate(2));
    c.drawPath(path, st(col, w));
    c.restore();
  }

  void dot(double x, double y, Color col, [double rad = 7]) {
    c.drawCircle(at(x, y), rad + 2, fl(const Color(0xFFFFFFFF)));
    c.drawCircle(at(x, y), rad, fl(col));
  }
}

String f1(double v) => v.toStringAsFixed(1);
String f2(double v) => v.toStringAsFixed(2);
String sig3(double v) {
  if (v == 0) return '0';
  final e = (math.log(v.abs()) / math.ln10).floor();
  if (e >= 5 || e <= -3) return '${(v / math.pow(10, e)).toStringAsFixed(2)}×10^$e';
  return v.toStringAsFixed(math.max(0, 2 - e));
}

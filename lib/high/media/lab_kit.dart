// Physics-lab sim framework (on top of sims.dart): sliders + choice chips, live readouts with the formula, a "Try this"
// prompt, play / pause / replay for animated labs and optional drag input on the canvas.
// Performance (low-end Android): one Ticker per lab, started only by the Play button and stopped when the lab scrolls
// off screen, its route is covered (TickerMode) or it has been left running untouched for 2 minutes. Frames repaint the
// canvas only (RepaintBoundary + repaint Listenable, no widget rebuild); readouts rebuild at ~8 Hz when they depend on
// time. Paints and text layouts are cached; no shadows or blurs.
import 'dart:math' as math;
import 'dart:typed_data';
import 'dart:ui' as ui;

import 'package:flutter/scheduler.dart';
import 'package:flutter/widgets.dart';

import '../notes/jr/notes/cards.dart' show ClaySlider;
import '../notes/jr/theme/tokens.dart';
import '../notes/jr/widgets/clay_widgets.dart';
import '../state/app_state.dart';
import 'sims.dart';

/// slider control (value in [V] under [name])
class Sl {
  const Sl(this.name, this.label, this.min, this.max, this.def, {this.step = 1, this.unit = '', this.fmt, this.when});
  final String name, label, unit;
  final double min, max, def, step;
  final String Function(double v)? fmt;
  final bool Function(V v)? when;
  String show(double v) => fmt?.call(v) ?? '${numStr(v, step)}${unit.isEmpty ? '' : ' $unit'}';
}

/// choice chips / toggle (the chosen index is stored in [V] under [name])
class Opt {
  const Opt(this.name, this.options, {this.label = '', this.def = 0, this.when});
  final String name, label;
  final List<String> options;
  final int def;
  final bool Function(V v)? when;
}

typedef LabPaint = void Function(Canvas c, Size s, V v, double t, Palette p);
typedef LabRead = List<(String, String)> Function(V v, double t);

void _noPaint(Canvas c, Size s, V v, double t, Palette p) {}
List<(String, String)> _noOut(V v) => const [];

/// A lab spec. It is a [SimSpec] so it registers in `kSims` like every other sim; [SimBox] hands it to [LabView].
/// The builder in the registry runs once per card, so a closure can keep per-card state for [step] / [reset].
class LabSpec extends SimSpec {
  LabSpec({
    this.sliders = const [],
    this.opts = const [],
    required this.draw,
    required this.read,
    this.formula = '',
    this.formulaOf,
    this.tryThis = '',
    this.anim = false,
    this.replay = false,
    super.height = 260,
    this.drag,
    this.pan = false,
    this.step,
    this.reset,
    this.changed,
    this.live = false,
    this.t0 = 0,
    this.tEnd,
  }) : super(params: const [], paint: _noPaint, out: _noOut);
  final List<Sl> sliders;
  final List<Opt> opts;
  final LabPaint draw;
  final LabRead read;
  final String formula, tryThis;
  final String Function(V v)? formulaOf;

  /// animated (Play button); [replay]: a run from t0 that restarts when a control changes
  final bool anim, replay;

  /// canvas touch: horizontal drags (or free 2-D drags when [pan]) and taps; set values in [V]
  final void Function(V v, Offset at, Size s)? drag;
  final bool pan;

  /// per-frame integration (dt in s) and its reset, for labs that are not closed-form in t
  final void Function(double dt, V v)? step;
  final void Function(V v)? reset;
  final void Function(V v, String key)? changed;

  /// readouts depend on t (rebuilt ~8×/s while running)
  final bool live;
  final double t0;

  /// a replay run stops by itself at this time
  final double Function(V v)? tEnd;
}

/// lets tests switch the 2-minute idle stop off
Duration labIdleStop = const Duration(minutes: 2);

class _Rep extends ChangeNotifier {
  void ping() => notifyListeners();
}

class LabView extends StatefulWidget {
  const LabView({super.key, required this.spec, required this.p, required this.gameKey});
  final LabSpec spec;
  final Map<String, dynamic> p;
  final String gameKey;
  @override
  State<LabView> createState() => LabViewState();
}

class LabViewState extends State<LabView> with SingleTickerProviderStateMixin {
  LabSpec get s => widget.spec;
  late final V v = _defaults();
  late double t = s.t0;
  double _base = 0, _lastOut = 0;
  int rev = 0;
  bool playing = false, _visible = true, _touched = false;
  late final Ticker _tk = createTicker(_onTick);
  final _rep = _Rep(), _outRep = _Rep();
  ScrollPosition? _pos;
  double _screenH = 2000;
  DateTime _lastTouch = DateTime.now();

  V _defaults() {
    final m = <String, double>{};
    for (final x in s.sliders) {
      m[x.name] = ((widget.p[x.name] as num?)?.toDouble() ?? x.def).clamp(x.min, x.max).toDouble();
    }
    for (final o in s.opts) {
      m[o.name] = ((widget.p[o.name] as num?)?.toInt() ?? o.def).clamp(0, o.options.length - 1).toDouble();
    }
    return m;
  }

  @override
  void initState() {
    super.initState();
    s.reset?.call(v);
    WidgetsBinding.instance.addPostFrameCallback((_) => _checkVisible());
  }

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
    final pos = Scrollable.maybeOf(context)?.position;
    if (pos != _pos) {
      _pos?.removeListener(_checkVisible);
      _pos = pos?..addListener(_checkVisible);
    }
  }

  @override
  void dispose() {
    _pos?.removeListener(_checkVisible);
    _tk.dispose();
    _rep.dispose();
    _outRep.dispose();
    super.dispose();
  }

  void _checkVisible() {
    if (!mounted) return;
    final ro = context.findRenderObject();
    if (ro is! RenderBox || !ro.attached || !ro.hasSize) return;
    final y = ro.localToGlobal(Offset.zero).dy;
    final vis = y < _screenH && y + ro.size.height > 0;
    if (vis != _visible) {
      _visible = vis;
      _sync();
    }
  }

  void _sync() {
    final run = playing && _visible;
    if (run && !_tk.isActive) {
      _base = t;
      _tk.start();
    } else if (!run && _tk.isActive) {
      _tk.stop();
    }
  }

  void _onTick(Duration e) {
    final nt = _base + e.inMicroseconds / 1e6, dt = (nt - t).clamp(0.0, .05);
    t = nt;
    if (s.step != null && dt > 0) s.step!(dt, v);
    final end = s.tEnd?.call(v);
    if (end != null && t >= end) {
      t = end;
      _pause();
    } else if (DateTime.now().difference(_lastTouch) > labIdleStop) {
      _pause();
    }
    _rep.ping();
    if (s.live && (t - _lastOut).abs() > .12) {
      _lastOut = t;
      _outRep.ping();
    }
  }

  void _pause() {
    playing = false;
    _sync();
    if (mounted) setState(() {});
  }

  void _award() {
    _lastTouch = DateTime.now();
    if (_touched) return;
    _touched = true;
    HighScope.read(context).award('sim:${widget.gameKey}', 3, kind: 'sim');
  }

  void _restart() {
    t = s.t0;
    s.reset?.call(v);
  }

  /// set a control value (slider, chip or drag)
  void set(String k, double x) {
    if (v[k] == x) return;
    setState(() {
      v[k] = x;
      rev++;
      if (s.replay) {
        _restart();
        playing = false;
        _sync();
      }
      s.changed?.call(v, k);
    });
    _award();
  }

  void togglePlay() {
    setState(() {
      if (!playing && s.replay && s.tEnd != null && t >= s.tEnd!(v) - 1e-6) _restart();
      playing = !playing;
      rev++;
    });
    _sync();
    _award();
  }

  void replay() {
    setState(() {
      _restart();
      rev++;
      if (s.replay || s.step != null) playing = true;
    });
    _base = t;
    if (_tk.isActive) _tk.stop();
    _sync();
    _award();
  }

  void _drag(Offset at, Size sz) {
    final before = Map.of(v);
    s.drag!(v, at, sz);
    var diff = false;
    for (final e in v.entries) {
      if (before[e.key] != e.value) {
        diff = true;
        s.changed?.call(v, e.key);
      }
    }
    if (!diff) return;
    setState(() {
      rev++;
      if (s.replay) {
        _restart();
        playing = false;
        _sync();
      }
    });
    _award();
  }

  @override
  Widget build(BuildContext context) {
    final k = Kit.of(context), p = k.p;
    _screenH = MediaQuery.sizeOf(context).height;
    Widget canvas = LayoutBuilder(
      builder: (context, box) {
        final sz = Size(box.maxWidth, s.height);
        Widget cp = CustomPaint(size: sz, painter: _LabPainter(this, p, rev, _rep));
        if (s.drag != null) {
          cp = GestureDetector(
            behavior: HitTestBehavior.opaque,
            onTapDown: (d) => _drag(d.localPosition, sz),
            onHorizontalDragUpdate: s.pan ? null : (d) => _drag(d.localPosition, sz),
            onPanUpdate: s.pan ? (d) => _drag(d.localPosition, sz) : null,
            child: cp,
          );
        }
        return cp;
      },
    );
    final flat = BoxDecoration(color: p.surface2, borderRadius: BorderRadius.circular(18));
    final outs = s.live ? ListenableBuilder(listenable: _outRep, builder: (_, _) => _readouts(p)) : _readouts(p);
    final f = s.formulaOf?.call(v) ?? s.formula;
    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        Stack(
          children: [
            DecoratedBox(
              decoration: flat,
              child: SizedBox(
                height: s.height,
                child: ClipRRect(
                  borderRadius: BorderRadius.circular(18),
                  child: RepaintBoundary(child: canvas),
                ),
              ),
            ),
            if (s.anim)
              Positioned(
                right: 8,
                top: 8,
                child: Row(
                  spacing: 8,
                  children: [
                    if (s.replay || s.step != null) _RoundIcon(kind: 2, onTap: replay, p: p, label: 'Replay'),
                    _RoundIcon(kind: playing ? 1 : 0, onTap: togglePlay, p: p, label: playing ? 'Pause' : 'Play'),
                  ],
                ),
              ),
          ],
        ),
        if (f.isNotEmpty)
          Padding(
            padding: const EdgeInsets.only(top: 10),
            child: DecoratedBox(
              decoration: BoxDecoration(color: p.blue.tile, borderRadius: BorderRadius.circular(12)),
              child: Padding(
                padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 7),
                child: Text(f, textAlign: TextAlign.center, style: ts(16, FontWeight.w900, p.blue.deep, height: 1.25)),
              ),
            ),
          ),
        const SizedBox(height: 8),
        outs,
        for (final o in s.opts)
          if (o.when?.call(v) ?? true) _chips(o, p),
        for (final x in s.sliders)
          if (x.when?.call(v) ?? true) ...[
            Padding(
              padding: const EdgeInsets.only(top: 8),
              child: Row(
                children: [
                  Expanded(child: Text(x.label, style: ts(15.5, FontWeight.w800, p.ink2))),
                  Text(x.show(v[x.name]!), style: ts(16, FontWeight.w900, p.blue.deep)),
                ],
              ),
            ),
            ClaySlider(
              value: ((v[x.name]! - x.min) / x.step).round(),
              max: ((x.max - x.min) / x.step).round(),
              onChanged: (i) => set(x.name, _snap(x.min + i * x.step, x.step)),
            ),
          ],
        if (s.tryThis.isNotEmpty || '${widget.p['try'] ?? ''}'.isNotEmpty)
          Padding(
            padding: const EdgeInsets.only(top: 12),
            child: DecoratedBox(
              decoration: BoxDecoration(color: p.sage.tile, borderRadius: BorderRadius.circular(14)),
              child: Padding(
                padding: const EdgeInsets.fromLTRB(12, 8, 12, 9),
                child: Text.rich(
                  TextSpan(
                    children: [
                      TextSpan(text: 'Try this  ', style: ts(15, FontWeight.w900, p.sage.deep)),
                      TextSpan(text: '${widget.p['try'] ?? s.tryThis}', style: ts(15.5, FontWeight.w600, p.ink, height: 1.35)),
                    ],
                  ),
                ),
              ),
            ),
          ),
      ],
    );
  }

  static double _snap(double x, double step) => step >= 1 ? x.roundToDouble() : double.parse(x.toStringAsFixed(6));

  Widget _readouts(Palette p) => Wrap(
    spacing: 8,
    runSpacing: 8,
    children: [
      for (final (a, b) in s.read(v, t))
        DecoratedBox(
          decoration: BoxDecoration(color: p.surface, borderRadius: BorderRadius.circular(12)),
          child: Padding(
            padding: const EdgeInsets.symmetric(horizontal: 11, vertical: 6),
            child: Text.rich(
              TextSpan(
                children: [
                  TextSpan(text: a.isEmpty ? '' : '$a  ', style: ts(14, FontWeight.w700, p.ink2)),
                  TextSpan(text: b, style: ts(15.5, FontWeight.w900, p.ink)),
                ],
              ),
            ),
          ),
        ),
    ],
  );

  Widget _chips(Opt o, Palette p) => Padding(
    padding: const EdgeInsets.only(top: 10),
    child: Wrap(
      spacing: 6,
      runSpacing: 6,
      crossAxisAlignment: WrapCrossAlignment.center,
      children: [
        if (o.label.isNotEmpty)
          Padding(
            padding: const EdgeInsets.only(right: 4),
            child: Text(o.label, style: ts(15, FontWeight.w800, p.ink2)),
          ),
        for (final (i, name) in o.options.indexed)
          GestureDetector(
            behavior: HitTestBehavior.opaque,
            onTap: () => set(o.name, i.toDouble()),
            child: DecoratedBox(
              decoration: BoxDecoration(
                color: v[o.name] == i ? p.blue.deep : p.surface2,
                borderRadius: BorderRadius.circular(20),
                border: Border.all(color: v[o.name] == i ? p.blue.deep : p.line, width: 1.5),
              ),
              child: Padding(
                padding: const EdgeInsets.symmetric(horizontal: 13, vertical: 8),
                child: Text(name, style: ts(14.5, FontWeight.w800, v[o.name] == i ? const Color(0xFFFFFFFF) : p.ink, height: 1.1)),
              ),
            ),
          ),
      ],
    ),
  );
}

class _LabPainter extends CustomPainter {
  _LabPainter(this.st, this.p, this.rev, Listenable rep) : super(repaint: rep);
  final LabViewState st;
  final Palette p;
  final int rev;
  @override
  void paint(Canvas canvas, Size size) => st.s.draw(canvas, size, st.v, st.t, p);
  @override
  bool shouldRepaint(_LabPainter o) => o.rev != rev || o.p != p || o.st != st;
}

/// play (0) / pause (1) / replay (2), drawn (no font glyphs)
class _RoundIcon extends StatelessWidget {
  const _RoundIcon({required this.kind, required this.onTap, required this.p, required this.label});
  final int kind;
  final VoidCallback onTap;
  final Palette p;
  final String label;
  @override
  Widget build(BuildContext context) => Semantics(
    button: true,
    label: label,
    child: GestureDetector(
      onTap: onTap,
      child: Container(
        width: 44,
        height: 44,
        decoration: BoxDecoration(
          color: kind == 0 ? p.peach.deep : p.surface,
          shape: BoxShape.circle,
          border: Border.all(color: p.peach.deep, width: 2),
        ),
        child: CustomPaint(painter: _IconPainter(kind, kind == 0 ? const Color(0xFFFFFFFF) : p.peach.deep)),
      ),
    ),
  );
}

class _IconPainter extends CustomPainter {
  _IconPainter(this.kind, this.c);
  final int kind;
  final Color c;
  @override
  void paint(Canvas cv, Size s) {
    final o = s.center(Offset.zero);
    if (kind == 0) {
      cv.drawPath(Path()..addPolygon([o + const Offset(-6, -9), o + const Offset(10, 0), o + const Offset(-6, 9)], true), fi(c));
    } else if (kind == 1) {
      cv.drawRect(Rect.fromCenter(center: o + const Offset(-5, 0), width: 5, height: 17), fi(c));
      cv.drawRect(Rect.fromCenter(center: o + const Offset(5, 0), width: 5, height: 17), fi(c));
    } else {
      cv.drawArc(Rect.fromCircle(center: o, radius: 9), -1.2, 5, false, sk(c, 3));
      final a = o + Offset(math.cos(-1.2) * 9, math.sin(-1.2) * 9);
      cv.drawPath(Path()..addPolygon([a + const Offset(-6, -4), a + const Offset(3, -5), a + const Offset(0, 4)], true), fi(c));
    }
  }

  @override
  bool shouldRepaint(_IconPainter o) => o.kind != kind || o.c != c;
}

// ---------------------------------------------------------------- cached drawing helpers
final _sk = <int, Paint>{}, _fi = <int, Paint>{};

/// cached stroke paint (do not mutate the result)
Paint sk(Color c, [double w = 2]) {
  final k = c.toARGB32() * 4096 + (w * 16).round();
  final hit = _sk[k];
  if (hit != null) return hit;
  if (_sk.length > 800) _sk.clear();
  return _sk[k] = Paint()
    ..color = c
    ..style = PaintingStyle.stroke
    ..strokeWidth = w
    ..strokeCap = StrokeCap.round
    ..strokeJoin = StrokeJoin.round;
}

/// cached fill paint (do not mutate the result)
Paint fi(Color c) {
  final k = c.toARGB32();
  final hit = _fi[k];
  if (hit != null) return hit;
  if (_fi.length > 800) _fi.clear();
  return _fi[k] = Paint()..color = c;
}

final _tps = <String, TextPainter>{};

/// cached text: [ax] 0 = left, .5 = centre, 1 = right of [o]; [ay] likewise vertically (0 = top)
void tx(Canvas c, String s, Offset o, Color col, {double size = 13, double ax = 0, double ay = 0, FontWeight w = FontWeight.w800}) {
  if (s.isEmpty) return;
  final key = '$s\u0001$size\u0001${col.toARGB32()}\u0001${w.value}';
  var tp = _tps[key];
  if (tp == null) {
    if (_tps.length > 500) {
      for (final x in _tps.values) {
        x.dispose();
      }
      _tps.clear();
    }
    tp = _tps[key] = TextPainter(
      text: TextSpan(text: s, style: ts(size, w, col, height: 1.1)),
      textDirection: TextDirection.ltr,
    )..layout();
  }
  tp.paint(c, o - Offset(tp.width * ax, tp.height * ay));
}

/// arrow with a filled head (cached paints)
void arw(Canvas c, Offset a, Offset b, Color col, [double w = 2.5, double head = 10]) {
  final d = b - a, len = d.distance;
  if (len < .5) return;
  final u = d / len, n = Offset(-u.dy, u.dx), h = math.min(head, len * .5);
  c.drawLine(a, b - u * (h * .6), sk(col, w));
  c.drawPath(Path()..addPolygon([b, b - u * h + n * (h * .5), b - u * h - n * (h * .5)], true), fi(col));
}

/// dashed line (cached paints)
void dsh(Canvas c, Offset a, Offset b, Color col, [double w = 1.5, double dash = 6]) {
  final d = b - a, len = d.distance;
  if (len < 1) return;
  final n = (len / dash).ceil(), u = d / len, pt = sk(col, w);
  for (var i = 0; i < n; i += 2) {
    c.drawLine(a + u * (i * dash), a + u * math.min(len, (i + 1) * dash), pt);
  }
}

/// small arrow head in the middle of a segment (for field lines / rays)
void midHead(Canvas c, Offset a, Offset b, Color col, [double h = 7]) {
  final d = b - a, len = d.distance;
  if (len < 1) return;
  final u = d / len, n = Offset(-u.dy, u.dx), m = a + d * .5 + u * (h * .5);
  c.drawPath(Path()..addPolygon([m, m - u * h + n * (h * .55), m - u * h - n * (h * .55)], true), fi(col));
}

/// angle arc at [o] from direction angle a0 to a1 (radians, screen coordinates) with a label
void angArc(Canvas c, Offset o, double r, double a0, double a1, Color col, [String label = '']) {
  var sw = a1 - a0;
  while (sw > math.pi) {
    sw -= 2 * math.pi;
  }
  while (sw < -math.pi) {
    sw += 2 * math.pi;
  }
  c.drawArc(Rect.fromCircle(center: o, radius: r), a0, sw, false, sk(col, 1.6));
  if (label.isNotEmpty) {
    final am = a0 + sw / 2;
    tx(c, label, o + Offset(math.cos(am), math.sin(am)) * (r + 12), col, size: 12, ax: .5, ay: .5);
  }
}

// ---------------------------------------------------------------- numbers
const deg = math.pi / 180;
String numStr(double v, double step) => step >= 1 ? v.round().toString() : v.toStringAsFixed(step < .01 ? 3 : (step < .1 ? 2 : 1));
const _sup = {'-': '⁻', '0': '⁰', '1': '¹', '2': '²', '3': '³', '4': '⁴', '5': '⁵', '6': '⁶', '7': '⁷', '8': '⁸', '9': '⁹'};

/// 3 significant figures, scientific (a × 10ⁿ) outside 0.01 … 99 999
String sci(double v, [int sig = 3]) {
  if (v == 0 || !v.isFinite) return v == 0 ? '0' : '—';
  final e = (math.log(v.abs()) / math.ln10).floor();
  if (e >= 5 || e <= -3) {
    final m = v / math.pow(10, e);
    return '${m.toStringAsFixed(sig - 1)} × 10${'$e'.split('').map((ch) => _sup[ch] ?? ch).join()}';
  }
  return v.toStringAsFixed(math.max(0, sig - 1 - e));
}

String fx(double v, [int d = 1]) => (v.abs() < .5 * math.pow(10, -d) ? 0.0 : v).toStringAsFixed(d);

/// approximate colour of light of wavelength [nm] (380–750); outside: UV violet / IR dark red
Color waveColor(double nm, [double alpha = 1]) {
  double r = 0, g = 0, b = 0;
  final l = nm.clamp(380.0, 750.0);
  if (l < 440) {
    r = -(l - 440) / 60;
    b = 1;
  } else if (l < 490) {
    g = (l - 440) / 50;
    b = 1;
  } else if (l < 510) {
    g = 1;
    b = -(l - 510) / 20;
  } else if (l < 580) {
    r = (l - 510) / 70;
    g = 1;
  } else if (l < 645) {
    r = 1;
    g = -(l - 645) / 65;
  } else {
    r = 1;
  }
  final f = l < 420 ? .35 + .65 * (l - 380) / 40 : (l > 700 ? .35 + .65 * (750 - l) / 50 : 1.0);
  int ch(double x) => (255 * math.pow(x * f, .8)).round().clamp(0, 255);
  return Color.fromARGB((255 * alpha).round(), ch(r), ch(g), ch(b));
}

// ---------------------------------------------------------------- geometry
double cross2(Offset a, Offset b) => a.dx * b.dy - a.dy * b.dx;
double dot2(Offset a, Offset b) => a.dx * b.dx + a.dy * b.dy;

/// ray o + t·d against segment a–b: t (>eps) or null
double? raySeg(Offset o, Offset d, Offset a, Offset b) {
  final e = b - a, den = cross2(d, e);
  if (den.abs() < 1e-9) return null;
  final w = a - o, t = cross2(w, e) / den, u = cross2(w, d) / den;
  return (t > 1e-6 && u >= -1e-9 && u <= 1 + 1e-9) ? t : null;
}

Offset reflectDir(Offset d, Offset n) => d - n * (2 * dot2(d, n));

/// trace a ray through a convex polygon of index [n] in a medium [n0]: points visited and the final direction.
/// Snell at every face, total internal reflection when sin > 1 (and a [weak] list of the partial reflections).
({List<Offset> pts, Offset dir, bool tir}) tracePoly(Offset o, Offset d, List<Offset> poly, double n, {double n0 = 1, int maxHits = 8}) {
  final pts = [o];
  var inside = false, tir = false;
  d = d / d.distance;
  for (var hit = 0; hit < maxHits; hit++) {
    double? best;
    var bi = -1;
    for (var i = 0; i < poly.length; i++) {
      final t = raySeg(o, d, poly[i], poly[(i + 1) % poly.length]);
      if (t != null && (best == null || t < best)) {
        best = t;
        bi = i;
      }
    }
    if (best == null) break;
    o = o + d * best;
    pts.add(o);
    final e = poly[(bi + 1) % poly.length] - poly[bi];
    var nn = Offset(e.dy, -e.dx) / e.distance; // one of the normals
    if (dot2(nn, d) > 0) nn = -nn; // nn faces against the ray
    final n1 = inside ? n : n0, n2 = inside ? n0 : n;
    final ci = -dot2(nn, d), r = n1 / n2, k = 1 - r * r * (1 - ci * ci);
    if (k < 0) {
      d = reflectDir(d, nn);
      tir = true;
    } else {
      d = d * r + nn * (r * ci - math.sqrt(k));
      inside = !inside;
    }
    d = d / d.distance;
    o = o + d * 1e-4;
    if (!inside && hit > 0) break;
  }
  return (pts: pts, dir: d, tir: tir);
}

/// polyline through [pts] then on along [dir] by [far]
void rayPath(Canvas c, List<Offset> pts, Offset dir, Color col, {double w = 2.5, double far = 1500, bool heads = true}) {
  final path = Path()..moveTo(pts.first.dx, pts.first.dy);
  for (final q in pts.skip(1)) {
    path.lineTo(q.dx, q.dy);
  }
  final end = pts.last + dir * far;
  path.lineTo(end.dx, end.dy);
  c.drawPath(path, sk(col, w));
  if (heads) {
    for (var i = 0; i + 1 < pts.length; i++) {
      midHead(c, pts[i], pts[i + 1], col);
    }
    midHead(c, pts.last, pts.last + dir * 80, col);
  }
}

/// point charges (or magnetic poles) field-line tracer; returns polylines in canvas coordinates
List<List<Offset>> traceField(List<(Offset, double)> qs, Rect bounds, {int perUnit = 4, double stepLen = 4, int maxSteps = 500}) {
  final lines = <List<Offset>>[];
  Offset field(Offset x) {
    var e = Offset.zero;
    for (final (o, q) in qs) {
      final d = x - o, r2 = d.distanceSquared + 1;
      e += d * (q / (r2 * math.sqrt(r2)));
    }
    return e;
  }

  final total = qs.fold(0.0, (a, b) => a + b.$2.abs());
  for (final (o, q) in qs) {
    if (q == 0) continue;
    // start from positives; from negatives only when the positives do not exist / cannot cover them
    final fromNeg = q < 0;
    final hasPos = qs.any((x) => x.$2 > 0);
    if (fromNeg && hasPos && qs.where((x) => x.$2 > 0).fold(0.0, (a, b) => a + b.$2) >= -q) continue;
    final n = math.max(4, (q.abs() * perUnit).round());
    for (var i = 0; i < n; i++) {
      final a = 2 * math.pi * (i + .5) / n;
      var x = o + Offset(math.cos(a), math.sin(a)) * 10;
      final line = [x];
      final sgn = fromNeg ? -1.0 : 1.0;
      for (var k = 0; k < maxSteps; k++) {
        var e = field(x);
        final m = e.distance;
        if (m < 1e-12) break;
        final mid = x + e / m * (stepLen * .5 * sgn);
        e = field(mid);
        final m2 = e.distance;
        if (m2 < 1e-12) break;
        x = x + e / m2 * (stepLen * sgn);
        line.add(x);
        if (!bounds.inflate(40).contains(x)) break;
        var end = false;
        for (final (o2, q2) in qs) {
          if (o2 != o && (x - o2).distance < 8 && q2 * q < 0) end = true;
        }
        if (end) break;
      }
      lines.add(line);
    }
  }
  if (total == 0) return const [];
  return lines;
}

void polyline(Canvas c, List<Offset> pts, Paint pt) {
  if (pts.length < 2) return;
  final path = Path()..moveTo(pts.first.dx, pts.first.dy);
  for (final q in pts.skip(1)) {
    path.lineTo(q.dx, q.dy);
  }
  c.drawPath(path, pt);
}

/// a coloured wave-field image drawn with one drawVertices call: a grid of [nx]×[ny] cells whose value is
/// Re(Z·e^{-iωt}) for a complex amplitude Z per vertex (precomputed when the parameters change)
class WaveField {
  WaveField(this.nx, this.ny);
  final int nx, ny;
  Size? _sz;
  Float32List? _pos;
  Uint16List? _idx;
  Float32List zr = Float32List(0), zi = Float32List(0);
  late Int32List _col;
  String _sig = '';

  /// (re)build the amplitudes with [amp] (x, y in canvas px) -> (re, im) when [sig] changes
  void prepare(Size s, String sig, (double, double) Function(double x, double y) amp) {
    if (_sz == s && sig == _sig) return;
    _sig = sig;
    final n = (nx + 1) * (ny + 1);
    if (_sz != s) {
      _sz = s;
      _pos = Float32List(n * 2);
      for (var j = 0; j <= ny; j++) {
        for (var i = 0; i <= nx; i++) {
          final k = j * (nx + 1) + i;
          _pos![k * 2] = s.width * i / nx;
          _pos![k * 2 + 1] = s.height * j / ny;
        }
      }
      _idx = Uint16List(nx * ny * 6);
      var m = 0;
      for (var j = 0; j < ny; j++) {
        for (var i = 0; i < nx; i++) {
          final a = j * (nx + 1) + i, b = a + 1, c = a + nx + 1, d = c + 1;
          _idx!.setAll(m, [a, b, c, b, d, c]);
          m += 6;
        }
      }
      _col = Int32List(n);
    }
    zr = Float32List(n);
    zi = Float32List(n);
    for (var k = 0; k < n; k++) {
      final (re, im) = amp(_pos![k * 2], _pos![k * 2 + 1]);
      zr[k] = re;
      zi[k] = im;
    }
  }

  /// value -> colour: [lo] at -1, [mid] at 0, [hi] at +1
  void draw(Canvas c, double wt, Color lo, Color mid, Color hi, {double gain = 1}) {
    if (_pos == null) return;
    final cs = math.cos(wt), sn = math.sin(wt);
    final l = lo.toARGB32(), m0 = mid.toARGB32(), h = hi.toARGB32();
    for (var k = 0; k < zr.length; k++) {
      final x = ((zr[k] * cs + zi[k] * sn) * gain).clamp(-1.0, 1.0);
      _col[k] = x >= 0 ? _lerp(m0, h, x) : _lerp(m0, l, -x);
    }
    final vx = ui.Vertices.raw(ui.VertexMode.triangles, _pos!, colors: _col, indices: _idx);
    c.drawVertices(vx, BlendMode.dst, fi(const Color(0xFF000000)));
    vx.dispose();
  }

  static int _lerp(int a, int b, double t) {
    int ch(int s) => (((a >> s) & 255) + ((((b >> s) & 255) - ((a >> s) & 255)) * t)).round();
    return (255 << 24) | (ch(16) << 16) | (ch(8) << 8) | ch(0);
  }
}

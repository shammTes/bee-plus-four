// Physics (+ maths graph) sims.
import 'dart:math' as math;

import 'package:flutter/widgets.dart';

import '../notes/jr/theme/tokens.dart';
import 'sims.dart';

const _g = 9.8;

final Map<String, SimSpec Function(Map<String, dynamic>)> physSims = {
  'projectile': (_) => SimSpec(
    animated: true,
    params: const [
      Prm('a', 'Launch angle', 10, 80, 45, step: 5, unit: '°'),
      Prm('v', 'Launch speed', 5, 40, 20, unit: 'm/s'),
    ],
    out: (v) {
      final a = v['a']! * math.pi / 180, u = v['v']!;
      return [
        ('Range', '${f1(u * u * math.sin(2 * a) / _g)} m'),
        ('Max height', '${f1(math.pow(u * math.sin(a), 2) / (2 * _g))} m'),
        ('Time of flight', '${f2(2 * u * math.sin(a) / _g)} s'),
      ];
    },
    paint: (c, s, v, t, p) {
      final pl = Plot(c, s, 0, 180, 0, 80, p, xl: 'x (m)', yl: 'y (m)', xt: 6, yt: 4);
      double y(double x, double a, double u) => x * math.tan(a) - _g * x * x / (2 * u * u * math.pow(math.cos(a), 2));
      final u = v['v']!, a = v['a']! * math.pi / 180, r = u * u * math.sin(2 * a) / _g;
      pl.curve((x) => y(x, math.pi / 4, u), p.line, w: 2, to: u * u / _g);
      pl.curve((x) => y(x, a, u), p.peach.deep, to: r);
      final T = 2 * u * math.sin(a) / _g, tt = (t % (T + .6)).clamp(0, T), bx = u * math.cos(a) * tt, by = u * math.sin(a) * tt - _g * tt * tt / 2;
      pl.dot(bx, math.max(0, by), p.blue.deep);
      arrow(c, pl.at(0, 0), pl.at(0, 0) + Offset(math.cos(a), -math.sin(a)) * 40, p.sage.deep);
      txt(c, 'grey: 45° at the same speed', pl.r.topRight + const Offset(-4, 2), p.ink2, size: 11, right: true);
    },
  ),
  'pendulum': (_) => SimSpec(
    animated: true,
    params: const [
      Prm('L', 'String length', .2, 2, 1, step: .1, unit: 'm'),
      Prm('A', 'Swing (amplitude)', 5, 30, 15, unit: '°'),
      Prm('g', 'Gravity g', 1.6, 24.8, 9.8, step: .1, unit: 'm/s²'),
    ],
    out: (v) {
      final T = 2 * math.pi * math.sqrt(v['L']! / v['g']!);
      return [
        ('Period T = 2π√(L/g)', '${f2(T)} s'),
        ('Frequency', '${f2(1 / T)} Hz'),
        ('', v['g']! < 2 ? 'like the Moon' : (v['g']! > 20 ? 'like Jupiter' : (v['g']! > 9 && v['g']! < 10.5 ? 'like Earth' : ''))),
      ];
    },
    paint: (c, s, v, t, p) {
      final T = 2 * math.pi * math.sqrt(v['L']! / v['g']!), th = v['A']! * math.pi / 180 * math.cos(2 * math.pi * t / T);
      final o = Offset(s.width / 2, 18), len = (s.height - 50) * v['L']! / 2, b = o + Offset(math.sin(th), math.cos(th)) * len;
      c.drawLine(Offset(s.width / 2 - 60, 18), Offset(s.width / 2 + 60, 18), st(p.ink, 5));
      dashed(c, o, o + Offset(0, len + 20), st(p.line, 1.5));
      c.drawLine(o, b, st(p.ink2, 2));
      c.drawCircle(b, 16, fl(p.peach.deep));
      txt(c, 'L = ${f1(v['L']!)} m', Offset(14, s.height - 24), p.ink2);
    },
  ),
  'wave': (_) => SimSpec(
    animated: true,
    params: const [
      Prm('A', 'Amplitude', .2, 1, .6, step: .1, unit: 'm'),
      Prm('l', 'Wavelength λ', .5, 4, 2, step: .5, unit: 'm'),
      Prm('f', 'Frequency f', .2, 3, 1, step: .2, unit: 'Hz'),
    ],
    out: (v) => [('Speed v = fλ', '${f2(v['f']! * v['l']!)} m/s'), ('Period T = 1/f', '${f2(1 / v['f']!)} s')],
    paint: (c, s, v, t, p) {
      final pl = Plot(c, s, 0, 8, -1.2, 1.2, p, xl: 'distance (m)', yl: 'displacement (m)', xt: 8, yt: 4);
      double y(double x) => v['A']! * math.sin(2 * math.pi * (x / v['l']! - v['f']! * t));
      pl.curve(y, p.blue.deep, n: 240);
      pl.dot(2, y(2), p.peach.deep);
      final a = pl.at(.25 * v['l']!, 1.05), b = pl.at(1.25 * v['l']!, 1.05);
      if (1.25 * v['l']! <= 8) {
        arrow(c, a, b, p.sage.deep, 2);
        txt(c, 'λ', Offset((a.dx + b.dx) / 2, a.dy - 14), p.sage.deep, center: true);
      }
    },
  ),
  'ohm': (_) => SimSpec(
    animated: true,
    params: const [
      Prm('V', 'Battery voltage', 1.5, 12, 6, step: 1.5, unit: 'V'),
      Prm('R', 'Resistance', 2, 100, 20, step: 2, unit: 'Ω'),
    ],
    out: (v) {
      final i = v['V']! / v['R']!;
      return [('Current I = V/R', '${f2(i)} A'), ('Power P = VI', '${f2(v['V']! * i)} W')];
    },
    paint: (c, s, v, t, p) {
      final r = Rect.fromLTRB(50, 40, s.width - 50, s.height - 40), i = v['V']! / v['R']!, pw = v['V']! * i;
      final wire = st(p.ink, 3);
      c.drawRRect(RRect.fromRectAndRadius(r, const Radius.circular(10)), wire);
      // battery (left), resistor (top), bulb (right), ammeter (bottom)
      final bt = Offset(r.left, r.center.dy);
      c.drawRect(Rect.fromCenter(center: bt, width: 30, height: 30), fl(p.surface2));
      c.drawLine(bt + const Offset(-14, -6), bt + const Offset(14, -6), st(p.ink, 4));
      c.drawLine(bt + const Offset(-8, 6), bt + const Offset(8, 6), st(p.ink, 4));
      txt(c, '${f1(v['V']!)} V', bt + const Offset(20, -8), p.ink);
      final zz = Path()..moveTo(r.center.dx - 50, r.top);
      for (var k = 0; k < 8; k++) {
        zz.lineTo(r.center.dx - 50 + 12.5 * (k + .5), r.top + (k.isEven ? -10 : 10));
      }
      zz.lineTo(r.center.dx + 50, r.top);
      c.drawRect(Rect.fromLTRB(r.center.dx - 52, r.top - 12, r.center.dx + 52, r.top + 12), fl(p.surface2));
      c.drawPath(zz, st(p.peach.deep, 3));
      txt(c, '${v['R']!.toInt()} Ω', Offset(r.center.dx, r.top - 26), p.ink, center: true);
      final bl = Offset(r.right, r.center.dy), glow = (pw / 8).clamp(0.0, 1.0);
      c.drawCircle(bl, 34 + 20 * glow, fl(Color.fromARGB((120 * glow).toInt(), 255, 210, 60)));
      c.drawCircle(bl, 18, fl(Color.lerp(p.surface, const Color(0xFFFFD84A), glow)!));
      c.drawCircle(bl, 18, st(p.ink, 2));
      final am = Offset(r.center.dx, r.bottom);
      c.drawCircle(am, 16, fl(p.surface));
      c.drawCircle(am, 16, st(p.ink, 2));
      txt(c, 'A', am, p.ink, center: true);
      txt(c, '${f2(i)} A', am + const Offset(24, 6), p.blue.deep);
      // moving charges (conventional current: + terminal round to -)
      final per = 2 * (r.width + r.height), n = 14;
      for (var k = 0; k < n; k++) {
        var d = (k / n * per + t * 90 * i) % per;
        Offset q;
        if (d < r.width) {
          q = Offset(r.left + d, r.top);
        } else if ((d -= r.width) < r.height) {
          q = Offset(r.right, r.top + d);
        } else if ((d -= r.height) < r.width) {
          q = Offset(r.right - d, r.bottom);
        } else {
          q = Offset(r.left, r.bottom - (d - r.width));
        }
        c.drawCircle(q, 4, fl(p.blue.deep));
      }
    },
  ),
  'lens': (m) => _optics(false),
  'mirror': (m) => _optics(true),
  'buoyancy': (_) => SimSpec(
    params: const [
      Prm('ro', 'Object density', 200, 2000, 600, step: 50, unit: 'kg/m³'),
      Prm('rl', 'Liquid density', 700, 1400, 1000, step: 50, unit: 'kg/m³'),
    ],
    out: (v) {
      final f = v['ro']! / v['rl']!;
      return [('', f < 1 ? 'Floats' : (f == 1 ? 'Hovers' : 'Sinks')), ('Fraction under the surface', f < 1 ? '${(f * 100).round()} %' : '100 %')];
    },
    paint: (c, s, v, t, p) {
      final tank = Rect.fromLTRB(s.width * .2, 30, s.width * .8, s.height - 12), wl = tank.top + 50;
      c.drawRect(Rect.fromLTRB(tank.left, wl, tank.right, tank.bottom), fl(Color.lerp(const Color(0x664A90D9), const Color(0x99365E9E), (v['rl']! - 700) / 700)!));
      c.drawPath(
        Path()
          ..moveTo(tank.left, tank.top)
          ..lineTo(tank.left, tank.bottom)
          ..lineTo(tank.right, tank.bottom)
          ..lineTo(tank.right, tank.top),
        st(p.ink, 3),
      );
      final f = v['ro']! / v['rl']!, hb = 70.0;
      final top = f < 1 ? wl - hb * (1 - f) : tank.bottom - hb - 2;
      final b = Rect.fromLTWH(tank.center.dx - 40, top, 80, hb);
      c.drawRect(b, fl(Color.lerp(const Color(0xFFE8C07A), const Color(0xFF6E5A48), (v['ro']! - 200) / 1800)!));
      arrow(c, b.center, b.center + const Offset(0, 48), p.peach.deep, 3);
      txt(c, 'weight', b.center + const Offset(8, 36), p.peach.deep, size: 12);
      arrow(c, b.bottomCenter + const Offset(-24, 0), b.bottomCenter + Offset(-24, -48 * math.min(1, f < 1 ? 1 : 1 / f)), p.sage.deep, 3);
      txt(c, 'upthrust', b.bottomLeft + const Offset(-64, -30), p.sage.deep, size: 12);
    },
  ),
  'coulomb': (_) => SimSpec(
    params: const [
      Prm('q1', 'Charge q₁', -5, 5, 3, unit: 'µC'),
      Prm('q2', 'Charge q₂', -5, 5, -2, unit: 'µC'),
      Prm('r', 'Separation r', .1, 1, .3, step: .05, unit: 'm'),
    ],
    out: (v) {
      final F = 9e9 * v['q1']! * 1e-6 * v['q2']! * 1e-6 / (v['r']! * v['r']!);
      return [('F = kq₁q₂/r²', '${sig3(F.abs())} N'), ('', F == 0 ? 'no force' : (F < 0 ? 'attract' : 'repel'))];
    },
    paint: (c, s, v, t, p) {
      final cx = s.width / 2, cy = s.height / 2, d = v['r']! * (s.width - 120) / 2, a = Offset(cx - d, cy), b = Offset(cx + d, cy);
      final F = 9e9 * v['q1']! * 1e-6 * v['q2']! * 1e-6 / (v['r']! * v['r']!), len = F == 0 ? 0.0 : (18 + 14 * math.log(1 + F.abs())).clamp(0, 90).toDouble();
      for (final (o, q, dir) in [(a, v['q1']!, -1.0), (b, v['q2']!, 1.0)]) {
        final sgn = F > 0 ? dir : -dir;
        if (len > 0) arrow(c, o, o + Offset(sgn * (len + 24), 0), p.ink, 3);
        c.drawCircle(o, 22, fl(q > 0 ? p.peach.deep : (q < 0 ? p.blue.deep : p.line)));
        txt(c, q > 0 ? '+' : (q < 0 ? '−' : '0'), o, const Color(0xFFFFFFFF), size: 22, center: true);
      }
      txt(c, 'r = ${f2(v['r']!)} m', Offset(cx, cy + 40), p.ink2, center: true);
    },
  ),
  'graph': (m) {
    final fn = '${m['fn'] ?? 'quad'}';
    if (fn == 'line') {
      return SimSpec(
        params: const [Prm('m', 'Gradient m', -4, 4, 1, step: .5), Prm('c', 'Intercept c', -6, 6, 2, step: .5)],
        out: (v) => [
          ('y = mx + c', 'y = ${f1(v['m']!)}x ${v['c']! < 0 ? '−' : '+'} ${f1(v['c']!.abs())}'),
          ('x-intercept', v['m'] == 0 ? 'none' : f2(-v['c']! / v['m']!)),
        ],
        paint: (c, s, v, t, p) => _grid(c, s, p, (x) => v['m']! * x + v['c']!),
      );
    }
    if (fn == 'exp') {
      return SimSpec(
        params: const [Prm('a', 'a', .5, 3, 1, step: .5), Prm('b', 'Base b', .5, 3, 2, step: .1)],
        out: (v) => [('y = a·bˣ', v['b']! > 1 ? 'growth' : (v['b']! < 1 ? 'decay' : 'constant')), ('y-intercept', f1(v['a']!))],
        paint: (c, s, v, t, p) => _grid(c, s, p, (x) => v['a']! * math.pow(v['b']!, x).toDouble()),
      );
    }
    if (fn == 'sqrt') {
      return SimSpec(
        params: const [Prm('a', 'a', -3, 3, 1, step: .5), Prm('h', 'h (shift right)', -5, 5, 0), Prm('k', 'k (shift up)', -5, 5, 0)],
        out: (v) => [('y = a√(x − h) + k', 'domain x ≥ ${v['h']!.toInt()}'), ('Range', v['a']! >= 0 ? 'y ≥ ${v['k']!.toInt()}' : 'y ≤ ${v['k']!.toInt()}')],
        paint: (c, s, v, t, p) => _grid(c, s, p, (x) => x < v['h']! ? double.nan : v['a']! * math.sqrt(x - v['h']!) + v['k']!),
      );
    }
    if (fn == 'rational') {
      return SimSpec(
        params: const [Prm('a', 'a', -4, 4, 2, step: .5), Prm('h', 'Vertical asymptote x = h', -4, 4, 1), Prm('k', 'Horizontal asymptote y = k', -4, 4, 0)],
        out: (v) => [('y = a/(x − h) + k', 'asymptotes x = ${v['h']!.toInt()}, y = ${v['k']!.toInt()}')],
        paint: (c, s, v, t, p) => _grid(c, s, p, (x) => (x - v['h']!).abs() < .02 ? double.nan : v['a']! / (x - v['h']!) + v['k']!),
      );
    }
    if (fn == 'log') {
      return SimSpec(
        params: const [Prm('b', 'Base b', 1.5, 10, 2, step: .5)],
        out: (v) => [('y = log_b x', 'passes through (1, 0) and (b, 1)'), ('Inverse of', 'y = ${f1(v['b']!)}ˣ')],
        paint: (c, s, v, t, p) => _grid(c, s, p, (x) => x <= 0 ? double.nan : math.log(x) / math.log(v['b']!)),
      );
    }
    if (fn == 'sin') {
      return SimSpec(
        params: const [Prm('a', 'Amplitude a', .5, 4, 2, step: .5), Prm('b', 'b (cycles)', .5, 3, 1, step: .5)],
        out: (v) => [('y = a sin(bx)', 'period ${f2(2 * math.pi / v['b']!)}'), ('max', f1(v['a']!))],
        paint: (c, s, v, t, p) => _grid(c, s, p, (x) => v['a']! * math.sin(v['b']! * x)),
      );
    }
    return SimSpec(
      params: const [Prm('a', 'a', -3, 3, 1, step: .5), Prm('b', 'b', -6, 6, 0, step: .5), Prm('c', 'c', -6, 6, -4, step: .5)],
      out: (v) {
        final a = v['a']!, b = v['b']!, cc = v['c']!, d = b * b - 4 * a * cc;
        if (a == 0) return [('', 'a = 0: a straight line')];
        final xv = -b / (2 * a);
        return [
          ('Vertex', '(${f2(xv)}, ${f2(a * xv * xv + b * xv + cc)})'),
          ('Discriminant b²−4ac', f2(d)),
          ('Roots', d < 0 ? 'none (real)' : (d == 0 ? f2(xv) : '${f2((-b - math.sqrt(d)) / (2 * a))}, ${f2((-b + math.sqrt(d)) / (2 * a))}')),
        ];
      },
      paint: (c, s, v, t, p) => _grid(c, s, p, (x) => v['a']! * x * x + v['b']! * x + v['c']!),
    );
  },
};

void _grid(Canvas c, Size s, Palette p, double Function(double) f) {
  final r = Rect.fromLTRB(10, 10, s.width - 10, s.height - 10), sc = math.min(r.width / 16, r.height / 12), o = r.center;
  for (var i = -8; i <= 8; i++) {
    c.drawLine(o + Offset(i * sc, -6 * sc), o + Offset(i * sc, 6 * sc), st(p.line, .7));
  }
  for (var j = -6; j <= 6; j++) {
    c.drawLine(o + Offset(-8 * sc, j * sc), o + Offset(8 * sc, j * sc), st(p.line, .7));
  }
  arrow(c, o + Offset(-8 * sc, 0), o + Offset(8 * sc, 0), p.ink2, 1.5);
  arrow(c, o + Offset(0, 6 * sc), o + Offset(0, -6 * sc), p.ink2, 1.5);
  txt(c, 'x', o + Offset(8 * sc - 12, 4), p.ink2);
  txt(c, 'y', o + Offset(6, -6 * sc), p.ink2);
  final path = Path();
  var started = false;
  for (var i = 0; i <= 320; i++) {
    final x = -8 + 16 * i / 320, y = f(x);
    if (y.isNaN || y.abs() > 6.5) {
      started = false;
      continue;
    }
    final q = o + Offset(x * sc, -y * sc);
    started ? path.lineTo(q.dx, q.dy) : path.moveTo(q.dx, q.dy);
    started = true;
  }
  c.drawPath(path, st(p.peach.deep, 3.5));
}

/// thin converging lens / concave mirror: 1/f = 1/u + 1/v (real-is-positive)
SimSpec _optics(bool mirror) => SimSpec(
  height: 280,
  params: const [
    Prm('f', 'Focal length f', 5, 20, 10, unit: 'cm'),
    Prm('u', 'Object distance u', 4, 60, 30, unit: 'cm'),
  ],
  out: (v) {
    final f = v['f']!, u = v['u']!;
    if ((u - f).abs() < 1e-6) return [('', 'Object at F: image at infinity')];
    final im = 1 / (1 / f - 1 / u), mag = -im / u;
    return [
      ('Image distance v', '${f1(im.abs())} cm ${im > 0 ? (mirror ? 'in front' : 'behind lens') : (mirror ? 'behind mirror' : 'same side')}'),
      ('Magnification', '${f2(mag.abs())}×'),
      ('', '${im > 0 ? 'real, inverted' : 'virtual, upright'}, ${mag.abs() > 1.001 ? 'magnified' : (mag.abs() < .999 ? 'diminished' : 'same size')}'),
    ];
  },
  paint: (c, s, v, t, p) {
    final f = v['f']!, u = v['u']!, sc = (s.width - 20) / 140, ax = s.height / 2, x0 = s.width / 2;
    Offset at(double x, double y) => Offset(x0 + x * sc, ax - y * sc * 1.3);
    c.drawLine(Offset(0, ax), Offset(s.width, ax), st(p.ink2, 1));
    if (mirror) {
      c.drawArc(Rect.fromCircle(center: at(-2 * f * 0 + 40, 0), radius: 40 * sc), math.pi - .6, 1.2, false, st(p.blue.deep, 4));
    } else {
      c.drawOval(Rect.fromCenter(center: at(0, 0), width: 14, height: s.height - 30), fl(const Color(0x664A90D9)));
      c.drawOval(Rect.fromCenter(center: at(0, 0), width: 14, height: s.height - 30), st(p.blue.deep, 2));
    }
    for (final k in mirror ? [1.0, 2.0] : [-1.0, 1.0, -2.0, 2.0]) {
      final x = mirror ? -k * f : k * f;
      c.drawCircle(at(x, 0), 4, fl(p.ink));
      txt(c, k.abs() == 1 ? 'F' : (mirror ? 'C' : '2F'), at(x, 0) + const Offset(0, 12), p.ink, center: true, size: 12);
    }
    const h = 6.0;
    final ob = at(-u, 0), ot = at(-u, h);
    arrow(c, ob, ot, p.sage.deep, 4);
    if ((u - f).abs() < 1e-6) return;
    final im = 1 / (1 / f - 1 / u), hi = -im / u * h;
    // image x: lens -> +im (right side real); mirror -> -im (in front = left)
    final ix = mirror ? -im : im;
    final ray = st(p.peach.deep, 2);
    // ray 1: parallel then through (or from) F
    final hit1 = at(0, h);
    c.drawLine(ot, hit1, ray);
    final fx = mirror ? -f : f;
    final dir1 = (at(fx, 0) - hit1);
    final end1 = hit1 + dir1 / dir1.distance * 900 * (mirror ? 1 : 1);
    c.drawLine(hit1, end1, ray);
    // ray 2: through the centre (lens) / to the pole (mirror)
    final pole = at(0, 0), d2 = pole - ot;
    final end2 = mirror ? pole + Offset(-d2.dx, d2.dy) / d2.distance * 900 : pole + d2 / d2.distance * 900;
    c.drawLine(ot, pole, ray);
    c.drawLine(pole, end2, ray);
    final virt = im < 0;
    if (virt) {
      final dv = st(p.peach.deep, 1.3);
      dashed(c, hit1, hit1 - dir1 / dir1.distance * 900, dv);
      dashed(c, pole, mirror ? pole - (end2 - pole) : pole - d2 / d2.distance * 900, dv);
    }
    if (ix.abs() < 75 && hi.abs() < 30) {
      final ib = at(ix, 0), itp = at(ix, hi);
      virt ? dashed(c, ib, itp, st(p.lilac.deep, 4)) : arrow(c, ib, itp, p.lilac.deep, 4);
      txt(c, 'image', itp + const Offset(6, -4), p.lilac.deep, size: 12);
    }
    txt(c, 'object', ot + const Offset(-20, -18), p.sage.deep, size: 12);
  },
);

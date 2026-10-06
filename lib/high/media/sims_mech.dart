// Physics labs: measurement, vectors and mechanics (Grades 9–10). Physics and drawing written from scratch.
import 'dart:math' as math;

import 'package:flutter/widgets.dart';

import 'lab_kit.dart';
import 'sims.dart';

const _g = 9.8;
const _steel = Color(0xFFB9BEC4), _steelD = Color(0xFF7D848C);

double _trackH(double x) {
  final u = x / 10;
  return 10 * u * u + 4 * math.exp(-(u / .25) * (u / .25));
}

double _trackDh(double x) => (_trackH(x + 1e-3) - _trackH(x - 1e-3)) / 2e-3;

final Map<String, SimSpec Function(Map<String, dynamic>)> mechLabs = {
  'vectors': (_) => LabSpec(
    height: 280,
    opts: const [
      Opt('m', ['Tip to tail', 'Parallelogram']),
    ],
    sliders: const [
      Sl('F1', 'Force F₁', 0, 10, 6, step: .5, unit: 'N'),
      Sl('a1', 'Direction of F₁', 0, 360, 0, step: 5, unit: '°'),
      Sl('F2', 'Force F₂', 0, 10, 4, step: .5, unit: 'N'),
      Sl('a2', 'Direction of F₂', 0, 360, 90, step: 5, unit: '°'),
    ],
    formula: 'Rx = F₁cos θ₁ + F₂cos θ₂,  Ry = F₁sin θ₁ + F₂sin θ₂;   R = √(Rx² + Ry²)',
    tryThis: 'Point both forces the same way: R = F₁ + F₂. Opposite ways: R = F₁ − F₂. At 90° use Pythagoras: 6 N and 8 N give 10 N.',
    read: (v, t) {
      final a1 = v['a1']! * deg,
          a2 = v['a2']! * deg,
          rx = v['F1']! * math.cos(a1) + v['F2']! * math.cos(a2),
          ry = v['F1']! * math.sin(a1) + v['F2']! * math.sin(a2);
      final r = math.sqrt(rx * rx + ry * ry), th = (math.atan2(ry, rx) / deg + 360) % 360;
      return [('Rx', '${fx(rx, 2)} N'), ('Ry', '${fx(ry, 2)} N'), ('R', '${fx(r, 2)} N'), ('direction', r < 1e-9 ? '—' : '${fx(th)}°')];
    },
    draw: (c, s, v, t, p) {
      final o = Offset(s.width / 2, s.height / 2), sc = (math.min(s.width, s.height) / 2 - 16) / math.max(6.0, v['F1']! + v['F2']!);
      c.drawLine(Offset(10, o.dy), Offset(s.width - 10, o.dy), sk(p.line, 1));
      c.drawLine(Offset(o.dx, 10), Offset(o.dx, s.height - 10), sk(p.line, 1));
      tx(c, 'x', Offset(s.width - 18, o.dy + 2), p.ink2, size: 11);
      tx(c, 'y', Offset(o.dx + 4, 6), p.ink2, size: 11);
      Offset vec(double f, double a) => Offset(math.cos(a * deg), -math.sin(a * deg)) * (f * sc);
      final f1 = vec(v['F1']!, v['a1']!), f2 = vec(v['F2']!, v['a2']!), r = f1 + f2;
      if (v['m'] == 0) {
        arw(c, o, o + f1, p.blue.deep, 3.5, 12);
        arw(c, o + f1, o + r, p.sage.deep, 3.5, 12);
        tx(c, 'F₁', o + f1 / 2 + const Offset(6, 4), p.blue.deep, size: 13);
        tx(c, 'F₂', o + f1 + f2 / 2 + const Offset(6, 4), p.sage.deep, size: 13);
      } else {
        dsh(c, o + f1, o + r, p.ink2, 1.2);
        dsh(c, o + f2, o + r, p.ink2, 1.2);
        arw(c, o, o + f1, p.blue.deep, 3.5, 12);
        arw(c, o, o + f2, p.sage.deep, 3.5, 12);
        tx(c, 'F₁', o + f1 + const Offset(4, 4), p.blue.deep, size: 13);
        tx(c, 'F₂', o + f2 + const Offset(4, 4), p.sage.deep, size: 13);
      }
      if (r.distance > 1) {
        arw(c, o, o + r, p.peach.deep, 4, 13);
        tx(c, 'R', o + r + const Offset(6, -16), p.peach.deep, size: 14, w: FontWeight.w900);
      }
    },
  ),
  'atwood': (_) => LabSpec(
    height: 290,
    anim: true,
    replay: true,
    live: true,
    sliders: const [
      Sl('m1', 'Left mass m₁', 50, 500, 200, step: 10, unit: 'g'),
      Sl('m2', 'Right mass m₂', 50, 500, 250, step: 10, unit: 'g'),
    ],
    tEnd: (v) {
      final a = (v['m2']! - v['m1']!).abs() * _g / (v['m1']! + v['m2']!);
      return a < 1e-9 ? 3 : math.sqrt(2 * 1.0 / a);
    },
    formula: 'a = (m₂ − m₁) g / (m₁ + m₂);   T = 2 m₁ m₂ g / (m₁ + m₂)',
    tryThis:
        'Equal masses do not move (or keep moving at constant speed): the forces balance. The heavier side accelerates down, but always with a < g, because the string pulls back on it.',
    read: (v, t) {
      final m1 = v['m1']! / 1000, m2 = v['m2']! / 1000, a = (m2 - m1) * _g / (m1 + m2), T = 2 * m1 * m2 * _g / (m1 + m2);
      return [
        ('a', '${fx(a.abs(), 2)} m/s²'),
        ('tension T', '${fx(T, 2)} N'),
        ('speed now', '${fx(a.abs() * t, 2)} m/s'),
        ('', a == 0 ? 'balanced' : (a > 0 ? 'right side falls' : 'left side falls')),
      ];
    },
    draw: (c, s, v, t, p) {
      final m1 = v['m1']!, m2 = v['m2']!, a = (m2 - m1) * _g / (m1 + m2), y = .5 * a * t * t; // right mass moves down by y (m)
      final cx = s.width / 2, py = 34.0, R = 30.0, sc = 100.0, y0 = 150.0;
      c.drawLine(Offset(cx, 8), Offset(cx, py), sk(p.ink2, 3));
      c.drawLine(Offset(cx - 60, 8), Offset(cx + 60, 8), sk(p.ink, 4));
      final rot = y / (R / sc);
      c.drawCircle(Offset(cx, py), R, fi(_steel));
      c.drawCircle(Offset(cx, py), R, sk(_steelD, 2));
      c.drawLine(Offset(cx, py), Offset(cx, py) + Offset(math.cos(rot), math.sin(rot)) * (R - 4), sk(_steelD, 2));
      final yl = y0 - y * sc, yr = y0 + y * sc;
      double side(double m) => 22 + 22 * math.sqrt(m / 500);
      final s1 = side(m1), s2 = side(m2);
      c.drawLine(Offset(cx - R, py), Offset(cx - R, yl - s1 / 2), sk(p.ink, 1.5));
      c.drawLine(Offset(cx + R, py), Offset(cx + R, yr - s2 / 2), sk(p.ink, 1.5));
      c.drawRect(Rect.fromCenter(center: Offset(cx - R, yl), width: s1, height: s1), fi(p.blue.deep));
      c.drawRect(Rect.fromCenter(center: Offset(cx + R, yr), width: s2, height: s2), fi(p.peach.deep));
      tx(c, '${m1.round()} g', Offset(cx - R, yl), const Color(0xFFFFFFFF), size: 10.5, ax: .5, ay: .5);
      tx(c, '${m2.round()} g', Offset(cx + R, yr), const Color(0xFFFFFFFF), size: 10.5, ax: .5, ay: .5);
      final floor = y0 + sc + 26;
      c.drawLine(Offset(20, floor), Offset(s.width - 20, floor), sk(p.ink2, 2));
      // force arrows on the right mass: weight and tension (to scale)
      final w2 = m2 / 1000 * _g, T = 2 * m1 * m2 / 1e6 * _g / ((m1 + m2) / 1000), k = 18.0;
      arw(c, Offset(cx + R + s2 / 2 + 14, yr), Offset(cx + R + s2 / 2 + 14, yr + w2 * k), p.ink, 2.5, 8);
      arw(c, Offset(cx + R + s2 / 2 + 14, yr), Offset(cx + R + s2 / 2 + 14, yr - T * k), p.sage.deep, 2.5, 8);
      tx(c, 'W', Offset(cx + R + s2 / 2 + 20, yr + w2 * k - 14), p.ink, size: 11);
      tx(c, 'T', Offset(cx + R + s2 / 2 + 20, yr - T * k), p.sage.deep, size: 11);
      tx(c, 'press play', Offset(8, s.height - 18), p.ink2, size: 10.5);
    },
  ),
  'collision': (_) => LabSpec(
    height: 200,
    anim: true,
    replay: true,
    live: true,
    opts: const [
      Opt('k', ['Elastic (bounce)', 'Sticky (stick together)']),
    ],
    sliders: const [
      Sl('m1', 'Mass of A', .5, 5, 2, step: .5, unit: 'kg'),
      Sl('u1', 'Velocity of A', -5, 5, 3, step: .5, unit: 'm/s'),
      Sl('m2', 'Mass of B', .5, 5, 1, step: .5, unit: 'kg'),
      Sl('u2', 'Velocity of B', -5, 5, -1, step: .5, unit: 'm/s'),
    ],
    tEnd: (v) => 4,
    formula: 'momentum is conserved:  m₁u₁ + m₂u₂ = m₁v₁ + m₂v₂',
    tryThis:
        'In every collision the total momentum stays the same. Kinetic energy is conserved only in the elastic one; when the trolleys stick, some KE turns into heat and sound.',
    read: (v, t) {
      final r = _coll(v), m1 = v['m1']!, m2 = v['m2']!, u1 = v['u1']!, u2 = v['u2']!;
      final p0 = m1 * u1 + m2 * u2, k0 = .5 * m1 * u1 * u1 + .5 * m2 * u2 * u2;
      if (r.tc == null) return [('p total', '${fx(p0, 1)} kg m/s'), ('', 'they never meet: change the velocities')];
      final after = t >= r.tc!, k1 = .5 * m1 * r.v1 * r.v1 + .5 * m2 * r.v2 * r.v2;
      return [
        ('p before', '${fx(p0, 1)} kg m/s'),
        ('p after', '${fx(m1 * r.v1 + m2 * r.v2, 1)} kg m/s'),
        ('KE before', '${fx(k0, 1)} J'),
        ('KE after', after ? '${fx(k1, 1)} J' : '…'),
        if (after) ('v_A, v_B', '${fx(r.v1, 2)}, ${fx(r.v2, 2)} m/s'),
      ];
    },
    draw: (c, s, v, t, p) {
      final r = _coll(v), sc = (s.width - 20) / 10, base = s.height * .7;
      c.drawLine(Offset(0, base), Offset(s.width, base), sk(p.ink2, 2));
      double xA(double tt) => r.tc == null || tt < r.tc! ? 2.2 + v['u1']! * tt : r.xc1 + r.v1 * (tt - r.tc!);
      double xB(double tt) => r.tc == null || tt < r.tc! ? 7.8 + v['u2']! * tt : r.xc2 + r.v2 * (tt - r.tc!);
      void cart(double x, double hw, Color col, String lab, double vel) {
        final q = Offset(10 + x * sc, base), w = hw * 2 * sc, h = 22 + 18 * hw;
        c.drawRect(Rect.fromLTWH(q.dx - w / 2, base - h - 8, w, h), fi(col));
        c.drawCircle(Offset(q.dx - w * .3, base - 5), 5, fi(p.ink));
        c.drawCircle(Offset(q.dx + w * .3, base - 5), 5, fi(p.ink));
        tx(c, lab, Offset(q.dx, base - h / 2 - 8), const Color(0xFFFFFFFF), size: 13, ax: .5, ay: .5, w: FontWeight.w900);
        if (vel.abs() > .01) arw(c, Offset(q.dx, base - h - 18), Offset(q.dx + vel * 12, base - h - 18), col, 2.5, 8);
        tx(c, '${fx(vel, 1)} m/s', Offset(q.dx, base - h - 40), col, size: 10.5, ax: .5);
      }

      final after = r.tc != null && t >= r.tc!;
      cart(xA(t), r.hw1, p.blue.deep, 'A', after ? r.v1 : v['u1']!);
      cart(xB(t), r.hw2, p.peach.deep, 'B', after ? r.v2 : v['u2']!);
      tx(c, after ? 'after the collision' : 'before', Offset(8, s.height - 20), p.ink2, size: 11);
      tx(c, 'press play', Offset(s.width - 8, s.height - 20), p.ink2, size: 10.5, ax: 1);
    },
  ),
  'circular': (_) => LabSpec(
    height: 280,
    anim: true,
    replay: true,
    opts: const [
      Opt('cut', ['On the string', 'Cut the string']),
    ],
    sliders: const [
      Sl('r', 'Radius r', .5, 3, 1.5, step: .1, unit: 'm'),
      Sl('v', 'Speed v', 1, 10, 4, step: .5, unit: 'm/s'),
      Sl('m', 'Mass m', .1, 2, .5, step: .1, unit: 'kg'),
    ],
    tEnd: (v) => v['cut'] == 1 ? 6 : 1e9,
    formula: 'a = v²/r towards the centre;   F = m v²/r;   T = 2πr/v',
    tryThis:
        'Cut the string: with no centripetal force the ball flies off along the tangent in a straight line (Newton’s first law). Double the speed and the force needed is 4 times bigger.',
    read: (v, t) {
      final r = v['r']!, sp = v['v']!, m = v['m']!;
      return [
        ('ω = v/r', '${fx(sp / r, 2)} rad/s'),
        ('T', '${fx(2 * math.pi * r / sp, 2)} s'),
        ('a = v²/r', '${fx(sp * sp / r, 1)} m/s²'),
        ('F = mv²/r', '${fx(m * sp * sp / r, 1)} N'),
      ];
    },
    draw: (c, s, v, t, p) {
      const slow = .25; // animation runs at a quarter of real speed
      final o = Offset(s.width / 2, s.height / 2), R = (s.height / 2 - 24) * v['r']! / 3, sp = v['v']!, w = sp / v['r']!;
      final tc = v['cut'] == 1 ? 1.2 : 1e9, tt = math.min(t, tc);
      final th = w * tt * slow, ball = o + Offset(math.cos(th), -math.sin(th)) * R, tg = Offset(-math.sin(th), -math.cos(th));
      dsh(c, o + Offset(R, 0), o + Offset(R, 0), p.line);
      c.drawCircle(o, R, sk(p.line, 1.2));
      c.drawCircle(o, 4, fi(p.ink));
      var pos = ball;
      if (t > tc) {
        pos = ball + tg * ((t - tc) * slow * sp * R / v['r']!);
        dsh(c, ball, pos, p.ink2, 1.2);
      } else {
        c.drawLine(o, ball, sk(p.ink, 1.5));
        arw(c, pos, pos + (o - pos) / (o - pos).distance * math.min(70.0, 10 + 3 * sp * sp / v['r']!), p.peach.deep, 3, 10);
        tx(c, 'F', pos + (o - pos) / (o - pos).distance * 30 + const Offset(6, -6), p.peach.deep, size: 12);
      }
      arw(c, pos, pos + tg * (14 + sp * 6), p.sage.deep, 3, 10);
      tx(c, 'v', pos + tg * (20 + sp * 6), p.sage.deep, size: 12);
      c.drawCircle(pos, 6 + 6 * math.sqrt(v['m']! / 2), fi(p.blue.deep));
      tx(c, 'slowed ×4', Offset(8, s.height - 18), p.ink2, size: 10.5);
    },
  ),
  'energy_track': (_) {
    var x = -8.0, vel = 0.0, heat = 0.0;
    void reset(V v) {
      double lo = -10, hi = -2.5;
      for (var i = 0; i < 40; i++) {
        final m = (lo + hi) / 2;
        _trackH(m) > v['h']! ? lo = m : hi = m;
      }
      x = (lo + hi) / 2;
      vel = 0;
      heat = 0;
    }

    return LabSpec(
      height: 270,
      anim: true,
      replay: true,
      live: true,
      opts: const [
        Opt('fr', ['No friction', 'With friction']),
      ],
      sliders: const [
        Sl('h', 'Release height', 3, 10, 7, step: .5, unit: 'm'),
        Sl('m', 'Mass', 1, 5, 2, unit: 'kg'),
      ],
      reset: reset,
      step: (dt, v) {
        final fr = v['fr'] == 1, m = v['m']!, e0 = m * _g * v['h']!;
        for (var k = 0; k < 10; k++) {
          final h1 = _trackDh(x), cosA = 1 / math.sqrt(1 + h1 * h1), sinA = h1 * cosA, d = dt / 10;
          var acc = -_g * sinA;
          if (fr && vel.abs() > 1e-3) acc -= .05 * _g * cosA * vel.sign;
          final v0 = vel;
          vel += acc * d;
          if (fr && v0 != 0 && v0.sign != vel.sign && (_g * sinA).abs() < .05 * _g * cosA) vel = 0;
          final dx = vel * cosA * d;
          if (fr) heat += .05 * m * _g * cosA * (vel * d).abs();
          x = (x + dx).clamp(-10.0, 10.0);
          if (!fr) {
            final ke = e0 - m * _g * _trackH(x);
            vel = vel.sign * math.sqrt(math.max(0, 2 * ke / m));
            if (ke <= 0) vel = -_trackDh(x).sign * 1e-3;
          }
        }
      },
      formula: 'PE = m g h,   KE = ½ m v²;   PE + KE (+ heat) = constant',
      tryThis:
          'Release it from below 4 m and it can never get over the 4 m hump. With friction, the total of PE + KE falls and the missing energy appears as heat.',
      read: (v, t) {
        final m = v['m']!, pe = m * _g * _trackH(x), ke = .5 * m * vel * vel;
        return [
          ('PE', '${fx(pe, 0)} J'),
          ('KE', '${fx(ke, 0)} J'),
          ('heat', '${fx(heat, 0)} J'),
          ('total', '${fx(pe + ke + heat, 0)} J'),
          ('speed', '${fx(vel.abs(), 1)} m/s'),
        ];
      },
      draw: (c, s, v, t, p) {
        final sx = (s.width - 70) / 20, sy = (s.height - 40) / 11;
        Offset at(double xx, double hh) => Offset(10 + (xx + 10) * sx, s.height - 16 - hh * sy);
        final path = Path();
        for (var i = 0; i <= 120; i++) {
          final xx = -10 + 20 * i / 120, q = at(xx, _trackH(xx));
          i == 0 ? path.moveTo(q.dx, q.dy) : path.lineTo(q.dx, q.dy);
        }
        c.drawPath(path, sk(p.ink, 3));
        dsh(c, at(-10, v['h']!), at(10, v['h']!), p.sage.deep, 1);
        tx(c, 'start height', at(-10, v['h']!) + const Offset(2, -14), p.sage.deep, size: 10);
        final h1 = _trackDh(x), n = Offset(-h1, -1) / math.sqrt(1 + h1 * h1);
        final q = at(x, _trackH(x)) + Offset(n.dx * sx, n.dy * sy) / math.sqrt(sx * sx * n.dx * n.dx + sy * sy * n.dy * n.dy) * 9;
        c.drawCircle(q, 9, fi(p.peach.deep));
        // energy bars
        final m = v['m']!, e0 = m * _g * v['h']!, pe = m * _g * _trackH(x), ke = .5 * m * vel * vel, bx = s.width - 54, bh = s.height - 50;
        for (final (i, val, col, lab) in [(0, pe, p.blue.deep, 'PE'), (1, ke, p.peach.deep, 'KE'), (2, heat, p.ink2, 'heat')]) {
          final hgt = (val / e0).clamp(0.0, 1.0) * bh, x0 = bx + i * 17.0;
          c.drawRect(Rect.fromLTWH(x0, 16 + bh - hgt, 13, hgt), fi(col));
          tx(c, lab, Offset(x0 + 6, 20 + bh), p.ink2, size: 9, ax: .5);
        }
        c.drawRect(Rect.fromLTWH(bx - 2, 14, 53, bh + 4), sk(p.line, 1));
        tx(c, 'press play', const Offset(8, 8), p.ink2, size: 10.5);
      },
    );
  },
  'vernier': (_) => LabSpec(
    height: 250,
    opts: const [
      Opt('show', ['Hide the reading', 'Show the reading']),
    ],
    sliders: const [Sl('L', 'Object width (drag the jaw)', 0, 60, 23.4, step: .1, unit: 'mm')],
    drag: (v, at, s) {
      final cur = v['L']!, ppm = (s.width - 20) / 30, x0 = s.width / 2 - cur * ppm;
      if (at.dy > 70) v['L'] = (((at.dx - x0) / ppm) * 10).roundToDouble().clamp(0, 600) / 10;
    },
    formula: 'reading = main scale (mm) + coinciding vernier line × 0.1 mm',
    tryThis:
        'Find the main-scale mark just before the vernier 0, then the vernier line that lines up exactly with a main-scale line. Check your answer with “Show the reading”.',
    read: (v, t) {
      final L = (v['L']! * 10).round() / 10, ms = L.floor(), vc = ((L - ms) * 10).round();
      if (v['show'] == 0) return [('least count', '0.1 mm'), ('reading', '?  (read the scale)')];
      return [('main scale', '$ms mm'), ('vernier line', '$vc'), ('reading', '$ms + $vc × 0.1 = ${L.toStringAsFixed(1)} mm')];
    },
    draw: (c, s, v, t, p) {
      final L = v['L']!;
      // top: the whole caliper, schematic
      final x0 = 20.0, pmm = (s.width - 60) / 70, y = 18.0;
      c.drawRect(Rect.fromLTWH(x0, y, s.width - 40, 12), fi(_steel));
      c.drawRect(Rect.fromLTWH(x0, y, 10, 42), fi(_steelD));
      final jx = x0 + 10 + L * pmm;
      c.drawRect(Rect.fromLTWH(jx, y - 4, 34, 20), fi(_steelD));
      c.drawRect(Rect.fromLTWH(jx, y, 10, 42), fi(_steelD));
      if (L > .5) c.drawRect(Rect.fromLTWH(x0 + 10, y + 18, L * pmm, 22), fi(const Color(0xFFD9A35A)));
      // bottom: zoomed scales around the vernier zero
      final ppm = (s.width - 20) / 30, z = s.width / 2 - L * ppm, my = 112.0, vy = my + 4;
      c.drawRect(Rect.fromLTWH(0, my - 40, s.width, 40), fi(_steel));
      for (var mm = 0; mm <= 80; mm++) {
        final x = z + mm * ppm;
        if (x < -2 || x > s.width + 2) continue;
        final len = mm % 10 == 0 ? 22.0 : (mm % 5 == 0 ? 16.0 : 10.0);
        c.drawLine(Offset(x, my), Offset(x, my - len), sk(p.ink, 1.3));
        if (mm % 10 == 0) tx(c, '${mm ~/ 10}', Offset(x, my - 38), p.ink, size: 11, ax: .5);
      }
      tx(c, 'cm', Offset(s.width - 8, my - 38), p.ink2, size: 10, ax: 1);
      final vx = s.width / 2, show = v['show'] == 1, vc = ((L - L.floor()) * 10).round();
      c.drawRect(Rect.fromLTWH(vx - 12, vy, 9 * ppm + 24, 40), fi(const Color(0xFFD5D9DE)));
      for (var i = 0; i <= 10; i++) {
        final x = vx + i * .9 * ppm;
        c.drawLine(Offset(x, vy), Offset(x, vy + (i % 5 == 0 ? 18 : 11)), sk(show && i == vc ? p.peach.deep : p.ink, show && i == vc ? 2.4 : 1.3));
        if (i % 5 == 0) tx(c, '$i', Offset(x, vy + 20), p.ink, size: 10.5, ax: .5);
      }
      tx(c, 'vernier: 10 lines in 9 mm', Offset(vx - 14, vy + 42), p.ink2, size: 10, ax: 1);
      if (show) tx(c, '0 of vernier just after ${L.floor()} mm', Offset(8, s.height - 18), p.peach.deep, size: 10.5);
    },
  ),
  'micrometer': (_) => LabSpec(
    height: 230,
    opts: const [
      Opt('show', ['Hide the reading', 'Show the reading']),
    ],
    sliders: const [Sl('R', 'Spindle gap (drag to turn)', 0, 25, 7.38, step: .01, unit: 'mm', fmt: _mm2)],
    drag: (v, at, s) => v['R'] = ((at.dx - 16) / (s.width - 120) * 25 * 100).roundToDouble().clamp(0, 2500) / 100,
    formula: 'reading = sleeve (mm and ½ mm) + thimble line × 0.01 mm',
    tryThis:
        'Read the last visible sleeve mark (do not miss a half-millimetre mark below the line), then the thimble line that sits on the datum line. Check with “Show the reading”.',
    read: (v, t) {
      final r = (v['R']! * 100).round() / 100, sl = (r * 2).floor() / 2, th = ((r - sl) * 100).round();
      if (v['show'] == 0) return [('least count', '0.01 mm'), ('reading', '?  (read the scale)')];
      return [('sleeve', '${sl.toStringAsFixed(1)} mm'), ('thimble', '$th'), ('reading', '${sl.toStringAsFixed(1)} + $th × 0.01 = ${r.toStringAsFixed(2)} mm')];
    },
    draw: (c, s, v, t, p) {
      final r = v['R']!, x0 = 16.0, ppm = (s.width - 120) / 25, cy = s.height * .45, edge = x0 + r * ppm;
      c.drawRect(Rect.fromLTRB(0, cy - 22, edge, cy + 22), fi(_steel));
      c.drawLine(Offset(0, cy), Offset(edge, cy), sk(p.ink, 1.5));
      for (var k = 0; k <= 50; k++) {
        final x = x0 + k * .5 * ppm;
        if (x > edge - 1) break;
        if (k.isEven) {
          c.drawLine(Offset(x, cy), Offset(x, cy - (k % 10 == 0 ? 16 : 10)), sk(p.ink, 1.3));
          if (k % 10 == 0) tx(c, '${k ~/ 2}', Offset(x, cy - 32), p.ink, size: 11, ax: .5);
        } else {
          c.drawLine(Offset(x, cy), Offset(x, cy + 9), sk(p.ink, 1.3));
        }
      }
      // thimble: 50 divisions round; the datum line points at the current one
      final thW = 70.0, th = (r * 100) % 50;
      c.drawRect(Rect.fromLTRB(edge, cy - 46, edge + thW, cy + 46), fi(_steelD));
      c.drawRect(Rect.fromLTRB(edge, cy - 46, edge + 8, cy + 46), fi(const Color(0xFF6A7178)));
      const gap = 8.0;
      for (var k = -6; k <= 6; k++) {
        final div = (th.floor() + k) % 50, y = cy - (th.floor() + k - th) * gap;
        if ((y - cy).abs() > 44) continue;
        c.drawLine(Offset(edge, y), Offset(edge + (div % 5 == 0 ? 20 : 12), y), sk(const Color(0xFFF2F2F2), 1.3));
        if (div % 5 == 0) tx(c, '$div', Offset(edge + 24, y), const Color(0xFFF2F2F2), size: 10.5, ay: .5);
      }
      c.drawRect(Rect.fromLTRB(edge + thW, cy - 16, s.width, cy + 16), fi(_steelD));
      tx(c, 'sleeve', Offset(6, cy + 26), p.ink2, size: 10.5);
      tx(c, 'thimble', Offset(edge + 4, cy + 50), p.ink2, size: 10.5);
      if (v['show'] == 1) {
        final sl = (r * 2).floor() / 2;
        tx(c, 'last sleeve mark ${sl.toStringAsFixed(1)} mm', Offset(8, s.height - 18), p.peach.deep, size: 10.5);
      }
    },
  ),
};

String _mm2(double x) => '${x.toStringAsFixed(2)} mm';

class _Coll {
  _Coll(this.tc, this.v1, this.v2, this.xc1, this.xc2, this.hw1, this.hw2);
  final double? tc;
  final double v1, v2, xc1, xc2, hw1, hw2;
}

_Coll _coll(V v) {
  final m1 = v['m1']!, m2 = v['m2']!, u1 = v['u1']!, u2 = v['u2']!;
  double hw(double m) => .3 + .25 * math.pow(m / 5, 1 / 3);
  final h1 = hw(m1), h2 = hw(m2), gap = (7.8 - h2) - (2.2 + h1);
  if (u1 - u2 <= 1e-9) return _Coll(null, u1, u2, 0, 0, h1, h2);
  final tc = gap / (u1 - u2);
  double v1, v2;
  if (v['k'] == 0) {
    v1 = ((m1 - m2) * u1 + 2 * m2 * u2) / (m1 + m2);
    v2 = ((m2 - m1) * u2 + 2 * m1 * u1) / (m1 + m2);
  } else {
    v1 = v2 = (m1 * u1 + m2 * u2) / (m1 + m2);
  }
  return _Coll(tc, v1, v2, 2.2 + u1 * tc, 7.8 + u2 * tc, h1, h2);
}

// Physics labs: oscillations, waves and sound (Grade 11 unit 3) and light interference (Grade 12). Written from scratch.
import 'dart:math' as math;
import 'dart:typed_data';
import 'dart:ui' as ui;

import 'package:flutter/widgets.dart';

import '../notes/jr/theme/tokens.dart';
import 'lab_kit.dart';
import 'sims.dart';

const _water0 = Color(0xFF1F4E7A), _water1 = Color(0xFF5E9CC9), _water2 = Color(0xFFE6F2FA);

/// a small framed x–y plot strip
void _strip(Canvas c, Rect r, Palette p, double Function(double u) y, Color col, {String label = '', double w = 2.2, int n = 160}) {
  c.drawRect(r, fi(p.surface));
  c.drawLine(Offset(r.left, r.center.dy), Offset(r.right, r.center.dy), sk(p.line, 1));
  final path = Path();
  for (var i = 0; i <= n; i++) {
    final u = i / n, q = Offset(r.left + r.width * u, r.center.dy - y(u).clamp(-1.05, 1.05) * r.height * .45);
    i == 0 ? path.moveTo(q.dx, q.dy) : path.lineTo(q.dx, q.dy);
  }
  c.drawPath(path, sk(col, w));
  if (label.isNotEmpty) tx(c, label, r.topLeft + const Offset(4, 2), p.ink2, size: 10.5);
}

/// spring zig-zag from a to b
void spring(Canvas c, Offset a, Offset b, Color col, {int coils = 12, double width = 14}) {
  final d = b - a, len = d.distance, u = d / len, n = Offset(-u.dy, u.dx), path = Path()..moveTo(a.dx, a.dy);
  final lead = math.min(10.0, len * .1), s0 = a + u * lead;
  path.lineTo(s0.dx, s0.dy);
  for (var i = 0; i < coils * 2; i++) {
    final q = s0 + u * ((len - 2 * lead) * (i + .5) / (coils * 2)) + n * (i.isEven ? width / 2 : -width / 2);
    path.lineTo(q.dx, q.dy);
  }
  final e = b - u * lead;
  path
    ..lineTo(e.dx, e.dy)
    ..lineTo(b.dx, b.dy);
  c.drawPath(path, sk(col, 2));
}

double _shmX(V v, double t) {
  final m = v['m']!, k = v['k']!, g = v['b']! / (2 * m), w0 = math.sqrt(k / m), A = v['A']! / 100;
  if (g < w0) {
    final w = math.sqrt(w0 * w0 - g * g);
    return A * math.exp(-g * t) * (math.cos(w * t) + g / w * math.sin(w * t));
  }
  if ((g - w0).abs() < 1e-9) return A * math.exp(-g * t) * (1 + g * t);
  final r1 = -g + math.sqrt(g * g - w0 * w0), r2 = -g - math.sqrt(g * g - w0 * w0);
  return A * (r2 * math.exp(r1 * t) - r1 * math.exp(r2 * t)) / (r2 - r1);
}

final Map<String, SimSpec Function(Map<String, dynamic>)> wavesLabs = {
  'shm': (_) => LabSpec(
    height: 260,
    anim: true,
    replay: true,
    live: true,
    sliders: const [
      Sl('m', 'Mass m', .1, 2, .5, step: .1, unit: 'kg'),
      Sl('k', 'Spring constant k', 5, 100, 20, step: 5, unit: 'N/m'),
      Sl('A', 'Amplitude A', 2, 10, 8, unit: 'cm'),
      Sl('b', 'Damping (friction)', 0, 2, 0, step: .1, unit: 'kg/s'),
    ],
    formula: 'T = 2π √(m/k);   x = A cos ωt  (ω = 2π/T)',
    tryThis:
        'Four times the mass doubles the period; a stiffer spring makes it faster. The amplitude does not change T. Add damping to see the oscillation die away.',
    read: (v, t) {
      final T = 2 * math.pi * math.sqrt(v['m']! / v['k']!), w = 2 * math.pi / T, A = v['A']! / 100;
      return [('T', '${fx(T, 2)} s'), ('f = 1/T', '${fx(1 / T, 2)} Hz'), ('v max = Aω', '${fx(A * w, 2)} m/s'), ('x now', '${fx(_shmX(v, t) * 100)} cm')];
    },
    draw: (c, s, v, t, p) {
      final sx = s.width * .2, top = 14.0, eq = s.height * .5, sc = (s.height * .36) / 10;
      c.drawLine(Offset(sx - 40, top), Offset(sx + 40, top), sk(p.ink, 4));
      for (var x = sx - 36; x < sx + 40; x += 10) {
        c.drawLine(Offset(x, top), Offset(x + 7, top - 7), sk(p.ink2, 1.2));
      }
      final x = _shmX(v, t) * 100, my = eq + x * sc, bs = 24 + 14 * math.sqrt(v['m']! / 2);
      spring(c, Offset(sx, top), Offset(sx, my - bs / 2), p.ink2, coils: 10, width: 10 + v['k']! / 10);
      dsh(c, Offset(sx - 50, eq), Offset(sx + 50, eq), p.sage.deep, 1.2);
      tx(c, 'rest', Offset(sx + 34, eq - 16), p.sage.deep, size: 10.5);
      c.drawRect(Rect.fromCenter(center: Offset(sx, my), width: bs, height: bs), fi(p.peach.deep));
      tx(c, '${fx(v['m']!)} kg', Offset(sx, my), const Color(0xFFFFFFFF), size: 10.5, ax: .5, ay: .5);
      // x-t graph of the last 6 s
      final g = Rect.fromLTRB(s.width * .4, 20, s.width - 8, s.height - 20), A = v['A']!;
      c.drawRect(g, fi(p.surface));
      c.drawLine(Offset(g.left, g.center.dy), Offset(g.right, g.center.dy), sk(p.line, 1));
      final t0 = math.max(0.0, t - 6), path = Path();
      for (var i = 0; i <= 150; i++) {
        final tt = t0 + (t - t0) * i / 150, q = Offset(g.left + g.width * (tt - t0) / 6, g.center.dy + _shmX(v, tt) * 100 / 10 * g.height * .45);
        i == 0 ? path.moveTo(q.dx, q.dy) : path.lineTo(q.dx, q.dy);
      }
      c.drawPath(path, sk(p.blue.deep, 2));
      c.drawCircle(Offset(g.left + g.width * (t - t0) / 6, g.center.dy + x / 10 * g.height * .45), 4, fi(p.peach.deep));
      c.drawLine(
        Offset(sx + bs / 2 + 4, my),
        Offset(g.left + g.width * (t - t0) / 6, g.center.dy + x / 10 * g.height * .45),
        sk(p.peach.deep.withValues(alpha: .3), 1),
      );
      tx(c, 'x (down +) against time', g.bottomLeft + const Offset(4, -28), p.ink2, size: 10.5);
      tx(c, '±${A.round()} cm', g.bottomLeft + const Offset(4, -14), p.ink2, size: 10);
    },
  ),
  'standing': (_) => LabSpec(
    height: 230,
    anim: true,
    t0: .15,
    opts: const [
      Opt('kind', ['String (fixed ends)', 'Pipe closed at one end', 'Pipe open at both ends']),
    ],
    sliders: [
      const Sl('n', 'Mode (1 = fundamental)', 1, 6, 1),
      const Sl('L', 'Length L', .2, 2, 1, step: .1, unit: 'm'),
      Sl('v', 'Wave speed on the string', 50, 400, 200, step: 10, unit: 'm/s', when: (v) => v['kind'] == 0),
    ],
    formulaOf: (v) => switch (v['kind']!.round()) {
      0 => 'λ = 2L/n,   f = n v / 2L   (all harmonics)',
      1 => 'λ = 4L/(2n−1),   f = (2n−1) v / 4L   (odd harmonics only)',
      _ => 'λ = 2L/n,   f = n v / 2L   (all harmonics)',
    },
    tryThis:
        'Count the nodes (N) and antinodes (A). A pipe closed at one end has a node at the closed end and an antinode at the open end, so only odd harmonics fit.',
    read: (v, t) {
      final kind = v['kind']!.round(), n = v['n']!.round(), L = v['L']!, sp = kind == 0 ? v['v']! : 343.0;
      final lam = kind == 1 ? 4 * L / (2 * n - 1) : 2 * L / n, h = kind == 1 ? 2 * n - 1 : n;
      return [('harmonic', '${_ord(h)} (×$h)'), ('λ', '${fx(lam, 2)} m'), ('f = v/λ', '${fx(sp / lam, 0)} Hz'), if (kind != 0) ('v (air, 20 °C)', '343 m/s')];
    },
    draw: (c, s, v, t, p) {
      final kind = v['kind']!.round(), n = v['n']!.round(), x0 = 24.0, x1 = s.width - 24, cy = s.height * .5, A = s.height * .3;
      final cosw = math.cos(2 * math.pi * .7 * t);
      double shape(double u) => switch (kind) {
        0 => math.sin(n * math.pi * u),
        1 => math.sin((2 * n - 1) * math.pi / 2 * u),
        _ => math.cos(n * math.pi * u),
      };
      if (kind == 0) {
        c.drawRect(Rect.fromLTWH(x0 - 10, cy - 30, 10, 60), fi(p.ink2));
        c.drawRect(Rect.fromLTWH(x1, cy - 30, 10, 60), fi(p.ink2));
      } else {
        c.drawLine(Offset(x0, cy - A - 12), Offset(x1, cy - A - 12), sk(p.ink, 3));
        c.drawLine(Offset(x0, cy + A + 12), Offset(x1, cy + A + 12), sk(p.ink, 3));
        if (kind == 1) c.drawLine(Offset(x0, cy - A - 12), Offset(x0, cy + A + 12), sk(p.ink, 6));
        tx(c, kind == 1 ? 'closed' : 'open', Offset(x0 + 4, cy + A + 16), p.ink2, size: 10.5);
        tx(c, 'open', Offset(x1 - 4, cy + A + 16), p.ink2, size: 10.5, ax: 1);
      }
      final env1 = Path(), env2 = Path(), wave = Path();
      for (var i = 0; i <= 160; i++) {
        final u = i / 160, x = x0 + (x1 - x0) * u, y = shape(u);
        i == 0 ? env1.moveTo(x, cy - A * y) : env1.lineTo(x, cy - A * y);
        i == 0 ? env2.moveTo(x, cy + A * y) : env2.lineTo(x, cy + A * y);
        i == 0 ? wave.moveTo(x, cy - A * y * cosw) : wave.lineTo(x, cy - A * y * cosw);
      }
      c.drawPath(env1, sk(p.ink2.withValues(alpha: .35), 1.2));
      c.drawPath(env2, sk(p.ink2.withValues(alpha: .35), 1.2));
      c.drawPath(wave, sk(kind == 0 ? p.peach.deep : p.blue.deep, 3));
      // nodes and antinodes
      for (var i = 0; i <= 240; i++) {
        final u = i / 240, y = shape(u).abs(), ya = shape(math.max(0, u - 1 / 240)).abs(), yb = shape(math.min(1, u + 1 / 240)).abs();
        final x = x0 + (x1 - x0) * u;
        if (y <= ya && y <= yb && y < .05) tx(c, 'N', Offset(x, cy + 6), p.ink, size: 11, ax: .5, w: FontWeight.w900);
        if (y >= ya && y >= yb && y > .95) tx(c, 'A', Offset(x, cy - A - (kind == 0 ? 18 : 30)), p.sage.deep, size: 11, ax: .5, w: FontWeight.w900);
      }
      if (kind != 0) tx(c, 'curves: how far the air moves', Offset(s.width - 8, 6), p.ink2, size: 10, ax: 1);
    },
  ),
  'superposition': (_) => LabSpec(
    height: 280,
    anim: true,
    t0: .1,
    opts: const [
      Opt('dir', ['Same direction', 'Opposite directions']),
    ],
    sliders: const [
      Sl('A1', 'Amplitude of wave 1', 0, 1, .6, step: .1, unit: 'm'),
      Sl('A2', 'Amplitude of wave 2', 0, 1, .6, step: .1, unit: 'm'),
      Sl('l2', 'Wavelength of wave 2 (wave 1 = 2 m)', 1, 4, 2, step: .1, unit: 'm'),
      Sl('ph', 'Phase difference', 0, 360, 0, step: 15, unit: '°'),
    ],
    formula: 'principle of superposition: y = y₁ + y₂ at every point',
    tryThis:
        'Equal waves in phase (0°) add to double height; at 180° they cancel completely. Make the wavelengths slightly different to see beats. Send them in opposite directions to make a standing wave.',
    read: (v, t) {
      final same = (v['l2']! - 2).abs() < .01, ph = v['ph']!, opp = v['dir'] == 1;
      String what;
      if (!same) {
        what = opp ? 'a moving, changing pattern' : 'beats: loud and quiet groups';
      } else if (opp) {
        what = 'standing wave (nodes stay still)';
      } else if (ph % 360 == 0) {
        what = 'constructive: amplitude ${fx(v['A1']! + v['A2']!)} m';
      } else if (ph == 180) {
        what = v['A1'] == v['A2'] ? 'destructive: they cancel' : 'destructive: amplitude ${fx((v['A1']! - v['A2']!).abs())} m';
      } else {
        final a = math.sqrt(math.pow(v['A1']!, 2) + math.pow(v['A2']!, 2) + 2 * v['A1']! * v['A2']! * math.cos(ph * deg));
        what = 'partial: amplitude ${fx(a, 2)} m';
      }
      return [('', what)];
    },
    draw: (c, s, v, t, p) {
      const xm = 8.0, sp = 1.0; // metres across, wave speed (m/s, slowed)
      final k1 = 2 * math.pi / 2, k2 = 2 * math.pi / v['l2']!, w1 = k1 * sp, w2 = k2 * sp, opp = v['dir'] == 1 ? -1.0 : 1.0, ph = v['ph']! * deg;
      double y1(double x) => v['A1']! * math.sin(k1 * x - w1 * t);
      double y2(double x) => v['A2']! * math.sin(k2 * x - opp * w2 * t + ph);
      final h = (s.height - 24) / 4;
      _strip(c, Rect.fromLTWH(8, 6, s.width - 16, h), p, (u) => y1(u * xm), p.blue.deep, label: 'wave 1');
      _strip(c, Rect.fromLTWH(8, 12 + h, s.width - 16, h), p, (u) => y2(u * xm), p.sage.deep, label: 'wave 2');
      _strip(c, Rect.fromLTWH(8, 18 + 2 * h, s.width - 16, 2 * h), p, (u) => (y1(u * xm) + y2(u * xm)) / 2, p.peach.deep, label: 'sum y₁ + y₂', w: 3, n: 240);
    },
  ),
  'ripple': (_) => _rippleLab(false),
  'interference2d': (_) => _rippleLab(true),
  'doppler': (_) => LabSpec(
    height: 250,
    anim: true,
    replay: true,
    live: true,
    sliders: const [
      Sl('m', 'Source speed ÷ wave speed', 0, 1.4, .5, step: .05),
      Sl('f0', 'Source frequency', 200, 1000, 500, step: 50, unit: 'Hz'),
    ],
    tEnd: (v) => v['m']! == 0 ? 6 : math.min(12.0, 380 / (v['m']! * 60)),
    formula: 'ahead: f = f₀ v/(v − vs);   behind: f = f₀ v/(v + vs)   (v = 340 m/s in air)',
    tryThis:
        'Press play. Ahead of the moving source the wavefronts bunch up (higher pitch); behind they spread out (lower pitch). At speed ratio 1 or more they pile into a shock wave: a sonic boom.',
    read: (v, t) {
      const c = 340.0;
      final vs = v['m']! * c, f0 = v['f0']!;
      return [
        ('vs', '${fx(vs, 0)} m/s'),
        ('ahead', v['m']! >= 1 ? 'shock wave' : '${fx(f0 * c / (c - vs), 0)} Hz'),
        ('behind', '${fx(f0 * c / (c + vs), 0)} Hz'),
      ];
    },
    draw: (c, s, v, t, p) {
      const cpx = 60.0, T = .35; // wave speed (px/s) and emission period (s), slowed down
      final m = v['m']!, cy = s.height / 2, x0 = m == 0 ? s.width / 2 : 20.0;
      double xs(double tt) => x0 + m * cpx * tt;
      for (var k = (t / T).floor(); k >= 0; k--) {
        final te = k * T, r = cpx * (t - te);
        if (r > s.width * 1.3) break;
        c.drawCircle(Offset(xs(te), cy), r, sk(p.blue.deep.withValues(alpha: (1 - r / (s.width * 1.3)).clamp(.15, 1)), 1.6));
      }
      final src = Offset(xs(t), cy);
      c.drawCircle(src, 8, fi(p.peach.deep));
      if (m > 0) arw(c, src + const Offset(10, 0), src + Offset(10 + 30 * m, 0), p.peach.deep, 2, 7);
      for (final (x, lab) in [(s.width - 18, 'ahead: high'), (18.0, 'behind: low')]) {
        c.drawOval(Rect.fromCenter(center: Offset(x, cy + 70), width: 14, height: 20), fi(p.surface));
        c.drawOval(Rect.fromCenter(center: Offset(x, cy + 70), width: 14, height: 20), sk(p.ink, 2));
        tx(c, lab, Offset(x, cy + 84), p.ink2, size: 10.5, ax: x > s.width / 2 ? 1 : 0);
      }
      tx(c, 'press play', Offset(8, s.height - 18), p.ink2, size: 10.5);
    },
  ),
  'sound_particles': (_) => LabSpec(
    height: 250,
    anim: true,
    t0: .1,
    sliders: const [
      Sl('f', 'Frequency', 100, 1000, 300, step: 50, unit: 'Hz'),
      Sl('T', 'Air temperature', 0, 40, 20, unit: '°C'),
    ],
    formula: 'v = f λ;   in air v ≈ 331 + 0.6 T  (m/s, T in °C)',
    tryThis:
        'Watch one particle: it only moves back and forth while the compressions travel on. Raise the frequency: the compressions get closer together (shorter λ). Warmer air carries sound faster.',
    read: (v, t) {
      final sp = 331 + .6 * v['T']!, lam = sp / v['f']!;
      return [('v', '${fx(sp, 0)} m/s'), ('λ = v/f', '${fx(lam, 2)} m'), ('period', '${fx(1000 / v['f']!, 1)} ms')];
    },
    draw: (c, s, v, t, p) {
      final sp = 331 + .6 * v['T']!, lam = sp / v['f']!, metres = 4.0, x0 = 36.0, x1 = s.width - 8, lpx = (x1 - x0) * lam / metres;
      final ph = 2 * math.pi * .6 * t, amp = math.min(9.0, lpx * .18), top = 14.0, bot = s.height * .62;
      final pts = <double>[];
      final rows = 9, cols = ((x1 - x0) / 7).floor();
      for (var j = 0; j < rows; j++) {
        for (var i = 0; i < cols; i++) {
          final x = x0 + i * 7 + (j.isEven ? 0 : 3.5), xi = amp * math.sin(2 * math.pi * (x - x0) / lpx - ph);
          pts
            ..add(x + xi)
            ..add(top + (bot - top) * (j + .5) / rows);
        }
      }
      c.drawRawPoints(
        ui.PointMode.points,
        Float32List.fromList(pts),
        Paint()
          ..color = p.ink2
          ..strokeWidth = 3.4
          ..strokeCap = StrokeCap.round,
      );
      // tracked particle
      final xi0 = amp * math.sin(2 * math.pi * (lpx * 1.25) / lpx - ph);
      c.drawCircle(Offset(x0 + lpx * 1.25 + xi0, (top + bot) / 2), 5, fi(p.peach.deep));
      // speaker
      final cone = 4 * math.sin(-ph);
      c.drawRect(Rect.fromLTWH(4, (top + bot) / 2 - 18, 14, 36), fi(p.ink));
      c.drawPath(
        Path()..addPolygon([Offset(18, (top + bot) / 2 - 10), Offset(28 + cone, top + 6), Offset(28 + cone, bot - 6), Offset(18, (top + bot) / 2 + 10)], true),
        fi(p.ink2),
      );
      // pressure graph: compressions where the displacement gradient is negative
      final g = Rect.fromLTRB(x0, bot + 12, x1, s.height - 8);
      _strip(c, g, p, (u) => -math.cos(2 * math.pi * (u * (x1 - x0)) / lpx - ph), p.blue.deep, label: 'pressure');
      for (var k = 0; k < 8; k++) {
        final xc = x0 + ((ph / (2 * math.pi)) * lpx + (k + .5) * lpx) % ((x1 - x0) + lpx);
        if (xc > x1 - 8 || lpx < 24) continue;
        tx(c, 'C', Offset(xc, g.top + 2), p.peach.deep, size: 10.5, ax: .5, w: FontWeight.w900);
        if (xc + lpx / 2 < x1 - 8) tx(c, 'R', Offset(xc + lpx / 2, g.top + 2), p.sage.deep, size: 10.5, ax: .5, w: FontWeight.w900);
      }
      tx(c, '4 m of air, slowed down', Offset(x1, top - 12), p.ink2, size: 10, ax: 1);
    },
  ),
  'pulse_reflection': (_) => LabSpec(
    height: 210,
    anim: true,
    replay: true,
    opts: const [
      Opt('end', ['Fixed end', 'Free end', 'Light → heavy rope', 'Heavy → light rope']),
    ],
    tEnd: (v) => 5.4,
    formula: 'fixed end / denser rope: reflected pulse inverted;   free end / lighter rope: upright',
    tryThis:
        'Press play. At a fixed end the pulse comes back upside down; at a free end it comes back the same way up. At a join some of the pulse is reflected and some goes on.',
    read: (v, t) {
      final e = v['end']!.round();
      if (e < 2) return [('reflected pulse', e == 0 ? 'inverted' : 'upright')];
      final r = e == 2 ? (.5 - 1) / 1.5 : (2 - 1) / 3, tau = e == 2 ? 2 * .5 / 1.5 : 2 * 2 / 3;
      return [
        ('reflected', '${fx(r, 2)} × (${r < 0 ? 'inverted' : 'upright'})'),
        ('transmitted', '${fx(tau, 2)} ×'),
        ('speed in 2nd rope', e == 2 ? 'half' : 'double'),
      ];
    },
    draw: (c, s, v, t, p) {
      final e = v['end']!.round(), x0 = 16.0, cy = s.height * .55, A = s.height * .3, v1 = (s.width - 40) / 2.6;
      final L = e < 2 ? s.width - 26 : s.width * .55, v2 = e == 2 ? v1 * .5 : v1 * 2, wd = 22.0;
      double g(double u) => A * math.exp(-(u / wd) * (u / wd));
      final r = e == 0 ? -1.0 : (e == 1 ? 1.0 : (e == 2 ? -1 / 3 : 1 / 3)), tau = e == 2 ? 2 / 3 : 4 / 3;
      final start = x0 - 50;
      double y(double x) {
        final inc = x - start - v1 * t;
        if (x <= L) return g(inc) + r * g(2 * L - x - start - v1 * t);
        return tau * g((x - L) * v1 / v2 + L - start - v1 * t);
      }

      final p1 = Path();
      for (var x = x0; x <= L; x += 2) {
        final q = Offset(x, cy - y(x));
        x == x0 ? p1.moveTo(q.dx, q.dy) : p1.lineTo(q.dx, q.dy);
      }
      if (e >= 2) {
        final p3 = Path()..moveTo(L, cy - y(L));
        for (var x = L; x <= s.width - 8; x += 2) {
          p3.lineTo(x, cy - y(x));
        }
        c.drawPath(p3, sk(e == 2 ? p.ink : p.peach.deep, e == 2 ? 5 : 2));
      }
      c.drawPath(p1, sk(e == 3 ? p.ink : p.peach.deep, e == 3 ? 5 : 2.5));
      if (e == 0) {
        c.drawRect(Rect.fromLTWH(L, cy - 50, 10, 100), fi(p.ink2));
      } else if (e == 1) {
        c.drawLine(Offset(L + 4, cy - 60), Offset(L + 4, cy + 50), sk(p.ink2, 3));
        c.drawCircle(Offset(L + 4, cy - y(L)), 6, sk(p.ink, 2.5));
      } else {
        c.drawCircle(Offset(L, cy - y(L)), 4, fi(p.ink));
      }
      c.drawCircle(Offset(x0, cy - y(x0)), 5, fi(p.ink));
      tx(c, 'press play', const Offset(8, 8), p.ink2, size: 10.5);
    },
  ),
  'double_slit': (_) => LabSpec(
    height: 270,
    sliders: [
      Sl('d', 'Slit separation d', .1, 1, .3, step: .05, unit: 'mm'),
      Sl('l', 'Wavelength λ', 400, 700, 600, step: 10, unit: 'nm', fmt: (x) => '${x.round()} nm'),
      const Sl('D', 'Slits to screen D', .5, 3, 2, step: .1, unit: 'm'),
    ],
    drag: (v, at, s) {
      if (at.dx > s.width * .55) v['y'] = ((s.height / 2 - at.dy) / (s.height / 2 - 14) * 25).clamp(-25.0, 25.0);
    },
    formula: 'bright fringes where the path difference = nλ;   fringe spacing Δy = λD/d',
    tryThis:
        'Tap the screen to measure the path difference at a point. Red light (longer λ) gives wider fringes than blue; moving the slits closer together also spreads the fringes.',
    read: (v, t) {
      final d = v['d']! * 1e-3, l = v['l']! * 1e-9, D = v['D']!, y = (v['y'] ?? 0) * 1e-3, pd = d * y / D / l;
      final frac = (pd - pd.roundToDouble()).abs();
      return [
        ('Δy = λD/d', '${fx(l * D / d * 1000, 2)} mm'),
        ('path difference at the point', '${fx(pd, 2)} λ'),
        ('', frac < .15 ? 'bright (n = ${pd.round().abs()})' : (frac > .35 ? 'dark' : 'in between')),
      ];
    },
    draw: (c, s, v, t, p) {
      final d = v['d']! * 1e-3, l = v['l']! * 1e-9, D = v['D']!, col = waveColor(v['l']!), cy = s.height / 2;
      final bx = s.width * .28, scx = s.width * .62, half = s.height / 2 - 14;
      // light and barrier
      c.drawCircle(Offset(18, cy), 8, fi(col));
      for (var k = 1; k < 6; k++) {
        c.drawLine(Offset(18 + k * (bx - 18) / 6, cy - 22), Offset(18 + k * (bx - 18) / 6, cy + 22), sk(col.withValues(alpha: .5), 1.5));
      }
      final sg = 8 + 22 * v['d']!;
      c.drawLine(Offset(bx, 8), Offset(bx, cy - sg - 3), sk(p.ink, 5));
      c.drawLine(Offset(bx, cy - sg + 3), Offset(bx, cy + sg - 3), sk(p.ink, 5));
      c.drawLine(Offset(bx, cy + sg + 3), Offset(bx, s.height - 8), sk(p.ink, 5));
      // screen: brightness I = cos²(π d y/λD) × single-slit envelope
      const a = .06e-3;
      for (var py = -half; py <= half; py += 2) {
        final y = py / half * .025, b = math.pi * d * y / (l * D), e = math.pi * a * y / (l * D);
        final env = e.abs() < 1e-6 ? 1.0 : math.pow(math.sin(e) / e, 2).toDouble(), I = math.pow(math.cos(b), 2) * env;
        c.drawRect(Rect.fromLTWH(scx, cy - py - 1, 18, 2.2), fi(Color.lerp(const Color(0xFF15120F), col, I.toDouble())!));
        final gx = scx + 26 + I * (s.width - scx - 34);
        c.drawLine(Offset(scx + 26, cy - py), Offset(gx, cy - py), sk(col.withValues(alpha: .7), 1.2));
      }
      tx(c, 'screen', Offset(scx + 9, s.height - 12), p.ink2, size: 10, ax: .5);
      // rays to the probe point
      final yp = (v['y'] ?? 0) / 25 * half, q = Offset(scx, cy - yp);
      for (final sy in [-sg, sg]) {
        c.drawLine(Offset(bx, cy + sy), q, sk(col.withValues(alpha: .9), 1.5));
      }
      c.drawCircle(q, 5, fi(p.peach.deep));
      tx(c, '±25 mm', Offset(scx - 4, 8), p.ink2, size: 10, ax: 1);
      tx(c, 'tap the screen', Offset(scx - 4, s.height - 22), p.ink2, size: 10, ax: 1);
    },
  ),
};

String _ord(int n) => switch (n) {
  1 => '1st',
  2 => '2nd',
  3 => '3rd',
  _ => '${n}th',
};

/// ripple tank on one coloured mesh: point source, plane wave, a gap (diffraction) or two sources (interference)
SimSpec _rippleLab(bool two) {
  final field = WaveField(72, 56);
  return LabSpec(
    height: 260,
    anim: true,
    t0: .05,
    opts: two
        ? const []
        : const [
            Opt('kind', ['Point source', 'Plane wave', 'Through a gap']),
          ],
    sliders: [
      const Sl('l', 'Wavelength λ', 1, 4, 2, step: .2, unit: 'cm'),
      if (two) const Sl('d', 'Distance between the sources d', 2, 12, 6, step: .5, unit: 'cm'),
      if (!two) Sl('g', 'Gap width', .5, 10, 2, step: .5, unit: 'cm', when: (v) => v['kind'] == 2),
    ],
    formula: two
        ? 'bright (antinodal) lines where |r₁ − r₂| = nλ;  calm (nodal) lines where it is (n + ½)λ'
        : 'v = f λ;  a gap about as wide as λ spreads the waves most (diffraction)',
    tryThis: two
        ? 'Move the sources further apart or shorten λ: more antinodal lines appear and they get closer together.'
        : 'Choose “Through a gap”. Make the gap about one wavelength: the waves spread out in circles. A wide gap lets a straight beam through with little spreading.',
    read: (v, t) {
      final l = v['l']!;
      if (two) {
        final n = (v['d']! / l).floor();
        return [('d / λ', fx(v['d']! / l, 2)), ('antinodal lines', '${2 * n + 1}')];
      }
      if (v['kind'] == 2) {
        final r = v['g']! / l;
        return [('gap / λ', fx(r, 2)), ('', r < 1.5 ? 'strong spreading (diffraction)' : (r < 4 ? 'some spreading' : 'little spreading'))];
      }
      return [('λ', '${fx(l)} cm'), ('', v['kind'] == 0 ? 'circular wavefronts' : 'straight wavefronts')];
    },
    draw: (c, s, v, t, p) {
      final cmPx = s.width / 30, k = 2 * math.pi / (v['l']! * cmPx), kind = two ? 3 : v['kind']!.round(), cy = s.height / 2;
      final bx = s.width * .3, g = (v['g'] ?? 2) * cmPx;
      final srcs = two ? [Offset(s.width * .14, cy - v['d']! * cmPx / 2), Offset(s.width * .14, cy + v['d']! * cmPx / 2)] : [Offset(s.width * .14, cy)];
      field.prepare(s, '$kind|${v['l']}|${v['d']}|${v['g']}', (x, y) {
        if (kind == 1 || (kind == 2 && x <= bx)) {
          final ph = k * x;
          return (math.cos(ph) * .8, math.sin(ph) * .8);
        }
        if (kind == 2) {
          double re = 0, im = 0;
          const n = 14;
          for (var i = 0; i < n; i++) {
            final sy = cy - g / 2 + g * (i + .5) / n,
                r = math.sqrt((x - bx) * (x - bx) + (y - sy) * (y - sy)) + 1,
                a = 4.2 / n / math.sqrt(r / (s.width * .25) + .15),
                ph = k * (r + bx);
            re += a * math.cos(ph);
            im += a * math.sin(ph);
          }
          return (re, im);
        }
        double re = 0, im = 0;
        for (final o in srcs) {
          final r = (Offset(x, y) - o).distance + 1, a = .9 / math.sqrt(r / (s.width * .2) + .2), ph = k * r;
          re += a * math.cos(ph);
          im += a * math.sin(ph);
        }
        return (re, im);
      });
      field.draw(c, 2 * math.pi * .8 * t, _water0, _water1, _water2, gain: .9);
      if (kind == 2) {
        c.drawRect(Rect.fromLTRB(bx - 3, 0, bx + 3, cy - g / 2), fi(const Color(0xFF3A3530)));
        c.drawRect(Rect.fromLTRB(bx - 3, cy + g / 2, bx + 3, s.height), fi(const Color(0xFF3A3530)));
      }
      if (kind == 0 || kind == 3) {
        for (final o in srcs) {
          c.drawCircle(o, 5, fi(const Color(0xFFFFFFFF)));
          c.drawCircle(o, 5, sk(const Color(0xFF3A3530), 1.5));
        }
      }
      tx(c, '30 cm ripple tank (top view)', Offset(s.width - 8, s.height - 18), const Color(0xFFFFFFFF), size: 10, ax: 1);
    },
  );
}

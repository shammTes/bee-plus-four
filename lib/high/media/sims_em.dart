// Physics labs: magnetism and electromagnetism (Grade 11 unit 2, EM waves) and electrostatics / circuits (Grade 10
// units 3–4). Physics and drawing written from scratch.
import 'dart:math' as math;

import 'package:flutter/widgets.dart';

import '../notes/jr/theme/tokens.dart';
import 'lab_kit.dart';
import 'sims.dart';

const _nRed = Color(0xFFD9473F), _sBlue = Color(0xFF3F6FD9), _copper = Color(0xFFC07A35), _wire = Color(0xFF5A5148);
const mu0 = 4 * math.pi * 1e-7, kC = 8.99e9, cLight = 2.998e8, hPl = 6.626e-34, eCh = 1.602e-19;

/// a bar magnet drawn from [a] (S end) to [b] (N end)
void magnetBar(Canvas c, Offset s, Offset n, double thick) {
  final m = (s + n) / 2, d = n - s, u = d / d.distance, w = Offset(-u.dy, u.dx) * (thick / 2);
  c.drawPath(Path()..addPolygon([s + w, m + w, m - w, s - w], true), fi(_sBlue));
  c.drawPath(Path()..addPolygon([m + w, n + w, n - w, m - w], true), fi(_nRed));
  tx(c, 'S', s + u * (thick * .55), const Color(0xFFFFFFFF), size: 14, ax: .5, ay: .5, w: FontWeight.w900);
  tx(c, 'N', n - u * (thick * .55), const Color(0xFFFFFFFF), size: 14, ax: .5, ay: .5, w: FontWeight.w900);
}

/// compass needle at [o] pointing along [dir] (red = north-seeking end)
void needle(Canvas c, Offset o, Offset dir, double len) {
  final m = dir.distance;
  if (m == 0) return;
  final u = dir / m * (len / 2), n = Offset(-u.dy, u.dx) * .28;
  c.drawPath(Path()..addPolygon([o + u, o + n, o - n], true), fi(_nRed));
  c.drawPath(Path()..addPolygon([o - u, o + n, o - n], true), fi(const Color(0xFF8D99A6)));
}

/// current symbol: dot (out of the page) or cross (into)
void currentSym(Canvas c, Offset o, double r, bool out, Palette p) {
  c.drawCircle(o, r, fi(p.surface));
  c.drawCircle(o, r, sk(_copper, 3));
  if (out) {
    c.drawCircle(o, r * .28, fi(p.ink));
  } else {
    final k = r * .55;
    c.drawLine(o + Offset(-k, -k), o + Offset(k, k), sk(p.ink, 2.5));
    c.drawLine(o + Offset(k, -k), o + Offset(-k, k), sk(p.ink, 2.5));
  }
}

/// streamlines of a 2-D vector field from [starts]
List<List<Offset>> traceVec(Offset Function(Offset) f, List<Offset> starts, Rect bounds, {double step = 4, int max = 400, bool Function(Offset)? stop}) {
  final out = <List<Offset>>[];
  for (final s0 in starts) {
    var x = s0;
    final line = [x];
    for (var k = 0; k < max; k++) {
      final e = f(x), m = e.distance;
      if (m < 1e-9) break;
      final mid = x + e / m * (step / 2), e2 = f(mid), m2 = e2.distance;
      if (m2 < 1e-9) break;
      x = x + e2 / m2 * step;
      line.add(x);
      if (!bounds.contains(x) || (stop?.call(x) ?? false)) break;
    }
    out.add(line);
  }
  return out;
}

void _lineHeads(Canvas c, List<Offset> l, Color col, {double at = .5}) {
  if (l.length < 6) return;
  final i = (l.length * at).floor().clamp(1, l.length - 2);
  midHead(c, l[i - 1], l[i + 1], col, 8);
}

String _si(double v, String unit) {
  final a = v.abs();
  if (a == 0) return '0 $unit';
  if (a >= 1) return '${sci(v)} $unit';
  if (a >= 1e-3) return '${(v * 1e3).toStringAsFixed(a >= 1e-2 ? 1 : 2)} m$unit';
  if (a >= 1e-6) return '${(v * 1e6).toStringAsFixed(a >= 1e-5 ? 1 : 2)} µ$unit';
  return '${sci(v)} $unit';
}

final Map<String, SimSpec Function(Map<String, dynamic>)> emLabs = {
  'bar_magnet': (_) {
    var sig = '';
    var lines = <List<Offset>>[];
    var poles = <(Offset, double)>[];
    return LabSpec(
      height: 270,
      opts: const [
        Opt('setup', ['One magnet', 'N facing S', 'N facing N']),
        Opt('view', ['Field lines', 'Compasses']),
      ],
      sliders: [Sl('gap', 'Gap between the magnets', 2, 10, 5, unit: 'cm', when: (v) => v['setup'] != 0)],
      formula: 'field lines leave N, enter S and never cross',
      tryThis:
          'Put N facing N: the lines push apart and there is a neutral point (no field) in the gap. N facing S: the lines join across the gap, so the magnets attract.',
      read: (v, t) => [
        (
          '',
          switch (v['setup']!.round()) {
            0 => 'strongest field (closest lines) at the poles',
            1 => 'unlike poles attract: lines run across the gap',
            _ => 'like poles repel: neutral point X in the gap',
          },
        ),
      ],
      draw: (c, s, v, t, p) {
        final setup = v['setup']!.round(), cy = s.height / 2, ml = math.min(s.width * .3, 110.0), th = 26.0, gap = v['gap']! * 9;
        final k = '$setup|${v['gap']}|${s.width}|${s.height}';
        if (k != sig) {
          sig = k;
          if (setup == 0) {
            poles = [(Offset(s.width / 2 + ml / 2 - 8, cy), 1), (Offset(s.width / 2 - ml / 2 + 8, cy), -1)];
          } else {
            final a = s.width / 2 - gap / 2, b = s.width / 2 + gap / 2;
            poles = [
              (Offset(a - 8, cy), 1),
              (Offset(a - ml + 8, cy), -1),
              if (setup == 1) ...[(Offset(b + 8, cy), -1), (Offset(b + ml - 8, cy), 1)] else ...[(Offset(b + 8, cy), 1), (Offset(b + ml - 8, cy), -1)],
            ];
          }
          lines = traceField(poles, Offset.zero & s, perUnit: 14, stepLen: 4, maxSteps: 420);
        }
        if (v['view'] == 0) {
          for (final l in lines) {
            polyline(c, l, sk(p.ink2, 1.3));
            _lineHeads(c, l, p.ink2, at: .3);
          }
        } else {
          for (var y = 18.0; y < s.height; y += 30) {
            for (var x = 16.0; x < s.width; x += 30) {
              final q = Offset(x, y);
              if ((q.dy - cy).abs() < th && poles.any((pp) => (pp.$1.dx - q.dx).abs() < ml * .55 + 10 && (q.dy - cy).abs() < th)) continue;
              var e = Offset.zero;
              for (final (o, m) in poles) {
                final d = q - o, r2 = d.distanceSquared + 30;
                e += d * (m / (r2 * math.sqrt(r2)));
              }
              needle(c, q, e, 20);
            }
          }
        }
        if (setup == 0) {
          magnetBar(c, Offset(s.width / 2 - ml / 2, cy), Offset(s.width / 2 + ml / 2, cy), th);
        } else {
          final a = s.width / 2 - gap / 2, b = s.width / 2 + gap / 2;
          magnetBar(c, Offset(a - ml, cy), Offset(a, cy), th);
          setup == 1 ? magnetBar(c, Offset(b, cy), Offset(b + ml, cy), th) : magnetBar(c, Offset(b + ml, cy), Offset(b, cy), th);
          if (setup == 2) tx(c, 'X', Offset(s.width / 2, cy), p.peach.deep, size: 15, ax: .5, ay: .5, w: FontWeight.w900);
        }
      },
    );
  },
  'wire_field': (_) => LabSpec(
    height: 270,
    opts: const [
      Opt('kind', ['Straight wire', 'Circular loop']),
      Opt('dir', ['Current out of page ⊙', 'Into page ⊗']),
    ],
    sliders: [
      const Sl('I', 'Current I', 1, 20, 5, unit: 'A'),
      Sl('r', 'Compass distance r', 1, 10, 3, unit: 'cm', when: (v) => v['kind'] == 0),
      Sl('N', 'Turns N', 1, 100, 10, when: (v) => v['kind'] == 1),
      Sl('R', 'Loop radius R', 2, 10, 5, unit: 'cm', when: (v) => v['kind'] == 1),
    ],
    pan: true,
    drag: (v, at, s) {
      if (v['kind'] != 0) return;
      final o = Offset(s.width / 2, s.height / 2), d = at - o, sc = math.min(s.width, s.height) / 2 / 11;
      v['r'] = (d.distance / sc).roundToDouble().clamp(1, 10);
      v['phi'] = math.atan2(d.dy, d.dx);
    },
    formulaOf: (v) => v['kind'] == 0 ? 'B = μ₀I / (2πr)    (μ₀ = 4π × 10⁻⁷ T m/A)' : 'B at the centre = μ₀NI / (2R)',
    tryThis:
        'Right-hand grip rule: thumb along the current, fingers curl the way the field goes. Reverse the current and every compass turns round. Double r and B halves.',
    read: (v, t) {
      final I = v['I']!;
      if (v['kind'] == 1) {
        final b = mu0 * v['N']! * I / (2 * v['R']! / 100);
        return [('B centre', _si(b, 'T')), ('compared with Earth (≈ 40 µT)', '${fx(b / 40e-6)} ×')];
      }
      final b = mu0 * I / (2 * math.pi * v['r']! / 100);
      return [('B at r', _si(b, 'T')), ('compared with Earth (≈ 40 µT)', '${fx(b / 40e-6)} ×'), ('field', v['dir'] == 0 ? 'anticlockwise' : 'clockwise')];
    },
    draw: (c, s, v, t, p) {
      final o = Offset(s.width / 2, s.height / 2), out = v['dir'] == 0;
      if (v['kind'] == 1) {
        // loop seen edge-on: top wire and bottom wire carry opposite currents
        final a = math.min(s.height * .28, v['R']! * 9 + 20);
        final top = o - Offset(0, a), bot = o + Offset(0, a);
        for (final eta in [.35, .6, .9, 1.3, 1.8]) {
          final rr = a / _sinh(eta), cy = a * _coth(eta);
          for (final sg in [-1.0, 1.0]) {
            final cc = o + Offset(0, sg * cy);
            c.drawCircle(cc, rr, sk(p.ink2, 1.2));
            // direction: around the top wire anticlockwise if it carries current out of the page
            final cw = (sg < 0) != out;
            final q = cc + Offset(rr, 0);
            midHead(c, q + Offset(0, cw ? -4 : 4), q - Offset(0, cw ? -4 : 4), p.ink2, 7);
          }
        }
        c.drawLine(Offset(8, o.dy), Offset(s.width - 8, o.dy), sk(p.ink2, 1.2));
        final right = out;
        midHead(c, Offset(right ? o.dx - 6 : o.dx + 6, o.dy), Offset(right ? o.dx + 6 : o.dx - 6, o.dy), p.peach.deep, 10);
        c.drawLine(top, bot, sk(_copper.withValues(alpha: .35), 2));
        currentSym(c, top, 11, out, p);
        currentSym(c, bot, 11, !out, p);
        tx(c, right ? 'N face →' : '← N face', Offset(right ? s.width - 8 : 8, o.dy + 8), _nRed, size: 12, ax: right ? 1 : 0);
        tx(c, 'loop seen edge-on', const Offset(8, 8), p.ink2, size: 11);
        return;
      }
      final sc = math.min(s.width, s.height) / 2 / 11;
      for (final r in [1.0, 2.0, 3.5, 5.5, 8.0, 11.0]) {
        c.drawCircle(o, r * sc, sk(p.ink2.withValues(alpha: .6), 1.1));
        for (final ph in [0.0, math.pi / 2, math.pi, 3 * math.pi / 2]) {
          final q = o + Offset(math.cos(ph), math.sin(ph)) * (r * sc), tg = Offset(math.sin(ph), -math.cos(ph)) * (out ? 1 : -1);
          if (r > 1.5) midHead(c, q - tg * 4, q + tg * 4, p.ink2, 6);
        }
      }
      currentSym(c, o, 12, out, p);
      final ph = v['phi'] ?? -.6, r = v['r']!, q = o + Offset(math.cos(ph), math.sin(ph)) * (r * sc);
      final tg = Offset(math.sin(ph), -math.cos(ph)) * (out ? 1 : -1);
      c.drawCircle(q, 14, fi(p.surface));
      c.drawCircle(q, 14, sk(p.ink, 1.5));
      needle(c, q, tg, 24);
      dsh(c, o, q, p.peach.deep, 1.2, 4);
      tx(c, 'r', (o + q) / 2 + const Offset(4, -14), p.peach.deep, size: 12);
      tx(c, 'drag the compass', const Offset(8, 8), p.ink2, size: 11);
    },
  ),
  'solenoid': (_) => LabSpec(
    height: 250,
    opts: const [
      Opt('dir', ['Current one way', 'Reversed']),
      Opt('core', ['Air core', 'Soft-iron core']),
    ],
    sliders: const [
      Sl('N', 'Number of turns N', 50, 1000, 300, step: 50),
      Sl('L', 'Length L', .1, 1, .3, step: .05, unit: 'm'),
      Sl('I', 'Current I', .5, 5, 2, step: .5, unit: 'A'),
    ],
    formula: 'B = μ₀ n I = μ₀ N I / L   (inside a long solenoid)',
    tryThis:
        'Double the turns or the current and B doubles; stretch the coil to twice the length and B halves. Look at an end: anticlockwise current makes that end a N pole.',
    read: (v, t) {
      final b0 = mu0 * v['N']! * v['I']! / v['L']!, iron = v['core'] == 1, b = iron ? math.min(b0 * 1000, 2.0) : b0;
      return [
        ('n = N/L', '${fx(v['N']! / v['L']!, 0)} turns/m'),
        ('B inside', _si(b, 'T')),
        if (iron) ('', b0 * 1000 > 2 ? 'iron saturates near 2 T' : 'iron (μr ≈ 1000) multiplies B'),
        ('left end is', v['dir'] == 0 ? 'N' : 'S'),
      ];
    },
    draw: (c, s, v, t, p) {
      final cy = s.height / 2, len = (s.width - 120) * (.35 + .65 * (v['L']! - .1) / .9), x0 = s.width / 2 - len / 2, x1 = s.width / 2 + len / 2, R = 34.0;
      final turns = (v['N']! / 50).round().clamp(4, 20), up = v['dir'] == 0;
      if (v['core'] == 1) c.drawRect(Rect.fromLTRB(x0 - 6, cy - R * .55, x1 + 6, cy + R * .55), fi(const Color(0xFFA9A39B)));
      // field: inside parallel, outside loops from N to S
      final nLeft = up, lc = p.ink2;
      for (final y in [-14.0, 0.0, 14.0]) {
        c.drawLine(Offset(x0 - 10, cy + y), Offset(x1 + 10, cy + y), sk(lc, 1.2));
        midHead(c, Offset(s.width / 2 + (nLeft ? 6 : -6), cy + y), Offset(s.width / 2 + (nLeft ? -6 : 6), cy + y), lc, 7);
      }
      for (final k in [1.0, 1.7]) {
        for (final sg in [-1.0, 1.0]) {
          final path = Path()
            ..moveTo(x0 - 10, cy + sg * 7 * k)
            ..cubicTo(x0 - 60 * k, cy + sg * 60 * k, x1 + 60 * k, cy + sg * 60 * k, x1 + 10, cy + sg * 7 * k);
          c.drawPath(path, sk(lc, 1.2));
          final top = Offset(s.width / 2, cy + sg * 45 * k);
          midHead(c, top + Offset(nLeft ? 6 : -6, 0), top + Offset(nLeft ? -6 : 6, 0), lc, 7);
        }
      }
      // coil: back halves light, front halves copper with current arrows
      final dx = len / turns;
      for (var i = 0; i < turns; i++) {
        final x = x0 + dx * (i + .5);
        c.drawLine(Offset(x - dx * .3, cy - R), Offset(x + dx * .2, cy + R), sk(_copper.withValues(alpha: .35), 2.5));
      }
      for (var i = 0; i < turns; i++) {
        final x = x0 + dx * (i + .5);
        c.drawLine(Offset(x + dx * .2, cy + R), Offset(x + dx * .7, cy - R), sk(_copper, 3));
        if (i % 3 == 1) midHead(c, Offset(x + dx * .45, cy + (up ? 6 : -6)), Offset(x + dx * .45, cy + (up ? -6 : 6)), _nRed, 8);
      }
      tx(c, nLeft ? 'N' : 'S', Offset(x0 - 26, cy), nLeft ? _nRed : _sBlue, size: 18, ax: .5, ay: .5, w: FontWeight.w900);
      tx(c, nLeft ? 'S' : 'N', Offset(x1 + 26, cy), nLeft ? _sBlue : _nRed, size: 18, ax: .5, ay: .5, w: FontWeight.w900);
      tx(c, 'red arrows: current on the front of the coil', Offset(8, s.height - 18), p.ink2, size: 11);
    },
  ),
  'force_on_wire': (_) {
    var sig = '';
    var lines = <List<Offset>>[];
    return LabSpec(
      height: 270,
      sliders: const [
        Sl('B', 'Magnetic field B', .1, 1, .5, step: .05, unit: 'T'),
        Sl('I', 'Current I (− = into page)', -10, 10, 5, unit: 'A'),
        Sl('L', 'Length of wire in the field', .05, .5, .2, step: .05, unit: 'm'),
        Sl('th', 'Angle between wire and field θ', 0, 90, 90, step: 5, unit: '°'),
      ],
      formula: 'F = B I L sin θ   (Fleming’s left-hand rule)',
      tryThis: 'Reverse the current: the wire is pushed the other way. Turn the wire until it is parallel to the field (θ = 0°): the force disappears.',
      read: (v, t) {
        final f = v['B']! * v['I']!.abs() * v['L']! * math.sin(v['th']! * deg);
        return [('F', '${fx(f, 3)} N'), ('direction', v['I'] == 0 || f == 0 ? 'no force' : (v['I']! > 0 ? 'up' : 'down'))];
      },
      draw: (c, s, v, t, p) {
        final cy = s.height / 2, o = Offset(s.width / 2, cy), I = v['I']!, b = v['B']!, st = I * math.sin(v['th']! * deg);
        c.drawRect(Rect.fromLTWH(0, cy - 70, 34, 140), fi(_nRed));
        c.drawRect(Rect.fromLTWH(s.width - 34, cy - 70, 34, 140), fi(_sBlue));
        tx(c, 'N', Offset(17, cy), const Color(0xFFFFFFFF), size: 18, ax: .5, ay: .5, w: FontWeight.w900);
        tx(c, 'S', Offset(s.width - 17, cy), const Color(0xFFFFFFFF), size: 18, ax: .5, ay: .5, w: FontWeight.w900);
        final k = '${v['B']}|${v['I']}|${v['th']}|${s.width}';
        if (k != sig) {
          sig = k;
          // uniform field + circular field of the wire (catapult field)
          final kw = st * 26;
          Offset f(Offset x) {
            final d = x - o, r2 = math.max(d.distanceSquared, 120);
            return Offset(b * 10, 0) + Offset(-d.dy, d.dx) * (-kw / r2);
          }

          final starts = [for (var y = cy - 66; y <= cy + 66; y += 12) Offset(36, y)];
          lines = traceVec(f, starts, Rect.fromLTRB(34, cy - 90, s.width - 34, cy + 90), step: 4, max: 300, stop: (x) => (x - o).distance < 14);
        }
        for (final l in lines) {
          polyline(c, l, sk(p.ink2, 1.2));
          _lineHeads(c, l, p.ink2, at: .2);
        }
        currentSym(c, o, 14, I >= 0, p);
        final f = b * I.abs() * v['L']! * math.sin(v['th']! * deg);
        if (f > 0) arw(c, o + Offset(0, I > 0 ? -18 : 18), o + Offset(0, (I > 0 ? -1 : 1) * (24 + 60 * f / 5).clamp(24, 100)), p.peach.deep, 4, 12);
        if (f > 0) tx(c, 'F', o + Offset(10, I > 0 ? -60 : 50), p.peach.deep, size: 14);
        // inset: top view of the wire at angle θ to B
        final ib = Rect.fromLTWH(44, 8, 74, 54);
        c.drawRRect(RRect.fromRectAndRadius(ib, const Radius.circular(8)), fi(p.surface));
        arw(c, ib.centerLeft + const Offset(6, 18), ib.centerRight + const Offset(-6, 18), p.ink2, 1.5, 6);
        final a = v['th']! * deg, cc = ib.center - const Offset(0, 4);
        c.drawLine(cc - Offset(math.cos(a), -math.sin(a)) * 22, cc + Offset(math.cos(a), -math.sin(a)) * 22, sk(_copper, 3));
        tx(c, 'θ ${v['th']!.round()}°', ib.topLeft + const Offset(4, 2), p.ink, size: 10.5);
        tx(c, 'B', ib.bottomRight + const Offset(-12, -14), p.ink2, size: 10.5);
      },
    );
  },
  'induction': (_) {
    final hist = List<double>.filled(150, 0);
    var hi = 0, emf = 0.0, prevD = 9.0, dSm = 0.0, flux = 0.0;
    const a = .03, phi0 = 2e-4; // coil radius scale (m), flux per turn with the magnet at the coil (Wb)
    double phiAt(double dcm) => phi0 / math.pow(1 + math.pow(dcm / 100 / a, 2), 1.5);
    double posAt(V v, double t) => v['mode'] == 0 ? 6.5 + 5.5 * math.cos(2 * math.pi * v['f']! * t) : (v['d'] ?? 9.0);
    return LabSpec(
      height: 290,
      anim: true,
      live: true,
      playOnDrag: true,
      opts: const [
        Opt('mode', ['Push and pull', 'Drag the magnet']),
        Opt('pole', ['N end first', 'S end first']),
      ],
      sliders: [
        const Sl('N', 'Turns on the coil N', 50, 500, 200, step: 50),
        Sl('f', 'Push–pull rate', .2, 2, .6, step: .2, unit: 'Hz', when: (v) => v['mode'] == 0),
      ],
      formula: 'ε = −N ΔΦ/Δt   (Faraday)    the current opposes the motion (Lenz)',
      tryThis:
          'Hold the magnet still: no current. Move it faster or use more turns: the meter swings further. Pulling out gives the opposite current to pushing in.',
      drag: (v, at, s) {
        if (v['mode'] != 1) return;
        final x0m = s.width * .3 + 46;
        v['d'] = ((at.dx - 30 - x0m) / (s.width - x0m - 90) * 12).clamp(.5, 12.0);
      },
      reset: (v) {
        hist.fillRange(0, hist.length, 0);
        emf = 0;
        dSm = 0;
        prevD = posAt(v, 0);
      },
      step: (dt, v) {
        // time is advanced by the view; recover the position history from the current state
        final d = v['mode'] == 0 ? prevD : (v['d'] ?? 9.0);
        if (v['mode'] == 0) return;
        final vel = (d - prevD) / 100 / dt; // m/s
        dSm = dSm * .6 + vel * .4;
        prevD = d;
        final dphi = (phiAt(d + .01) - phiAt(d - .01)) / (.02 / 100);
        emf = -v['N']! * dphi * dSm * (v['pole'] == 0 ? 1 : -1);
        flux = phiAt(d);
        hist[hi] = emf;
        hi = (hi + 1) % hist.length;
      },
      read: (v, t) {
        final d = posAt(v, t);
        double e = emf;
        if (v['mode'] == 0) {
          final vel = -5.5 * 2 * math.pi * v['f']! * math.sin(2 * math.pi * v['f']! * t) / 100;
          e = -v['N']! * (phiAt(d + .01) - phiAt(d - .01)) / (.02 / 100) * vel * (v['pole'] == 0 ? 1 : -1);
        }
        return [('EMF ε', '${fx(e * 1000, 0)} mV'), ('flux per turn Φ', _si(v['mode'] == 0 ? phiAt(d) : flux, 'Wb'))];
      },
      draw: (c, s, v, t, p) {
        final N = v['N']!, sign = v['pole'] == 0 ? 1.0 : -1.0;
        final d = posAt(v, t);
        double e;
        if (v['mode'] == 0) {
          final w = 2 * math.pi * v['f']!, vel = -5.5 * w * math.sin(w * t) / 100;
          e = -N * (phiAt(d + .01) - phiAt(d - .01)) / (.02 / 100) * vel * sign;
        } else {
          e = emf;
        }
        final cy = s.height * .32, cx = s.width * .3, R = 30.0;
        // coil (axis horizontal), face nearest the magnet on the right
        final turns = (N / 50).round() + 2;
        for (var i = 0; i < turns; i++) {
          final x = cx - 40 + 80 * i / (turns - 1);
          c.drawOval(Rect.fromCenter(center: Offset(x, cy), width: 16, height: 2 * R), sk(_copper, 2.2));
        }
        // magnet to the right, approaching end = N (or S)
        const ml = 84.0;
        final x0m = cx + 46, mx = x0m + d / 12 * (s.width - x0m - ml - 6);
        sign > 0 ? magnetBar(c, Offset(mx + ml, cy), Offset(mx, cy), 24) : magnetBar(c, Offset(mx, cy), Offset(mx + ml, cy), 24);
        // Lenz: face of the coil nearest the magnet
        if (e.abs() > 2e-4) {
          final approaching = (e * sign) < 0;
          final faceN = approaching == (sign > 0);
          tx(c, faceN ? 'N' : 'S', Offset(cx + 54, cy - R - 16), faceN ? _nRed : _sBlue, size: 16, ax: .5, w: FontWeight.w900);
          tx(c, 'induced', Offset(cx + 54, cy - R - 30), p.ink2, size: 10.5, ax: .5);
        }
        // galvanometer
        final g = Offset(cx, s.height * .64), gr = 30.0;
        c.drawLine(Offset(cx - 40, cy + R), Offset(cx - 40, g.dy), sk(_wire, 2));
        c.drawLine(Offset(cx + 40, cy + R), Offset(cx + 40, g.dy), sk(_wire, 2));
        c.drawCircle(g, gr, fi(p.surface));
        c.drawCircle(g, gr, sk(p.ink, 2));
        c.drawArc(Rect.fromCircle(center: g, radius: gr - 7), -math.pi * .85, math.pi * .7, false, sk(p.ink2, 1));
        final ang = -math.pi / 2 + (e / .5).clamp(-1.0, 1.0) * math.pi * .35;
        c.drawLine(g, g + Offset(math.cos(ang), math.sin(ang)) * (gr - 6), sk(_nRed, 2.5));
        tx(c, '0', g + Offset(0, -gr + 6), p.ink2, size: 9.5, ax: .5);
        tx(c, 'G', g + const Offset(0, 8), p.ink, size: 12, ax: .5);
        // EMF trace
        final gx = s.width * .56, gw = s.width - gx - 8, gy = s.height * .64, gh = s.height * .3;
        c.drawRect(Rect.fromLTWH(gx, gy - gh / 2, gw, gh), fi(p.surface));
        c.drawLine(Offset(gx, gy), Offset(gx + gw, gy), sk(p.line, 1));
        final path = Path();
        if (v['mode'] == 0) {
          final w = 2 * math.pi * v['f']!;
          for (var i = 0; i <= 80; i++) {
            final tt = t - 3 + 3 * i / 80, dd = 6.5 + 5.5 * math.cos(w * tt), vel = -5.5 * w * math.sin(w * tt) / 100;
            final ee = -N * (phiAt(dd + .01) - phiAt(dd - .01)) / (.02 / 100) * vel * sign;
            final q = Offset(gx + gw * i / 80, gy - (ee / .5).clamp(-1.0, 1.0) * gh * .45);
            i == 0 ? path.moveTo(q.dx, q.dy) : path.lineTo(q.dx, q.dy);
          }
        } else {
          for (var i = 0; i < hist.length; i++) {
            final ee = hist[(hi + i) % hist.length], q = Offset(gx + gw * i / (hist.length - 1), gy - (ee / .5).clamp(-1.0, 1.0) * gh * .45);
            i == 0 ? path.moveTo(q.dx, q.dy) : path.lineTo(q.dx, q.dy);
          }
        }
        c.drawPath(path, sk(p.peach.deep, 2));
        tx(c, 'EMF vs time', Offset(gx + 4, gy - gh / 2 + 2), p.ink2, size: 10.5);
        if (v['mode'] == 1) tx(c, 'drag the magnet sideways', const Offset(8, 8), p.ink2, size: 11);
      },
    );
  },
  'generator': (_) => LabSpec(
    height: 290,
    anim: true,
    live: true,
    t0: .3,
    opts: const [
      Opt('dev', ['AC generator', 'DC motor']),
    ],
    sliders: [
      Sl('f', 'Turns per second', .2, 2, .5, step: .1, unit: 'Hz', when: (v) => v['dev'] == 0),
      const Sl('N', 'Turns on the coil N', 10, 200, 50, step: 10),
      const Sl('B', 'Magnetic field B', .1, 1, .4, step: .05, unit: 'T'),
      Sl('I', 'Current I', .5, 5, 2, step: .5, unit: 'A', when: (v) => v['dev'] == 1),
    ],
    formulaOf: (v) => v['dev'] == 0
        ? 'ε = N B A ω sin ωt,   peak ε₀ = N B A ω   (A = 0.01 m², ω = 2πf)'
        : 'torque τ = N B I A sin θ;  the split ring reverses the current every half turn',
    tryThis:
        'Generator: double the speed and both the peak EMF and the frequency double. The EMF is largest when the coil sides cut straight across the field (coil plane along B).',
    read: (v, t) {
      const A = .01;
      if (v['dev'] == 1) {
        final tq = v['N']! * v['B']! * v['I']! * A;
        return [('τ max = NBIA', '${fx(tq, 3)} N m')];
      }
      final w = 2 * math.pi * v['f']!, e0 = v['N']! * v['B']! * A * w;
      return [('ε now', '${fx(e0 * math.sin(w * t), 2)} V'), ('peak ε₀', '${fx(e0, 2)} V'), ('frequency', '${fx(v['f']!, 1)} Hz')];
    },
    draw: (c, s, v, t, p) {
      final motor = v['dev'] == 1;
      final w = motor ? 2 * math.pi * (.15 + .15 * v['B']! * v['I']!) : 2 * math.pi * v['f']!;
      final th = w * t, cy = s.height * .3, cx = s.width / 2, W = math.min(s.width * .32, 120.0), H = s.height * .32;
      c.drawRect(Rect.fromLTRB(8, cy - H * .7, cx - W * .62 - 8, cy + H * .7), fi(_nRed));
      c.drawRect(Rect.fromLTRB(cx + W * .62 + 8, cy - H * .7, s.width - 8, cy + H * .7), fi(_sBlue));
      tx(c, 'N', Offset((8 + cx - W * .62 - 8) / 2, cy), const Color(0xFFFFFFFF), size: 18, ax: .5, ay: .5, w: FontWeight.w900);
      tx(c, 'S', Offset((cx + W * .62 + 8 + s.width - 8) / 2, cy), const Color(0xFFFFFFFF), size: 18, ax: .5, ay: .5, w: FontWeight.w900);
      for (final y in [-.45, 0.0, .45]) {
        c.drawLine(Offset(cx - W * .62 - 6, cy + y * H), Offset(cx + W * .62 + 6, cy + y * H), sk(p.ink2.withValues(alpha: .45), 1));
      }
      // coil rotating about a vertical axis: sides at x = ±(W/2)·sin θ, depth ±cos θ
      final sx = W / 2 * math.sin(th), front = math.cos(th) >= 0;
      final a = Offset(cx - sx, cy - H / 2), b = Offset(cx + sx, cy - H / 2), cc = Offset(cx + sx, cy + H / 2), d = Offset(cx - sx, cy + H / 2);
      c.drawPath(Path()..addPolygon([a, b, cc, d], true), fi(_copper.withValues(alpha: .12)));
      c.drawLine(a, d, sk(_copper, front ? 4 : 2.5));
      c.drawLine(b, cc, sk(_copper, front ? 2.5 : 4));
      c.drawLine(a, b, sk(_copper, 3));
      c.drawLine(d, Offset(cx - 3, cy + H / 2), sk(_copper, 3));
      c.drawLine(cc, Offset(cx + 3, cy + H / 2), sk(_copper, 3));
      // rings / commutator and brushes on the axle
      final ry = cy + H / 2 + 16;
      c.drawLine(Offset(cx, cy + H / 2), Offset(cx, ry + 22), sk(p.ink2, 3));
      if (motor) {
        final flip = math.sin(th) >= 0;
        c.drawArc(Rect.fromCenter(center: Offset(cx, ry + 6), width: 30, height: 12), 0, math.pi, false, sk(flip ? _nRed : _sBlue, 5));
        c.drawArc(Rect.fromCenter(center: Offset(cx, ry + 6), width: 30, height: 12), math.pi, math.pi, false, sk(flip ? _sBlue : _nRed, 5));
      } else {
        c.drawOval(Rect.fromCenter(center: Offset(cx, ry), width: 30, height: 10), sk(_copper, 3));
        c.drawOval(Rect.fromCenter(center: Offset(cx, ry + 12), width: 30, height: 10), sk(_copper, 3));
      }
      c.drawRect(Rect.fromLTWH(cx - 26, ry - 2, 10, 16), fi(p.ink2));
      c.drawRect(Rect.fromLTWH(cx + 16, ry + 2, 10, 16), fi(p.ink2));
      tx(c, motor ? 'split-ring commutator' : 'slip rings', Offset(cx + 32, ry), p.ink2, size: 10.5);
      // inset: top view (coil edge, B left → right, forces / velocities)
      final ib = Rect.fromLTWH(8, s.height * .62 - 4, 84, 84), ic = ib.center;
      c.drawRRect(RRect.fromRectAndRadius(ib, const Radius.circular(8)), fi(p.surface));
      for (final y in [-24.0, 0.0, 24.0]) {
        arw(c, ic + Offset(-38, y), ic + Offset(38, y), p.line, 1, 5);
      }
      final ed = Offset(-math.sin(th), math.cos(th)) * 30;
      c.drawLine(ic - ed, ic + ed, sk(_copper, 4));
      if (motor) {
        final sg = math.sin(th) >= 0 ? 1.0 : -1.0;
        arw(c, ic + ed, ic + ed + Offset(0, -20 * sg), p.peach.deep, 2, 6);
        arw(c, ic - ed, ic - ed + Offset(0, 20 * sg), p.peach.deep, 2, 6);
      }
      tx(c, 'top view', ib.topLeft + const Offset(4, 2), p.ink2, size: 10);
      // graph of EMF (generator) or torque (motor) over the last 2 s
      final gx = ib.right + 10, gw = s.width - gx - 8, gy = ib.center.dy, gh = 80.0;
      c.drawRect(Rect.fromLTWH(gx, gy - gh / 2, gw, gh), fi(p.surface));
      c.drawLine(Offset(gx, gy), Offset(gx + gw, gy), sk(p.line, 1));
      final path = Path();
      for (var i = 0; i <= 100; i++) {
        final tt = t - 2 + 2 * i / 100, y = motor ? math.sin(w * tt).abs() : math.sin(w * tt);
        final q = Offset(gx + gw * i / 100, gy - y * gh * .42);
        i == 0 ? path.moveTo(q.dx, q.dy) : path.lineTo(q.dx, q.dy);
      }
      c.drawPath(path, sk(p.peach.deep, 2));
      c.drawCircle(Offset(gx + gw, gy - (motor ? math.sin(th).abs() : math.sin(th)) * gh * .42), 4, fi(p.peach.deep));
      tx(c, motor ? 'torque (always one way)' : 'EMF (alternating)', Offset(gx + 4, gy - gh / 2 + 2), p.ink2, size: 10.5);
    },
  ),
  'transformer': (_) => LabSpec(
    height: 250,
    opts: const [
      Opt('ac', ['AC supply', 'DC battery']),
    ],
    sliders: const [
      Sl('Np', 'Primary turns Np', 10, 1000, 200, step: 10),
      Sl('Ns', 'Secondary turns Ns', 10, 1000, 50, step: 10),
      Sl('Vp', 'Primary voltage Vp', 10, 240, 240, step: 10, unit: 'V'),
      Sl('R', 'Load resistance', 10, 1000, 100, step: 10, unit: 'Ω'),
    ],
    formula: 'Vs / Vp = Ns / Np;    ideal: Vp Ip = Vs Is',
    tryThis:
        'Make Ns bigger than Np for a step-up transformer: the voltage goes up but the current goes down by the same factor. Switch to DC: the flux does not change, so nothing is induced.',
    read: (v, t) {
      if (v['ac'] == 1) return [('Vs', '0 V'), ('', 'steady current → no changing flux → no induced EMF')];
      final vs = v['Vp']! * v['Ns']! / v['Np']!, is_ = vs / v['R']!, ip = is_ * v['Ns']! / v['Np']!;
      return [
        ('Vs', '${fx(vs)} V'),
        ('Is = Vs/R', '${fx(is_, 3)} A'),
        ('Ip', '${fx(ip, 3)} A'),
        ('P', '${fx(vs * is_)} W in = out'),
        ('', v['Ns']! > v['Np']! ? 'step-up' : (v['Ns']! < v['Np']! ? 'step-down' : '1 : 1')),
      ];
    },
    draw: (c, s, v, t, p) {
      final cx = s.width / 2, cy = s.height / 2 - 6, W = math.min(s.width * .44, 170.0), H = s.height * .62;
      final core = Rect.fromCenter(center: Offset(cx, cy), width: W, height: H);
      c.drawRect(core, sk(const Color(0xFF9A948C), 18));
      void coil(double x, double n, Color col) {
        final k = math.sqrt(n).clamp(2.0, 30.0).round(), top = cy - H * .36, bot = cy + H * .36;
        for (var i = 0; i < k; i++) {
          final y = top + (bot - top) * i / math.max(1, k - 1);
          c.drawLine(Offset(x - 16, y + 4), Offset(x + 16, y - 4), sk(col, 2.4));
        }
      }

      coil(core.left, v['Np']!, _copper);
      coil(core.right, v['Ns']!, const Color(0xFF8C5A2B));
      final on = v['ac'] == 0, vs = on ? v['Vp']! * v['Ns']! / v['Np']! : 0.0, ps = vs * vs / v['R']!;
      // supply
      final sp = Offset(core.left - 46, cy);
      c.drawLine(Offset(core.left - 16, cy - H * .36), Offset(sp.dx, cy - H * .36), sk(_wire, 2));
      c.drawLine(Offset(sp.dx, cy - H * .36), Offset(sp.dx, sp.dy - 16), sk(_wire, 2));
      c.drawLine(Offset(core.left - 16, cy + H * .36), Offset(sp.dx, cy + H * .36), sk(_wire, 2));
      c.drawLine(Offset(sp.dx, cy + H * .36), Offset(sp.dx, sp.dy + 16), sk(_wire, 2));
      c.drawCircle(sp, 16, fi(p.surface));
      c.drawCircle(sp, 16, sk(p.ink, 2));
      tx(c, on ? '~' : '=', sp, p.ink, size: 20, ax: .5, ay: .5);
      tx(c, '${v['Vp']!.round()} V', sp + const Offset(0, 22), p.ink, size: 11, ax: .5);
      // load bulb
      final bp = Offset(core.right + 46, cy), glow = (ps / 200).clamp(0.0, 1.0);
      c.drawLine(Offset(core.right + 16, cy - H * .36), Offset(bp.dx, cy - H * .36), sk(_wire, 2));
      c.drawLine(Offset(bp.dx, cy - H * .36), Offset(bp.dx, bp.dy - 15), sk(_wire, 2));
      c.drawLine(Offset(core.right + 16, cy + H * .36), Offset(bp.dx, cy + H * .36), sk(_wire, 2));
      c.drawLine(Offset(bp.dx, cy + H * .36), Offset(bp.dx, bp.dy + 15), sk(_wire, 2));
      if (glow > 0) c.drawCircle(bp, 18 + 14 * glow, fi(Color.fromARGB((110 * glow).round(), 255, 210, 60)));
      c.drawCircle(bp, 15, fi(Color.lerp(p.surface, const Color(0xFFFFD84A), glow)!));
      c.drawCircle(bp, 15, sk(p.ink, 2));
      tx(c, '${fx(vs)} V', bp + const Offset(0, 22), p.ink, size: 11, ax: .5);
      tx(c, 'Np ${v['Np']!.round()}', Offset(core.left, core.bottom + 12), p.ink, size: 11.5, ax: .5);
      tx(c, 'Ns ${v['Ns']!.round()}', Offset(core.right, core.bottom + 12), p.ink, size: 11.5, ax: .5);
      tx(c, 'soft-iron core', Offset(cx, core.top - 24), p.ink2, size: 11, ax: .5);
    },
  ),
  'em_spectrum': (_) => LabSpec(
    height: 230,
    sliders: [Sl('lg', 'Wavelength λ', -12, 3, -6.3, step: .05, fmt: (x) => _lambda(math.pow(10, x).toDouble()))],
    formula: 'c = f λ = 3.00 × 10⁸ m/s;    photon energy E = h f',
    drag: (v, at, s) => v['lg'] = (-12 + 15 * ((at.dx - 12) / (s.width - 24))).clamp(-12.0, 3.0).toDouble(),
    tryThis:
        'All these waves travel at the same speed in a vacuum. Shorter wavelength means higher frequency and more energetic photons: X-rays and gamma rays can ionise atoms; radio waves cannot.',
    read: (v, t) {
      final l = math.pow(10, v['lg']!).toDouble(), f = cLight / l, e = hPl * f / eCh;
      return [('region', _region(l)), ('f = c/λ', '${sci(f)} Hz'), ('E = hf', '${sci(e)} eV'), ('used for', _uses(l))];
    },
    draw: (c, s, v, t, p) {
      final x0 = 12.0, x1 = s.width - 12, by = 40.0, bh = 44.0;
      double xOf(double lg) => x0 + (x1 - x0) * (lg + 12) / 15;
      const regions = [
        (-12.0, -11.0, 'γ', Color(0xFFB9A4D9)),
        (-11.0, -8.0, 'X-ray', Color(0xFFA9B9E3)),
        (-8.0, -6.42, 'UV', Color(0xFFC6B3EE)),
        (-6.42, -6.12, '', Color(0x00000000)),
        (-6.12, -3.0, 'infrared', Color(0xFFEFB8A8)),
        (-3.0, -1.0, 'micro', Color(0xFFF2D49B)),
        (-1.0, 3.0, 'radio', Color(0xFFD9E3A5)),
      ];
      for (final (a, b, name, col) in regions) {
        final r = Rect.fromLTRB(xOf(a), by, xOf(b), by + bh);
        if (name.isEmpty) {
          for (var i = 0; i < 6; i++) {
            final nm = 380 + 370 * i / 5;
            c.drawRect(Rect.fromLTRB(r.left + r.width * i / 6, by, r.left + r.width * (i + 1) / 6 + .5, by + bh), fi(waveColor(nm)));
          }
          tx(c, 'visible', Offset(r.center.dx, by - 18), p.ink, size: 11, ax: .5);
          c.drawLine(Offset(r.center.dx, by - 5), Offset(r.center.dx, by), sk(p.ink, 1));
        } else {
          c.drawRect(r, fi(col));
          tx(c, name, r.center, const Color(0xFF3A3530), size: 11, ax: .5, ay: .5);
        }
      }
      for (var e = -12; e <= 3; e += 3) {
        tx(c, '10${_supN(e)} m', Offset(xOf(e.toDouble()), by + bh + 4), p.ink2, size: 10, ax: .5);
      }
      final px = xOf(v['lg']!);
      c.drawPath(Path()..addPolygon([Offset(px, by + bh - 2), Offset(px - 8, by + bh + 16), Offset(px + 8, by + bh + 16)], true), fi(p.peach.deep));
      c.drawLine(Offset(px, by - 4), Offset(px, by + bh), sk(p.peach.deep, 2.5));
      // a wave whose drawn wavelength grows with λ (not to scale)
      final wy = s.height * .74, lp = 6 * math.pow(1.28, v['lg']! + 12).toDouble(), path = Path();
      final l = math.pow(10, v['lg']!).toDouble();
      final col = l > 3.8e-7 && l < 7.5e-7 ? waveColor(l * 1e9) : p.blue.deep;
      for (var x = 12.0; x <= s.width - 12; x += 1.5) {
        final y = wy - 26 * math.sin(2 * math.pi * (x - 12) / lp);
        x == 12 ? path.moveTo(x, y) : path.lineTo(x, y);
      }
      c.drawPath(path, sk(col, 2.2));
      tx(c, 'drawn wavelength not to scale', Offset(s.width - 10, s.height - 16), p.ink2, size: 10, ax: 1);
      tx(c, 'tap or drag along the spectrum', const Offset(12, 8), p.ink2, size: 11);
    },
  ),
  'em_wave': (_) => LabSpec(
    height: 250,
    anim: true,
    t0: .2,
    opts: const [
      Opt('kind', ['Radio 3 m', 'Microwave 3 cm', 'Green light 530 nm', 'X-ray 0.1 nm']),
    ],
    sliders: const [Sl('E0', 'Electric field amplitude E₀', 10, 100, 60, step: 5, unit: 'V/m')],
    formula: 'E ⟂ B ⟂ direction of travel;   B₀ = E₀ / c;   c = f λ',
    tryThis:
        'E (red, vertical) and B (blue, horizontal) rise and fall together and are always at right angles; every kind of EM wave has this shape, only the wavelength changes.',
    read: (v, t) {
      final l = const [3.0, .03, 530e-9, 1e-10][v['kind']!.round()], f = cLight / l;
      return [('λ', _lambda(l)), ('f = c/λ', '${sci(f)} Hz'), ('B₀ = E₀/c', _si(v['E0']! / cLight, 'T'))];
    },
    draw: (c, s, v, t, p) {
      final o = Offset(24, s.height * .55), len = s.width - 48, lam = len / 2.2, a = v['E0']! / 100 * s.height * .36;
      const sk3 = Offset(.28, -.42); // oblique projection of the horizontal (z) axis
      c.drawLine(o, o + Offset(len, 0), sk(p.ink2, 1.5));
      arw(c, o + Offset(len - 30, 0), o + Offset(len + 4, 0), p.ink2, 1.5, 8);
      tx(c, 'travel', o + Offset(len - 40, 6), p.ink2, size: 10.5);
      final ep = Path(), bp = Path();
      for (var i = 0; i <= 160; i++) {
        final x = len * i / 160, ph = 2 * math.pi * (x / lam - .5 * t), y = math.sin(ph);
        final e = o + Offset(x, -a * y), b = o + Offset(x, 0) + sk3 * (a * .9 * y);
        i == 0 ? ep.moveTo(e.dx, e.dy) : ep.lineTo(e.dx, e.dy);
        i == 0 ? bp.moveTo(b.dx, b.dy) : bp.lineTo(b.dx, b.dy);
        if (i % 8 == 0) {
          c.drawLine(o + Offset(x, 0), e, sk(_nRed.withValues(alpha: .35), 1));
          c.drawLine(o + Offset(x, 0), b, sk(_sBlue.withValues(alpha: .35), 1));
        }
      }
      c.drawPath(bp, sk(_sBlue, 2.5));
      c.drawPath(ep, sk(_nRed, 2.5));
      tx(c, 'E', o + Offset(6, -a - 16), _nRed, size: 14, w: FontWeight.w900);
      tx(c, 'B', o + sk3 * (a * .9) + const Offset(6, -6), _sBlue, size: 14, w: FontWeight.w900);
    },
  ),
  'field_lines': (_) {
    var sig = '';
    var last = const Size(360, 280);
    var lines = <List<Offset>>[];
    return LabSpec(
      height: 280,
      opts: const [
        Opt('setup', ['+ and −', '+ and +', 'Single +']),
      ],
      sliders: [
        const Sl('q1', 'Charge q₁', 1, 5, 2, unit: 'µC'),
        Sl('q2', 'Size of charge q₂', 1, 5, 2, unit: 'µC', when: (v) => v['setup'] != 2),
        Sl('d', 'Separation', 4, 14, 8, unit: 'cm', when: (v) => v['setup'] != 2),
      ],
      pan: true,
      drag: (v, at, s) {
        v['px'] = at.dx;
        v['py'] = at.dy;
      },
      formula: 'E = k q / r²  from each charge, added as vectors   (k = 8.99 × 10⁹ N m²/C²)',
      tryThis:
          'Drag the yellow test point. Lines start on + and end on −; where they are close together the field is strong. With + and + there is a neutral point midway where E = 0.',
      read: (v, t) {
        final e = _eAt(v, last, Offset(v['px'] ?? last.width / 2, v['py'] ?? 60));
        return [('E at test point', '${sci(e.distance)} N/C'), ('', 'line density shows field strength')];
      },
      draw: (c, s, v, t, p) {
        last = s;
        final qs = _charges(v, s);
        final k = '${v['setup']}|${v['q1']}|${v['q2']}|${v['d']}|${s.width}';
        if (k != sig) {
          sig = k;
          lines = traceField([for (final (o, q) in qs) (o, q)], Offset.zero & s, perUnit: 4, stepLen: 4, maxSteps: 450);
        }
        for (final l in lines) {
          polyline(c, l, sk(p.ink2, 1.2));
          _lineHeads(c, l, p.ink2, at: .25);
        }
        for (final (o, q) in qs) {
          c.drawCircle(o, 15, fi(q > 0 ? _nRed : _sBlue));
          tx(c, q > 0 ? '+' : '−', o, const Color(0xFFFFFFFF), size: 20, ax: .5, ay: .5, w: FontWeight.w900);
        }
        final pt = Offset(v['px'] ?? s.width / 2, v['py'] ?? 60), e = _eAt(v, s, pt);
        if (e.distance > 0) arw(c, pt, pt + e / e.distance * (14 + 10 * math.log(1 + e.distance / 1e5)).clamp(14, 70), p.peach.deep, 3, 9);
        c.drawCircle(pt, 7, fi(const Color(0xFFF2B400)));
        c.drawCircle(pt, 7, sk(p.ink, 1.5));
        tx(c, 'drag the test point', const Offset(8, 8), p.ink2, size: 11);
      },
    );
  },
  'electroscope': (_) {
    var qNet = 0.0, prevD = 10.0;
    double sep(V v) => (v['rod'] == 0 ? 1 : -1) * 3 / math.pow(1 + v['d']! / 2.5, 2);
    void update(V v, String k) {
      final s = sep(v), earthed = v['earth'] == 1;
      if (k == 'd' && v['d'] == 0 && prevD > 0 && !earthed) qNet += (v['rod'] == 0 ? 1 : -1) * 2.0;
      prevD = v['d']!;
      if (earthed) qNet = v['d'] == 0 ? 0 : -2 * s;
    }

    return LabSpec(
      height: 280,
      opts: const [
        Opt('rod', ['+ rod (glass)', '− rod (polythene)']),
        Opt('earth', ['Not earthed', 'Finger on the cap (earthed)']),
      ],
      sliders: const [Sl('d', 'Rod distance from the cap (0 = touching)', 0, 10, 10, unit: 'cm')],
      reset: (v) {
        qNet = 0;
        prevD = v['d']!;
      },
      changed: update,
      formula: 'like charges repel: the leaves spread when they carry the same charge',
      tryThis:
          'Charge by induction: bring the − rod close, put a finger on the cap, take the finger away, then move the rod away. The leaves stay open with a + charge (opposite to the rod).',
      read: (v, t) {
        final s = sep(v), qL = v['earth'] == 1 ? 0.0 : qNet / 2 + s;
        String sg(double q) => q.abs() < .05 ? 'neutral' : (q > 0 ? '+' : '−');
        return [('leaves', sg(qL)), ('cap', sg(v['earth'] == 1 ? qNet : qNet / 2 - s)), ('whole electroscope', sg(qNet))];
      },
      draw: (c, s, v, t, p) {
        final sp = sep(v), earthed = v['earth'] == 1, qL = earthed ? 0.0 : qNet / 2 + sp, qC = earthed ? qNet : qNet / 2 - sp;
        final cx = s.width * .42, capY = s.height * .34, jar = Rect.fromCenter(center: Offset(cx, s.height * .7), width: 150, height: 140);
        c.drawRRect(RRect.fromRectAndRadius(jar, const Radius.circular(20)), fi(const Color(0x2246A0DC)));
        c.drawRRect(RRect.fromRectAndRadius(jar, const Radius.circular(20)), sk(_wire, 2));
        final stemB = Offset(cx, jar.center.dy - 6);
        c.drawLine(Offset(cx, capY), stemB, sk(const Color(0xFF9A948C), 5));
        c.drawRRect(
          RRect.fromRectAndRadius(Rect.fromCenter(center: Offset(cx, capY), width: 70, height: 10), const Radius.circular(5)),
          fi(const Color(0xFF9A948C)),
        );
        final ang = (qL.abs() / 4).clamp(0.0, 1.0) * 42 * deg + 3 * deg;
        for (final sg in [-1.0, 1.0]) {
          final tip = stemB + Offset(math.sin(ang) * sg, math.cos(ang)) * 48;
          c.drawLine(stemB, tip, sk(const Color(0xFFD9A300), 5));
          if (qL.abs() > .05) tx(c, qL > 0 ? '+' : '−', tip + Offset(sg * 10, -6), qL > 0 ? _nRed : _sBlue, size: 15, ax: .5, ay: .5, w: FontWeight.w900);
        }
        final nc = (qC.abs() * 1.2).round().clamp(0, 5);
        for (var i = 0; i < nc; i++) {
          tx(c, qC > 0 ? '+' : '−', Offset(cx - 26 + 13 * i, capY - 16), qC > 0 ? _nRed : _sBlue, size: 15, ax: .5, ay: .5, w: FontWeight.w900);
        }
        // rod above the cap
        final ry = capY - 30 - v['d']! * (capY - 50) / 10, pos = v['rod'] == 0;
        c.drawRRect(
          RRect.fromRectAndRadius(Rect.fromLTRB(cx - 50, ry - 18, cx + s.width * .5, ry - 4), const Radius.circular(7)),
          fi(pos ? const Color(0xFFBFD8E6) : const Color(0xFF6E6A66)),
        );
        for (var i = 0; i < 6; i++) {
          tx(c, pos ? '+' : '−', Offset(cx - 38 + 14 * i, ry - 11), pos ? _nRed : const Color(0xFFFFFFFF), size: 13, ax: .5, ay: .5, w: FontWeight.w900);
        }
        if (earthed) {
          final f = Offset(cx + 40, capY);
          c.drawLine(Offset(cx + 30, capY), f + const Offset(30, 0), sk(p.ink, 2));
          final g = f + const Offset(30, 0);
          c.drawLine(g, g + const Offset(0, 30), sk(p.ink, 2));
          for (var i = 0; i < 3; i++) {
            c.drawLine(g + Offset(-12 + 4.0 * i, 30 + 5.0 * i), g + Offset(12 - 4.0 * i, 30 + 5.0 * i), sk(p.ink, 2));
          }
          tx(c, 'earth', g + const Offset(14, 10), p.ink, size: 11);
        }
        tx(c, 'leaves ${(ang / deg - 3).round()}° apart each', Offset(jar.right + 8, jar.bottom - 16), p.ink2, size: 10.5);
      },
    );
  },
  'resistivity': (_) => LabSpec(
    height: 210,
    opts: const [
      Opt('mat', ['Copper', 'Aluminium', 'Iron', 'Nichrome']),
    ],
    sliders: const [
      Sl('L', 'Length L', .1, 5, 1, step: .1, unit: 'm'),
      Sl('d', 'Diameter', .1, 2, .5, step: .05, unit: 'mm'),
    ],
    formula: 'R = ρ L / A,   A = π d² / 4',
    tryThis:
        'Double the length: R doubles. Double the diameter: the area is 4 times bigger, so R falls to a quarter. Nichrome has about 65 times the resistivity of copper, which is why heaters use it.',
    read: (v, t) {
      const rho = [1.7e-8, 2.8e-8, 9.7e-8, 1.1e-6];
      final r = rho[v['mat']!.round()], A = math.pi * math.pow(v['d']! / 1000, 2) / 4, R = r * v['L']! / A;
      return [('ρ', '${sci(r)} Ω m'), ('A', '${sci(A)} m²'), ('R', '${sci(R)} Ω'), ('I from 1.5 V', '${sci(1.5 / R)} A')];
    },
    draw: (c, s, v, t, p) {
      const cols = [Color(0xFFC77A3A), Color(0xFFB8BCC2), Color(0xFF7D7F84), Color(0xFF8F8A6E)];
      final x0 = 30.0, len = (s.width - 60) * v['L']! / 5, th = 3 + 12 * v['d']! / 2, cy = s.height * .45;
      c.drawRRect(RRect.fromRectAndRadius(Rect.fromLTWH(x0, cy - th / 2, len, th), Radius.circular(th / 2)), fi(cols[v['mat']!.round()]));
      c.drawOval(Rect.fromCenter(center: Offset(x0 + len, cy), width: th * .5, height: th), fi(const Color(0x33000000)));
      arw(c, Offset(x0, cy + 26), Offset(x0 + len, cy + 26), p.ink2, 1.3, 6);
      tx(c, 'L = ${fx(v['L']!)} m', Offset(x0 + len / 2, cy + 32), p.ink2, size: 11.5, ax: .5);
      tx(c, 'd = ${fx(v['d']!, 2)} mm', Offset(x0, cy - th / 2 - 20), p.ink2, size: 11.5);
      // cross-section circle (to scale with the slider)
      final cc = Offset(s.width - 44, s.height * .2);
      c.drawCircle(cc, 4 + 22 * v['d']! / 2, fi(cols[v['mat']!.round()]));
      tx(c, 'cross-section', cc + const Offset(0, 30), p.ink2, size: 10, ax: .5);
    },
  ),
  'wheatstone': (_) => LabSpec(
    height: 270,
    sliders: const [
      Sl('R1', 'R₁', 10, 1000, 100, step: 10, unit: 'Ω'),
      Sl('R2', 'R₂', 10, 1000, 200, step: 10, unit: 'Ω'),
      Sl('R3', 'R₃ (variable)', 10, 1000, 100, step: 10, unit: 'Ω'),
    ],
    formula: 'balanced (no current in G) when R₁/R₂ = R₃/Rx,  so Rx = R₂R₃/R₁',
    tryThis: 'The unknown resistor Rx is hidden. Adjust R₃ until the galvanometer reads zero, then work out Rx = R₂R₃/R₁.',
    read: (v, t) {
      final rx = (v['rx'] ?? 330.0), vb = 6 * v['R2']! / (v['R1']! + v['R2']!), vd = 6 * rx / (v['R3']! + rx), dv = vb - vd;
      final bal = dv.abs() < .02;
      return [('V across G', '${fx(dv * 1000, 0)} mV'), ('', bal ? 'balanced! Rx = R₂R₃/R₁ = ${fx(v['R2']! * v['R3']! / v['R1']!, 0)} Ω' : 'not balanced yet')];
    },
    draw: (c, s, v, t, p) {
      final cx = s.width / 2, cy = s.height * .48, rw = math.min(s.width * .34, 130.0), rh = s.height * .34;
      final a = Offset(cx - rw, cy), b = Offset(cx, cy - rh), cc = Offset(cx + rw, cy), d = Offset(cx, cy + rh);
      void res(Offset p1, Offset p2, String name) {
        final m = (p1 + p2) / 2, u = (p2 - p1) / (p2 - p1).distance, n = Offset(-u.dy, u.dx);
        c.drawLine(p1, m - u * 22, sk(_wire, 2.5));
        c.drawLine(m + u * 22, p2, sk(_wire, 2.5));
        c.drawPath(Path()..addPolygon([m - u * 22 + n * 8, m + u * 22 + n * 8, m + u * 22 - n * 8, m - u * 22 - n * 8], true), fi(p.surface));
        c.drawPath(Path()..addPolygon([m - u * 22 + n * 8, m + u * 22 + n * 8, m + u * 22 - n * 8, m - u * 22 - n * 8], true), sk(p.ink, 2));
        tx(c, name, m + n * (p1.dy < p2.dy == (p1.dx < p2.dx) ? -22 : 22) * (m.dy < cy ? 1 : -1), p.ink, size: 12, ax: .5, ay: .5);
      }

      res(a, b, 'R₁');
      res(b, cc, 'R₂');
      res(a, d, 'R₃');
      res(d, cc, 'Rx ?');
      final rx = (v['rx'] ?? 330.0), vb = 6 * v['R2']! / (v['R1']! + v['R2']!), vd = 6 * rx / (v['R3']! + rx), dv = vb - vd;
      c.drawLine(b, Offset(cx, cy - 20), sk(_wire, 2));
      c.drawLine(d, Offset(cx, cy + 20), sk(_wire, 2));
      c.drawCircle(Offset(cx, cy), 20, fi(p.surface));
      c.drawCircle(Offset(cx, cy), 20, sk(p.ink, 2));
      final ang = -math.pi / 2 + (dv / 1.5).clamp(-1.0, 1.0) * math.pi * .38;
      c.drawLine(Offset(cx, cy + 8), Offset(cx, cy + 8) + Offset(math.cos(ang), math.sin(ang)) * 22, sk(dv.abs() < .02 ? p.sage.deep : _nRed, 2.5));
      tx(c, 'G', Offset(cx + 8, cy + 4), p.ink2, size: 10);
      // battery from A round the bottom to C
      final by = s.height - 16;
      c.drawLine(a, Offset(a.dx, by), sk(_wire, 2));
      c.drawLine(Offset(a.dx, by), Offset(cx - 6, by), sk(_wire, 2));
      c.drawLine(Offset(cx + 6, by), Offset(cc.dx, by), sk(_wire, 2));
      c.drawLine(Offset(cc.dx, by), cc, sk(_wire, 2));
      c.drawLine(Offset(cx - 6, by - 10), Offset(cx - 6, by + 10), sk(p.ink, 3));
      c.drawLine(Offset(cx + 6, by - 6), Offset(cx + 6, by + 6), sk(p.ink, 4));
      tx(c, '6 V', Offset(cx + 14, by - 18), p.ink2, size: 11);
    },
  ),
};

double _sinh(double x) => (math.exp(x) - math.exp(-x)) / 2;
double _coth(double x) => (math.exp(x) + math.exp(-x)) / (math.exp(x) - math.exp(-x));

const _supD = {'-': '⁻', '0': '⁰', '1': '¹', '2': '²', '3': '³', '4': '⁴', '5': '⁵', '6': '⁶', '7': '⁷', '8': '⁸', '9': '⁹'};
String _supN(int e) => '$e'.split('').map((ch) => _supD[ch] ?? ch).join();

String _lambda(double l) {
  if (l >= 1) return '${fx(l, l < 10 ? 1 : 0)} m';
  if (l >= 1e-2) return '${fx(l * 100, 1)} cm';
  if (l >= 1e-3) return '${fx(l * 1000, 1)} mm';
  if (l >= 1e-6) return '${fx(l * 1e6, 1)} µm';
  if (l >= 1e-9) return '${fx(l * 1e9, 0)} nm';
  return '${fx(l * 1e12, 1)} pm';
}

String _region(double l) => l < 1e-11
    ? 'gamma rays'
    : l < 1e-8
    ? 'X-rays'
    : l < 3.8e-7
    ? 'ultraviolet'
    : l < 7.5e-7
    ? 'visible light'
    : l < 1e-3
    ? 'infrared'
    : l < .1
    ? 'microwaves'
    : 'radio waves';

String _uses(double l) => l < 1e-11
    ? 'killing cancer cells, sterilising'
    : l < 1e-8
    ? 'X-ray photographs of bones'
    : l < 3.8e-7
    ? 'sun-tan, detecting forged notes'
    : l < 7.5e-7
    ? 'seeing, photography'
    : l < 1e-3
    ? 'remote controls, heat cameras'
    : l < .1
    ? 'cooking, mobile phones, radar'
    : 'radio and TV broadcasts';

List<(Offset, double)> _charges(V v, Size s) {
  final setup = v['setup']!.round(), cx = s.width / 2, cy = s.height / 2, half = v['d']! / 2 * (s.width / 20);
  if (setup == 2) return [(Offset(cx, cy), v['q1']!)];
  return [(Offset(cx - half, cy), v['q1']!), (Offset(cx + half, cy), setup == 0 ? -v['q2']! : v['q2']!)];
}

/// field (N/C) at a canvas point: 20 cm across the canvas width
Offset _eAt(V v, Size s, Offset pt) {
  var e = Offset.zero;
  final m = .2 / s.width;
  for (final (o, q) in _charges(v, s)) {
    final d = (pt - o) * m, r = math.max(d.distance, .004);
    e += d / r * (kC * q * 1e-6 / (r * r));
  }
  return e;
}

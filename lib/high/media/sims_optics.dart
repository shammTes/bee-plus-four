// Physics labs: geometrical optics (Grade 10 unit 5, Grade 11 unit 1). Physics and drawing written from scratch.
import 'dart:math' as math;

import 'package:flutter/widgets.dart';

import '../notes/jr/theme/tokens.dart';
import 'lab_kit.dart';
import 'sims.dart';

const laser = Color(0xFFE0302C);
const _glass = Color(0x5546A0DC), _glassEdge = Color(0xFF3F86BF);

String material(double n) {
  final m = {1.00: 'air', 1.33: 'water', 1.36: 'ethanol', 1.47: 'glycerine', 1.50: 'glass', 1.52: 'crown glass', 1.65: 'flint glass', 2.42: 'diamond'};
  for (final e in m.entries) {
    if ((e.key - n).abs() < .005) return '${n.toStringAsFixed(2)} ${e.value}';
  }
  return n.toStringAsFixed(2);
}

Color _medium(double n) => Color.fromARGB((25 + 150 * ((n - 1) / 1.42).clamp(0.0, 1.0)).round(), 70, 150, 215);

/// unpolarised Fresnel reflectance
double fresnel(double n1, double n2, double ti, double tt) {
  final ci = math.cos(ti), ct = math.cos(tt);
  final rs = (n1 * ci - n2 * ct) / (n1 * ci + n2 * ct), rp = (n1 * ct - n2 * ci) / (n1 * ct + n2 * ci);
  return (rs * rs + rp * rp) / 2;
}

final Map<String, SimSpec Function(Map<String, dynamic>)> opticsLabs = {
  'refraction': (_) => LabSpec(
    height: 280,
    opts: const [
      Opt('mode', ['Boundary', 'Glass block']),
    ],
    sliders: [
      const Sl('i', 'Angle of incidence θ₁', 0, 89, 40, unit: '°'),
      Sl('n1', 'Top medium n₁', 1, 2.42, 1, step: .01, fmt: material, when: (v) => v['mode'] == 0),
      Sl('n2', 'Bottom medium n₂', 1, 2.42, 1.5, step: .01, fmt: material, when: (v) => v['mode'] == 0),
      Sl('n', 'Block refractive index n', 1, 2.42, 1.5, step: .01, fmt: material, when: (v) => v['mode'] == 1),
    ],
    formulaOf: (v) => v['mode'] == 0 ? 'n₁ sin θ₁ = n₂ sin θ₂' : 'sin i = n sin r;  ray leaves parallel, shifted sideways',
    tryThis:
        'Set n₁ = 1.50 (glass) and n₂ = 1.00 (air), then raise θ₁ past the critical angle (41.8°): the refracted ray vanishes and all the light is reflected (total internal reflection).',
    read: (v, t) {
      final i = v['i']! * deg;
      if (v['mode'] == 1) {
        final n = v['n']!, r = math.asin(math.sin(i) / n), d = 5 * math.sin(i - r) / math.cos(r);
        return [('r', '${fx(r / deg)}°'), ('emerges at', '${fx(v['i']!, 0)}° (parallel)'), ('sideways shift (5 cm block)', '${fx(d, 2)} cm')];
      }
      final n1 = v['n1']!, n2 = v['n2']!, s2 = n1 * math.sin(i) / n2;
      return [
        ('n₁ sin θ₁', fx(n1 * math.sin(i), 3)),
        if (s2 <= 1) ('θ₂', '${fx(math.asin(s2) / deg)}°') else ('θ₂', 'none: total internal reflection'),
        if (n1 > n2)
          ('critical angle sin⁻¹(n₂/n₁)', '${fx(math.asin(n2 / n1) / deg)}°')
        else
          ('', n1 == n2 ? 'same medium: no bending' : 'into denser: bends towards the normal'),
        if (s2 <= 1) ('reflected', '${(fresnel(n1, n2, i, math.asin(s2)) * 100).toStringAsFixed(0)} %'),
      ];
    },
    draw: (c, s, v, t, p) {
      final i = v['i']! * deg;
      if (v['mode'] == 1) {
        final n = v['n']!, top = s.height * .36, bot = s.height * .66;
        final poly = [Offset(-60, top), Offset(s.width + 60, top), Offset(s.width + 60, bot), Offset(-60, bot)];
        c.drawRect(Rect.fromLTRB(0, top, s.width, bot), fi(_medium(n)));
        c.drawLine(Offset(0, top), Offset(s.width, top), sk(_glassEdge, 2));
        c.drawLine(Offset(0, bot), Offset(s.width, bot), sk(_glassEdge, 2));
        final hit = Offset(s.width * .38, top), d = Offset(math.sin(i), math.cos(i)), o = hit - d * 400;
        final tr = tracePoly(o, d, poly, n);
        dsh(c, hit, hit + d * 400, p.ink2, 1.2);
        for (final q in tr.pts.skip(1)) {
          dsh(c, q - const Offset(0, 46), q + const Offset(0, 46), p.ink2, 1.2, 5);
        }
        rayPath(c, tr.pts, tr.dir, laser);
        final r = math.asin(math.sin(i) / n);
        angArc(c, hit, 30, -math.pi / 2, math.atan2(-d.dy, -d.dx), p.peach.deep, 'i');
        angArc(c, hit, 30, math.pi / 2, math.atan2(math.cos(r), math.sin(r)), p.blue.deep, 'r');
        tx(c, 'air', const Offset(10, 8), p.ink2, size: 12);
        tx(c, 'block n = ${n.toStringAsFixed(2)}', Offset(10, top + 6), p.ink, size: 12);
        tx(c, 'dashed: the ray if there were no block', Offset(s.width - 8, s.height - 18), p.ink2, size: 11, ax: 1);
        return;
      }
      final n1 = v['n1']!, n2 = v['n2']!, o = Offset(s.width / 2, s.height / 2);
      c.drawRect(Rect.fromLTRB(0, 0, s.width, o.dy), fi(_medium(n1)));
      c.drawRect(Rect.fromLTRB(0, o.dy, s.width, s.height), fi(_medium(n2)));
      c.drawLine(Offset(0, o.dy), Offset(s.width, o.dy), sk(_glassEdge, 2));
      dsh(c, Offset(o.dx, 6), Offset(o.dx, s.height - 6), p.ink2, 1.3);
      tx(c, 'normal', Offset(o.dx + 5, 6), p.ink2, size: 11);
      tx(c, 'n₁ = ${material(n1)}', const Offset(10, 8), p.ink, size: 12.5);
      tx(c, 'n₂ = ${material(n2)}', Offset(10, s.height - 24), p.ink, size: 12.5);
      final L = s.height * .48, din = Offset(math.sin(i), math.cos(i)), src = o - din * L;
      final s2 = n1 * math.sin(i) / n2, tirOn = s2 > 1;
      final R = tirOn ? 1.0 : fresnel(n1, n2, i, math.asin(s2));
      // reflected (brightness = Fresnel reflectance), refracted, incident
      final refl = Offset(math.sin(i), -math.cos(i));
      final rc = laser.withValues(alpha: .18 + .82 * R);
      c.drawLine(o, o + refl * L, sk(rc, 2.5));
      midHead(c, o, o + refl * L, rc);
      if (!tirOn) {
        final t2 = math.asin(s2), dout = Offset(math.sin(t2), math.cos(t2)), tc = laser.withValues(alpha: .3 + .7 * (1 - R));
        c.drawLine(o, o + dout * L * 1.2, sk(tc, 2.5));
        midHead(c, o, o + dout * L, tc);
        angArc(c, o, 34, math.pi / 2, math.atan2(dout.dy, dout.dx), p.blue.deep, 'θ₂');
      } else {
        tx(c, 'total internal reflection', Offset(o.dx + 10, o.dy + 14), laser, size: 13);
      }
      c.drawLine(src, o, sk(laser, 3));
      midHead(c, src, o, laser);
      c.drawCircle(src, 6, fi(laser));
      angArc(c, o, 34, -math.pi / 2, math.atan2(-din.dy, -din.dx), p.peach.deep, 'θ₁');
    },
  ),
  'reflection': (_) {
    return LabSpec(
      height: 270,
      opts: const [
        Opt('mode', ['Plane mirror', 'Two mirrors']),
      ],
      sliders: [
        const Sl('i', 'Angle of incidence i', 0, 85, 35, unit: '°'),
        Sl('a', 'Angle between the mirrors', 30, 150, 90, step: 5, unit: '°', when: (v) => v['mode'] == 1),
      ],
      formulaOf: (v) => v['mode'] == 0 ? 'angle of incidence i = angle of reflection r' : 'number of images = 360° ÷ angle − 1',
      tryThis:
          'Measure from the normal, not from the mirror. With two mirrors at 90° the ray comes back parallel to where it started (like a bicycle reflector); at 60° you would see 5 images.',
      read: (v, t) {
        if (v['mode'] == 0) {
          return [('i = r', '${fx(v['i']!, 0)}°'), ('glancing angle', '${fx(90 - v['i']!, 0)}°'), ('ray turned through', '${fx(180 - 2 * v['i']!, 0)}°')];
        }
        final a = v['a']!, n = 360 / a - 1;
        return [
          ('images', n == n.roundToDouble() ? '${n.round()}' : '≈ ${n.floor()} (360/${a.round()} not whole)'),
          ('after 2 reflections the ray turns', '${fx(360 - 2 * a, 0)}°'),
        ];
      },
      draw: (c, s, v, t, p) {
        final i = v['i']! * deg;
        if (v['mode'] == 0) {
          final o = Offset(s.width / 2, s.height * .8), L = s.height * .68;
          c.drawLine(Offset(30, o.dy), Offset(s.width - 30, o.dy), sk(p.blue.deep, 4));
          for (var x = 36.0; x < s.width - 30; x += 12) {
            c.drawLine(Offset(x, o.dy + 3), Offset(x - 8, o.dy + 12), sk(p.ink2, 1.2));
          }
          dsh(c, o, Offset(o.dx, 10), p.ink2, 1.3);
          tx(c, 'normal', Offset(o.dx + 5, 8), p.ink2, size: 11);
          final din = Offset(math.sin(i), math.cos(i)), src = o - din * L, out = o + Offset(math.sin(i), -math.cos(i)) * L;
          c.drawLine(src, o, sk(laser, 3));
          midHead(c, src, o, laser);
          c.drawLine(o, out, sk(laser, 3));
          midHead(c, o, out, laser);
          c.drawCircle(src, 6, fi(laser));
          angArc(c, o, 44, -math.pi / 2, math.atan2(-din.dy, -din.dx), p.peach.deep, 'i = ${v['i']!.round()}°');
          angArc(c, o, 30, -math.pi / 2, math.atan2(-din.dy, din.dx), p.blue.deep, 'r');
          tx(c, 'mirror', Offset(34, o.dy + 14), p.blue.deep, size: 12);
          return;
        }
        final a = v['a']! * deg, vx = Offset(s.width * .3, s.height * .86), L = math.min(s.width * .66, s.height * 1.2);
        final m1 = (vx, vx + Offset(L, 0)), m2 = (vx, vx + Offset(math.cos(a), -math.sin(a)) * L);
        for (final m in [m1, m2]) {
          c.drawLine(m.$1, m.$2, sk(p.blue.deep, 4));
        }
        angArc(c, vx, 26, 0, -a, p.ink2, '${v['a']!.round()}°');
        // ray comes in from the upper right and hits mirror 1
        var o = vx + Offset(L * .62, 0) - Offset(-math.sin(i), math.cos(i)) * 600;
        var d = Offset(-math.sin(i), math.cos(i));
        final pts = [o];
        for (var k = 0; k < 12; k++) {
          double? best;
          (Offset, Offset)? hm;
          for (final m in [m1, m2]) {
            final tt = raySeg(o, d, m.$1, m.$2);
            if (tt != null && (best == null || tt < best)) {
              best = tt;
              hm = m;
            }
          }
          if (best == null) break;
          o = o + d * best;
          pts.add(o);
          final e = hm!.$2 - hm.$1;
          d = reflectDir(d, Offset(-e.dy, e.dx) / e.distance);
          o = o + d * .01;
        }
        rayPath(c, pts, d, laser);
        tx(c, 'mirror 1', vx + Offset(L - 4, 6), p.blue.deep, size: 12, ax: 1);
        tx(c, 'mirror 2', m2.$2 + const Offset(6, 0), p.blue.deep, size: 12);
      },
    );
  },
  'plane_image': (_) => LabSpec(
    height: 270,
    sliders: const [
      Sl('u', 'Object distance from mirror', 5, 40, 20, unit: 'cm'),
      Sl('e', 'Eye height', -10, 12, 0, unit: 'cm'),
    ],
    formula: 'image distance = object distance;  image height = object height',
    tryThis: 'Move the eye up and down: the rays change but the image stays in the same place. The flag points the other way in the image: lateral inversion.',
    drag: (v, at, s) {
      if (at.dx < s.width / 2 - 8) v['u'] = ((s.width / 2 - at.dx) / ((s.width / 2 - 20) / 42)).roundToDouble().clamp(5, 40);
    },
    read: (v, t) => [('image distance', '${v['u']!.round()} cm behind'), ('image', 'virtual, upright, same size'), ('', 'laterally inverted')],
    draw: (c, s, v, t, p) {
      final mx = s.width / 2, sc = (s.width / 2 - 20) / 42, base = s.height * .9;
      c.drawLine(Offset(mx, 14), Offset(mx, s.height - 10), sk(p.blue.deep, 4));
      for (var y = 18.0; y < s.height - 10; y += 12) {
        c.drawLine(Offset(mx + 3, y), Offset(mx + 11, y - 7), sk(p.ink2, 1.2));
      }
      final u = v['u']!, ox = mx - u * sc, ix = mx + u * sc, hgt = 14 * sc;
      void candle(double x, bool img) {
        final col = img ? p.ink2 : p.peach.deep;
        final r = Rect.fromLTRB(x - 5, base - hgt, x + 5, base);
        img ? c.drawRect(r, sk(col, 1.5)) : c.drawRect(r, fi(col));
        final f = Offset(x, base - hgt - 9);
        c.drawOval(Rect.fromCenter(center: f, width: 9, height: 15), img ? sk(const Color(0xFFE5A100), 1.5) : fi(const Color(0xFFF2B400)));
        final dir = img ? -1.0 : 1.0;
        c.drawLine(Offset(x, base - hgt * .55), Offset(x + dir * 16, base - hgt * .55 - 5), sk(col, 2));
        c.drawLine(Offset(x + dir * 16, base - hgt * .55 - 5), Offset(x, base - hgt * .55 - 10), sk(col, 2));
      }

      candle(ox, false);
      candle(ix, true);
      final eye = Offset(mx - 26 * sc, s.height * .3 - v['e']! * sc * .9);
      for (final ty in [base - hgt - 9, base - 2]) {
        final obj = Offset(ox, ty), img = Offset(ix, ty), k = (mx - eye.dx) / (img.dx - eye.dx), m = eye + (img - eye) * k;
        c.drawLine(obj, m, sk(laser, 2));
        midHead(c, obj, m, laser);
        c.drawLine(m, eye, sk(laser, 2));
        midHead(c, m, eye, laser);
        dsh(c, m, img, laser.withValues(alpha: .6), 1.4, 5);
      }
      c.drawOval(Rect.fromCenter(center: eye, width: 26, height: 15), fi(p.surface));
      c.drawOval(Rect.fromCenter(center: eye, width: 26, height: 15), sk(p.ink, 2));
      c.drawCircle(eye + const Offset(4, 0), 4, fi(p.ink));
      dsh(c, Offset(ox, base + 6), Offset(ix, base + 6), p.ink2, 1);
      tx(c, '${u.round()} cm', Offset((ox + mx) / 2, base + 8), p.ink2, size: 11, ax: .5);
      tx(c, '${u.round()} cm', Offset((ix + mx) / 2, base + 8), p.ink2, size: 11, ax: .5);
      tx(c, 'object', Offset(ox, base - hgt - 32), p.peach.deep, size: 12, ax: .5);
      tx(c, 'image', Offset(ix, base - hgt - 32), p.ink2, size: 12, ax: .5);
      tx(c, 'drag the candle', const Offset(8, 8), p.ink2, size: 11);
    },
  ),
  'apparent_depth': (_) => LabSpec(
    height: 280,
    sliders: [
      const Sl('d', 'Real depth of the coin', 10, 100, 60, unit: 'cm'),
      Sl('n', 'Liquid refractive index n', 1, 2.42, 1.33, step: .01, fmt: material),
    ],
    formula: 'apparent depth = real depth ÷ n',
    tryThis: 'Water (n = 1.33) makes a pool look only ¾ as deep as it is. Set n = 1.00: the image sits on the coin.',
    read: (v, t) {
      final d = v['d']!, n = v['n']!;
      return [('apparent depth', '${fx(d / n)} cm'), ('raised by', '${fx(d - d / n)} cm'), ('n = real ÷ apparent', fx(n, 2))];
    },
    draw: (c, s, v, t, p) {
      final d = v['d']!, n = v['n']!, top = 64.0, sc = (s.height - top - 22) / 100, cx = s.width * .42;
      c.drawRect(Rect.fromLTRB(cx - s.width * .3, top, cx + s.width * .3, s.height - 10), fi(_medium(n)));
      c.drawLine(Offset(cx - s.width * .3, top), Offset(cx + s.width * .3, top), sk(_glassEdge, 2));
      final coin = Offset(cx, top + d * sc);
      final t1 = 9 * deg, t2s = n * math.sin(t1);
      final dx = d * sc * math.tan(t1), t2 = math.asin(t2s.clamp(-1.0, 1.0)), app = top + dx / math.tan(t2);
      for (final sg in [-1.0, 1.0]) {
        final hit = Offset(cx + sg * dx, top), up = Offset(sg * math.sin(t2), -math.cos(t2));
        c.drawLine(coin, hit, sk(laser, 2));
        midHead(c, coin, hit, laser);
        c.drawLine(hit, hit + up * (top + 10) / math.cos(t2), sk(laser, 2));
        dsh(c, hit, Offset(cx, app), laser.withValues(alpha: .7), 1.4, 5);
      }
      c.drawOval(Rect.fromCenter(center: Offset(cx, app), width: 30, height: 8), sk(const Color(0xFFC08A00), 2));
      c.drawOval(Rect.fromCenter(center: coin, width: 30, height: 8), fi(const Color(0xFFD9A300)));
      final eye = Offset(cx, 16);
      c.drawOval(Rect.fromCenter(center: eye, width: 26, height: 15), fi(p.surface));
      c.drawOval(Rect.fromCenter(center: eye, width: 26, height: 15), sk(p.ink, 2));
      c.drawCircle(eye + const Offset(0, 3), 4, fi(p.ink));
      final rx = cx + s.width * .34;
      arw(c, Offset(rx, top), Offset(rx, coin.dy), p.ink, 1.6, 7);
      tx(c, 'real ${d.round()} cm', Offset(rx + 4, (top + coin.dy) / 2), p.ink, size: 11.5);
      arw(c, Offset(rx - 16, top), Offset(rx - 16, app), p.peach.deep, 1.6, 7);
      tx(c, 'seen', Offset(rx - 20, (top + app) / 2 - 7), p.peach.deep, size: 11.5, ax: 1);
      tx(c, 'coin', coin + const Offset(20, -6), p.ink, size: 11.5);
      tx(c, 'image', Offset(cx + 20, app - 6), p.peach.deep, size: 11.5);
      tx(c, 'viewed from straight above', Offset(s.width - 8, s.height - 26), p.ink2, size: 11, ax: 1);
    },
  ),
  'prism': (_) => LabSpec(
    height: 280,
    opts: [
      const Opt('mode', ['Dispersion', 'Right-angle prism']),
      Opt('w', const ['White light', 'Red only'], when: (v) => v['mode'] == 0),
      Opt('turn', const ['Turn 90° (periscope)', 'Turn 180° (binoculars)'], when: (v) => v['mode'] == 1),
    ],
    sliders: [
      Sl('i', 'Angle of incidence', 20, 80, 50, unit: '°', when: (v) => v['mode'] == 0),
      Sl('A', 'Prism angle A', 40, 70, 60, unit: '°', when: (v) => v['mode'] == 0),
      Sl('n', 'Refractive index n', 1.3, 1.9, 1.5, step: .01, when: (v) => v['mode'] == 1),
      Sl('y', 'Ray position', 20, 80, 45, unit: '%', when: (v) => v['mode'] == 1),
    ],
    formulaOf: (v) =>
        v['mode'] == 0 ? 'deviation δ = i + e − A;   n = sin((A + δmin)/2) ÷ sin(A/2)' : 'total internal reflection when 45° > critical angle c = sin⁻¹(1/n)',
    tryThis:
        'Violet bends most and red least, because n is bigger for violet. In the right-angle prism, lower n below 1.41: the critical angle grows past 45° and the light leaks out instead of turning.',
    read: (v, t) {
      if (v['mode'] == 1) {
        final n = v['n']!, cA = math.asin(1 / n) / deg;
        return [
          ('critical angle c', '${fx(cA)}°'),
          ('angle on the long face', '45°'),
          ('', n > math.sqrt2 ? 'TIR: the prism works as a mirror' : 'no TIR: light escapes'),
        ];
      }
      final r = _prismRun(v, const Size(360, 280));
      if (r.isEmpty) return [('', 'light does not get out of the prism')];
      final dr = r.first.$2, dv = r.last.$2;
      final A = v['A']! * deg, nm = _nGlass(589), dmin = 2 * math.asin(nm * math.sin(A / 2)) - A;
      return [
        if (v['w'] == 0) ...[
          ('δ red', dr == null ? 'TIR' : '${fx(dr)}°'),
          ('δ violet', dv == null ? 'TIR' : '${fx(dv)}°'),
        ] else
          ('δ', dr == null ? 'TIR at 2nd face' : '${fx(dr)}°'),
        ('δmin (yellow, n = ${fx(nm, 3)})', '${fx(dmin / deg)}°'),
      ];
    },
    draw: (c, s, v, t, p) {
      if (v['mode'] == 1) return _rightPrism(c, s, v, p);
      final g = _prismGeom(v, s);
      c.drawPath(Path()..addPolygon(g.poly, true), fi(_glass));
      c.drawPath(Path()..addPolygon(g.poly, true), sk(_glassEdge, 2));
      tx(c, 'A', g.poly[0] + const Offset(0, 16), p.ink, size: 12, ax: .5);
      final o = g.hit - g.d * 500;
      c.drawLine(o, g.hit, sk(v['w'] == 0 ? p.ink : laser, 3));
      midHead(c, g.hit - g.d * 80, g.hit, v['w'] == 0 ? p.ink : laser);
      if (v['w'] == 0) tx(c, 'white light', g.hit - g.d * 90 + const Offset(-10, 6), p.ink, size: 12, ax: .5);
      for (final nm in v['w'] == 0 ? _bands : const [656.0]) {
        final tr = tracePoly(o, g.d, g.poly, _nGlass(nm));
        final col = v['w'] == 0 ? waveColor(nm) : laser;
        rayPath(c, tr.pts.skip(1).toList(), tr.dir, col, w: 2, heads: false);
      }
      dsh(c, g.hit, g.hit + g.d * 400, p.ink2, 1);
      tx(c, 'dense flint glass', Offset(s.width - 8, s.height - 20), p.ink2, size: 11, ax: 1);
    },
  ),
  'color_mix': (_) => LabSpec(
    height: 260,
    opts: const [
      Opt('mode', ['Coloured lights (add)', 'Paints / filters (subtract)']),
    ],
    sliders: [
      Sl('r', 'Red light', 0, 255, 255, step: 5, when: (v) => v['mode'] == 0),
      Sl('g', 'Green light', 0, 255, 255, step: 5, when: (v) => v['mode'] == 0),
      Sl('b', 'Blue light', 0, 255, 255, step: 5, when: (v) => v['mode'] == 0),
      Sl('c', 'Cyan filter', 0, 255, 255, step: 5, when: (v) => v['mode'] == 1),
      Sl('m', 'Magenta filter', 0, 255, 255, step: 5, when: (v) => v['mode'] == 1),
      Sl('y', 'Yellow filter', 0, 255, 255, step: 5, when: (v) => v['mode'] == 1),
    ],
    formulaOf: (v) => v['mode'] == 0 ? 'red + green + blue = white;  red + green = yellow' : 'white − red = cyan;  cyan + yellow filters pass only green',
    tryThis:
        'Turn the blue light off: red + green make yellow. With filters, a yellow filter absorbs blue and a cyan filter absorbs red, so together only green gets through.',
    read: (v, t) {
      final col = _mixCentre(v);
      return [('middle', _colorName(col)), ('RGB', '${(col.r * 255).round()}, ${(col.g * 255).round()}, ${(col.b * 255).round()}')];
    },
    draw: (c, s, v, t, p) {
      final add = v['mode'] == 0, cx = s.width / 2, cy = s.height / 2 + 6, R = math.min(s.width, s.height) * .27, d = R * .62;
      c.drawRect(Offset.zero & s, fi(add ? const Color(0xFF000000) : const Color(0xFFFFFFFF)));
      final cols = add
          ? [Color.fromARGB(255, v['r']!.round(), 0, 0), Color.fromARGB(255, 0, v['g']!.round(), 0), Color.fromARGB(255, 0, 0, v['b']!.round())]
          : [
              Color.fromARGB(255, 255 - v['c']!.round(), 255, 255),
              Color.fromARGB(255, 255, 255 - v['m']!.round(), 255),
              Color.fromARGB(255, 255, 255, 255 - v['y']!.round()),
            ];
      for (var k = 0; k < 3; k++) {
        final a = -math.pi / 2 + k * 2 * math.pi / 3;
        c.drawCircle(
          Offset(cx + math.cos(a) * d, cy + math.sin(a) * d),
          R,
          Paint()
            ..color = cols[k]
            ..blendMode = add ? BlendMode.plus : BlendMode.multiply,
        );
      }
      final lab = add ? ['red', 'green', 'blue'] : ['cyan', 'magenta', 'yellow'];
      for (var k = 0; k < 3; k++) {
        final a = -math.pi / 2 + k * 2 * math.pi / 3;
        tx(
          c,
          lab[k],
          Offset(cx + math.cos(a) * (d + R * .62), cy + math.sin(a) * (d + R * .62)),
          add ? const Color(0xFFFFFFFF) : const Color(0xFF333333),
          size: 12,
          ax: .5,
          ay: .5,
        );
      }
    },
  ),
  'telescope': (_) => LabSpec(
    height: 240,
    sliders: const [
      Sl('fo', 'Objective focal length fₒ', 20, 100, 60, step: 5, unit: 'cm'),
      Sl('fe', 'Eyepiece focal length fₑ', 2, 15, 6, step: 1, unit: 'cm'),
      Sl('a', 'Angle of the distant object α', 1, 6, 3, step: .5, unit: '°'),
    ],
    formula: 'M = β/α ≈ fₒ/fₑ;    tube length L = fₒ + fₑ  (normal adjustment: final image at infinity)',
    tryThis:
        'A long-focus objective and a short-focus eyepiece give a big magnification. The rays leave the eyepiece parallel (relaxed eye) and the image is upside down: fine for stars, not for a terrestrial telescope.',
    read: (v, t) {
      final fo = v['fo']!, fe = v['fe']!, a = v['a']! * deg, b = math.atan(fo / fe * math.tan(a));
      return [('M', '${fx(fo / fe, 1)}×'), ('L', '${fx(fo + fe, 0)} cm'), ('β', '${fx(b / deg, 1)}°'), ('image', 'inverted, at infinity')];
    },
    draw: (c, s, v, t, p) {
      final fo = v['fo']!, fe = v['fe']!, a = v['a']! * deg, ay = s.height / 2 + 6, x0 = 56.0, sc = (s.width - 150) / (fo + fe), xe = x0 + (fo + fe) * sc;
      c.drawLine(Offset(0, ay), Offset(s.width, ay), sk(p.line, 1));
      void lens(double x, double h, String lab) {
        final w = h * .16,
            path = Path()
              ..moveTo(x, ay - h)
              ..quadraticBezierTo(x + w * 2, ay, x, ay + h)
              ..quadraticBezierTo(x - w * 2, ay, x, ay - h);
        c.drawPath(path, fi(_glass));
        c.drawPath(path, sk(_glassEdge, 1.5));
        tx(c, lab, Offset(x, ay + h + 3), p.ink2, size: 10, ax: .5);
      }

      lens(x0, 64, 'objective');
      lens(xe, 40, 'eyepiece');
      // common focus F (objective) = F (eyepiece): the intermediate image forms there
      final xf = x0 + fo * sc, yI = ay + fo * sc * math.tan(a);
      c.drawCircle(Offset(xf, ay), 2.5, fi(p.ink));
      tx(c, 'Fₒ = Fₑ', Offset(xf, ay - 16), p.ink, size: 10, ax: .5);
      c.drawLine(Offset(xf, ay), Offset(xf, yI), sk(p.peach.deep, 2.5));
      tx(c, 'image', Offset(xf - 4, yI + 2), p.peach.deep, size: 10, ax: 1);
      final out = Offset(fe * sc, -(yI - ay)) / math.sqrt(fe * sc * fe * sc + (yI - ay) * (yI - ay));
      for (final h in const [-40.0, 0.0, 40.0]) {
        final hit = Offset(x0, ay + h), start = hit - Offset(math.cos(a), math.sin(a)) * 60;
        final d = Offset(xf, yI) - hit, ye = hit.dy + d.dy / d.dx * (xe - x0);
        c.drawLine(start, hit, sk(laser, 1.8));
        c.drawLine(hit, Offset(xe, ye), sk(laser, 1.8));
        midHead(c, start, hit, laser, 6);
        final end = Offset(xe, ye) + out * 120;
        c.drawLine(Offset(xe, ye), end, sk(laser, 1.8));
      }
      angArc(c, Offset(x0, ay), 26, math.pi, math.pi + a, p.blue.deep, 'α');
      final b = math.atan(fo / fe * math.tan(a));
      angArc(c, Offset(xe, ay), 22, 0, -b, p.blue.deep, 'β');
      tx(c, 'M = ${fx(fo / fe, 1)}×', Offset(s.width - 8, 8), p.ink, size: 12, ax: 1);
    },
  ),
  'lens': (_) => _lensLab(),
  'mirror': (m) => _mirrorLab(),
};

const _bands = [410.0, 450.0, 485.0, 530.0, 575.0, 600.0, 656.0];
double _nGlass(double nm) => 1.6 + .01 / math.pow(nm / 1000, 2);

({List<Offset> poly, Offset hit, Offset d}) _prismGeom(V v, Size s) {
  final A = v['A']! * deg, i = v['i']! * deg, hh = math.min(s.height * .72, s.width * .5 / math.tan(A / 2) / 2 * 1.4);
  final top = Offset(s.width * .44, s.height * .14), bl = top + Offset(-hh * math.tan(A / 2), hh), br = top + Offset(hh * math.tan(A / 2), hh);
  final e = top - bl, hit = bl + e * .55, nin = Offset(-e.dy, e.dx) / e.distance; // inward normal (right/down)
  Offset rot(Offset q, double a) => Offset(q.dx * math.cos(a) - q.dy * math.sin(a), q.dx * math.sin(a) + q.dy * math.cos(a));
  final d1 = rot(nin, i), d2 = rot(nin, -i);
  return (poly: [top, br, bl], hit: hit, d: d1.dy < d2.dy ? d1 : d2);
}

/// (wavelength, deviation° or null when TIR)
List<(double, double?)> _prismRun(V v, Size s) {
  final g = _prismGeom(v, s), o = g.hit - g.d * 500, out = <(double, double?)>[];
  for (final nm in v['w'] == 0 ? _bands : const [656.0]) {
    final tr = tracePoly(o, g.d, g.poly, _nGlass(nm));
    final escaped = !tr.tir && tr.pts.length >= 3;
    final dev = (math.atan2(tr.dir.dy, tr.dir.dx) - math.atan2(g.d.dy, g.d.dx)) / deg;
    out.add((nm, escaped ? dev.abs() : null));
  }
  out.sort((a, b) => b.$1.compareTo(a.$1));
  return out;
}

void _rightPrism(Canvas c, Size s, V v, Palette p) {
  final n = v['n']!, L = math.min(s.width * .5, s.height * .62), y = v['y']! / 100;
  late List<Offset> poly;
  late Offset o;
  if (v['turn'] == 0) {
    final a = Offset(s.width * .38, s.height * .1);
    poly = [a, a + Offset(0, L), a + Offset(L, L)];
    o = Offset(-10, a.dy + L * (.25 + .7 * y));
  } else {
    final a = Offset(s.width * .3, s.height * .06), h = math.min(L, s.height * .44);
    poly = [a, a + Offset(h, h), a + Offset(0, 2 * h)];
    o = Offset(-10, a.dy + h * (.15 + .7 * y));
  }
  c.drawPath(Path()..addPolygon(poly, true), fi(_glass));
  c.drawPath(Path()..addPolygon(poly, true), sk(_glassEdge, 2));
  final tr = tracePoly(o, const Offset(1, 0), poly, n);
  rayPath(c, tr.pts, tr.dir, laser);
  tx(c, 'n = ${n.toStringAsFixed(2)}', poly[0] + const Offset(6, 4), p.ink, size: 12);
  tx(c, n > math.sqrt2 ? 'TIR at 45°' : 'light escapes', Offset(s.width - 8, 8), n > math.sqrt2 ? p.sage.deep : laser, size: 13, ax: 1);
}

Color _mixCentre(V v) {
  if (v['mode'] == 0) return Color.fromARGB(255, v['r']!.round(), v['g']!.round(), v['b']!.round());
  return Color.fromARGB(255, 255 - v['c']!.round(), 255 - v['m']!.round(), 255 - v['y']!.round());
}

String _colorName(Color c) {
  final r = c.r, g = c.g, b = c.b, mx = math.max(r, math.max(g, b)), mn = math.min(r, math.min(g, b));
  if (mx < .12) return 'black';
  if (mx - mn < .12) return mx > .85 ? 'white' : 'grey';
  bool hi(double x) => x > mx * .6;
  final key = '${hi(r) ? 'r' : ''}${hi(g) ? 'g' : ''}${hi(b) ? 'b' : ''}';
  return switch (key) {
    'r' => 'red',
    'g' => 'green',
    'b' => 'blue',
    'rg' => r > g * 1.4 ? 'orange' : 'yellow',
    'gb' => 'cyan',
    'rb' => 'magenta',
    _ => 'pale (whitish)',
  };
}

// ---------------------------------------------------------------- lens and mirror ray diagrams
/// image distance for 1/f = 1/u + 1/v (real is positive); null at infinity
double? _img(double f, double u) => (u - f).abs() < 1e-6 ? null : 1 / (1 / f - 1 / u);

List<(String, String)> _imgRead(double f, double u, {required bool mirror}) {
  final im = _img(f, u);
  if (im == null) return [('', 'object at F: rays leave parallel, image at infinity')];
  final m = -im / u;
  final side = im > 0 ? (mirror ? 'in front (real)' : 'behind the lens (real)') : (mirror ? 'behind the mirror (virtual)' : 'same side as object (virtual)');
  return [
    ('v', '${fx(im.abs())} cm $side'),
    ('m = −v/u', fx(m, 2)),
    ('', '${im > 0 ? 'real, inverted' : 'virtual, upright'}, ${m.abs() > 1.005 ? 'magnified' : (m.abs() < .995 ? 'diminished' : 'same size')}'),
  ];
}

SimSpec _lensLab() => LabSpec(
  height: 280,
  opts: const [
    Opt('kind', ['Converging (convex)', 'Diverging (concave)']),
    Opt('mode', ['Object and image', 'Parallel rays']),
  ],
  sliders: [
    const Sl('f', 'Focal length |f|', 5, 20, 10, unit: 'cm'),
    Sl('u', 'Object distance u', 4, 60, 30, unit: 'cm', when: (v) => v['mode'] == 0),
  ],
  formulaOf: (v) => v['mode'] == 0 ? '1/f = 1/u + 1/v   (real is positive; f < 0 for a diverging lens)' : 'power P = 1/f  (f in metres, P in dioptres)',
  tryThis:
      'Converging lens: beyond 2F the image is real and smaller, between F and 2F real and bigger, inside F virtual and magnified (a magnifying glass). A diverging lens always gives a virtual, upright, smaller image.',
  drag: (v, at, s) {
    if (v['mode'] != 0) return;
    final g = _lensGeom(v, s), u = ((g.$1 - at.dx) / g.$2).roundToDouble();
    if (u >= 4) v['u'] = u.clamp(4, 60);
  },
  read: (v, t) {
    final f = v['kind'] == 0 ? v['f']! : -v['f']!;
    if (v['mode'] == 1) {
      return [
        ('f', '${fx(f, 0)} cm'),
        ('P = 1/f', '${fx(100 / f)} D'),
        ('', f > 0 ? 'rays meet at the real focus F' : 'rays spread as if from the virtual focus F'),
      ];
    }
    return _imgRead(f, v['u']!, mirror: false);
  },
  draw: (c, s, v, t, p) {
    final conv = v['kind'] == 0, f = conv ? v['f']! : -v['f']!, g = _lensGeom(v, s), sc = g.$2, ay = s.height / 2, x0 = g.$1;
    Offset at(double x, double y) => Offset(x0 + x * sc, ay - y * sc * 1.3);
    c.drawLine(Offset(0, ay), Offset(s.width, ay), sk(p.ink2, 1));
    final H = s.height / 2 - 14, w = 9.0;
    final lens = Path();
    if (conv) {
      lens
        ..moveTo(x0, ay - H)
        ..quadraticBezierTo(x0 + w * 2, ay, x0, ay + H)
        ..quadraticBezierTo(x0 - w * 2, ay, x0, ay - H);
    } else {
      lens
        ..moveTo(x0 - w, ay - H)
        ..lineTo(x0 + w, ay - H)
        ..quadraticBezierTo(x0 + 1, ay, x0 + w, ay + H)
        ..lineTo(x0 - w, ay + H)
        ..quadraticBezierTo(x0 - 1, ay, x0 - w, ay - H);
    }
    c.drawPath(lens, fi(_glass));
    c.drawPath(lens, sk(_glassEdge, 2));
    for (final k in [-2.0, -1.0, 1.0, 2.0]) {
      final q = at(k * v['f']!, 0);
      c.drawCircle(q, 3.5, fi(p.ink));
      tx(c, k.abs() == 1 ? 'F' : '2F', q + const Offset(0, 8), p.ink, size: 11.5, ax: .5);
    }
    const ray = laser, far = 2000.0;
    if (v['mode'] == 1) {
      for (final y in [-8.0, -4.0, 0.0, 4.0, 8.0]) {
        final a = at(-200, y * g.$3 / 6), b = at(0, y * g.$3 / 6);
        c.drawLine(a, b, sk(ray, 2));
        midHead(c, a, b, ray);
        final fp = conv ? at(f, 0) : at(f, 0);
        var d = conv ? fp - b : b - fp;
        if (y == 0) d = const Offset(1, 0);
        d = d / d.distance;
        c.drawLine(b, b + d * far, sk(ray, 2));
        if (!conv && y != 0) dsh(c, b, fp, ray.withValues(alpha: .6), 1.3, 5);
      }
      return;
    }
    final u = v['u']!, h = g.$3, ot = at(-u, h);
    arw(c, at(-u, 0), ot, p.sage.deep, 4, 11);
    tx(c, 'object', ot + const Offset(0, -16), p.sage.deep, size: 11.5, ax: .5);
    final im = _img(f, u);
    final hit1 = at(0, h);
    // 1: parallel, then through F' (converging) or away from F (diverging)
    c.drawLine(ot, hit1, sk(ray, 2));
    midHead(c, ot, hit1, ray);
    final d1 = conv ? (at(f, 0) - hit1) : (hit1 - at(f, 0));
    c.drawLine(hit1, hit1 + d1 / d1.distance * far, sk(ray, 2));
    // 2: through the optical centre
    final o = at(0, 0), d2 = o - ot;
    c.drawLine(ot, o + d2 / d2.distance * far, sk(ray, 2));
    midHead(c, ot, o, ray);
    // 3: towards F (object side for converging, far side for diverging), leaves parallel
    final fq = conv ? at(-f, 0) : at(-f, 0);
    final d3 = fq - ot;
    if (d3.dx.abs() > 1) {
      final k3 = (x0 - ot.dx) / d3.dx;
      if (k3 > 0) {
        final hit3 = ot + d3 * k3;
        if ((hit3.dy - ay).abs() < H + 40) {
          c.drawLine(ot, hit3, sk(ray, 2));
          c.drawLine(hit3, hit3 + const Offset(far, 0), sk(ray, 2));
          if (!conv) dsh(c, hit3, fq, ray.withValues(alpha: .5), 1.2, 5);
          if (im != null && im < 0) dsh(c, hit3, hit3 - const Offset(far, 0), ray.withValues(alpha: .5), 1.2, 5);
        }
      }
    }
    if (im == null) return;
    if (im < 0) {
      dsh(c, hit1, hit1 - d1 / d1.distance * far, ray.withValues(alpha: .5), 1.2, 5);
      dsh(c, o, o - d2 / d2.distance * far, ray.withValues(alpha: .5), 1.2, 5);
    }
    final hi = -im / u * h, ib = at(im, 0), itp = at(im, hi);
    if (ib.dx > 0 && ib.dx < s.width && (itp.dy - ay).abs() < ay - 4) {
      if (im < 0) {
        dsh(c, ib, itp, p.lilac.deep, 3.5, 5);
      } else {
        arw(c, ib, itp, p.lilac.deep, 4, 11);
      }
      tx(c, im < 0 ? 'virtual image' : 'image', itp + Offset(0, hi > 0 ? -16 : 4), p.lilac.deep, size: 11.5, ax: .5);
    } else {
      tx(c, 'image off the picture', Offset(s.width - 8, 8), p.lilac.deep, size: 11.5, ax: 1);
    }
  },
);

SimSpec _mirrorLab() => LabSpec(
  height: 280,
  opts: const [
    Opt('kind', ['Concave', 'Convex', 'Plane']),
    Opt('mode', ['Object and image', 'Parallel rays']),
  ],
  sliders: <Sl>[
    Sl('f', 'Focal length |f|', 5, 20, 10, unit: 'cm', when: (v) => v['kind'] != 2),
    Sl('u', 'Object distance u', 4, 60, 30, unit: 'cm', when: (v) => v['mode'] == 0),
  ],
  formulaOf: (v) => v['kind'] == 2 ? 'plane mirror: v = u, m = 1' : '1/f = 1/u + 1/v,  f = R/2   (real is positive; f < 0 for convex)',
  tryThis:
      'Concave: move the object inside F and the image becomes virtual, upright and magnified (a shaving mirror). Convex: the image is always virtual, upright and smaller, which is why it is used as a car wing mirror.',
  drag: (v, at, s) {
    if (v['mode'] != 0) return;
    final g = _mGeom(v, s), u = ((g.$1 - at.dx) / g.$2).roundToDouble();
    if (u >= 4) v['u'] = u.clamp(4, 60);
  },
  read: (v, t) {
    final kind = v['kind']!;
    if (v['mode'] == 1) {
      return [
        if (kind == 2)
          ('', 'parallel rays stay parallel: no focus')
        else
          ('F', kind == 0 ? '${fx(v['f']!, 0)} cm in front (real)' : '${fx(v['f']!, 0)} cm behind (virtual)'),
        if (kind != 2) ('R = 2f', '${fx(2 * v['f']!, 0)} cm'),
      ];
    }
    if (kind == 2) return [('v = u', '${fx(v['u']!, 0)} cm behind'), ('m', '1'), ('', 'virtual, upright, same size')];
    return _imgRead(kind == 0 ? v['f']! : -v['f']!, v['u']!, mirror: true);
  },
  draw: (c, s, v, t, p) {
    final kind = v['kind']!, g = _mGeom(v, s), x0 = g.$1, sc = g.$2, ay = s.height / 2;
    final f = kind == 2 ? 1e9 : (kind == 0 ? v['f']! : -v['f']!);
    Offset at(double x, double y) => Offset(x0 + x * sc, ay - y * sc * 1.3); // x < 0: in front
    c.drawLine(Offset(0, ay), Offset(s.width, ay), sk(p.ink2, 1));
    final H = s.height / 2 - 14, sag = kind == 2 ? 0.0 : (kind == 0 ? -10.0 : 10.0);
    final m = Path()
      ..moveTo(x0 + sag, ay - H)
      ..quadraticBezierTo(x0 - sag, ay, x0 + sag, ay + H);
    c.drawPath(m, sk(p.blue.deep, 4));
    for (var y = ay - H + 6; y < ay + H; y += 12) {
      final k = (y - ay) / H, xx = x0 + sag * k * k + 3;
      c.drawLine(Offset(xx, y), Offset(xx + 8, y - 7), sk(p.ink2, 1.2));
    }
    if (kind != 2) {
      for (final k in [1.0, 2.0]) {
        final q = at(-k * f, 0);
        c.drawCircle(q, 3.5, fi(p.ink));
        tx(c, k == 1 ? 'F' : 'C', q + const Offset(0, 8), p.ink, size: 11.5, ax: .5);
      }
    }
    const ray = laser, far = 2000.0;
    if (v['mode'] == 1) {
      for (final y in [-8.0, -4.0, 4.0, 8.0]) {
        final a = at(-300, y * g.$3 / 6), b = at(0, y * g.$3 / 6);
        c.drawLine(a, b, sk(ray, 2));
        midHead(c, a, b, ray);
        if (kind == 2) {
          c.drawLine(b, a, sk(ray, 2));
          continue;
        }
        final fq = at(-f, 0);
        final d = kind == 0 ? fq - b : b - fq;
        c.drawLine(b, b + d / d.distance * far, sk(ray, 2));
        if (kind == 1) dsh(c, b, fq, ray.withValues(alpha: .6), 1.3, 5);
      }
      return;
    }
    final u = v['u']!, h = g.$3, ot = at(-u, h);
    arw(c, at(-u, 0), ot, p.sage.deep, 4, 11);
    tx(c, 'object', ot + const Offset(0, -16), p.sage.deep, size: 11.5, ax: .5);
    final im = kind == 2 ? -u : _img(f, u);
    // 1: parallel to the axis
    final h1 = at(0, h);
    c.drawLine(ot, h1, sk(ray, 2));
    midHead(c, ot, h1, ray);
    final d1 = kind == 2 ? const Offset(-1, 0) : (kind == 0 ? at(-f, 0) - h1 : h1 - at(-f, 0));
    final u1 = d1 / d1.distance;
    c.drawLine(h1, h1 + u1 * far, sk(ray, 2));
    // 2: to the pole, reflected symmetrically
    final o = at(0, 0), din = (o - ot) / (o - ot).distance, u2 = Offset(-din.dx, din.dy);
    c.drawLine(ot, o, sk(ray, 2));
    midHead(c, ot, o, ray);
    c.drawLine(o, o + u2 * far, sk(ray, 2));
    if (im == null) return;
    if (im < 0) {
      dsh(c, h1, h1 - u1 * far, ray.withValues(alpha: .5), 1.2, 5);
      dsh(c, o, o - u2 * far, ray.withValues(alpha: .5), 1.2, 5);
    }
    final hi = -im / u * h, ib = at(-im, 0), itp = at(-im, hi);
    if (ib.dx > 0 && ib.dx < s.width && (itp.dy - ay).abs() < ay - 4) {
      if (im < 0) {
        dsh(c, ib, itp, p.lilac.deep, 3.5, 5);
      } else {
        arw(c, ib, itp, p.lilac.deep, 4, 11);
      }
      tx(c, im < 0 ? 'virtual image' : 'image', itp + Offset(0, hi > 0 ? -16 : 4), p.lilac.deep, size: 11.5, ax: .5);
    } else {
      tx(c, 'image off the picture', const Offset(8, 8), p.lilac.deep, size: 11.5);
    }
  },
);

/// lens x position, px per cm and object height (cm): zoomed so the object and image fill the picture
(double, double, double) _lensGeom(V v, Size s) {
  final f = v['f']!, u = v['u']!, fs = v['kind'] == 0 ? f : -f, im = _img(fs, u);
  var L = v['mode'] == 1 ? 2.6 * f : math.max(u + 6, 2.3 * f);
  if (v['mode'] == 0 && im != null && im.abs() < 90) L = math.max(L, im.abs() + 6);
  L = L.clamp(20.0, 90.0);
  final sc = (s.width / 2 - 12) / L;
  return (s.width / 2, sc, (s.height / 2) * .38 / (sc * 1.3));
}

/// mirror x position, px per cm and object height (cm)
(double, double, double) _mGeom(V v, Size s) {
  final u = v['u']!, kind = v['kind']!;
  double front, back;
  if (kind == 2) {
    front = back = v['mode'] == 1 ? 30 : u + 8;
  } else {
    final f = v['f']!, im = _img(kind == 0 ? f : -f, u);
    front = v['mode'] == 1 ? 2.6 * f : math.max(u + 6, kind == 0 ? 2.3 * f : 10);
    back = kind == 1 ? 2.3 * f : 10;
    if (v['mode'] == 0 && im != null && im.abs() < 90) {
      im > 0 ? front = math.max(front, im + 6) : back = math.max(back, -im + 6);
    }
    front = front.clamp(15.0, 90.0);
    back = back.clamp(8.0, 90.0);
  }
  final sc = (s.width - 20) / (front + back);
  return (10 + front * sc, sc, (s.height / 2) * .38 / (sc * 1.3));
}

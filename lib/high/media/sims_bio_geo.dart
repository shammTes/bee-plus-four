// Biology + geography sims.
import 'dart:math' as math;

import 'package:flutter/widgets.dart';

import 'sims.dart';

double _bell(double x, double mu, double sd) => math.exp(-math.pow((x - mu) / sd, 2) / 2);

/// enzyme activity (0..1): rises ~2× per 10 °C up to the optimum, then denatures quickly
double enzymeAct(double t, double ph, double optT, double optPh) {
  final up = math.pow(2, (t - optT) / 10).toDouble(), down = math.max(0.0, 1 - math.pow((t - optT) / 16, 2).toDouble());
  return (t <= optT ? up : down) * _bell(ph, optPh, 1.3);
}

const _months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
String dayName(int d) {
  const len = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];
  var m = 0;
  while (m < 11 && d > len[m]) {
    d -= len[m];
    m++;
  }
  return '$d ${_months[m]}';
}

final Map<String, SimSpec Function(Map<String, dynamic>)> bioGeoSims = {
  'enzyme': (m) {
    final optPh = (m['optPh'] as num?)?.toDouble() ?? 7, name = '${m['name'] ?? 'amylase'}';
    return SimSpec(
      params: [
        const Prm('T', 'Temperature', 0, 70, 20, step: 5, unit: '°C'),
        Prm('ph', 'pH', 1, 13, optPh, step: .5),
      ],
      out: (v) {
        final a = enzymeAct(v['T']!, v['ph']!, 37, optPh);
        return [
          ('Activity of $name', '${(a * 100).round()} %'),
          ('', v['T']! > 50 ? 'denatured: active site lost its shape' : (v['T']! < 10 ? 'slow: few collisions' : (a > .85 ? 'near the optimum' : ''))),
        ];
      },
      paint: (c, s, v, t, p) {
        final pl = Plot(c, s, 0, 70, 0, 100, p, xl: 'temperature (°C)', yl: 'activity (%)', xt: 7);
        pl.curve((x) => 100 * enzymeAct(x, v['ph']!, 37, optPh), p.sage.deep);
        pl.dot(v['T']!, 100 * enzymeAct(v['T']!, v['ph']!, 37, optPh), p.peach.deep);
      },
    );
  },
  'photosynthesis': (_) => SimSpec(
    params: const [
      Prm('L', 'Light intensity', 0, 100, 40, step: 5, unit: '%'),
      Prm('co2', 'CO₂ level', 1, 3, 1, fmt: _co2),
    ],
    out: (v) {
      final r = _ps(v['L']!, v['co2']!);
      return [('Rate', '${f1(r)} units'), ('Limiting factor', v['L']! < 25 * v['co2']! ? 'light' : 'CO₂ (or temperature)')];
    },
    paint: (c, s, v, t, p) {
      final pl = Plot(c, s, 0, 100, 0, 30, p, xl: 'light intensity (%)', yl: 'rate of photosynthesis');
      for (final k in [1.0, 2.0, 3.0]) {
        pl.curve((x) => _ps(x, k), k == v['co2'] ? p.sage.deep : p.line, w: k == v['co2'] ? 3.5 : 2);
      }
      pl.dot(v['L']!, _ps(v['L']!, v['co2']!), p.peach.deep);
    },
  ),
  'punnett': (m) {
    final dom = '${m['dom'] ?? 'tall'}', rec = '${m['rec'] ?? 'short'}', a = '${m['allele'] ?? 'T'}';
    String g(double v) => ['$a$a', '$a${a.toLowerCase()}', '${a.toLowerCase()}${a.toLowerCase()}'][v.toInt()];
    return SimSpec(
      height: 250,
      params: [
        Prm('p1', 'Parent 1', 0, 2, 1, fmt: g),
        Prm('p2', 'Parent 2', 0, 2, 1, fmt: g),
      ],
      out: (v) {
        final kids = [
          for (final x in g(v['p1']!).split(''))
            for (final y in g(v['p2']!).split('')) x + y,
        ];
        final d = kids.where((k) => k.contains(a)).length;
        return [
          ('$dom : $rec', '$d : ${4 - d}'),
          ('Genotypes', {for (final k in kids) (k.split('')..sort()).join()}.map((k) => '${kids.where((x) => (x.split('')..sort()).join() == k).length}×$k').join('  ')),
        ];
      },
      paint: (c, s, v, t, p) {
        final g1 = g(v['p1']!).split(''), g2 = g(v['p2']!).split(''), cell = math.min(70.0, (s.height - 60) / 2), x0 = s.width / 2 - cell, y0 = 50.0;
        for (var i = 0; i < 2; i++) {
          txt(c, g1[i], Offset(x0 + cell * i + cell / 2, y0 - 22), p.blue.deep, size: 22, center: true);
          txt(c, g2[i], Offset(x0 - 22, y0 + cell * i + cell / 2), p.peach.deep, size: 22, center: true);
        }
        for (var i = 0; i < 2; i++) {
          for (var j = 0; j < 2; j++) {
            final k = [g1[i], g2[j]]..sort(), r = Rect.fromLTWH(x0 + cell * i, y0 + cell * j, cell, cell).deflate(3);
            c.drawRRect(RRect.fromRectAndRadius(r, const Radius.circular(12)), fl(k.join().contains(a) ? p.sage.tile : p.butter.tile));
            txt(c, k.join(), r.center, p.ink, size: 22, center: true);
          }
        }
        txt(c, 'gametes of parent 1 across, parent 2 down', Offset(s.width / 2, s.height - 16), p.ink2, size: 11, center: true);
      },
    );
  },
  'pyramid': (_) => SimSpec(
    params: const [
      Prm('e', 'Energy passed on', 5, 20, 10, unit: '%'),
      Prm('E', 'Producer energy', 1000, 20000, 10000, step: 1000, unit: 'kJ'),
    ],
    out: (v) => [('Top carnivore gets', '${f1(v['E']! * math.pow(v['e']! / 100, 3))} kJ'), ('', 'the rest is lost as heat, movement and waste')],
    paint: (c, s, v, t, p) {
      const names = ['Producers (plants)', 'Herbivores', 'Carnivores', 'Top carnivores'];
      final tones = [p.sage, p.butter, p.peach, p.lilac], h = (s.height - 20) / 4;
      for (var i = 0; i < 4; i++) {
        final e = v['E']! * math.pow(v['e']! / 100, i), w = math.max(26.0, (s.width - 30) * math.pow(e / v['E']!, .35));
        final r = Rect.fromCenter(center: Offset(s.width / 2, s.height - 10 - h * (i + .5)), width: w, height: h - 6);
        c.drawRRect(RRect.fromRectAndRadius(r, const Radius.circular(10)), fl(tones[i].mid));
        txt(c, '${names[i]}: ${e >= 10 ? e.round() : f1(e.toDouble())} kJ', r.center, p.ink, size: 12.5, center: true);
      }
    },
  ),
  'seasons': (m) => SimSpec(
    height: 250,
    params: [
      const Prm('d', 'Day of the year', 1, 365, 172, fmt: _day),
      Prm('lat', 'Latitude', -60, 60, (m['lat'] as num?)?.toDouble() ?? 15, unit: '°'),
    ],
    out: (v) {
      final dec = 23.44 * math.sin(2 * math.pi * (284 + v['d']!) / 365), phi = v['lat']! * math.pi / 180, dr = dec * math.pi / 180;
      final x = (-math.tan(phi) * math.tan(dr)).clamp(-1.0, 1.0), len = 24 / math.pi * math.acos(x);
      return [
        ('Sun overhead at', '${f1(dec.abs())}° ${dec >= 0 ? 'N' : 'S'}'),
        ('Day length', '${len.floor()} h ${((len % 1) * 60).round()} min'),
        ('Noon sun height', '${f1(90 - (v['lat']! - dec).abs())}°'),
      ];
    },
    paint: (c, s, v, t, p) {
      final o = Offset(s.width / 2, s.height / 2), rx = s.width * .36, ry = s.height * .32;
      c.drawOval(Rect.fromCenter(center: o, width: 2 * rx, height: 2 * ry), st(p.line, 1.5));
      c.drawCircle(o, 22, fl(const Color(0xFFFFC107)));
      txt(c, 'Sun', o, p.ink, size: 12, center: true);
      // day 172 (June solstice): northern hemisphere tilted towards the Sun -> Earth to the left of the Sun, N pole tipped right
      final a = 2 * math.pi * (v['d']! - 172) / 365, e = o + Offset(-math.cos(a) * rx, math.sin(a) * ry);
      c.drawCircle(e, 18, fl(p.blue.mid));
      final lit = (o - e) / (o - e).distance;
      c.drawArc(Rect.fromCircle(center: e, radius: 18), math.atan2(lit.dy, lit.dx) + math.pi / 2, math.pi, true, fl(const Color(0x88202040)));
      const tilt = 23.44 * math.pi / 180;
      c.drawLine(e + Offset(-math.sin(tilt), math.cos(tilt)) * 28, e + Offset(math.sin(tilt), -math.cos(tilt)) * 28, st(p.ink, 2));
      txt(c, 'N', e + Offset(math.sin(tilt), -math.cos(tilt)) * 36, p.ink, size: 12, center: true);
      txt(c, dayName(v['d']!.toInt()), e + const Offset(0, 30), p.ink, size: 12, center: true);
      for (final (d, n) in [(172, 'Jun solstice'), (355, 'Dec solstice'), (80, 'Mar equinox'), (266, 'Sep equinox')]) {
        final b = 2 * math.pi * (d - 172) / 365, q = o + Offset(-math.cos(b) * rx, math.sin(b) * ry);
        c.drawCircle(q, 3, fl(p.ink2));
        txt(c, n, q + Offset(q.dx < o.dx - 5 ? -6 : 6, q.dy < o.dy ? -16 : 6), p.ink2, size: 10.5, right: q.dx < o.dx - 5, center: false);
      }
    },
  ),
  'contour': (_) => SimSpec(
    height: 300,
    params: const [
      Prm('H', 'Hill height', 200, 800, 500, step: 50, unit: 'm'),
      Prm('I', 'Contour interval', 50, 200, 100, step: 50, unit: 'm'),
      Prm('k', 'Shape', 1, 3, 2, fmt: _shapeName),
    ],
    out: (v) => [
      ('Contour lines', '${(v['H']! / v['I']!).floor()}'),
      (
        '',
        v['k'] == 1
            ? 'concave slope: lines close together near the top'
            : (v['k'] == 3 ? 'convex slope: lines close together near the bottom' : 'even slope: evenly spaced lines'),
      ),
    ],
    paint: (c, s, v, t, p) {
      final H = v['H']!, I = v['I']!, k = [0, .5, 1.0, 2.2][v['k']!.toInt()], R = s.width * .42, ox = s.width / 2, oy = 70.0;
      double r(double h) => R * math.pow(1 - h / H, k == 1 ? 1 : k).toDouble();
      // plan view (squashed circles) + section below
      for (var h = I; h < H; h += I) {
        c.drawOval(Rect.fromCenter(center: Offset(ox, oy), width: 2 * r(h), height: r(h) * .55), st(p.peach.deep, 1.6));
        txt(c, '${h.toInt()}', Offset(ox + r(h) - 4, oy - 6), p.peach.deep, size: 9.5, right: true);
      }
      c.drawCircle(Offset(ox, oy), 3, fl(p.ink));
      txt(c, '▲ ${H.toInt()} m', Offset(ox + 6, oy - 14), p.ink, size: 11);
      final base = s.height - 16, top = oy + 70, path = Path()..moveTo(ox - R, base);
      for (var i = 0; i <= 100; i++) {
        final x = -R + 2 * R * i / 100, hh = x.abs() >= R ? 0.0 : H * (1 - math.pow(x.abs() / R, 1 / (k == 1 ? 1 : k)));
        path.lineTo(ox + x, base - (base - top) * hh / H);
      }
      path.lineTo(ox + R, base);
      c.drawPath(path, fl(p.sage.tile));
      c.drawPath(path, st(p.sage.deep, 2));
      for (var h = I; h < H; h += I) {
        final y = base - (base - top) * h / H;
        dashed(c, Offset(ox - r(h), oy + r(h) * .275), Offset(ox - r(h), y), st(p.line, 1));
        dashed(c, Offset(ox + r(h), oy + r(h) * .275), Offset(ox + r(h), y), st(p.line, 1));
      }
      txt(c, 'plan (map)', const Offset(10, 8), p.ink2, size: 11);
      txt(c, 'cross-section', Offset(10, top - 4), p.ink2, size: 11);
    },
  ),
  'mapscale': (_) => SimSpec(
    height: 150,
    params: const [
      Prm('s', 'Map scale', 0, 5, 2, fmt: _scaleName),
      Prm('d', 'Distance on the map', 1, 20, 4, step: .5, unit: 'cm'),
    ],
    out: (v) {
      final n = _scales[v['s']!.toInt()], km = v['d']! * n / 100000;
      return [
        ('Real distance', km >= 1 ? '${km.toStringAsFixed(km >= 10 ? 0 : 2)} km' : '${(km * 1000).round()} m'),
        ('1 cm on the map =', n >= 100000 ? '${n / 100000} km' : '${n ~/ 100} m'),
      ];
    },
    paint: (c, s, v, t, p) {
      final n = _scales[v['s']!.toInt()], cm = (s.width - 40) / 20;
      final y = 60.0;
      for (var i = 0; i <= 20; i++) {
        c.drawLine(Offset(20 + i * cm, y), Offset(20 + i * cm, y - (i % 5 == 0 ? 16 : 8)), st(p.ink, 1.5));
      }
      c.drawLine(Offset(20, y), Offset(20 + 20 * cm, y), st(p.ink, 2));
      c.drawRRect(RRect.fromRectAndRadius(Rect.fromLTWH(20, y + 8, v['d']! * cm, 14), const Radius.circular(7)), fl(p.peach.deep));
      txt(c, '0', Offset(20, y - 30), p.ink2, size: 11, center: true);
      txt(c, '5 cm', Offset(20 + 5 * cm, y - 30), p.ink2, size: 11, center: true);
      txt(c, '10 cm', Offset(20 + 10 * cm, y - 30), p.ink2, size: 11, center: true);
      txt(c, 'RF 1 : ${_fmtN(n)}', Offset(20, y + 36), p.ink, size: 15);
    },
  ),
  'population': (m) => SimSpec(
    params: [
      Prm('r', 'Growth rate', .5, 4, (m['r'] as num?)?.toDouble() ?? 2.5, step: .1, unit: '% per year'),
      const Prm('y', 'Years ahead', 0, 100, 35, step: 5),
    ],
    out: (v) => [('Doubling time ≈ 70 / r', '${(70 / v['r']!).round()} years'), ('Population ×', f2(math.exp(v['r']! / 100 * v['y']!)))],
    paint: (c, s, v, t, p) {
      final pl = Plot(c, s, 0, 100, 0, 20, p, xl: 'years', yl: '× starting population', xt: 5, yt: 4);
      for (final r in [1.0, 2.0, 3.0]) {
        pl.curve((x) => math.exp(r / 100 * x), p.line, w: 1.5);
      }
      pl.curve((x) => math.exp(v['r']! / 100 * x), p.blue.deep);
      pl.dot(v['y']!, math.exp(v['r']! / 100 * v['y']!).clamp(0, 20), p.peach.deep);
    },
  ),
};

double _ps(double l, double co2) => (8 + 7 * co2) * l / (l + 18 + 6 * co2);
String _co2(double v) => ['', 'low', 'medium', 'high'][v.toInt()];
String _day(double v) => dayName(v.toInt());
String _shapeName(double v) => ['', 'concave', 'even', 'convex'][v.toInt()];
const _scales = [10000, 25000, 50000, 100000, 250000, 1000000];
String _scaleName(double v) => '1 : ${_fmtN(_scales[v.toInt()])}';
String _fmtN(int n) => n.toString().replaceAllMapped(RegExp(r'\B(?=(\d{3})+(?!\d))'), (m) => ',');

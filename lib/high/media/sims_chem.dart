// Chemistry sims.
import 'dart:math' as math;

import 'package:flutter/widgets.dart';

import 'mesh3d.dart';
import 'sims.dart';

const _els = [
  ('H', 'Hydrogen'),
  ('He', 'Helium'),
  ('Li', 'Lithium'),
  ('Be', 'Beryllium'),
  ('B', 'Boron'),
  ('C', 'Carbon'),
  ('N', 'Nitrogen'),
  ('O', 'Oxygen'),
  ('F', 'Fluorine'),
  ('Ne', 'Neon'),
  ('Na', 'Sodium'),
  ('Mg', 'Magnesium'),
  ('Al', 'Aluminium'),
  ('Si', 'Silicon'),
  ('P', 'Phosphorus'),
  ('S', 'Sulphur'),
  ('Cl', 'Chlorine'),
  ('Ar', 'Argon'),
  ('K', 'Potassium'),
  ('Ca', 'Calcium'),
];
// most common neutron numbers for Z = 1..20
const _n0 = [0, 2, 4, 5, 6, 6, 7, 8, 10, 10, 12, 12, 14, 14, 16, 16, 18, 22, 20, 20];

List<int> shells(int e) {
  final out = <int>[];
  for (final cap in [2, 8, 8, 2]) {
    if (e <= 0) break;
    out.add(math.min(cap, e));
    e -= cap;
  }
  return out;
}

/// pH during titration of 25 mL 0.1 M acid with 0.1 M NaOH
double titrPH(double vb, bool weak) {
  const na = 2.5, ka = 1.8e-5;
  final nb = .1 * vb, vt = 25 + vb;
  if (weak) {
    if (nb < 1e-9) return -math.log(math.sqrt(ka * .1)) / math.ln10;
    if (nb < na - 1e-9) return -math.log(ka) / math.ln10 + math.log(nb / (na - nb)) / math.ln10;
    if ((nb - na).abs() < 1e-9) return 14 + math.log(math.sqrt(1e-14 / ka * na / vt)) / math.ln10;
  } else {
    if (nb < na - 1e-9) return -math.log((na - nb) / vt) / math.ln10;
    if ((nb - na).abs() < 1e-9) return 7;
  }
  return 14 + math.log((nb - na) / vt) / math.ln10;
}

Color phColor(double ph) {
  const stops = [
    Color(0xFFE53935),
    Color(0xFFFF7043),
    Color(0xFFFFB300),
    Color(0xFFFFEE58),
    Color(0xFF9CCC65),
    Color(0xFF43A047),
    Color(0xFF26A69A),
    Color(0xFF1E88E5),
    Color(0xFF3949AB),
    Color(0xFF6A1B9A),
  ];
  final x = (ph / 14 * (stops.length - 1)).clamp(0, stops.length - 1.001), i = x.floor();
  return Color.lerp(stops[i], stops[i + 1], (x - i).toDouble())!;
}

final Map<String, SimSpec Function(Map<String, dynamic>)> chemSims = {
  'atom': (_) => SimSpec(
    animated: true,
    height: 280,
    params: const [Prm('p', 'Protons', 1, 20, 6), Prm('n', 'Neutrons', 0, 22, 6), Prm('e', 'Electrons', 0, 20, 6)],
    out: (v) {
      final z = v['p']!.toInt(), n = v['n']!.toInt(), e = v['e']!.toInt(), q = z - e, el = _els[z - 1];
      return [
        ('Element', '${el.$2} (${el.$1})'),
        ('Mass number A', '${z + n}'),
        ('Charge', q == 0 ? 'neutral atom' : '${q > 0 ? '+' : '−'}${q.abs() == 1 ? '' : q.abs()} ion'),
        ('Electrons', shells(e).join(',')),
        if (n != _n0[z - 1]) ('', 'isotope: usual neutrons ${_n0[z - 1]}'),
      ];
    },
    paint: (c, s, v, t, p) {
      final o = s.center(Offset.zero), z = v['p']!.toInt(), n = v['n']!.toInt(), e = v['e']!.toInt();
      final tot = z + n, rn = 8 + 3.2 * math.sqrt(tot.toDouble());
      final rnd = math.Random(7);
      for (var i = 0; i < tot; i++) {
        final a = rnd.nextDouble() * 2 * math.pi, r = math.sqrt(rnd.nextDouble()) * (rn - 6);
        c.drawCircle(o + Offset(math.cos(a), math.sin(a)) * r, 5.5, fl(i < z ? p.peach.deep : p.ink2));
      }
      final sh = shells(e), step = (s.height / 2 - rn - 10) / 4;
      for (var k = 0; k < 4; k++) {
        c.drawCircle(o, rn + step * (k + 1), st(k < sh.length ? p.blue.mid : p.line, 1.5));
      }
      for (var k = 0; k < sh.length; k++) {
        for (var j = 0; j < sh[k]; j++) {
          final a = 2 * math.pi * j / sh[k] + t * (1.2 - k * .2);
          c.drawCircle(o + Offset(math.cos(a), math.sin(a)) * (rn + step * (k + 1)), 6, fl(p.blue.deep));
        }
      }
      txt(
        c,
        '${_els[z - 1].$1}${z - e == 0 ? '' : (z - e > 0 ? '${z - e > 1 ? z - e : ''}+' : '${e - z > 1 ? e - z : ''}−')}',
        const Offset(16, 12),
        p.ink,
        size: 28,
        w: FontWeight.w900,
      );
      txt(c, '● proton  ● neutron  ● electron', Offset(16, s.height - 22), p.ink2, size: 11);
    },
  ),
  'titration': (m) {
    final weak = m['weak'] == true;
    return SimSpec(
      params: const [Prm('vb', 'NaOH added', 0, 50, 0, step: .5, unit: 'mL')],
      out: (v) {
        final ph = titrPH(v['vb']!, weak);
        return [
          ('pH', f2(ph)),
          ('Phenolphthalein', ph >= 8.2 ? 'pink' : 'colourless'),
          ('', v['vb']! < 25 ? 'before equivalence' : (v['vb'] == 25 ? 'equivalence point (25 mL)' : 'excess base')),
        ];
      },
      paint: (c, s, v, t, p) {
        final pl = Plot(c, s, 0, 50, 0, 14, p, xl: 'volume of 0.1 M NaOH (mL)', yl: 'pH', yt: 7, xt: 5, right: 70);
        pl.curve((x) => titrPH(x, weak), p.blue.deep, n: 300);
        dashed(c, pl.at(25, 0), pl.at(25, 14), st(p.line, 1.2));
        final ph = titrPH(v['vb']!, weak);
        pl.dot(v['vb']!, ph, p.peach.deep);
        // flask
        final fx = s.width - 36, fy = s.height - 60.0;
        final fcol = ph >= 8.2 ? Color.fromARGB((80 + 12 * (ph - 8.2)).clamp(80, 200).toInt(), 230, 60, 150) : const Color(0x3390CAF9);
        c.drawPath(
          Path()
            ..moveTo(fx - 8, fy - 40)
            ..lineTo(fx + 8, fy - 40)
            ..lineTo(fx + 8, fy - 20)
            ..lineTo(fx + 26, fy + 20)
            ..lineTo(fx - 26, fy + 20)
            ..lineTo(fx - 8, fy - 20)
            ..close(),
          fl(fcol),
        );
        c.drawPath(
          Path()
            ..moveTo(fx - 8, fy - 40)
            ..lineTo(fx - 8, fy - 20)
            ..lineTo(fx - 26, fy + 20)
            ..lineTo(fx + 26, fy + 20)
            ..lineTo(fx + 8, fy - 20)
            ..lineTo(fx + 8, fy - 40),
          st(p.ink, 2),
        );
        txt(c, weak ? 'ethanoic acid' : 'HCl', Offset(fx, fy + 34), p.ink2, size: 11, center: true);
      },
    );
  },
  'gaslaw': (_) => SimSpec(
    animated: true,
    params: const [
      Prm('V', 'Volume', 2, 10, 6, unit: 'L'),
      Prm('T', 'Temperature', 200, 600, 300, step: 10, unit: 'K'),
    ],
    out: (v) {
      final P = 8.314 * v['T']! / v['V']!;
      return [('Pressure (1 mol)', '${f1(P * 1)} kPa'), ('PV/T', f2(P * v['V']! / v['T']!)), ('', 'T in °C: ${(v['T']! - 273).round()}')];
    },
    paint: (c, s, v, t, p) {
      final box = Rect.fromLTRB(s.width * .25, 20, s.width * .75, s.height - 16), top = box.bottom - (box.height - 10) * v['V']! / 10;
      c.drawRect(Rect.fromLTRB(box.left, top, box.right, box.bottom), fl(Color.lerp(const Color(0x2242A5F5), const Color(0x33EF5350), (v['T']! - 200) / 400)!));
      c.drawPath(
        Path()
          ..moveTo(box.left, box.top)
          ..lineTo(box.left, box.bottom)
          ..lineTo(box.right, box.bottom)
          ..lineTo(box.right, box.top),
        st(p.ink, 3),
      );
      c.drawRect(Rect.fromLTRB(box.left + 2, top - 12, box.right - 2, top), fl(p.ink2));
      c.drawLine(Offset(box.center.dx, top - 12), Offset(box.center.dx, box.top - 20), st(p.ink2, 6));
      final sp = math.sqrt(v['T']! / 300) * 60, rnd = math.Random(3), w = box.width - 16, h = box.bottom - top - 16;
      for (var i = 0; i < 26; i++) {
        final vx = (rnd.nextDouble() - .5) * 2 * sp, vy = (rnd.nextDouble() - .5) * 2 * sp;
        double bounce(double x0, double vv, double len) {
          final x = (x0 + vv * t) % (2 * len);
          return (x < 0 ? x + 2 * len : x) > len ? 2 * len - ((x < 0 ? x + 2 * len : x)) : (x < 0 ? x + 2 * len : x);
        }

        c.drawCircle(Offset(box.left + 8 + bounce(rnd.nextDouble() * w, vx, w), top + 8 + bounce(rnd.nextDouble() * h, vy, h)), 5, fl(p.blue.deep));
      }
    },
  ),
  'rate': (_) => SimSpec(
    animated: true,
    params: const [
      Prm('T', 'Temperature', 20, 80, 20, step: 10, unit: '°C'),
      Prm('c', 'Concentration', 1, 5, 2, unit: '×'),
    ],
    out: (v) {
      final r = v['c']! * v['c']! * math.pow(2, (v['T']! - 20) / 10) / 4;
      return [('Relative rate', '${f1(r)}×'), ('', 'rule of thumb: +10 °C ≈ 2× faster')];
    },
    paint: (c, s, v, t, p) {
      final n = (v['c']! * 6).toInt(), sp = 30 * math.sqrt(math.pow(2, (v['T']! - 20) / 10)), rnd = math.Random(5);
      final pts = <Offset>[];
      for (var i = 0; i < 2 * n; i++) {
        final a = rnd.nextDouble() * 2 * math.pi, x0 = rnd.nextDouble() * s.width, y0 = rnd.nextDouble() * s.height;
        double wrap(double x, double m) => ((x % (2 * m)) + 2 * m) % (2 * m) > m ? 2 * m - (((x % (2 * m)) + 2 * m) % (2 * m)) : ((x % (2 * m)) + 2 * m) % (2 * m);
        pts.add(Offset(wrap(x0 + math.cos(a) * sp * t, s.width - 10) + 5, wrap(y0 + math.sin(a) * sp * t, s.height - 10) + 5));
      }
      for (var i = 0; i < pts.length; i++) {
        final hitting = [
          for (var j = 0; j < pts.length; j++)
            if (j != i && (i < n) != (j < n) && (pts[i] - pts[j]).distance < 16) 1,
        ].isNotEmpty;
        if (hitting) c.drawCircle(pts[i], 12, fl(const Color(0x66FFB300)));
        c.drawCircle(pts[i], 6, fl(i < n ? p.peach.deep : p.blue.deep));
      }
      txt(c, 'glow = collision between A and B', Offset(10, s.height - 20), p.ink2, size: 11);
    },
  ),
  'ph': (_) => SimSpec(
    height: 170,
    params: const [Prm('ph', 'pH', 0, 14, 7, step: .5)],
    out: (v) {
      final ph = v['ph']!;
      const ex = {
        0: 'battery acid',
        1: 'stomach acid',
        2: 'lemon juice',
        3: 'vinegar',
        4: 'tomato juice',
        5: 'black coffee',
        6: 'milk',
        7: 'pure water',
        8: 'sea water',
        9: 'baking soda',
        10: 'milk of magnesia',
        11: 'ammonia solution',
        12: 'soapy water',
        13: 'bleach',
        14: 'drain cleaner (NaOH)',
      };
      return [('', ph < 7 ? 'acidic' : (ph == 7 ? 'neutral' : 'basic / alkaline')), ('[H⁺]', '${sig3(math.pow(10, -ph).toDouble())} mol/L'), ('e.g.', ex[ph.round()]!)];
    },
    paint: (c, s, v, t, p) {
      final r = Rect.fromLTRB(16, 30, s.width - 16, 90);
      for (var i = 0; i < 140; i++) {
        c.drawRect(Rect.fromLTWH(r.left + r.width * i / 140, r.top, r.width / 140 + 1, r.height), fl(phColor(i / 10)));
      }
      for (var i = 0; i <= 14; i++) {
        txt(c, '$i', Offset(r.left + r.width * i / 14, r.bottom + 6), p.ink, size: 12, center: false);
      }
      final x = r.left + r.width * v['ph']! / 14;
      c.drawPath(
        Path()
          ..moveTo(x, r.top - 2)
          ..lineTo(x - 10, r.top - 18)
          ..lineTo(x + 10, r.top - 18)
          ..close(),
        fl(p.ink),
      );
      c.drawCircle(Offset(s.width / 2, 138), 18, fl(phColor(v['ph']!)));
      txt(c, 'universal indicator colour', Offset(s.width / 2 + 26, 132), p.ink2, size: 12);
    },
  ),
  'halflife': (_) => SimSpec(
    params: const [
      Prm('T', 'Half-life', 1, 10, 4, unit: 'days'),
      Prm('t', 'Time passed', 0, 40, 0, unit: 'days'),
    ],
    out: (v) {
      final f = math.pow(.5, v['t']! / v['T']!).toDouble();
      return [('Half-lives', f1(v['t']! / v['T']!)), ('Remaining N/N₀', '${(f * 100).toStringAsFixed(1)} %')];
    },
    paint: (c, s, v, t, p) {
      final f = math.pow(.5, v['t']! / v['T']!).toDouble(), n = (100 * f).round();
      final order = List<int>.generate(100, (i) => i)..shuffle(math.Random(11));
      final live = order.take(n).toSet(), cell = math.min((s.width * .45) / 10, (s.height - 20) / 10);
      for (var i = 0; i < 100; i++) {
        c.drawCircle(Offset(12 + cell * (i % 10) + cell / 2, 10 + cell * (i ~/ 10) + cell / 2), cell * .36, fl(live.contains(i) ? p.lilac.deep : p.line));
      }
      final sub = Size(s.width * .5, s.height);
      c.save();
      c.translate(s.width * .5, 0);
      final pl = Plot(c, sub, 0, 40, 0, 100, p, xl: 'days', yl: '% left', left: 36);
      pl.curve((x) => 100 * math.pow(.5, x / v['T']!).toDouble(), p.lilac.deep);
      pl.dot(v['t']!, 100 * f, p.peach.deep);
      c.restore();
    },
  ),
  'vsepr': (_) => SimSpec(
    height: 300,
    params: const [Prm('b', 'Bonding pairs', 2, 6, 4), Prm('l', 'Lone pairs', 0, 3, 0)],
    out: (v) {
      final s = _shape(v['b']!.toInt(), v['l']!.toInt());
      return [('Shape', s.$1), ('Bond angle', s.$2), ('Example', s.$3)];
    },
    paint: (c, s, v, t, p) {},
    ballStick: (v, y, pi, z) {
      var b = v['b']!.toInt(), l = v['l']!.toInt();
      if (b + l > 6) l = 6 - b;
      final dirs = _domains(b + l);
      // lone pairs take the equatorial slots (5) / opposite axial slots (6)
      final lp = List<int>.generate(l, (i) => i); // domain order puts lone pairs in the right slots
      final atoms = <(double, double, double, double, Color)>[(0, 0, 0, .42, const Color(0xFF5B6B8C))];
      final bonds = <(int, int)>[];
      for (var i = 0; i < dirs.length; i++) {
        final d = dirs[i];
        if (lp.contains(i)) {
          atoms.add((d.$1 * .75, d.$2 * .75, d.$3 * .75, .26, const Color(0xFFFFC857)));
        } else {
          atoms.add((d.$1 * 1.35, d.$2 * 1.35, d.$3 * 1.35, .3, const Color(0xFFEFEFEF)));
          bonds.add((0, atoms.length - 1));
        }
      }
      return BallStickPainter(atoms, bonds, y, pi, z, labels: ['A', for (var i = 0; i < dirs.length; i++) lp.contains(i) ? '' : 'X']);
    },
  ),
};

/// electron-domain directions for 2..6 domains (for 5: 3 equatorial first, then axial; for 6: pairs of opposites first)
List<(double, double, double)> _domains(int n) {
  final s3 = math.sqrt(3) / 2;
  switch (n) {
    case 2:
      return [(1, 0, 0), (-1, 0, 0)];
    case 3:
      return [(0, 1, 0), (s3, -.5, 0), (-s3, -.5, 0)];
    case 4:
      return [(0, 1, 0), (.9428, -1 / 3, 0), (-.4714, -1 / 3, .8165), (-.4714, -1 / 3, -.8165)];
    case 5:
      return [(1, 0, 0), (-.5, 0, s3), (-.5, 0, -s3), (0, 1, 0), (0, -1, 0)];
    default:
      return [(0, 1, 0), (0, -1, 0), (1, 0, 0), (-1, 0, 0), (0, 0, 1), (0, 0, -1)];
  }
}

(String, String, String) _shape(int b, int l) {
  if (b + l > 6) l = 6 - b;
  return switch ((b, l)) {
    (2, 0) => ('linear', '180°', 'CO₂, BeCl₂'),
    (3, 0) => ('trigonal planar', '120°', 'BF₃'),
    (2, 1) => ('bent (V-shaped)', '< 120° (~118°)', 'SO₂'),
    (4, 0) => ('tetrahedral', '109.5°', 'CH₄'),
    (3, 1) => ('trigonal pyramidal', '~107°', 'NH₃'),
    (2, 2) => ('bent (V-shaped)', '~104.5°', 'H₂O'),
    (5, 0) => ('trigonal bipyramidal', '90° and 120°', 'PCl₅'),
    (4, 1) => ('see-saw', '< 90° and < 120°', 'SF₄'),
    (3, 2) => ('T-shaped', '< 90°', 'ClF₃'),
    (2, 3) => ('linear', '180°', 'XeF₂'),
    (6, 0) => ('octahedral', '90°', 'SF₆'),
    (5, 1) => ('square pyramidal', '< 90°', 'BrF₅'),
    (4, 2) => ('square planar', '90°', 'XeF₄'),
    _ => ('—', '—', '—'),
  };
}

// Physics labs: temperature, fluid pressure (Grades 10 and 12) and quantum physics (Grade 12).
// Physics and drawing written from scratch.
import 'dart:math' as math;

import 'package:flutter/widgets.dart';

import 'lab_kit.dart';
import 'sims.dart';

const _g = 9.8;
const _glass = Color(0xFFDDE7EE), _glassEdge = Color(0xFF8FA3B3);
const _steel = Color(0xFFB9BEC4), _steelD = Color(0xFF7D848C);
const _mercury = Color(0xFF9AA0A8), _alcohol = Color(0xFFD8443A), _oil = Color(0xFFE2B85A);
const _white = Color(0xFFFFFFFF);

/// cheap deterministic pseudo-random number in [0, 1) for particle [i]
double _rnd(int i, [int salt = 0]) {
  final x = math.sin(i * 12.9898 + salt * 78.233) * 43758.5453;
  return x - x.floorToDouble();
}

/// small wavy photon arrow from [a] towards [b]
void _photon(Canvas c, Offset a, Offset b, Color col, [double amp = 3]) {
  final d = b - a, len = d.distance;
  if (len < 1) return;
  final u = d / len, n = Offset(-u.dy, u.dx);
  final path = Path()..moveTo(a.dx, a.dy);
  const k = 10;
  for (var i = 1; i <= k; i++) {
    final f = i / k, q = a + d * f + n * (amp * math.sin(f * 3 * math.pi));
    path.lineTo(q.dx, q.dy);
  }
  c.drawPath(path, sk(col, 1.8));
  c.drawCircle(b, 2.2, fi(col));
}

const _metals = [('caesium', 2.1), ('sodium', 2.3), ('zinc', 4.3), ('copper', 4.7)];
const _liquids = [('fresh water', 1000.0), ('sea water', 1030.0), ('mercury', 13600.0)];

final Map<String, SimSpec Function(Map<String, dynamic>)> fluidsLabs = {
  // ------------------------------------------------------------------ temperature scales
  'thermometer': (_) => LabSpec(
    height: 300,
    pan: true,
    opts: const [
      Opt('liq', ['Mercury', 'Alcohol']),
    ],
    sliders: const [Sl('C', 'Temperature (drag the column)', -50, 150, 25, step: 1, unit: '°C')],
    drag: (v, at, s) {
      final top = 26.0, bot = s.height - 64;
      v['C'] = (150 - (at.dy - top) / (bot - top) * 200).roundToDouble().clamp(-50, 150);
    },
    formula: 'F = 1.8 C + 32;    K = C + 273.15',
    tryThis:
        'Find the temperature where the Celsius and Fahrenheit readings are equal (−40°). Mercury freezes at −39 °C and alcohol boils at 78 °C: which liquid would you use in a very cold place?',
    read: (v, t) {
      final c = v['C']!;
      return [('Celsius', '${fx(c, 0)} °C'), ('Fahrenheit', '${fx(1.8 * c + 32)} °F'), ('Kelvin', '${fx(c + 273.15, 2)} K')];
    },
    draw: (c, s, v, t, p) {
      final top = 26.0, bot = s.height - 64, cx = s.width * .52;
      double y(double cel) => bot - (cel + 50) / 200 * (bot - top);
      final merc = v['liq'] == 0, col = merc ? _mercury : _alcohol, T = v['C']!;
      // reference temperatures
      for (final (cel, lab) in [(100.0, 'water boils'), (37.0, 'body'), (0.0, 'ice melts'), (-40.0, '−40: C = F')]) {
        dsh(c, Offset(6, y(cel)), Offset(cx - 44, y(cel)), p.line, 1);
        tx(c, lab, Offset(6, y(cel) - 13), p.ink2, size: 10);
      }
      // glass tube and bulb
      c.drawRRect(RRect.fromRectAndRadius(Rect.fromLTRB(cx - 8, top - 12, cx + 8, bot + 20), const Radius.circular(8)), fi(_glass));
      c.drawRRect(RRect.fromRectAndRadius(Rect.fromLTRB(cx - 8, top - 12, cx + 8, bot + 20), const Radius.circular(8)), sk(_glassEdge, 1.5));
      final bulb = Offset(cx, bot + 34);
      c.drawCircle(bulb, 18, fi(_glass));
      c.drawCircle(bulb, 18, sk(_glassEdge, 1.5));
      c.drawCircle(bulb, 14, fi(col));
      var shown = T;
      String? warn;
      if (merc && T < -38.8) {
        shown = -38.8;
        warn = 'mercury is frozen solid below −39 °C';
      } else if (!merc && T > 78) {
        shown = 78;
        warn = 'alcohol boils at 78 °C: the thermometer would break';
      }
      c.drawRect(Rect.fromLTRB(cx - 3.5, y(shown), cx + 3.5, bot + 22), fi(col));
      // Celsius scale (left), Fahrenheit and Kelvin (right)
      for (var cel = -50; cel <= 150; cel += 5) {
        final yy = y(cel.toDouble()), big = cel % 50 == 0;
        c.drawLine(Offset(cx - 10, yy), Offset(cx - (big ? 22 : (cel % 10 == 0 ? 17 : 13)), yy), sk(p.ink, 1.2));
        if (big || cel == 100 || cel == 0) tx(c, '$cel', Offset(cx - 25, yy), p.ink, size: 10.5, ax: 1, ay: .5);
      }
      for (var f = -50; f <= 300; f += 10) {
        final yy = y((f - 32) / 1.8);
        if (yy < top - 2 || yy > bot + 2) continue;
        final big = f % 50 == 0;
        c.drawLine(Offset(cx + 10, yy), Offset(cx + (big ? 22 : 15), yy), sk(p.blue.deep, 1.2));
        if (big) tx(c, '$f', Offset(cx + 25, yy), p.blue.deep, size: 10.5, ay: .5);
      }
      final kx = cx + 62;
      c.drawLine(Offset(kx, top), Offset(kx, bot), sk(p.sage.deep, 1));
      for (var k = 225; k <= 425; k += 25) {
        final yy = y(k - 273.15);
        if (yy < top - 2 || yy > bot + 2) continue;
        c.drawLine(Offset(kx, yy), Offset(kx + (k % 50 == 0 ? 9 : 5), yy), sk(p.sage.deep, 1.2));
        if (k % 50 == 0) tx(c, '$k', Offset(kx + 12, yy), p.sage.deep, size: 10.5, ay: .5);
      }
      tx(c, '°C', Offset(cx - 25, top - 22), p.ink, size: 11, ax: 1);
      tx(c, '°F', Offset(cx + 14, top - 22), p.blue.deep, size: 11);
      tx(c, 'K', Offset(kx + 4, top - 22), p.sage.deep, size: 11);
      // pointer at the liquid level
      arw(c, Offset(cx - 70, y(shown)), Offset(cx - 30, y(shown)), p.peach.deep, 2, 7);
      if (warn != null) tx(c, warn, Offset(6, s.height - 14), p.peach.deep, size: 10.5, ay: .5);
    },
  ),
  // ------------------------------------------------------------------ pressure in a liquid
  'depth_pressure': (_) => LabSpec(
    height: 290,
    pan: true,
    opts: const [
      Opt('liq', ['Fresh water', 'Sea water', 'Mercury']),
      Opt('air', ['Sea level', 'Asmara (2325 m)']),
    ],
    sliders: const [Sl('h', 'Depth (drag the gauge)', 0, 100, 20, step: 1, unit: 'm')],
    drag: (v, at, s) => v['h'] = ((at.dy - 40) / (s.height - 56) * 100).roundToDouble().clamp(0, 100),
    formula: 'P = P₀ + ρgh     (P₀ = air pressure on the surface)',
    tryThis:
        'Every 10 m of water adds about 1 atmosphere (98 kPa). The arrows are the same length in every direction: pressure at a point acts equally in all directions. Try mercury: 13.6 times denser.',
    read: (v, t) {
      final rho = _liquids[v['liq']!.round()].$2, p0 = v['air'] == 0 ? 101.3 : 76.7, pg = rho * _g * v['h']! / 1000;
      return [('ρ', '${rho.round()} kg/m³'), ('ρgh', '${sci(pg, 3)} kPa'), ('P', '${sci(p0 + pg, 4)} kPa'), ('', '${fx((p0 + pg) / 101.3, 2)} atm')];
    },
    draw: (c, s, v, t, p) {
      final li = v['liq']!.round(), rho = _liquids[li].$2, surf = 40.0, bot = s.height - 16, h = v['h']!;
      double y(double d) => surf + d / 100 * (bot - surf);
      final base = li == 2 ? const Color(0xFFB8BEC6) : const Color(0xFF8CC4E8), deep = li == 2 ? const Color(0xFF5E656E) : const Color(0xFF1F5C8C);
      c.drawRect(Rect.fromLTRB(0, 0, s.width, surf), fi(v['air'] == 0 ? const Color(0xFFE3F1FA) : const Color(0xFFEAF2F7)));
      for (var i = 0; i < 10; i++) {
        c.drawRect(Rect.fromLTRB(0, y(i * 10.0), s.width, y(i * 10.0 + 10) + .5), fi(Color.lerp(base, deep, i / 9)!));
      }
      tx(c, v['air'] == 0 ? 'air: P₀ = 101.3 kPa' : 'air in Asmara: P₀ ≈ 76.7 kPa', Offset(s.width - 8, 12), p.ink, size: 10.5, ax: 1);
      for (var d = 0; d <= 100; d += 10) {
        c.drawLine(Offset(0, y(d.toDouble())), Offset(d % 20 == 0 ? 12 : 7, y(d.toDouble())), sk(_white, 1.2));
        if (d % 20 == 0 && d > 0) tx(c, '$d m', Offset(15, y(d.toDouble())), _white, size: 10, ay: .5);
      }
      final p0 = v['air'] == 0 ? 101.3 : 76.7, P = p0 + rho * _g * h / 1000, pMax = p0 + rho * _g * 100 / 1000;
      final o = Offset(s.width * .5, y(h).clamp(surf + 18, bot - 18));
      dsh(c, Offset(s.width * .5 - 70, y(h)), Offset(s.width * .5 + 70, y(h)), _white, 1);
      final L = 8 + 30 * P / pMax;
      for (final d in const [Offset(1, 0), Offset(-1, 0), Offset(0, 1), Offset(0, -1)]) {
        arw(c, o + d * (14 + L), o + d * 13, p.peach.deep, 2.5, 8);
      }
      c.drawCircle(o, 12, fi(_white));
      c.drawCircle(o, 12, sk(p.ink, 1.5));
      c.drawLine(
        o,
        o + Offset(math.cos(-math.pi * .75 + 1.5 * math.pi * P / pMax), math.sin(-math.pi * .75 + 1.5 * math.pi * P / pMax)) * 9,
        sk(p.peach.deep, 2),
      );
      c.drawLine(Offset(o.dx, surf), Offset(o.dx, o.dy - 12 - L - 14), sk(p.ink2, 1));
      tx(c, '${sci(P, 4)} kPa', o + Offset(18 + L, 6), _white, size: 11.5);
      // bar graph of pressure
      final bx = s.width - 26.0, hb = (bot - surf - 8) * P / pMax;
      c.drawRect(Rect.fromLTWH(bx, bot - hb, 14, hb), fi(p.peach.deep));
      c.drawRect(Rect.fromLTWH(bx, surf + 8, 14, bot - surf - 8), sk(_white, 1));
      tx(c, 'P', Offset(bx + 7, surf + 6), _white, size: 10, ax: .5, ay: 1);
    },
  ),
  // ------------------------------------------------------------------ barometer and manometer
  'barometer': (_) => LabSpec(
    height: 300,
    opts: const [
      Opt('m', ['Mercury barometer', 'U-tube manometer']),
      Opt('liq', ['Water', 'Mercury'], when: _mano),
    ],
    sliders: [
      Sl('alt', 'Altitude', 0, 5000, 2325, step: 25, unit: 'm', when: (v) => v['m'] == 0),
      Sl('pg', 'Gas pressure', 90, 115, 105, step: .5, unit: 'kPa', when: _mano),
    ],
    formulaOf: (v) => v['m'] == 0
        ? 'P = ρgh   (ρ = 13 600 kg/m³ for mercury);   P ≈ 101.3 kPa × e^(−altitude / 8400 m)'
        : 'P_gas = P₀ + ρgΔh   (Δh = difference in liquid levels)',
    tryThis:
        'Barometer: at sea level the column is about 760 mm; in Asmara it is only about 580 mm. A water barometer would need a tube over 10 m tall! Manometer: gas pressure above P₀ pushes the liquid down on the gas side.',
    read: (v, t) {
      if (v['m'] == 0) {
        final P = 101.325 * math.exp(-v['alt']! / 8400), h = P * 1000 / (13600 * _g);
        return [
          ('air pressure P', '${fx(P)} kPa'),
          ('mercury column h', '${(h * 1000).round()} mm'),
          ('water would need', '${fx(P * 1000 / (1000 * _g), 1)} m'),
        ];
      }
      final rho = v['liq'] == 0 ? 1000.0 : 13600.0, dp = (v['pg']! - 101.3) * 1000, dh = dp / (rho * _g);
      return [
        ('P_gas − P₀', '${fx(dp / 1000)} kPa'),
        ('Δh', v['liq'] == 0 ? '${fx(dh * 100)} cm' : '${fx(dh * 1000, 0)} mm'),
        ('', dh.abs() < 1e-6 ? 'levels equal: P_gas = P₀' : (dh > 0 ? 'gas side lower: P_gas > P₀' : 'gas side higher: P_gas < P₀')),
      ];
    },
    draw: (c, s, v, t, p) {
      if (v['m'] == 0) {
        final P = 101.325 * math.exp(-v['alt']! / 8400), h = P * 1000 / (13600 * _g) * 1000; // mm
        final dishY = s.height - 36, pmm = (dishY - 34) / 900, cx = s.width * .42;
        // dish
        c.drawRect(Rect.fromLTRB(cx - 70, dishY - 4, cx + 70, dishY + 18), fi(_mercury));
        c.drawLine(Offset(cx - 74, dishY - 10), Offset(cx - 74, dishY + 22), sk(_glassEdge, 2));
        c.drawLine(Offset(cx - 74, dishY + 22), Offset(cx + 74, dishY + 22), sk(_glassEdge, 2));
        c.drawLine(Offset(cx + 74, dishY + 22), Offset(cx + 74, dishY - 10), sk(_glassEdge, 2));
        // tube (closed at the top, 900 mm long)
        final topY = dishY - 900 * pmm + 6, lvl = dishY - h * pmm;
        c.drawRect(Rect.fromLTRB(cx - 9, topY, cx + 9, dishY + 12), fi(_glass));
        c.drawRect(Rect.fromLTRB(cx - 6, lvl, cx + 6, dishY + 12), fi(_mercury));
        c.drawRect(Rect.fromLTRB(cx - 9, topY, cx + 9, dishY + 12), sk(_glassEdge, 1.5));
        tx(c, 'vacuum', Offset(cx + 14, (topY + lvl) / 2), p.ink2, size: 10, ay: .5);
        // scale
        final sx = cx + 50;
        c.drawLine(Offset(sx, dishY - 4), Offset(sx, dishY - 4 - 850 * pmm), sk(p.ink, 1));
        for (var mm = 0; mm <= 850; mm += 50) {
          final yy = dishY - 4 - mm * pmm;
          c.drawLine(Offset(sx, yy), Offset(sx + (mm % 100 == 0 ? 9 : 5), yy), sk(p.ink, 1.2));
          if (mm % 200 == 0) tx(c, '$mm', Offset(sx + 12, yy), p.ink, size: 10, ay: .5);
        }
        tx(c, 'mm', Offset(sx + 12, dishY - 4 - 850 * pmm - 14), p.ink2, size: 10);
        dsh(c, Offset(cx - 60, lvl), Offset(sx, lvl), p.peach.deep, 1.2);
        c.drawLine(Offset(cx - 44, lvl), Offset(cx - 44, dishY - 4), sk(p.peach.deep, 1.5));
        tx(c, 'h = ${h.round()} mm', Offset(cx - 48, (lvl + dishY) / 2), p.peach.deep, size: 11, ax: 1, ay: .5);
        for (final dx in const [-60.0, 50.0]) {
          arw(c, Offset(cx + dx, dishY - 34), Offset(cx + dx, dishY - 8), p.blue.deep, 2, 7);
        }
        tx(c, 'air pushes down', Offset(cx + 70, dishY - 34), p.blue.deep, size: 10);
        final alt = v['alt']!;
        final place = alt < 100 ? 'sea level (Massawa)' : ((alt - 2325).abs() < 150 ? 'Asmara' : '${alt.round()} m');
        tx(c, place, const Offset(8, 8), p.ink, size: 11);
        return;
      }
      // U-tube manometer
      final water = v['liq'] == 0, rho = water ? 1000.0 : 13600.0, dh = (v['pg']! - 101.3) * 1000 / (rho * _g);
      final hMax = 15000 / (rho * _g), pxm = 110 / hMax, base = s.height * .62, lx = s.width * .40, rx = s.width * .62, half = dh * pxm / 2;
      final liqCol = water ? const Color(0xFF6FB3E0) : _mercury;
      // gas bulb on the left
      final bulb = Offset(lx - 70, 60);
      c.drawCircle(bulb, 30, fi(const Color(0xFFF3E1B8)));
      c.drawCircle(bulb, 30, sk(_glassEdge, 1.5));
      tx(c, 'gas', bulb, p.ink, size: 11, ax: .5, ay: .5);
      c.drawRect(Rect.fromLTRB(bulb.dx + 28, 54, lx + 7, 66), fi(_glass));
      // tube outline
      final bottom = s.height - 22;
      c.drawRect(Rect.fromLTRB(lx - 7, 54, lx + 7, bottom), fi(_glass));
      c.drawRect(Rect.fromLTRB(rx - 7, 30, rx + 7, bottom), fi(_glass));
      c.drawRect(Rect.fromLTRB(lx - 7, bottom - 14, rx + 7, bottom), fi(_glass));
      // liquid
      final yl = base + half, yr = base - half;
      c.drawRect(Rect.fromLTRB(lx - 5, yl, lx + 5, bottom - 2), fi(liqCol));
      c.drawRect(Rect.fromLTRB(rx - 5, yr, rx + 5, bottom - 2), fi(liqCol));
      c.drawRect(Rect.fromLTRB(lx - 5, bottom - 12, rx + 5, bottom - 2), fi(liqCol));
      arw(c, Offset(rx, 6), Offset(rx, 26), p.blue.deep, 2, 7);
      tx(c, 'air  P₀ = 101.3 kPa', Offset(rx + 12, 8), p.blue.deep, size: 10);
      dsh(c, Offset(lx - 20, yl), Offset(rx + 40, yl), p.ink2, 1);
      dsh(c, Offset(lx - 20, yr), Offset(rx + 40, yr), p.ink2, 1);
      if (dh.abs() > 1e-6) {
        arw(c, Offset(rx + 34, yl), Offset(rx + 34, yr), p.peach.deep, 2, 7);
        tx(c, 'Δh = ${water ? '${fx(dh.abs() * 100)} cm' : '${fx(dh.abs() * 1000, 0)} mm'}', Offset(rx + 40, (yl + yr) / 2), p.peach.deep, size: 11, ay: .5);
      }
    },
  ),
  // ------------------------------------------------------------------ hydraulic press (Pascal)
  'hydraulic': (_) => LabSpec(
    height: 270,
    sliders: const [
      Sl('F1', 'Effort F₁ on the small piston', 10, 200, 50, step: 5, unit: 'N'),
      Sl('d1', 'Small piston diameter', 1, 5, 2, step: .5, unit: 'cm'),
      Sl('d2', 'Large piston diameter', 6, 30, 20, step: 1, unit: 'cm'),
      Sl('x1', 'Push the small piston down (drag)', 0, 10, 4, step: .5, unit: 'cm'),
    ],
    drag: (v, at, s) => v['x1'] = ((at.dx / s.width) * 10 * 2).roundToDouble().clamp(0, 20) / 2,
    formula: 'P = F₁/A₁ = F₂/A₂   ⇒   F₂ = F₁ × A₂/A₁;    x₂ = x₁ × A₁/A₂  (work in = work out)',
    tryThis:
        'Double the large diameter: the area and the output force go up 4 times, but the large piston moves 4 times less. Pascal: the same pressure is passed to every part of the liquid.',
    read: (v, t) {
      final a1 = math.pi * math.pow(v['d1']! / 200, 2), a2 = math.pi * math.pow(v['d2']! / 200, 2), P = v['F1']! / a1, f2 = P * a2, x2 = v['x1']! * a1 / a2;
      return [
        ('pressure P', '${sci(P / 1000, 3)} kPa'),
        ('F₂', '${sci(f2, 3)} N'),
        ('lifts', '${sci(f2 / _g, 3)} kg'),
        ('A₂/A₁', fx(a2 / a1, 1)),
        ('x₂', '${fx(x2 * 10, 2)} mm'),
      ];
    },
    draw: (c, s, v, t, p) {
      final d1 = v['d1']!, d2 = v['d2']!, ratio = (d1 / d2) * (d1 / d2), x1 = v['x1']!, x2 = x1 * ratio;
      final w1 = 6 * d1 + 6, w2 = 5.0 * d2 + 10, lx = 26 + w1 / 2 + 20, rx = s.width - 30 - w2 / 2, top = 70.0, bot = s.height - 30, ppc = 9.0;
      final y1 = top + x1 * ppc, yp2 = top + 40 - x2 * ppc; // rest levels: small piston at top, large at top + 40
      // oil
      c.drawRect(Rect.fromLTRB(lx - w1 / 2, y1, lx + w1 / 2, bot), fi(_oil));
      c.drawRect(Rect.fromLTRB(rx - w2 / 2, yp2, rx + w2 / 2, bot), fi(_oil));
      c.drawRect(Rect.fromLTRB(lx - w1 / 2, bot - 22, rx + w2 / 2, bot), fi(_oil));
      // cylinder walls
      for (final (x, w) in [(lx, w1), (rx, w2)]) {
        c.drawLine(Offset(x - w / 2, top - 30), Offset(x - w / 2, bot), sk(_steelD, 3));
        c.drawLine(Offset(x + w / 2, top - 30), Offset(x + w / 2, x == lx ? bot - 22 : bot), sk(_steelD, 3));
      }
      c.drawLine(Offset(lx + w1 / 2, bot - 22), Offset(rx - w2 / 2, bot - 22), sk(_steelD, 3));
      c.drawLine(Offset(lx - w1 / 2, bot), Offset(rx + w2 / 2, bot), sk(_steelD, 3));
      // pistons
      c.drawRect(Rect.fromLTRB(lx - w1 / 2 + 1.5, y1 - 8, lx + w1 / 2 - 1.5, y1), fi(_steel));
      c.drawRect(Rect.fromLTRB(rx - w2 / 2 + 1.5, yp2 - 8, rx + w2 / 2 - 1.5, yp2), fi(_steel));
      // load on the large piston
      c.drawRect(Rect.fromLTRB(rx - w2 * .32, yp2 - 34, rx + w2 * .32, yp2 - 8), fi(p.blue.deep));
      tx(c, 'load', Offset(rx, yp2 - 21), _white, size: 10, ax: .5, ay: .5);
      // forces
      final a1 = math.pi * math.pow(d1 / 200, 2), f2 = v['F1']! / a1 * math.pi * math.pow(d2 / 200, 2);
      arw(c, Offset(lx, y1 - 52), Offset(lx, y1 - 9), p.peach.deep, 3, 9);
      tx(c, 'F₁ = ${v['F1']!.round()} N', Offset(lx + 8, y1 - 60), p.peach.deep, size: 11);
      final lab2 = 'F₂ = ${sci(f2, 3)} N';
      arw(c, Offset(rx - w2 / 2 - 12, yp2 + 30), Offset(rx - w2 / 2 - 12, yp2 - 30), p.sage.deep, 3.5, 10);
      tx(c, lab2, Offset(rx - w2 / 2 - 18, yp2 + 34), p.sage.deep, size: 11, ax: .5);
      tx(c, 'same pressure everywhere in the oil', Offset((lx + rx) / 2, bot - 11), p.ink, size: 10, ax: .5, ay: .5);
      tx(c, 'x₁ = ${fx(x1)} cm', Offset(8, 8), p.ink2, size: 10.5);
      tx(c, 'x₂ = ${fx(x2 * 10, 2)} mm', Offset(s.width - 8, 8), p.ink2, size: 10.5, ax: 1);
    },
  ),
  // ------------------------------------------------------------------ photoelectric effect
  'photoelectric': (_) => LabSpec(
    height: 280,
    anim: true,
    opts: const [
      Opt('met', ['Caesium (2.1 eV)', 'Sodium (2.3 eV)', 'Zinc (4.3 eV)', 'Copper (4.7 eV)']),
    ],
    sliders: const [
      Sl('lam', 'Wavelength λ', 200, 700, 450, step: 5, unit: 'nm'),
      Sl('I', 'Brightness (intensity)', 0, 100, 60, step: 5, unit: '%'),
      Sl('Vs', 'Reverse (stopping) voltage', 0, 4, 0, step: .1, unit: 'V'),
    ],
    formula: 'hf = φ + KEmax;    E (eV) = 1240 / λ (nm);    eV₀ = KEmax',
    tryThis:
        'Make the light brighter: more electrons, but not faster ones. Shorten λ: faster electrons. Below the threshold frequency no electrons come out however bright the light is: light comes in photons.',
    read: (v, t) {
      final m = _metals[v['met']!.round()], E = 1240 / v['lam']!, ke = E - m.$2;
      final cur = ke <= 0 ? 0.0 : v['I']! / 100 * (1 - v['Vs']! / ke).clamp(0.0, 1.0) * 2.0;
      return [
        ('photon E', '${fx(E, 2)} eV'),
        ('φ (${m.$1})', '${m.$2} eV'),
        ('KEmax', ke <= 0 ? 'no emission' : '${fx(ke, 2)} eV'),
        ('threshold λ₀', '${(1240 / m.$2).round()} nm'),
        ('stopping V₀', ke <= 0 ? '—' : '${fx(ke, 2)} V'),
        ('current', '${fx(cur, 2)} μA'),
      ];
    },
    draw: (c, s, v, t, p) {
      final m = _metals[v['met']!.round()], lam = v['lam']!, E = 1240 / lam, ke = E - m.$2, vs = v['Vs']!, I = v['I']!;
      final uv = lam < 380, col = uv ? p.lilac.deep : waveColor(lam);
      final g0 = 20.0, g1 = s.width - 20, ty = 56.0, by = 176.0, cxk = g0 + 28, cxa = g1 - 28;
      c.drawRRect(RRect.fromRectAndRadius(Rect.fromLTRB(g0, ty, g1, by), const Radius.circular(26)), fi(const Color(0xFFEFF4F7)));
      c.drawRRect(RRect.fromRectAndRadius(Rect.fromLTRB(g0, ty, g1, by), const Radius.circular(26)), sk(_glassEdge, 1.5));
      c.drawRect(Rect.fromLTRB(cxk - 6, ty + 18, cxk, by - 18), fi(_steelD));
      c.drawRect(Rect.fromLTRB(cxa, ty + 24, cxa + 5, by - 24), fi(_steelD));
      tx(c, m.$1, Offset(cxk - 2, by - 14), p.ink2, size: 9.5, ax: .2);
      tx(c, 'collector', Offset(cxa + 4, by - 18), p.ink2, size: 9.5, ax: .8);
      // lamp
      final lamp = Offset(g0 + 90, 16);
      c.drawCircle(lamp, 10, fi(col));
      tx(c, uv ? 'UV ${lam.round()} nm' : '${lam.round()} nm', lamp + const Offset(16, -6), p.ink, size: 10.5);
      // circuit: cathode – battery (reverse) – ammeter – collector
      final wy = s.height - 34;
      c.drawLine(Offset(cxk - 3, by - 18), Offset(cxk - 3, wy), sk(p.ink, 1.5));
      c.drawLine(Offset(cxa + 2, by - 24), Offset(cxa + 2, wy), sk(p.ink, 1.5));
      final bx = s.width * .38, ax = s.width * .68;
      c.drawLine(Offset(cxk - 3, wy), Offset(bx - 5, wy), sk(p.ink, 1.5));
      c.drawLine(Offset(bx + 5, wy), Offset(ax - 13, wy), sk(p.ink, 1.5));
      c.drawLine(Offset(ax + 13, wy), Offset(cxa + 2, wy), sk(p.ink, 1.5));
      c.drawLine(Offset(bx - 5, wy - 12), Offset(bx - 5, wy + 12), sk(p.ink, 2));
      c.drawLine(Offset(bx + 5, wy - 6), Offset(bx + 5, wy + 6), sk(p.ink, 4));
      tx(c, 'V = ${fx(vs)} V', Offset(bx, wy + 14), p.ink, size: 10, ax: .5);
      final cur = ke <= 0 ? 0.0 : I / 100 * (1 - vs / ke).clamp(0.0, 1.0) * 2.0;
      c.drawCircle(Offset(ax, wy), 13, fi(_white));
      c.drawCircle(Offset(ax, wy), 13, sk(p.ink, 1.5));
      tx(c, 'μA', Offset(ax, wy), p.ink, size: 9, ax: .5, ay: .5);
      tx(c, '${fx(cur, 2)} μA', Offset(ax, wy + 15), p.peach.deep, size: 10, ax: .5);
      // photons and electrons (closed form in t: particle i is emitted at i / rate)
      final rate = 1 + 11 * I / 100, L = cxa - cxk;
      if (I <= 0) return;
      final now = (t * rate).floor();
      const tp = .55; // photon flight time (s)
      final k = L / .9; // electron speed scale: 1 eV with no field crosses in 0.9 s
      for (var j = 0; j < (rate * 3.6).ceil(); j++) {
        final i = now - j;
        if (i < 0) break;
        final age = t - i / rate, yT = ty + 24 + _rnd(i) * (by - ty - 48);
        if (age < tp) {
          final a = lamp + Offset(4 + _rnd(i, 3) * 8, 8), b = Offset(cxk, yT), f = age / tp;
          final head = Offset.lerp(a, b, f)!, tail = Offset.lerp(a, b, math.max(0, f - .22))!;
          _photon(c, tail, head, col);
          continue;
        }
        if (ke <= 0) continue;
        final e0 = ke * (.15 + .85 * _rnd(i, 7)), tau = age - tp, v0 = k * math.sqrt(e0), acc = k * k * vs / (2 * L);
        final x = v0 * tau - .5 * acc * tau * tau;
        if (x < 0 || x > L) continue;
        c.drawCircle(Offset(cxk + 4 + x, yT), 3.2, fi(p.blue.deep));
      }
      if (ke <= 0) tx(c, 'no electrons: photon energy < φ', Offset(s.width / 2, ty + 10), p.peach.deep, size: 10.5, ax: .5);
    },
  ),
  // ------------------------------------------------------------------ X-ray tube
  'xray_tube': (_) => LabSpec(
    height: 320,
    anim: true,
    sliders: const [
      Sl('kV', 'Accelerating voltage', 5, 100, 30, step: 1, unit: 'kV'),
      Sl('mA', 'Tube current', 1, 10, 4, step: 1, unit: 'mA'),
    ],
    formula: 'eV = hf_max = hc/λmin   ⇒   λmin (nm) = 1.24 / V (kV);   tungsten target',
    tryThis:
        'Raise the voltage: λmin gets shorter (harder X-rays). Raise the current: more X-rays of the same wavelengths. The sharp peaks are tungsten’s characteristic lines; the K lines need more than 69.5 kV.',
    read: (v, t) {
      final kv = v['kV']!, g = 1 + kv / 511, beta = math.sqrt(1 - 1 / (g * g)), eff = 1.1e-9 * 74 * kv * 1000;
      return [
        ('λmin', '${sci(1.24 / kv, 3)} nm'),
        ('max photon E', '${kv.round()} keV'),
        ('electron speed', '${fx(beta, 3)} c'),
        ('tube power', '${fx(kv * v['mA']!, 0)} W'),
        ('X-ray efficiency', '${fx(eff * 100, 2)} %  (rest is heat)'),
      ];
    },
    draw: (c, s, v, t, p) {
      final kv = v['kV']!, mA = v['mA']!, lmin = 1.24 / kv;
      // tube
      const ty = 14.0, by = 120.0;
      final x0 = 16.0, x1 = s.width - 16;
      c.drawRRect(RRect.fromRectAndRadius(Rect.fromLTRB(x0, ty, x1, by), const Radius.circular(40)), fi(const Color(0xFFEFF4F7)));
      c.drawRRect(RRect.fromRectAndRadius(Rect.fromLTRB(x0, ty, x1, by), const Radius.circular(40)), sk(_glassEdge, 1.5));
      final cy = (ty + by) / 2, kx = x0 + 44, ax = x1 - 64;
      // filament coil
      final coil = Path()..moveTo(kx - 18, cy);
      for (var i = 1; i <= 12; i++) {
        coil.lineTo(kx - 18 + i * 2.0, cy + (i.isOdd ? -6 : 6));
      }
      c.drawPath(coil, sk(const Color(0xFFE07A2E), 2));
      tx(c, 'hot filament (−)', Offset(kx - 22, by - 22), p.ink2, size: 9.5);
      // tungsten target on the anode, at 45°
      final tgt = Path()
        ..moveTo(ax, cy - 22)
        ..lineTo(ax + 22, cy - 22)
        ..lineTo(ax + 22, cy + 22)
        ..lineTo(ax - 22, cy + 22)
        ..close();
      c.drawRect(Rect.fromLTRB(ax + 22, cy - 10, x1 - 4, cy + 10), fi(const Color(0xFFC07A3C)));
      c.drawPath(tgt, fi(_steelD));
      tx(c, 'tungsten (+)', Offset(ax, ty + 6), p.ink2, size: 9.5, ax: .5);
      // electrons: closed form, rate ∝ current, speed grows with voltage (cosmetic scale)
      final speed = 120 + 3.0 * kv, rate = 3 + 2.4 * mA, gap = ax - kx;
      final flight = gap / speed, now = (t * rate).floor();
      for (var j = 0; j < (rate * (flight + .5)).ceil(); j++) {
        final i = now - j;
        if (i < 0) break;
        final age = t - i / rate, y = cy + (_rnd(i) - .5) * 14;
        if (age < flight) {
          final xx = kx + age * speed;
          if (xx < ax - (y - cy) - 2) c.drawCircle(Offset(xx, y), 2.6, fi(p.blue.deep));
        } else if (age < flight + .5 && _rnd(i, 5) < .5) {
          final f = (age - flight) / .5, a0 = Offset(ax - 4, cy + 4), dir = Offset(-.5 + _rnd(i, 9) * .7, 1);
          final head = a0 + dir * (14 + f * 70), tail = a0 + dir * (f * 70);
          _photon(c, tail, head, p.lilac.deep, 2.5);
        }
      }
      tx(c, 'X-rays', Offset(ax - 70, by + 6), p.lilac.deep, size: 10.5);
      tx(c, '${kv.round()} kV', Offset((kx + ax) / 2, ty + 6), p.ink, size: 11, ax: .5);
      // spectrum: Kramers continuum + tungsten L and K lines, λ axis 0–0.30 nm
      final gx0 = 40.0, gx1 = s.width - 14, gy0 = s.height - 26, gy1 = by + 40;
      c.drawLine(Offset(gx0, gy0), Offset(gx1, gy0), sk(p.ink, 1.3));
      c.drawLine(Offset(gx0, gy0), Offset(gx0, gy1 - 6), sk(p.ink, 1.3));
      double X(double nm) => gx0 + nm / .3 * (gx1 - gx0);
      for (var q = 0; q <= 3; q++) {
        c.drawLine(Offset(X(q * .1), gy0), Offset(X(q * .1), gy0 + 4), sk(p.ink, 1.2));
        tx(c, fx(q * .1), Offset(X(q * .1), gy0 + 5), p.ink2, size: 9.5, ax: .5);
      }
      tx(c, 'λ (nm)', Offset(gx1, gy0 - 14), p.ink2, size: 9.5, ax: 1);
      tx(c, 'intensity (relative)', Offset(gx0 + 4, gy1 - 8), p.ink2, size: 9.5);
      // Kramers continuum: true shape, peak (at 2λmin) ∝ current × V²; the peak height is drawn on a cube-root scale so that
      // 5 kV and 100 kV both show (100 kV, 10 mA fills the plot)
      final hgt = gy0 - gy1, ref = 1 / (4 * math.pow(1.24 / 100, 2) as double);
      double I(double nm) => nm <= lmin ? 0 : (nm / lmin - 1) / (nm * nm);
      final ipk = 1 / (4 * lmin * lmin), amp = math.pow(ipk * (mA / 10) / ref, 1 / 3).toDouble(), pts = <Offset>[];
      double hOf(double nm) => I(nm) / ipk * amp * hgt;
      for (var i = 0; i <= 90; i++) {
        final nm = i / 90 * .3;
        pts.add(Offset(X(nm), gy0 - hOf(nm)));
      }
      polyline(c, pts, sk(p.peach.deep, 2));
      void line(double nm, double edgeKv, double rel, String lab) {
        if (kv <= edgeKv) return;
        final base = gy0 - hOf(nm), top = math.max(gy1, base - hgt * .45 * rel * math.pow(mA / 10, 1 / 3).toDouble());
        c.drawLine(Offset(X(nm), base), Offset(X(nm), top), sk(p.blue.deep, 2.2));
        tx(c, lab, Offset(X(nm) + 3, top), p.blue.deep, size: 9.5);
      }

      line(.148, 10.2, .9, 'Lα');
      line(.128, 11.5, .6, 'Lβ');
      line(.0209, 69.5, 1, 'Kα');
      line(.0184, 69.5, .5, 'Kβ');
      dsh(c, Offset(X(lmin), gy0), Offset(X(lmin), gy1), p.ink2, 1);
      tx(c, 'λmin', Offset(X(lmin) + 3, gy1 + 10), p.ink, size: 10);
    },
  ),
};

bool _mano(V v) => v['m'] == 1;

// Mathematics, business/economics and history sims.
import 'dart:math' as math;

import 'package:flutter/widgets.dart';

import 'sims.dart';

double _fact(int n) => n <= 1 ? 1 : n * _fact(n - 1);

final Map<String, SimSpec Function(Map<String, dynamic>)> mathEconSims = {
  'pythagoras': (_) => SimSpec(
    height: 280,
    params: const [Prm('a', 'Side a', 1, 12, 3), Prm('b', 'Side b', 1, 12, 4)],
    out: (v) {
      final c = math.sqrt(v['a']! * v['a']! + v['b']! * v['b']!);
      return [('a² + b² = c²', '${(v['a']! * v['a']!).toInt()} + ${(v['b']! * v['b']!).toInt()} = ${f2(c * c)}'), ('Hypotenuse c', f2(c))];
    },
    paint: (c, s, v, t, p) {
      final a = v['a']!, b = v['b']!, k = math.min((s.width - 40) / (a + b + b), (s.height - 30) / (a + b + a) * 1.0).clamp(3.0, 40.0);
      final o = Offset(s.width * .42, s.height * .55), A = o + Offset(0, -a * k), B = o + Offset(b * k, 0);
      c.drawPath(Path()..moveTo(o.dx, o.dy)..lineTo(A.dx, A.dy)..lineTo(B.dx, B.dy)..close(), fl(p.butter.tile));
      c.drawRect(Rect.fromPoints(o, o + Offset(-a * k, -a * k)), fl(p.peach.tile));
      c.drawRect(Rect.fromPoints(o, o + Offset(b * k, b * k)), fl(p.blue.tile));
      final d = B - A, n = Offset(d.dy, -d.dx);
      c.drawPath(Path()..moveTo(A.dx, A.dy)..lineTo(B.dx, B.dy)..lineTo(B.dx + n.dx, B.dy + n.dy)..lineTo(A.dx + n.dx, A.dy + n.dy)..close(), fl(p.sage.tile));
      c.drawPath(Path()..moveTo(o.dx, o.dy)..lineTo(A.dx, A.dy)..lineTo(B.dx, B.dy)..close(), st(p.ink, 2.5));
      c.drawRect(Rect.fromLTWH(o.dx, o.dy - 10, 10, 10), st(p.ink, 1.5));
      txt(c, 'a²', o + Offset(-a * k / 2, -a * k / 2), p.peach.deep, size: 16, center: true);
      txt(c, 'b²', o + Offset(b * k / 2, b * k / 2), p.blue.deep, size: 16, center: true);
      txt(c, 'c²', (A + B) / 2 + n / 2, p.sage.deep, size: 16, center: true);
    },
  ),
  'trig': (_) => SimSpec(
    height: 270,
    params: const [Prm('th', 'Angle θ', 0, 360, 30, step: 5, unit: '°')],
    out: (v) {
      final r = v['th']! * math.pi / 180, cs = math.cos(r);
      return [('sin θ', f2(math.sin(r))), ('cos θ', f2(cs)), ('tan θ', cs.abs() < 1e-9 ? 'undefined' : f2(math.tan(r)))];
    },
    paint: (c, s, v, t, p) {
      final o = Offset(s.width / 2, s.height / 2), R = s.height * .4, r = v['th']! * math.pi / 180, q = o + Offset(math.cos(r), -math.sin(r)) * R;
      c.drawCircle(o, R, st(p.line, 1.5));
      c.drawLine(o - Offset(R + 20, 0), o + Offset(R + 20, 0), st(p.ink2, 1));
      c.drawLine(o - Offset(0, R + 10), o + Offset(0, R + 10), st(p.ink2, 1));
      c.drawArc(Rect.fromCircle(center: o, radius: 26), 0, -r, false, st(p.lilac.deep, 2));
      c.drawLine(o, q, st(p.ink, 2.5));
      c.drawLine(Offset(q.dx, o.dy), q, st(p.peach.deep, 3));
      c.drawLine(o, Offset(q.dx, o.dy), st(p.blue.deep, 3));
      c.drawCircle(q, 7, fl(p.ink));
      txt(c, 'sin', Offset(q.dx + 6, (q.dy + o.dy) / 2), p.peach.deep, size: 12);
      txt(c, 'cos', Offset((o.dx + q.dx) / 2, o.dy + 6), p.blue.deep, size: 12, center: false);
      txt(c, 'unit circle, r = 1', Offset(10, s.height - 20), p.ink2, size: 11);
    },
  ),
  'interest': (_) => SimSpec(
    params: const [Prm('P', 'Principal', 1000, 20000, 5000, step: 1000, unit: 'Nfa'), Prm('r', 'Rate', 1, 20, 8, unit: '% p.a.'), Prm('n', 'Years', 1, 30, 10)],
    out: (v) {
      final P = v['P']!, r = v['r']! / 100, n = v['n']!;
      return [('Simple: P(1 + rn)', '${(P * (1 + r * n)).round()}'), ('Compound: P(1 + r)ⁿ', '${(P * math.pow(1 + r, n)).round()}')];
    },
    paint: (c, s, v, t, p) {
      final P = v['P']!, r = v['r']! / 100, top = (P * math.pow(1 + r, 30) * 1.05).toDouble();
      final pl = Plot(c, s, 0, 30, 0, top, p, xl: 'years', yl: 'amount', left: 52);
      pl.curve((x) => P * (1 + r * x), p.blue.deep);
      pl.curve((x) => P * math.pow(1 + r, x).toDouble(), p.peach.deep);
      pl.dot(v['n']!, P * math.pow(1 + r, v['n']!).toDouble(), p.peach.deep, 6);
      pl.dot(v['n']!, P * (1 + r * v['n']!), p.blue.deep, 6);
      txt(c, 'compound', pl.r.topLeft + const Offset(60, 4), p.peach.deep, size: 12);
      txt(c, 'simple', pl.r.topLeft + const Offset(60, 20), p.blue.deep, size: 12);
    },
  ),
  'sequence': (m) {
    final geo = m['geo'] == true;
    return SimSpec(
      params: geo ? const [Prm('a', 'First term a', 1, 10, 2), Prm('d', 'Common ratio r', .5, 2, 1.5, step: .1)] : const [Prm('a', 'First term a', -10, 10, 3), Prm('d', 'Common difference d', -5, 5, 2, step: .5)],
      out: (v) {
        final a = v['a']!, d = v['d']!;
        double term(int n) => geo ? a * math.pow(d, n - 1).toDouble() : a + (n - 1) * d;
        final sum = [for (var n = 1; n <= 10; n++) term(n)].fold(0.0, (x, y) => x + y);
        return [('Terms', [for (var n = 1; n <= 5; n++) f1(term(n))].join(', ')), ('10th term', f1(term(10))), ('Sum of 10 terms', f1(sum))];
      },
      paint: (c, s, v, t, p) {
        final a = v['a']!, d = v['d']!;
        final ts_ = [for (var n = 1; n <= 10; n++) geo ? a * math.pow(d, n - 1).toDouble() : a + (n - 1) * d];
        final hi = ts_.map((x) => x.abs()).reduce(math.max) * 1.1, lo = ts_.any((x) => x < 0) ? -hi : 0.0;
        final pl = Plot(c, s, 0, 11, lo, hi == 0 ? 1 : hi, p, xl: 'n', yl: geo ? 'aₙ = a·rⁿ⁻¹' : 'aₙ = a + (n−1)d', xt: 11);
        for (var i = 0; i < 10; i++) {
          c.drawRect(Rect.fromPoints(pl.at(i + .7, 0), pl.at(i + 1.3, ts_[i])), fl(p.blue.mid));
        }
      },
    );
  },
  'dice': (_) => SimSpec(
    params: const [Prm('n', 'Number of throws', 10, 1000, 60, step: 10)],
    out: (v) => [('P(sum = 7)', '6/36 = ${f2(6 / 36)}'), ('', 'the more throws, the closer to the theory')],
    paint: (c, s, v, t, p) {
      final n = v['n']!.toInt(), rnd = math.Random(42), cnt = List<int>.filled(13, 0);
      for (var i = 0; i < n; i++) {
        cnt[rnd.nextInt(6) + rnd.nextInt(6) + 2]++;
      }
      final pl = Plot(c, s, 1, 13, 0, .25, p, xl: 'sum of two dice', yl: 'relative frequency', xt: 12, yt: 5);
      for (var k = 2; k <= 12; k++) {
        final th = (6 - (k - 7).abs()) / 36;
        c.drawRect(Rect.fromPoints(pl.at(k - .35, 0), pl.at(k + .35, cnt[k] / n)), fl(p.blue.mid));
        c.drawLine(pl.at(k - .45, th), pl.at(k + .45, th), st(p.peach.deep, 3));
      }
      txt(c, 'bars: experiment · red: theory', pl.r.topRight + const Offset(-4, 0), p.ink2, size: 11, right: true);
    },
  ),
  'circle': (_) => SimSpec(
    height: 280,
    params: const [Prm('arc', 'Arc AB', 40, 300, 120, step: 10, unit: '°'), Prm('p', 'Point P on the circle', 0, 100, 50, unit: '%')],
    out: (v) => [('Angle at centre AOB', '${v['arc']!.toInt()}°'), ('Angle at circumference APB', '${f1(v['arc']! / 2)}°'), ('', 'the angle at the centre is twice the angle at the circumference')],
    paint: (c, s, v, t, p) {
      final o = Offset(s.width / 2, s.height / 2 + 6), R = s.height * .4, arc = v['arc']! * math.pi / 180;
      Offset on(double a) => o + Offset(math.sin(a), math.cos(a)) * R;
      final a0 = -arc / 2, a1 = arc / 2, A = on(a0), B = on(a1);
      final pa = a1 + (2 * math.pi - arc) * (.05 + .9 * v['p']! / 100), P = on(pa);
      c.drawCircle(o, R, st(p.ink2, 2));
      c.drawLine(o, A, st(p.blue.deep, 2.5));
      c.drawLine(o, B, st(p.blue.deep, 2.5));
      c.drawLine(P, A, st(p.peach.deep, 2.5));
      c.drawLine(P, B, st(p.peach.deep, 2.5));
      for (final (q, n) in [(A, 'A'), (B, 'B'), (P, 'P'), (o, 'O')]) {
        c.drawCircle(q, 5, fl(p.ink));
        txt(c, n, q + (q == o ? const Offset(8, -18) : (q - o) / R * 16), p.ink, size: 14, center: true);
      }
    },
  ),
  'transform': (_) => SimSpec(
    height: 280,
    params: const [Prm('dx', 'Translate x', -6, 6, 2), Prm('dy', 'Translate y', -6, 6, 1), Prm('rot', 'Rotate about O', 0, 360, 0, step: 15, unit: '°'), Prm('ref', 'Reflect', 0, 2, 0, fmt: _refName)],
    out: (v) => [('', 'Shape and size stay the same: the image is congruent to the object')],
    paint: (c, s, v, t, p) {
      final r = Rect.fromLTRB(10, 10, s.width - 10, s.height - 10), sc = math.min(r.width / 16, r.height / 12), o = r.center;
      for (var i = -8; i <= 8; i++) {
        c.drawLine(o + Offset(i * sc, -6 * sc), o + Offset(i * sc, 6 * sc), st(p.line, .7));
      }
      for (var j = -6; j <= 6; j++) {
        c.drawLine(o + Offset(-8 * sc, j * sc), o + Offset(8 * sc, j * sc), st(p.line, .7));
      }
      c.drawLine(o + Offset(-8 * sc, 0), o + Offset(8 * sc, 0), st(p.ink2, 1.5));
      c.drawLine(o + Offset(0, -6 * sc), o + Offset(0, 6 * sc), st(p.ink2, 1.5));
      const tri = [(1.0, 1.0), (3.0, 1.0), (1.0, 3.0)];
      Path path(List<(double, double)> pts) {
        final pa = Path();
        for (final (i, q) in pts.indexed) {
          final z = o + Offset(q.$1 * sc, -q.$2 * sc);
          i == 0 ? pa.moveTo(z.dx, z.dy) : pa.lineTo(z.dx, z.dy);
        }
        return pa..close();
      }

      final a = v['rot']! * math.pi / 180, ref = v['ref']!.toInt();
      final img = [
        for (final (x0, y0) in tri)
          () {
            var x = x0, y = y0;
            if (ref == 1) y = -y;
            if (ref == 2) x = -x;
            final xr = x * math.cos(a) - y * math.sin(a), yr = x * math.sin(a) + y * math.cos(a);
            return (xr + v['dx']!, yr + v['dy']!);
          }(),
      ];
      c.drawPath(path(tri), fl(const Color(0x5542A5F5)));
      c.drawPath(path(tri), st(p.blue.deep, 2));
      c.drawPath(path(img), fl(const Color(0x55EF6C4A)));
      c.drawPath(path(img), st(p.peach.deep, 2.5));
      txt(c, 'object', o + Offset(3.2 * sc, -1.2 * sc), p.blue.deep, size: 11);
    },
  ),
  'supply': (_) => SimSpec(
    params: const [Prm('D', 'Demand shift', -3, 3, 0, fmt: _shift), Prm('S', 'Supply shift', -3, 3, 0, fmt: _shift)],
    out: (v) {
      // Qd = 10 - P + D, Qs = P - 2 + S -> P* = (12 + D - S)/2
      final P = (12 + v['D']! - v['S']!) / 2, Q = 10 - P + v['D']!;
      return [('Equilibrium price', f1(P)), ('Equilibrium quantity', f1(Q))];
    },
    paint: (c, s, v, t, p) {
      final pl = Plot(c, s, 0, 12, 0, 12, p, xl: 'quantity', yl: 'price', xt: 6, yt: 6);
      c.drawLine(pl.at(0, 10), pl.at(10, 0), st(p.line, 1.5));
      c.drawLine(pl.at(0, 2), pl.at(10, 12), st(p.line, 1.5));
      final D = v['D']!, S = v['S']!;
      pl.curve((q) => 10 + D - q, p.blue.deep);
      pl.curve((q) => q + 2 - S, p.peach.deep);
      final P = (12 + D - S) / 2, Q = 10 - P + D;
      dashed(c, pl.at(Q, 0), pl.at(Q, P), st(p.ink2, 1.2));
      dashed(c, pl.at(0, P), pl.at(Q, P), st(p.ink2, 1.2));
      pl.dot(Q, P, p.sage.deep);
      txt(c, 'D', pl.at(math.min(11, 9.5 + D), 10 + D - math.min(11, 9.5 + D)) + const Offset(6, -10), p.blue.deep, size: 14);
      txt(c, 'S', pl.at(math.min(9.5 + S, 11), math.min(9.5 + S, 11) + 2 - S) + const Offset(6, -4), p.peach.deep, size: 14);
    },
  ),
  'timeline': (m) {
    final ev = [for (final e in (m['events'] as List? ?? const [])) ((e[0] as num).toDouble(), '${e[1]}')]..sort((a, b) => a.$1.compareTo(b.$1));
    final y0 = ev.isEmpty ? 0.0 : ev.first.$1, y1 = ev.isEmpty ? 1.0 : ev.last.$1;
    String yr(double y) => y < 0 ? '${-y.round()} BC' : '${y.round()}';
    return SimSpec(
      height: 230,
      params: [Prm('y', 'Year', y0, y1, y0, step: math.max(1, ((y1 - y0) / 200).roundToDouble()), fmt: yr)],
      out: (v) {
        final e = ev.lastWhere((e) => e.$1 <= v['y']!, orElse: () => ev.first);
        return [(yr(e.$1), e.$2)];
      },
      paint: (c, s, v, t, p) {
        final l = 24.0, r = s.width - 24, y = s.height * .55;
        double x(double yy) => l + (r - l) * (yy - y0) / (y1 - y0 == 0 ? 1 : y1 - y0);
        c.drawLine(Offset(l, y), Offset(r, y), st(p.ink2, 3));
        final cur = ev.lastIndexWhere((e) => e.$1 <= v['y']!);
        for (final (i, e) in ev.indexed) {
          final on = i == cur, q = Offset(x(e.$1), y);
          c.drawCircle(q, on ? 9 : 5, fl(on ? p.peach.deep : p.blue.deep));
          if (on || ev.length <= 6) {
            final up = i.isEven;
            c.drawLine(q, q + Offset(0, up ? -30 : 30), st(p.line, 1));
            txt(c, yr(e.$1), q + Offset(0, up ? -44 : 36), on ? p.peach.deep : p.ink2, size: on ? 14 : 11, center: true);
          }
        }
        final xv = x(v['y']!);
        c.drawPath(Path()..moveTo(xv, y + 14)..lineTo(xv - 8, y + 26)..lineTo(xv + 8, y + 26)..close(), fl(p.ink));
      },
    );
  },
};

String _refName(double v) => ['none', 'in the x-axis', 'in the y-axis'][v.toInt()];
String _shift(double v) => v == 0 ? 'none' : (v > 0 ? 'increase +${v.toInt()}' : 'decrease ${v.toInt()}');
// keep _fact for future probability sims
double nCr(int n, int r) => _fact(n) / (_fact(r) * _fact(n - r));

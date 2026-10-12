// Original quote-card artwork, drawn natively (no image files): a gradient, two soft circles, a woven
// tilet-style band along the bottom edge, and one simple motif from school life and the Eritrean landscape
// (amba mountains, the winding road up from Massawa, palm avenues, a jebena, a dhow on the Red Sea, a lamp…).
// One CustomPainter per card, never repainted (shouldRepaint compares the motif only); lists wrap each card in a
// RepaintBoundary, so scrolling the gallery only moves cached layers.
import 'dart:math' as math;

import 'package:flutter/widgets.dart';

/// card gradients (top-left → bottom-right); white text sits on all of them
const Map<String, (Color, Color)> kQuoteTones = {
  'sunrise': (Color(0xFFF2996F), Color(0xFFD9534F)),
  'meadow': (Color(0xFF7FB97A), Color(0xFF3C8460)),
  'sky': (Color(0xFF6FA8E0), Color(0xFF3E64B3)),
  'dusk': (Color(0xFFA77BD0), Color(0xFFD5607F)),
  'sand': (Color(0xFFD9A867), Color(0xFFA9692F)),
  'coral': (Color(0xFFF08372), Color(0xFFC2415A)),
  'sea': (Color(0xFF4FB0B4), Color(0xFF256E90)),
  'night': (Color(0xFF3F4C80), Color(0xFF1C2244)),
  'butter': (Color(0xFFE9B949), Color(0xFFC77E1E)),
  'lilac': (Color(0xFFAE95DD), Color(0xFF6D52AD)),
  'mint': (Color(0xFF5DBFA8), Color(0xFF2B7F72)),
};

(Color, Color) quoteTone(String t) => kQuoteTones[t] ?? kQuoteTones['sky']!;

/// motifs [QuoteArtPainter] can draw
const kQuoteMotifs = {
  'road', 'sprout', 'sun', 'flag', 'clock', 'desk', 'book', 'pencil', 'stones', 'tree', 'mountain', 'lamp', 'bicycle', 'map', 'bulb', //
  'flask', 'gear', 'chat', 'cap', 'globe', 'cloud', 'moon', 'star', 'chart', 'palms', 'jebena', 'board', 'boat',
};

class QuoteArtPainter extends CustomPainter {
  QuoteArtPainter({required this.motif, required this.tone, this.radius = 22, this.motifScale = .5});
  final String motif, tone;
  final double radius, motifScale;

  static final _c1 = Paint()..color = const Color(0xE6FFFFFF);
  static final _c2 = Paint()..color = const Color(0x8CFFFFFF);
  static final _c3 = Paint()..color = const Color(0x4DFFFFFF);
  static final _c4 = Paint()..color = const Color(0x1FFFFFFF);
  static Paint _st(Paint p, double w) => Paint()
    ..color = p.color
    ..style = PaintingStyle.stroke
    ..strokeWidth = w
    ..strokeCap = StrokeCap.round
    ..strokeJoin = StrokeJoin.round;

  @override
  void paint(Canvas canvas, Size size) {
    final (a, b) = quoteTone(tone);
    final r = Offset.zero & size;
    final rr = RRect.fromRectAndRadius(r, Radius.circular(radius));
    canvas.save();
    canvas.clipRRect(rr);
    canvas.drawRect(r, Paint()..shader = LinearGradient(begin: Alignment.topLeft, end: Alignment.bottomRight, colors: [a, b]).createShader(r));
    // soft circles
    canvas.drawCircle(Offset(size.width * .92, size.height * .06), size.width * .34, _c4);
    canvas.drawCircle(Offset(size.width * .02, size.height * .78), size.width * .22, _c4);
    // motif in the bottom-right corner, in a 100×100 design box
    final m = math.min(size.width, size.height) * motifScale;
    canvas.save();
    canvas.translate(size.width - m - size.width * .04, size.height - m - 14);
    canvas.scale(m / 100);
    _motif(canvas, motif);
    canvas.restore();
    _tilet(canvas, size);
    canvas.restore();
  }

  /// woven border band: a light strip with small diamonds and dots
  void _tilet(Canvas c, Size s) {
    const h = 10.0;
    final y = s.height - h;
    c.drawRect(Rect.fromLTWH(0, y, s.width, h), Paint()..color = const Color(0x33000000));
    c.drawRect(Rect.fromLTWH(0, y, s.width, 1.2), _c3);
    var i = 0;
    for (double x = 6; x < s.width; x += 12, i++) {
      final p = Path()
        ..moveTo(x, y + 1.8)
        ..lineTo(x + 3.6, y + h / 2 + .6)
        ..lineTo(x, y + h - .6)
        ..lineTo(x - 3.6, y + h / 2 + .6)
        ..close();
      c.drawPath(p, i.isEven ? _c2 : _c3);
      c.drawCircle(Offset(x + 6, y + h / 2 + .6), .9, _c2);
    }
  }

  void _motif(Canvas c, String m) {
    final s1 = _st(_c1, 4), s2 = _st(_c2, 3);
    switch (m) {
      case 'road':
        c.drawPath(_hill(42, 22, 50), _c3);
        c.drawPath(_hill(70, 55, 66), _c2);
        c.drawCircle(const Offset(80, 18), 9, _c1);
        c.drawPath(
          Path()
            ..moveTo(18, 100)
            ..cubicTo(60, 92, 70, 84, 40, 78)
            ..cubicTo(14, 72, 30, 64, 58, 62)
            ..cubicTo(76, 60, 70, 54, 56, 52),
          _st(_c1, 5),
        );
      case 'sprout':
        c.drawOval(const Rect.fromLTWH(18, 84, 64, 18), _c3);
        c.drawLine(const Offset(50, 92), const Offset(50, 46), s1);
        c.drawPath(_leaf(const Offset(50, 62), -1, 30), _c1);
        c.drawPath(_leaf(const Offset(50, 50), 1, 26), _c2);
      case 'sun':
        c.drawPath(_hill(80, 60, 72), _c3);
        for (var i = 0; i < 10; i++) {
          final a = i * math.pi / 5;
          c.drawLine(Offset(50 + 26 * math.cos(a), 46 + 26 * math.sin(a)), Offset(50 + 36 * math.cos(a), 46 + 36 * math.sin(a)), s2);
        }
        c.drawCircle(const Offset(50, 46), 19, _c1);
      case 'flag':
        c.drawPath(_amba(), _c3);
        c.drawPath(_hill(86, 70, 80), _c2);
        c.drawLine(const Offset(52, 74), const Offset(52, 16), _st(_c1, 3.5));
        c.drawPath(
          Path()
            ..moveTo(53, 17)
            ..lineTo(86, 26)
            ..lineTo(53, 37)
            ..close(),
          _c1,
        );
      case 'clock':
        c.drawCircle(const Offset(50, 52), 36, _c3);
        c.drawCircle(const Offset(50, 52), 30, _c1);
        final ink = _st(Paint()..color = const Color(0x66000000), 4);
        c.drawLine(const Offset(50, 52), const Offset(50, 32), ink);
        c.drawLine(const Offset(50, 52), const Offset(64, 60), ink);
        for (var i = 0; i < 12; i++) {
          final a = i * math.pi / 6;
          c.drawCircle(Offset(50 + 25 * math.cos(a), 52 + 25 * math.sin(a)), 1.4, Paint()..color = const Color(0x55000000));
        }
      case 'desk':
        c.drawRRect(RRect.fromLTRBR(8, 58, 92, 66, const Radius.circular(3)), _c1);
        c.drawRect(const Rect.fromLTWH(14, 66, 5, 32), _c2);
        c.drawRect(const Rect.fromLTWH(81, 66, 5, 32), _c2);
        c.drawPath(_book(const Offset(36, 56), 34, 12), _c2);
        c.drawRRect(RRect.fromLTRBR(70, 38, 80, 58, const Radius.circular(2)), _c3);
        c.drawLine(const Offset(73, 38), const Offset(70, 24), _st(_c1, 2.5));
        c.drawLine(const Offset(77, 38), const Offset(82, 26), _st(_c2, 2.5));
      case 'book':
        c.drawPath(
          Path()
            ..moveTo(50, 40)
            ..quadraticBezierTo(30, 30, 8, 36)
            ..lineTo(8, 86)
            ..quadraticBezierTo(30, 80, 50, 90)
            ..close(),
          _c1,
        );
        c.drawPath(
          Path()
            ..moveTo(50, 40)
            ..quadraticBezierTo(70, 30, 92, 36)
            ..lineTo(92, 86)
            ..quadraticBezierTo(70, 80, 50, 90)
            ..close(),
          _c2,
        );
        final ln = _st(Paint()..color = const Color(0x33000000), 2);
        for (var i = 0; i < 4; i++) {
          c.drawLine(Offset(16, 48 + i * 9.0), Offset(42, 52 + i * 9.0), ln);
          c.drawLine(Offset(58, 52 + i * 9.0), Offset(84, 48 + i * 9.0), ln);
        }
      case 'pencil':
        c.drawPath(
          Path()
            ..moveTo(10, 92)
            ..cubicTo(30, 70, 40, 96, 60, 80),
          _st(_c3, 3),
        );
        c.save();
        c.translate(52, 50);
        c.rotate(-math.pi / 4);
        c.drawRect(const Rect.fromLTWH(-8, -40, 16, 58), _c1);
        c.drawRect(const Rect.fromLTWH(-8, -48, 16, 8), _c2);
        c.drawPath(
          Path()
            ..moveTo(-8, 18)
            ..lineTo(8, 18)
            ..lineTo(0, 34)
            ..close(),
          _c2,
        );
        c.restore();
      case 'stones':
        c.drawOval(const Rect.fromLTWH(14, 80, 72, 18), _c1);
        c.drawOval(const Rect.fromLTWH(24, 64, 52, 18), _c2);
        c.drawOval(const Rect.fromLTWH(34, 50, 32, 16), _c1);
        for (final (x, y, r) in const [(50.0, 18.0, 6.0), (50.0, 36.0, 4.0)]) {
          c.drawPath(_drop(Offset(x, y), r), _c2);
        }
      case 'tree':
        c.drawOval(const Rect.fromLTWH(4, 88, 92, 12), _c3);
        c.drawPath(
          Path()
            ..moveTo(46, 92)
            ..lineTo(48, 56)
            ..lineTo(34, 40)
            ..moveTo(48, 60)
            ..lineTo(64, 40)
            ..moveTo(52, 92)
            ..lineTo(50, 60),
          _st(_c1, 5),
        );
        c.drawOval(const Rect.fromLTWH(10, 22, 80, 22), _c2);
        c.drawOval(const Rect.fromLTWH(22, 14, 56, 18), _c1);
      case 'mountain':
        c.drawCircle(const Offset(74, 22), 9, _c1);
        c.drawPath(_amba(), _c2);
        c.drawPath(
          Path()
            ..moveTo(-4, 100)
            ..lineTo(14, 70)
            ..lineTo(30, 70)
            ..lineTo(44, 84)
            ..lineTo(60, 60)
            ..lineTo(78, 60)
            ..lineTo(104, 100)
            ..close(),
          _c1,
        );
      case 'lamp':
        c.drawCircle(const Offset(50, 46), 40, _c4);
        c.drawCircle(const Offset(50, 46), 26, _c4);
        c.drawOval(const Rect.fromLTWH(26, 84, 48, 14), _c1);
        c.drawPath(
          Path()
            ..moveTo(38, 84)
            ..quadraticBezierTo(28, 56, 42, 36)
            ..lineTo(58, 36)
            ..quadraticBezierTo(72, 56, 62, 84)
            ..close(),
          _c2,
        );
        c.drawPath(_drop(const Offset(50, 54), 8), _c1);
        c.drawRect(const Rect.fromLTWH(40, 28, 20, 8), _c1);
      case 'bicycle':
        c.drawLine(const Offset(0, 92), const Offset(100, 92), _st(_c3, 3));
        final w = _st(_c1, 4);
        c.drawCircle(const Offset(24, 72), 18, w);
        c.drawCircle(const Offset(76, 72), 18, w);
        c.drawPath(
          Path()
            ..moveTo(24, 72)
            ..lineTo(42, 46)
            ..lineTo(66, 46)
            ..lineTo(76, 72)
            ..moveTo(42, 46)
            ..lineTo(50, 72)
            ..lineTo(24, 72)
            ..moveTo(50, 72)
            ..lineTo(66, 46)
            ..moveTo(40, 38)
            ..lineTo(48, 38)
            ..moveTo(42, 46)
            ..lineTo(44, 38)
            ..moveTo(66, 46)
            ..lineTo(64, 34)
            ..lineTo(72, 32),
          _st(_c1, 3.5),
        );
      case 'map':
        for (var i = 0; i < 3; i++) {
          final x = 10 + i * 27.0;
          c.drawPath(
            Path()
              ..moveTo(x, i.isOdd ? 34 : 28)
              ..lineTo(x + 27, i.isOdd ? 28 : 34)
              ..lineTo(x + 27, i.isOdd ? 92 : 98)
              ..lineTo(x, i.isOdd ? 98 : 92)
              ..close(),
            i.isOdd ? _c2 : _c1,
          );
        }
        final dash = _st(Paint()..color = const Color(0x55000000), 2.5);
        for (var i = 0; i < 6; i++) {
          c.drawLine(Offset(18 + i * 10.0, 84 - i * 6.0 + (i.isOdd ? 4 : 0)), Offset(22 + i * 10.0, 82 - i * 6.0 + (i.isOdd ? 4 : 0)), dash);
        }
        c.drawPath(_pin(const Offset(76, 40), 11), Paint()..color = const Color(0xFFFFFFFF));
        c.drawCircle(const Offset(76, 38), 4, Paint()..color = const Color(0x55000000));
      case 'bulb':
        for (var i = 0; i < 7; i++) {
          final a = math.pi + i * math.pi / 6;
          c.drawLine(Offset(50 + 30 * math.cos(a), 42 + 30 * math.sin(a)), Offset(50 + 40 * math.cos(a), 42 + 40 * math.sin(a)), s2);
        }
        c.drawCircle(const Offset(50, 42), 22, _c1);
        c.drawRect(const Rect.fromLTWH(41, 60, 18, 10), _c1);
        c.drawRRect(RRect.fromLTRBR(42, 72, 58, 84, const Radius.circular(3)), _c2);
      case 'flask':
        final f = Path()
          ..moveTo(42, 16)
          ..lineTo(58, 16)
          ..lineTo(58, 44)
          ..lineTo(82, 90)
          ..lineTo(18, 90)
          ..lineTo(42, 44)
          ..close();
        c.drawPath(f, _c2);
        c.save();
        c.clipPath(f);
        c.drawRect(const Rect.fromLTWH(0, 64, 100, 40), _c1);
        c.restore();
        for (final (x, y, r) in const [(44.0, 74.0, 3.0), (56.0, 80.0, 4.0), (52.0, 54.0, 2.5), (60.0, 30.0, 3.5), (66.0, 14.0, 2.5)]) {
          c.drawCircle(Offset(x, y), r, _c3);
        }
      case 'gear':
        final g = Path();
        for (var i = 0; i < 8; i++) {
          final a = i * math.pi / 4;
          g.addRect(Rect.fromCenter(center: Offset(50 + 32 * math.cos(a), 54 + 32 * math.sin(a)), width: 13, height: 13));
        }
        c.drawPath(g, _c2);
        c.drawCircle(const Offset(50, 54), 30, _c1);
        c.drawCircle(const Offset(50, 54), 11, Paint()..color = const Color(0x44000000));
      case 'chat':
        c.drawRRect(RRect.fromLTRBR(4, 20, 64, 58, const Radius.circular(12)), _c1);
        c.drawPath(
          Path()
            ..moveTo(16, 56)
            ..lineTo(12, 70)
            ..lineTo(30, 57)
            ..close(),
          _c1,
        );
        c.drawRRect(RRect.fromLTRBR(36, 52, 96, 86, const Radius.circular(12)), _c2);
        c.drawPath(
          Path()
            ..moveTo(84, 84)
            ..lineTo(90, 96)
            ..lineTo(72, 85)
            ..close(),
          _c2,
        );
        for (var i = 0; i < 3; i++) {
          c.drawCircle(Offset(22 + i * 12.0, 39), 3.2, Paint()..color = const Color(0x55000000));
        }
      case 'cap':
        c.drawPath(
          Path()
            ..moveTo(50, 24)
            ..lineTo(96, 42)
            ..lineTo(50, 60)
            ..lineTo(4, 42)
            ..close(),
          _c1,
        );
        c.drawPath(
          Path()
            ..moveTo(24, 50)
            ..lineTo(24, 70)
            ..quadraticBezierTo(50, 84, 76, 70)
            ..lineTo(76, 50)
            ..lineTo(50, 60)
            ..close(),
          _c2,
        );
        c.drawLine(const Offset(50, 42), const Offset(84, 52), _st(_c1, 2.5));
        c.drawLine(const Offset(84, 52), const Offset(84, 74), _st(_c1, 2.5));
        c.drawCircle(const Offset(84, 76), 4, _c1);
      case 'globe':
        c.drawCircle(const Offset(50, 44), 32, _c2);
        final l = _st(_c1, 2.6);
        c.drawOval(const Rect.fromLTWH(34, 12, 32, 64), l);
        c.drawLine(const Offset(18, 44), const Offset(82, 44), l);
        c.drawLine(const Offset(24, 28), const Offset(76, 28), l);
        c.drawLine(const Offset(24, 60), const Offset(76, 60), l);
        c.drawCircle(const Offset(50, 44), 32, l);
        c.drawLine(const Offset(50, 76), const Offset(50, 88), _st(_c1, 4));
        c.drawRRect(RRect.fromLTRBR(30, 88, 70, 96, const Radius.circular(4)), _c1);
      case 'cloud':
        for (var i = 0; i < 3; i++) {
          c.drawLine(Offset(8 + i * 8.0, 82 + i * 7.0), Offset(52 + i * 8.0, 82 + i * 7.0), s2);
        }
        for (final (x, y, r) in const [(30.0, 56.0, 16.0), (50.0, 44.0, 22.0), (72.0, 56.0, 16.0)]) {
          c.drawCircle(Offset(x, y), r, _c1);
        }
        c.drawRRect(RRect.fromLTRBR(14, 54, 88, 72, const Radius.circular(9)), _c1);
      case 'moon':
        final moon = Path.combine(
          PathOperation.difference,
          Path()..addOval(Rect.fromCircle(center: const Offset(56, 50), radius: 32)),
          Path()..addOval(Rect.fromCircle(center: const Offset(72, 40), radius: 28)),
        );
        c.drawPath(moon, _c1);
        for (final (x, y, r) in const [(80.0, 76.0, 4.0), (90.0, 54.0, 2.5), (20.0, 20.0, 3.0), (34.0, 92.0, 2.0)]) {
          c.drawPath(_star(Offset(x, y), r * 2, r), _c2);
        }
      case 'star':
        c.drawPath(_star(const Offset(54, 52), 34, 14), _c1);
        c.drawPath(_star(const Offset(16, 22), 9, 4), _c2);
        c.drawPath(_star(const Offset(88, 90), 7, 3), _c2);
      case 'chart':
        for (final (i, h) in const [(0, 22.0), (1, 38.0), (2, 54.0), (3, 72.0)]) {
          c.drawRRect(RRect.fromLTRBR(8 + i * 22.0, 96 - h, 24 + i * 22.0, 96, const Radius.circular(4)), i == 3 ? _c1 : _c2);
        }
        c.drawPath(
          Path()
            ..moveTo(10, 62)
            ..lineTo(36, 48)
            ..lineTo(56, 40)
            ..lineTo(86, 12),
          _st(_c1, 3.5),
        );
        c.drawPath(
          Path()
            ..moveTo(76, 12)
            ..lineTo(88, 10)
            ..lineTo(86, 22),
          _st(_c1, 3.5),
        );
      case 'palms':
        c.drawLine(const Offset(0, 96), const Offset(100, 96), _st(_c3, 3));
        for (final (x, h) in const [(18.0, 80.0), (50.0, 62.0), (76.0, 48.0)]) {
          _palm(c, Offset(x, 96), h);
        }
      case 'jebena':
        c.drawCircle(const Offset(56, 70), 22, _c1);
        c.drawPath(
          Path()
            ..moveTo(50, 52)
            ..lineTo(52, 26)
            ..lineTo(60, 26)
            ..lineTo(62, 52)
            ..close(),
          _c1,
        );
        c.drawOval(const Rect.fromLTWH(48, 20, 16, 7), _c2);
        c.drawLine(const Offset(38, 64), const Offset(22, 46), _st(_c1, 5));
        c.drawPath(
          Path()
            ..moveTo(62, 34)
            ..quadraticBezierTo(86, 36, 76, 62),
          _st(_c2, 4),
        );
        c.drawRRect(RRect.fromLTRBR(8, 84, 22, 94, const Radius.circular(3)), _c2);
        c.drawRRect(RRect.fromLTRBR(26, 86, 38, 95, const Radius.circular(3)), _c2);
        for (var i = 0; i < 3; i++) {
          c.drawPath(
            Path()
              ..moveTo(52 + i * 6.0, 16)
              ..quadraticBezierTo(48 + i * 6.0, 10, 53 + i * 6.0, 4),
            _st(_c3, 2),
          );
        }
      case 'board':
        c.drawRRect(RRect.fromLTRBR(4, 18, 96, 80, const Radius.circular(6)), _c1);
        c.drawRRect(RRect.fromLTRBR(10, 24, 90, 74, const Radius.circular(3)), Paint()..color = const Color(0x55000000));
        final ch = _st(_c1, 2.6);
        // a² + b² = c² in chalk strokes: two short formulas and a small triangle
        c.drawPath(
          Path()
            ..moveTo(18, 58)
            ..lineTo(40, 58)
            ..lineTo(18, 38)
            ..close(),
          ch,
        );
        c.drawLine(const Offset(50, 40), const Offset(82, 40), ch);
        c.drawLine(const Offset(50, 52), const Offset(74, 52), ch);
        c.drawLine(const Offset(50, 64), const Offset(80, 64), ch);
        c.drawLine(const Offset(30, 80), const Offset(30, 96), _st(_c2, 4));
        c.drawLine(const Offset(70, 80), const Offset(70, 96), _st(_c2, 4));
      case 'boat':
        for (var i = 0; i < 2; i++) {
          final y = 86 + i * 8.0;
          final wv = Path()..moveTo(0, y);
          for (double x = 0; x < 100; x += 20) {
            wv.quadraticBezierTo(x + 5, y - 4, x + 10, y);
            wv.quadraticBezierTo(x + 15, y + 4, x + 20, y);
          }
          c.drawPath(wv, _st(i == 0 ? _c2 : _c3, 3));
        }
        c.drawPath(
          Path()
            ..moveTo(14, 70)
            ..lineTo(90, 66)
            ..lineTo(78, 82)
            ..lineTo(26, 82)
            ..close(),
          _c1,
        );
        c.drawLine(const Offset(52, 68), const Offset(52, 18), _st(_c1, 3));
        c.drawPath(
          Path()
            ..moveTo(52, 14)
            ..quadraticBezierTo(80, 34, 84, 62)
            ..lineTo(54, 62)
            ..close(),
          _c2,
        );
      default:
        c.drawPath(_star(const Offset(50, 50), 30, 12), _c1);
    }
  }

  void _palm(Canvas c, Offset base, double h) {
    final top = Offset(base.dx + h * .08, base.dy - h);
    c.drawPath(
      Path()
        ..moveTo(base.dx, base.dy)
        ..quadraticBezierTo(base.dx - h * .06, base.dy - h * .5, top.dx, top.dy),
      _st(_c1, math.max(2.5, h * .07)),
    );
    for (var i = 0; i < 6; i++) {
      final a = -math.pi + i * math.pi / 5;
      final len = h * .42;
      final end = Offset(top.dx + len * math.cos(a), top.dy + len * math.sin(a) * .6 + len * .25);
      final ctl = Offset(top.dx + len * .55 * math.cos(a), top.dy - len * .25);
      c.drawPath(
        Path()
          ..moveTo(top.dx, top.dy)
          ..quadraticBezierTo(ctl.dx, ctl.dy, end.dx, end.dy),
        _st(i.isEven ? _c1 : _c2, math.max(2, h * .055)),
      );
    }
  }

  /// a soft mound that rises from the bottom edge (no hard sides)
  Path _hill(double peakX, double peakY, double baseY) => Path()
    ..moveTo(-6, 100)
    ..quadraticBezierTo(peakX * .35, baseY, peakX, peakY + 4)
    ..quadraticBezierTo(peakX + (100 - peakX) * .6, peakY + 6, 106, 100)
    ..close();

  /// flat-topped amba mountains of the Eritrean highlands
  Path _amba() => Path()
    ..moveTo(-4, 100)
    ..lineTo(14, 42)
    ..lineTo(38, 42)
    ..lineTo(50, 60)
    ..lineTo(64, 34)
    ..lineTo(86, 34)
    ..lineTo(104, 100)
    ..close();

  Path _leaf(Offset o, double dir, double len) => Path()
    ..moveTo(o.dx, o.dy)
    ..quadraticBezierTo(o.dx + dir * len * .5, o.dy - len * .7, o.dx + dir * len, o.dy - len * .45)
    ..quadraticBezierTo(o.dx + dir * len * .55, o.dy + len * .05, o.dx, o.dy)
    ..close();

  Path _drop(Offset o, double r) => Path()
    ..moveTo(o.dx, o.dy - r * 1.8)
    ..quadraticBezierTo(o.dx + r * 1.2, o.dy - r * .2, o.dx + r, o.dy + r * .3)
    ..arcToPoint(Offset(o.dx - r, o.dy + r * .3), radius: Radius.circular(r), clockwise: true)
    ..quadraticBezierTo(o.dx - r * 1.2, o.dy - r * .2, o.dx, o.dy - r * 1.8)
    ..close();

  Path _pin(Offset o, double r) => Path()
    ..moveTo(o.dx, o.dy + r * 2)
    ..quadraticBezierTo(o.dx - r * 1.2, o.dy + r * .4, o.dx - r, o.dy - r * .2)
    ..arcToPoint(Offset(o.dx + r, o.dy - r * .2), radius: Radius.circular(r))
    ..quadraticBezierTo(o.dx + r * 1.2, o.dy + r * .4, o.dx, o.dy + r * 2)
    ..close();

  Path _star(Offset o, double ro, double ri) {
    final p = Path();
    for (var i = 0; i < 10; i++) {
      final r = i.isEven ? ro : ri, a = -math.pi / 2 + i * math.pi / 5;
      final pt = Offset(o.dx + r * math.cos(a), o.dy + r * math.sin(a));
      i == 0 ? p.moveTo(pt.dx, pt.dy) : p.lineTo(pt.dx, pt.dy);
    }
    return p..close();
  }

  Path _book(Offset o, double w, double h) => Path()..addRRect(RRect.fromLTRBR(o.dx, o.dy - h, o.dx + w, o.dy, const Radius.circular(2)));

  @override
  bool shouldRepaint(QuoteArtPainter o) => o.motif != motif || o.tone != tone || o.radius != radius || o.motifScale != motifScale;
}

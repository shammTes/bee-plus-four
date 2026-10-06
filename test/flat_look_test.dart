// Flat look (Perf.flat): clay decorations paint one solid colour + hairline / hard ledge, nothing blurred.
import 'dart:typed_data';
import 'dart:ui' as ui;

import 'package:flutter/rendering.dart';
import 'package:flutter/widgets.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:high/high/theme/clay.dart';
import 'package:high/high/theme/perf.dart';

const _card = ClayDecoration(
  fills: [
    LinearFill.vertical([Color(0xFFFFFFFF), Color(0xFFE0E8F0)], [0, 1]),
    LinearFill.vertical([Color(0x66FFFFFF), Color(0x00FFFFFF)], [0, 1]), // sheen over the base: dropped when flat
  ],
  shadows: [Shadow3(0, 10, 24, 0, Color(0x40203040)), Shadow3(0, -2, 6, 0, Color(0x30000000), inset: true)],
  radius: BorderRadius.all(Radius.circular(16)),
);

Future<(int, int, ByteData)> _paint(WidgetTester t, Decoration d) async {
  final k = GlobalKey();
  await t.pumpWidget(const SizedBox());
  await t.pumpWidget(
    Directionality(
      textDirection: TextDirection.ltr,
      child: Center(
        child: RepaintBoundary(
          key: k,
          child: Container(
            width: 200,
            height: 160,
            color: const Color(0xFF808080),
            alignment: Alignment.center,
            child: Container(width: 120, height: 60, decoration: d),
          ),
        ),
      ),
    ),
  );
  final rb = k.currentContext!.findRenderObject()! as RenderRepaintBoundary;
  final data = await t.runAsync(() async {
    final img = await rb.toImage();
    return (await img.toByteData(format: ui.ImageByteFormat.rawRgba))!;
  });
  return (200, 160, data!);
}

Color _px((int, int, ByteData) img, int x, int y) {
  final o = (y * img.$1 + x) * 4;
  final b = img.$3;
  return Color.fromARGB(b.getUint8(o + 3), b.getUint8(o), b.getUint8(o + 1), b.getUint8(o + 2));
}

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();
  tearDown(() => Perf.flat = true);

  testWidgets('flat: no blur halo around the card, solid fill', (t) async {
    Perf.flat = true;
    final img = await _paint(t, _card);
    // the card spans x 40..160, y 50..110; 12px below it is plain background (a blurred 24px shadow would darken it)
    expect(_px(img, 100, 122), const Color(0xFF808080));
    expect(_px(img, 20, 80), const Color(0xFF808080));
    // centre: one colour (gradient midpoint, sheen dropped), same near the top and bottom
    final mid = _px(img, 100, 80), top = _px(img, 100, 56), bottom = _px(img, 100, 104);
    expect(mid.toARGB32(), top.toARGB32());
    expect(mid.toARGB32(), bottom.toARGB32());
  });

  testWidgets('clay: soft shadow and gradient are still painted', (t) async {
    Perf.flat = false;
    final img = await _paint(t, _card);
    expect(_px(img, 100, 122), isNot(const Color(0xFF808080)));
    expect(_px(img, 100, 56).toARGB32(), isNot(_px(img, 100, 104).toARGB32()));
  });

  testWidgets('pressed look darkens in flat mode only', (t) async {
    Perf.flat = true;
    expect(_card.pressedBy(1), isNot(_card));
    expect(_card.pressedBy(0), _card);
    Perf.flat = false;
    expect(_card.pressedBy(1), _card);
  });
}

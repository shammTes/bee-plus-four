// Cached maths pictures (lib/high/notes/jr/notes/math_pic.dart) must look exactly like live flutter_math.
import 'dart:io' as io;
import 'dart:typed_data';
import 'dart:ui' as ui;

import 'package:flutter/rendering.dart';
import 'package:flutter/widgets.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:high/high/notes/jr/notes/math_pic.dart';
import 'package:high/high/notes/jr/notes/rich.dart';

import 'helpers.dart';

const _paras = [
  r'Speed is \(v = \frac{d}{t}\) and energy \(E_k = \tfrac12 m v^2\) in joules.',
  r'Display: \[ x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a} \] then more text \(\alpha + \beta^2\).',
  r'Sum \(\sum_{i=1}^{n} i = \frac{n(n+1)}{2}\), matrix \(\begin{pmatrix} 1 & 2 \\ 3 & 4 \end{pmatrix}\).',
  r'A very long inline formula \(a_1 + a_2 + a_3 + a_4 + a_5 + a_6 + a_7 + a_8 + a_9 + a_{10} + a_{11} + a_{12} + a_{13} + a_{14} + a_{15}\) shrinks.',
  r'Broken TeX \(\frac{1}{\) falls back to text.',
];

Widget _host(Key k, List<String> paras, {double scale = 1}) => Directionality(
  textDirection: TextDirection.ltr,
  child: MediaQuery(
    data: MediaQueryData(size: const Size(360, 900), textScaler: TextScaler.linear(scale)),
    child: Center(
      child: RepaintBoundary(
        key: k,
        child: Container(
          width: 340,
          color: const Color(0xFFFFFFFF),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [for (final p in paras) RichPara(p, style: const TextStyle(fontFamily: 'HighNunito', fontSize: 16, color: Color(0xFF223344)))],
          ),
        ),
      ),
    ),
  ),
);

Future<(Size, Uint8List)> _shot(WidgetTester t, List<String> paras, {required bool cached, double scale = 1}) async {
  MathPictures.enabled = cached;
  MathPictures.clear();
  final k = GlobalKey();
  await t.pumpWidget(const SizedBox());
  await t.pumpWidget(_host(k, paras, scale: scale));
  final rb = k.currentContext!.findRenderObject()! as RenderRepaintBoundary;
  final bytes = await t.runAsync(() async {
    final img = await rb.toImage();
    final d = await img.toByteData(format: ui.ImageByteFormat.rawRgba);
    return d!.buffer.asUint8List();
  });
  return (rb.size, bytes!);
}

bool _isLong(String p) => p.contains('shrinks');

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();
  setUpAll(loadFonts);
  tearDown(() => MathPictures.enabled = true);

  // a shrunk formula is the same picture, but anti-aliased at a fractional scale by a canvas transform instead of a
  // transform layer, so its edge pixels may differ by a few levels
  final cases = {'plain': (_paras.where((p) => !_isLong(p)).toList(), 2000), 'shrunk': (_paras.where(_isLong).toList(), 20)};
  for (final scale in [1.0, 1.3]) {
    for (final MapEntry(key: name, value: (paras, frac)) in cases.entries) {
      testWidgets('pictured maths match live flutter_math ($name, text scale $scale)', (t) async {
        final live = await _shot(t, paras, cached: false, scale: scale);
        final pic = await _shot(t, paras, cached: true, scale: scale);
        expect(MathPictures.pictured, greaterThan(0), reason: '${MathPictures.lastError}');
        expect(pic.$1, live.$1);
        var diff = 0;
        for (var i = 0; i < live.$2.length; i++) {
          if ((live.$2[i] - pic.$2[i]).abs() > 8) diff++;
        }
        if (diff >= live.$2.length ~/ frac) {
          await t.runAsync(() async {
            for (final (n, b) in [('live', live.$2), ('pic', pic.$2)]) {
              final w = (live.$1.width).round(), h = (live.$1.height).round();
              final buf = await ui.ImmutableBuffer.fromUint8List(b);
              final desc = ui.ImageDescriptor.raw(buf, width: w, height: h, pixelFormat: ui.PixelFormat.rgba8888);
              final img = (await (await desc.instantiateCodec()).getNextFrame()).image;
              final png = await img.toByteData(format: ui.ImageByteFormat.png);
              io.File('${io.Directory.systemTemp.path}/math_$n.png').writeAsBytesSync(png!.buffer.asUint8List());
            }
          });
        }
        expect(diff, lessThan(live.$2.length ~/ frac), reason: '$diff differing channels (images in the temp dir)');
      });
    }
  }

  testWidgets('a formula is a single leaf box, also inside a lazy list built during layout', (t) async {
    MathPictures.clear();
    await t.pumpWidget(
      Directionality(
        textDirection: TextDirection.ltr,
        child: MediaQuery(
          data: const MediaQueryData(size: Size(360, 640)),
          child: ListView.builder(
            itemCount: 200,
            itemBuilder: (_, i) => RichPara(_paras[i % 4], style: const TextStyle(fontSize: 16, color: Color(0xFF000000))),
          ),
        ),
      ),
    );
    expect(t.takeException(), isNull);
    expect(find.byType(MathPictureBox), findsWidgets);
    // the same paragraph (and formula) on screen several times: no GlobalKey clashes
    await t.drag(find.byType(ListView), const Offset(0, -3000));
    await t.pumpAndSettle();
    expect(t.takeException(), isNull);
    expect(find.byType(MathPictureBox), findsWidgets);
    expect(MathPictures.length, lessThan(20)); // reused, not re-rendered per row
  });

  testWidgets('narrow line: inline maths scale down, baseline kept', (t) async {
    final pic = MathPictures.of(r'a_1 + a_2 + a_3 + a_4 + a_5 + a_6 + a_7', display: false, fontSize: 17, color: const Color(0xFF000000))!;
    await t.pumpWidget(
      Directionality(
        textDirection: TextDirection.ltr,
        child: Align(
          alignment: Alignment.topLeft,
          child: SizedBox(width: pic.size.width / 2, child: Align(alignment: Alignment.topLeft, child: MathPictureBox(pic, scaleDown: true))),
        ),
      ),
    );
    final box = t.renderObject<RenderBox>(find.byType(MathPictureBox));
    expect(box.size.width, closeTo(pic.size.width / 2, .01));
    expect(box.getDryBaseline(BoxConstraints(maxWidth: pic.size.width / 2), TextBaseline.alphabetic), closeTo(pic.baseline / 2, .01));
  });
}

// High: cheap maths for long notes / exam pages.
//
// flutter_math builds a deep widget + render tree for every formula (a paragraph per glyph run, rows, fraction bars …)
// and the notes list rebuilds and re-lays it out every time a card scrolls back into view. Here each formula is laid
// out ONCE, off screen, with the very same flutter_math code, and its painting is kept as a ui.Picture (a recorded
// display list: vector, crisp at any zoom, a few KB). On screen a formula is then a single leaf render box that draws
// that picture, memoised by (TeX, style, size, colour, text scale) in an LRU, so the output is identical to the live
// renderer. Anything that cannot be pictured (TeX errors, unusual layers) falls back to the live Math widget.
import 'dart:ui' as ui;

import 'package:flutter/rendering.dart';
import 'package:flutter/widgets.dart';
import 'package:flutter_math_fork/flutter_math.dart';

/// one formula, laid out and painted once
class MathPicture {
  MathPicture(this.picture, this.size, this.baseline);
  final ui.Picture picture;
  final Size size;

  /// distance from the top to the alphabetic baseline (for inline maths in a text line)
  final double baseline;
}

@immutable
class _Key {
  const _Key(this.tex, this.display, this.fontSize, this.color, this.scale, this.bold);
  final String tex;
  final bool display, bold;
  final double fontSize, scale;
  final Color color;
  @override
  bool operator ==(Object o) => o is _Key && o.tex == tex && o.display == display && o.fontSize == fontSize && o.color == color && o.scale == scale && o.bold == bold;
  @override
  int get hashCode => Object.hash(tex, display, fontSize, color, scale, bold);
}

abstract final class MathPictures {
  /// switch off to draw every formula live (debugging / comparison tests)
  static bool enabled = true;

  /// formulas kept (a picture is a few KB; pictures still on screen stay alive through their render boxes)
  static int maxEntries = 700;

  static final _lru = <_Key, MathPicture?>{}; // insertion order = LRU; null = cannot be pictured, draw live
  static _Offscreen? _off;

  static int get length => _lru.length;

  /// formulas currently drawn from a picture (the rest fall back to the live widget)
  static int get pictured => _lru.values.where((v) => v != null).length;

  /// why the last formula could not be pictured (diagnostics / tests)
  static Object? lastError;
  static void clear() => _lru.clear();

  /// the cached picture of a formula, rendering it now if needed; null = use the live Math widget
  static MathPicture? of(String tex, {required bool display, required double fontSize, required Color color, double scale = 1, bool bold = false}) {
    if (!enabled) return null;
    final k = _Key(tex, display, fontSize, color, scale, bold);
    if (_lru.containsKey(k)) {
      final v = _lru.remove(k);
      _lru[k] = v;
      return v;
    }
    MathPicture? v;
    try {
      v = (_off ??= _Offscreen()).render(tex, display: display, fontSize: fontSize, color: color, scale: scale, bold: bold);
    } catch (e) {
      lastError = e;
      _off = null; // start from a fresh offscreen tree next time
      v = null;
    }
    _lru[k] = v;
    while (_lru.length > maxEntries) {
      _lru.remove(_lru.keys.first);
    }
    return v;
  }
}

/// the root of the offscreen render tree: lays its child out unconstrained, is its own repaint boundary
class _OffRoot extends RenderObject with RenderObjectWithChildMixin<RenderBox> {
  void prepare() {
    scheduleInitialLayout();
    scheduleInitialPaint(OffsetLayer()..attach(this));
  }

  OffsetLayer get rootLayer => layer! as OffsetLayer;

  @override
  bool get isRepaintBoundary => true;

  /// the child's alphabetic baseline (may only be asked by the parent during layout)
  double? baseline;

  @override
  void performLayout() {
    final c = child;
    if (c == null) return;
    c.layout(const BoxConstraints(), parentUsesSize: true);
    baseline = c.getDistanceToBaseline(TextBaseline.alphabetic);
  }

  @override
  void performResize() {}

  @override
  bool get sizedByParent => false;

  @override
  void debugAssertDoesMeetConstraints() {}

  @override
  Rect get paintBounds => Offset.zero & (child?.size ?? Size.zero);

  @override
  Rect get semanticBounds => paintBounds;

  @override
  void paint(PaintingContext context, Offset offset) {
    final c = child;
    if (c != null) context.paintChild(c, offset);
  }
}

class _Offscreen {
  _Offscreen() {
    _pipeline.rootNode = _root;
    _root.prepare();
  }
  final _pipeline = PipelineOwner();
  final _root = _OffRoot();
  final _build = BuildOwner(focusManager: FocusManager());
  RenderObjectToWidgetElement<RenderBox>? _element;

  MathPicture? render(String tex, {required bool display, required double fontSize, required Color color, required double scale, required bool bold}) {
    final m = Math.tex(
      tex,
      mathStyle: display ? MathStyle.display : MathStyle.text,
      textStyle: TextStyle(fontSize: fontSize, color: color, fontWeight: bold ? FontWeight.bold : FontWeight.normal),
      textScaleFactor: scale,
      onErrorFallback: (e) => throw e,
    );
    if (m.parseError != null) return null;
    final w = MediaQuery(
      data: MediaQueryData(textScaler: TextScaler.linear(scale), boldText: bold),
      child: Directionality(textDirection: TextDirection.ltr, child: m),
    );
    _element = RenderObjectToWidgetAdapter<RenderBox>(container: _root, child: w).attachToRenderTree(_build, _element);
    _build.buildScope(_element!);
    _build.finalizeTree();
    _pipeline.flushLayout();
    _pipeline.flushCompositingBits();
    _pipeline.flushPaint();
    final box = _root.child;
    if (box == null || !box.hasSize) return null;
    final size = box.size;
    final baseline = _root.baseline ?? size.height;
    // copy the recorded pictures into one (the layers' own pictures are released on the next render)
    final rec = ui.PictureRecorder();
    final canvas = Canvas(rec);
    for (Layer? l = _root.rootLayer.firstChild; l != null; l = l.nextSibling) {
      if (l is! PictureLayer) {
        rec.endRecording().dispose();
        return null; // clip / transform layers: keep it simple, draw this one live
      }
      final p = l.picture;
      if (p != null) canvas.drawPicture(p);
    }
    return MathPicture(rec.endRecording(), size, baseline);
  }
}

/// draws a [MathPicture]; with [scaleDown] a formula wider than the line is shrunk to fit (like FittedBox.scaleDown)
class MathPictureBox extends LeafRenderObjectWidget {
  const MathPictureBox(this.pic, {super.key, this.scaleDown = false});
  final MathPicture pic;
  final bool scaleDown;
  @override
  RenderObject createRenderObject(BuildContext context) => _RenderMathPicture(pic, scaleDown);
  @override
  void updateRenderObject(BuildContext context, covariant RenderObject r) => (r as _RenderMathPicture)
    ..pic = pic
    ..scaleDown = scaleDown;
}

class _RenderMathPicture extends RenderBox {
  _RenderMathPicture(this._pic, this._scaleDown);
  MathPicture _pic;
  bool _scaleDown;
  double _s = 1;

  set pic(MathPicture v) {
    if (identical(v, _pic)) return;
    final relayout = v.size != _pic.size || v.baseline != _pic.baseline;
    _pic = v;
    relayout ? markNeedsLayout() : markNeedsPaint();
  }

  set scaleDown(bool v) {
    if (v == _scaleDown) return;
    _scaleDown = v;
    markNeedsLayout();
  }

  double _scaleFor(BoxConstraints c) => _scaleDown && c.hasBoundedWidth && c.maxWidth < _pic.size.width && _pic.size.width > 0 ? c.maxWidth / _pic.size.width : 1;

  @override
  double computeMinIntrinsicWidth(double height) => _scaleDown ? 0 : _pic.size.width;
  @override
  double computeMaxIntrinsicWidth(double height) => _pic.size.width;
  @override
  double computeMinIntrinsicHeight(double width) => _pic.size.height;
  @override
  double computeMaxIntrinsicHeight(double width) => _pic.size.height;

  @override
  Size computeDryLayout(BoxConstraints constraints) => constraints.constrain(_pic.size * _scaleFor(constraints));

  @override
  double? computeDryBaseline(BoxConstraints constraints, TextBaseline baseline) => _pic.baseline * _scaleFor(constraints);

  @override
  void performLayout() {
    _s = _scaleFor(constraints);
    size = constraints.constrain(_pic.size * _s);
  }

  @override
  double? computeDistanceToActualBaseline(TextBaseline baseline) => _pic.baseline * _s;

  @override
  bool get isRepaintBoundary => false;

  @override
  void paint(PaintingContext context, Offset offset) {
    final c = context.canvas;
    c.save();
    c.translate(offset.dx, offset.dy);
    if (_s != 1) c.scale(_s);
    c.drawPicture(_pic.picture);
    c.restore();
  }
}

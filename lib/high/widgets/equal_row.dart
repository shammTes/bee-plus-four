// A row whose children all get the height of the tallest one, without IntrinsicHeight.
//
// `IntrinsicHeight(child: Row(crossAxisAlignment: stretch, …))` asks every descendant for its intrinsic height first
// (a separate, uncached measuring walk through text, nested rows, … that can grow exponentially when intrinsics are
// nested) and then lays the row out. EqualHeightRow lays each child out normally (loose height), takes the tallest,
// and lays out again with that tight height only the children that came out shorter. Results are cached by the
// normal layout cache, so an unchanged row costs nothing on the next frame.
import 'dart:math' as math;

import 'package:flutter/rendering.dart';
import 'package:flutter/widgets.dart';

/// Row of children stretched to the tallest one. Children are sized like in a [Row]: [Expanded] / [Flexible] share
/// the width left over after the others (which are laid out with loose width, e.g. a [SizedBox] with a width).
/// The row is as wide as the incoming max width when it has flexible children (it needs bounded width).
class EqualHeightRow extends MultiChildRenderObjectWidget {
  const EqualHeightRow({super.key, this.spacing = 0, super.children});
  final double spacing;
  @override
  RenderObject createRenderObject(BuildContext context) => RenderEqualHeightRow(spacing);
  @override
  void updateRenderObject(BuildContext context, covariant RenderEqualHeightRow r) => r.spacing = spacing;
}

class RenderEqualHeightRow extends RenderBox
    with ContainerRenderObjectMixin<RenderBox, FlexParentData>, RenderBoxContainerDefaultsMixin<RenderBox, FlexParentData> {
  RenderEqualHeightRow(this._spacing);
  double _spacing;
  set spacing(double v) {
    if (v == _spacing) return;
    _spacing = v;
    markNeedsLayout();
  }

  @override
  void setupParentData(RenderBox child) {
    if (child.parentData is! FlexParentData) child.parentData = FlexParentData();
  }

  int _flexOf(RenderBox c) => (c.parentData! as FlexParentData).flex ?? 0;

  /// widths of the children for [c] (laying out / dry-laying out the non-flexible ones with [size])
  List<double> _widths(BoxConstraints c, Size Function(RenderBox, BoxConstraints) size) {
    final kids = getChildrenAsList();
    final widths = List<double>.filled(kids.length, 0);
    final gaps = _spacing * math.max(0, kids.length - 1);
    var used = gaps, flexTotal = 0;
    for (final (i, k) in kids.indexed) {
      final f = _flexOf(k);
      if (f > 0) {
        flexTotal += f;
        continue;
      }
      final maxW = c.hasBoundedWidth ? math.max(0.0, c.maxWidth - used) : double.infinity;
      widths[i] = size(k, BoxConstraints(maxWidth: maxW, maxHeight: c.maxHeight)).width;
      used += widths[i];
    }
    if (flexTotal > 0) {
      assert(c.hasBoundedWidth, 'EqualHeightRow with Expanded children needs a bounded width');
      final free = math.max(0.0, c.maxWidth - used);
      for (final (i, k) in kids.indexed) {
        final f = _flexOf(k);
        if (f > 0) widths[i] = free * f / flexTotal;
      }
    }
    return widths;
  }

  BoxConstraints _flexConstraints(RenderBox k, double w, double maxH) {
    final tight = (k.parentData! as FlexParentData).fit != FlexFit.loose;
    return BoxConstraints(minWidth: tight ? w : 0, maxWidth: w, maxHeight: maxH);
  }

  @override
  void performLayout() {
    final c = constraints, kids = getChildrenAsList();
    final widths = _widths(c, (k, bc) {
      k.layout(bc, parentUsesSize: true);
      return k.size;
    });
    var h = c.minHeight;
    for (final (i, k) in kids.indexed) {
      if (_flexOf(k) > 0) k.layout(_flexConstraints(k, widths[i], c.maxHeight), parentUsesSize: true);
      h = math.max(h, k.size.height);
    }
    h = math.min(h, c.maxHeight);
    var x = 0.0;
    for (final k in kids) {
      if (k.size.height != h) k.layout(BoxConstraints.tightFor(width: k.size.width, height: h), parentUsesSize: true);
      (k.parentData! as FlexParentData).offset = Offset(x, 0);
      x += k.size.width + _spacing;
    }
    final w = kids.isEmpty ? 0.0 : x - _spacing;
    final flex = kids.any((k) => _flexOf(k) > 0);
    size = c.constrain(Size(flex ? c.maxWidth : w, h));
  }

  @override
  Size computeDryLayout(covariant BoxConstraints c) {
    final kids = getChildrenAsList();
    final widths = _widths(c, (k, bc) => k.getDryLayout(bc));
    var h = c.minHeight;
    for (final (i, k) in kids.indexed) {
      final s = _flexOf(k) > 0 ? k.getDryLayout(_flexConstraints(k, widths[i], c.maxHeight)) : k.getDryLayout(BoxConstraints(maxWidth: widths[i], maxHeight: c.maxHeight));
      h = math.max(h, s.height);
    }
    final w = widths.fold(0.0, (a, b) => a + b) + _spacing * math.max(0, kids.length - 1);
    return c.constrain(Size(kids.any((k) => _flexOf(k) > 0) ? c.maxWidth : w, math.min(h, c.maxHeight)));
  }

  double _sumW(double Function(RenderBox) f) {
    final kids = getChildrenAsList();
    return kids.fold(0.0, (a, k) => a + f(k)) + _spacing * math.max(0, kids.length - 1);
  }

  @override
  double computeMinIntrinsicWidth(double height) => _sumW((k) => k.getMinIntrinsicWidth(height));
  @override
  double computeMaxIntrinsicWidth(double height) => _sumW((k) => k.getMaxIntrinsicWidth(height));
  @override
  double computeMinIntrinsicHeight(double width) => getChildrenAsList().fold(0.0, (a, k) => math.max(a, k.getMinIntrinsicHeight(width)));
  @override
  double computeMaxIntrinsicHeight(double width) => getChildrenAsList().fold(0.0, (a, k) => math.max(a, k.getMaxIntrinsicHeight(width)));

  @override
  double? computeDistanceToActualBaseline(TextBaseline baseline) => defaultComputeDistanceToFirstActualBaseline(baseline);
  @override
  bool hitTestChildren(BoxHitTestResult result, {required Offset position}) => defaultHitTestChildren(result, position: position);
  @override
  void paint(PaintingContext context, Offset offset) => defaultPaint(context, offset);
}

// Notes table renderer (`table` cards): a generic grid plus opt-in accounting layouts (journal, ledger, statement, T-account).
//
// One custom render object lays every cell out at a fixed column width, gives each row the height of its tallest cell, and
// paints the stripes / rules itself (no IntrinsicHeight, no per-row Table, no shadows). When the columns need more room than
// the card has, the grid scrolls sideways inside a Scrollable while the first column(s) stay frozen. Column widths are
// measured once per card and cached.
import 'dart:math' as math;
import 'dart:typed_data';

import 'package:flutter/rendering.dart';
import 'package:flutter/widgets.dart';

import '../data/notes_models.dart';
import '../theme/tokens.dart';
import '../widgets/clay_widgets.dart';
import '../widgets/tx.dart';
import 'rich.dart';
import 'ui.dart' show richColors;

/// column types (`cols` in the JSON)
enum ColT { text, num, money, dr, cr, date, ref }

extension on ColT {
  bool get figure => this == ColT.num || this == ColT.money || this == ColT.dr || this == ColT.cr;
  bool get amount => this == ColT.money || this == ColT.dr || this == ColT.cr;
}

const _accountingKinds = {'journal', 'ledger', 'statement', 't_account'};

final _numRe = RegExp(r'^\s*[(\-−+±]?\s*[\d][\d,  ]*(\.\d+)?\s*\)?\s*%?\s*$');
final _moneyRe = RegExp(r'^\s*(\(|-|−)?\s*(\d[\d,]*)(\.\d+)?\s*\)?\s*$');

String _plain(String s) => s.replaceAll('**', '').replaceAll(RegExp(r'\$([^$]*)\$'), r'$1');
bool isFigure(String s) => _numRe.hasMatch(_plain(s));

/// 1234567.5 -> 1,234,567.5; -6167 / (6,167) -> (6,167); anything that is not a plain amount is returned unchanged
String fmtMoney(String s) {
  final bold = s.contains('**');
  final m = _moneyRe.firstMatch(_plain(s));
  if (m == null) return s;
  final d = m[2]!.replaceAll(',', '');
  final b = StringBuffer();
  for (var i = 0; i < d.length; i++) {
    if (i > 0 && (d.length - i) % 3 == 0) b.write(',');
    b.write(d[i]);
  }
  var out = '$b${m[3] ?? ''}';
  if (m[1] != null) out = '($out)';
  return bold ? '**$out**' : out;
}

ColT _guess(String head, List<List<String>> rows, int j, bool acc) {
  final h = _plain(head).toLowerCase().trim();
  if (acc) {
    if (RegExp(r'^date\b|\bdate$|^date —|— date').hasMatch(h) && !h.contains('balance')) return ColT.date;
    if (RegExp(
      r'^(p\s*/\s*r\.?|p\s*o\s*s\s*t\.? ref\.?|post\.? ?ref\.?|ref\.?|l\.?\s*f\.?|f\.|folio|pr|no\.?|cheq no\.?|invoice no\.?)$',
    ).hasMatch(h)) {
      return ColT.ref;
    }
    if (RegExp(r'\bdebit\b|\bdr\.?$|\(dr\.?\)').hasMatch(h) && !h.contains('credit')) return ColT.dr;
    if (RegExp(r'\bcredit\b|\bcr\.?$|\(cr\.?\)').hasMatch(h) && !h.contains('debit')) return ColT.cr;
  }
  var n = 0, f = 0;
  for (final r in rows) {
    if (j >= r.length) continue;
    final c = r[j].trim();
    if (c.isEmpty || c == '?' || c == '—' || c == '-') continue;
    n++;
    if (isFigure(c)) f++;
  }
  if (n > 0 && f >= n * .6) return acc ? ColT.money : ColT.num;
  if (acc && RegExp(r'\b(nakfa|nfa|birr|amount|balance|total)\b').hasMatch(h) && f > 0) return ColT.money;
  return ColT.text;
}

/// resolved presentation of one table card
class TableModel {
  TableModel(
    this.head,
    this.rows, {
    this.kind = 'table',
    List<String> cols = const [],
    List<String> marks = const [],
    this.frozen,
    this.layout,
    this.to,
  }) : n = [head.length, for (final r in rows) r.length].fold(0, math.max) {
    acc = _accountingKinds.contains(kind) || cols.any((c) => c == 'money' || c == 'dr' || c == 'cr');
    types = [
      for (var j = 0; j < n; j++)
        j < cols.length && ColT.values.any((t) => t.name == cols[j])
            ? ColT.values.byName(cols[j])
            : _guess(j < head.length ? head[j] : '', rows, j, acc),
    ];
    if (cols.isEmpty && types.isNotEmpty && types[0].figure && kind != 't_account' && n > 1 && types.skip(1).any((t) => !t.figure)) {
      // a first column of years / numbers still reads as a label
      types[0] = ColT.text;
    }
    this.marks = [for (var i = 0; i < rows.length; i++) (i < marks.length ? marks[i] : '').split(RegExp(r'\s+')).where((x) => x.isNotEmpty).toSet()];
    if (acc && marks.isEmpty) _autoMarks();
  }
  factory TableModel.of(TableCard c) =>
      TableModel(c.head, c.rows, kind: c.kind, cols: c.cols, marks: c.marks, frozen: c.frozen, layout: c.layout, to: c.to);

  final List<String> head;
  final List<List<String>> rows;
  final String kind;
  final int? frozen;
  final String? layout, to;
  final int n;
  late final bool acc;
  late final List<ColT> types;
  late final List<Set<String>> marks;

  String cell(int i, int j) => j < rows[i].length ? rows[i][j] : '';
  bool get hasHead => head.any((h) => h.trim().isNotEmpty);
  int? get textCol => [for (var j = 0; j < n; j++) j].where((j) => types[j] == ColT.text).firstOrNull;

  void _autoMarks() {
    final tc = textCol;
    for (var i = 0; i < rows.length; i++) {
      final label = tc == null ? '' : _plain(cell(i, tc)).trim().toLowerCase();
      final figs = [
        for (var j = 0; j < n; j++)
          if (types[j].figure && cell(i, j).trim().isNotEmpty) j,
      ];
      if (RegExp(r'^(totals?\b|net (income|loss|profit|sales|purchases)\b|gross (profit|margin)\b|cost of goods sold\b|total )').hasMatch(label) &&
          figs.isNotEmpty) {
        marks[i].add(i == rows.length - 1 ? 'final' : 'total');
      } else if (figs.isEmpty && label.isNotEmpty && label.startsWith('(') && label.endsWith(')')) {
        marks[i].add('note');
      } else if (figs.isEmpty &&
          label.isNotEmpty &&
          kind == 'statement' &&
          (label.endsWith(':') || [for (var j = 0; j < n; j++) cell(i, j)].where((x) => x.trim().isNotEmpty).length == 1)) {
        marks[i].add('head');
      }
    }
  }
}

final _models = Expando<TableModel>('tableModel');

/// the cached model of a card (its JSON never changes while the app runs)
TableModel tableModelOf(TableCard c) => _models[c] ??= TableModel.of(c);

// ------------------------------------------------------------------ measuring

final _wordW = <String, double>{};
double _measure(String s, TextStyle st, TextScaler sc) {
  final k = '${st.fontSize}|${st.fontWeight?.value}|${sc.scale(10)}|$s';
  final hit = _wordW[k];
  if (hit != null) return hit;
  final tp = TextPainter(
    text: TextSpan(text: s, style: st),
    textDirection: TextDirection.ltr,
    textScaler: sc,
  )..layout();
  final w = tp.width;
  tp.dispose();
  if (_wordW.length > 20000) _wordW.clear();
  return _wordW[k] = w;
}

final _wordBreak = RegExp(r'\s+|(?<=[A-Za-z][-–—])(?=[A-Za-z])');

/// (one-line width, widest word) of [s]; maths gets 15 % slack because KaTeX boxes are wider than their source letters
(double, double) _extent(String s, TextStyle st, TextStyle bold, TextScaler sc) {
  final p = _plain(s).trim();
  if (p.isEmpty) return (0, 0);
  final slack = s.contains(r'$') ? 1.15 : 1.0;
  final marked = s.contains('**') || s.contains('[[');
  final isBold = marked || st.fontWeight == FontWeight.w900;
  double line = 0, word = 0;
  for (final l in p.split('\n')) {
    line = math.max(line, _measure(l, isBold ? bold : st, sc) + (marked ? 4.0 * ' '.allMatches(l).length + 6 : 1));
    // the line breaker may also break after a hyphen / dash ("Depreciation-Furniture"), so those parts are words too
    // (not in cells with **key words**: each of those is one unbreakable box)
    for (final w in l.split(marked ? RegExp(r'\s+') : _wordBreak)) {
      if (w.isEmpty) continue;
      // words are measured in the heaviest weight a cell may use, so **bold** words never break mid-word; a **key word**
      // is drawn as its own box with 2 px side padding (+ rounding), hence the +6
      word = math.max(word, _measure(w, bold, sc) + (marked ? 6 : 1));
    }
  }
  return (line * slack, word * slack);
}

// ------------------------------------------------------------------ the grid render object

/// what the grid paints besides its cells
class GridSpec {
  GridSpec({
    required this.widths,
    required this.cols,
    required this.frozen,
    required this.rowBg,
    required this.flags,
    required this.base,
    required this.rule,
    required this.edge,
    this.headRows = 0,
    this.vRules = const [],
    this.radius = 14,
    this.frame = true,
  });
  final List<double> widths;
  final int cols, frozen, headRows;
  final List<Color?> rowBg;

  /// per cell: 1 = single rule above, 2 = double rule below, 4 = rule below (header)
  final Uint8List flags;
  final Color base, rule, edge;
  final List<int> vRules;
  final double radius;
  final bool frame;
}

class _GridParentData extends ContainerBoxParentData<RenderBox> {
  int col = 0;
}

class GridView2 extends MultiChildRenderObjectWidget {
  const GridView2({super.key, required this.spec, required this.offset, required super.children});
  final GridSpec spec;
  final ViewportOffset offset;
  @override
  RenderObject createRenderObject(BuildContext context) => RenderNoteGrid(spec, offset);
  @override
  void updateRenderObject(BuildContext context, RenderNoteGrid r) => r
    ..spec = spec
    ..offset = offset;
}

class RenderNoteGrid extends RenderBox
    with ContainerRenderObjectMixin<RenderBox, _GridParentData>, RenderBoxContainerDefaultsMixin<RenderBox, _GridParentData> {
  RenderNoteGrid(this._spec, this._offset);
  GridSpec _spec;
  ViewportOffset _offset;
  GridSpec get spec => _spec;
  set spec(GridSpec v) {
    if (identical(v, _spec)) return;
    _spec = v;
    markNeedsLayout();
  }

  set offset(ViewportOffset v) {
    if (v == _offset) return;
    if (attached) _offset.removeListener(markNeedsPaint);
    _offset = v;
    if (attached) _offset.addListener(markNeedsPaint);
    markNeedsLayout();
  }

  /// row tops (rows + 1 entries), column lefts (cols + 1), total content width, frozen width
  List<double> _y = const [0], _x = const [0];
  double _total = 0, _frozenW = 0;
  final _kids = <RenderBox>[];

  double get scroll => _total > size.width + .5 ? _offset.pixels.clamp(0.0, _total - size.width) : 0.0;
  double get maxScroll => math.max(0, _total - size.width);

  @override
  void attach(PipelineOwner owner) {
    super.attach(owner);
    _offset.addListener(markNeedsPaint);
  }

  @override
  void detach() {
    _offset.removeListener(markNeedsPaint);
    super.detach();
  }

  @override
  void setupParentData(RenderBox child) {
    if (child.parentData is! _GridParentData) child.parentData = _GridParentData();
  }

  @override
  double computeMinIntrinsicWidth(double height) => _spec.widths.take(_spec.frozen).fold(0.0, (a, b) => a + b);
  @override
  double computeMaxIntrinsicWidth(double height) => _spec.widths.fold(0.0, (a, b) => a + b);
  @override
  double computeMinIntrinsicHeight(double width) => computeMaxIntrinsicHeight(width);
  @override
  double computeMaxIntrinsicHeight(double width) {
    var h = 0.0, row = 0.0, i = 0;
    var c = firstChild;
    while (c != null) {
      row = math.max(row, c.getMaxIntrinsicHeight(_spec.widths[i % _spec.cols]));
      i++;
      if (i % _spec.cols == 0) {
        h += row;
        row = 0;
      }
      c = childAfter(c);
    }
    return h + row;
  }

  @override
  Size computeDryLayout(BoxConstraints constraints) {
    final total = _spec.widths.fold(0.0, (a, b) => a + b);
    return constraints.constrain(Size(math.min(total, constraints.maxWidth), computeMaxIntrinsicHeight(total)));
  }

  @override
  void performLayout() {
    final s = _spec, n = s.cols;
    _x = [0];
    for (final w in s.widths) {
      _x.add(_x.last + w);
    }
    _total = _x.last;
    _frozenW = _x[math.min(s.frozen, n)];
    _kids.clear();
    var c = firstChild;
    while (c != null) {
      _kids.add(c);
      c = childAfter(c);
    }
    final m = (_kids.length / n).ceil();
    _y = [0];
    for (var r = 0; r < m; r++) {
      var h = 0.0;
      for (var j = 0; j < n && r * n + j < _kids.length; j++) {
        final k = _kids[r * n + j];
        k.layout(BoxConstraints.tightFor(width: s.widths[j]), parentUsesSize: true);
        final pd = k.parentData! as _GridParentData
          ..offset = Offset(_x[j], _y.last)
          ..col = j;
        assert(pd.col == j);
        h = math.max(h, k.size.height);
      }
      _y.add(_y.last + h);
    }
    size = constraints.constrain(Size(math.min(_total, constraints.maxWidth), _y.last));
    _offset.applyViewportDimension(size.width);
    _offset.applyContentDimensions(0, maxScroll);
  }

  Offset _shift(_GridParentData pd) => pd.col < _spec.frozen ? pd.offset : pd.offset - Offset(scroll, 0);

  @override
  void applyPaintTransform(RenderBox child, Matrix4 transform) {
    final o = _shift(child.parentData! as _GridParentData);
    transform.translateByDouble(o.dx, o.dy, 0, 1);
  }

  @override
  bool hitTestChildren(BoxHitTestResult result, {required Offset position}) {
    for (final k in _kids.reversed) {
      final pd = k.parentData! as _GridParentData;
      if (pd.col >= _spec.frozen && position.dx < _frozenW) continue;
      final hit = result.addWithPaintOffset(
        offset: _shift(pd),
        position: position,
        hitTest: (r, p) => k.hitTest(r, position: p),
      );
      if (hit) return true;
    }
    return false;
  }

  final _clipOuter = LayerHandle<ClipRRectLayer>();
  final _clipScroll = LayerHandle<ClipRectLayer>();

  @override
  void dispose() {
    _clipOuter.layer = null;
    _clipScroll.layer = null;
    super.dispose();
  }

  // NB: a child may be its own layer (a KaTeX repaint boundary), after which `context.canvas` is a new canvas, so the
  // canvas is fetched afresh for every drawing call and clipping goes through push… (never canvas.save / clip).
  @override
  void paint(PaintingContext context, Offset offset) {
    final s = _spec;
    final outer = RRect.fromRectAndRadius(Offset.zero & size, Radius.circular(s.radius));
    _clipOuter.layer = context.pushClipRRect(needsCompositing, offset, Offset.zero & size, outer, _paintInner, oldLayer: _clipOuter.layer);
    if (s.frame) {
      context.canvas.drawRRect(
        outer.shift(offset).deflate(.5),
        Paint()
          ..style = PaintingStyle.stroke
          ..strokeWidth = 1
          ..color = withA(s.edge, .16),
      );
    }
  }

  void _paintInner(PaintingContext context, Offset offset) {
    final s = _spec, w = size.width, h = size.height, sx = scroll;
    final fill = Paint();
    // row backgrounds (opaque colours, so frozen cells hide what scrolls under them)
    for (var r = 0; r + 1 < _y.length; r++) {
      final c = r < s.rowBg.length ? s.rowBg[r] : null;
      if (c == null) continue;
      context.canvas.drawRect(Rect.fromLTRB(offset.dx, offset.dy + _y[r], offset.dx + w, offset.dy + _y[r + 1]), fill..color = c);
    }
    // scrolling part
    _clipScroll.layer = context.pushClipRect(needsCompositing, offset, Rect.fromLTRB(_frozenW, 0, w, h), (ctx, o) {
      _paintRules(ctx, o, false, sx);
      for (final k in _kids) {
        final pd = k.parentData! as _GridParentData;
        if (pd.col < s.frozen) continue;
        final x = pd.offset.dx - sx;
        if (x > w || x + k.size.width < _frozenW) continue;
        ctx.paintChild(k, o + Offset(x, pd.offset.dy));
      }
    }, oldLayer: _clipScroll.layer);
    // frozen column(s) on top
    if (s.frozen > 0 && sx > 0) {
      for (var r = 0; r + 1 < _y.length; r++) {
        final c = (r < s.rowBg.length ? s.rowBg[r] : null) ?? s.base;
        context.canvas.drawRect(Rect.fromLTRB(offset.dx, offset.dy + _y[r], offset.dx + _frozenW, offset.dy + _y[r + 1]), fill..color = c);
      }
    }
    _paintRules(context, offset, true, sx);
    for (final k in _kids) {
      final pd = k.parentData! as _GridParentData;
      if (pd.col >= s.frozen) continue;
      context.paintChild(k, offset + pd.offset);
    }
    // vertical rules (T-account centre line)
    final line = Paint()
      ..color = s.rule
      ..strokeWidth = 1.5;
    for (final j in s.vRules) {
      final x = offset.dx + _x[j + 1] - (j + 1 > s.frozen ? sx : 0);
      final top = offset.dy + (s.headRows < _y.length ? _y[s.headRows] : 0);
      context.canvas.drawLine(Offset(x, top), Offset(x, offset.dy + h), line);
    }
    if (_total > w + .5) {
      // the frozen edge: a hairline plus a 6 px soft fade once something has slid under it
      if (s.frozen > 0 && sx > .5) {
        final ex = offset.dx + _frozenW, r = Rect.fromLTWH(ex, offset.dy, 6, h);
        context.canvas.drawRect(r, Paint()..shader = LinearGradient(colors: [withA(s.edge, .22), withA(s.edge, 0)]).createShader(r));
        context.canvas.drawLine(
          Offset(ex, offset.dy),
          Offset(ex, offset.dy + h),
          Paint()
            ..color = withA(s.edge, .35)
            ..strokeWidth = 1,
        );
      }
      // more to the right: fade the last 22 px
      if (sx < maxScroll - .5) {
        final r = Rect.fromLTWH(offset.dx + w - 22, offset.dy, 22, h);
        context.canvas.drawRect(r, Paint()..shader = LinearGradient(colors: [withA(s.base, 0), withA(s.base, .92)]).createShader(r));
      }
    }
  }

  void _paintRules(PaintingContext context, Offset offset, bool frozen, double sx) {
    final s = _spec, n = s.cols;
    final p = Paint()
      ..color = s.rule
      ..strokeWidth = 1.2;
    final m = _y.length - 1;
    for (var r = 0; r < m; r++) {
      for (var j = 0; j < n; j++) {
        if ((j < s.frozen) != frozen) continue;
        final i = r * n + j;
        if (i >= s.flags.length) continue;
        final f = s.flags[i];
        if (f == 0) continue;
        final dx = frozen ? 0.0 : -sx;
        final x0 = offset.dx + _x[j] + dx + (f & 4 != 0 ? 0 : 6), x1 = offset.dx + _x[j + 1] + dx - (f & 4 != 0 ? 0 : 6);
        final y0 = offset.dy + _y[r], y1 = offset.dy + _y[r + 1];
        if (f & 1 != 0) context.canvas.drawLine(Offset(x0, y0 + 1), Offset(x1, y0 + 1), p);
        if (f & 2 != 0) {
          context.canvas.drawLine(Offset(x0, y1 - 4), Offset(x1, y1 - 4), p);
          context.canvas.drawLine(Offset(x0, y1 - 1.5), Offset(x1, y1 - 1.5), p);
        }
        if (f & 4 != 0) context.canvas.drawLine(Offset(x0, y1 - .75), Offset(x1, y1 - .75), p..strokeWidth = 1.5);
        p.strokeWidth = 1.2;
      }
    }
  }
}

/// the grid inside a sideways Scrollable when it is wider than the card
class _ScrollGrid extends StatelessWidget {
  const _ScrollGrid({required this.spec, required this.children, required this.scroll});
  final GridSpec spec;
  final List<Widget> children;
  final bool scroll;
  @override
  Widget build(BuildContext context) {
    if (!scroll) return GridView2(spec: spec, offset: ViewportOffset.zero(), children: children);
    return RepaintBoundary(
      child: Scrollable(
        axisDirection: AxisDirection.right,
        physics: const ClampingScrollPhysics(),
        viewportBuilder: (context, offset) => GridView2(spec: spec, offset: offset, children: children),
      ),
    );
  }
}

// ------------------------------------------------------------------ widths

final _slashWord = RegExp(r'\b(\w{1,3})/(\w{1,3})\b');

/// keeps short slash words whole ("Balance c/d" wraps before "c/d", never as "c/ | d")
String noBreakSlash(String s) => s.contains('/') ? s.replaceAllMapped(_slashWord, (m) => '${m[1]}\u2060/\u2060${m[2]}') : s;

/// fits columns into [avail]: each column has a hard minimum (widest word / whole figure), a comfortable minimum (text
/// columns are not squeezed below ~7 em, so rows don't turn into towers) and a preferred width (its longest line, capped).
List<double> fitWidths(List<double> minW, List<double> comfy, List<double> pref, double avail) {
  double sum(List<double> l) => l.fold(0.0, (a, b) => a + b);
  final n = minW.length;
  if (n == 0) return const [];
  final sp = sum(pref), sc = sum(comfy), sm = sum(minW);
  if (sp <= avail) {
    // everything fits on one line: share the spare room by preferred width
    return [for (final p in pref) p + (avail - sp) * p / sp];
  }
  List<double> lerp(List<double> a, List<double> b, double sa, double sb) {
    final t = (avail - sa) / (sb - sa == 0 ? 1 : sb - sa);
    return [for (var j = 0; j < n; j++) a[j] + (b[j] - a[j]) * t];
  }

  if (sc <= avail) return lerp(comfy, pref, sc, sp);
  if (sm <= avail && sc > avail * 1.25) return comfy; // far too wide: scroll at comfortable widths
  if (sm <= avail) return lerp(minW, comfy, sm, sc);
  return comfy;
}

// ------------------------------------------------------------------ the widget

/// `.ntable`: every `table` card
class NTable extends StatelessWidget {
  NTable({super.key, required List<String> head, required List<List<String>> rows, TableModel? model}) : model = model ?? TableModel(head, rows);
  NTable.card(TableCard c, {super.key}) : model = tableModelOf(c);
  final TableModel model;

  @override
  Widget build(BuildContext context) {
    final k = Kit.of(context), p = k.p;
    final sc = MediaQuery.textScalerOf(context);
    return LayoutBuilder(
      builder: (context, box) {
        final m = model;
        if (m.n == 0) return const SizedBox.shrink();
        final w = box.maxWidth;
        if (m.kind == 't_account') return _TAccounts(m, p, sc, w);
        final pc = m.acc ? null : prosConsCols(m);
        if (pc != null && m.layout != 'grid') return _ProsCons(m, p, pc);
        final narrow = w < 520;
        switch (m.layout) {
          case 'stack':
            return _RowCards(m, p);
          case 'cards' when narrow:
            return _RowCards(m, p);
          case 'compare' when narrow:
            return _Compare(m, p);
          case 'terms' when narrow:
            return _Terms(m, p);
          case 'entries':
            return _Entries(m, p);
        }
        return _grid(context, m, p, sc, w);
      },
    );
  }

  static TextStyle _fig(TextStyle s) => s.copyWith(fontFeatures: const [FontFeature.tabularFigures()]);

  Widget _grid(BuildContext context, TableModel m, Palette p, TextScaler sc, double avail) {
    final rc = richColors(p);
    final acc = m.acc;
    // narrow phones: accounting tables get smaller (tabular) figures, short headers and slimmer padding so they fit
    final tight = acc && avail < 420;
    final fs = tight ? 15.0 : (acc ? 16.0 : 17.0);
    final body = ts(fs, FontWeight.w700, p.ink, height: 1.3);
    final first = ts(fs, FontWeight.w800, p.ink, height: 1.3);
    final bold = ts(fs, FontWeight.w900, p.ink, height: 1.3);
    final th = ts(tight ? 13.5 : (acc ? 14.5 : 15), FontWeight.w900, p.ink2, height: 1.25);
    final thB = th;
    final muted = ts(tight ? 13 : 14, FontWeight.w700, p.ink2, height: 1.3);
    final padX = tight ? 4.5 : 7.0;
    final drInk = p.dark ? p.blue.deep : mix(p.blue.deep, .8, p.ink), crInk = p.dark ? p.peach.deep : mix(p.peach.deep, .8, p.ink);
    const padY = 8.0;
    final types = m.types;
    final used = <int, List<String>>{};
    final heads = [
      for (var j = 0; j < m.head.length; j++)
        () {
          if (!tight) return m.head[j];
          final (h, u) = shortHead(m.head[j], j < m.n ? types[j] : ColT.text);
          used[j] = u;
          return h;
        }(),
    ];

    // ---- which logical columns are shown (a date column folds into the next text column when room is short)
    final cols = [for (var j = 0; j < m.n; j++) j];
    final dateInto = <int, int>{}; // shown column -> source date column
    final tc = m.textCol;
    // an accounting table's posting-reference column left blank (the book's P/R before posting): not shown
    if (acc) {
      cols.removeWhere((j) => types[j] == ColT.ref && j < m.head.length && [for (var i = 0; i < m.rows.length; i++) m.cell(i, j).trim()].every((c) => c.isEmpty));
    }

    // ---- measure (cached on the model: the JSON never changes)
    final cache = _meas[m] ??= {};
    final mm = cache[tight] ??= () {
      final minW = List.filled(m.n, 0.0), pref = List.filled(m.n, 0.0);
      for (var j = 0; j < m.n; j++) {
        if (j < heads.length) {
          final (l, w) = _extent(heads[j], thB, thB, sc);
          pref[j] = math.max(pref[j], math.min(l, 140));
          minW[j] = math.max(minW[j], w);
        }
        for (var i = 0; i < m.rows.length; i++) {
          final raw = m.cell(i, j);
          if (raw.trim().isEmpty) continue;
          final txt = types[j].amount ? fmtMoney(raw) : raw;
          final mk = m.marks[i];
          final st = (mk.contains('total') || mk.contains('final') || mk.contains('head') || mk.contains('bold')) ? bold : (j == 0 && types[j] == ColT.text ? first : body);
          final (l, w) = _extent(txt, types[j].figure ? _fig(st) : st, bold, sc);
          final indent = (mk.contains('indent') || mk.contains('note') || (m.kind == 'journal' && j == tc && _isCreditLine(m, i))) ? 18.0 : 0.0;
          pref[j] = math.max(pref[j], l + indent);
          // a figure never wraps, except after a label such as the worksheet's "(b) 16,500.00"
          minW[j] = math.max(minW[j], (types[j].figure && !_plain(txt).trim().contains(' ') ? l : w) + indent);
        }
      }
      return (minW, pref);
    }();
    final rawMin = mm.$1, rawPref = mm.$2;
    // shown column -> the statement money columns folded into it (inner subtotal levels, left to right)
    final foldInto = <int, List<int>>{};
    const step = 12.0;
    double raw(List<double> a, int j) {
      final f = foldInto[j];
      if (f == null) return a[j];
      var best = 0.0;
      for (final (k, src) in f.indexed) {
        best = math.max(best, a[src] + (f.length - 1 - k) * step);
      }
      return best;
    }

    double minOf(int j) => raw(rawMin, j) + 2 * padX;
    double prefOf(int j) {
      final t = types[j];
      final cap = t.figure || t == ColT.ref || t == ColT.date ? 1e9 : (j == 0 ? 190.0 : 230.0);
      return math.max(minOf(j), math.min(raw(rawPref, j), cap) + 2 * padX);
    }

    double comfyOf(int j) {
      final t = types[j];
      if (t != ColT.text) return math.min(prefOf(j), math.max(minOf(j), t == ColT.date ? 64 : 0));
      return math.min(prefOf(j), math.max(minOf(j), tight ? 84 : (j == 0 ? 96 : 112)));
    }

    // fold the date column into the particulars column when the table would not fit
    List<double> sumOf(double Function(int) f, List<int> cs) => [for (final j in cs) f(j)];
    if (acc && tc != null && tc > 0 && types[tc - 1] == ColT.date) {
      final need = sumOf(comfyOf, cols).fold(0.0, (a, b) => a + b);
      if (need > avail) {
        cols.remove(tc - 1);
        dateInto[tc] = tc - 1;
      }
    }

    // a statement's money columns are subtotal levels (one figure per line): when they don't fit, the inner levels share
    // one column, each level stepped in from the right, and the last column keeps the results
    if (m.kind == 'statement') {
      final money = [for (final j in cols) if (types[j] == ColT.money) j];
      final inner = money.length >= 3 ? money.sublist(0, money.length - 1) : const <int>[];
      bool single(int i) => inner.where((j) => m.cell(i, j).trim().isNotEmpty).length <= 1;
      if (inner.isNotEmpty &&
          inner.last - inner.first == inner.length - 1 &&
          sumOf(comfyOf, cols).fold(0.0, (a, b) => a + b) > avail &&
          [for (var i = 0; i < m.rows.length; i++) i].every(single)) {
        cols.removeWhere((j) => inner.contains(j) && j != inner.last);
        foldInto[inner.last] = inner;
      }
    }

    // ---- stacked blocks for wide all-text tables on narrow screens
    final allText = m.n >= 3 && types.every((t) => t == ColT.text) && !acc && m.hasHead;
    final comfySum = sumOf(comfyOf, cols).fold(0.0, (a, b) => a + b);
    if (m.layout == null && allText && avail < 520 && comfySum > avail * 1.3) {
      final h0 = _plain(m.head.isEmpty ? '' : m.head[0]).toLowerCase();
      return RegExp(r'^(features?|basis|bases|aspects?|criteri(a|on)|points?|characteristics?|factors?)\b').hasMatch(h0) ? _Compare(m, p) : _RowCards(m, p);
    }

    var widths = fitWidths(sumOf(minOf, cols), sumOf(comfyOf, cols), sumOf(prefOf, cols), avail);
    final total = widths.fold(0.0, (a, b) => a + b);
    final scroll = total > avail + .5;
    if (scroll && acc && m.layout != 'grid' && avail < 520) {
      final groups = sectionGroups(m);
      final labelCols = [for (final j in cols) if (!types[j].figure) j];
      double need(List<int> cs) => sumOf(minOf, [...labelCols, ...cs]).fold(0.0, (a, b) => a + b);
      if (groups.isNotEmpty && groups.every((g) => need(g.$2) <= avail + .5)) return _Sections(m, groups);
      return _Entries(m, p);
    }
    // frozen: the label column(s) — in a journal / ledger everything up to the particulars column
    var frozen = scroll ? (m.frozen ?? 1) : 0;
    if (scroll && m.frozen == null && tc != null) {
      final upto = cols.indexOf(tc) + 1;
      final w = widths.take(upto).fold(0.0, (a, b) => a + b);
      frozen = w <= avail * .62 ? upto : 1;
    }
    // a figure column first (a cash journal's Cash Dr, a month-by-month schedule): nothing worth pinning
    if (m.frozen == null && const {ColT.num, ColT.money, ColT.dr, ColT.cr}.contains(m.types[0])) frozen = 0;
    if (scroll && frozen > 0) {
      // keep the frozen part under ~45 % of the card so there is room to scroll
      final f0 = widths.take(frozen).fold(0.0, (a, b) => a + b);
      final cap = math.max(avail * .45, sumOf(minOf, cols).take(frozen).fold(0.0, (a, b) => a + b));
      if (f0 > cap && frozen == 1) widths = [cap, ...widths.skip(1)];
    }

    // ---- colours (all opaque, mixed over the card surface)
    final base = p.surface;
    final headBg = mix(p.ink, p.dark ? .10 : .075, base);
    final stripe = mix(p.ink, p.dark ? .045 : .032, base);
    final headRow = mix(p.ink, p.dark ? .07 : .05, base);
    final ruleC = mix(p.ink, .55, base);
    final totBg = p.dark ? mix(p.butter.tile, .6, base) : mix(p.butter.tile, .5, base);

    final hasHead = m.hasHead;
    final nRows = m.rows.length + (hasHead ? 1 : 0);
    final nc = cols.length;
    final flags = Uint8List(nRows * nc);
    final rowBg = <Color?>[];
    final kids = <Widget>[];

    Widget pad(Widget c, {double left = 0, double right = 0, bool tight = false}) =>
        Padding(padding: EdgeInsets.fromLTRB(padX + left, tight ? 4 : padY, padX + right, tight ? 4 : padY), child: c);

    if (hasHead) {
      rowBg.add(headBg);
      for (final (jj, j) in cols.indexed) {
        flags[jj] |= 4;
        final t = types[j];
        final h = foldInto[j]?.map((k) => k < heads.length ? heads[k] : '').firstWhere((x) => x.trim().isNotEmpty, orElse: () => '') ??
            (j < heads.length ? heads[j] : '');
        final tag = t == ColT.dr && !RegExp(r'\bdr\b', caseSensitive: false).hasMatch(h)
            ? 'Dr'
            : t == ColT.cr && !RegExp(r'\bcr\b', caseSensitive: false).hasMatch(h)
            ? 'Cr'
            : null;
        Widget w = RichPara(
          dateInto.containsKey(j) && (heads[dateInto[j]!]).trim().isNotEmpty ? '${heads[dateInto[j]!]} / $h' : h,
          style: t == ColT.dr ? th.copyWith(color: drInk) : (t == ColT.cr ? th.copyWith(color: crInk) : th),
          colors: rc,
          textAlign: t.figure ? TextAlign.right : null,
        );
        if (tag != null) {
          w = Column(
            crossAxisAlignment: CrossAxisAlignment.end,
            mainAxisSize: MainAxisSize.min,
            children: [
              w,
              Tx(tag, style: ts(13, FontWeight.w900, t == ColT.dr ? drInk : crInk, height: 1.2)),
            ],
          );
        }
        kids.add(pad(t.figure ? Align(alignment: Alignment.bottomRight, child: w) : Align(alignment: Alignment.bottomLeft, child: w)));
      }
    }
    var stripeOn = false;
    for (var i = 0; i < m.rows.length; i++) {
      final mk = m.marks[i];
      final r = (hasHead ? 1 : 0) + i;
      final isHead = mk.contains('head'), isTot = mk.contains('total') || mk.contains('final');
      final isNote = mk.contains('note');
      if (isHead) {
        rowBg.add(headRow);
        stripeOn = false;
      } else if (isTot) {
        rowBg.add(acc ? totBg : null);
      } else {
        rowBg.add(stripeOn ? stripe : null);
        stripeOn = !stripeOn;
      }
      final credit = m.kind == 'journal' && _isCreditLine(m, i);
      for (final (jj, j) in cols.indexed) {
        final t = types[j];
        var txt = m.cell(i, j);
        var right = 0.0;
        final f = foldInto[j];
        if (f != null) {
          final k = f.indexWhere((src) => m.cell(i, src).trim().isNotEmpty);
          if (k >= 0) {
            txt = m.cell(i, f[k]);
            right = (f.length - 1 - k) * step;
          }
        }
        if (t != ColT.text) txt = txt.trim();
        if (t.amount) txt = fmtMoney(txt);
        if (t == ColT.text) txt = txt.trimLeft();
        final st = isHead || isTot || mk.contains('bold') ? bold : (jj == 0 && t == ColT.text ? first : body);
        if (isTot && t.figure && txt.trim().isNotEmpty) {
          flags[r * nc + jj] |= 1;
          if (mk.contains('final')) flags[r * nc + jj] |= 2;
        }
        Widget w;
        if (t.figure) {
          final s2 = _fig(txt.contains('**') ? bold : st);
          w = pad(Tx(_plain(txt), style: s2, textAlign: TextAlign.right), right: right);
        } else {
          final indent = j == tc && (credit || mk.contains('indent')) ? 18.0 : (j == tc && isNote ? 18.0 : 0.0);
          if (credit && m.to != null && txt.isNotEmpty && !txt.startsWith(m.to!)) txt = '${m.to}$txt';
          final style = isNote ? muted.copyWith(fontStyle: FontStyle.italic) : st;
          final para = txt.isEmpty ? const SizedBox.shrink() : RichPara(noBreakSlash(txt), style: style, colors: rc);
          final d = dateInto[j];
          final date = d == null ? '' : m.cell(i, d).trim();
          w = pad(
            date.isEmpty
                ? para
                : Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      Tx(date, style: muted),
                      para,
                    ],
                  ),
            left: indent,
          );
        }
        kids.add(w);
      }
    }
    final spec = GridSpec(
      widths: widths,
      cols: nc,
      frozen: math.min(frozen, nc),
      rowBg: rowBg,
      flags: flags,
      base: base,
      rule: ruleC,
      edge: p.ink,
      headRows: hasHead ? 1 : 0,
    );
    final grid = _ScrollGrid(spec: spec, scroll: scroll, children: kids);
    final legend = <String>{
      for (final j in cols) ...?used[j],
      for (final f in foldInto.values) for (final j in f) ...?used[j],
    };
    if (legend.isEmpty) return grid;
    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      spacing: 6,
      children: [
        grid,
        Padding(padding: const EdgeInsets.symmetric(horizontal: 4), child: Tx(legend.join('  ·  '), style: muted.copyWith(fontSize: 12.5))),
      ],
    );
  }

  static bool _isCreditLine(TableModel m, int i) {
    // only a two-money-column journal (Dr | Cr): a cash journal's several columns have no "credit line"
    int? dj, cj;
    var nd = 0, nc = 0;
    for (var j = 0; j < m.n; j++) {
      if (m.types[j] == ColT.dr) {
        dj ??= j;
        nd++;
      }
      if (m.types[j] == ColT.cr) {
        cj ??= j;
        nc++;
      }
    }
    if (dj == null || cj == null || nd != 1 || nc != 1) return false;
    return m.cell(i, dj).trim().isEmpty && m.cell(i, cj).trim().isNotEmpty;
  }

}

final _meas = Expando<Map<bool, (List<double>, List<double>)>>('tableWidths');

// ------------------------------------------------------------------ T-accounts

/// kind t_account: rows are [Dr date, Dr particulars, Dr amount, Cr date, Cr particulars, Cr amount] (or the 4 columns
/// without dates). A row marked `head` starts a new account (its first cell is the name, an optional second cell the
/// account number); rows marked `total` / `final` are the balancing totals on both sides.
class _TAccounts extends StatelessWidget {
  const _TAccounts(this.m, this.p, this.sc, this.avail);
  final TableModel m;
  final Palette p;
  final TextScaler sc;
  final double avail;

  @override
  Widget build(BuildContext context) {
    final groups = <(String, String, List<int>)>[];
    for (var i = 0; i < m.rows.length; i++) {
      if (m.marks[i].contains('head')) {
        groups.add((m.cell(i, 0), m.n > 1 ? m.cell(i, 1) : '', []));
      } else {
        if (groups.isEmpty) groups.add(('', '', []));
        groups.last.$3.add(i);
      }
    }
    // one type size for the whole card: the largest at which every account fits the width without scrolling
    final fs = [16.0, 15.0, 14.0].firstWhere((f) => groups.every((g) => _widths(g.$3, f).$2 <= avail + .5), orElse: () => 14.0);
    return Column(crossAxisAlignment: CrossAxisAlignment.stretch, spacing: 18, children: [for (final g in groups) _one(context, g.$1, g.$2, g.$3, fs)]);
  }

  static const padX = 6.0;
  bool get dated => m.n >= 6;
  int get o => dated ? 3 : 2; // offset of the Cr side
  TextStyle _body(double fs) => ts(fs, FontWeight.w700, p.ink, height: 1.3);
  TextStyle _bold(double fs) => ts(fs, FontWeight.w900, p.ink, height: 1.3);
  TextStyle _muted(double fs) => ts(fs - 2.5, FontWeight.w800, p.ink2, height: 1.25);

  /// particulars | amount | particulars | amount, and their total
  (List<double>, double) _widths(List<int> idx, double fs) {
    final body = _body(fs), bold = _bold(fs), muted = _muted(fs);
    final figB = bold.copyWith(fontFeatures: const [FontFeature.tabularFigures()]);
    double amtW = 0, partMin = 0, partPref = 0;
    for (final i in idx) {
      for (final side in [0, o]) {
        final a = fmtMoney(m.cell(i, side + o - 1).trim());
        if (a.isNotEmpty) amtW = math.max(amtW, _extent(a, figB, figB, sc).$1);
        final txt = m.cell(i, side + (dated ? 1 : 0));
        final (l, w) = _extent(txt, body, bold, sc);
        final d = dated ? _extent(m.cell(i, side), muted, muted, sc).$1 : 0.0;
        partMin = math.max(partMin, math.max(w, d));
        partPref = math.max(partPref, l);
      }
    }
    amtW += 2 * padX;
    final minP = partMin + 2 * padX;
    final half = avail / 2;
    final partW = math.max(minP, math.min(partPref + 2 * padX, math.max(half - amtW, 70.0)));
    final widths = <double>[partW, amtW, partW, amtW];
    return (widths, widths.fold(0.0, (a, b) => a + b));
  }

  Widget _one(BuildContext context, String name, String no, List<int> idx, double fs) {
    final rc = richColors(p);
    final body = _body(fs), bold = _bold(fs), muted = _muted(fs);
    final fig = body.copyWith(fontFeatures: const [FontFeature.tabularFigures()]);
    final figB = bold.copyWith(fontFeatures: const [FontFeature.tabularFigures()]);
    final ruleC = mix(p.ink, .6, p.surface);
    final (widths, total) = _widths(idx, fs);
    final scroll = total > avail + .5;
    final grid = <double>[for (final w in widths) scroll ? w : w * avail / total];

    final flags = Uint8List(idx.length * 4);
    final kids = <Widget>[];
    for (final (r, i) in idx.indexed) {
      final mk = m.marks[i];
      final tot = mk.contains('total') || mk.contains('final');
      for (final side in [0, o]) {
        final date = dated ? m.cell(i, side).trim() : '';
        final part = m.cell(i, side + (dated ? 1 : 0)).trim();
        final amt = fmtMoney(m.cell(i, side + o - 1).trim());
        final c0 = side == 0 ? 0 : 2;
        if (tot && amt.isNotEmpty) {
          flags[r * 4 + c0 + 1] |= 1;
          if (mk.contains('final') || mk.contains('total')) flags[r * 4 + c0 + 1] |= 2;
        }
        final st = tot || mk.contains('bold') ? bold : body;
        kids.add(
          Padding(
            padding: EdgeInsets.fromLTRB(side == 0 ? padX : padX + 6, 6, padX, 6),
            child: date.isEmpty && part.isEmpty
                ? const SizedBox.shrink()
                : Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      if (date.isNotEmpty) Tx(date, style: muted),
                      if (part.isNotEmpty) RichPara(noBreakSlash(part), style: st, colors: rc),
                    ],
                  ),
          ),
        );
        kids.add(
          Padding(
            padding: const EdgeInsets.fromLTRB(padX, 6, padX, 6),
            child: Align(
              alignment: Alignment.bottomRight,
              child: Tx(_plain(amt), style: amt.contains('**') || tot ? figB : fig, textAlign: TextAlign.right),
            ),
          ),
        );
      }
    }
    final spec = GridSpec(
      widths: grid,
      cols: 4,
      frozen: 0,
      rowBg: [
        for (final i in idx) m.marks[i].contains('total') || m.marks[i].contains('final') ? (p.dark ? mix(p.butter.tile, .6, p.surface) : mix(p.butter.tile, .5, p.surface)) : null,
      ],
      flags: flags,
      base: p.surface,
      rule: ruleC,
      edge: p.ink,
      vRules: const [1],
      radius: 0,
      frame: false,
    );
    final tag = ts(14, FontWeight.w900, p.dark ? p.blue.deep : mix(p.blue.deep, .8, p.ink), height: 1.2);
    final tagCr = tag.copyWith(color: p.dark ? p.peach.deep : mix(p.peach.deep, .8, p.ink));
    final title = ts(17, FontWeight.w900, p.ink, height: 1.25);
    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        // the bar of the T: Dr ... account name (No.) ... Cr
        Padding(
          padding: const EdgeInsets.only(bottom: 4),
          child: Row(
            crossAxisAlignment: CrossAxisAlignment.end,
            children: [
              Tx('Dr', style: tag),
              Expanded(
                child: Padding(
                  padding: const EdgeInsets.symmetric(horizontal: 8),
                  child: RichPara(no.trim().isEmpty ? name : '$name  ·  No. ${no.trim()}', style: title, colors: rc, textAlign: TextAlign.center),
                ),
              ),
              Tx('Cr', style: tagCr),
            ],
          ),
        ),
        DecoratedBox(
          decoration: BoxDecoration(color: ruleC),
          child: const SizedBox(height: 2),
        ),
        _ScrollGrid(spec: spec, scroll: scroll, children: kids),
      ],
    );
  }
}

// ------------------------------------------------------------------ study layouts (narrow screens)

/// the card tone of a table (header strip, card accents)
Tone tableTone(Palette p, TableModel m) => switch (m.kind == 'table' ? (m.layout ?? 'table') : m.kind) {
  'journal' || 'ledger' => p.blue,
  'statement' => p.mint,
  't_account' => p.lilac,
  'compare' => p.lilac,
  'proscons' => p.sage,
  'terms' || 'cards' || 'stack' => p.butter,
  _ => p.peach,
};

const _cycle = ['blue', 'sage', 'lilac', 'butter', 'peach', 'mint'];

Color _soft(Palette p, Tone t) => p.dark ? mix(t.tile, .55, p.surface) : mix(t.tile, .45, p.surface);
Color _band(Palette p, Tone t) => p.dark ? t.tile : mix(t.tile, .95, p.surface);

/// a coloured study card: a title band, then (mini-heading, text) pairs
Widget _tile(Palette p, RichColors rc, Tone t, String title, List<(String, String)> items) {
  final head = ts(17, FontWeight.w900, p.ink, height: 1.25);
  final label = ts(13.5, FontWeight.w900, p.dark ? t.deep : mix(t.deep, .8, p.ink), height: 1.25, spacing: .2);
  final body = ts(16, FontWeight.w700, p.ink, height: 1.35);
  return DecoratedBox(
    decoration: BoxDecoration(
      color: _soft(p, t),
      borderRadius: BorderRadius.circular(16),
      border: Border.all(color: p.dark ? t.mid.withValues(alpha: .35) : t.mid.withValues(alpha: .6), width: 1.2),
    ),
    child: Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        if (title.trim().isNotEmpty)
          DecoratedBox(
            decoration: BoxDecoration(color: _band(p, t), borderRadius: const BorderRadius.vertical(top: Radius.circular(15))),
            child: Padding(padding: const EdgeInsets.fromLTRB(14, 10, 14, 10), child: RichPara(title, style: head, colors: rc)),
          ),
        Padding(
          padding: const EdgeInsets.fromLTRB(14, 10, 14, 12),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            spacing: 9,
            children: [
              for (final (l, v) in items)
                Column(
                  crossAxisAlignment: CrossAxisAlignment.stretch,
                  spacing: 1,
                  children: [
                    if (l.trim().isNotEmpty) RichPara(l, style: label, colors: rc),
                    RichPara(v, style: body, colors: rc),
                  ],
                ),
            ],
          ),
        ),
      ],
    ),
  );
}

/// layout cards: one card per row, the first cell as its title
class _RowCards extends StatelessWidget {
  const _RowCards(this.m, this.p);
  final TableModel m;
  final Palette p;
  @override
  Widget build(BuildContext context) {
    final rc = richColors(p);
    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      spacing: 10,
      children: [
        for (var i = 0; i < m.rows.length; i++)
          _tile(p, rc, p.tone(_cycle[i % _cycle.length]), m.cell(i, 0), [
            for (var j = 1; j < m.n; j++)
              if (m.cell(i, j).trim().isNotEmpty) (j < m.head.length ? m.head[j] : '', m.cell(i, j)),
          ]),
      ],
    );
  }
}

/// layout compare: one card per compared item (column), the first column's labels as mini-headings
class _Compare extends StatelessWidget {
  const _Compare(this.m, this.p);
  final TableModel m;
  final Palette p;
  @override
  Widget build(BuildContext context) {
    final rc = richColors(p);
    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      spacing: 10,
      children: [
        for (var j = 1; j < m.n; j++)
          _tile(p, rc, p.tone(_cycle[(j - 1) % _cycle.length]), j < m.head.length ? m.head[j] : '', [
            for (var i = 0; i < m.rows.length; i++)
              if (m.cell(i, j).trim().isNotEmpty) (m.cell(i, 0), m.cell(i, j)),
          ]),
      ],
    );
  }
}

/// layout terms: a clean two-line list (term, then its explanation; further columns as labelled lines)
class _Terms extends StatelessWidget {
  const _Terms(this.m, this.p);
  final TableModel m;
  final Palette p;
  @override
  Widget build(BuildContext context) {
    final rc = richColors(p);
    final t = p.butter;
    final term = ts(17, FontWeight.w900, p.dark ? t.deep : mix(t.deep, .55, p.ink), height: 1.3);
    final body = ts(16, FontWeight.w700, p.ink, height: 1.35);
    final more = ts(15, FontWeight.w700, p.ink2, height: 1.35);
    final label = ts(13, FontWeight.w900, p.dark ? t.deep : mix(t.deep, .7, p.ink), height: 1.25, spacing: .2);
    final line = mix(p.ink, p.dark ? .14 : .10, p.surface);
    return DecoratedBox(
      decoration: BoxDecoration(color: _soft(p, t), borderRadius: BorderRadius.circular(16)),
      child: Padding(
        padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 4),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            for (var i = 0; i < m.rows.length; i++) ...[
              if (i > 0) DecoratedBox(decoration: BoxDecoration(color: line), child: const SizedBox(height: 1)),
              Padding(
                padding: const EdgeInsets.symmetric(vertical: 10),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.stretch,
                  spacing: 3,
                  children: [
                    RichPara(m.cell(i, 0), style: term, colors: rc),
                    if (m.n > 1 && m.cell(i, 1).trim().isNotEmpty) RichPara(m.cell(i, 1), style: body, colors: rc),
                    for (var j = 2; j < m.n; j++)
                      if (m.cell(i, j).trim().isNotEmpty)
                        Padding(
                          padding: const EdgeInsets.only(top: 3),
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.stretch,
                            children: [
                              if (j < m.head.length && m.head[j].trim().isNotEmpty) Tx(_plain(m.head[j]).trim(), style: label),
                              RichPara(m.cell(i, j), style: more, colors: rc),
                            ],
                          ),
                        ),
                  ],
                ),
              ),
            ],
          ],
        ),
      ),
    );
  }
}

final _proRe = RegExp(r'\b(advantages?|merits?|pros|benefits?|strengths?)\b', caseSensitive: false);
final _conRe = RegExp(r'\b(disadvantages?|demerits?|cons|limitations?|drawbacks?|weaknesses?)\b', caseSensitive: false);

/// (item column, pro column, con column) of an advantages / disadvantages table, or null
(int?, int, int)? prosConsCols(TableModel m) {
  int? pro, con;
  for (var j = 0; j < m.head.length; j++) {
    final h = _plain(m.head[j]);
    if (_conRe.hasMatch(h)) {
      con ??= j;
    } else if (_proRe.hasMatch(h)) {
      pro ??= j;
    }
  }
  if (pro == null || con == null) return null;
  final item = [for (var j = 0; j < m.n; j++) j].where((j) => j != pro && j != con).firstOrNull;
  return (item, pro, con);
}

List<String> _points(String s) => [
  for (final x in s.split(RegExp(r'\n|;\s+')))
    if (x.trim().isNotEmpty) x.trim(),
];

/// ✔ / ✖ drawn with two strokes (no glyph or SVG needed)
class _MarkPainter extends CustomPainter {
  const _MarkPainter(this.good, this.color);
  final bool good;
  final Color color;
  @override
  void paint(Canvas canvas, Size size) {
    final w = size.width, h = size.height;
    final pt = Paint()
      ..color = color
      ..strokeWidth = 2.6
      ..style = PaintingStyle.stroke
      ..strokeCap = StrokeCap.round
      ..strokeJoin = StrokeJoin.round;
    if (good) {
      canvas.drawPath(Path()..moveTo(w * .14, h * .54)..lineTo(w * .4, h * .8)..lineTo(w * .88, h * .22), pt);
    } else {
      canvas.drawLine(Offset(w * .2, h * .2), Offset(w * .8, h * .8), pt);
      canvas.drawLine(Offset(w * .8, h * .2), Offset(w * .2, h * .8), pt);
    }
  }

  @override
  bool shouldRepaint(_MarkPainter old) => old.good != good || old.color != color;
}

/// layout proscons: per item a card with a green advantages section and a red disadvantages section
class _ProsCons extends StatelessWidget {
  const _ProsCons(this.m, this.p, this.cols);
  final TableModel m;
  final Palette p;
  final (int?, int, int) cols;
  @override
  Widget build(BuildContext context) {
    final rc = richColors(p);
    final (item, pro, con) = cols;
    final title = ts(17, FontWeight.w900, p.ink, height: 1.25);
    final body = ts(16, FontWeight.w700, p.ink, height: 1.35);
    Widget section(bool good, String head, List<String> pts) {
      final t = good ? p.sage : p.peach;
      final deep = p.dark ? t.deep : mix(t.deep, .85, p.ink);
      return DecoratedBox(
        decoration: BoxDecoration(color: _soft(p, t), borderRadius: BorderRadius.circular(12)),
        child: Padding(
          padding: const EdgeInsets.fromLTRB(12, 9, 12, 10),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            spacing: 6,
            children: [
              RichPara(head, style: ts(14, FontWeight.w900, deep, height: 1.2, spacing: .3), colors: rc),
              for (final x in pts)
                Row(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Padding(
                      padding: const EdgeInsets.only(top: 3, right: 8),
                      child: CustomPaint(size: const Size(16, 16), painter: _MarkPainter(good, deep)),
                    ),
                    Expanded(child: RichPara(x, style: body, colors: rc)),
                  ],
                ),
            ],
          ),
        ),
      );
    }

    final proH = _plain(m.head[pro]).trim().isEmpty ? 'Advantages' : m.head[pro];
    final conH = _plain(m.head[con]).trim().isEmpty ? 'Disadvantages' : m.head[con];
    // no item column: one card with every point
    final groups = item == null
        ? [('', [for (var i = 0; i < m.rows.length; i++) ..._points(m.cell(i, pro))], [for (var i = 0; i < m.rows.length; i++) ..._points(m.cell(i, con))])]
        : [for (var i = 0; i < m.rows.length; i++) (m.cell(i, item), _points(m.cell(i, pro)), _points(m.cell(i, con)))];
    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      spacing: 12,
      children: [
        for (final (name, pros, cons) in groups)
          Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            spacing: 6,
            children: [
              if (name.trim().isNotEmpty) Padding(padding: const EdgeInsets.only(left: 2, top: 2), child: RichPara(name, style: title, colors: rc)),
              if (pros.isNotEmpty) section(true, proH, pros),
              if (cons.isNotEmpty) section(false, conH, cons),
            ],
          ),
      ],
    );
  }
}

// ------------------------------------------------------------------ accounting: abbreviations, sections, entries

const _abbr = <(String, String, String)>[
  // (pattern word, short form, legend meaning)
  ('Accounts', 'Acc.', 'accounts'),
  ('Account', 'Acc.', 'account'),
  ('Receivable', 'Rec.', 'receivable'),
  ('Payable', 'Pay.', 'payable'),
  ('General', 'Gen.', 'general'),
  ('Discounts', 'Disc.', 'discounts'),
  ('Discount', 'Disc.', 'discount'),
  ('Purchases', 'Purch.', 'purchases'),
  ('Balance', 'Bal.', 'balance'),
  ('Quantity', 'Qty', 'quantity'),
  ('Amount', 'Amt', 'amount'),
];

/// short header for a narrow accounting grid, and the abbreviations it used ("Acc. = accounts")
(String, List<String>) shortHead(String h, ColT t) {
  var s = _plain(h).replaceAll(RegExp(r'\s*\((Sundry)\)'), '').trim();
  final used = <String>[];
  if (t == ColT.ref) {
    if (RegExp(r'^p\s*/\s*r\.?$|^post\.?\s*ref\.?$|^posting ref', caseSensitive: false).hasMatch(s)) return ('PR', const ['PR = posting reference']);
    return (s, used);
  }
  if (!t.figure) return (h, used);
  // "Unadjusted Trial Balance — Debit" -> "UTB Dr" (UTB = Unadjusted Trial Balance)
  final k = s.lastIndexOf(' — ');
  if (k > 0) {
    final g = s.substring(0, k).trim(), words = g.split(RegExp(r'\s+')).where((w) => RegExp(r'^[A-Za-z]').hasMatch(w)).toList();
    if (words.length >= 2) {
      final ini = words.map((w) => w[0].toUpperCase()).join();
      used.add('$ini = $g');
      s = '$ini ${s.substring(k + 3)}';
    }
  }
  s = s
      .replaceAllMapped(RegExp(r'\(?\b(debit|dr)\b\.?\)?', caseSensitive: false), (_) => 'Dr')
      .replaceAllMapped(RegExp(r'\(?\b(credit|cr)\b\.?\)?', caseSensitive: false), (_) => 'Cr');
  for (final (w, a, mean) in _abbr) {
    final re = RegExp('\\b$w\\b');
    if (re.hasMatch(s)) {
      s = s.replaceAll(re, a);
      used.add('$a = $mean');
    }
  }
  return (s.replaceAll(RegExp(r'\s+'), ' ').trim(), used);
}

/// column groups of a worksheet-style header ("Trial Balance — Debit"): group name -> its figure columns
List<(String, List<int>)> sectionGroups(TableModel m) {
  final out = <(String, List<int>)>[];
  for (var j = 0; j < m.n; j++) {
    if (!m.types[j].figure || j >= m.head.length) continue;
    final h = _plain(m.head[j]).trim();
    final k = h.lastIndexOf(' — ');
    // "Trial Balance — Debit", or "Income Statement Debit"
    final side = RegExp(r'^(.*\S)\s+(debit|credit|dr\.?|cr\.?)$', caseSensitive: false).firstMatch(h);
    if (k <= 0 && side == null) return const [];
    final g = k > 0 ? h.substring(0, k).trim() : side![1]!.trim();
    if (out.isNotEmpty && out.last.$1 == g) {
      out.last.$2.add(j);
    } else {
      if (out.any((x) => x.$1 == g)) return const [];
      out.add((g, [j]));
    }
  }
  // a section is a Debit / Credit pair (or more): single-column "groups" are just account columns (special journals)
  return out.length >= 2 && out.every((g) => g.$2.length >= 2) ? out : const [];
}

final _sectionModels = Expando<List<TableModel>>('tableSections');

/// the table restricted to its label columns plus one column group (layout grid, so it never nests)
List<TableModel> sectionModels(TableModel m, List<(String, List<int>)> groups) => _sectionModels[m] ??= [
  for (final (_, cs) in groups)
    () {
      final keep = [
        for (var j = 0; j < m.n; j++)
          if (!m.types[j].figure || cs.contains(j)) j,
      ];
      String hd(int j) {
        final h = j < m.head.length ? m.head[j] : '';
        if (!cs.contains(j)) return h;
        final k = h.lastIndexOf(' — ');
        return k > 0 ? h.substring(k + 3) : h.trim().split(RegExp(r'\s+')).last;
      }

      // a total line with nothing in this group: no rule / band; an unlabeled one is left out
      bool has(int i) => cs.any((j) => m.cell(i, j).trim().isNotEmpty);
      bool tot(int i) => m.marks[i].contains('total') || m.marks[i].contains('final');
      bool labeled(int i) => keep.any((j) => !cs.contains(j) && m.cell(i, j).trim().isNotEmpty);
      final rows = [
        for (var i = 0; i < m.rows.length; i++)
          if (!tot(i) || has(i) || labeled(i)) i,
      ];
      return TableModel(
        [for (final j in keep) hd(j)],
        [
          for (final i in rows) [for (final j in keep) m.cell(i, j)],
        ],
        kind: m.kind,
        cols: [for (final j in keep) m.types[j].name],
        marks: [for (final i in rows) tot(i) && !has(i) ? '' : m.marks[i].join(' ')],
        layout: 'grid',
      );
    }(),
  TableModel(m.head, m.rows, kind: m.kind, cols: [for (final t in m.types) t.name], marks: [for (final mk in m.marks) mk.join(' ')], layout: 'grid'),
];

/// layout sections: a toggle between the column groups (+ "All")
class _Sections extends StatefulWidget {
  const _Sections(this.m, this.groups);
  final TableModel m;
  final List<(String, List<int>)> groups;
  @override
  State<_Sections> createState() => _SectionsState();
}

class _SectionsState extends State<_Sections> {
  var at = 0;
  @override
  Widget build(BuildContext context) {
    final p = Kit.of(context).p;
    final names = [for (final g in widget.groups) g.$1, 'All'];
    final models = sectionModels(widget.m, widget.groups);
    final t = p.mint;
    final on = _band(p, t), off = mix(p.ink, p.dark ? .08 : .05, p.surface);
    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      spacing: 10,
      children: [
        Wrap(
          spacing: 6,
          runSpacing: 6,
          children: [
            for (final (i, n) in names.indexed)
              Semantics(
                button: true,
                selected: i == at,
                child: GestureDetector(
                  behavior: HitTestBehavior.opaque,
                  onTap: () => setState(() => at = i),
                  child: DecoratedBox(
                    key: ValueKey('section$i'),
                    decoration: BoxDecoration(
                      color: i == at ? on : off,
                      borderRadius: BorderRadius.circular(999),
                      border: Border.all(color: i == at ? (p.dark ? t.deep : mix(t.deep, .7, t.mid)) : transparent, width: 1.5),
                    ),
                    child: Padding(
                      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 7),
                      child: Tx(n, style: ts(14, FontWeight.w900, i == at ? p.ink : p.ink2, height: 1.2)),
                    ),
                  ),
                ),
              ),
          ],
        ),
        NTable(head: const [], rows: const [], model: models[at]),
      ],
    );
  }
}

/// layout entries: one block per row; text cells on top, figures as labelled chips (Dr blue, Cr red)
class _Entries extends StatelessWidget {
  const _Entries(this.m, this.p);
  final TableModel m;
  final Palette p;
  @override
  Widget build(BuildContext context) {
    final rc = richColors(p);
    final body = ts(16, FontWeight.w800, p.ink, height: 1.3);
    final muted = ts(13.5, FontWeight.w800, p.ink2, height: 1.25);
    final chipL = ts(12.5, FontWeight.w900, p.ink2, height: 1.15);
    final fig = ts(15.5, FontWeight.w800, p.ink, height: 1.2).copyWith(fontFeatures: const [FontFeature.tabularFigures()]);
    final figB = fig.copyWith(fontWeight: FontWeight.w900);
    final stripe = mix(p.ink, p.dark ? .045 : .032, p.surface);
    final totBg = _soft(p, p.butter);
    Color chipBg(ColT t) => t == ColT.dr ? _soft(p, p.blue) : t == ColT.cr ? _soft(p, p.peach) : mix(p.ink, p.dark ? .08 : .05, p.surface);
    Color chipInk(ColT t) => t == ColT.dr
        ? (p.dark ? p.blue.deep : mix(p.blue.deep, .8, p.ink))
        : t == ColT.cr
        ? (p.dark ? p.peach.deep : mix(p.peach.deep, .8, p.ink))
        : p.ink2;
    final short = [for (var j = 0; j < m.n; j++) shortHead(j < m.head.length ? m.head[j] : '', m.types[j])];
    final labels = [for (final x in short) x.$1];
    final legend = <String>{
      for (var j = 0; j < m.n; j++)
        if (m.types[j].figure || m.types[j] == ColT.ref) ...short[j].$2,
    }..remove('PR = posting reference');
    final kids = <Widget>[];
    var stripeOn = false;
    for (var i = 0; i < m.rows.length; i++) {
      final mk = m.marks[i];
      final tot = mk.contains('total') || mk.contains('final');
      final texts = <Widget>[];
      final meta = <String>[];
      for (var j = 0; j < m.n; j++) {
        final c = m.cell(i, j).trim();
        if (c.isEmpty || m.types[j].figure) continue;
        if (m.types[j] == ColT.text) {
          texts.add(
            RichPara(
              noBreakSlash(c),
              style: mk.contains('note') ? muted.copyWith(fontStyle: FontStyle.italic) : (tot || mk.contains('head') ? body.copyWith(fontWeight: FontWeight.w900) : body),
              colors: rc,
            ),
          );
        } else {
          meta.add(m.types[j] == ColT.ref && labels[j].isNotEmpty && labels[j] != 'PR' ? '${labels[j]} $c' : c);
        }
      }
      final chips = <Widget>[
        for (var j = 0; j < m.n; j++)
          if (m.types[j].figure && m.cell(i, j).trim().isNotEmpty)
            DecoratedBox(
              decoration: BoxDecoration(color: chipBg(m.types[j]), borderRadius: BorderRadius.circular(10)),
              child: Padding(
                padding: const EdgeInsets.fromLTRB(9, 5, 9, 6),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.end,
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    if (labels[j].isNotEmpty) Tx(labels[j], style: chipL.copyWith(color: chipInk(m.types[j]))),
                    Tx(_plain(m.types[j].amount ? fmtMoney(m.cell(i, j).trim()) : m.cell(i, j).trim()), style: tot ? figB : fig),
                  ],
                ),
              ),
            ),
      ];
      if (texts.isEmpty && chips.isEmpty && meta.isEmpty) continue;
      final bg = tot ? totBg : (mk.contains('head') ? mix(p.ink, p.dark ? .07 : .05, p.surface) : (stripeOn ? stripe : null));
      if (!tot && !mk.contains('head')) stripeOn = !stripeOn;
      kids.add(
        DecoratedBox(
          decoration: BoxDecoration(color: bg, borderRadius: BorderRadius.circular(12)),
          child: Padding(
            padding: const EdgeInsets.fromLTRB(10, 8, 10, 9),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              spacing: 6,
              children: [
                if (meta.isNotEmpty) Tx(meta.join('  ·  '), style: muted),
                ...texts,
                if (chips.isNotEmpty) Wrap(spacing: 6, runSpacing: 6, children: chips),
              ],
            ),
          ),
        ),
      );
    }
    if (legend.isNotEmpty) {
      kids.add(Padding(padding: const EdgeInsets.fromLTRB(4, 4, 4, 0), child: Tx(legend.join('  ·  '), style: muted.copyWith(fontSize: 12.5))));
    }
    return Column(crossAxisAlignment: CrossAxisAlignment.stretch, spacing: 4, children: kids);
  }
}

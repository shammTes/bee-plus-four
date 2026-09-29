// Concept map of one notes unit (High extension `unitMap`): the unit in the middle, its topics on a ring, key ideas on an
// outer ring next to their topic. Pan / pinch to zoom; tap a node to jump to the card where it is taught.
import 'dart:math' as math;

import 'package:flutter/widgets.dart';

import 'jr/data/repository.dart';
import 'jr/theme/tokens.dart';
import 'jr/widgets/clay_widgets.dart';

/// radial layout (pure; tested)
({Size size, Map<String, Offset> pos}) layoutConceptMap(UnitMap m) {
  final byId = {for (final n in m.nodes) n.id: n};
  final root = byId[m.root] ?? m.nodes.first;
  final topics = m.nodes.where((n) => n.id != root.id && n.kind == 'topic').toList();
  final parent = <String, String>{};
  for (final n in m.nodes) {
    if (n.id == root.id || n.kind == 'topic') continue;
    for (final e in m.edges) {
      final other = e.from == n.id ? e.to : (e.to == n.id ? e.from : null);
      if (other != null && byId[other]?.kind == 'topic') {
        parent[n.id] = other;
        break;
      }
    }
  }
  final ideasOf = <String, List<MapNode>>{};
  for (final n in m.nodes) {
    if (n.id == root.id || n.kind == 'topic') continue;
    (ideasOf[parent[n.id] ?? root.id] ??= []).add(n);
  }
  // a map without topic nodes: everything on one ring
  final ring1 = topics.isEmpty ? (ideasOf.remove(root.id) ?? []) : topics;
  final loose = ideasOf.remove(root.id) ?? [];
  final r1 = math.max(150.0, ring1.length * 34.0);
  var maxIdeas = 0;
  for (final l in ideasOf.values) {
    maxIdeas = math.max(maxIdeas, l.length);
  }
  final r2 = r1 + 150 + math.max(0, maxIdeas - 3) * 12.0;
  final pos = <String, Offset>{root.id: Offset.zero};
  final n1 = ring1.length + (loose.isNotEmpty ? 1 : 0);
  final slot = n1 == 0 ? 0.0 : 2 * math.pi / n1;
  for (var i = 0; i < ring1.length; i++) {
    final a = -math.pi / 2 + i * slot;
    pos[ring1[i].id] = Offset(math.cos(a), math.sin(a)) * r1;
    final ideas = ideasOf[ring1[i].id] ?? const [];
    for (var j = 0; j < ideas.length; j++) {
      final spread = math.min(slot * .85, ideas.length * .32);
      final b = ideas.length == 1 ? a : a - spread / 2 + spread * j / (ideas.length - 1);
      final rr = r2 + (j.isOdd ? 46 : 0);
      pos[ideas[j].id] = Offset(math.cos(b), math.sin(b)) * rr;
    }
  }
  if (loose.isNotEmpty) {
    final a = -math.pi / 2 + ring1.length * slot;
    for (var j = 0; j < loose.length; j++) {
      final spread = math.min(slot * .85, loose.length * .32);
      final b = loose.length == 1 ? a : a - spread / 2 + spread * j / (loose.length - 1);
      pos[loose[j].id] = Offset(math.cos(b), math.sin(b)) * (r1 + (j.isOdd ? 60 : 0));
    }
  }
  var minX = 0.0, minY = 0.0, maxX = 0.0, maxY = 0.0;
  for (final o in pos.values) {
    minX = math.min(minX, o.dx);
    minY = math.min(minY, o.dy);
    maxX = math.max(maxX, o.dx);
    maxY = math.max(maxY, o.dy);
  }
  const pad = Offset(90, 50);
  final shift = Offset(-minX, -minY) + pad;
  return (size: Size(maxX - minX + 2 * pad.dx, maxY - minY + 2 * pad.dy), pos: {for (final e in pos.entries) e.key: e.value + shift});
}

class ConceptMapView extends StatefulWidget {
  const ConceptMapView({super.key, required this.map, required this.tone, required this.onCard, this.height = 360});
  final UnitMap map;
  final String tone;
  final ValueChanged<String> onCard;
  final double height;
  @override
  State<ConceptMapView> createState() => _ConceptMapViewState();
}

class _ConceptMapViewState extends State<ConceptMapView> {
  final _tc = TransformationController();
  late var _lay = layoutConceptMap(widget.map);
  double? _fitW;

  @override
  void didUpdateWidget(ConceptMapView old) {
    super.didUpdateWidget(old);
    if (old.map != widget.map) {
      _lay = layoutConceptMap(widget.map);
      _fitW = null;
    }
  }

  @override
  void dispose() {
    _tc.dispose();
    super.dispose();
  }

  void _fit(double w) {
    if (_fitW == w) return;
    _fitW = w;
    final s = math.min(w / _lay.size.width, widget.height / _lay.size.height).clamp(.2, 1.0);
    final dx = (w - _lay.size.width * s) / 2, dy = (widget.height - _lay.size.height * s) / 2;
    _tc.value = Matrix4.identity()
      ..translateByDouble(dx, dy, 0, 1)
      ..scaleByDouble(s, s, 1, 1);
  }

  @override
  Widget build(BuildContext context) {
    final k = Kit.of(context), p = k.p, t = p.tone(widget.tone);
    final nodes = widget.map.nodes;
    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        LayoutBuilder(
          builder: (context, box) {
            _fit(box.maxWidth);
            return SizedBox(
              height: widget.height,
              child: DecoratedBox(
                decoration: k.c.track(radius: 24),
                child: ClipRRect(
                  borderRadius: BorderRadius.circular(24),
                  child: InteractiveViewer(
                    transformationController: _tc,
                    constrained: false,
                    minScale: .15,
                    maxScale: 3,
                    boundaryMargin: const EdgeInsets.all(400),
                    child: SizedBox.fromSize(
                      size: _lay.size,
                      child: Stack(
                        clipBehavior: Clip.none,
                        children: [
                          Positioned.fill(child: CustomPaint(painter: _Edges(widget.map, _lay.pos, withA(t.deep, .45), p.ink2, p.surface))),
                          for (final n in nodes)
                            if (_lay.pos[n.id] != null) _node(k, n, _lay.pos[n.id]!, t),
                        ],
                      ),
                    ),
                  ),
                ),
              ),
            );
          },
        ),
        Padding(
          padding: const EdgeInsets.only(top: 10),
          child: Text('Pinch to zoom · drag to move · tap a bubble to read that part', textAlign: TextAlign.center, style: ts(15, FontWeight.w700, p.ink2)),
        ),
      ],
    );
  }

  Widget _node(Kit k, MapNode n, Offset c, Tone t) {
    final p = k.p;
    final root = n.id == widget.map.root, topic = n.kind == 'topic';
    final w = root ? 170.0 : (topic ? 150.0 : 128.0);
    final bg = root ? t.mid : (topic ? t.tile : p.surface);
    final fg = root ? (p.dark ? p.bg : white) : (topic ? t.deep : p.ink);
    return Positioned(
      left: c.dx - w / 2,
      top: c.dy - 40,
      width: w,
      height: 80,
      child: Center(
        child: Press(
          key: ValueKey('map-${n.id}'),
          onTap: n.cards.isEmpty ? null : () => widget.onCard(n.cards.first),
          deco: k.c.puffy(c: bg, d: t.deep, radius: 20),
          pressedDeco: k.c.puffyPressed(c: bg, d: t.deep, radius: 20),
          dy: 3,
          padding: EdgeInsets.symmetric(horizontal: 12, vertical: root ? 12 : 9),
          child: Text(
            n.label,
            textAlign: TextAlign.center,
            maxLines: 3,
            overflow: TextOverflow.ellipsis,
            style: ts(root ? 19 : (topic ? 17 : 15.5), FontWeight.w900, fg, height: 1.15),
          ),
        ),
      ),
    );
  }
}

class _Edges extends CustomPainter {
  _Edges(this.m, this.pos, this.line, this.ink, this.bg);
  final UnitMap m;
  final Map<String, Offset> pos;
  final Color line, ink, bg;
  @override
  void paint(Canvas c, Size size) {
    final pen = Paint()
      ..color = line
      ..strokeWidth = 2
      ..style = PaintingStyle.stroke;
    for (final e in m.edges) {
      final a = pos[e.from], b = pos[e.to];
      if (a == null || b == null) continue;
      c.drawLine(a, b, pen);
    }
    for (final e in m.edges) {
      final a = pos[e.from], b = pos[e.to];
      if (a == null || b == null || e.label.isEmpty) continue;
      final mid = Offset.lerp(a, b, .5)!;
      final tp = TextPainter(
        text: TextSpan(text: e.label, style: ts(12, FontWeight.w800, ink, height: 1.1)),
        textDirection: TextDirection.ltr,
        maxLines: 2,
        textAlign: TextAlign.center,
      )..layout(maxWidth: 110);
      final r = Rect.fromCenter(center: mid, width: tp.width + 10, height: tp.height + 4);
      c.drawRRect(RRect.fromRectAndRadius(r, const Radius.circular(8)), Paint()..color = withA(bg, .92));
      tp.paint(c, r.topLeft + const Offset(5, 2));
    }
  }

  @override
  bool shouldRepaint(_Edges o) => o.m != m || o.line != line;
}

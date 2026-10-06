// Theme access + the clay widgets used by every screen (one widget per web component).
import 'dart:ui' show lerpDouble;

import 'package:flutter/rendering.dart';
import 'package:flutter/widgets.dart';

import '../state/app_state.dart';
import '../theme/clay.dart';
import '../theme/deco.dart';
import '../theme/tokens.dart';
import 'art.dart';
import 'page.dart';
import '../theme/perf.dart';

final _dL = Deco(Palette.light), _dD = Deco(Palette.darkP);

/// `final k = Kit.of(context); k.p.ink, k.d.card()`
class Kit {
  Kit._(this.s) : p = s.dark ? Palette.darkP : Palette.light, d = s.dark ? _dD : _dL;
  final HighState s;
  final Palette p;
  final Deco d;
  static Kit of(BuildContext ctx) => Kit._(HighScope.of(ctx));
  Tone tone(String n) => p.tone(n);
}

/// Text with a CSS-like strut; use instead of Text.
class Tx extends StatelessWidget {
  const Tx(this.data, {super.key, required this.style, this.align, this.maxLines, this.ellipsis = false});
  final String data;
  final TextStyle style;
  final TextAlign? align;
  final int? maxLines;
  final bool ellipsis;
  @override
  Widget build(BuildContext context) {
    final t = Text(
      data,
      style: style,
      strutStyle: strutOf(style),
      textAlign: align,
      maxLines: ellipsis ? (maxLines ?? 1) : maxLines,
      overflow: ellipsis ? TextOverflow.ellipsis : null,
      softWrap: ellipsis && (maxLines ?? 1) == 1 ? false : null,
    );
    final h = style.height, fs = style.fontSize;
    if (h == null || fs == null) return t;
    return ExactLines(lineHeight: fs * h * MediaQuery.textScalerOf(context).scale(1), child: t);
  }
}

/// Flutter rounds each line box to whole pixels (18.6 -> 19); Chrome keeps fractions. Reports n × [lineHeight]
/// so stacked text blocks don't drift against the web layout.
class ExactLines extends SingleChildRenderObjectWidget {
  const ExactLines({super.key, required this.lineHeight, super.child});
  final double lineHeight;
  @override
  RenderObject createRenderObject(BuildContext context) => RenderExactLines(lineHeight);
  @override
  void updateRenderObject(BuildContext context, RenderExactLines r) => r.lineHeight = lineHeight;
}

class RenderExactLines extends RenderProxyBox {
  RenderExactLines(this._lh);
  double _lh;
  set lineHeight(double v) {
    if (v == _lh) return;
    _lh = v;
    markNeedsLayout();
  }

  double _fix(double h) {
    if (_lh <= 0 || h <= 0) return h;
    final n = (h / _lh).round();
    return n < 1 ? h : n * _lh;
  }

  @override
  void performLayout() {
    child!.layout(constraints, parentUsesSize: true);
    size = constraints.constrain(Size(child!.size.width, _fix(child!.size.height)));
  }

  @override
  double computeMinIntrinsicHeight(double width) => _fix(super.computeMinIntrinsicHeight(width));
  @override
  double computeMaxIntrinsicHeight(double width) => _fix(super.computeMaxIntrinsicHeight(width));
  @override
  Size computeDryLayout(BoxConstraints c) {
    final s = child!.getDryLayout(c);
    return c.constrain(Size(s.width, _fix(s.height)));
  }
}

/// spring used by `.press` release (cubic-bezier(.34,1.56,.64,1))
const springCurve = Cubic(.34, 1.56, .64, 1);

/// Anything tappable in clay: animates [deco] -> [pressedDeco], moves down [dy] and scales to [scale] while pressed
/// (CSS :active with transition .12s ease-out). [selected] keeps the pressed look (chosen key, current tab).
class Press extends StatefulWidget {
  const Press({
    super.key,
    required this.child,
    this.onTap,
    this.deco,
    this.pressedDeco,
    this.dy = 0,
    this.scale = 1,
    this.selected = false,
    this.padding = EdgeInsets.zero,
    this.constraints,
    this.label,
    this.enabled = true,
  });
  final Widget child;
  final VoidCallback? onTap;
  final ClayDecoration? deco, pressedDeco;
  final double dy, scale;
  final bool selected, enabled;
  final EdgeInsets padding;
  final BoxConstraints? constraints;
  final String? label;
  @override
  State<Press> createState() => _PressState();
}

class _PressState extends State<Press> with SingleTickerProviderStateMixin {
  late final AnimationController _c = AnimationController.unbounded(vsync: this, value: widget.selected ? 1 : 0);
  Offset? _downAt;

  @override
  void didUpdateWidget(Press old) {
    super.didUpdateWidget(old);
    if (old.selected != widget.selected) _c.animateTo(widget.selected ? 1 : 0, duration: const Duration(milliseconds: 120), curve: Curves.easeOut);
  }

  @override
  void dispose() {
    _c.dispose();
    super.dispose();
  }

  void _down(PointerDownEvent e) {
    if (!widget.enabled || widget.onTap == null) return;
    _downAt = e.position;
    _c.animateTo(1, duration: const Duration(milliseconds: 80), curve: Curves.easeOut);
  }

  void _up([Object? _]) {
    if (_downAt == null) return;
    _downAt = null;
    if (widget.selected) return;
    _c.animateTo(0, duration: const Duration(milliseconds: 300), curve: springCurve);
  }

  void _move(PointerMoveEvent e) {
    if (_downAt != null && (e.position - _downAt!).distance > 10) _up();
  }

  @override
  Widget build(BuildContext context) {
    final w = widget;
    final box = AnimatedBuilder(
      animation: _c,
      child: Padding(padding: w.padding, child: w.child),
      builder: (context, child) {
        final t = _c.value;
        final deco = w.deco == null ? null : (w.pressedDeco == null ? w.deco! : ClayDecoration.lerp(w.deco!, w.pressedDeco!, t.clamp(0.0, 1.0))).pressedBy(t);
        Widget b = deco == null ? child! : DecoratedBox(decoration: deco, child: child);
        if (w.constraints != null) b = ConstrainedBox(constraints: w.constraints!, child: b);
        final s = lerpDouble(1, w.scale, t)!;
        if (t == 0) return b;
        return Transform(
          alignment: Alignment.center,
          transform: Matrix4.identity()
            ..translateByDouble(0, w.dy * t, 0, 1)
            ..scaleByDouble(s, s, 1, 1),
          child: b,
        );
      },
    );
    if (w.onTap == null) return box;
    return Semantics(
      button: true,
      label: w.label,
      enabled: w.enabled,
      child: Listener(
        onPointerDown: _down,
        onPointerUp: _up,
        onPointerCancel: _up,
        onPointerMove: _move,
        child: GestureDetector(behavior: HitTestBehavior.opaque, onTap: w.enabled ? w.onTap : null, child: box),
      ),
    );
  }
}

/// `.badge` glossy tone icon (--s px)
class Badge extends StatelessWidget {
  const Badge(this.tone, this.icon, {super.key, this.s = 40});
  final String tone, icon;
  final double s;
  @override
  Widget build(BuildContext context) {
    final k = Kit.of(context), t = k.tone(tone);
    final fg = k.p.dark ? const Color(0xFF2A211B) : white;
    final isz = s * .52;
    return SizedBox(
      width: s,
      height: s,
      child: DecoratedBox(
        decoration: k.d.badge(t, s),
        child: Center(
          child: SizedBox(
            width: isz,
            height: isz,
            child: Stack(
              clipBehavior: Clip.none,
              children: [
                // filter: drop-shadow(0 1px 1px rgba(0,0,0,.18)), drawn unblurred and only in the Clay look
                if (!Perf.flat) Positioned(left: 0, top: 1, child: Ic(icon, size: isz, color: const Color.fromRGBO(0, 0, 0, .14))),
                Ic(icon, size: isz, color: fg),
              ],
            ),
          ),
        ),
      ),
    );
  }
}


// ---------------------------------------------------------------- buttons
enum BtnKind { coral, tone, soft }

/// `.btn` (padding 13 18, 900 14.5px, icon 18, gap 8); disabled = pushed in and grey
class Btn extends StatelessWidget {
  const Btn(this.label, {super.key, this.icon, this.kind = BtnKind.coral, this.tone = 'sage', this.onTap, this.enabled = true, this.block = false, this.trailing = false, this.padding = const EdgeInsets.symmetric(horizontal: 18, vertical: 13), this.fontSize = 14.5});
  final String label;
  final String? icon;
  final BtnKind kind;
  final String tone;
  final VoidCallback? onTap;
  final bool enabled, block, trailing;
  final EdgeInsets padding;
  final double fontSize;
  @override
  Widget build(BuildContext context) {
    final k = Kit.of(context), p = k.p, d = k.d, t = k.tone(tone);
    var (deco, pd, fg) = switch (kind) {
      BtnKind.coral => (d.btnCoral(), d.btnCoralPressed(), p.onCoral),
      BtnKind.tone => (d.btnTone(t), d.btnTonePressed(t), p.dark ? const Color(0xFF1F1915) : white),
      BtnKind.soft => (d.btnSoft(), d.btnSoftPressed(), p.ink),
    };
    if (!enabled) {
      deco = d.btnDisabled();
      pd = deco;
      fg = p.ink3;
    }
    final shadow = kind == BtnKind.tone && !p.dark && enabled ? const [Shadow(offset: Offset(0, 1), color: Color.fromRGBO(0, 0, 0, .12))] : null;
    final st = ts(fontSize, w900, fg).copyWith(shadows: shadow);
    final ic = icon == null ? null : Ic(icon!, size: 18, color: fg);
    final row = Row(
      mainAxisSize: block ? MainAxisSize.max : MainAxisSize.min,
      mainAxisAlignment: MainAxisAlignment.center,
      spacing: 8,
      children: [if (ic != null && !trailing) ic, Flexible(child: Text(label, style: st, maxLines: 1, overflow: TextOverflow.ellipsis, softWrap: false)), if (ic != null && trailing) ic],
    );
    if (!enabled) {
      return Transform.translate(offset: const Offset(0, 4), child: DecoratedBox(decoration: deco, child: Padding(padding: padding, child: row)));
    }
    return Press(onTap: onTap ?? () {}, deco: deco, pressedDeco: pd, dy: 4, padding: padding, child: row);
  }
}

/// `.cbtn` 42px round (top bar)
class CBtn extends StatelessWidget {
  const CBtn(this.icon, {super.key, required this.onTap, this.label, this.size = 42});
  final String icon;
  final VoidCallback onTap;
  final String? label;
  final double size;
  @override
  Widget build(BuildContext context) {
    final k = Kit.of(context);
    return Press(
      onTap: onTap,
      label: label,
      deco: k.d.cbtn(),
      pressedDeco: k.d.cbtnPressed(),
      dy: 3,
      child: SizedBox(width: size, height: size, child: Center(child: Ic(icon, size: 20, color: k.p.ink2))),
    );
  }
}

/// `.playbtn` 40px round with the play triangle (colour var(--deep, blue-3))
class PlayBtn extends StatelessWidget {
  const PlayBtn({super.key, required this.onTap, this.tone, this.size = 40, this.icon = 16, this.onArt = false, this.color, this.label});
  final VoidCallback? onTap;
  final String? tone;
  final double size, icon;
  final bool onArt;
  final Color? color;
  final String? label;
  @override
  Widget build(BuildContext context) {
    final k = Kit.of(context);
    final c = color ?? (tone != null ? k.tone(tone!).deep : k.p.blue.deep);
    return Press(
      onTap: onTap,
      label: label,
      deco: onArt ? k.d.playOnArt() : k.d.cbtn(),
      pressedDeco: k.d.cbtnPressed(),
      dy: 3,
      child: SizedBox(
        width: size,
        height: size,
        child: Center(child: Padding(padding: const EdgeInsets.only(left: 2), child: Ic('play', size: icon, color: c))),
      ),
    );
  }
}

/// `.avatar` 42px (first letter of the name)
class Avatar extends StatelessWidget {
  const Avatar({super.key, this.onTap, this.size = 42, this.fontSize = 17});
  final VoidCallback? onTap;
  final double size, fontSize;
  @override
  Widget build(BuildContext context) {
    final k = Kit.of(context);
    final n = (k.s.name ?? 'S').trim();
    final letter = (n.isEmpty ? 'S' : n[0]).toUpperCase();
    return Press(
      onTap: onTap,
      label: 'Profile',
      deco: k.d.avatar(),
      pressedDeco: k.d.avatarPressed(),
      dy: 3,
      child: SizedBox(
        width: size,
        height: size,
        child: Center(child: Text(letter, style: ts(fontSize, w900, k.p.dark ? const Color(0xFF1F2A22) : white))),
      ),
    );
  }
}

/// `.chip` (9 14, 800 13px) with optional counter `.c`
class ChipX extends StatelessWidget {
  const ChipX(this.label, {super.key, this.count, this.on = false, this.onTap, this.small = false, this.tone, this.icon});
  final String label;
  final Object? count;
  final bool on, small;
  final String? tone, icon;
  final VoidCallback? onTap;
  @override
  Widget build(BuildContext context) {
    final k = Kit.of(context), p = k.p;
    final t = tone == null ? null : k.tone(tone!);
    final fg = on ? p.bg : (t?.deep ?? p.ink2);
    return Press(
      onTap: onTap ?? () {},
      selected: on,
      deco: t != null ? k.d.chipTone(t) : k.d.chip(),
      pressedDeco: on ? k.d.chipOn() : k.d.chipPressed(),
      dy: 3,
      padding: small ? const EdgeInsets.symmetric(horizontal: 12, vertical: 7) : const EdgeInsets.symmetric(horizontal: 14, vertical: 9),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        spacing: 6,
        children: [
          if (icon != null) Ic(icon!, size: 14, color: fg),
          Flexible(child: Text(label, maxLines: 1, overflow: TextOverflow.ellipsis, softWrap: false, style: ts(small ? 12.5 : 13, w800, fg))),
          if (count != null)
            DecoratedBox(
              decoration: k.d.count(on ? const Color.fromRGBO(255, 255, 255, .18) : p.surface2),
              child: Padding(
                padding: const EdgeInsets.symmetric(horizontal: 7, vertical: 1),
                child: Text('$count', style: ts(11, w800, on ? fg : p.ink3)),
              ),
            ),
        ],
      ),
    );
  }
}

/// `.pill` (6 12, 800 12px, icon 14)
class PillX extends StatelessWidget {
  const PillX(this.label, {super.key, this.icon, this.onTap});
  final String label;
  final String? icon;
  final VoidCallback? onTap;
  @override
  Widget build(BuildContext context) {
    final k = Kit.of(context), p = k.p;
    return Press(
      onTap: onTap,
      deco: k.d.pill(),
      pressedDeco: k.d.pillPressed(),
      dy: 3,
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
      child: Row(mainAxisSize: MainAxisSize.min, spacing: 5, children: [if (icon != null) Ic(icon!, size: 14, color: p.ink2), Text(label, style: ts(12, w800, p.ink2))]),
    );
  }
}

/// `.bar` progress (debossed track, puffy fill)
class Bar extends StatelessWidget {
  const Bar(this.pct, {super.key, required this.tone, this.height = 9, this.onTile = false});
  final num pct;
  final String tone;
  final double height;
  final bool onTile;
  @override
  Widget build(BuildContext context) {
    final k = Kit.of(context);
    return SizedBox(
      height: height,
      child: DecoratedBox(
        decoration: k.d.barTrack(onTile: onTile),
        child: ClipRRect(
          borderRadius: BorderRadius.circular(99),
          child: Align(
            alignment: Alignment.centerLeft,
            child: FractionallySizedBox(
              widthFactor: (pct / 100).clamp(0.0, 1.0).toDouble(),
              heightFactor: 1,
              child: DecoratedBox(decoration: k.d.barFill(k.tone(tone))),
            ),
          ),
        ),
      ),
    );
  }
}

/// `.section-label` (13px/900, margin 22 6 4)
class SectionLabel extends StatelessWidget implements Spaced {
  const SectionLabel(this.text, {super.key, this.n, this.icon});
  final String text;
  final Object? n;
  final String? icon;
  @override
  EdgeInsets get blockMargin => const EdgeInsets.fromLTRB(6, 22, 6, 4);
  @override
  Widget build(BuildContext context) {
    final p = Kit.of(context).p;
    return Padding(
      padding: bareM(context, this, blockMargin),
      child: Row(
        spacing: 8,
        children: [
          if (icon != null) Ic(icon!, size: 16, color: p.ink2),
          Flexible(child: Text(text, style: ts(13, w900, p.ink2), maxLines: 1, overflow: TextOverflow.ellipsis)),
          if (n != null) Text('$n', style: ts(11.5, w800, p.ink3)),
        ],
      ),
    );
  }
}

/// `.card` / `.tile.t-x`: puffy panel; tappable panels get the pressed-in state
class Panel extends StatelessWidget implements Spaced {
  const Panel({super.key, required this.child, this.tone, this.padding = const EdgeInsets.all(16), this.margin = const EdgeInsets.symmetric(vertical: 14), this.radius = R.lg, this.onTap, this.fills, this.clip = false, this.label});
  final Widget child;
  final String? tone;
  final EdgeInsets padding, margin;
  final double radius;
  final VoidCallback? onTap;
  final List<Fill>? fills;
  final bool clip;
  final String? label;
  @override
  EdgeInsets get blockMargin => margin;
  @override
  Widget build(BuildContext context) {
    final k = Kit.of(context), d = k.d;
    final margin = bareM(context, this, this.margin);
    final t = tone == null ? null : k.tone(tone!);
    ClayDecoration deco, pd;
    if (fills != null) {
      deco = d.tileWith(t ?? k.p.peach, fills!, radius: radius);
      pd = d.tileWith(t ?? k.p.peach, fills!, radius: radius, pressed: true);
    } else if (t != null) {
      deco = d.tile(t, radius: radius);
      pd = d.tilePressed(t, radius: radius);
    } else {
      deco = d.card(radius: radius);
      pd = d.cardPressed(radius: radius);
    }
    Widget c = Padding(padding: padding, child: child);
    if (clip) c = ClipRRect(borderRadius: BorderRadius.circular(radius), child: c);
    return Padding(
      padding: margin,
      child: onTap == null ? DecoratedBox(decoration: deco, child: c) : Press(onTap: onTap, label: label, deco: deco, pressedDeco: pd, dy: 3, scale: .985, child: c),
    );
  }
}

/// `.thumb` 48px raised tone knob (radius 15) with a child (badge / year)
class Knob extends StatelessWidget {
  const Knob({super.key, this.tone, required this.child, this.size = 48, this.radius = 15});
  final String? tone;
  final Widget child;
  final double size, radius;
  @override
  Widget build(BuildContext context) {
    final k = Kit.of(context);
    return SizedBox(
      width: size,
      height: size,
      child: DecoratedBox(decoration: k.d.knob(tone == null ? null : k.tone(tone!), radius: radius), child: Center(child: child)),
    );
  }
}

/// segmented control `.seg` (track + raised keys, chosen key pressed in); [cat] = `.catseg`
class Seg extends StatelessWidget {
  const Seg({super.key, required this.items, required this.current, required this.onPick, this.cat = false});
  final List<({String id, String label, String icon, Object? count, String tone, bool enabled})> items;
  final String current;
  final ValueChanged<String> onPick;
  final bool cat;
  @override
  Widget build(BuildContext context) {
    final k = Kit.of(context), p = k.p;
    return DecoratedBox(
      decoration: k.d.segTrack(),
      child: Padding(
        padding: cat ? const EdgeInsets.fromLTRB(6, 6, 6, 10) : const EdgeInsets.fromLTRB(5, 5, 5, 9),
        child: Row(
          spacing: cat ? 6 : 4,
          children: [
            for (final it in items)
              Expanded(
                child: () {
                  final on = it.id == current, t = k.tone(it.tone);
                  final fg = on ? (cat ? t.deep : p.sage.deep) : p.ink2;
                  return Press(
                    onTap: it.enabled ? () => onPick(it.id) : null,
                    selected: on,
                    deco: k.d.segKey(),
                    pressedDeco: k.d.segKeyOn(cat ? t : p.sage, cat: cat),
                    dy: 4,
                    padding: cat ? const EdgeInsets.symmetric(horizontal: 8, vertical: 15) : const EdgeInsets.all(10),
                    constraints: BoxConstraints(minHeight: cat ? 54 : 0),
                    child: CenterOverflow(child: Row(
                      mainAxisSize: MainAxisSize.min,
                      spacing: 6,
                      children: [
                        Ic(it.icon, size: cat ? 20 : 16, color: fg),
                        Text(it.label, style: ts(cat ? 16 : 13.5, w900, fg, spacing: cat ? -.16 : null), maxLines: 1, softWrap: false),
                        if (it.count != null)
                          DecoratedBox(
                            decoration: k.d.count(on ? (cat ? p.surface : p.surface) : p.surface2),
                            child: Padding(
                              padding: cat ? const EdgeInsets.symmetric(horizontal: 9, vertical: 2) : const EdgeInsets.symmetric(horizontal: 7, vertical: 1),
                              child: Text('${it.count}', style: ts(cat ? 12.5 : 11, w800, on ? fg : p.ink3)),
                            ),
                          ),
                      ],
                    )),
                  );
                }(),
              ),
          ],
        ),
      ),
    );
  }
}

/// text input without Material: `.field` (debossed well, 800 16px, padding 15 16) or `.search` (pill, 700 14px)
class Field extends StatefulWidget {
  const Field({super.key, this.controller, this.placeholder = '', this.search = false, this.onChanged, this.onSubmitted, this.maxLength, this.autofocus = false, this.fieldKey});
  final TextEditingController? controller;
  final String placeholder;
  final bool search, autofocus;
  final ValueChanged<String>? onChanged, onSubmitted;
  final int? maxLength;
  final Key? fieldKey;
  @override
  State<Field> createState() => _FieldState();
}

class _FieldState extends State<Field> {
  late final TextEditingController _c = widget.controller ?? TextEditingController();
  final _f = FocusNode();
  @override
  void initState() {
    super.initState();
    _c.addListener(_l);
    _f.addListener(_l);
  }

  void _l() => setState(() {});
  @override
  void dispose() {
    _c.removeListener(_l);
    if (widget.controller == null) _c.dispose();
    _f.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final k = Kit.of(context), p = k.p;
    final st = widget.search ? ts(14, w700, p.ink) : ts(16, w800, p.ink);
    final ph = st.copyWith(color: p.ink3);
    final input = Stack(
      children: [
        if (_c.text.isEmpty) IgnorePointer(child: Text(widget.placeholder, style: ph, maxLines: 1, softWrap: false, overflow: TextOverflow.clip)),
        EditableText(
          key: widget.fieldKey,
          controller: _c,
          focusNode: _f,
          style: st,
          cursorColor: p.sage.deep,
          backgroundCursorColor: p.ink3,
          autofocus: widget.autofocus,
          maxLines: 1,
          onChanged: (v) {
            if (widget.maxLength != null && v.length > widget.maxLength!) {
              _c.text = v.substring(0, widget.maxLength);
              return;
            }
            widget.onChanged?.call(v);
          },
          onSubmitted: widget.onSubmitted,
          selectionColor: withA(p.sage.mid, .35),
        ),
      ],
    );
    if (widget.search) {
      return GestureDetector(
        onTap: _f.requestFocus,
        child: SizedBox(
          height: 44,
          child: DecoratedBox(
            decoration: k.d.well(radius: R.pill, fill: p.surface),
            child: Padding(
              padding: const EdgeInsets.symmetric(horizontal: 14),
              child: Row(spacing: 8, children: [Ic('search', size: 18, color: p.ink3), Expanded(child: input)]),
            ),
          ),
        ),
      );
    }
    return GestureDetector(
      onTap: _f.requestFocus,
      child: DecoratedBox(
        decoration: _f.hasFocus ? k.d.well(fill: p.surface).copyWith(shadows: [...k.d.well().shadows, Shadow3(0, 0, 0, 2, p.sage.mid)]) : k.d.well(fill: p.surface),
        child: Padding(padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 15), child: input),
      ),
    );
  }
}

/// lays [child] out at its natural width and centres it, letting it overflow both sides (CSS flex centring of
/// content wider than the box, e.g. the category keys)
class CenterOverflow extends SingleChildRenderObjectWidget {
  const CenterOverflow({super.key, super.child});
  @override
  RenderObject createRenderObject(BuildContext context) => _RenderCenterOverflow();
}

class _RenderCenterOverflow extends RenderShiftedBox {
  _RenderCenterOverflow() : super(null);
  @override
  void performLayout() {
    final c = child!;
    c.layout(BoxConstraints(maxHeight: constraints.maxHeight), parentUsesSize: true);
    size = constraints.constrain(Size(constraints.maxWidth, c.size.height));
    (c.parentData! as BoxParentData).offset = Offset((size.width - c.size.width) / 2, (size.height - c.size.height) / 2);
  }

  @override
  double computeMinIntrinsicHeight(double width) => child?.getMinIntrinsicHeight(double.infinity) ?? 0;
  @override
  double computeMaxIntrinsicHeight(double width) => child?.getMaxIntrinsicHeight(double.infinity) ?? 0;
}

/// text that stays on one line (shrinking up to 2 %) when it is only a pixel or two too wide — browsers round glyph
/// advances, so a line that just fits on the web can be ~1 % wider here — and wraps normally otherwise
class OneLine extends StatelessWidget {
  const OneLine(this.text, {super.key, required this.style});
  final String text;
  final TextStyle style;
  @override
  Widget build(BuildContext context) => LayoutBuilder(
    builder: (context, c) {
      final tp = TextPainter(text: TextSpan(text: text, style: style), textDirection: TextDirection.ltr, maxLines: 1, textScaler: MediaQuery.textScalerOf(context))..layout();
      final w = tp.width;
      tp.dispose();
      if (w <= c.maxWidth || w > c.maxWidth * 1.02) return Text(text, style: style);
      return FittedBox(
        fit: BoxFit.scaleDown,
        alignment: Alignment.centerLeft,
        child: Text(text, style: style, maxLines: 1, softWrap: false),
      );
    },
  );
}

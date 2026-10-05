// Warsay Prep's clay + High's 3D embossed layer (design/clay3d.css) as decorations: one method per CSS rule set.
import 'package:flutter/widgets.dart';

import 'clay.dart';
import 'tokens.dart';

const _defD = Color(0xFF9C7A5B); // var(--deep, #9C7A5B)
const _w = Color(0xFFFFFFFF), _k = Color(0xFF000000);
Color _wa(double a) => withA(_w, a);
Color _ka(double a) => withA(_k, a);

class Deco {
  Deco(this.p);
  final Palette p;
  bool get dk => p.dark;
  BorderRadius _r(double r) => BorderRadius.circular(r);

  // ---------------------------------------------------------------- puffy raised panels (.card .tile .nav .timerbar .msg.bot)
  List<Fill> puffyFill(Color c, Color d) => [
    LinearFill.vertical([mix(c, .58, p.lift), c, mix(c, .9, d)], const [0, .52, 1]),
  ];
  List<Shadow3> puffyShadows(Color d) => dk
      ? [
          Shadow3(0, 14, 18, -12, _ka(.65)),
          Shadow3(0, 5, 8, -6, _ka(.42)),
          Shadow3.inset(4, 6, 9, -4, p.hi),
          Shadow3.inset(-5, -7, 10, -5, _ka(.3)),
        ]
      : [
          Shadow3(0, 14, 18, -14, withA(d, .48)),
          Shadow3(0, 5, 8, -6, withA(d, .3)),
          Shadow3.inset(5, 7, 9, -4, p.hi),
          Shadow3.inset(-5, -7, 10, -5, withA(d, .22)),
        ];
  List<Shadow3> puffyPressedShadows(Color d) => dk
      ? [Shadow3(0, 8, 14, -10, _ka(.7)), Shadow3.inset(4, 6, 11, -4, p.hi), Shadow3.inset(-5, -7, 12, -4, _ka(.45))]
      : [Shadow3(0, 8, 14, -10, withA(d, .55)), Shadow3.inset(5, 7, 11, -4, p.hi), Shadow3.inset(-5, -7, 12, -4, withA(d, .36))];

  /// `.card` (surface) / `.tile.t-x` (tone tile)
  /// Lighter shadow set for long scrolling lists (Matric / Exercise rows).
  List<Shadow3> litePuffyShadows(Color d) => dk
      ? [Shadow3(0, 8, 10, -8, _ka(.55)), Shadow3.inset(3, 4, 6, -3, p.hi)]
      : [Shadow3(0, 8, 10, -8, withA(d, .38)), Shadow3.inset(3, 4, 6, -3, p.hi)];

  ClayDecoration card({double radius = R.lg, bool lite = false}) => ClayDecoration(
        radius: _r(radius),
        fills: puffyFill(p.surface, _defD),
        shadows: lite ? litePuffyShadows(_defD) : puffyShadows(_defD),
      );
  ClayDecoration cardPressed({double radius = R.lg}) =>
      ClayDecoration(radius: _r(radius), fills: puffyFill(p.surface, _defD), shadows: puffyPressedShadows(_defD));
  ClayDecoration tile(Tone t, {double radius = R.lg}) => ClayDecoration(radius: _r(radius), fills: puffyFill(t.tile, t.deep), shadows: puffyShadows(t.deep));
  ClayDecoration tilePressed(Tone t, {double radius = R.lg}) =>
      ClayDecoration(radius: _r(radius), fills: puffyFill(t.tile, t.deep), shadows: puffyPressedShadows(t.deep));

  /// tile with its own background (hero / banner): only the puffy shadows
  ClayDecoration tileWith(Tone t, List<Fill> fills, {double radius = R.lg, bool pressed = false}) =>
      ClayDecoration(radius: _r(radius), fills: fills, shadows: pressed ? puffyPressedShadows(t.deep) : puffyShadows(t.deep));

  List<Fill> heroFill() => dk
      ? [
          RadialFill.circle(.85, .1, const [Color.fromRGBO(255, 220, 190, .10), Color.fromRGBO(255, 220, 190, 0)], const [0, .45]),
          AngleFill(135, [p.peach.tile, mix(p.peach.tile, .7, p.butter.tile)], const [0, 1]),
        ]
      : [
          RadialFill.circle(.85, .1, [_wa(.5), _wa(0)], const [0, .4]),
          AngleFill(135, [p.peach.tile, mix(p.peach.tile, .65, p.butter.tile)], const [0, 1]),
        ];

  /// .banner: linear-gradient(135deg, tile, color-mix(tile 70%, other))
  List<Fill> bannerFill(Tone t, Tone other) => [AngleFill(135, [t.tile, mix(t.tile, .7, other.tile)], const [0, 1])];

  ClayDecoration nav() => ClayDecoration(radius: _r(28), fills: puffyFill(p.surface, _defD), shadows: [...puffyShadows(_defD), Shadow3(0, -6, 20, -12, p.sh(.2))]);

  // ---------------------------------------------------------------- buttons (.btn.coral / .tone / .soft / [disabled])
  ClayDecoration btnCoral({double radius = R.pill}) => ClayDecoration(
    radius: _r(radius),
    fills: [
      RadialFill.ellipse(1.2, .7, .5, -.1, [_wa(.32), _wa(0)], const [0, .55]),
      LinearFill.vertical([p.coral2, p.coral], const [0, 1]),
    ],
    shadows: [Shadow3(0, 5, 0, 0, p.coralEdge), Shadow3(0, 12, 18, -8, withA(p.coral, .7)), Shadow3.inset(0, 2, 1, 0, _wa(.45)), Shadow3.inset(0, -3, 5, 0, _ka(.12))],
  );
  ClayDecoration btnCoralPressed({double radius = R.pill}) =>
      btnCoral(radius: radius).copyWith(shadows: [Shadow3(0, 1, 0, 0, p.coralEdge), Shadow3(0, 4, 8, -4, p.coral), Shadow3.inset(0, 3, 8, 0, _ka(.28))]);

  ClayDecoration btnTone(Tone t) => ClayDecoration(
    radius: _r(R.pill),
    fills: [LinearFill.vertical(dk ? [t.deep, t.mid] : [t.mid, mix(t.mid, .7, t.deep)], const [0, 1])],
    shadows: [Shadow3(0, 5, 0, 0, t.edge(dk)), Shadow3(0, 12, 16, -8, withA(t.deep, .7)), Shadow3.inset(0, 2, 1, 0, _wa(.45)), Shadow3.inset(0, -3, 5, 0, _ka(.12))],
  );
  ClayDecoration btnTonePressed(Tone t) => btnTone(t).copyWith(shadows: [Shadow3(0, 1, 0, 0, t.edge(dk)), Shadow3.inset(0, 3, 8, 0, _ka(.25))]);

  ClayDecoration btnSoft() => ClayDecoration(
    radius: _r(R.pill),
    fills: [LinearFill.vertical([mix(p.surface2, .55, p.lift), p.surface2], const [0, 1])],
    shadows: [Shadow3(0, 5, 0, 0, p.edgeN), Shadow3(0, 12, 16, -9, p.sh(.4)), Shadow3.inset(0, 2, 1, 0, p.hi), Shadow3.inset(0, -3, 5, 0, p.sh(.08))],
  );
  ClayDecoration btnSoftPressed() => btnSoft().copyWith(shadows: [Shadow3(0, 1, 0, 0, p.edgeN), Shadow3.inset(0, 3, 8, 0, p.sh(.25))]);
  ClayDecoration btnDisabled() => ClayDecoration(
    radius: _r(R.pill),
    fills: [SolidFill(p.surface2)],
    shadows: [Shadow3(0, 1, 0, 0, p.edgeN), Shadow3.inset(0, 3, 8, 0, p.sh(.18))],
  );

  // ---------------------------------------------------------------- round buttons (.cbtn .playbtn .bm .avatar)
  ClayDecoration cbtn() => ClayDecoration(
    radius: _r(R.pill),
    fills: [RadialFill.circle(.35, .28, [p.lift, p.surface], const [0, .62])],
    shadows: [Shadow3(0, 4, 0, 0, p.edgeN), Shadow3(0, 10, 14, -7, p.sh(.45)), Shadow3.inset(0, -3, 5, 0, p.sh(.12)), Shadow3.inset(0, 2, 2, 0, p.hi)],
  );
  ClayDecoration cbtnPressed() => cbtn().copyWith(shadows: [Shadow3(0, 1, 0, 0, p.edgeN), Shadow3.inset(0, 3, 6, 0, p.sh(.3))]);

  /// .daily .ov .playbtn (on the illustration)
  ClayDecoration playOnArt() => cbtn().copyWith(
    shadows: [
      const Shadow3(0, 4, 0, 0, Color.fromRGBO(120, 50, 30, .35)),
      const Shadow3(0, 10, 14, -7, Color.fromRGBO(80, 30, 10, .5)),
      Shadow3.inset(0, -3, 5, 0, p.sh(.12)),
      Shadow3.inset(0, 2, 2, 0, p.hi),
    ],
  );

  ClayDecoration bm(bool on) => ClayDecoration(
    radius: _r(R.pill),
    fills: [RadialFill.circle(.35, .28, on ? [mix(p.butter.tile, .5, _w), p.butter.tile] : [p.lift, p.surface2], const [0, .66])],
    shadows: [Shadow3(0, 3, 0, 0, on ? p.butter.mid : p.edgeN), Shadow3(0, 7, 10, -6, p.sh(.4)), Shadow3.inset(0, 2, 2, 0, p.hi)],
  );
  ClayDecoration bmPressed(bool on) => bm(on).copyWith(shadows: [Shadow3(0, 0, 0, 0, withA(p.edgeN, 0)), Shadow3.inset(0, 2, 5, 0, p.sh(.3))]);

  ClayDecoration avatar() => ClayDecoration(
    radius: _r(R.pill),
    fills: [
      RadialFill.circle(.32, .28, [_wa(.55), _wa(0)], const [0, .42]),
      AngleFill(150, [p.sage.mid, p.sage.deep], const [0, 1]),
    ],
    shadows: [Shadow3(0, 4, 0, 0, p.avatarEdge), Shadow3(0, 10, 14, -7, p.sh(.45)), Shadow3.inset(0, 2, 2, 0, _wa(.35)), Shadow3.inset(0, -3, 5, 0, _ka(.12))],
  );
  ClayDecoration avatarPressed() => avatar().copyWith(shadows: [Shadow3(0, 1, 0, 0, p.avatarEdge), Shadow3.inset(0, 3, 6, 0, _ka(.3))]);

  // ---------------------------------------------------------------- chips / pills
  List<Shadow3> _keySm() => [Shadow3(0, 3, 0, 0, p.edgeN), Shadow3(0, 7, 9, -6, p.sh(.35)), Shadow3.inset(0, 2, 1, 0, p.hi)];
  ClayDecoration chip() => ClayDecoration(radius: _r(R.pill), fills: [LinearFill.vertical([mix(p.surface, .5, p.lift), p.surface], const [0, 1])], shadows: _keySm());
  ClayDecoration chipOn() => ClayDecoration(radius: _r(R.pill), fills: [SolidFill(p.ink)], shadows: [Shadow3(0, 0, 0, 0, withA(p.edgeN, 0)), Shadow3.inset(2, 3, 6, 0, _ka(.35))]);
  ClayDecoration chipPressed() => chip().copyWith(shadows: [Shadow3(0, 0, 0, 0, withA(p.edgeN, 0)), Shadow3.inset(2, 3, 6, 0, p.sh(.25))]);
  ClayDecoration chipTone(Tone t) => ClayDecoration(
    radius: _r(R.pill),
    fills: [LinearFill.vertical([mix(t.tile, .5, p.lift), t.tile], const [0, 1])],
    shadows: [Shadow3(0, 3, 0, 0, t.edge(dk)), Shadow3(0, 7, 9, -6, p.sh(.35)), Shadow3.inset(0, 2, 1, 0, p.hi)],
  );
  ClayDecoration pill() => ClayDecoration(radius: _r(R.pill), fills: [LinearFill.vertical([mix(p.surface2, .5, p.lift), p.surface2], const [0, 1])], shadows: _keySm());
  ClayDecoration pillPressed() => pill().copyWith(shadows: [Shadow3(0, 0, 0, 0, withA(p.edgeN, 0)), Shadow3.inset(2, 3, 6, 0, p.sh(.25))]);
  /// .chip .c counter
  ClayDecoration count(Color c) => ClayDecoration(radius: _r(99), fills: [SolidFill(c)]);

  // ---------------------------------------------------------------- segmented control (.seg / .catseg)
  ClayDecoration segTrack() => ClayDecoration(
    radius: _r(R.pill),
    fills: [SolidFill(p.surface2)],
    shadows: [Shadow3.inset(3, 4, 8, 0, p.sh(.2)), Shadow3.inset(-2, -2, 5, 0, p.hi2)],
  );
  ClayDecoration segKey() => ClayDecoration(
    radius: _r(R.pill),
    fills: [LinearFill.vertical([mix(p.surface, .5, p.lift), p.surface], const [0, 1])],
    shadows: [Shadow3(0, 4, 0, 0, p.edgeN), Shadow3(0, 8, 10, -6, p.sh(.35)), Shadow3.inset(0, 2, 1, 0, p.hi)],
  );
  ClayDecoration segKeyOn(Tone t, {bool cat = false}) => ClayDecoration(
    radius: _r(R.pill),
    fills: [LinearFill.vertical([t.tile, t.tile], const [0, 1])],
    shadows: [
      Shadow3(0, 0, 0, 0, withA(p.edgeN, 0)),
      Shadow3(0, 0, 0, -6, p.sh(0)),
      Shadow3.inset(0, 0, 0, 2, cat ? t.mid : p.sage.mid),
      Shadow3.inset(2, 3, 6, 0, withA(cat ? t.deep : p.sage.deep, .35)),
    ],
  );

  // ---------------------------------------------------------------- bottom nav keys
  ClayDecoration navKey() => ClayDecoration(
    radius: _r(18),
    fills: [LinearFill.vertical([mix(p.surface, .45, p.lift), p.surface], const [0, 1])],
    shadows: [Shadow3(0, 4, 0, 0, p.edgeN), Shadow3(0, 8, 10, -8, p.sh(.35)), Shadow3.inset(0, 2, 1, 0, p.hi)],
  );
  ClayDecoration navKeyOn() => ClayDecoration(
    radius: _r(18),
    fills: [LinearFill.vertical([p.sage.tile, p.sage.tile], const [0, 1])],
    shadows: [
      Shadow3(0, 0, 0, 0, withA(p.edgeN, 0)),
      Shadow3(0, 0, 0, -8, p.sh(0)),
      Shadow3.inset(0, 0, 0, 2, p.sage.mid),
      Shadow3.inset(3, 4, 8, 0, withA(p.sage.deep, .32)),
    ],
  );

  // ---------------------------------------------------------------- icons & small raised bits
  /// .badge (--s): glossy tone icon with a thickness edge
  ClayDecoration badge(Tone t, double s) => ClayDecoration(
    radius: _r(s * .32),
    fills: dk
        ? [RadialFill.ellipse(1.2, .9, .3, .18, [_wa(.45), _wa(0)], const [0, .42]), AngleFill(155, [t.deep, t.mid], const [0, 1])]
        : [RadialFill.ellipse(1.2, .9, .3, .18, [_wa(.62), _wa(0)], const [0, .42]), AngleFill(155, [t.mid, t.deep], const [0, 1])],
    shadows: dk
        ? [Shadow3.inset(0, 2, 2, 0, _wa(.4)), Shadow3.inset(0, -3, 5, 0, _ka(.14)), Shadow3(0, 3, 0, 0, mix(t.deep, .45, _k)), Shadow3(0, 8, 12, -5, _ka(.55))]
        : [Shadow3.inset(0, 2, 2, 0, _wa(.55)), Shadow3.inset(0, -3, 5, 0, _ka(.14)), Shadow3(0, 3, 0, 0, mix(t.deep, .72, _k)), Shadow3(0, 8, 12, -5, withA(t.deep, .55))],
  );

  /// .thumb / .qnum / .mring: raised tone knob
  ClayDecoration knob(Tone? t, {double radius = 15}) {
    final tile = t?.tile ?? p.surface, deep = t?.deep ?? _defD;
    final edge = t == null ? mix(const Color(0xFFD9C3A8), .55, const Color(0xFF8C6A4C)) : t.edge(dk);
    return ClayDecoration(
      radius: _r(radius),
      fills: [RadialFill.circle(.35, .28, [mix(tile, .45, p.lift), tile], const [0, .66])],
      shadows: [Shadow3(0, 3, 0, 0, edge), Shadow3(0, 7, 10, -6, dk ? _ka(.55) : withA(deep, .45)), Shadow3.inset(0, 2, 2, 0, p.hi)],
    );
  }

  /// .cat .go
  ClayDecoration goBtn(Tone t) => ClayDecoration(
    radius: _r(99),
    fills: [RadialFill.circle(.35, .28, [p.lift, p.surface], const [0, .62])],
    shadows: [Shadow3(0, 3, 0, 0, t.edge(dk)), Shadow3(0, 7, 10, -6, dk ? _ka(.55) : withA(t.deep, .45)), Shadow3.inset(0, 2, 2, 0, p.hi)],
  );

  /// .cat .cnts span
  ClayDecoration cnt(Tone t) => ClayDecoration(
    radius: _r(99),
    fills: [SolidFill(withA(p.surface, .72))],
    shadows: [Shadow3.inset(0, 1, 1, 0, p.hi), Shadow3(0, 2, 0, 0, withA(t.mid, .6))],
  );

  /// .bar track ([onTile] = color-mix(surface 60%, transparent) inside tiles)
  ClayDecoration barTrack({bool onTile = false, double radius = 99}) => ClayDecoration(
    radius: _r(radius),
    fills: [SolidFill(onTile ? withA(p.surface, .6) : p.surface2)],
    shadows: [Shadow3.inset(1, 2, 4, 0, p.sh(.25)), Shadow3.inset(-1, -1, 2, 0, p.hi2)],
  );
  ClayDecoration barFill(Tone t, {double radius = 99}) => ClayDecoration(
    radius: _r(radius),
    fills: [
      LinearFill.vertical(
        dk ? [mix(t.mid, .7, _w), t.mid, mix(t.mid, .75, _k)] : [mix(t.mid, .55, _w), t.mid, mix(t.mid, .7, t.deep)],
        dk ? const [0, .6, 1] : const [0, .55, 1],
      ),
    ],
    shadows: [Shadow3.inset(0, 1, 1, 0, _wa(.55)), Shadow3.inset(0, -1, 2, 0, withA(t.deep, .3))],
  );

  /// .chart .b
  ClayDecoration chartBar(Tone t) => ClayDecoration(
    radius: const BorderRadius.vertical(top: Radius.circular(12), bottom: Radius.circular(10)),
    fills: [LinearFill.vertical([mix(t.mid, .8, _w), t.mid], const [0, 1])],
    shadows: dk
        ? [Shadow3.inset(3, 3, 3, -1, _wa(.3)), Shadow3.inset(-2, -4, 5, 0, _ka(.18)), Shadow3(0, 3, 0, 0, t.edge(dk)), Shadow3(0, 8, 10, -6, _ka(.6))]
        : [Shadow3.inset(3, 3, 3, -1, _wa(.6)), Shadow3.inset(-2, -4, 5, 0, _ka(.10)), Shadow3(0, 3, 0, 0, t.edge(dk)), Shadow3(0, 8, 10, -6, t.deep)],
  );
  ClayDecoration chartBarZero() => ClayDecoration(
    radius: const BorderRadius.vertical(top: Radius.circular(12), bottom: Radius.circular(10)),
    fills: [SolidFill(p.surface2)],
    shadows: [Shadow3.inset(1, 2, 4, 0, p.sh(.2))],
  );

  /// debossed wells (.search .field .acc .mcolb)
  ClayDecoration well({double radius = R.md, Color? fill}) => ClayDecoration(
    radius: _r(radius),
    fills: [SolidFill(fill ?? p.surface)],
    shadows: [Shadow3.inset(2, 3, 7, 0, p.sh(.18)), Shadow3.inset(-2, -2, 4, 0, p.hi2)],
  );

  /// bottom sheet
  ClayDecoration sheet() => ClayDecoration(
    radius: const BorderRadius.vertical(top: Radius.circular(32)),
    fills: [LinearFill.vertical([mix(p.bg, .6, p.lift), p.bg, p.bg], const [0, .3, 1])],
    shadows: [Shadow3(0, -14, 30, -10, p.sh(.35)), Shadow3.inset(0, 8, 12, -6, p.hi)],
  );

  // ---------------------------------------------------------------- exam player (clay3d.css overrides of the Warsay card rules)
  /// small raised key (.mrow .mch .mslot .qlink): 0 3 0 edge, soft drop, top highlight
  ClayDecoration raised(Color fill, {double radius = R.md, Color? edge, List<Shadow3> extra = const []}) => ClayDecoration(
    radius: _r(radius),
    fills: [SolidFill(fill)],
    shadows: [Shadow3(0, 3, 0, 0, edge ?? p.edgeN), Shadow3(0, 7, 10, -7, p.sh(.35)), Shadow3.inset(0, 2, 1, 0, p.hi), ...extra],
  );

  /// .tips li / .simq / .model / .note
  ClayDecoration raisedSoft(Color fill, {double radius = R.sm}) => ClayDecoration(
    radius: _r(radius),
    fills: [SolidFill(fill)],
    shadows: [Shadow3(0, 3, 0, 0, withA(p.edgeN, .7)), Shadow3(0, 7, 10, -7, p.sh(.35)), Shadow3.inset(0, 2, 1, 0, p.hi)],
  );

  /// tone row with a 2px inner ring (.mrow.ok / .bad / .rev, .mslot.sel)
  ClayDecoration ringed(Tone t, {double radius = R.md}) => ClayDecoration(
    radius: _r(radius),
    fills: [SolidFill(t.tile)],
    shadows: [Shadow3(0, 6, 12, -6, p.ti(.3)), Shadow3.inset(0, 0, 0, 2, t.mid)],
  );

  /// flat fill (.tag)
  ClayDecoration flat(Color c, {double radius = 10}) => ClayDecoration(radius: _r(radius), fills: [SolidFill(c)]);

  /// .opt states: '' | sel | correct | wrong | dim
  ClayDecoration opt(String st, {double radius = R.md}) {
    final r = _r(radius);
    switch (st) {
      case 'sel':
        return ClayDecoration(radius: r, fills: [SolidFill(p.blue.tile)], shadows: [Shadow3.inset(0, 0, 0, 2, p.blue.mid), Shadow3.inset(3, 5, 9, 0, withA(p.blue.deep, .3))]);
      case 'wrong':
        return ClayDecoration(radius: r, fills: [SolidFill(p.peach.tile)], shadows: [Shadow3.inset(0, 0, 0, 2, p.peach.mid), Shadow3.inset(3, 5, 9, 0, withA(p.peach.deep, .35))]);
      case 'correct':
        return ClayDecoration(
          radius: r,
          fills: [LinearFill.vertical([mix(p.sage.tile, .5, p.lift), p.sage.tile, p.sage.tile], const [0, .6, 1])],
          shadows: [
            Shadow3(0, 4, 0, 0, mix(p.sage.mid, .55, p.sage.deep)),
            Shadow3(0, 10, 14, -8, withA(p.sage.deep, .55)),
            Shadow3.inset(0, 0, 0, 2, p.sage.mid),
            Shadow3.inset(3, 4, 7, -3, p.hi),
          ],
        );
      case 'dim':
        return ClayDecoration(
          radius: r,
          fills: [LinearFill.vertical([mix(p.surface2, .5, p.lift), p.surface2, p.surface2], const [0, .6, 1])],
          shadows: [Shadow3(0, 2, 0, 0, p.edgeN), Shadow3.inset(0, 1, 1, 0, p.hi)],
        );
      default:
        return ClayDecoration(
          radius: r,
          fills: [LinearFill.vertical([mix(p.surface2, .5, p.lift), p.surface2, p.surface2], const [0, .6, 1])],
          shadows: [Shadow3(0, 4, 0, 0, p.edgeN), Shadow3(0, 10, 14, -8, p.sh(.35)), Shadow3.inset(3, 4, 7, -3, p.hi), Shadow3.inset(-3, -4, 7, -4, p.sh(.10))],
        );
    }
  }

  ClayDecoration optPressed({double radius = R.md}) => opt('', radius: radius).copyWith(shadows: [Shadow3(0, 0, 0, 0, withA(p.edgeN, 0)), Shadow3.inset(3, 4, 8, 0, p.sh(.22))]);

  /// .opt .l letter disc
  ClayDecoration optLetter(String st) {
    final c = switch (st) {
      'correct' => p.sage.deep,
      'wrong' => p.peach.deep,
      'sel' => p.blue.deep,
      _ => null,
    };
    if (c == null) {
      return ClayDecoration(
        radius: _r(99),
        fills: [RadialFill.circle(.35, .28, [p.lift, p.surface], const [0, .70])],
        shadows: [Shadow3(0, 3, 0, 0, p.edgeN), Shadow3(0, 5, 7, -4, p.sh(.4)), Shadow3.inset(0, 2, 2, 0, p.hi)],
      );
    }
    return ClayDecoration(
      radius: _r(99),
      fills: [RadialFill.circle(.35, .28, [mix(c, .55, _w), c], const [0, .68])],
      shadows: [Shadow3(0, 3, 0, 0, mix(c, .7, _k)), Shadow3.inset(0, 2, 2, 0, _wa(.35))],
    );
  }

  /// .verdict
  ClayDecoration verdict(Tone t) => ClayDecoration(radius: _r(R.md), fills: [SolidFill(t.tile)], shadows: [Shadow3(0, 8, 14, -10, p.sh(.5)), Shadow3.inset(3, 4, 7, -3, p.hi)]);

  /// .steps li:before
  ClayDecoration stepDot() => ClayDecoration(radius: _r(99), fills: [SolidFill(p.sage.tile)], shadows: [Shadow3(0, 2, 0, 0, mix(p.sage.mid, .6, p.sage.deep)), Shadow3.inset(0, 1, 1, 0, p.hi)]);

  /// .palette button
  ClayDecoration palKey(Color fill, {bool cur = false}) => ClayDecoration(
    radius: _r(10),
    fills: [cur ? SolidFill(fill) : LinearFill.vertical([mix(fill, .5, p.lift), fill], const [0, 1])],
    shadows: cur ? [Shadow3.inset(0, 0, 0, 2, p.blue.deep)] : [Shadow3(0, 3, 0, 0, p.edgeN), Shadow3.inset(0, 1, 1, 0, p.hi)],
  );

  /// .msg.me
  ClayDecoration msgMe() => ClayDecoration(
    radius: const BorderRadius.only(topLeft: Radius.circular(22), topRight: Radius.circular(22), bottomLeft: Radius.circular(22), bottomRight: Radius.circular(8)),
    fills: [LinearFill.vertical([p.blue.mid, mix(p.blue.mid, .75, p.blue.deep)], const [0, 1])],
    shadows: [Shadow3(0, 6, 12, -6, p.ti(.3)), Shadow3.inset(0, 2, 1, 0, _wa(.35))],
  );

  /// .msg.bot (puffy card, 8px bottom-left corner)
  ClayDecoration msgBot({Tone? t}) => ClayDecoration(
    radius: const BorderRadius.only(topLeft: Radius.circular(22), topRight: Radius.circular(22), bottomRight: Radius.circular(22), bottomLeft: Radius.circular(8)),
    fills: puffyFill(t?.tile ?? p.surface, t?.deep ?? _defD),
    shadows: puffyShadows(t?.deep ?? _defD),
  );
}

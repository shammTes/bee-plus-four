// Design tokens from the Warsay Prep template (:root / [data-theme="dark"]) plus High's 3D clay variables
// (design/clay3d.css). Keep in sync with those two files.
import 'package:flutter/widgets.dart';

/// color-mix(in srgb, a p, b) with premultiplied alpha, as browsers do it.
Color mix(Color a, double p, Color b) {
  final q = 1 - p;
  final aa = a.a * p + b.a * q;
  if (aa == 0) return const Color(0x00000000);
  double ch(double x, double y) => (x * a.a * p + y * b.a * q) / aa;
  return Color.from(alpha: aa, red: ch(a.r, b.r), green: ch(a.g, b.g), blue: ch(a.b, b.b));
}

Color withA(Color c, double a) => c.withValues(alpha: a);
const transparent = Color(0x00000000);
const white = Color(0xFFFFFFFF);
const black = Color(0xFF000000);

/// CSS `transparent` inside a gradient next to colour c (browsers interpolate premultiplied, so it is c at alpha 0)
Color clear(Color c) => withA(c, 0);

/// `.t-<tone>`: --tile / --mid / --deep
class Tone {
  final String name;
  final Color tile, mid, deep;
  const Tone(this.name, this.tile, this.mid, this.deep);

  /// --tone-edge: light = mix(mid 55%, deep); dark = mix(tile 55%, #000)
  Color edge(bool dark) => dark ? mix(tile, .55, black) : mix(mid, .55, deep);
}

class Palette {
  final bool dark;
  final Color desk, bg, surface, surface2, line, ink, ink2, ink3;
  final Tone sage, peach, butter, blue, lilac, rose, mint;
  final Color coral, coral2, onCoral;
  final Color tint; // --shadow-tint (Warsay --clay shadows)
  final Color hi, hi2, lift, shade, edgeN, coralEdge, avatarEdge; // 3D layer
  final List<Color> phone;

  const Palette._({
    required this.dark,
    required this.desk,
    required this.bg,
    required this.surface,
    required this.surface2,
    required this.line,
    required this.ink,
    required this.ink2,
    required this.ink3,
    required this.sage,
    required this.peach,
    required this.butter,
    required this.blue,
    required this.lilac,
    required this.rose,
    required this.mint,
    required this.coral,
    required this.coral2,
    required this.onCoral,
    required this.tint,
    required this.hi,
    required this.hi2,
    required this.lift,
    required this.shade,
    required this.edgeN,
    required this.coralEdge,
    required this.avatarEdge,
    required this.phone,
  });

  static const light = Palette._(
    dark: false,
    desk: Color(0xFFEFE5D6),
    bg: Color(0xFFF7F0E5),
    surface: Color(0xFFFFFAF2),
    surface2: Color(0xFFF3EADC),
    line: Color.fromRGBO(120, 90, 60, .10),
    ink: Color(0xFF3E3129),
    ink2: Color(0xFF6F6055),
    ink3: Color(0xFFA3938A),
    sage: Tone('sage', Color(0xFFDCEBD5), Color(0xFFA9CBA4), Color(0xFF5B8C63)),
    peach: Tone('peach', Color(0xFFFADAD0), Color(0xFFF4A58E), Color(0xFFD56A50)),
    butter: Tone('butter', Color(0xFFFBEBC1), Color(0xFFF5D27A), Color(0xFFB08316)),
    blue: Tone('blue', Color(0xFFDCE7F2), Color(0xFFA8C4E0), Color(0xFF4F7BA6)),
    lilac: Tone('lilac', Color(0xFFE8DFF4), Color(0xFFC6B3E3), Color(0xFF8466B5)),
    rose: Tone('rose', Color(0xFFF8DCE3), Color(0xFFEDAFBF), Color(0xFFBD5577)),
    mint: Tone('mint', Color(0xFFD5EEE9), Color(0xFF9FD6CB), Color(0xFF3C8C7D)),
    coral: Color(0xFFEE7B5F),
    coral2: Color(0xFFF59A7F),
    onCoral: Color(0xFFFFFFFF),
    tint: Color.fromRGBO(120, 85, 55, 1),
    hi: Color.fromRGBO(255, 255, 255, .78),
    hi2: Color.fromRGBO(255, 255, 255, .5),
    lift: Color(0xFFFFFFFF),
    shade: Color.fromRGBO(120, 85, 55, 1),
    edgeN: Color(0xFFE5D5BF),
    coralEdge: Color(0xFFC65A40),
    avatarEdge: Color(0xFF467550),
    phone: [Color(0xFFFBF5EC), Color(0xFFF7F0E5), Color(0xFFF2E9DB)],
  );

  static const darkP = Palette._(
    dark: true,
    desk: Color(0xFF15110E),
    bg: Color(0xFF211C18),
    surface: Color(0xFF2C2621),
    surface2: Color(0xFF362F29),
    line: Color.fromRGBO(255, 235, 210, .07),
    ink: Color(0xFFF4EADC),
    ink2: Color(0xFFCDBFB0),
    ink3: Color(0xFF978A7D),
    sage: Tone('sage', Color(0xFF33433A), Color(0xFF7FAF84), Color(0xFFA9D4AB)),
    peach: Tone('peach', Color(0xFF4B3530), Color(0xFFD98C77), Color(0xFFF5AE99)),
    butter: Tone('butter', Color(0xFF4A4029), Color(0xFFD4B25E), Color(0xFFF3D27F)),
    blue: Tone('blue', Color(0xFF2F3D4C), Color(0xFF7EA2C8), Color(0xFFA9C8EA)),
    lilac: Tone('lilac', Color(0xFF3E3549), Color(0xFFA08BC6), Color(0xFFCDB8EE)),
    rose: Tone('rose', Color(0xFF4A323A), Color(0xFFC98699), Color(0xFFF0B3C3)),
    mint: Tone('mint', Color(0xFF2D4541), Color(0xFF6FB3A6), Color(0xFFA2DCD1)),
    coral: Color(0xFFE9826A),
    coral2: Color(0xFFF09A83),
    onCoral: Color(0xFF2A1B16),
    tint: Color.fromRGBO(0, 0, 0, 1),
    hi: Color.fromRGBO(255, 236, 214, .10),
    hi2: Color.fromRGBO(255, 236, 214, .06),
    lift: Color(0xFF5A4E44),
    shade: Color.fromRGBO(0, 0, 0, 1),
    edgeN: Color(0xFF15110E),
    coralEdge: Color(0xFFA85A44),
    avatarEdge: Color(0xFF2F4A36),
    phone: [Color(0xFF27211C), Color(0xFF211C18), Color(0xFF1B1714)],
  );

  List<Tone> get tones => [sage, peach, butter, blue, lilac, rose, mint];

  Tone tone(String name) => switch (name) {
    'sage' => sage,
    'peach' => peach,
    'butter' => butter,
    'blue' => blue,
    'lilac' => lilac,
    'rose' => rose,
    'mint' => mint,
    _ => sage,
  };

  /// rgba(var(--shade), a)
  Color sh(double a) => withA(shade, a);

  /// rgba(var(--shadow-tint), a)
  Color ti(double a) => withA(tint, a);

  /// CSS custom property lookup for inline SVG art: var(--sage) etc.
  Color? cssVar(String name) => switch (name) {
    'bg' => bg,
    'surface' => surface,
    'surface-2' => surface2,
    'ink' => ink,
    'ink-2' => ink2,
    'ink-3' => ink3,
    'coral' => coral,
    _ => () {
      final m = RegExp(r'^(sage|peach|butter|blue|lilac|rose|mint)(?:-(2|3))?$').firstMatch(name);
      if (m == null) return null;
      final t = tone(m[1]!);
      return m[2] == null ? t.tile : (m[2] == '2' ? t.mid : t.deep);
    }(),
  };
}

/// Radii (CSS --r-*)
class R {
  static const xl = 28.0, lg = 24.0, md = 18.0, sm = 14.0, pill = 999.0;
}

/// Nunito, bundled under a High-only family name so it cannot clash with the host app.
const kFont = 'HighNunito';

/// [normal] = CSS `line-height: normal` (Nunito: ascent + descent = 1.364 em).
/// CSS `line-height: normal` as Chrome computes it for Nunito: round(ascent) + round(descent) (1011 / 353 per 1000 em)
double chromeNormal(double size) => ((size * 1.011).roundToDouble() + (size * .353).roundToDouble()) / size;

/// bundled math/symbol fallback (Greek, arrows incl. ⇌, super/subscripts, operators …) – see tool/build_symbols.py
const kSymbolFallback = ['HighSymbols', 'HighSymbols2', 'HighSymbols3', 'HighGeez'];

TextStyle ts(double size, FontWeight w, Color color, {double? height, double? spacing, FontStyle? style, TextDecoration? decoration}) => TextStyle(
  inherit: false,
  fontFamily: kFont,
  fontFamilyFallback: kSymbolFallback,
  fontSize: size,
  fontWeight: w,
  color: color,
  height: height ?? chromeNormal(size),
  letterSpacing: spacing,
  fontStyle: style ?? FontStyle.normal,
  textBaseline: TextBaseline.alphabetic,
  decoration: decoration ?? TextDecoration.none,
  decorationColor: color,
  leadingDistribution: TextLeadingDistribution.even,
);

/// Chrome line boxes: a fixed line-height makes every line exactly size × line-height (forced strut).
StrutStyle strutOf(TextStyle s) => StrutStyle(
  fontFamily: kFont,
  fontSize: s.fontSize,
  height: s.height,
  leadingDistribution: TextLeadingDistribution.even,
  fontWeight: s.fontWeight,
  forceStrutHeight: s.height != null && (s.height! - chromeNormal(s.fontSize!)).abs() > 1e-9,
);

const w600 = FontWeight.w600, w700 = FontWeight.w700, w800 = FontWeight.w800, w900 = FontWeight.w900;

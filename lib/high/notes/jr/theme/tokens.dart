// Ported from Junior (junior_flutter/lib/junior/theme/tokens.dart) by tool/port_junior_notes.py; High glue edits marked "High:".
// Design tokens copied from the web template CSS (:root and [data-theme="dark"]). Keep the two in sync.
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

class Tone {
  final Color tile, mid, deep;
  const Tone(this.tile, this.mid, this.deep);

  /// --tone-edge: light = mix(mid 55%, deep); dark = mix(tile 55%, #000)
  Color edge(bool dark) => dark ? mix(tile, .55, black) : mix(mid, .55, deep);
}

class Palette {
  final bool dark;
  final Color desk, bg, surface, surface2, line, ink, ink2;
  final Tone sage, peach, butter, blue, mint, lilac;
  final Color primary, primary2, onPrimary;
  final Color hi, hi2, lift, shade, edgeN, primaryEdge;
  final List<Color> phone; // .phone background gradient (3 stops at 0, 45/50, 100 %)
  final Color jumpBg;

  const Palette._({
    required this.dark,
    required this.desk,
    required this.bg,
    required this.surface,
    required this.surface2,
    required this.line,
    required this.ink,
    required this.ink2,
    required this.sage,
    required this.peach,
    required this.butter,
    required this.blue,
    required this.mint,
    required this.lilac,
    required this.primary,
    required this.primary2,
    required this.onPrimary,
    required this.hi,
    required this.hi2,
    required this.lift,
    required this.shade,
    required this.edgeN,
    required this.primaryEdge,
    required this.phone,
    required this.jumpBg,
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
    sage: Tone(Color(0xFFDCEBD5), Color(0xFFA9CBA4), Color(0xFF5B8C63)),
    peach: Tone(Color(0xFFFADAD0), Color(0xFFF4A58E), Color(0xFFD56A50)),
    butter: Tone(Color(0xFFFBEBC1), Color(0xFFF5D27A), Color(0xFFB08316)),
    blue: Tone(Color(0xFFDCE7F2), Color(0xFFA8C4E0), Color(0xFF4F7BA6)),
    mint: Tone(Color(0xFFD5EEE9), Color(0xFF9FD6CB), Color(0xFF3C8C7D)),
    lilac: Tone(Color(0xFFE8DFF4), Color(0xFFC6B3E3), Color(0xFF8466B5)),
    primary: Color(0xFFEE7B5F),
    primary2: Color(0xFFF59A7F),
    onPrimary: Color(0xFFFFFFFF),
    hi: Color.fromRGBO(255, 255, 255, .78),
    hi2: Color.fromRGBO(255, 255, 255, .5),
    lift: Color(0xFFFFFFFF),
    shade: Color.fromRGBO(120, 85, 55, 1),
    edgeN: Color(0xFFE5D5BF),
    primaryEdge: Color(0xFFC65A40),
    phone: [Color(0xFFFBF5EC), Color(0xFFF7F0E5), Color(0xFFF2E9DB)],
    jumpBg: Color(0xFFF7F0E5),
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
    sage: Tone(Color(0xFF33433A), Color(0xFF7FAF84), Color(0xFFA9D4AB)),
    peach: Tone(Color(0xFF4B3530), Color(0xFFD98C77), Color(0xFFF5AE99)),
    butter: Tone(Color(0xFF4A4029), Color(0xFFD4B25E), Color(0xFFF3D27F)),
    blue: Tone(Color(0xFF2F3D4C), Color(0xFF7EA2C8), Color(0xFFA9C8EA)),
    mint: Tone(Color(0xFF2D4541), Color(0xFF6FB3A6), Color(0xFFA2DCD1)),
    lilac: Tone(Color(0xFF3E3549), Color(0xFFA08BC6), Color(0xFFCDB8EE)),
    primary: Color(0xFFE9826A),
    primary2: Color(0xFFF09A83),
    onPrimary: Color(0xFF2A1B16),
    hi: Color.fromRGBO(255, 236, 214, .10),
    hi2: Color.fromRGBO(255, 236, 214, .06),
    lift: Color(0xFF5A4E44),
    shade: Color.fromRGBO(0, 0, 0, 1),
    edgeN: Color(0xFF15110E),
    primaryEdge: Color(0xFFA85A44),
    phone: [Color(0xFF27211C), Color(0xFF211C18), Color(0xFF1B1714)],
    jumpBg: Color(0xFF211C18),
  );

  Tone tone(String name) => switch (name) {
    'sage' => sage,
    'peach' => peach,
    'butter' => butter,
    'blue' => blue,
    'mint' => mint,
    'lilac' => lilac,
    _ => sage,
  };

  /// rgba(var(--shade), a)
  Color sh(double a) => withA(shade, a);

  /// CSS custom property lookup used when theming inline SVG icons: var(--lilac-2) etc.
  Color? cssVar(String name) => switch (name) {
    'bg' => bg,
    'surface' => surface,
    'surface-2' => surface2,
    'ink' => ink,
    'ink-2' => ink2,
    'primary' => primary,
    _ => () {
      final m = RegExp(r'^(sage|peach|butter|blue|mint|lilac)(?:-(2|3))?$').firstMatch(name);
      if (m == null) return null;
      final t = tone(m[1]!);
      return m[2] == null ? t.tile : (m[2] == '2' ? t.mid : t.deep);
    }(),
  };
}

/// High: Junior's notes type sizes × this
const kNoteScale = .82;

/// Radii (CSS --r-*)
class R {
  static const xl = 28.0, lg = 24.0, md = 18.0, pill = 999.0; // High radii
}

/// Font stack: Nunito for Latin, Noto Sans Ethiopic for Ge'ez (the web app's "Junior Ethiopic" is a subset of the same font).
const kFont = 'HighNunito';
const kFontFallback = ['HighSymbols', 'HighSymbols2', 'HighSymbols3'];

/// [normal] = CSS `line-height: normal` (text inside <button>s: the font's own ascent + descent, 1.364 em for Nunito).
TextStyle ts(double size, FontWeight w, Color color, {double height = 1.45, bool normal = false, double? spacing, String? family, FontStyle? style}) =>
    TextStyle(
      inherit: false,
      // High: type scaled for Grade 9-12 readers (Junior's sizes are for Grade 1-8) // never merge a null height (CSS "normal") with the default 1.45
      fontFamily: family ?? kFont,
      fontFamilyFallback: kFontFallback,
      fontSize: size * kNoteScale,
      fontWeight: w,
      color: color,
      height: normal ? null : height,
      letterSpacing: spacing,
      fontStyle: style ?? FontStyle.normal,
      textBaseline: TextBaseline.alphabetic,
      decoration: TextDecoration.none,
      leadingDistribution: TextLeadingDistribution.even,
    );

/// font-weight 1000 (Nunito's extra-black instance, bundled as its own family)
TextStyle ts1000(double size, Color color, {double height = 1.0}) => ts(size, FontWeight.w900, color, height: height, family: 'HighNunito');

/// Chrome's line boxes: with a fixed line-height every line is exactly (primary font) × line-height, even when the glyphs come
/// from the fallback Ge'ez font -> forced strut. With `line-height: normal` the fallback font's taller metrics do count, but the
/// primary font is still the minimum -> non-forced strut.
StrutStyle strutOf(TextStyle s) => StrutStyle(
  fontFamily: kFont,
  fontSize: s.fontSize,
  height: s.height,
  leadingDistribution: TextLeadingDistribution.even,
  fontWeight: s.fontWeight,
  forceStrutHeight: s.height != null,
);

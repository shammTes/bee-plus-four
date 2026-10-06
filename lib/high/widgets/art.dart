// Icons (`ic()`) and illustrations (`ART.*`) from the web app, themed like the CSS (currentColor, var(--…)).
import 'package:flutter/widgets.dart';
import 'package:flutter_svg/flutter_svg.dart';
import 'package:vector_graphics/vector_graphics_compat.dart' show RenderingStrategy;

import '../theme/tokens.dart';
import 'art_data.dart';

String hex(Color c) {
  int ch(double v) => (v * 255).round().clamp(0, 255);
  return '#${[ch(c.r), ch(c.g), ch(c.b)].map((x) => x.toRadixString(16).padLeft(2, '0')).join()}';
}

String themeSvg(String svg, Palette p, Color current) => rgbaToHex(
  svg.replaceAllMapped(RegExp(r'var\(--([\w-]+)\)'), (m) => hex(p.cssVar(m[1]!) ?? current)).replaceAll('currentColor', hex(current)),
);

/// flutter_svg ignores the alpha of `rgba()` paints: rewrite `attr="rgba(r,g,b,a)"` as hex + `<attr>-opacity`
/// (stop-color -> stop-opacity, fill -> fill-opacity, stroke -> stroke-opacity).
String rgbaToHex(String svg) => svg.replaceAllMapped(
  RegExp(r'(stop-color|fill|stroke)="rgba\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*,\s*([\d.]+)\s*\)"'),
  (m) {
    final h = [m[2], m[3], m[4]].map((x) => int.parse(x!).toRadixString(16).padLeft(2, '0')).join();
    final op = m[1] == 'stop-color' ? 'stop-opacity' : '${m[1]}-opacity';
    return '${m[1]}="#$h" $op="${m[5]}"';
  },
);

final Map<String, String> _cache = {};

/// `ic(name)`: 24×24 line icon, stroke 2.2, round caps.
class Ic extends StatelessWidget {
  const Ic(this.name, {super.key, this.size = 20, required this.color, this.strokeWidth = 2.2});
  final String name;
  final double size, strokeWidth;
  final Color color;
  @override
  Widget build(BuildContext context) {
    final k = '$name|${color.toARGB32()}|$strokeWidth';
    final svg = _cache[k] ??=
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="${hex(color)}" stroke-opacity="${color.a.toStringAsFixed(3)}" stroke-width="$strokeWidth" stroke-linecap="round" stroke-linejoin="round">${(kIcons[name] ?? kIcons['book']!).replaceAll('currentColor', hex(color))}</svg>';
    return SizedBox(width: size, height: size, child: SvgPicture.string(svg, width: size, height: size));
  }
}

/// An original illustration (student, plant, kokob, desk, sprout).
class Art extends StatelessWidget {
  const Art(this.name, {super.key, required this.palette, this.width, this.height, this.fit = BoxFit.contain});
  final String name;
  final Palette palette;
  final double? width, height;
  final BoxFit fit;
  @override
  Widget build(BuildContext context) {
    final k = 'art|$name|${palette.dark}';
    final svg = _cache[k] ??= themeSvg(
      (kArt[name] ?? '').replaceFirst('<svg ', '<svg xmlns="http://www.w3.org/2000/svg" ').replaceAll('font-family="Nunito,sans-serif"', 'font-family="$kFont"'),
      palette,
      palette.ink,
    );
    // illustrations are detailed: draw once into a cached raster instead of replaying every path each frame
    return SvgPicture.string(svg, width: width, height: height, fit: fit, renderingStrategy: RenderingStrategy.raster);
  }
}

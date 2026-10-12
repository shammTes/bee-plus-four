// Exam text (web rich()): Unicode text with \( \) \[ \] $$ maths (flutter_math_fork), x^2 / x^(…) superscripts, <u>underline</u>.
// [tex] = stem_tex mode (\\frac drawn as \\dfrac); $…$ inline maths are parsed in every mode. Reuses the notes renderer's parser (notes/jr/notes/rich.dart).
import 'package:flutter/widgets.dart';

import '../notes/jr/notes/rich.dart';
import '../theme/tokens.dart';

class RichTx extends StatelessWidget {
  const RichTx(this.text, {super.key, required this.style, this.tex = false, this.align, this.maxLines});
  final String text;
  final TextStyle style;
  final bool tex;
  final TextAlign? align;
  final int? maxLines;
  @override
  Widget build(BuildContext context) {
    if (maxLines != null) {
      // one-line preview: same split as the full renderer, maths shown as its source without any $ / \( delimiters
      final plain = [for (final (t, m, _) in richSegments(text)) t ?? m!.trim()].join();
      return Text(plain, style: style, maxLines: maxLines, overflow: TextOverflow.ellipsis);
    }
    final p = style.color ?? const Color(0xFF3E3129);
    return RichPara(text, style: style, notes: tex, textAlign: align, colors: RichColors(withA(p, .25), p, p));
  }
}

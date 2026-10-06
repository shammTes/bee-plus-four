// Tutor tokenizer: the same algorithm as tool/build_tutor_index.py (stop words and synonyms come from the index's meta,
// so the two can't drift; test/tutor_index_test.dart checks the samples the builder tokenized).
const _sub = {
  '₀': '0', '₁': '1', '₂': '2', '₃': '3', '₄': '4', '₅': '5', '₆': '6', '₇': '7', '₈': '8', '₉': '9', //
  '⁰': '0', '¹': '1', '²': '2', '³': '3', '⁴': '4', '⁵': '5', '⁶': '6', '⁷': '7', '⁸': '8', '⁹': '9', '⁺': '+', '⁻': '-',
};
final _subRe = RegExp('[₀-₉⁰-⁹⁺⁻¹²³]');
final _split = RegExp('[^a-z0-9\u1200-\u137f]+');
final _half = RegExp('half[- ]life');
final _digit = RegExp('[0-9]');

class TutorText {
  TutorText(this.stop, this.syn);
  final Set<String> stop;
  final Map<String, String> syn;

  static String stem(String w) {
    final n = w.length;
    if (n > 4 && w.endsWith('ies')) return '${w.substring(0, n - 3)}y';
    if (n > 4 && w.endsWith('sses')) return w.substring(0, n - 2);
    if ((n > 4 && w.endsWith('es') && (w.substring(n - 4, n - 2) == 'sh' || w.substring(n - 4, n - 2) == 'ch')) ||
        (n > 3 && w.endsWith('es') && (w[n - 3] == 'x' || w[n - 3] == 'z'))) {
      return w.substring(0, n - 2);
    }
    if (n > 3 && w.endsWith('s') && !w.endsWith('ss') && !w.endsWith('us') && !w.endsWith('is')) return w.substring(0, n - 1);
    return w;
  }

  List<String> tokens(String s) {
    final t = s.replaceAllMapped(_subRe, (m) => _sub[m[0]] ?? m[0]!).toLowerCase().replaceAll(_half, 'halflife');
    final out = <String>[];
    for (final w in t.split(_split)) {
      if (w.isEmpty || stop.contains(w)) continue;
      if (w.length == 1 && !_digit.hasMatch(w)) continue;
      if (w.length > 30) continue;
      out.add(stem(w));
    }
    return out;
  }
}

/// Levenshtein distance, giving up (returning max + 1) as soon as it must exceed [max]
int editDistance(String a, String b, int max) {
  if ((a.length - b.length).abs() > max) return max + 1;
  var prev = List<int>.generate(b.length + 1, (i) => i), cur = List<int>.filled(b.length + 1, 0);
  for (var i = 1; i <= a.length; i++) {
    cur[0] = i;
    var best = cur[0];
    for (var j = 1; j <= b.length; j++) {
      final c = a.codeUnitAt(i - 1) == b.codeUnitAt(j - 1) ? 0 : 1;
      var v = prev[j - 1] + c;
      if (prev[j] + 1 < v) v = prev[j] + 1;
      if (cur[j - 1] + 1 < v) v = cur[j - 1] + 1;
      cur[j] = v;
      if (v < best) best = v;
    }
    if (best > max) return max + 1;
    final t = prev;
    prev = cur;
    cur = t;
  }
  return prev[b.length];
}

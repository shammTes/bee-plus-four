// Every maths segment in the notes the app loads (assets/high/notes/split/<unit>.json, all subjects) parses in
// flutter_math_fork; a parse error falls back to raw TeX on screen. Same rules as lib/high/notes/jr/notes/rich.dart:
// \$ is a literal dollar sign (money), $x$ becomes \(x\), then $$x$$, \[x\] and \(x\) are maths.
// Set NOTES_MATH_REPORT=<file> to write every problem found. (Replaces the chemistry-only test/notes_math_render_test.dart.)
import 'dart:convert';
import 'dart:io';

import 'package:high/high/widgets/rich.dart';
import 'package:flutter/widgets.dart';
import 'package:flutter_math_fork/flutter_math.dart';
import 'package:flutter_test/flutter_test.dart';

final _dollar = RegExp(r'(^|[^$\\])\$([^$\n]+)\$(?!\$)');
final _seg = RegExp(r'\$\$([\s\S]+?)\$\$|\\\[([\s\S]+?)\\\]|\\\(([\s\S]+?)\\\)');

List<String> mathOf(String s) {
  s = s.replaceAll(RegExp(r'(?<!\\)\\\$(?!\$)'), '\uE000');
  s = s.replaceAllMapped(_dollar, (m) => '${m[1]}\\(${m[2]}\\)');
  return [for (final m in _seg.allMatches(s)) (m[1] ?? m[2] ?? m[3])!.replaceAll('\uE000', r'\$')];
}

void walk(Object? x, String path, void Function(String path, String s) f) {
  if (x is String) {
    f(path, x);
  } else if (x is List) {
    for (var i = 0; i < x.length; i++) {
      walk(x[i], '$path[$i]', f);
    }
  } else if (x is Map) {
    final id = x['id'];
    for (final e in x.entries) {
      if (e.key == 'id' || e.key == 'src' || e.key == 'svg') continue;
      walk(e.value, id is String ? '$id.${e.key}' : '$path.${e.key}', f);
    }
  }
}

/// unit id -> problems
Map<String, List<String>> scan() {
  final out = <String, List<String>>{};
  final files = Directory('assets/high/notes/split').listSync().whereType<File>().where((f) => f.path.endsWith('.json')).toList()
    ..sort((a, b) => a.path.compareTo(b.path));
  for (final f in files) {
    final unit = f.uri.pathSegments.last.replaceAll('.json', '');
    final bad = <String>[];
    walk(jsonDecode(f.readAsStringSync()), unit, (path, s) {
      // a JSON-escaping slip turns \frac / \text / \beta into a form feed / TAB / backspace + "rac" / "ext" / "eta"
      if (RegExp(r'[\x08\x0c]|\t(ext|imes|heta|au|riangle)\b|(?<![\\a-z])(rac|ext)\{').hasMatch(s)) bad.add('$path: lost TeX command ${jsonEncode(s)}');
      // money: "from $2 to $34" pairs the two dollar signs into maths "2 to " (write \$2)
      for (final m in _dollar.allMatches(s.replaceAll(RegExp(r'(?<!\\)\\\$(?!\$)'), '\uE000'))) {
        final x = m[2]!;
        if (RegExp(r'^\s*\d').hasMatch(x) && !x.contains(r'\') && RegExp(r'[A-Za-z]{2,}').allMatches(x).length >= 2) {
          bad.add('$path: money taken as maths \$$x\$');
        }
      }
      if (!s.contains(r'$') && !s.contains(r'\(') && !s.contains(r'\[')) return;
      for (final m in mathOf(s)) {
        if (Math.tex(m).parseError != null) bad.add('$path: tex $m');
        // a JSON-escaping slip leaves \\frac etc.; \\ followed by a letter is fine only as a row break inside an environment
        if (RegExp(r'\\\\[a-zA-Z]').hasMatch(m) && !m.contains(r'\begin{')) bad.add('$path: double backslash $m');
      }
    });
    if (bad.isNotEmpty) out[unit] = bad;
  }
  return out;
}

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();

  test('notes of every subject: every maths segment parses', () {
    final bad = scan();
    final out = Platform.environment['NOTES_MATH_REPORT'];
    if (out != null) File(out).writeAsStringSync(const JsonEncoder.withIndent(' ').convert(bad));
    expect(bad, isEmpty, reason: bad.entries.expand((e) => e.value).take(60).join('\n'));
  });

  test('the scanner sees maths and treats \\\$ as money', () {
    expect(mathOf(r'costs \$300 and \$60'), isEmpty);
    expect(mathOf(r'area $x^2$ and $$\frac{a}{b}$$ and \(y\)'), [r'x^2', r'\frac{a}{b}', 'y']);
    // guards the scanner itself: these units are full of \( \) and $$ $$ maths
    for (final u in ['math9-u1', 'chem10-u3']) {
      var n = 0;
      walk(jsonDecode(File('assets/high/notes/split/$u.json').readAsStringSync()), u, (p, s) => n += mathOf(s).length);
      expect(n, greaterThan(20), reason: u);
    }
  });

  testWidgets('\\\$ shows as a plain dollar sign, maths around it still renders', (t) async {
    await t.pumpWidget(Directionality(
      textDirection: TextDirection.ltr,
      child: Column(children: [
        RichTx(r'costs \$300 and \$60 \(x^2\)', style: const TextStyle(fontSize: 14)),
        RichTx(r'$$ \$1,000 \times 25\% $$', style: const TextStyle(fontSize: 14)),
      ]),
    ));
    expect(find.textContaining(r'costs $300 and $60', findRichText: true), findsOneWidget);
    expect(find.textContaining(r'\$', findRichText: true), findsNothing);
    // a formula that fails to parse falls back to its raw TeX as text
    for (final raw in [r'x^2', r'\times', '1,000']) {
      expect(find.textContaining(raw, findRichText: true), findsNothing, reason: raw);
    }
  });
}

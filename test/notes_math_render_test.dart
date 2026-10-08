// Every maths segment in the notes the app loads (assets/high/notes/split/<unit>.json) parses in flutter_math_fork.
// A parse error falls back to raw TeX on screen, which reads as garbage. Same rules as lib/high/notes/jr/notes/rich.dart:
// $x$ becomes \(x\) first, then $$x$$, \[x\] and \(x\) are maths. Same check as test/papers_render_test.dart for exams.
import 'dart:convert';
import 'dart:io';

import 'package:flutter_math_fork/flutter_math.dart';
import 'package:flutter_test/flutter_test.dart';

final _dollar = RegExp(r'(^|[^$\\])\$([^$\n]+)\$(?!\$)');
final _seg = RegExp(r'\$\$([\s\S]+?)\$\$|\\\[([\s\S]+?)\\\]|\\\(([\s\S]+?)\\\)');

List<String> mathOf(String s) {
  s = s.replaceAllMapped(_dollar, (m) => '${m[1]}\\(${m[2]}\\)');
  return [for (final m in _seg.allMatches(s)) (m[1] ?? m[2] ?? m[3])!];
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
      walk(e.value, id is String ? '$id.${e.key}' : '$path.${e.key}', f);
    }
  }
}

/// unit id -> problems
Map<String, List<String>> scan(bool Function(String unitId) which) {
  final out = <String, List<String>>{};
  final files = Directory('assets/high/notes/split').listSync().whereType<File>().where((f) => f.path.endsWith('.json')).toList()
    ..sort((a, b) => a.path.compareTo(b.path));
  for (final f in files) {
    final unit = f.uri.pathSegments.last.replaceAll('.json', '');
    if (!which(unit)) continue;
    final bad = <String>[];
    walk(jsonDecode(f.readAsStringSync()), unit, (path, s) {
      if (!s.contains(r'$') && !s.contains(r'\(') && !s.contains(r'\[')) return;
      for (final m in mathOf(s)) {
        if (Math.tex(m).parseError != null) bad.add('$path: tex $m');
        if (RegExp(r'\\\\[a-zA-Z]').hasMatch(m)) bad.add('$path: double backslash $m');
      }
    });
    if (bad.isNotEmpty) out[unit] = bad;
  }
  return out;
}

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();

  test('chemistry notes: every maths segment parses', () {
    final bad = scan((u) => u.startsWith('chem'));
    expect(bad, isEmpty, reason: bad.entries.expand((e) => e.value).take(40).join('\n'));
  });

  test('the formula cards of the chemistry tutor notes have maths to render', () {
    // guards the scanner itself: the concentration and gas-law notes use \( \) and $$ $$ maths
    var n = 0;
    walk(jsonDecode(File('assets/high/notes/split/chem10-u3.json').readAsStringSync()), 'chem10-u3', (p, s) => n += mathOf(s).length);
    expect(n, greaterThan(20));
  });
}

// Every exam item (assets/high/exams/index.json packs incl. bank_*.json, and matric_lazy/subjects): after the exam renderer's parse (RichTx -> richSegments) no raw
// '$' delimiter is left in the visible text and every formula parses with flutter_math. A literal dollar is written \$.
import 'dart:convert';
import 'dart:io';

import 'package:flutter_math_fork/tex.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:high/high/notes/jr/notes/rich.dart';

final _money = RegExp(r'(?<!\\)\\\$(?!\$)');

void _walk(Object? o, String path, void Function(String, String) f) {
  if (o is String) {
    f(path, o);
  } else if (o is Map) {
    o.forEach((k, v) => _walk(v, '$path.$k', f));
  } else if (o is List) {
    for (var i = 0; i < o.length; i++) {
      _walk(o[i], '$path[$i]', f);
    }
  }
}

/// problems of one string as the Matric screen draws it (empty = fine)
List<String> dollarProblems(String s, {bool notes = false}) {
  final out = <String>[];
  final allowed = _money.allMatches(s).length;
  var shown = 0;
  for (final (text, math, _) in richSegments(s, notes: notes)) {
    if (text != null) shown += '\$'.allMatches(text).length;
    if (math != null) {
      try {
        TexParser(math, const TexParserSettings()).parse();
      } catch (e) {
        out.add('formula does not parse: $math ($e)');
      }
    }
  }
  if (shown > allowed) out.add('raw \$ shown');
  return out;
}

void main() {
  test('no visible \$ delimiter and every formula parses in all matric/exam packs', () {
    // every paper the Matric screen can open: the eager index (bank_*.json and the other packs) + the lazy subject packs
    final idx = jsonDecode(File('assets/high/exams/index.json').readAsStringSync()) as Map;
    final files = [
      for (final e in idx['exams'] as List) File('assets/high/exams/$e'),
      ...Directory('assets/high/exams/matric_lazy/subjects').listSync().whereType<File>().where((f) => f.path.endsWith('.json')),
    ]..sort((a, b) => a.path.compareTo(b.path));
    expect(files, isNotEmpty);
    final bad = <String>[];
    var strings = 0, withMath = 0;
    for (final f in files) {
      final j = jsonDecode(f.readAsStringSync());
      _walk(j, f.path.split('/').last, (path, s) {
        if (!s.contains(r'$') && !s.contains(r'\(') && !s.contains(r'\[')) return;
        strings++;
        if (richSegments(s).any((g) => g.$2 != null)) withMath++;
        for (final p in dollarProblems(s, notes: path.endsWith('.stem_tex'))) {
          bad.add('$path: $p :: ${s.length > 160 ? s.substring(0, 160) : s}');
        }
      });
    }
    // ignore: avoid_print
    print('scanned ${files.length} banks, $strings strings with maths/\$, $withMath with formulas, ${bad.length} problems');
    if (bad.isNotEmpty) File('build/matric_dollar_report.txt').writeAsStringSync(bad.join('\n'));
    expect(bad, isEmpty, reason: bad.take(40).join('\n'));
  });

  test('renderer rules', () {
    expect(dollarProblems(r'Cost is \$20 and $x^2$ and $$\frac{1}{2}$$'), isEmpty);
    expect(dollarProblems(r'broken $$x'), isNotEmpty);
    expect(richSegments(r'area $a^2$').last.$2, 'a^2');
  });
}

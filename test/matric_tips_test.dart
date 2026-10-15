// Every matric / model question has a 'How to answer' tip and at least one similar question with a keyed answer.
//   flutter test test/matric_tips_test.dart
import 'dart:convert';
import 'dart:io';

import 'package:flutter_test/flutter_test.dart';

void main() {
  test('every matric question has tips and similar questions', () {
    final idx = jsonDecode(File('assets/high/exams/index.json').readAsStringSync()) as Map;
    var n = 0;
    final bad = <String>[];
    for (final f in (idx['exams'] as List).cast<String>()) {
      final d = jsonDecode(File('assets/high/exams/$f').readAsStringSync()) as Map;
      for (final q in (d['questions'] as List).cast<Map>()) {
        n++;
        final tips = q['tips'] as List?, sim = q['similar_questions'] as List?;
        if (tips == null || tips.isEmpty || sim == null || sim.isEmpty) {
          bad.add(q['id'] as String);
          continue;
        }
        for (final s in sim.cast<Map>()) {
          expect((s['stem'] as String?)?.isNotEmpty, isTrue, reason: '${q['id']} similar stem');
          expect('${s['answer'] ?? ''}'.isNotEmpty, isTrue, reason: '${q['id']} similar answer');
          final o = s['options'];
          if (o is Map && s['from'] != null) expect(o.containsKey(s['answer']), isTrue, reason: '${q['id']} similar answer not an option');
        }
      }
    }
    expect(n, greaterThan(10000));
    expect(bad, isEmpty, reason: '${bad.length} questions without tips / similar questions, e.g. ${bad.take(5)}');
  });
}

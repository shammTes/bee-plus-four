// notes unit -> matric/model question links (assets/high/notes/unit_questions.json, tools/map_unit_questions.py)
// and notes unit -> exercise links resolve against what ExamRepo actually loads
import 'dart:convert';
import 'dart:io';

import 'package:flutter_test/flutter_test.dart';
import 'package:high/high/data/repository.dart';

const family = {
  'Agriculture': ['agriculture'],
  'Biology': ['biology'],
  'Business and Economics': ['business_economics'],
  'Chemistry': ['chemistry'],
  'English': ['english'],
  'Geography': ['geography'],
  'History': ['history'],
  'Mathematics': ['mathematics'],
  'Physics': ['physics'],
  'Social Studies': ['history', 'geography', 'business_economics'],
  'General Science': ['biology', 'chemistry', 'physics'],
  'General Knowledge': ['history', 'geography', 'biology', 'chemistry', 'physics', 'agriculture', 'business_economics'],
};

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();
  test('unit_questions + exercise units resolve to loaded questions of the right subject', () async {
    final unitSubject = <String, String>{};
    for (final name in ['index.json', 'english_index.json']) {
      final f = File('assets/high/notes/notes/$name');
      if (!f.existsSync()) continue;
      final idx = jsonDecode(f.readAsStringSync()) as Map<String, dynamic>;
      for (final g in (idx['grades'] as Map).values) {
        (g as Map).forEach((subj, b) {
          for (final u in (b as Map)['units'] as List) {
            unitSubject.putIfAbsent((u as Map)['id'] as String, () => subj as String);
          }
        });
      }
    }
    final raw = File('assets/high/notes/unit_questions.json').readAsStringSync();
    final uq = jsonDecode(raw) as Map<String, dynamic>;
    expect(raw, jsonEncode(uq), reason: 'unit_questions.json should stay compact');
    final r = ExamRepo(useIsolate: false);
    await r.init();
    var linked = 0;
    (uq['units'] as Map).forEach((unit, list) {
      expect(unitSubject.containsKey(unit), isTrue, reason: 'unknown unit $unit');
      final seen = <String>{};
      for (final m in (list as List).cast<Map<String, dynamic>>()) {
        final id = m['id'] as String;
        expect(seen.add(id), isTrue, reason: 'duplicate $id in $unit');
        final q = r.byId[id];
        expect(q, isNotNull, reason: 'dangling $id in $unit');
        expect(family[q!.exam.subject], contains(unitSubject[unit]), reason: '$id (${q.exam.subject}) linked to $unit');
        expect(q.isScored || q.type != 'mcq', isTrue, reason: '$id has no usable key');
        linked++;
      }
    });
    expect(linked, greaterThan(10000));
    r.exerciseUnits.forEach((k, ids) {
      if (k.startsWith('general|') || RegExp(r'^eng\d+-practice$').hasMatch(k)) return; // untagged items
      expect(unitSubject.containsKey(k), isTrue, reason: 'exercise unit $k is not a notes unit');
      expect(ids.toSet().length, ids.length, reason: 'duplicate exercise ids in $k');
    });
  });
}

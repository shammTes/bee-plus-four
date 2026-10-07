// Every matric / model paper (eager packs + lazy Drive subject packs) loads exactly as the app loads it and has
// renderable questions: non-empty stem (or picture / match list / passage), MCQ options + answer, and every maths
// segment parses in flutter_math_fork (a parse error falls back to raw TeX in the app, which reads as garbage).
import 'dart:convert';
import 'dart:io';

import 'package:flutter/services.dart';
import 'package:flutter_math_fork/flutter_math.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:high/high/data/models.dart';
import 'package:high/high/data/repository.dart';

final _seg = RegExp(r'\$\$([\s\S]+?)\$\$|\\\[([\s\S]+?)\\\]|\\\(([\s\S]+?)\\\)');

List<String> mathOf(String s) => [for (final m in _seg.allMatches(s)) (m[1] ?? m[2] ?? m[3])!];

List<String> problems(Question q) {
  final out = <String>[];
  final stem = q.isMatch ? q.matchPrompt : q.stem;
  if (stem.trim().isEmpty && (q.stemTex ?? '').trim().isEmpty && q.image == null && q.passageId == null && q.subparts.isEmpty) out.add('blank stem');
  if (q.type == 'mcq' && !q.isMCQ) out.add('mcq without options');
  if (q.isMCQ) {
    // a known gap in the source paper is allowed when the question says so (review flag)
    if (q.options!.values.any((v) => v.trim().isEmpty) && q.reviewFlag == null) out.add('empty option');
    if (!q.options!.containsKey(q.answer) && !q.accepted.any(q.options!.containsKey)) out.add('answer not an option');
  }
  for (final t in [stem, ...q.opts.values]) {
    for (final m in mathOf(t)) {
      final w = Math.tex(m);
      if (w.parseError != null) out.add('tex: $m');
      if (RegExp(r'\\\\[a-zA-Z]').hasMatch(m)) out.add('double backslash: $m');
    }
  }
  return out;
}

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();
  test('every paper parses and has renderable questions', () async {
    final repo = ExamRepo(lazyExams: true);
    await repo.init();
    for (final s in [...repo.subjects]) {
      await repo.ensureLazySubject(s);
    }
    await repo.ensureAllExams();
    final report = <String, Object>{};
    final bad = <String>[];
    final dupes = <String, String>{};
    for (final e in repo.exams) {
      // the same paper must not be listed twice (lazy Drive packs used to repeat the eager ones under other ids)
      final sig = ([for (final q in e.questions) q.stem.toLowerCase().replaceAll(RegExp(r'[^a-z0-9]'), '')]..sort()).join('|');
      if (e.questions.length >= 10 && dupes.containsKey(sig)) bad.add('${e.id}: same questions as ${dupes[sig]}');
      dupes[sig] = e.id;
      if (!e.questions.any((q) => q.stem.trim().isNotEmpty || q.image != null)) bad.add('${e.id}: no renderable question');
      for (final q in e.questions) {
        if (q.stem.contains('android_asset')) bad.add('${q.id}: link to a picture that is not shipped');
      }
      final issues = {for (final q in e.questions) q.id: problems(q)}..removeWhere((_, v) => v.isEmpty);
      report[e.id] = {'subject': e.subject, 'year': e.year, 'file': e.file, 'questions': e.questions.length, 'issues': issues};
      if (e.questions.isEmpty) bad.add('${e.id}: no questions');
      for (final x in issues.entries) {
        bad.add('${e.id} ${x.key}: ${x.value.join('; ')}');
      }
    }
    final out = Platform.environment['PAPER_REPORT'];
    if (out != null) File(out).writeAsStringSync(const JsonEncoder.withIndent(' ').convert(report));
    expect(repo.exams, isNotEmpty);
    expect(bad, isEmpty, reason: bad.take(40).join('\n'));
  });
}

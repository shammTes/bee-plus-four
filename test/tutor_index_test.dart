// Tutor: the committed index matches its sources, the Dart tokenizer matches the builder, search finds the right
// content for questions from every subject and grade, answers resolve to real notes cards / questions, and the chat UI
// answers and deep-links into the notes. Regenerate the index with:  python3 tool/build_tutor_index.py
import 'dart:convert';
import 'dart:io';

import 'package:crypto/crypto.dart';
import 'package:flutter/widgets.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:high/high/app.dart';
import 'package:high/high/data/repository.dart';
import 'package:high/high/notes/jr/data/notes_models.dart';
import 'package:high/high/notes/jr/data/repository.dart';
import 'package:high/high/notes/jr/screens/unit_page.dart';
import 'package:high/high/state/app_state.dart';
import 'package:high/high/tutor/tutor_answer.dart';
import 'package:high/high/tutor/tutor_index.dart';
import 'package:high/high/tutor/tutor_page.dart';
import 'package:high/high/widgets/page.dart';
import 'package:shared_preferences/shared_preferences.dart';

import 'helpers.dart';

/// the builder's source set (tool/build_tutor_index.py source_files())
List<String> sourceFiles() {
  final out = <String>{};
  void dir(String d) {
    final x = Directory(d);
    if (!x.existsSync()) return;
    for (final f in x.listSync().whereType<File>()) {
      if (f.path.endsWith('.json')) out.add(f.path.replaceAll('\\', '/'));
    }
  }

  for (final d in [
    'assets/high/notes/notes',
    'assets/high/exams',
    'assets/high/exams/matric_lazy/subjects',
    'assets/high/exercises',
    'assets/high/exercises/school',
  ]) {
    dir(d);
  }
  for (final f in [
    'assets/high/notes/unit_questions.json',
    'assets/high/media/placements.json',
    'assets/high/media/taxonomy_extra.json',
    'assets/high/media/g11_extra.json',
    'assets/high/media/commons_extra.json',
    'tool/build_tutor_index.py',
  ]) {
    if (File(f).existsSync()) out.add(f);
  }
  return out.toList()..sort();
}

void main() {
  late TutorIndex ix;
  final repo = ExamRepo(useIsolate: false);
  final notes = NotesRepo(useIsolate: false);
  setUpAll(() async {
    TestWidgetsFlutterBinding.ensureInitialized();
    await repo.init();
    await notes.init();
    final sw = Stopwatch()..start();
    ix = TutorIndex.decode(File(TutorIndex.asset).readAsBytesSync());
    // ignore: avoid_print
    print(
      'tutor index: ${(File(TutorIndex.asset).lengthSync() / 1e6).toStringAsFixed(2)} MB, ${ix.length} docs, ${ix.terms.length} terms, decoded in ${sw.elapsedMilliseconds} ms',
    );
  });

  test('committed index is up to date with its sources (else run: python3 tool/build_tutor_index.py)', () {
    final man = jsonDecode(File('tool/tutor_index_sources.json').readAsStringSync()) as Map<String, dynamic>;
    final files = (man['files'] as Map).cast<String, String>();
    final now = sourceFiles();
    final added = now.where((f) => !files.containsKey(f)).toList(), gone = files.keys.where((f) => !now.contains(f)).toList();
    final changed = [
      for (final f in now)
        if (files[f] != null && files[f] != sha256.convert(File(f).readAsBytesSync()).toString().substring(0, 16)) f,
    ];
    final stale = [...added.map((f) => '+ $f'), ...gone.map((f) => '- $f'), ...changed.map((f) => '~ $f')];
    expect(stale, isEmpty, reason: 'Tutor index is stale; regenerate with: python3 tool/build_tutor_index.py\n${stale.take(20).join('\n')}');
    // the manifest digest is the one baked into the index (python json.dumps(sort_keys=True) layout)
    final keys = files.keys.toList()..sort();
    final dump = '{${[for (final k in keys) '"$k": "${files[k]}"'].join(', ')}}';
    expect(sha256.convert(utf8.encode(dump)).toString().substring(0, 16), man['digest']);
    expect(ix.sources, man['digest'], reason: 'assets/high/tutor/tutor_index.bin and tool/tutor_index_sources.json come from different builds');
    final concepts = jsonDecode(File(TutorIndex.conceptsAsset).readAsStringSync()) as Map;
    expect(concepts['sources'], man['digest'], reason: '${TutorIndex.conceptsAsset} comes from a different build');
  });

  test('Dart tokenizer = builder tokenizer', () {
    for (final s in ix.meta['tokSamples'] as List) {
      expect(ix.text.tokens(s[0] as String), [for (final w in s[1] as List) '$w'], reason: '${s[0]}');
    }
  });

  test('covers every notes book, unit and lesson, the exercise bank and the papers', () {
    final idx = jsonDecode(File('assets/high/notes/notes/index.json').readAsStringSync()) as Map;
    for (final ge in (idx['grades'] as Map).entries) {
      for (final se in (ge.value as Map).entries) {
        for (final u in (se.value as Map)['units'] as List) {
          expect(ix.units.any((x) => x.id == u['id'] && x.grade == int.parse('${ge.key}') && x.subject == se.key), isTrue, reason: '${u['id']}');
        }
      }
    }
    final count = <int, int>{};
    for (var d = 0; d < ix.length; d++) {
      count[ix.kind[d]] = (count[ix.kind[d]] ?? 0) + 1;
    }
    for (final k in [TK.text, TK.worked, TK.glossary, TK.tip, TK.unitQ, TK.media, TK.concept, TK.exercise, TK.school, TK.exam]) {
      expect(count[k] ?? 0, greaterThan(100), reason: 'kind $k');
    }
    expect((count[TK.exercise] ?? 0) + (count[TK.school] ?? 0), greaterThan(12000));
    // every lesson of the Grade 11 per-unit files (unit_phys11-u1.json …) is in
    final u1 = jsonDecode(File('assets/high/notes/notes/unit_phys11-u1.json').readAsStringSync()) as Map;
    for (final l in u1['lessons'] as List) {
      expect(ix.lessons.any((x) => x.id == l['id']), isTrue, reason: '${l['id']}');
    }
  });

  test('sample questions from every subject find the right lesson', () {
    final cases = <(String, String, String)>[
      ('what is refraction', 'physics', 'refraction'),
      ('photosynthesis', 'biology', 'photosynthesis'),
      ('law of demand', 'business_economics', 'demand'),
      ('quadratic formula', 'mathematics', 'quadratic'),
      ('present perfect tense', 'english', 'tense'),
      ('newton second law of motion', 'physics', 'newton'),
      ('what is the mole concept', 'chemistry', 'mole'),
      ('soil erosion', 'geography|agriculture', 'erosion'), // both subjects teach soil erosion
      ('causes of the french revolution', 'history', 'revolution'),
      ('stages of mitosis', 'biology', 'mitosis'),
      ('elasticity of demand', 'business_economics', 'elasticity'),
      ('refractoin of light', 'physics', 'refraction'), // typo
      ('photosinthesis', 'biology', 'photosynthesis'), // typo
      ('ohms law', 'physics', 'ohm'),
    ];
    for (final (q, subj, word) in cases) {
      final r = ix.search(q);
      expect(r.explain, isNotEmpty, reason: q);
      final top = r.explain.first.doc;
      expect(subj.split('|'), contains(ix.subjectOf(top)), reason: '$q -> ${ix.keys[top]} (${ix.where(top)})');
      expect(r.explain.take(3).any((h) => ix.keys[h.doc].toLowerCase().contains(word)), isTrue, reason: '$q -> ${[for (final h in r.explain) ix.keys[h.doc]]}');
      expect(r.practice.isNotEmpty || r.matric.isNotEmpty, isTrue, reason: q);
    }
    // Adwa: the notes mention it once; the matric / exercise questions must be on Ethiopian/Eritrean history
    final adwa = ix.search('causes of the Battle of Adwa');
    expect(ix.subjectOf(adwa.matric.first.doc), 'history');
    expect(ix.subjectOf(adwa.practice.first.doc), 'history');
    // filters written in the question, and from the filter row
    final g9 = ix.search('grade 9 physics newton law');
    expect(g9.grade, 9);
    expect(g9.subject, 'physics');
    expect(g9.explain.every((h) => ix.grade[h.doc] == 9 && ix.subjectOf(h.doc) == 'physics'), isTrue);
    final f = ix.search('energy', subject: 'chemistry', grade: 10);
    expect([...f.explain, ...f.practice].every((h) => ix.subjectOf(h.doc) == 'chemistry' && ix.grade[h.doc] == 10), isTrue);
    // a soft focus ranks the student's subject first without hiding the rest
    final focus = ix.search('energy', preferSubject: 'physics', preferGrade: 9);
    expect(ix.subjectOf(focus.explain.first.doc), 'physics');
    expect(ix.search('qwertyuiop zxcvb').empty, isTrue);
    // a subject abbreviation is a filter, not a search word
    final m = ix.search('maths quadratic');
    expect(m.subject, 'mathematics');
    expect(m.explain.every((h) => ix.subjectOf(h.doc) == 'mathematics'), isTrue);
    // Tigrinya glosses in the English books are searchable
    final ti = ix.search('ሓገዝቲ ግሲ');
    expect(ti.explain, isNotEmpty);
    expect(ix.subjectOf(ti.explain.first.doc), 'english');
  });

  test('every subject and grade: unit titles lead to their own unit', () {
    var ok = 0, all = 0;
    final miss = <String>[];
    for (final u in ix.units) {
      if (u.title.trim().length < 4) continue;
      all++;
      final r = ix.search(u.title, subject: u.subject, grade: u.grade);
      if ([...r.explain, ...r.media].take(6).any((h) => ix.unitOf(h.doc)?.id == u.id)) {
        ok++;
      } else {
        miss.add('${u.id} ${u.title}');
      }
    }
    // ignore: avoid_print
    print('unit-title retrieval: $ok / $all${miss.isEmpty ? '' : '; missed: ${miss.take(8).join(' | ')}'}');
    expect(ok / all, greaterThan(.85));
  });

  test('concept texts sidecar: one per concept doc', () {
    final c = TutorIndex.parseConcepts(File(TutorIndex.conceptsAsset).readAsStringSync());
    final docs = [
      for (var d = 0; d < ix.length; d++)
        if (ix.kind[d] == TK.concept) d,
    ];
    expect(c.length, docs.length);
    expect(docs.every((d) => c.containsKey('$d')), isTrue);
    expect(c.values.where((x) => x.$1.trim().isNotEmpty).length, greaterThan(docs.length * .9));
  });

  test('with the app\'s lazy repo the tutor reads only the packs it shows', () async {
    // the app's settings (lib/high/high.dart): exam packs and the Exercise bank are read on demand
    final lazy = ExamRepo(useIsolate: false, lazyExercises: true, lazyExams: true, deferCodes: true);
    await lazy.init();
    expect(lazy.fromSummary, isTrue);
    final before = lazy.exams.where((e) => e.full).length;
    final a = TutorAnswerer(ix, lazy, notes);
    for (final q in ['what is refraction', 'law of demand', 'causes of the Battle of Adwa', 'what is the mole concept']) {
      final r = await a.answer(q);
      expect(r.refuse, isFalse, reason: q);
      expect(r.matric, isNotEmpty, reason: q);
      expect(r.practice, isNotEmpty, reason: q);
      expect([...r.matric, ...r.practice].every((x) => !x.isStub && x.stem.isNotEmpty), isTrue, reason: q);
    }
    final read = lazy.exams.where((e) => e.full).length - before;
    // ignore: avoid_print
    print('lazy repo: 4 answers read $read of ${lazy.exams.length} exam packs, concepts loaded: ${lazy.conceptsLoaded}');
    expect(lazy.allExamsLoaded, isFalse);
    expect(lazy.conceptsLoaded, isFalse);
    expect(read, lessThan(lazy.exams.length ~/ 3));
  });

  test('every lab / media hit deep-links to its card in the notes unit (placements incl. the physics lab sims)', () async {
    var sims = 0;
    final bad = <String>[];
    for (var d = 0; d < ix.length; d++) {
      if (ix.kind[d] != TK.media) continue;
      final u = ix.unitOf(d)!, l = ix.lessonOf(d);
      Lesson? lesson;
      try {
        lesson = (await notes.unitBook(u.book, u.id)).unit(u.id)?.lessons.where((x) => x.id == l?.id).firstOrNull;
      } on FormatException {
        lesson = null;
      }
      final c = lesson == null || ix.pos[d] >= lesson.cards.length ? null : lesson.cards[ix.pos[d]];
      final kind = ix.keys[d].split('\t').first;
      if (c is! MediaCard || c.kind != kind || !ix.keys[d].endsWith(c.title)) {
        bad.add('${ix.keys[d]} @ ${l?.id}~${ix.pos[d]}');
      } else if (kind == 'sim') {
        sims++;
      }
    }
    // a unit whose source file does not parse (see notes_parse_test) cannot open; nothing else may miss
    expect(bad.where((b) => !b.contains('math11-u1')), isEmpty, reason: bad.take(10).join('\n'));
    expect(sims, greaterThan(40));
  });

  group('answers with the real content', () {
    test('notes card, deep link, practice and matric', () async {
      final a = TutorAnswerer(ix, repo, notes);
      final r = await a.answer('what is refraction');
      expect(r.refuse, isFalse);
      expect(r.where, contains('Physics'));
      expect(r.blocks, isNotEmpty);
      expect(r.open?.unit, isNotNull);
      expect(r.open!.focus, matches(RegExp(r'^phys\d+-u\d-l[\d-]+~\d+$')));
      expect(r.practice, isNotEmpty);
      expect(r.matric, isNotEmpty);

      final q = await a.answer('quadratic formula');
      expect(q.blocks.map((b) => b.text).join(' ').toLowerCase(), anyOf(contains('quadratic'), contains('b^2'), contains('b²')));

      final adwa = await a.answer('causes of the Battle of Adwa');
      expect(adwa.refuse, isFalse);
      final all = [...adwa.blocks.map((b) => b.text), ...adwa.matric.map((q) => q.stem), ...adwa.practice.map((q) => q.stem)].join(' ');
      expect(all.toLowerCase(), contains('adwa'));
      expect(adwa.open?.where, contains('History'));

      final ti = await a.answer('ሓገዝቲ ግሲ'); // Tigrinya: "auxiliary verb"
      expect(ti.refuse, isFalse);
      expect(ti.where, contains('English'));

      final g = await a.answer('photosynthesis', const TutorScope(subject: 'biology', grade: 9));
      expect(g.where, startsWith('Grade 9 · Biology'));

      final tense = await a.answer('present perfect tense');
      expect(tense.where, contains('English'));
      expect((await a.answer('law of demand')).where, contains('Business'));
      expect((await a.answer('qwertyuiop zxcvb')).refuse, isTrue);
    });

    test('a question only in a lazy matric pack is loaded on demand', () async {
      final a = TutorAnswerer(ix, repo, notes);
      final lazy = [
        for (var d = 0; d < ix.length; d++)
          if (ix.kind[d] == TK.lazy) d,
      ];
      expect(lazy, isNotEmpty);
      final d = lazy.first;
      final label = ix.lazySubjects[ix.subjectOf(d)];
      expect(label, isNotNull);
      await repo.ensureLazySubject(label!);
      expect(repo.byId[ix.keys[d]], isNotNull, reason: ix.keys[d]);
      expect(a, isNotNull);
    });
  });

  testWidgets('Tutor tab answers and opens the lesson', (t) async {
    HighState.tickStudy = false;
    highDecorAnimations = false;
    await loadFonts();
    resetTutorChat();
    t.view.physicalSize = const Size(780, 1688);
    t.view.devicePixelRatio = 2;
    addTearDown(t.view.reset);
    final repo = ExamRepo(useIsolate: false, lazyExercises: true, lazyExams: true, deferCodes: true);
    await t.runAsync(() async {
      await repo.init();
      await TutorIndex.load();
      await notes.book('physics_11');
    });
    SharedPreferences.setMockInitialValues({'high:v1': '{"name":"Abel"}'});
    final s = HighState(repo, await SharedPreferences.getInstance(), notes);
    await s.load();
    await t.pumpWidget(HighApp(state: s, initialTab: HighTab.tutor));
    await t.pumpAndSettle();
    expect(find.byType(TutorPage), findsOneWidget);
    await t.enterText(find.byType(EditableText), 'what is refraction');
    await t.testTextInput.receiveAction(TextInputAction.done);
    // the answer resolves notes/question files for real: give it wall-clock time, then settle
    for (var i = 0; i < 100 && find.text('Open in Notes').evaluate().isEmpty; i++) {
      await t.runAsync(() => Future<void>.delayed(const Duration(milliseconds: 50)));
      await t.pump(const Duration(milliseconds: 50));
    }
    await t.pumpAndSettle();
    expect(t.takeException(), isNull);
    expect(find.textContaining('Physics', findRichText: true), findsWidgets);
    expect(find.text('MATRIC & MODEL QUESTIONS'), findsOneWidget);
    final open = find.text('Open in Notes');
    expect(open, findsOneWidget);
    await t.ensureVisible(open);
    await t.pumpAndSettle();
    await t.tap(open);
    await t.pumpAndSettle();
    expect(find.byType(UnitPage), findsOneWidget);
    expect(t.widget<UnitPage>(find.byType(UnitPage)).focus, isNotNull);
    HighNav.of(t.element(find.byType(UnitPage))).back();
    await t.pumpAndSettle();
    await t.pump(const Duration(seconds: 5));
  });
}

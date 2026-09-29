// M3: media cards (photos, 3D, sims, quick checks, label + match games), credits and gamification.
import 'dart:convert';
import 'dart:io';
import 'dart:typed_data';
import 'dart:ui' as ui;

import 'package:flutter/rendering.dart';
import 'package:flutter/widgets.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:high/high/app.dart';
import 'package:high/high/data/repository.dart';
import 'package:high/high/media/media.dart';
import 'package:high/high/media/mesh3d.dart';
import 'package:high/high/media/sims.dart';
import 'package:high/high/notes/jr/data/json_util.dart';
import 'package:high/high/notes/jr/data/notes_models.dart';
import 'package:high/high/notes/jr/data/repository.dart';
import 'package:high/high/state/app_state.dart';
import 'package:high/high/widgets/page.dart';
import 'package:shared_preferences/shared_preferences.dart';

import 'helpers.dart';

class Gallery extends StatelessWidget {
  const Gallery(this.cards, {super.key});
  final List<Map<String, dynamic>> cards;
  @override
  Widget build(BuildContext context) => PageShell(
    top: TopBar(title: 'Media', onBack: HighNav.of(context).back, tab: false),
    body: ListView(
      padding: const EdgeInsets.all(16),
      children: [
        for (final (i, c) in cards.indexed)
          Padding(
            padding: const EdgeInsets.only(bottom: 16),
            child: MediaCardView(c: NoteCard.fromJ(J({'type': 'media', 'page': 1, ...c}, 'test')) as MediaCard, unitId: 'test-u', ckey: 'k$i'),
          ),
      ],
    ),
  );
}

void main() {
  HighState.tickStudy = false;
  highDecorAnimations = false;
  highNow = () => DateTime(2026, 9, 29, 10);
  final repo = ExamRepo(useIsolate: false), notes = NotesRepo(useIsolate: false);
  final key = GlobalKey();
  final pl = [for (final x in (jsonDecode(File('assets/high/media/placements.json').readAsStringSync())['cards'] as List)) Map<String, dynamic>.from(x['card'] as Map)];
  final cred = jsonDecode(File('assets/high/media/credits.json').readAsStringSync()) as Map<String, dynamic>;
  setUpAll(() async {
    await loadFonts();
    await repo.init();
    await notes.init();
  });

  test('every placed item is credited, openly licensed, small, and every sim exists', () {
    final ok = RegExp(r'^(public domain|cc0|cc by(-sa)? [\d.]+)$', caseSensitive: false);
    for (final c in pl) {
      final id = c['id'] ?? c['img'];
      if (id != null) {
        expect(cred.containsKey(id), isTrue, reason: '$id');
        final f = File('assets/high/media/${cred[id]['file']}');
        expect(f.existsSync(), isTrue, reason: f.path);
        expect(ok.hasMatch('${cred[id]['licence']}'), isTrue, reason: '$id ${cred[id]['licence']}');
        expect(f.lengthSync(), lessThan(id.toString().startsWith('m_') ? 3000000 : 180000), reason: f.path);
      }
      if (c['kind'] == 'sim') expect(kSims.containsKey(c['sim']), isTrue, reason: '${c['sim']}');
    }
    for (final e in cred.entries) {
      for (final k in ['title', 'author', 'licence', 'source']) {
        expect('${e.value[k] ?? ''}'.isNotEmpty, isTrue, reason: '${e.key}.$k');
      }
      if (e.value['kind'] == 'model') {
        final m = Mesh.parse(ByteData.sublistView(File('assets/high/media/${e.value['file']}').readAsBytesSync()));
        expect(m.nt, greaterThan(100));
        expect(m.idx.every((i) => i < m.pos.length ~/ 3), isTrue);
      }
    }
    expect(kSims.length, greaterThanOrEqualTo(20));
  });

  test('placed cards are appended to their lessons when a book loads', () async {
    final b = await notes.book(notes.books.firstWhere((b) => b.subject == 'biology' && b.grade == 10).id);
    final media = [for (final u in b.units) for (final l in u.lessons) ...l.cards.whereType<MediaCard>()];
    expect(media.map((c) => c.kind).toSet(), containsAll(['label', 'quick', 'photo']));
  });

  testWidgets('media cards render; games award XP, stars and badges', (t) async {
    t.view.physicalSize = const Size(800, 1400);
    t.view.devicePixelRatio = 1;
    addTearDown(t.view.reset);
    SharedPreferences.setMockInitialValues({HighState.key: jsonEncode({'v': 2, 'name': 'Hana', 'theme': 'light'})});
    final s = HighState(repo, await SharedPreferences.getInstance(), notes);
    await s.load();
    await t.pumpWidget(RepaintBoundary(key: key, child: HighApp(state: s)));
    await t.pumpAndSettle();
    final nav = HighNav.of(t.element(find.byType(PageShell).first));

    Future<void> save(String name) async {
      for (var i = 0; i < 4; i++) {
        await t.runAsync(() => Future<void>.delayed(const Duration(milliseconds: 80)));
        await t.pump(const Duration(milliseconds: 100));
      }
      final ro = t.renderObject<RenderRepaintBoundary>(find.byKey(key));
      await t.runAsync(() async {
        final img = await ro.toImage(pixelRatio: 1);
        final bd = await img.toByteData(format: ui.ImageByteFormat.png);
        File('compare/$name.png').writeAsBytesSync(bd!.buffer.asUint8List());
      });
    }

    // every distinct card renders without errors
    final seen = <String>{};
    for (final c in pl) {
      final sig = '${c['kind']}:${c['sim'] ?? c['id'] ?? c['img'] ?? c['title']}';
      if (!seen.add(sig)) continue;
      nav.push(Gallery([c]));
      await t.pumpAndSettle();
      await t.runAsync(() => Future<void>.delayed(const Duration(milliseconds: 20)));
      await t.pump();
      expect(t.takeException(), isNull, reason: sig);
      nav.back();
      await t.pumpAndSettle();
    }

    // quick check: answer both right -> XP + 3 stars
    final quick = pl.firstWhere((c) => c['kind'] == 'quick' && (c['qs'] as List).length == 2);
    nav.push(Gallery([quick]));
    await t.pumpAndSettle();
    for (final q in quick['qs'] as List) {
      await t.tap(find.text('${(q['o'] as List)[q['a'] as int]}').first);
      await t.pumpAndSettle();
    }
    expect(s.xp, 10);
    expect(s.starsOf('test-u'), 3);
    expect(find.textContaining('+10 XP'), findsOneWidget);
    nav.back();
    await t.pumpAndSettle();

    // match game by taps
    final mt = pl.firstWhere((c) => c['kind'] == 'match');
    nav.push(Gallery([mt]));
    await t.pumpAndSettle();
    for (final pr in mt['pairs'] as List) {
      await t.tap(find.text('${pr[0]}'));
      await t.pump();
      await t.tap(find.text('${pr[1]}'));
      await t.pumpAndSettle();
    }
    expect(find.text('All matched  ★★★  +10 XP'), findsOneWidget);
    expect(s.count('match'), 1);
    nav.back();
    await t.pumpAndSettle();
    expect(s.badges.contains('first'), isTrue);

    // screenshots: sims + 3D + label game
    nav.push(Gallery([pl.firstWhere((c) => c['sim'] == 'projectile'), pl.firstWhere((c) => c['id'] == 'm_earth')]));
    await t.pumpAndSettle();
    await save('media_sim_3d');
    nav.back();
    nav.push(Gallery([pl.firstWhere((c) => c['sim'] == 'vsepr'), pl.firstWhere((c) => c['id'] == 'm_microscope')]));
    await t.pumpAndSettle();
    await save('media_vsepr_model');
    nav.back();
    nav.push(Gallery([pl.firstWhere((c) => c['sim'] == 'supply'), pl.firstWhere((c) => c['sim'] == 'timeline' && '${c['title']}'.contains('Eritrea'))]));
    await t.pumpAndSettle();
    await save('media_batch2');
    nav.back();
    final heart = pl.firstWhere((c) => c['img'] == 'bio_heart');
    nav.push(Gallery([heart]));
    await t.pumpAndSettle();
    await t.tap(find.text('1'));
    await t.pump();
    await t.tap(find.text('${(heart['pins'] as List)[0]['t']}'));
    await t.pumpAndSettle();
    await save('media_label_game');
    nav.back();
    await t.pumpAndSettle();
    await t.dragUntilVisible(find.textContaining('-day streak'), find.byType(Scrollable).first, const Offset(0, -200));
    await t.pumpAndSettle();
    await save('home_game_card');
    expect(t.takeException(), isNull);
    await t.pump(const Duration(seconds: 5));
  });
}

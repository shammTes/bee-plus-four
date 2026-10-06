// Physics-lab sims (lib/high/media/lab_*.dart, sims_optics.dart …): every registered lab builds, every choice and the
// slider extremes paint, animated labs run a few frames, and every placement targets a lesson that exists.
// LAB_SHOTS=<dir> flutter test test/lab_sims_test.dart  also saves a PNG per lab and choice.
import 'dart:convert';
import 'dart:io';
import 'dart:ui' as ui;

import 'package:flutter/rendering.dart';
import 'package:flutter/widgets.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:high/high/app.dart';
import 'package:high/high/data/repository.dart';
import 'package:high/high/media/lab_kit.dart';
import 'package:high/high/media/lab_sims.dart';
import 'package:high/high/media/media.dart';
import 'package:high/high/media/sims.dart';
import 'package:high/high/notes/jr/data/json_util.dart';
import 'package:high/high/notes/jr/data/notes_models.dart';
import 'package:high/high/notes/jr/data/repository.dart';
import 'package:high/high/state/app_state.dart';
import 'package:high/high/widgets/page.dart';
import 'package:shared_preferences/shared_preferences.dart';

import 'helpers.dart';

class _Gallery extends StatelessWidget {
  const _Gallery(this.card);
  final Map<String, dynamic> card;
  @override
  Widget build(BuildContext context) => PageShell(
    top: TopBar(title: 'Lab', onBack: HighNav.of(context).back, tab: false),
    body: ListView(
      padding: const EdgeInsets.all(16),
      children: [
        MediaCardView(c: NoteCard.fromJ(J({'type': 'media', 'page': 1, ...card}, 'test')) as MediaCard, unitId: 'test-u', ckey: 'lab'),
      ],
    ),
  );
}

void main() {
  HighState.tickStudy = false;
  highDecorAnimations = false;
  final repo = ExamRepo(useIsolate: false), notes = NotesRepo(useIsolate: false);
  final shots = Platform.environment['LAB_SHOTS'];
  final key = GlobalKey();
  setUpAll(() async {
    await loadFonts();
    await repo.init();
    await notes.init();
  });

  test('lab sims are registered in kSims and every placed sim exists on a real lesson', () async {
    expect(labSims.length, greaterThanOrEqualTo(8));
    for (final k in labSims.keys) {
      expect(kSims[k]?.call(const {}), isA<LabSpec>(), reason: k);
    }
    final pl = (jsonDecode(File('assets/high/media/placements.json').readAsStringSync())['cards'] as List).cast<Map>();
    final lessons = <String>{};
    for (final b in notes.books.where((b) => b.subject == 'physics')) {
      final book = await notes.book(b.id);
      for (final u in book.units) {
        for (final l in u.lessons) {
          lessons.add(l.id);
        }
      }
    }
    for (final c in pl) {
      final card = c['card'] as Map;
      if (card['kind'] == 'sim' && labSims.containsKey(card['sim'])) {
        expect(lessons.contains(c['lesson']), isTrue, reason: '${card['sim']} -> ${c['lesson']}');
      }
    }
  });

  testWidgets('every lab builds, paints each choice and slider extreme, and animates', (t) async {
    t.view.physicalSize = const Size(400, 1400);
    t.view.devicePixelRatio = 1;
    addTearDown(t.view.reset);
    SharedPreferences.setMockInitialValues({
      HighState.key: jsonEncode({'v': 2, 'name': 'Hana', 'theme': 'light', 'tourDone': true}),
    });
    final s = HighState(repo, await SharedPreferences.getInstance(), notes);
    await s.load();
    await t.pumpWidget(
      RepaintBoundary(
        key: key,
        child: HighApp(state: s),
      ),
    );
    await t.pumpAndSettle();
    final nav = HighNav.of(t.element(find.byType(PageShell).first));

    Future<void> shot(String name) async {
      if (shots == null) return;
      final ro = t.renderObject<RenderRepaintBoundary>(find.byKey(key));
      await t.runAsync(() async {
        final img = await ro.toImage(pixelRatio: 1);
        final bd = await img.toByteData(format: ui.ImageByteFormat.png);
        Directory(shots).createSync(recursive: true);
        File('$shots/$name.png').writeAsBytesSync(bd!.buffer.asUint8List());
      });
    }

    for (final name in labSims.keys) {
      nav.push(_Gallery({'kind': 'sim', 'sim': name, 'title': name, 'p': <String, dynamic>{}}));
      await t.pumpAndSettle();
      expect(t.takeException(), isNull, reason: name);
      final st = t.state<LabViewState>(find.byType(LabView));
      final spec = st.s;
      // each choice of each option (others at default)
      final combos = <Map<String, double>>[{}];
      for (final o in spec.opts) {
        for (var i = 1; i < o.options.length; i++) {
          combos.add({o.name: i.toDouble()});
        }
      }
      if (spec.opts.length >= 2) {
        combos.add({for (final o in spec.opts) o.name: (o.options.length - 1).toDouble()});
      }
      for (final (ci, combo) in combos.indexed) {
        for (final o in spec.opts) {
          st.set(o.name, combo[o.name] ?? o.def.toDouble());
        }
        await t.pump();
        await t.runAsync(() => Future<void>.delayed(const Duration(milliseconds: 10)));
        await t.pump();
        await shot('${name}_$ci');
        for (final x in spec.sliders) {
          st.set(x.name, x.min);
          await t.pump();
          st.set(x.name, x.max);
          await t.pump();
          st.set(x.name, x.def);
          await t.pump();
          expect(t.takeException(), isNull, reason: '$name ${x.name} $combo');
        }
        if (spec.anim) {
          st.togglePlay();
          for (var f = 0; f < 6; f++) {
            await t.pump(const Duration(milliseconds: 120));
          }
          await shot('${name}_${ci}_run');
          st.replay();
          await t.pump(const Duration(milliseconds: 50));
          if (st.playing) st.togglePlay();
          await t.pump();
        }
        expect(t.takeException(), isNull, reason: '$name $combo');
      }
      if (spec.drag != null) {
        final cp = find.descendant(of: find.byType(LabView), matching: find.byType(CustomPaint)).first;
        await t.tapAt(t.getTopLeft(cp) + const Offset(40, 60));
        await t.pump();
        expect(t.takeException(), isNull, reason: '$name drag');
      }
      nav.back();
      await t.pumpAndSettle();
    }
    await t.pump(const Duration(seconds: 1));
  });
}

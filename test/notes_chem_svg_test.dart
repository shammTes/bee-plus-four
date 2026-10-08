// The chemistry tutor diagrams (tool/enrich/chem_models) parse in flutter_svg after the app's preprocessing, for every
// step / state key their cards use, and stay light (a few KB each) for low-end phones.
import 'dart:convert';
import 'dart:io';

import 'package:flutter_svg/flutter_svg.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:high/high/notes/jr/notes/svg_prep.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();

  test('chem_models diagrams parse for every key and are small', () async {
    final bad = <String>[];
    var n = 0;
    for (final f in Directory('assets/high/notes/split').listSync().whereType<File>().where((f) => f.path.contains('/chem'))) {
      final unit = jsonDecode(f.readAsStringSync())['units'][0] as Map<String, dynamic>;
      final diagrams = (unit['diagrams'] as Map<String, dynamic>? ?? {});
      final keys = <String, Set<String?>>{};
      for (final l in unit['lessons'] as List) {
        for (final c in (l as Map)['cards'] as List) {
          final d = (c as Map)['diagram'];
          if (d is! String || !d.startsWith('cm_')) continue;
          final k = keys.putIfAbsent(d, () => {null});
          for (final s in [...(c['steps'] as List? ?? []), ...(c['states'] as List? ?? [])]) {
            k.add((s as Map)['show'] as String? ?? s['key'] as String?);
          }
        }
      }
      for (final e in keys.entries) {
        final spec = diagrams[e.key] as Map<String, dynamic>?;
        if (spec == null) {
          bad.add('${unit['id']}: ${e.key} not registered');
          continue;
        }
        final file = File('assets/high/notes/notes/${spec['svg']}');
        final raw = file.readAsStringSync();
        if (raw.length > 8000) bad.add('${spec['svg']}: ${raw.length} bytes');
        final prepped = prepSvg(raw);
        for (final k in e.value) {
          if (k != null && !raw.contains('"$k"') && !RegExp('data-(s|hl)="[^"]*\\b$k\\b').hasMatch(raw)) bad.add('${spec['svg']}: key $k not in the SVG');
          try {
            final pic = await vg.loadPicture(SvgStringLoader(applyShow(prepped, k)), null);
            pic.picture.dispose();
            n++;
          } catch (err) {
            bad.add('${spec['svg']} [$k]: $err');
          }
        }
      }
    }
    expect(n, greaterThan(50));
    expect(bad, isEmpty, reason: bad.join('\n'));
  });
}

// EqualHeightRow must lay out like IntrinsicHeight(Row(crossAxisAlignment: stretch)) for the rows it replaced.
import 'package:flutter/widgets.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:high/high/widgets/equal_row.dart';

import 'helpers.dart';

const _st = TextStyle(fontFamily: 'HighNunito', fontSize: 15);

List<Widget> _kids(String a, String b, {bool fixed = false}) => [
  if (fixed) const SizedBox(width: 126, child: Align(alignment: Alignment.bottomLeft, child: SizedBox(width: 120, height: 139.6))),
  if (fixed) const SizedBox(width: 4),
  Expanded(child: Container(key: const Key('a'), padding: const EdgeInsets.all(10), child: Text(a, style: _st))),
  Expanded(flex: 2, child: Center(key: const Key('b'), child: Padding(padding: const EdgeInsets.only(bottom: 16), child: Text(b, style: _st)))),
];

Widget _host(Widget row, double w) => Directionality(
  textDirection: TextDirection.ltr,
  child: Align(alignment: Alignment.topLeft, child: SizedBox(width: w, child: SingleChildScrollView(child: Column(children: [row])))),
);

void main() {
  setUpAll(loadFonts);
  final texts = [('Short', 'Also short'), ('A much longer text that wraps over several lines in a narrow cell', 'x'), ('', 'One two three four five six seven eight nine ten eleven twelve')];
  for (final fixed in [false, true]) {
    for (final w in [200.0, 390.0]) {
      for (final (a, b) in texts) {
        testWidgets('same layout as IntrinsicHeight + stretch Row (w $w, fixed $fixed, "${a.length}/${b.length}")', (t) async {
          await t.pumpWidget(_host(IntrinsicHeight(child: Row(crossAxisAlignment: CrossAxisAlignment.stretch, spacing: 12, children: _kids(a, b, fixed: fixed))), w));
          final want = [for (final k in ['a', 'b']) t.getRect(find.byKey(Key(k)))];
          final wantRow = t.getSize(find.byType(Row));
          await t.pumpWidget(_host(EqualHeightRow(spacing: 12, children: _kids(a, b, fixed: fixed)), w));
          expect(t.getSize(find.byType(EqualHeightRow)), wantRow);
          expect([for (final k in ['a', 'b']) t.getRect(find.byKey(Key(k)))], want);
        });
      }
    }
  }

  testWidgets('min height is respected; taps reach the children', (t) async {
    var taps = 0;
    await t.pumpWidget(
      _host(
        ConstrainedBox(
          constraints: const BoxConstraints(minHeight: 150),
          child: EqualHeightRow(children: [Expanded(child: GestureDetector(onTap: () => taps++, child: const ColoredBox(color: Color(0xFF000000), child: Text('tap', style: _st))))]),
        ),
        300,
      ),
    );
    expect(t.getSize(find.byType(EqualHeightRow)).height, 150);
    expect(t.getSize(find.byType(ColoredBox)).height, 150);
    await t.tap(find.byType(ColoredBox));
    expect(taps, 1);
  });
}

// High: tiny stand-in for Junior's Shell, routing to High's shell (HighNav + showSheet).
import 'package:flutter/widgets.dart';

import '../../../app.dart' show showSheet;
import '../../../widgets/page.dart' show HighNav;


class Shell {
  Shell._(this._c);
  final BuildContext _c;
  static Shell of(BuildContext c) => Shell._(c);
  static final List<VoidCallback> _closers = [];
  void pop() => HighNav.of(_c).back();
  void showSheet(Widget child) => _closers.add(showSheetRaw(_c, child));
  void closeSheet() {
    if (_closers.isNotEmpty) _closers.removeLast()();
  }
}

VoidCallback showSheetRaw(BuildContext c, Widget child) => showSheet(c, child, bare: true);

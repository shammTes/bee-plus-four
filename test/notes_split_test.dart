// The committed per-unit notes files (assets/high/notes/split, made by tool/split_notes.py) must match the books:
// each one is {"book": <book block>, "units": [<the unit, or its unit_<id>.json override>]}. Fails when a notes book
// or override was edited without re-running `python3 tool/split_notes.py`.
import 'dart:convert';
import 'dart:io';

import 'package:flutter_test/flutter_test.dart';

const _notes = 'assets/high/notes/notes';
const _split = 'assets/high/notes/split';

Object? _read(String path) => jsonDecode(File(path).readAsStringSync());

/// book files in index order (same rule as tool/split_notes.py)
List<String> _bookFiles() {
  final files = <String>[];
  for (final name in ['index.json', 'english_index.json']) {
    final f = File('$_notes/$name');
    if (!f.existsSync()) continue;
    final idx = jsonDecode(f.readAsStringSync()) as Map;
    for (final subjects in ((idx['grades'] as Map?) ?? const {}).values) {
      for (final b in ((subjects as Map?) ?? const {}).values) {
        final fn = b is Map ? b['file'] : null;
        if (fn is String && !files.contains(fn)) files.add(fn);
      }
    }
  }
  return files;
}

void main() {
  test('every notes unit has an up-to-date split file, and there are no stale ones', () {
    final want = <String>{};
    final stale = <String>[];
    for (final fn in _bookFiles()) {
      final f = File('$_notes/$fn');
      if (!f.existsSync()) continue;
      final raw = jsonDecode(f.readAsStringSync());
      if (raw is! Map || raw['units'] is! List) continue;
      for (final u in raw['units'] as List) {
        if (u is! Map || u['id'] == null) continue;
        final id = '${u['id']}';
        want.add(id);
        Object? unit = u;
        final ov = File('$_notes/unit_$id.json');
        if (ov.existsSync()) {
          try {
            unit = jsonDecode(ov.readAsStringSync());
          } on FormatException {
            // the app ignores a broken override too
          }
        }
        final sf = File('$_split/$id.json');
        if (!sf.existsSync()) {
          stale.add('$id (missing)');
          continue;
        }
        final got = _read(sf.path);
        if (!const _Deep().eq(got, {'book': raw['book'], 'units': [unit]})) stale.add('$id (differs from $fn)');
      }
    }
    final have = Directory(_split).listSync().map((e) => e.uri.pathSegments.last).where((n) => n.endsWith('.json')).map((n) => n.substring(0, n.length - 5)).toSet();
    stale.addAll([for (final id in have.difference(want)) '$id (no such unit)']);
    expect(want.length, greaterThan(100));
    expect(stale, isEmpty, reason: 'split notes out of date: run `python3 tool/split_notes.py`\n${stale.take(20).join('\n')}');
  });
}

/// deep JSON equality (num compared by value: 1 == 1.0 like the app's parsers)
class _Deep {
  const _Deep();
  bool eq(Object? a, Object? b) {
    if (a is Map && b is Map) {
      if (a.length != b.length) return false;
      for (final e in a.entries) {
        if (!b.containsKey(e.key) || !eq(e.value, b[e.key])) return false;
      }
      return true;
    }
    if (a is List && b is List) {
      if (a.length != b.length) return false;
      for (var i = 0; i < a.length; i++) {
        if (!eq(a[i], b[i])) return false;
      }
      return true;
    }
    return a == b;
  }
}

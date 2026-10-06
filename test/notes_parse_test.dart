// every High notes book parses with the ported Junior models (book file + any unit_<id>.json override)
import 'dart:convert';
import 'dart:io';

import 'package:flutter_test/flutter_test.dart';
import 'package:high/high/notes/jr/data/repository.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();

  test('all notes books parse', () async {
    final r = NotesRepo(useIsolate: false);
    await r.init();
    // 9 subjects x 4 grades, minus Grade 9 English/History/Business economics = 33 books in index.json
    expect(r.books.length, 33);
    final bad = <String>[];
    var units = 0, lessons = 0, cards = 0;
    for (final b in r.books) {
      try {
        final book = await r.book(b.id);
        if (book.units.isEmpty) bad.add('${b.id}: no units');
        for (final u in book.units) {
          units++;
          if (u.lessons.isEmpty) bad.add('${b.id}/${u.id}: no lessons');
          for (final l in u.lessons) {
            lessons++;
            cards += l.cards.length;
            if (l.cards.isEmpty) bad.add('${b.id}/${u.id}/${l.id}: no cards');
          }
        }
      } catch (e) {
        bad.add('${b.id}: $e');
      }
    }
    expect(bad, isEmpty);
    expect(units, greaterThan(150));
    expect(lessons, greaterThan(400));
    expect(cards, greaterThan(4000));
    // ignore: avoid_print
    print("notes: ${r.books.length} books, $units units, $lessons lessons, $cards cards");
  });

  test('unit override files are valid JSON for an existing unit', () {
    // the loader silently ignores an override it cannot decode, so check them here
    final dir = Directory(NotesRepo.base);
    final ids = <String>{};
    for (final f in dir.listSync().whereType<File>()) {
      final name = f.uri.pathSegments.last;
      if (!name.endsWith('.json') || name.startsWith('unit_') || name.contains('index')) continue;
      final raw = jsonDecode(f.readAsStringSync());
      if (raw is Map && raw['units'] is List) {
        for (final u in raw['units'] as List) {
          if (u is Map && u['id'] != null) ids.add('${u['id']}');
        }
      }
    }
    for (final f in dir.listSync().whereType<File>()) {
      final name = f.uri.pathSegments.last;
      if (!name.startsWith('unit_') || !name.endsWith('.json')) continue;
      final id = name.substring(5, name.length - 5);
      expect(ids, contains(id), reason: '$name overrides a unit no book lists');
      final raw = jsonDecode(f.readAsStringSync());
      expect(raw, isA<Map>(), reason: name);
      expect((raw as Map)['id'], id, reason: name);
    }
  });
}

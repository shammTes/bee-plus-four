// High: notes content (assets/high/notes = /workspace/high/content, synced by tool/sync_assets.sh).
// notes/index.json lists grade -> subject -> book file + units; books are parsed lazily (isolate) and cached.
// English is listed in english_index.json so it can be added without rewriting the full index.
import 'dart:async';
import 'dart:convert';
import 'dart:isolate';

import '../../../media/media.dart' show MediaLib;

import 'package:flutter/services.dart';

import 'notes_models.dart';
import 'subjects.dart';

/// one unit entry of notes/index.json
class IndexUnit {
  IndexUnit(this.id, this.number, this.title, this.pages, this.questions, this.topics);
  final String id, title;
  final int number, questions;
  final List<int> pages;
  final List<({String id, String number, String title, int? page, List<String> cards})> topics;
}

class IndexBook {
  IndexBook(this.id, this.file, this.title, this.subject, this.grade, this.units);
  final String id, file, title, subject;
  final int grade;
  final List<IndexUnit> units;
  NotesSubject get look => notesSubject(subject);
}

/// High extension: unit concept map
class MapNode {
  MapNode(this.id, this.label, this.kind, this.cards);
  final String id, label, kind;
  final List<String> cards;
}

class UnitMap {
  UnitMap(this.root, this.nodes, this.edges);
  final String root;
  final List<MapNode> nodes;
  final List<({String from, String to, String label})> edges;
}

/// extras parsed from the raw JSON that the Junior models do not keep
class BookExtras {
  BookExtras(this.maps, this.cardKey);
  final Map<String, UnitMap> maps; // unit id -> map
  final Map<String, String> cardKey; // card id -> "lessonId~i"
}

class NotesRepo {
  NotesRepo({AssetBundle? bundle, this.useIsolate = false}) : bundle = bundle ?? rootBundle;
  final AssetBundle bundle;
  final bool useIsolate;
  static const base = 'assets/high/notes/notes';

  final List<IndexBook> books = [];
  final Map<String, List<Map<String, dynamic>>> unitQuestions = {}; // unit id -> [{id, confidence, via, exam, secondary}]
  final Map<String, NotesBook> _books = {};
  final Map<String, BookExtras> _extras = {};
  final Map<String, Future<NotesBook>> _loads = {};
  bool loaded = false;

  Future<void> init() async {
    Map<String, dynamic> idx;
    try {
      idx = jsonDecode(await bundle.loadString('$base/index.json')) as Map<String, dynamic>;
    } catch (_) {
      loaded = true; // no notes bundled
      return;
    }
    _addGradeMap((idx['grades'] as Map?) ?? const {});
    try {
      final extra = jsonDecode(await bundle.loadString('$base/english_index.json')) as Map<String, dynamic>;
      _addGradeMap((extra['grades'] as Map?) ?? const {});
    } catch (_) {}
    books.sort((a, b) => a.grade != b.grade ? a.grade - b.grade : _ord(a.subject) - _ord(b.subject));
    try {
      final uq = jsonDecode(await bundle.loadString('assets/high/notes/unit_questions.json')) as Map<String, dynamic>;
      for (final e in ((uq['units'] as Map?) ?? const {}).entries) {
        unitQuestions['${e.key}'] = [for (final x in (e.value as List? ?? const [])) if (x is Map) Map<String, dynamic>.from(x)];
      }
    } catch (_) {}
    await MediaLib.load(bundle);
    try {
      final pj = jsonDecode(await bundle.loadString('assets/high/media/placements.json')) as Map<String, dynamic>;
      placements = [for (final x in (pj['cards'] as List? ?? const [])) if (x is Map) Map<String, dynamic>.from(x)];
    } catch (_) {}
    loaded = true;
  }

  void _addGradeMap(Map grades) {
    for (final ge in grades.entries) {
      final g = int.tryParse('${ge.key}') ?? 0;
      for (final se in ((ge.value as Map?) ?? const {}).entries) {
        final b = se.value as Map;
        final id = '${b['book']}';
        if (books.any((x) => x.id == id)) continue;
        books.add(
          IndexBook(id, '${b['file']}', '${b['title'] ?? ''}', '${se.key}', g, [
            for (final u in (b['units'] as List? ?? const []))
              if (u is Map)
                IndexUnit(
                  '${u['id']}',
                  (u['number'] as num?)?.toInt() ?? 0,
                  '${u['title'] ?? ''}',
                  [for (final p in (u['pages'] as List? ?? const [])) (p as num).toInt()],
                  (u['questions'] as num?)?.toInt() ?? 0,
                  [
                    for (final t in (u['topics'] as List? ?? const []))
                      if (t is Map)
                        (
                          id: '${t['id']}',
                          number: '${t['number'] ?? ''}',
                          title: '${t['title'] ?? ''}',
                          page: (t['page'] as num?)?.toInt(),
                          cards: [for (final c in (t['cards'] as List? ?? const [])) '$c'],
                        ),
                  ],
                ),
          ]),
        );
      }
    }
  }

  /// High: media / interactive cards appended to lessons ({lesson, card}), see assets/high/media/placements.json
  List<Map<String, dynamic>> placements = [];

  /// append placed cards to their lessons (at the end, so saved card indices stay valid)
  static void injectMedia(Object? raw, List<Map<String, dynamic>> pl) {
    if (pl.isEmpty || raw is! Map) return;
    final by = <String, List<Map<String, dynamic>>>{};
    for (final x in pl) {
      (by['${x['lesson']}'] ??= []).add(Map<String, dynamic>.from(x['card'] as Map));
    }
    for (final u in (raw['units'] as List? ?? const [])) {
      if (u is! Map) continue;
      for (final l in (u['lessons'] as List? ?? const [])) {
        if (l is! Map) continue;
        final add = by[l['id']];
        if (add == null) continue;
        final pg = (l['pages'] as List?)?.firstOrNull ?? 0;
        (l['cards'] as List).addAll([for (final c in add) {'type': 'media', 'page': pg, ...c}]);
      }
    }
  }

  static int _ord(String s) {
    final i = kNotesOrder.indexOf(s);
    return i < 0 ? 99 : i;
  }

  List<int> get grades => ({for (final b in books) b.grade}.toList()..sort());
  List<IndexBook> grade(int g) => books.where((b) => b.grade == g).toList();
  IndexBook? byId(String id) => books.where((b) => b.id == id).firstOrNull;
  int get totalUnits => books.fold(0, (a, b) => a + b.units.length);

  /// book id + index unit of a unit id
  ({IndexBook book, IndexUnit unit})? unitById(String uid) {
    for (final b in books) {
      for (final u in b.units) {
        if (u.id == uid) return (book: b, unit: u);
      }
    }
    return null;
  }

  NotesBook? bookIfLoaded(String id) => _books[id];
  BookExtras? extras(String id) => _extras[id];

  Future<NotesBook> book(String id) {
    final hit = _books[id];
    if (hit != null) return Future.value(hit);
    return _loads[id] ??= () async {
      final file = byId(id)?.file ?? '$id.json';
      final s = await bundle.loadString('$base/$file', cache: false);
      final pl = placements;
      (NotesBook, BookExtras) parse() {
        final raw = jsonDecode(s);
        injectMedia(raw, pl);
        return (NotesBook.fromJson(raw, file), _parseExtras(raw));
      }

      final r = useIsolate ? await Isolate.run(parse) : parse();
      _books[id] = r.$1;
      _extras[id] = r.$2;
      return r.$1;
    }();
  }

  static BookExtras _parseExtras(Object? raw) {
    final maps = <String, UnitMap>{}, keys = <String, String>{};
    for (final u in ((raw as Map)['units'] as List? ?? const [])) {
      if (u is! Map) continue;
      for (final l in (u['lessons'] as List? ?? const [])) {
        if (l is! Map) continue;
        final cs = l['cards'] as List? ?? const [];
        for (var i = 0; i < cs.length; i++) {
          final c = cs[i];
          if (c is Map && c['id'] != null) keys['${c['id']}'] = '${l['id']}~$i';
        }
      }
      final m = u['unitMap'];
      if (m is Map) {
        maps['${u['id']}'] = UnitMap(
          '${m['root']}',
          [
            for (final n in (m['nodes'] as List? ?? const []))
              if (n is Map) MapNode('${n['id']}', '${n['label']}', '${n['kind'] ?? 'idea'}', [for (final c in (n['cards'] as List? ?? const [])) '$c']),
          ],
          [
            for (final e in (m['edges'] as List? ?? const []))
              if (e is Map) (from: '${e['from']}', to: '${e['to']}', label: '${e['label'] ?? ''}'),
          ],
        );
      }
    }
    return BookExtras(maps, keys);
  }

  /// diagram.svg is relative to content/notes (e.g. "svg/biology_12/cell.svg")
  String svgPath(String svg) => '$base/$svg';
}

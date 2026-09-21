from pathlib import Path
p = Path('lib/features/notes/notes_screen.dart')
t = p.read_text(encoding='utf-8')
old = '''      final exact = all
          .where((d) =>
              (d['unit_number'] as num?)?.toInt() == note.unitNumber)
          .toList();
      if (exact.isNotEmpty) return exact;
      // Title overlap fallback within same subject only
      final words = note.title
          .toLowerCase()
          .split(RegExp(r'\\W+'))
          .where((w) => w.length > 3)
          .take(3)
          .toList();
      final soft = all.where((d) {
        final t = '${d['title']}'.toLowerCase();
        return words.any((w) => t.contains(w));
      }).toList();
      return soft;'''
new = '''      // EXACT unit_number match only — no soft title matching
      final exact = all
          .where((d) =>
              (d['unit_number'] as num?)?.toInt() == note.unitNumber)
          .toList();
      return exact;'''
if old not in t:
    print('pattern not found — may already be patched')
else:
    p.write_text(t.replace(old, new), encoding='utf-8')
    print('patched notes_screen soft-match removed')

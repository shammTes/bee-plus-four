import 'dart:convert';

/// Resource kinds. Stage 1 only opens [pdf]; video/reel are reserved for Stage 2/3.
enum FourType { pdf, video, reel, web }

/// Metadata kept in the encrypted header.
class FourMeta {
  FourMeta({
    required this.title,
    required this.subject,
    required this.grade,
    this.unit = '',
    required this.type,
    required this.mime,
    this.pages,
    this.durationMs,
    this.note = '',
    this.licence = '',
    this.source = '',
    this.sourceUrl = '',
    this.author = '',
    this.entry = '',
    DateTime? createdAt,
  }) : createdAt = (createdAt ?? DateTime.now()).toUtc();

  final String title;

  /// lowercase id like the notes books use: `biology`, `chemistry`, `mathematics`…
  final String subject;
  final int grade;

  /// unit number (`3`) or unit id; empty = whole subject/grade
  final String unit;
  final FourType type;
  final String mime;
  final int? pages, durationMs;
  final String note;

  /// SPDX-ish licence id: `CC-BY-4.0`, `CC-BY-SA-4.0`, `CC0-1.0`, `PD`, `CC-BY-ND-4.0`.
  /// Empty when the content is the user's own.
  final String licence;

  /// Where it came from, e.g. "LabXchange".
  final String source;

  /// Canonical page URL (attribution; not fetched at playback).
  final String sourceUrl;
  final String author;

  /// `.4web` only: path of the start page inside the zip (default `index.html`).
  final String entry;
  final DateTime createdAt;

  Map<String, Object?> toJson() => {
    'title': title,
    'subject': subject,
    'grade': grade,
    'unit': unit,
    'type': type.name,
    'mime': mime,
    if (pages != null) 'pages': pages,
    if (durationMs != null) 'durationMs': durationMs,
    if (note.isNotEmpty) 'note': note,
    if (licence.isNotEmpty) 'licence': licence,
    if (source.isNotEmpty) 'source': source,
    if (sourceUrl.isNotEmpty) 'sourceUrl': sourceUrl,
    if (author.isNotEmpty) 'author': author,
    if (entry.isNotEmpty) 'entry': entry,
    'createdAt': createdAt.toIso8601String(),
  };

  factory FourMeta.fromJson(Map<String, Object?> j) => FourMeta(
    title: j['title'] as String? ?? '',
    subject: j['subject'] as String? ?? '',
    grade: (j['grade'] as num?)?.toInt() ?? 0,
    unit: '${j['unit'] ?? ''}',
    type: FourType.values.firstWhere((t) => t.name == j['type'], orElse: () => FourType.pdf),
    mime: j['mime'] as String? ?? 'application/octet-stream',
    pages: (j['pages'] as num?)?.toInt(),
    durationMs: (j['durationMs'] as num?)?.toInt(),
    note: j['note'] as String? ?? '',
    licence: j['licence'] as String? ?? '',
    source: j['source'] as String? ?? '',
    sourceUrl: j['sourceUrl'] as String? ?? '',
    author: j['author'] as String? ?? '',
    entry: j['entry'] as String? ?? '',
    createdAt: DateTime.tryParse(j['createdAt'] as String? ?? ''),
  );

  List<int> encode() => utf8.encode(jsonEncode(toJson()));
  static FourMeta decode(List<int> b) => FourMeta.fromJson((jsonDecode(utf8.decode(b)) as Map).cast<String, Object?>());

  /// Credit line shown under the content in 4, e.g. "Cell cycle · LabXchange · CC BY 4.0".
  String get creditLine {
    final bits = [if (author.isNotEmpty) author, if (source.isNotEmpty) source, if (licence.isNotEmpty) licence];
    return bits.join(' · ');
  }

  static String extensionFor(FourType t) => switch (t) {
    FourType.pdf => '.4pdf',
    FourType.video => '.4vid',
    FourType.reel => '.4reel',
    FourType.web => '.4web',
  };
}

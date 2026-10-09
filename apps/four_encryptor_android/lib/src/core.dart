// Encryption job model + the one code path that produces files (no Flutter imports, unit-tested on a PC).
import 'dart:async';
import 'dart:typed_data';

import 'package:four_format/four_format.dart';

/// One file to encrypt plus its metadata.
class Job {
  Job({required this.uri, required this.name, required this.size, required this.mime, required this.type, this.tempPath});

  /// content:// URI, or an absolute temp path (zipped folder, LabXchange download)
  final String uri, name, mime;
  final int size;
  final String? tempPath;
  FourType type;
  String title = '', subject = '', unit = '';
  int grade = 0;
  Uint8List? thumb;
  int? durationMs, pages;
  bool portrait = false;

  // .4web
  String entry = '';
  // third-party content (LabXchange or chosen by hand); empty licence = the user's own content
  bool thirdParty = false, locked = false;
  FourLicence licence = FourLicence.unknown;
  String author = '', source = '', sourceUrl = '';

  // progress / result
  String status = 'Ready';
  double progress = 0;
  String? outUri, outName, error, errorDetails;
  bool get done => outUri != null;

  /// Why this job may not be encrypted (licence gate), or null.
  String? get refusal {
    if (!thirdParty) return null;
    return licence.refusal(modified: false);
  }

  String get baseName {
    final i = name.lastIndexOf('.');
    final b = i > 0 ? name.substring(0, i) : name;
    return b.replaceAll(RegExp(r'[\\/:*?"<>|]'), '_');
  }

  String get outFileName => '$baseName${FourMeta.extensionFor(type)}';

  FourMeta meta() => FourMeta(
    title: title.trim().isEmpty ? baseName : title.trim(),
    subject: subject.trim().toLowerCase().replaceAll(' ', '_'),
    grade: grade,
    unit: unit.trim(),
    type: type,
    mime: type == FourType.web ? 'application/zip' : (mime.isEmpty ? guessMime(name) : mime),
    pages: type == FourType.pdf ? pages : null,
    durationMs: type == FourType.video || type == FourType.reel ? durationMs : null,
    licence: thirdParty ? licence.id : '',
    author: thirdParty ? author.trim() : '',
    source: thirdParty ? source.trim() : '',
    sourceUrl: thirdParty ? sourceUrl.trim() : '',
    entry: type == FourType.web ? entry : '',
  );
}

String guessMime(String name) {
  final l = name.toLowerCase();
  if (l.endsWith('.pdf')) return 'application/pdf';
  if (l.endsWith('.mp4') || l.endsWith('.m4v')) return 'video/mp4';
  if (l.endsWith('.webm')) return 'video/webm';
  if (l.endsWith('.mkv')) return 'video/x-matroska';
  if (l.endsWith('.3gp')) return 'video/3gpp';
  if (l.endsWith('.zip')) return 'application/zip';
  return 'application/octet-stream';
}

/// Auto-detected default: PDF → pdf, zip → web, portrait video → reel, other video → 16:9 video.
FourType? detectType(String name, String mime, {bool portrait = false}) {
  final m = mime.isEmpty ? guessMime(name) : mime;
  if (m == 'application/pdf') return FourType.pdf;
  if (m.contains('zip')) return FourType.web;
  if (m.startsWith('video/')) return portrait ? FourType.reel : FourType.video;
  return null;
}

/// Start page of a web bundle: `index.html` at the root, else the shallowest `…/index.html`, else the only .html.
String? bundleEntry(Iterable<String> entries) {
  final names = entries.where((e) => !e.startsWith('__MACOSX/') && !e.endsWith('/')).toList();
  if (names.contains('index.html')) return 'index.html';
  final idx = names.where((e) => e.toLowerCase().endsWith('/index.html')).toList()..sort((a, b) => '/'.allMatches(a).length.compareTo('/'.allMatches(b).length));
  if (idx.isNotEmpty) return idx.first;
  final html = names.where((e) => e.toLowerCase().endsWith('.html') || e.toLowerCase().endsWith('.htm')).toList()..sort((a, b) => a.length.compareTo(b.length));
  return html.isEmpty ? null : html.first;
}

/// Streams [input] into [add] as a 4 container. This is the only writer the app uses
/// (four_format's FourWriter: identical bytes layout to the Mac/CLI tools).
Future<FourPreamble> encryptStream({
  required FourSource input,
  required FutureOr<void> Function(List<int>) add,
  required FourMeta meta,
  required List<int> masterKey,
  required FourBatch batch,
  Uint8List? thumb,
  void Function(int done, int total)? onProgress,
}) => FourWriter.write(input: input, add: add, meta: meta, masterKey: masterKey, batch: batch, thumbnail: thumb, onProgress: onProgress);

String newBatchId() => 'android-${DateTime.now().toUtc().toIso8601String().substring(0, 19).replaceAll(':', '')}';

String fmtSize(int b) => b < 1024 * 1024 ? '${(b / 1024).toStringAsFixed(0)} KB' : '${(b / (1024 * 1024)).toStringAsFixed(1)} MB';

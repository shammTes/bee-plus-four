// Command-line encryptor for 4 resources. Works on macOS, Windows and Linux.
//
//   dart run four_format:four_encrypt encrypt notes.pdf --title "Cell biology" --subject biology --grade 11 --unit 3
//   dart run four_format:four_encrypt info  notes.4pdf
//   dart run four_format:four_encrypt decrypt notes.4pdf -o check.pdf
//   dart run four_format:four_encrypt newkey            (prints a fresh base64 master key)
//
// Master key: --mk <base64> or env FOUR_MK; otherwise the built-in DEV key (matches debug builds of 4).
import 'dart:convert';
import 'dart:io';

import 'package:four_format/four_format.dart';

Future<void> main(List<String> argv) async {
  if (argv.isEmpty || argv.first == '-h' || argv.first == '--help') return _usage();
  final cmd = argv.first;
  final pos = <String>[];
  final opt = <String, String>{};
  for (var i = 1; i < argv.length; i++) {
    final a = argv[i];
    if (a.startsWith('-')) {
      final k = a.replaceFirst(RegExp('^-+'), '');
      opt[k] = i + 1 < argv.length ? argv[++i] : '';
    } else {
      pos.add(a);
    }
  }
  try {
    switch (cmd) {
      case 'newkey':
        stdout.writeln(base64.encode(FourKeys.random(32)));
      case 'encrypt':
        await _encrypt(pos, opt);
      case 'info':
        await _info(pos, opt);
      case 'decrypt':
        await _decrypt(pos, opt);
      default:
        _usage();
        exitCode = 64;
    }
  } on FourFormatException catch (e) {
    stderr.writeln('error: ${e.message}');
    exitCode = 1;
  }
}

Future<List<int>> _mk(Map<String, String> opt) async {
  final s = opt['mk'] ?? Platform.environment['FOUR_MK'];
  if (s == null || s.isEmpty) {
    stderr.writeln('note: using the DEV master key (fine for testing; release builds need their own --mk)');
    return FourKeys.devMasterKey();
  }
  final k = base64.decode(s.trim());
  if (k.length != 32) throw const FourFormatException('master key must be 32 bytes (base64)');
  return k;
}

FourType _type(String path, String? t) {
  if (t != null) return FourType.values.byName(t);
  final l = path.toLowerCase();
  if (l.endsWith('.pdf')) return FourType.pdf;
  return FourType.video;
}

String _mime(String path) {
  final l = path.toLowerCase();
  if (l.endsWith('.pdf')) return 'application/pdf';
  if (l.endsWith('.mp4') || l.endsWith('.m4v')) return 'video/mp4';
  if (l.endsWith('.webm')) return 'video/webm';
  return 'application/octet-stream';
}

Future<void> _encrypt(List<String> pos, Map<String, String> opt) async {
  if (pos.isEmpty) throw const FourFormatException('encrypt needs at least one input file');
  final mk = await _mk(opt);
  final batch = FourBatch.create(opt['batch'] ?? 'b${DateTime.now().toUtc().millisecondsSinceEpoch}', mkVersion: int.parse(opt['mkver'] ?? '1'));
  final thumb = opt['thumb'] == null ? null : await File(opt['thumb']!).readAsBytes();
  for (final inPath in pos) {
    final type = _type(inPath, opt['type']);
    final base = inPath.replaceFirst(RegExp(r'\.[^./\\]+$'), '');
    final out = pos.length == 1 && opt['o'] != null ? opt['o']! : '${opt['outdir'] != null ? '${opt['outdir']}/${base.split(RegExp(r'[/\\]')).last}' : base}${FourMeta.extensionFor(type)}';
    final meta = FourMeta(
      title: opt['title'] ?? base.split(RegExp(r'[/\\]')).last,
      subject: (opt['subject'] ?? '').toLowerCase(),
      grade: int.tryParse(opt['grade'] ?? '') ?? 0,
      unit: opt['unit'] ?? '',
      type: type,
      mime: _mime(inPath),
      pages: int.tryParse(opt['pages'] ?? ''),
      note: opt['note'] ?? '',
    );
    final p = await FourWriter.encryptFile(inPath, out, meta: meta, masterKey: mk, batch: batch, thumbnail: thumb, chunkSize: int.tryParse(opt['chunk'] ?? '') ?? FourFormat.defaultChunk);
    stdout.writeln('wrote $out  id=${p.fileIdHex} batch=${p.batchId} chunks=${p.chunkCount}');
  }
}

Future<void> _info(List<String> pos, Map<String, String> opt) async {
  final src = await FileSource.open(pos.single);
  final p = await FourReader.peek(src);
  stdout.writeln('4 resource v${p.version}  id=${p.fileIdHex}  batch=${p.batchId}  mk=v${p.mkVersion}');
  stdout.writeln('size=${p.plainSize} chunk=${p.chunkSize} chunks=${p.chunkCount} thumb=${p.hasThumb}');
  final r = await FourReader.open(src, (_) => _mk(opt), verify: true);
  stdout.writeln(const JsonEncoder.withIndent('  ').convert(r.meta.toJson()));
  stdout.writeln('integrity: OK');
  await r.close();
}

Future<void> _decrypt(List<String> pos, Map<String, String> opt) async {
  final src = await FileSource.open(pos.single);
  final r = await FourReader.open(src, (_) => _mk(opt), verify: true);
  final out = File(opt['o'] ?? '${pos.single}.out');
  final sink = out.openWrite();
  for (var i = 0; i < r.preamble.chunkCount; i++) {
    sink.add(await r.readChunk(i));
  }
  await sink.close();
  await r.close();
  stdout.writeln('wrote ${out.path}');
}

void _usage() => stdout.writeln('''
four_encrypt — encrypt PDFs / videos for 4
  encrypt <files…> [-o out] [--outdir dir] --title T --subject biology --grade 11 [--unit 3]
          [--type pdf|video|reel] [--thumb thumb.jpg] [--batch id] [--mk base64] [--chunk bytes]
  info    <file.4pdf> [--mk base64]
  decrypt <file.4pdf> [-o out.pdf] [--mk base64]
  newkey''');

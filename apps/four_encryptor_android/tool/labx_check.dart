// Feasibility check on a PC: resolve LabXchange items, apply the licence gate, mirror interactives for offline use.
//   dart run tool/labx_check.dart <outdir> <labxchange item url | plain page url>...
// Writes <outdir>/<id>/... (the bundle files) and prints a summary line per item.
import 'dart:io';

import 'package:four_encryptor/src/labx.dart';
import 'package:four_encryptor/src/web_mirror.dart';

Future<void> main(List<String> args) async {
  final out = Directory(args.first);
  final lx = Labx();
  for (final url in args.skip(1)) {
    try {
      String? pageUrl;
      String name;
      if (Labx.itemId(url) != null) {
        final it = await lx.resolve(url);
        final why = Labx.refusal(it);
        stdout.writeln('${it.id} | ${it.title} | ${it.kind} | licence=${it.licenceRaw} | by=${it.author} | ${it.contentUrl}');
        stdout.writeln('   gate: ${why ?? 'ALLOWED'}');
        if (it.kind == 'simulation' || it.kind == 'interactive') pageUrl = it.contentUrl;
        name = it.id.split(':')[2];
      } else {
        pageUrl = url;
        name = Uri.parse(url).pathSegments.where((s) => s.isNotEmpty).last.replaceAll(RegExp(r'[^A-Za-z0-9_-]'), '_');
      }
      if (pageUrl == null) continue;
      final m = WebMirror();
      try {
        final (r, files) = await m.mirror(Uri.parse(pageUrl));
        await WebMirror.writeTo(Directory('${out.path}/$name'), files);
        stdout.writeln('   mirrored ${r.files.length} files, ${(r.totalBytes / 1024).round()} KB, entry=${r.entry}, unresolved=${r.unresolved.length} ${r.unresolved.take(5).toList()}, runtime hosts=${r.external}');
      } catch (e) {
        stdout.writeln('   mirror failed: $e');
      } finally {
        m.close();
      }
    } catch (e) {
      stdout.writeln('$url: $e');
    }
  }
  lx.close();
}

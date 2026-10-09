// Native PDF viewer for one decrypted resource. The PDF is decrypted into memory only (never written to disk),
// FLAG_SECURE blocks screenshots / recents thumbnails while it is open.
import 'dart:typed_data';

import 'package:flutter/material.dart' show Colors;
import 'package:flutter/widgets.dart';
import 'package:four_format/four_format.dart';
import 'package:pdfrx/pdfrx.dart';

import '../high/theme/tokens.dart';
import '../high/widgets/kit.dart';
import '../high/widgets/page.dart';
import 'library.dart';

class PdfResourcePage extends StatefulWidget with NoNav {
  const PdfResourcePage({super.key, required this.entry});
  final ResEntry entry;
  @override
  State<PdfResourcePage> createState() => _PdfResourcePageState();
}

class _PdfResourcePageState extends State<PdfResourcePage> {
  Uint8List? _bytes;
  Object? _err;

  @override
  void initState() {
    super.initState();
    ResourceLibrary.setSecure(true);
    _open();
  }

  Future<void> _open() async {
    try {
      final lib = ResourceLibrary.instance;
      final src = await FileSource.open(widget.entry.path);
      final r = await FourReader.open(src, lib.gate.masterKey);
      try {
        final b = await r.readAll();
        if (mounted) setState(() => _bytes = b);
      } finally {
        await r.close();
      }
    } catch (e) {
      if (mounted) setState(() => _err = e);
    }
  }

  @override
  void dispose() {
    ResourceLibrary.setSecure(false);
    _bytes = null;
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final p = Kit.of(context).p, b = _bytes;
    return PageShell(
      top: TopBar(title: widget.entry.meta.title, sub: widget.entry.meta.creditLine.isEmpty ? 'PDF' : 'PDF · ${widget.entry.meta.creditLine}', onBack: () => HighNav.of(context).back(), tab: false),
      body: _err != null
          ? Center(
              child: Padding(
                padding: const EdgeInsets.all(24),
                child: Text(_err is FourKeyException ? 'This phone cannot open this file. Unlock 4 first.' : 'Could not open this file. It may be damaged — copy it again and tap Refresh.', textAlign: TextAlign.center, style: ts(14, w800, p.ink2)),
              ),
            )
          : b == null
          ? Center(child: Text('Opening…', style: ts(14, w800, p.ink3)))
          : PdfViewer.data(
              b,
              sourceName: 'four-${widget.entry.id}',
              params: PdfViewerParams(backgroundColor: p.dark ? Colors.black : const Color(0xFFE9E4DC)),
            ),
    );
  }
}

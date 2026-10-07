// FourEncryptor — encrypts PDFs (and, from Stage 2, videos) for the 4 app.
// Drag files in, fill title / subject / grade / unit, apply to a batch, then Encrypt.
// The master key lives in the macOS Keychain (Windows: Credential Manager) via flutter_secure_storage.
import 'dart:async';
import 'dart:convert';
import 'dart:io';
import 'dart:isolate';
import 'dart:typed_data';

import 'package:desktop_drop/desktop_drop.dart';
import 'package:file_picker/file_picker.dart';
import 'package:flutter/material.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:four_format/four_format.dart';
import 'package:image/image.dart' as img;
import 'package:path/path.dart' as p;
import 'package:pdfrx/pdfrx.dart';

void main() => runApp(const EncryptorApp());

const kSubjects = [
  'agriculture', 'biology', 'business_economics', 'chemistry', 'civics', 'english', 'geography', 'history',
  'ict', 'mathematics', 'physics', 'tigrinya', 'general',
];

class EncryptorApp extends StatelessWidget {
  const EncryptorApp({super.key});
  @override
  Widget build(BuildContext context) => MaterialApp(
    title: 'FourEncryptor',
    debugShowCheckedModeBanner: false,
    theme: ThemeData(colorSchemeSeed: const Color(0xFFE88A6E), useMaterial3: true),
    home: const HomePage(),
  );
}

/// One input file plus its editable metadata.
class Item {
  Item(this.path)
    : title = p.basenameWithoutExtension(path).replaceAll(RegExp(r'[_-]+'), ' '),
      type = path.toLowerCase().endsWith('.pdf') ? FourType.pdf : FourType.video;
  final String path;
  String title, subject = 'biology', unit = '';
  int grade = 11;
  FourType type;
  Uint8List? thumb;
  String status = 'ready';
  double progress = 0;
  bool selected = true;

  String get mime => switch (p.extension(path).toLowerCase()) {
    '.pdf' => 'application/pdf',
    '.mp4' || '.m4v' => 'video/mp4',
    '.webm' => 'video/webm',
    _ => 'application/octet-stream',
  };
}

/// Master key storage (Keychain). Falls back to the DEV key so the tool works out of the box with debug builds of 4.
class KeyStore {
  static const _s = FlutterSecureStorage();
  static const _k = 'four_master_key_v1';
  static Future<(Uint8List, bool)> load() async {
    final v = await _s.read(key: _k);
    if (v == null) return (await FourKeys.devMasterKey(), true);
    return (base64.decode(v), false);
  }

  static Future<void> save(String b64) async {
    if (base64.decode(b64.trim()).length != 32) throw const FormatException('key must be 32 bytes (base64)');
    await _s.write(key: _k, value: b64.trim());
  }

  static Future<void> clear() => _s.delete(key: _k);
}

class HomePage extends StatefulWidget {
  const HomePage({super.key});
  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  final items = <Item>[];
  bool dragging = false, busy = false, devKey = true;
  String? outDir;
  final batchCtl = TextEditingController(text: 'batch-${DateTime.now().toIso8601String().substring(0, 10)}');

  // batch-apply fields
  String bSubject = 'biology', bUnit = '';
  int bGrade = 11;

  @override
  void initState() {
    super.initState();
    KeyStore.load().then((r) => setState(() => devKey = r.$2));
  }

  Future<void> _add(Iterable<String> paths) async {
    for (final path in paths) {
      if (FileSystemEntity.isDirectorySync(path)) {
        await _add(Directory(path).listSync(recursive: true).whereType<File>().map((f) => f.path));
        continue;
      }
      final ext = p.extension(path).toLowerCase();
      if (!['.pdf', '.mp4', '.m4v', '.webm'].contains(ext)) continue;
      if (items.any((i) => i.path == path)) continue;
      final it = Item(path);
      setState(() => items.add(it));
      unawaited(_thumb(it));
    }
  }

  Future<void> _thumb(Item it) async {
    try {
      if (it.type == FourType.pdf) {
        final doc = await PdfDocument.openFile(it.path);
        final page = doc.pages.first;
        final w = 240, h = (240 * page.height / page.width).round();
        final pi = await page.render(fullWidth: w.toDouble(), fullHeight: h.toDouble(), width: w, height: h);
        if (pi != null) {
          final im = img.Image.fromBytes(width: pi.width, height: pi.height, bytes: pi.pixels.buffer, order: img.ChannelOrder.bgra, numChannels: 4);
          it.thumb = img.encodeJpg(im, quality: 70);
          pi.dispose();
        }
        await doc.dispose();
      } else {
        // video: needs ffmpeg on PATH (brew install ffmpeg / winget install ffmpeg)
        final tmp = p.join(Directory.systemTemp.path, 'four_thumb_${DateTime.now().microsecondsSinceEpoch}.jpg');
        final r = await Process.run('ffmpeg', ['-y', '-ss', '2', '-i', it.path, '-frames:v', '1', '-vf', 'scale=320:-2', '-q:v', '6', tmp]);
        if (r.exitCode == 0) {
          it.thumb = await File(tmp).readAsBytes();
          await File(tmp).delete();
        }
      }
    } catch (e) {
      debugPrint('thumbnail ${it.path}: $e');
    }
    if (mounted) setState(() {});
  }

  Future<void> _pickThumb(Item it) async {
    final r = await FilePicker.pickFiles(type: FileType.image);
    final path = r.isEmpty ? null : r.first.path;
    if (path == null) return;
    final im = img.decodeImage(await File(path).readAsBytes());
    if (im == null) return;
    setState(() => it.thumb = img.encodeJpg(img.copyResize(im, width: 320), quality: 70));
  }

  void _applyBatch() => setState(() {
    for (final i in items.where((i) => i.selected)) {
      i.subject = bSubject;
      i.grade = bGrade;
      i.unit = bUnit;
    }
  });

  Future<void> _encrypt() async {
    final out = outDir ?? await FilePicker.getDirectoryPath(dialogTitle: 'Save encrypted files to…');
    if (out == null) return;
    setState(() {
      outDir = out;
      busy = true;
    });
    final (mk, _) = await KeyStore.load();
    final batch = FourBatch.create(batchCtl.text.trim().isEmpty ? 'batch' : batchCtl.text.trim());
    for (final it in items.where((i) => i.selected)) {
      setState(() => it.status = 'encrypting…');
      final meta = FourMeta(title: it.title, subject: it.subject, grade: it.grade, unit: it.unit, type: it.type, mime: it.mime);
      final dest = p.join(out, '${p.basenameWithoutExtension(it.path)}${FourMeta.extensionFor(it.type)}');
      final port = ReceivePort();
      port.listen((m) {
        if (m is double && mounted) setState(() => it.progress = m);
      });
      final send = port.sendPort, src = it.path, thumb = it.thumb, bk = batch.key, bid = batch.id;
      try {
        // heavy work off the UI thread; streams chunk by chunk so large videos never sit in RAM
        await Isolate.run(() async {
          var last = 0.0;
          await FourWriter.encryptFile(src, dest, meta: meta, masterKey: mk, batch: FourBatch(id: bid, key: bk), thumbnail: thumb, onProgress: (d, t) {
            final f = t == 0 ? 1.0 : d / t;
            if (f - last > .02 || f == 1) {
              last = f;
              send.send(f);
            }
          });
        });
        setState(() => it.status = 'done → ${p.basename(dest)}');
      } catch (e) {
        setState(() => it.status = 'failed: $e');
      } finally {
        port.close();
      }
    }
    setState(() => busy = false);
  }

  Future<void> _keyDialog() async {
    final ctl = TextEditingController();
    await showDialog<void>(
      context: context,
      builder: (c) => AlertDialog(
        title: const Text('Master key'),
        content: SizedBox(
          width: 520,
          child: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(devKey ? 'Using the DEV key (works with debug/test builds of 4).' : 'A custom key is stored in the Keychain.'),
              const SizedBox(height: 8),
              const Text('Release builds of 4 must be built with the same key: flutter build apk --dart-define=FOUR_MK=<key>. Keep it secret; anyone with it can decrypt.'),
              const SizedBox(height: 12),
              TextField(controller: ctl, decoration: const InputDecoration(labelText: 'Paste base64 key (32 bytes)')),
            ],
          ),
        ),
        actions: [
          TextButton(
            onPressed: () {
              ctl.text = base64.encode(FourKeys.random(32));
            },
            child: const Text('Generate new'),
          ),
          TextButton(
            onPressed: () async {
              await KeyStore.clear();
              if (c.mounted) Navigator.pop(c);
            },
            child: const Text('Use DEV key'),
          ),
          FilledButton(
            onPressed: () async {
              try {
                await KeyStore.save(ctl.text);
                if (c.mounted) Navigator.pop(c);
              } catch (e) {
                if (c.mounted) ScaffoldMessenger.of(c).showSnackBar(SnackBar(content: Text('$e')));
              }
            },
            child: const Text('Save to Keychain'),
          ),
        ],
      ),
    );
    final r = await KeyStore.load();
    setState(() => devKey = r.$2);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('FourEncryptor'),
        actions: [
          TextButton.icon(onPressed: _keyDialog, icon: const Icon(Icons.key), label: Text(devKey ? 'DEV key' : 'Keychain key')),
          const SizedBox(width: 8),
        ],
      ),
      body: DropTarget(
        onDragEntered: (_) => setState(() => dragging = true),
        onDragExited: (_) => setState(() => dragging = false),
        onDragDone: (d) {
          setState(() => dragging = false);
          _add(d.files.map((f) => f.path));
        },
        child: Column(
          children: [
            _batchBar(),
            const Divider(height: 1),
            Expanded(
              child: items.isEmpty
                  ? Center(
                      child: Container(
                        padding: const EdgeInsets.all(48),
                        decoration: BoxDecoration(border: Border.all(color: dragging ? Colors.orange : Colors.black26, width: 2), borderRadius: BorderRadius.circular(16)),
                        child: const Text('Drop PDFs or videos (or a folder) here', style: TextStyle(fontSize: 18)),
                      ),
                    )
                  : ListView.builder(itemCount: items.length, itemBuilder: (_, i) => _row(items[i])),
            ),
          ],
        ),
      ),
      bottomNavigationBar: Padding(
        padding: const EdgeInsets.all(12),
        child: Row(
          children: [
            OutlinedButton.icon(
              onPressed: busy
                  ? null
                  : () async {
                      final r = await FilePicker.pickFiles(type: FileType.custom, allowedExtensions: ['pdf', 'mp4', 'm4v', 'webm']);
                      _add([for (final f in r) ?f.path]);
                    },
              icon: const Icon(Icons.add),
              label: const Text('Add files'),
            ),
            const SizedBox(width: 12),
            Expanded(child: Text(outDir == null ? 'Output folder: ask on Encrypt' : 'Output: $outDir', overflow: TextOverflow.ellipsis)),
            FilledButton.icon(onPressed: busy || items.isEmpty ? null : _encrypt, icon: const Icon(Icons.lock), label: Text(busy ? 'Encrypting…' : 'Encrypt selected')),
          ],
        ),
      ),
    );
  }

  Widget _batchBar() => Padding(
    padding: const EdgeInsets.all(12),
    child: Wrap(
      spacing: 12,
      runSpacing: 8,
      crossAxisAlignment: WrapCrossAlignment.center,
      children: [
        SizedBox(width: 200, child: TextField(controller: batchCtl, decoration: const InputDecoration(labelText: 'Batch id'))),
        DropdownButton<String>(value: bSubject, items: [for (final s in kSubjects) DropdownMenuItem(value: s, child: Text(s))], onChanged: (v) => setState(() => bSubject = v!)),
        DropdownButton<int>(value: bGrade, items: [for (final g in [9, 10, 11, 12]) DropdownMenuItem(value: g, child: Text('Grade $g'))], onChanged: (v) => setState(() => bGrade = v!)),
        SizedBox(width: 90, child: TextField(decoration: const InputDecoration(labelText: 'Unit'), onChanged: (v) => bUnit = v)),
        OutlinedButton(onPressed: _applyBatch, child: const Text('Apply to selected')),
      ],
    ),
  );

  Widget _row(Item it) => Card(
    margin: const EdgeInsets.symmetric(horizontal: 12, vertical: 4),
    child: Padding(
      padding: const EdgeInsets.all(8),
      child: Row(
        children: [
          Checkbox(value: it.selected, onChanged: (v) => setState(() => it.selected = v!)),
          GestureDetector(
            onTap: () => _pickThumb(it),
            child: SizedBox(width: 56, height: 72, child: it.thumb == null ? const Icon(Icons.image_outlined) : Image.memory(it.thumb!, fit: BoxFit.cover)),
          ),
          const SizedBox(width: 12),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                TextFormField(initialValue: it.title, decoration: const InputDecoration(labelText: 'Title', isDense: true), onChanged: (v) => it.title = v),
                const SizedBox(height: 4),
                Wrap(
                  spacing: 10,
                  crossAxisAlignment: WrapCrossAlignment.center,
                  children: [
                    DropdownButton<String>(value: kSubjects.contains(it.subject) ? it.subject : 'general', items: [for (final s in kSubjects) DropdownMenuItem(value: s, child: Text(s))], onChanged: (v) => setState(() => it.subject = v!)),
                    DropdownButton<int>(value: it.grade, items: [for (final g in [9, 10, 11, 12]) DropdownMenuItem(value: g, child: Text('G$g'))], onChanged: (v) => setState(() => it.grade = v!)),
                    SizedBox(width: 70, child: TextFormField(key: ValueKey('u${it.path}${it.unit}'), initialValue: it.unit, decoration: const InputDecoration(labelText: 'Unit', isDense: true), onChanged: (v) => it.unit = v)),
                    DropdownButton<FourType>(value: it.type, items: [for (final t in FourType.values) DropdownMenuItem(value: t, child: Text(t.name))], onChanged: (v) => setState(() => it.type = v!)),
                    Text(it.status, style: const TextStyle(fontSize: 12)),
                  ],
                ),
                if (it.progress > 0 && it.progress < 1) LinearProgressIndicator(value: it.progress),
              ],
            ),
          ),
          IconButton(onPressed: busy ? null : () => setState(() => items.remove(it)), icon: const Icon(Icons.close)),
        ],
      ),
    ),
  );
}

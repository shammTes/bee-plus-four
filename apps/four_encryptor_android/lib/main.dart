// 4 Encryptor (Android): PDFs, 16:9 videos, reels and offline web pages → .4pdf/.4vid/.4reel/.4web for the 4 app.
// No decrypt path: the app only writes containers. Files stream through in 256 KiB chunks (never whole in RAM).
import 'dart:async';
import 'dart:io';

import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:four_format/four_format.dart';

import 'src/core.dart';
import 'src/io.dart';
import 'src/labx.dart';
import 'src/log.dart';
import 'src/master_key.dart';
import 'src/web_mirror.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await AppLog.init();
  FlutterError.onError = (d) {
    AppLog.log('flutter error: ${d.exceptionAsString()}');
    FlutterError.presentError(d);
  };
  WidgetsBinding.instance.platformDispatcher.onError = (e, st) {
    AppLog.log('uncaught: $e\n$st');
    return true;
  };
  AppLog.log('start · ${AppLog.device} · keys: 4 ${KeyTarget.four.isDev ? 'DEV' : 'FOUR_MK'}, Bee Plus ${KeyTarget.bee.isDev ? 'DEV' : 'BEE_MK'}');
  AppLog.log(await cryptoSelfTest());
  try {
    for (final t in KeyTarget.values) {
      AppLog.log('${t.label}: ${await fourSelfTest(await MasterKey.load(t))}');
    }
  } catch (e) {
    selfTestError = 'Master key: $e';
    AppLog.log('master key failed: $e');
  }
  runApp(const EncryptorApp());
}

/// Human-readable error text: PlatformException message (native step + exception) and the first stack lines.
String describeError(Object e, [StackTrace? st]) {
  if (e is PlatformException) {
    final d = e.details is String ? (e.details as String).split('\n').take(8).join('\n') : '';
    return '${e.message ?? e.code}${d.isEmpty ? '' : '\n$d'}';
  }
  final top = st == null ? '' : st.toString().split('\n').take(6).join('\n');
  return '${e.runtimeType}: $e${top.isEmpty ? '' : '\n$top'}';
}


class EncryptorApp extends StatelessWidget {
  const EncryptorApp({super.key});
  @override
  Widget build(BuildContext context) => MaterialApp(
    title: '4 Encryptor',
    debugShowCheckedModeBanner: false,
    theme: ThemeData(colorSchemeSeed: const Color(0xFFE88A6E), useMaterial3: true, visualDensity: VisualDensity.compact),
    home: const HomePage(),
  );
}

class HomePage extends StatefulWidget {
  const HomePage({super.key});
  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  final jobs = <Job>[];
  String? outTree, outName;
  bool busy = false;
  String fp = '';
  double overall = 0;

  @override
  void initState() {
    super.initState();
    _loadFp();
  }

  void _loadFp() {
    MasterKey.fingerprint().then((f) => mounted ? setState(() => fp = f) : null);
  }

  void _snack(String m) => ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(m)));

  // ---------- adding
  Future<void> _addFiles() async {
    final picked = await Io.pickFiles();
    for (final p in picked) {
      final mime = p.mime.isEmpty ? guessMime(p.name) : p.mime;
      final t = detectType(p.name, mime);
      if (t == null) {
        _snack('${p.name}: not a PDF, video or .zip');
        continue;
      }
      final j = Job(uri: p.uri, name: p.name, size: p.size, mime: mime, type: t)..title = _titleFrom(p.name);
      setState(() => jobs.add(j));
      if (t == FourType.web) {
        await _prepareZip(j);
      } else {
        unawaited(_probe(j));
      }
    }
  }

  String _titleFrom(String name) {
    final i = name.lastIndexOf('.');
    return (i > 0 ? name.substring(0, i) : name).replaceAll(RegExp(r'[_-]+'), ' ').trim();
  }

  Future<void> _probe(Job j) async {
    try {
      final m = await Io.probe(j.uri, j.mime);
      j.thumb = m['thumb'] as dynamic;
      j.durationMs = (m['durationMs'] as num?)?.toInt();
      j.pages = (m['pages'] as num?)?.toInt();
      j.portrait = m['portrait'] == true;
      if (j.mime.startsWith('video/') && j.portrait && j.type == FourType.video) j.type = FourType.reel; // auto-detect
      AppLog.log('probe ${j.name}: mime=${j.mime} size=${j.size} dur=${j.durationMs} portrait=${j.portrait} thumb=${j.thumb?.length}');
    } catch (e) {
      AppLog.log('probe ${j.name} failed (not fatal): ${describeError(e)}');
    }
    if (mounted) setState(() {});
  }

  Future<void> _prepareZip(Job j) async {
    try {
      final e = bundleEntry(await Io.zipEntries(j.uri));
      if (e == null) throw const FormatException('no .html page inside');
      setState(() {
        j.entry = e;
        j.thirdParty = true; // ask for the licence of web pages
      });
    } catch (e) {
      setState(() => jobs.remove(j));
      _snack('${j.name}: $e');
    }
  }

  Future<void> _addWebFolder() async {
    final tree = await Io.pickBundleFolder();
    if (tree == null) return;
    setState(() => busy = true);
    try {
      final r = await Io.zipFolder(tree);
      final entries = (r['entries'] as List).cast<String>();
      final e = bundleEntry(entries);
      final path = r['path'] as String;
      if (e == null) {
        await Io.deleteTemp(path);
        throw const FormatException('no .html page in that folder');
      }
      final name = '${r['name']}.zip';
      final j = Job(uri: path, name: name, size: await File(path).length(), mime: 'application/zip', type: FourType.web, tempPath: path)
        ..title = _titleFrom(name)
        ..entry = e
        ..thirdParty = true;
      setState(() => jobs.add(j));
    } catch (e) {
      _snack('Folder: $e');
    } finally {
      setState(() => busy = false);
    }
  }

  Future<void> _importLabx() async {
    final ctl = TextEditingController();
    final url = await showDialog<String>(
      context: context,
      builder: (c) => AlertDialog(
        title: const Text('Import from LabXchange'),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            TextField(controller: ctl, decoration: const InputDecoration(hintText: 'https://www.labxchange.org/library/items/lb:…'), autofocus: true),
            const SizedBox(height: 8),
            const Text('Only CC BY, CC BY-SA, CC0 and public-domain items can be packed (4 is a paid app). NC, LabXchange Standard License and "all rights reserved" are refused.', style: TextStyle(fontSize: 12)),
          ],
        ),
        actions: [TextButton(onPressed: () => Navigator.pop(c), child: const Text('Cancel')), FilledButton(onPressed: () => Navigator.pop(c, ctl.text), child: const Text('Import'))],
      ),
    );
    if (url == null || url.trim().isEmpty) return;
    setState(() => busy = true);
    final lx = Labx();
    String? tmp;
    try {
      final it = await lx.resolve(url);
      final why = Labx.refusal(it);
      if (why != null) {
        if (mounted) await _info('Cannot import "${it.title}"', '$why\n\nLicence on LabXchange: ${it.licence.label}${it.author.isEmpty ? '' : '\nBy: ${it.author}'}');
        return;
      }
      final dir = await Io.tempDir();
      final type = it.fourType!;
      final Job j;
      if (type == FourType.web) {
        final m = WebMirror(onProgress: (n, b, cur) => _status('Downloading page: $n files, ${fmtSize(b)}'));
        try {
          final (r, files) = await m.mirror(Uri.parse(it.contentUrl!));
          final d = Directory('$dir/${it.id.replaceAll(RegExp(r'[^A-Za-z0-9]'), '_')}');
          if (await d.exists()) await d.delete(recursive: true);
          await WebMirror.writeTo(d, files);
          final z = await Io.zipFiles(d.path);
          tmp = z['path'] as String;
          j = Job(uri: tmp, name: '${_safe(it.title)}.zip', size: await File(tmp).length(), mime: 'application/zip', type: type, tempPath: tmp)..entry = r.entry;
          if (r.unresolved.isNotEmpty || r.external.isNotEmpty) {
            unawaited(_info('Check it offline', 'Saved ${r.files.length} files (${fmtSize(r.totalBytes)}).\n'
                '${r.unresolved.isEmpty ? '' : '${r.unresolved.length} file(s) could not be downloaded.\n'}'
                '${r.external.isEmpty ? '' : 'The page also talks to: ${r.external.take(6).join(', ')}. Parts that load from there will not work offline.\n'}'
                'Open the .4web in 4 with Wi-Fi off before sharing it.'));
          }
        } finally {
          m.close();
        }
      } else {
        final ext = type == FourType.pdf ? '.pdf' : '.mp4';
        tmp = '$dir/labx_${DateTime.now().millisecondsSinceEpoch}$ext';
        await lx.download(it.contentUrl!, File(tmp), onProgress: (d, t) => _status('Downloading ${fmtSize(d)}${t > 0 ? ' / ${fmtSize(t)}' : ''}'));
        j = Job(uri: tmp, name: '${_safe(it.title)}$ext', size: await File(tmp).length(), mime: it.mime, type: type, tempPath: tmp);
      }
      j
        ..title = it.title
        ..thirdParty = true
        ..locked = true
        ..licence = it.licence
        ..author = it.author
        ..source = 'LabXchange'
        ..sourceUrl = it.pageUrl;
      tmp = null;
      setState(() => jobs.add(j));
      if (type != FourType.web) unawaited(_probe(j));
    } catch (e) {
      _snack('LabXchange: $e');
      if (tmp != null) await Io.deleteTemp(tmp);
    } finally {
      lx.close();
      if (mounted) setState(() => busy = false);
      _status(null);
    }
  }

  String _safe(String s) => s.replaceAll(RegExp(r'[\\/:*?"<>|]+'), ' ').trim().replaceAll(RegExp(r'\s+'), '_');

  String? statusLine;
  void _status(String? s) {
    if (mounted) setState(() => statusLine = s);
  }

  Future<void> _info(String title, String body) => showDialog<void>(
    context: context,
    builder: (c) => AlertDialog(title: Text(title), content: SingleChildScrollView(child: Text(body)), actions: [TextButton(onPressed: () => Navigator.pop(c), child: const Text('OK'))]),
  );

  // ---------- output + encrypt
  Future<bool> _ensureFolder() async {
    if (outTree != null && await Io.hasFolder(outTree!)) return true;
    final t = await Io.pickFolder();
    if (t == null) return false;
    final n = await Io.folderName(t);
    setState(() {
      outTree = t;
      outName = n;
    });
    return true;
  }

  Future<void> _encrypt() async {
    final todo = jobs.where((j) => !j.done).toList();
    for (final j in todo) {
      final r = j.refusal;
      if (r != null) {
        await _info('"${j.title}" cannot be encrypted', r);
        return;
      }
    }
    if (todo.isEmpty || !await _ensureFolder()) return;
    setState(() => busy = true);
    final mk = await MasterKey.load();
    final target = MasterKey.target;
    AppLog.log('batch target ${target.label} (${target.isDev ? 'DEV' : target.defineName}, fp $fp)');
    final batch = FourBatch.create(newBatchId());
    final total = todo.fold<int>(0, (a, j) => a + (j.size > 0 ? j.size : 1));
    var before = 0;
    for (final j in todo) {
      setState(() {
        j.status = 'Encrypting…';
        j.error = null;
        j.errorDetails = null;
      });
      SafSource? src;
      SafSink? out;
      var ok = false;
      var step = 'open the input file';
      final sw = Stopwatch()..start();
      try {
        src = await SafSource.open(j.uri);
        AppLog.log('encrypt ${j.name}: type=${j.type.name} size=${src.length} (picker said ${j.size}) read=${src.mode}');
        step = 'create ${j.outFileName} in the output folder';
        out = await SafSink.create(outTree!, j.outFileName);
        step = 'encrypt';
        var last = DateTime.now();
        var chunk = 0;
        await encryptStream(
          input: _StepSource(src, (off) => step = 'read + encrypt chunk ${chunk = off ~/ FourFormat.defaultChunk} (byte $off)'),
          add: (b) {
            step = 'write chunk $chunk to the output file';
            return out!.add(b);
          },
          meta: j.meta(),
          masterKey: mk,
          batch: batch,
          thumb: j.thumb,
          onProgress: (d, t) {
            final now = DateTime.now();
            if (now.difference(last).inMilliseconds < 150 && d < t) return;
            last = now;
            setState(() {
              j.progress = t == 0 ? 1 : d / t;
              overall = (before + d) / total;
            });
          },
        );
        step = 'finish writing the output file';
        ok = true;
        await out.close(ok: true);
        AppLog.log('done ${j.name} → ${out.name} in ${sw.elapsedMilliseconds} ms');
        setState(() {
          j.outUri = out!.uri;
          j.outName = out.name;
          j.progress = 1;
          j.status = 'Done → ${out.name}';
        });
        if (j.tempPath != null) await Io.deleteTemp(j.tempPath!);
      } catch (e, st) {
        if (out != null && !ok) {
          try {
            await out.close(ok: false);
          } catch (_) {}
        }
        final msg = describeError(e, st);
        final details = 'File: ${j.name} (${fmtSize(j.size)}, ${j.mime}, ${j.type.name})\nFailed step: $step\nError: $msg\nDevice: ${AppLog.device}\nApp: 4 Encryptor 1.1.0, target ${MasterKey.target.label}, key ${MasterKey.isDev ? 'DEV' : MasterKey.target.defineName}';
        AppLog.log('FAILED ${j.name} at "$step": $msg');
        setState(() {
          j.error = 'Could not $step: ${msg.split('\n').first}';
          j.errorDetails = details;
          j.status = 'Failed';
          j.progress = 0;
        });
      } finally {
        try {
          await src?.close();
        } catch (_) {}
      }
      before += j.size > 0 ? j.size : 1;
    }
    setState(() {
      busy = false;
      overall = 0;
    });
    final n = todo.where((j) => j.done).length;
    _snack('$n of ${todo.length} encrypted into $outName');
  }

  Future<void> _showLog() async {
    final text = await AppLog.read();
    if (!mounted) return;
    await showDialog<void>(
      context: context,
      builder: (c) => AlertDialog(
        title: const Text('Log'),
        content: SizedBox(width: double.maxFinite, child: SingleChildScrollView(reverse: true, child: SelectableText(text.isEmpty ? '(empty)' : text, style: const TextStyle(fontSize: 11, fontFamily: 'monospace')))),
        actions: [
          TextButton(onPressed: () => Clipboard.setData(ClipboardData(text: '${AppLog.device}\n$text')), child: const Text('Copy')),
          TextButton(onPressed: AppLog.share, child: const Text('Share')),
          TextButton(onPressed: () => Navigator.pop(c), child: const Text('Close')),
        ],
      ),
    );
  }

  Future<void> _remove(Job j) async {
    if (j.tempPath != null && !j.done) await Io.deleteTemp(j.tempPath!);
    setState(() => jobs.remove(j));
  }

  // ---------- UI
  @override
  Widget build(BuildContext context) {
    final doneUris = [for (final j in jobs) if (j.outUri != null) j.outUri!];
    final pending = jobs.where((j) => !j.done).length;
    return Scaffold(
      appBar: AppBar(
        title: const Text('4 Encryptor'),
        actions: [
          IconButton(tooltip: 'Log', icon: const Icon(Icons.receipt_long_outlined), onPressed: _showLog),
          Padding(
            padding: const EdgeInsets.only(right: 8),
            child: ActionChip(
              avatar: Icon(MasterKey.isDev ? Icons.science_outlined : Icons.verified_user_outlined, size: 18),
              label: Text(MasterKey.isDev ? 'DEV key' : 'Release key'),
              onPressed: () {
                final t = MasterKey.target;
                _info(
                  'Master key · ${t.label}',
                  MasterKey.isDev
                      ? 'This build uses the public ${t.label} DEV key (no ${t.defineName}). Files open in builds of ${t.label} made without ${t.defineName} (test builds).\n\nFingerprint: $fp'
                      : 'This build carries ${t.defineName}. Files open only in ${t.label} builds made with the same ${t.defineName}.\n\nFingerprint: $fp',
                );
              },
            ),
          ),
        ],
      ),
      body: Column(
        children: [
          // Which app the files are for: 4 and Bee Plus use different master keys (files are not interchangeable).
          Padding(
            padding: const EdgeInsets.fromLTRB(12, 8, 12, 4),
            child: Row(
              children: [
                const Text('Files for'),
                const SizedBox(width: 10),
                Expanded(
                  child: SegmentedButton<KeyTarget>(
                    segments: [for (final t in KeyTarget.values) ButtonSegment(value: t, label: Text(t.label))],
                    selected: {MasterKey.target},
                    onSelectionChanged: busy
                        ? null
                        : (v) {
                            setState(() {
                              MasterKey.target = v.first;
                              fp = '';
                              // subjects / grades differ per app: clear values the new target does not have
                              for (final j in jobs.where((j) => !j.done)) {
                                if (!MasterKey.target.subjects.contains(j.subject)) j.subject = '';
                                if (!MasterKey.target.grades.contains(j.grade)) j.grade = 0;
                              }
                            });
                            AppLog.log('target → ${MasterKey.target.label}');
                            _loadFp();
                          },
                  ),
                ),
              ],
            ),
          ),
          if (selfTestError != null)
            MaterialBanner(
              backgroundColor: Colors.red.withValues(alpha: .08),
              content: SelectableText('$selfTestError\nEncrypting will not work on this phone. Please share the log.', style: const TextStyle(color: Colors.red)),
              actions: [TextButton(onPressed: AppLog.share, child: const Text('Share log'))],
            ),
          if (busy) LinearProgressIndicator(value: overall > 0 ? overall : null),
          if (statusLine != null) Padding(padding: const EdgeInsets.all(8), child: Text(statusLine!)),
          Expanded(
            child: jobs.isEmpty
                ? _empty()
                : ListView.builder(padding: const EdgeInsets.only(bottom: 16), itemCount: jobs.length, itemBuilder: (_, i) => _JobCard(job: jobs[i], busy: busy, onChanged: () => setState(() {}), onRemove: () => _remove(jobs[i]))),
          ),
        ],
      ),
      bottomNavigationBar: SafeArea(
        child: Padding(
          padding: const EdgeInsets.fromLTRB(12, 4, 12, 8),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              Row(
                children: [
                  const Icon(Icons.folder_outlined, size: 18),
                  const SizedBox(width: 6),
                  Expanded(child: Text(outName == null ? 'Output folder: choose on Encrypt' : 'Output: $outName', overflow: TextOverflow.ellipsis)),
                  TextButton(
                    onPressed: busy
                        ? null
                        : () async {
                            final t = await Io.pickFolder();
                            if (t != null) {
                              final n = await Io.folderName(t);
                              setState(() {
                                outTree = t;
                                outName = n;
                              });
                            }
                          },
                    child: const Text('Change'),
                  ),
                ],
              ),
              Row(
                children: [
                  OutlinedButton.icon(onPressed: busy ? null : _addFiles, icon: const Icon(Icons.add), label: const Text('Add files')),
                  PopupMenuButton<int>(
                    enabled: !busy,
                    icon: const Icon(Icons.more_vert),
                    onSelected: (v) => v == 0 ? _addWebFolder() : _importLabx(),
                    itemBuilder: (_) => const [
                      PopupMenuItem(value: 0, child: Text('Add web page folder…')),
                      PopupMenuItem(value: 1, child: Text('Import LabXchange link…')),
                    ],
                  ),
                  const Spacer(),
                  if (doneUris.isNotEmpty)
                    IconButton.filledTonal(onPressed: () => Io.share(doneUris), icon: const Icon(Icons.share), tooltip: 'Share encrypted files'),
                  const SizedBox(width: 6),
                  FilledButton.icon(onPressed: busy || pending == 0 ? null : _encrypt, icon: const Icon(Icons.lock), label: Text(busy ? 'Working…' : 'Encrypt $pending')),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _empty() => Center(
    child: Padding(
      padding: const EdgeInsets.all(32),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(Icons.lock_outline, size: 56, color: Theme.of(context).colorScheme.primary),
          const SizedBox(height: 12),
          const Text('Add PDFs, videos or a web page (.zip / folder).', textAlign: TextAlign.center),
          const SizedBox(height: 4),
          const Text('Encrypted files open only in 4 on phones unlocked by QR.', textAlign: TextAlign.center, style: TextStyle(fontSize: 12)),
        ],
      ),
    ),
  );
}

class _ErrorBox extends StatelessWidget {
  const _ErrorBox({required this.job});
  final Job job;
  @override
  Widget build(BuildContext context) => Container(
    margin: const EdgeInsets.only(top: 6),
    padding: const EdgeInsets.all(8),
    decoration: BoxDecoration(color: Colors.red.withValues(alpha: .07), borderRadius: BorderRadius.circular(8)),
    child: Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        SelectableText(job.error!, style: const TextStyle(color: Colors.red, fontSize: 12.5)),
        if (job.errorDetails != null) SelectableText(job.errorDetails!, maxLines: 6, style: const TextStyle(fontSize: 11)),
        Row(
          children: [
            TextButton.icon(
              onPressed: () {
                Clipboard.setData(ClipboardData(text: job.errorDetails ?? job.error!));
                ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Error details copied')));
              },
              icon: const Icon(Icons.copy, size: 16),
              label: const Text('Copy error details'),
            ),
            TextButton.icon(onPressed: AppLog.share, icon: const Icon(Icons.share, size: 16), label: const Text('Share log')),
          ],
        ),
      ],
    ),
  );
}

/// Wraps the input so the UI knows which chunk failed.
class _StepSource extends FourSource {
  _StepSource(this.inner, this.onRead);
  final FourSource inner;
  final void Function(int off) onRead;
  @override
  int get length => inner.length;
  @override
  Future<Uint8List> read(int offset, int len) {
    onRead(offset);
    return inner.read(offset, len);
  }
}

class _JobCard extends StatelessWidget {
  const _JobCard({required this.job, required this.busy, required this.onChanged, required this.onRemove});
  final Job job;
  final bool busy;
  final VoidCallback onChanged, onRemove;

  @override
  Widget build(BuildContext context) {
    final j = job;
    final editable = !busy && !j.done;
    final types = j.type == FourType.web ? const [FourType.web] : (j.mime == 'application/pdf' ? const [FourType.pdf] : const [FourType.video, FourType.reel]);
    return Card(
      margin: const EdgeInsets.fromLTRB(10, 6, 10, 0),
      child: Padding(
        padding: const EdgeInsets.all(10),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                ClipRRect(
                  borderRadius: BorderRadius.circular(6),
                  child: SizedBox(
                    width: 52,
                    height: 52,
                    child: j.thumb != null ? Image.memory(j.thumb!, fit: BoxFit.cover, cacheWidth: 104) : ColoredBox(color: Colors.black12, child: Icon(_icon(j.type))),
                  ),
                ),
                const SizedBox(width: 10),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(j.name, maxLines: 1, overflow: TextOverflow.ellipsis, style: const TextStyle(fontWeight: FontWeight.w600)),
                      Text([fmtSize(j.size), if (j.durationMs != null) _dur(j.durationMs!), if (j.pages != null) '${j.pages} pages', if (j.type == FourType.web) j.entry].join(' · '), style: const TextStyle(fontSize: 12)),
                      Text(j.status, style: TextStyle(fontSize: 12, color: j.error != null ? Colors.red : (j.done ? Colors.green.shade700 : null))),
                    ],
                  ),
                ),
                IconButton(onPressed: busy ? null : onRemove, icon: const Icon(Icons.close), tooltip: 'Remove'),
              ],
            ),
            if (j.progress > 0 && j.progress < 1) Padding(padding: const EdgeInsets.only(top: 6), child: LinearProgressIndicator(value: j.progress)),
            if (j.error != null) _ErrorBox(job: j),
            if (!j.done) ...[
              const SizedBox(height: 6),
              if (types.length > 1)
                SegmentedButton<FourType>(
                  segments: [for (final t in types) ButtonSegment(value: t, label: Text(t == FourType.video ? 'Video 16:9' : 'Reel 9:16'))],
                  selected: {j.type},
                  onSelectionChanged: editable ? (s) {
                        j.type = s.first;
                        onChanged();
                      } : null,
                ),
              TextFormField(
                key: ValueKey('t${j.uri}'),
                initialValue: j.title,
                enabled: editable,
                decoration: const InputDecoration(labelText: 'Title', isDense: true),
                onChanged: (v) => j.title = v,
              ),
              Row(
                children: [
                  Expanded(
                    flex: 3,
                    child: DropdownButtonFormField<String>(
                      key: ValueKey('s${j.uri}|${MasterKey.target.name}'),
                      initialValue: MasterKey.target.subjects.contains(j.subject) ? j.subject : '',
                      isExpanded: true,
                      decoration: const InputDecoration(labelText: 'Subject', isDense: true),
                      items: [for (final s in MasterKey.target.subjects) DropdownMenuItem(value: s, child: Text(s.isEmpty ? '—' : s.replaceAll('_', ' ')))],
                      onChanged: editable ? (v) {
                        j.subject = v ?? '';
                        onChanged();
                      } : null,
                    ),
                  ),
                  const SizedBox(width: 8),
                  Expanded(
                    flex: 2,
                    child: DropdownButtonFormField<int>(
                      key: ValueKey('g${j.uri}|${MasterKey.target.name}'),
                      initialValue: j.grade,
                      decoration: const InputDecoration(labelText: 'Grade', isDense: true),
                      items: [for (final g in {...MasterKey.target.grades, j.grade}) DropdownMenuItem(value: g, child: Text(g == 0 ? '—' : '$g'))],
                      onChanged: editable ? (v) {
                        j.grade = v ?? 0;
                        onChanged();
                      } : null,
                    ),
                  ),
                  const SizedBox(width: 8),
                  Expanded(
                    flex: 2,
                    child: TextFormField(
                      key: ValueKey('u${j.uri}'),
                      initialValue: j.unit,
                      enabled: editable,
                      decoration: const InputDecoration(labelText: 'Unit', isDense: true),
                      onChanged: (v) => j.unit = v,
                    ),
                  ),
                ],
              ),
              _licence(context, j, editable),
            ],
          ],
        ),
      ),
    );
  }

  Widget _licence(BuildContext context, Job j, bool editable) {
    final refusal = j.refusal;
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        if (!j.locked)
          CheckboxListTile(
            contentPadding: EdgeInsets.zero,
            dense: true,
            value: j.thirdParty,
            onChanged: editable ? (v) {
                        j.thirdParty = v ?? false;
                        onChanged();
                      } : null,
            title: const Text('Made by someone else (needs a licence and credit)'),
          ),
        if (j.thirdParty) ...[
          if (j.locked)
            Text('${j.source}: ${j.licence.label}${j.author.isEmpty ? '' : ' · ${j.author}'}', style: const TextStyle(fontSize: 12))
          else ...[
            DropdownButtonFormField<String>(
              initialValue: j.licence.id.isEmpty ? null : j.licence.id,
              isExpanded: true,
              decoration: const InputDecoration(labelText: 'Licence (as shown on the source page)', isDense: true),
              items: [for (final l in FourLicence.choices) DropdownMenuItem(value: l.id, child: Text(l.label))],
              onChanged: editable ? (v) {
                        j.licence = FourLicence.byId(v ?? '');
                        onChanged();
                      } : null,
            ),
            TextFormField(key: ValueKey('a${j.uri}'), initialValue: j.author, enabled: editable, decoration: const InputDecoration(labelText: 'Author / organisation', isDense: true), onChanged: (v) => j.author = v),
            TextFormField(key: ValueKey('s${j.uri}'), initialValue: j.sourceUrl, enabled: editable, decoration: const InputDecoration(labelText: 'Source URL', isDense: true), onChanged: (v) => j.sourceUrl = v),
          ],
          if (refusal != null) Padding(padding: const EdgeInsets.only(top: 4), child: Text(refusal, style: const TextStyle(color: Colors.red, fontSize: 12))),
        ],
      ],
    );
  }

  static IconData _icon(FourType t) => switch (t) {
    FourType.pdf => Icons.picture_as_pdf_outlined,
    FourType.video => Icons.movie_outlined,
    FourType.reel => Icons.stay_current_portrait,
    FourType.web => Icons.language,
  };

  static String _dur(int ms) => '${ms ~/ 60000}:${((ms ~/ 1000) % 60).toString().padLeft(2, '0')}';
}

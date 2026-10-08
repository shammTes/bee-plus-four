// 4 Encryptor (Android): PDFs, 16:9 videos, reels and offline web pages → .4pdf/.4vid/.4reel/.4web for the 4 app.
// No decrypt path: the app only writes containers. Files stream through in 256 KiB chunks (never whole in RAM).
import 'dart:async';
import 'dart:io';

import 'package:flutter/material.dart';
import 'package:four_format/four_format.dart';

import 'src/core.dart';
import 'src/io.dart';
import 'src/labx.dart';
import 'src/master_key.dart';
import 'src/web_mirror.dart';

void main() => runApp(const EncryptorApp());

const kSubjects = ['', 'agriculture', 'biology', 'business_economics', 'chemistry', 'civics', 'english', 'geography', 'history', 'ict', 'mathematics', 'physics', 'tigrinya', 'general'];

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
    } catch (e) {
      debugPrint('probe ${j.name}: $e');
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
    final batch = FourBatch.create(newBatchId());
    final total = todo.fold<int>(0, (a, j) => a + (j.size > 0 ? j.size : 1));
    var before = 0;
    for (final j in todo) {
      setState(() {
        j.status = 'Encrypting…';
        j.error = null;
      });
      SafSource? src;
      SafSink? out;
      var ok = false;
      try {
        src = await SafSource.open(j.uri);
        out = await SafSink.create(outTree!, j.outFileName);
        var last = DateTime.now();
        await encryptStream(
          input: src,
          add: out.add,
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
        ok = true;
        await out.close(ok: true);
        setState(() {
          j.outUri = out!.uri;
          j.outName = out.name;
          j.progress = 1;
          j.status = 'Done → ${out.name}';
        });
        if (j.tempPath != null) await Io.deleteTemp(j.tempPath!);
      } catch (e) {
        if (out != null && !ok) {
          try {
            await out.close(ok: false);
          } catch (_) {}
        }
        setState(() {
          j.error = '$e';
          j.status = 'Failed: $e';
          j.progress = 0;
        });
      } finally {
        await src?.close();
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
          Padding(
            padding: const EdgeInsets.only(right: 8),
            child: ActionChip(
              avatar: Icon(MasterKey.isDev ? Icons.science_outlined : Icons.verified_user_outlined, size: 18),
              label: Text(MasterKey.isDev ? 'DEV key' : 'Release key'),
              onPressed: () => _info(
                'Master key',
                MasterKey.isDev
                    ? 'This build uses the public DEV key (no FOUR_MK). Files open in builds of 4 made without FOUR_MK (the current test builds).\n\nFingerprint: $fp'
                    : 'This build carries FOUR_MK. Files open only in 4 builds made with the same FOUR_MK.\n\nFingerprint: $fp',
              ),
            ),
          ),
        ],
      ),
      body: Column(
        children: [
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
                      initialValue: kSubjects.contains(j.subject) ? j.subject : '',
                      isExpanded: true,
                      decoration: const InputDecoration(labelText: 'Subject', isDense: true),
                      items: [for (final s in kSubjects) DropdownMenuItem(value: s, child: Text(s.isEmpty ? '—' : s.replaceAll('_', ' ')))],
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
                      initialValue: j.grade,
                      decoration: const InputDecoration(labelText: 'Grade', isDense: true),
                      items: [for (final g in [0, 9, 10, 11, 12]) DropdownMenuItem(value: g, child: Text(g == 0 ? '—' : '$g'))],
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

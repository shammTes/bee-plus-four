// LabXchange import: item URL → metadata (title, licence, authors/partner) via the public LabXchange API,
// then the content: a PDF (documents), an MP4 when one is offered (videos; YouTube-only videos are refused),
// or an offline mirror of a simulation/interactive page (see web_mirror.dart). Pure dart:io.
import 'dart:convert';
import 'dart:io';

import 'package:four_format/four_format.dart';

const kLabxApi = 'https://api.www.labxchange.org/api/v1';

class LabxItem {
  LabxItem({required this.id, required this.title, required this.kind, required this.licenceRaw, required this.author, required this.pageUrl, this.contentUrl, this.mime = '', this.youtubeOnly = false});
  final String id, title, kind, licenceRaw, author, pageUrl;

  /// PDF / MP4 / interactive entry page; null when nothing downloadable.
  final String? contentUrl;
  final String mime;
  final bool youtubeOnly;

  /// LabXchange "LX1" = LabXchange Standard License (ToS: personal, non-commercial use on the site only).
  FourLicence get licence => licenceRaw == 'LX1' ? FourLicence.lx1 : FourLicence.parse(licenceRaw);

  FourType? get fourType => switch (kind) {
    'document' => mime == 'application/pdf' ? FourType.pdf : null,
    'video' => contentUrl == null ? null : FourType.video,
    'simulation' || 'interactive' => contentUrl == null ? null : FourType.web,
    _ => null,
  };

  String get credit => [if (author.isNotEmpty) author, 'LabXchange', licence.label].join(' · ');
}

class LabxException implements Exception {
  LabxException(this.message);
  final String message;
  @override
  String toString() => message;
}

class Labx {
  Labx({HttpClient? client}) : _http = client ?? (HttpClient()..connectionTimeout = const Duration(seconds: 20));
  final HttpClient _http;

  /// `https://www.labxchange.org/library/items/lb:LabXchange:9e246666:lx_simulation:1?fullscreen=true` → item id.
  static String? itemId(String url) {
    final m = RegExp(r'(lb:[A-Za-z0-9_-]+:[0-9a-f]+:[a-z_]+:\d+)').firstMatch(Uri.decodeFull(url.trim()));
    return m?.group(1);
  }

  Future<Map<String, dynamic>> _json(String url) async {
    final rq = await _http.getUrl(Uri.parse(url));
    rq.headers.set('Accept', 'application/json');
    final rs = await rq.close();
    final body = await rs.transform(utf8.decoder).join();
    if (rs.statusCode != 200) throw LabxException('LabXchange answered ${rs.statusCode} for $url');
    return (jsonDecode(body) as Map).cast<String, dynamic>();
  }

  Future<LabxItem> resolve(String url) async {
    final id = itemId(url);
    if (id == null) throw LabxException('Not a LabXchange item link (expected …/library/items/lb:LabXchange:…)');
    final m = (await _json('$kLabxApi/items/${Uri.encodeComponent(id)}'))['metadata'] as Map<String, dynamic>;
    final authors = [for (final a in (m['authors'] as List? ?? const [])) ((a as Map)['full_name'] ?? a['fullName'] ?? a['username'] ?? '').toString()].where((s) => s.isNotEmpty).toList();
    final orgs = [for (final o in ((m['source'] as Map?)?['source_organizations'] as List? ?? const [])) (((o as Map)['organization'] as Map?)?['name'] ?? '').toString()].where((s) => s.isNotEmpty).toList();
    final kind = (m['type'] ?? '').toString();
    final page = 'https://www.labxchange.org/library/items/$id';
    String? content;
    var mime = '';
    var yt = false;
    final enc = Uri.encodeComponent(id);
    if (kind == 'document') {
      final d = await _json('$kLabxApi/xblocks/$enc/student_view_data');
      content = d['document_url'] as String?;
      mime = (d['document_type'] ?? '').toString();
    } else if (kind == 'video') {
      final d = await _json('$kLabxApi/xblocks/$enc/video_student_view_data');
      final ev = (d['encoded_videos'] as Map?)?.cast<String, dynamic>() ?? const {};
      for (final k in ['mobile_high', 'desktop_mp4', 'fallback', 'mobile_low']) {
        final u = (ev[k] as Map?)?['url'] as String?;
        if (u != null && u.toLowerCase().contains('.mp4')) {
          content = u;
          mime = 'video/mp4';
          break;
        }
      }
      yt = content == null && ev.containsKey('youtube');
    } else if (kind == 'simulation' || kind == 'interactive') {
      final d = await _json('$kLabxApi/xblocks/$enc/student_view_data');
      content = d['simulation_url'] as String?;
      mime = 'application/zip';
    }
    return LabxItem(
      id: id,
      title: (m['title'] ?? id).toString(),
      kind: kind,
      licenceRaw: (m['license'] ?? '').toString(),
      author: [...authors, ...orgs].join(', '),
      pageUrl: page,
      contentUrl: content,
      mime: mime,
      youtubeOnly: yt,
    );
  }

  /// Why this item cannot be imported, or null.
  static String? refusal(LabxItem it) {
    final l = it.licence.refusal(modified: it.fourType == FourType.web);
    if (l != null) return l;
    if (it.youtubeOnly) return 'This video is hosted on YouTube only; it cannot be downloaded for offline use.';
    if (it.fourType == null) return 'This LabXchange item type (${it.kind}) has no downloadable file.';
    return null;
  }

  /// Streams a PDF/MP4 to [dest] (temp file in the app cache).
  Future<void> download(String url, File dest, {void Function(int done, int total)? onProgress}) async {
    final rq = await _http.getUrl(Uri.parse(url));
    final rs = await rq.close();
    if (rs.statusCode != 200) throw LabxException('download failed (${rs.statusCode})');
    final sink = dest.openWrite();
    var done = 0;
    try {
      await for (final c in rs) {
        sink.add(c);
        done += c.length;
        onProgress?.call(done, rs.contentLength);
      }
    } finally {
      await sink.close();
    }
  }

  void close() => _http.close(force: true);
}

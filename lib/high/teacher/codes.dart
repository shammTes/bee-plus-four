// Board codes. Every question has a 5-char code (assets/high/codes.json, built by tools/build_codes.py). A whole
// selection is one "set code" that encodes the question list itself, so it works offline with no server:
//   sorted global indices -> runs of consecutive indices -> per run: v = gap*2 + (run longer than 1),
//   gap = start (first run) or start - previous end - 1; if flagged, (extra - 1) follows
//   -> 4-bit varint groups (one alphabet char = continuation bit + 4 data bits, low group first) -> + 2 checksum chars.
// Q1–Q10 of one exam cost ~6 chars in total; scattered nearby questions ~1–2 chars each. A set code is never 5 chars
// long, so it can't be mistaken for a question code.
import 'dart:convert';

import 'package:flutter/services.dart';

const kCodeAlphabet = '23456789ABCDEFGHJKLMNPQRSTUVWXYZ';

class QCodes {
  QCodes(this.order, this.codes) {
    for (var i = 0; i < order.length; i++) {
      index[order[i]] = i;
      byCode[codes[i]] = i;
    }
  }
  final List<String> order, codes;
  final Map<String, int> index = {}, byCode = {};

  static Future<QCodes?> load(AssetBundle b) async {
    try {
      final j = jsonDecode(await b.loadString('assets/high/codes.json')) as Map<String, dynamic>;
      return QCodes([for (final x in j['order'] as List) x as String], [for (final x in j['codes'] as List) x as String]);
    } catch (_) {
      return null;
    }
  }

  String? codeOf(String id) => index[id] == null ? null : codes[index[id]!];
  String? idOf(String code) => byCode[code] == null ? null : order[byCode[code]!];

  /// ids in set-code order (sorted by global index, duplicates and unknown ids removed)
  List<String> canonical(Iterable<String> ids) => ({for (final id in ids) ?index[id]}.toList()..sort()).map((i) => order[i]).toList();

  static int _check(String data) {
    var h = 0x2F1 ^ data.length;
    for (final c in data.codeUnits) {
      h = (h * 31 + kCodeAlphabet.indexOf(String.fromCharCode(c)) + 7) & 0xFFFFF;
    }
    return (h ^ (h >> 10)) & 0x3FF;
  }

  static void _varint(StringBuffer sb, int v, {bool pad = false}) {
    while (v >= 16) {
      sb.write(kCodeAlphabet[16 | (v & 15)]);
      v >>= 4;
    }
    if (pad) {
      sb.write(kCodeAlphabet[16 | v]);
      v = 0;
    }
    sb.write(kCodeAlphabet[v]);
  }

  static String _wrap(String data) {
    final c = _check(data);
    return '$data${kCodeAlphabet[c >> 5]}${kCodeAlphabet[c & 31]}';
  }

  /// one short code for the whole selection (order is canonicalised: see [canonical])
  String setCode(Iterable<String> ids) {
    final ix = ({for (final id in ids) ?index[id]}.toList()..sort());
    if (ix.isEmpty) return '';
    final runs = <(int, int)>[]; // (start, extra)
    for (final i in ix) {
      if (runs.isNotEmpty && runs.last.$1 + runs.last.$2 + 1 == i) {
        runs.last = (runs.last.$1, runs.last.$2 + 1);
      } else {
        runs.add((i, 0));
      }
    }
    String enc({bool pad = false}) {
      final sb = StringBuffer();
      var prevEnd = -1;
      for (final (j, (st, ex)) in runs.indexed) {
        _varint(sb, (st - prevEnd - 1) * 2 + (ex > 0 ? 1 : 0), pad: pad && j == 0);
        if (ex > 0) _varint(sb, ex - 1);
        prevEnd = st + ex;
      }
      return _wrap(sb.toString());
    }

    final c = enc();
    return c.length == 5 ? enc(pad: true) : c; // never look like a question code
  }

  /// question ids of a set code, or null if it is not a valid set code
  List<String>? decodeSet(String code) {
    code = normalize(code);
    if (code.length < 3 || code.length == 5) return null;
    final data = code.substring(0, code.length - 2);
    final c = _check(data);
    if (code.substring(code.length - 2) != '${kCodeAlphabet[c >> 5]}${kCodeAlphabet[c & 31]}') return null;
    final vals = <int>[];
    var v = 0, shift = 0;
    for (final ch in data.split('')) {
      final d = kCodeAlphabet.indexOf(ch);
      if (d < 0) return null;
      v |= (d & 15) << shift;
      shift += 4;
      if (d < 16) {
        vals.add(v);
        v = 0;
        shift = 0;
      }
    }
    if (shift != 0 || vals.isEmpty) return null;
    final out = <String>[];
    var prevEnd = -1;
    for (var j = 0; j < vals.length; j++) {
      final st = prevEnd + 1 + (vals[j] >> 1);
      var ex = 0;
      if (vals[j] & 1 == 1) {
        if (++j >= vals.length) return null;
        ex = vals[j] + 1;
      }
      if (st + ex >= order.length) return null;
      for (var i = st; i <= st + ex; i++) {
        out.add(order[i]);
      }
      prevEnd = st + ex;
    }
    return out;
  }

  static String normalize(String s) => s.toUpperCase().replaceAll(RegExp(r'[\s\-_.·]'), '');

  /// what a student typed: one set code and/or question codes separated by spaces / commas.
  /// Returns the ids (in the typed order, set contents expanded) and the tokens that were not understood.
  ({List<String> ids, List<String> bad}) parse(String input) {
    final ids = <String>[], bad = <String>[];
    for (final raw in input.toUpperCase().split(RegExp(r'[\s,;]+'))) {
      final t = raw.replaceAll(RegExp(r'[\-_.·]'), '');
      if (t.isEmpty) continue;
      final q = t.length == 5 ? idOf(t) : null;
      final l = q != null ? [q] : decodeSet(t);
      if (l == null) {
        bad.add(raw);
      } else {
        for (final id in l) {
          if (!ids.contains(id)) ids.add(id);
        }
      }
    }
    return (ids: ids, bad: bad);
  }
}

/// Licence gate for third-party content (LabXchange etc.). 4 is a paid app, so only licences that
/// allow commercial redistribution may be packed: CC BY, CC BY-SA, CC0, public domain, and
/// CC BY-ND when the file is passed through unmodified. NC and "all rights reserved" are refused.
class FourLicence {
  const FourLicence(this.id, this.label, {this.allowed = true, this.noDerivatives = false, this.shareAlike = false});

  /// Stored in [FourMeta.licence].
  final String id;
  final String label;
  final bool allowed, noDerivatives, shareAlike;

  static const ccBy = FourLicence('CC-BY-4.0', 'CC BY 4.0');
  static const ccBySa = FourLicence('CC-BY-SA-4.0', 'CC BY-SA 4.0', shareAlike: true);
  static const ccByNd = FourLicence('CC-BY-ND-4.0', 'CC BY-ND 4.0', noDerivatives: true);
  static const cc0 = FourLicence('CC0-1.0', 'CC0 1.0');
  static const pd = FourLicence('PD', 'Public domain');
  static const ccByNc = FourLicence('CC-BY-NC-4.0', 'CC BY-NC 4.0', allowed: false);
  static const ccByNcSa = FourLicence('CC-BY-NC-SA-4.0', 'CC BY-NC-SA 4.0', allowed: false);
  static const ccByNcNd = FourLicence('CC-BY-NC-ND-4.0', 'CC BY-NC-ND 4.0', allowed: false);
  static const arr = FourLicence('ARR', 'All rights reserved', allowed: false);
  static const unknown = FourLicence('', 'Unknown', allowed: false);

  /// LabXchange Standard License (LabXchange ToS): personal, non-commercial use on labxchange.org only.
  static const lx1 = FourLicence('LX1', 'LabXchange Standard License', allowed: false);

  /// Choices offered when the licence has to be picked by hand.
  static const choices = [ccBy, ccBySa, ccByNd, cc0, pd, ccByNc, ccByNcSa, ccByNcNd, arr];

  /// Parses free text from page/API metadata: "CC BY-NC-SA 4.0", "cc-by", a creativecommons.org URL,
  /// "Public Domain", "All rights reserved"… Returns [unknown] when nothing matches (caller asks the user).
  static FourLicence parse(String? raw) {
    if (raw == null) return unknown;
    final s = raw.toLowerCase().replaceAll('_', '-').trim();
    if (s.isEmpty) return unknown;
    if (s.contains('all rights reserved') || s == 'arr' || s.contains('copyright') && !s.contains('creativecommons')) return arr;
    if (s.contains('publicdomain/zero') || RegExp(r'\bcc0\b|cc-zero|cc zero').hasMatch(s)) return cc0;
    if (s.contains('public domain') || s.contains('publicdomain/mark') || s == 'pd' || s == 'pdm') return pd;
    // creativecommons.org/licenses/by-nc-sa/4.0 → by-nc-sa ; "CC BY-NC 4.0" → by-nc
    final m = RegExp(r'licenses/([a-z-]+)/').firstMatch(s);
    final body = m != null ? m.group(1)! : s.replaceAll(RegExp(r'\bcc\b|creative commons|attribution|[0-9.]+|licen[cs]e'), ' ');
    final t = body.replaceAll(RegExp(r'[^a-z]+'), ' ').trim().split(' ').toSet();
    final named = {
      if (s.contains('noncommercial') || s.contains('non-commercial') || t.contains('nc')) 'nc',
      if (s.contains('noderiv') || s.contains('no-deriv') || t.contains('nd')) 'nd',
      if (s.contains('sharealike') || s.contains('share-alike') || t.contains('sa')) 'sa',
    };
    final isCc = m != null || s.contains('cc') || s.contains('creative commons') || t.contains('by');
    if (!isCc) return unknown;
    if (named.contains('nc')) {
      if (named.contains('nd')) return ccByNcNd;
      if (named.contains('sa')) return ccByNcSa;
      return ccByNc;
    }
    if (named.contains('nd')) return ccByNd;
    if (named.contains('sa')) return ccBySa;
    if (t.contains('by') || s.contains('attribution')) return ccBy;
    return unknown;
  }

  static FourLicence byId(String id) => [...choices, lx1, unknown].firstWhere((l) => l.id == id, orElse: () => unknown);

  /// null = OK to pack; otherwise the message to show. [modified]: transcoded/cropped/re-bundled.
  String? refusal({bool modified = false}) {
    if (this == unknown || id.isEmpty) return 'Licence unknown: pick the licence shown on the source page before encrypting.';
    if (!allowed) {
      if (id == 'ARR') return '"All rights reserved": 4 is a paid app, so this cannot be packed without the owner\'s written permission.';
      if (id == 'LX1') return 'LabXchange Standard License: personal, non-commercial use on labxchange.org only (no downloading or redistribution). 4 is a paid app, so it cannot be packed.';
      return '$label is non-commercial (NC). 4 is a paid app, so NC content cannot be packed.';
    }
    if (noDerivatives && modified) return '$label allows no changes: turn off transcoding/cropping and pack the original file.';
    return null;
  }
}

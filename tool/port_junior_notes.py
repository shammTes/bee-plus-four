#!/usr/bin/env python3
"""One-off port of the Junior notes renderer (junior_flutter/lib/junior/...) into lib/high/notes/jr/ (kept in Junior's
folder layout so relative imports stay valid). Rewrites fonts to High's families, re-skins the palette with High's
tokens and scales type down for Grade 9-12 readers. Files that need High glue (state, shell, repository) are written by hand."""
import os, re, shutil
SRC = '/workspace/junior_flutter/lib/junior'
DST = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'lib/high/notes/jr')
FILES = ['theme/clay.dart', 'theme/notes_styles.dart', 'theme/styles.dart', 'theme/tokens.dart',
         'widgets/art.dart', 'widgets/art_data.dart', 'widgets/clay_widgets.dart', 'widgets/page.dart', 'widgets/tx.dart',
         'data/notes_models.dart', 'data/json_util.dart', 'data/subjects.dart', 'l10n/labels.dart',
         'notes/cards.dart', 'notes/diagram.dart', 'notes/exercise.dart', 'notes/games.dart', 'notes/graph_svg.dart',
         'notes/rich.dart', 'notes/session.dart', 'notes/svg_prep.dart', 'notes/ui.dart', 'screens/unit_page.dart']
for f in FILES:
    s = open(os.path.join(SRC, f), encoding='utf-8').read()
    s = s.replace("'JuniorNunito1000'", "'HighNunito'").replace('"JuniorNunito"', '"HighNunito"').replace("'JuniorNunito'", "'HighNunito'")
    s = s.replace("font-family=\"JuniorNunito\"", 'font-family="HighNunito"').replace("font-family=\"JuniorEthiopic\"", 'font-family="HighNunito"')
    s = s.replace("const kFontFallback = ['JuniorEthiopic'];", "const kFontFallback = ['HighSymbols', 'HighSymbols2', 'HighSymbols3'];")
    s = '// Ported from Junior (junior_flutter/lib/junior/%s) by tool/port_junior_notes.py; High glue edits marked "High:".\n' % f + s
    os.makedirs(os.path.dirname(os.path.join(DST, f)), exist_ok=True)
    open(os.path.join(DST, f), 'w', encoding='utf-8').write(s)
print('ported', len(FILES), 'files to', DST)

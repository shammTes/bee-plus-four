#!/usr/bin/env python3
"""Builds the math/symbol fallback fonts (family HighSymbols) for glyphs Nunito lacks: Greek, arrows (incl. ⇌),
super/subscripts, math operators, letterlike symbols, fractions, shapes, ✓✗ … plus every other non-Nunito character
found in the exam packs and notes. Two files: Noto Sans Bold subset + DejaVu Sans Bold subset for what Noto lacks."""
import glob, os
from fontTools.ttLib import TTFont
from fontTools import subset
from fontTools.varLib import instancer
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(HERE, 'assets/high/fonts')
NUNITO = TTFont(os.path.join(OUT, 'Nunito-800.ttf')).getBestCmap()
ranges = [(0x0370, 0x03FF), (0x02B0, 0x02FF), (0x1D2C, 0x1D6A), (0x2070, 0x209F), (0x2100, 0x214F), (0x2150, 0x218F),
          (0x2190, 0x21FF), (0x2200, 0x22FF), (0x2300, 0x23FF), (0x25A0, 0x25FF), (0x2600, 0x26FF), (0x2700, 0x27BF), (0x27C0, 0x27FF),
          (0x2016, 0x2016), (0x2032, 0x2037), (0x0250, 0x02AF), (0xFF04, 0xFF04)]
want = {c for a, b in ranges for c in range(a, b + 1)}
for f in glob.glob(os.path.join(HERE, 'assets/high/exams/*.json')) + glob.glob('/workspace/high/content/notes/**/*.json', recursive=True):
    want |= {ord(c) for c in open(f, encoding='utf-8').read() if ord(c) > 127}
want = {c for c in want if c not in NUNITO and c not in (0xFE0F, 0x200D) and not (0x1F000 <= c <= 0x1FFFF)}
noto = TTFont('/usr/share/fonts/truetype/sand-box/google/Noto Sans/NotoSans-VariableFont_wdth,wght.ttf')
noto = instancer.instantiateVariableFont(noto, {'wght': 700, 'wdth': 100})
ncm = noto.getBestCmap()
a = sorted(c for c in want if c in ncm)
dj = TTFont('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf')
dcm = dj.getBestCmap()
b = sorted(c for c in want if c not in ncm and c in dcm)
mx = TTFont('/usr/share/fonts/truetype/dejavu/DejaVuMathTeXGyre.ttf')
mcm = mx.getBestCmap()
m = sorted(c for c in want if c not in ncm and c not in dcm and c in mcm)
miss = sorted(c for c in want if c not in ncm and c not in dcm and c not in mcm)
def sub(font, cps, path):
    o = subset.Options(); o.layout_features = ['*']; o.name_IDs = ['*']; o.notdef_outline = True
    s = subset.Subsetter(o); s.populate(unicodes=cps); s.subset(font)
    font.save(path)
sub(noto, a, os.path.join(OUT, 'HighSymbols-Noto.ttf'))
sub(dj, b, os.path.join(OUT, 'HighSymbols-DejaVu.ttf'))
sub(mx, m, os.path.join(OUT, 'HighSymbols-Math.ttf'))
print(f'Noto {len(a)} glyphs, DejaVu {len(b)}, Math {len(m)}, missing {len(miss)}:', ''.join(chr(c) for c in miss if 0x2000 < c)[:200])

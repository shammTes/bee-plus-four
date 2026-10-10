r"""Grade 11 Unit 2 — Natural Resource Base (pp. 38-100): climate, soil, biodiversity, water resources, agro-ecological zones."""
import math
from common import set_unit, T, RM, MN, TB, DG, ST, WK, CK, QSet
from svglib import Fig, Plot, INK, BLUE, RED, GREEN, PURPLE, ORANGE, GREY, FILL
from agrilib import (box, tlines, wrap, flow, hflow, cycle, leader, ground, grass_tufts, sorghum, leaf, roots_fibrous,
                     roots_tap, cow, goat, sheep, camel, person, sun, cloud, tree, BROWN, SOIL, SOIL2, SOIL3, LEAF, STRAW,
                     WATER, ROCK)

UID = 'agri11-u2'
set_unit(UID)


# ------------------------------------------------------------------ figures
def f_instruments():
    f = Fig(340, 300)
    # rain gauge
    x = 46
    f.rect(x - 14, 60, 28, 70, GREY, 1.6, '#F1EEEA', 3).path(f'M{x - 22} 60 L{x - 14} 76 L{x + 14} 76 L{x + 22} 60Z', GREY, 1.4, '#FFFFFF')
    f.rect(x - 7, 92, 14, 34, BLUE, 1, FILL[BLUE]).rect(x - 7, 108, 14, 18, None, 0, WATER)
    tlines(f, x, 146, ['Rain gauge', 'rain (mm)'], 10.5)
    # max-min thermometer in Stevenson screen
    x = 128
    f.rect(x - 30, 40, 60, 56, GREY, 1.6, '#FFFFFF', 2)
    for i in range(5):
        f.line(x - 26, 48 + i * 10, x + 26, 52 + i * 10, GREY, 1)
    f.line(x - 20, 96, x - 20, 130, GREY, 2.4).line(x + 20, 96, x + 20, 130, GREY, 2.4)
    tlines(f, x, 152, ['Screen with', 'thermometers:', 'max/min °C,', 'humidity'], 10.5)
    # anemometer
    x = 214
    f.line(x, 60, x, 130, GREY, 2.2).line(x - 28, 60, x + 28, 60, GREY, 1.8)
    for dx in (-28, 28):
        f.path(f'M{x + dx - 8} 60 A8 8 0 0 0 {x + dx + 8} 60Z', INK, 1.2, ORANGE)
    f.path(f'M{x - 8} 48 A8 8 0 0 0 {x + 8} 48Z', INK, 1.2, ORANGE).line(x, 48, x, 60, GREY, 1.6)
    tlines(f, x, 146, ['Anemometer', 'wind speed'], 10.5)
    # wind vane
    x = 296
    f.line(x, 56, x, 130, GREY, 2).path(f'M{x - 28} 56 L{x + 18} 56 M{x + 18} 50 L{x + 30} 56 L{x + 18} 62Z M{x - 28} 48 L{x - 18} 56 L{x - 28} 64Z', INK, 1.6, INK)
    tlines(f, x - 8, 146, ['Wind vane', 'direction'], 10.5)
    # evaporation pan
    x = 70
    f.ellipse(x, 214, 54, 12, GREY, 1.6, FILL[BLUE]).path(f'M{x - 54} 214 L{x - 54} 236 A54 12 0 0 0 {x + 54} 236 L{x + 54} 214', GREY, 1.6)
    f.line(x + 20, 196, x + 20, 216, INK, 2)
    tlines(f, x, 268, ['Evaporation pan', 'water lost (mm/day)'], 11)
    # sunshine recorder
    x = 186
    f.circle(x, 210, 22, BLUE, 1.6, '#EAF3FA').path(f'M{x - 30} 222 A30 30 0 0 0 {x + 30} 222', ORANGE, 3)
    f.rect(x - 22, 238, 44, 8, GREY, 1.2, '#F1EEEA')
    f.line(x - 12, 228, x - 30, 222, '#D79A1E', 1.2, dash='2 2')
    tlines(f, x, 268, ['Sunshine recorder', 'hours of bright sun'], 11)
    # barograph
    x = 290
    f.rect(x - 34, 196, 68, 44, GREY, 1.6, '#F1EEEA', 4).circle(x - 14, 218, 12, INK, 1.4, '#FFFFFF')
    f.path(f'M{x + 2} 212 Q{x + 10} 204 {x + 16} 216 T{x + 30} 214', RED, 1.6)
    tlines(f, x, 268, ['Barograph', 'air pressure record'], 11)
    f.text(170, 20, 'Read the instruments every day before 8:00 a.m.', 11.5, GREEN)
    return f


def f_altitude():
    p = Plot(0, 3000, 0, 40, unit=0.095, uy=5.2, pad=34, grid=False, every=500, yevery=10, xlab='', ylab='')
    p.fn(lambda h: 36.8 - 0.005 * h, 0, 3000, RED, 2.6, steps=4)
    p.fn(lambda h: 31.0 - 0.006 * h, 0, 3000, PURPLE, 2.6, steps=4)
    p.fn(lambda h: 25.3 - 0.007 * h, 0, 3000, BLUE, 2.6, steps=4)
    for name, h in (('Massawa', 10), ('Keren', 1460), ('Asmara', 2325)):
        p.seg((h, 0), (h, 38), GREY, 1.2, dash='4 4')
        p.text(p.X(h) + 4, p.Y(38.5) + (0 if h != 1460 else 12), name, 11, INK, 'start')
    p.pt(2325, 25.3 - 0.007 * 2325, None, c=BLUE, r=4).text(p.X(2325) + 6, p.Y(9) + 14, '9.0 °C', 11, BLUE, 'start')
    p.text(p.X(1500), p.h - 4, 'altitude (m above sea level)', 11, GREY, 'middle', False)
    p.text(p.X(0) + 4, p.Y(40) - 4, '°C', 11, GREY, 'start', False)
    p.text(p.X(260), p.Y(35.2), 'maximum', 11, RED, 'start').text(p.X(260), p.Y(29.3), 'mean', 11, PURPLE, 'start').text(p.X(260), p.Y(23.4), 'minimum', 11, BLUE, 'start')
    return p


def f_roles():
    f = Fig(340, 250)
    roles = [('Medium for plant growth', GREEN), ('Regulates water supply', BLUE), ('Recycles nutrients and wastes', ORANGE),
             ('Habitat for soil organisms', PURPLE), ('Engineering medium (roads, houses)', BROWN)]
    cx, cy = 170, 128
    for i, (r, c) in enumerate(roles):
        a = math.radians(90 - 72 * i)
        x, y = cx + 112 * math.cos(a), cy - 92 * math.sin(a)
        f.line(cx, cy, x, y, GREY, 1.4)
        box(f, x - 54, y - 19, 108, 38, r, c if c in FILL else ORANGE, 11)
    f.ellipse(cx, cy, 44, 26, BROWN, 2, '#E9D9BF')
    tlines(f, cx, cy, ['SOIL'], 14, BROWN)
    return f


def f_formation():
    f = Fig(340, 200)
    ground(f, 150, c='#FFFFFF', h=1)
    stages = [('Bare rock', ROCK, 0), ('Weathering: cracks, rain, heat', '#BDB3A6', 1), ('Regolith + first plants', SOIL, 2), ('Mature soil with horizons', SOIL3, 3)]
    for i, (t, c, k) in enumerate(stages):
        x = 8 + i * 83
        if k == 0:
            f.rect(x, 90, 76, 60, INK, 1.2, ROCK)
        elif k == 1:
            f.rect(x, 90, 76, 60, INK, 1.2, ROCK)
            for j in range(5):
                f.path(f'M{x + 8 + j * 15} 90 l4 14 l-3 10 l5 14', '#5A5048', 1.3)
        elif k == 2:
            f.rect(x, 104, 76, 46, INK, 1.2, ROCK).rect(x, 90, 76, 14, None, 0, SOIL)
            grass_tufts(f, [x + 20, x + 52], 90, LEAF, 0.8)
        else:
            f.rect(x, 90, 76, 12, None, 0, '#4A3426').rect(x, 102, 76, 18, None, 0, SOIL2).rect(x, 120, 76, 16, None, 0, '#C9A57A').rect(x, 136, 76, 14, INK, 0, ROCK)
            grass_tufts(f, [x + 14, x + 40, x + 62], 90, LEAF, 0.9)
        tlines(f, x + 38, 50, wrap(t, 13), 11)
        if i:
            f.arrow(x - 7, 120, x - 1, 120, INK, 1.6, 5)
    f.text(170, 178, 'Parent material · Climate · Organisms · Topography · Time', 11, GREEN)
    f.text(170, 194, '1 cm of topsoil takes 120–400 years to form', 11, RED)
    return f


def f_profile():
    f = Fig(340, 312)
    x0, w = 46, 116
    layers = [('O', 0, 18, '#3B2A1E', 'Leaf litter, roots — organic layer'), ('A', 18, 72, '#5E4130', 'Topsoil: humus + minerals, dark, most roots'),
              ('B', 72, 150, '#A0663B', 'Subsoil: clay, iron, aluminium washed in (illuviation)'), ('C', 150, 225, '#C9A57A', 'Weathered parent material, rock structure visible'),
              ('R', 225, 270, ROCK, 'Bedrock')]
    for i, (h, a, b, c, d) in enumerate(layers):
        y0, y1 = 20 + a, 20 + b
        f.g(hl=f'h{h}')
        f.path(f'M{x0} {y0} Q{x0 + w / 2} {y0 + (4 if i else -2)} {x0 + w} {y0} L{x0 + w} {y1} Q{x0 + w / 2} {y1 + 4} {x0} {y1}Z', None, 0, c)
        f.text(x0 + w / 2, (y0 + y1) / 2 + 5, h, 15, '#FFFFFF' if i < 3 else INK)
        lines = wrap(d, 24)
        tlines(f, x0 + w + 14, (y0 + y1) / 2, lines, 11, INK, 'start', False)
        f.line(x0 + w + 2, (y0 + y1) / 2, x0 + w + 10, (y0 + y1) / 2, GREY, 1.2)
        f.end()
    for j in range(7):
        f.circle(x0 + 15 + j * 15, 20 + 160 + (j % 3) * 18, 4, None, 0, '#8E7F70')
        f.circle(x0 + 10 + j * 16, 20 + 240 + (j % 2) * 10, 6, None, 0, '#857B70')
    roots_fibrous(f, x0 + 40, 22, 40, '#D9C4A0')
    f.rect(x0 + w / 2 - 10, 20 + 236, 20, 20, None, 0, ROCK).text(x0 + w / 2, 20 + 252, 'R', 15, INK)
    f.raw(f'<path d="M{x0 - 14} 20 V{20 + 150}" stroke="{GREEN}" stroke-width="2"/>')
    f.text(x0 - 20, 100, 'solum', 11, GREEN, 'middle').text(170, 306, 'Soil profile: the master horizons O, A, B, C over rock R', 11, GREY, 'middle', False)
    return f


def f_composition():
    f = Fig(340, 210)
    parts = [('Mineral matter', 45, '#B98A5E'), ('Organic matter', 5, '#4A3426'), ('Water', 25, WATER), ('Air', 25, '#CFE3F2')]
    cx, cy, r = 96, 106, 82
    a0 = 90
    for name, p, c in parts:
        a1 = a0 - p * 3.6
        p0 = (cx + r * math.cos(math.radians(a0)), cy - r * math.sin(math.radians(a0)))
        p1 = (cx + r * math.cos(math.radians(a1)), cy - r * math.sin(math.radians(a1)))
        large = 1 if p > 50 else 0
        f.path(f'M{cx} {cy} L{p0[0]:.1f} {p0[1]:.1f} A{r} {r} 0 {large} 1 {p1[0]:.1f} {p1[1]:.1f}Z', '#FFFFFF', 1.6, c)
        a0 = a1
    for i, (name, p, c) in enumerate(parts):
        y = 40 + i * 34
        f.rect(196, y - 11, 16, 16, GREY, 1, c, 3)
        f.text(220, y + 2, f'{name} {p}%', 12, INK, 'start')
    f.text(266, 186, 'solids 50% | pores 50%', 11, GREEN)
    f.text(266, 202, 'water and air trade places', 11, GREY, 'middle', False)
    return f


def _tri(sand, silt, clay, x0=22, y0=276, W=296):
    H = W * 0.866
    return (x0 + W * (silt + clay / 2) / 100, y0 - H * clay / 100)


TEXTURE = {
    'sand': [(100, 0, 0), (85, 15, 0), (90, 0, 10)],
    'loamy sand': [(85, 15, 0), (70, 30, 0), (85, 0, 15), (90, 0, 10)],
    'sandy loam': [(70, 30, 0), (50, 50, 0), (43, 50, 7), (52, 41, 7), (52, 28, 20), (80, 0, 20), (85, 0, 15)],
    'loam': [(43, 50, 7), (52, 41, 7), (52, 28, 20), (45, 28, 27), (23, 50, 27)],
    'silt loam': [(50, 50, 0), (20, 80, 0), (8, 80, 12), (0, 88, 12), (0, 73, 27), (23, 50, 27), (43, 50, 7)],
    'silt': [(20, 80, 0), (0, 100, 0), (0, 88, 12), (8, 80, 12)],
    'sandy clay loam': [(80, 0, 20), (52, 28, 20), (45, 28, 27), (45, 20, 35), (65, 0, 35)],
    'clay loam': [(45, 28, 27), (20, 53, 27), (20, 40, 40), (45, 15, 40)],
    'silty clay loam': [(20, 53, 27), (0, 73, 27), (0, 60, 40), (20, 40, 40)],
    'sandy clay': [(65, 0, 35), (45, 20, 35), (45, 0, 55)],
    'silty clay': [(20, 40, 40), (0, 60, 40), (0, 40, 60)],
    'clay': [(45, 15, 40), (20, 40, 40), (0, 40, 60), (0, 0, 100), (45, 0, 55)],
}
TEXCOL = {'sand': '#F3E2B3', 'loamy sand': '#EFD9A4', 'sandy loam': '#E8CF96', 'loam': '#D9C08A', 'silt loam': '#E6DCC4', 'silt': '#EEE8D8',
          'sandy clay loam': '#D7B98E', 'clay loam': '#C9A97F', 'silty clay loam': '#D3C2A6', 'sandy clay': '#C79E78', 'silty clay': '#BFA88E', 'clay': '#B58D6B'}
LABPOS = {'sand': (93, 4, 3), 'loamy sand': (82, 10, 8), 'sandy loam': (63, 25, 12), 'loam': (41, 40, 19), 'silt loam': (22, 64, 14),
          'silt': (7, 88, 5), 'sandy clay loam': (60, 12, 28), 'clay loam': (33, 34, 33), 'silty clay loam': (10, 56, 34),
          'sandy clay': (52, 6, 42), 'silty clay': (7, 46, 47), 'clay': (20, 20, 60)}


def f_triangle():
    f = Fig(340, 312)
    for name, poly in TEXTURE.items():
        f.poly([_tri(*p) for p in poly], '#FFFFFF', 1.2, TEXCOL[name])
    f.poly([_tri(100, 0, 0), _tri(0, 100, 0), _tri(0, 0, 100)], INK, 1.8)
    for name, (a, b, c) in LABPOS.items():
        x, y = _tri(a, b, c)
        lines = name.split(' ') if name in ('sandy clay loam', 'silty clay loam', 'loamy sand', 'sandy loam', 'silt loam', 'clay loam', 'sandy clay', 'silty clay') and name not in ('clay loam',) else [name]
        if name == 'clay loam':
            lines = ['clay loam']
        tlines(f, x, y, lines, 9 if len(lines) > 1 else 10, INK, 'middle', True, 10)
    for v in (20, 40, 60, 80):
        x, y = _tri(0, 100 - v, v)
        f.text(x + 6, y + 4, str(v), 9.5, GREY, 'start', False)
        x, y = _tri(100 - v, v, 0)
        f.text(x, y + 13, str(v), 9.5, GREY, 'middle', False)
        x, y = _tri(v, 0, 100 - v)
        f.text(x - 5, y + 4, str(v), 9.5, GREY, 'end', False)
    f.text(70, 120, '% clay', 11, RED, 'middle').text(290, 120, '% silt', 11, GREEN, 'middle').text(170, 306, '% sand', 11, ORANGE, 'middle')
    # worked point: sand 60, silt 30, clay 10
    f.g('k1 k4').line(*_tri(90, 0, 10), *_tri(0, 90, 10), RED, 2).end()
    f.g('k2 k4').line(*_tri(70, 30, 0), *_tri(0, 30, 70), GREEN, 2).end()
    f.g('k3 k4').line(*_tri(60, 40, 0), *_tri(60, 0, 40), ORANGE, 2).end()
    f.g('k4')
    x, y = _tri(60, 30, 10)
    f.circle(x, y, 5, INK, 2, '#FFFFFF').text(x + 70, y - 26, '60 / 30 / 10', 10.5, INK).line(x + 3, y - 4, x + 40, y - 22, INK, 1)
    f.end()
    return f


def f_sizes():
    f = Fig(340, 170)
    rows = [('Sand', '0.05–2 mm', 20, '#E8CF96', 'gritty; drains fast; holds little'), ('Silt', '0.002–0.05 mm', 12, '#E6DCC4', 'smooth like flour'),
            ('Clay', '< 0.002 mm', 3, '#B58D6B', 'sticky; holds water and nutrients')]
    for i, (n_, s, r, c, d) in enumerate(rows):
        y = 40 + i * 44
        f.circle(44, y + 8, r if r > 3 else 2.5, INK, 1.2, c)
        f.text(96, y + 2, n_, 13, INK, 'start').text(96, y + 18, s, 11, GREY, 'start', False)
        tlines(f, 190, y + 8, wrap(d, 22), 10.5, INK, 'start', False)
    f.text(170, 18, 'Particle sizes of the soil separates (Table 2.4)', 12, INK)
    f.text(170, 166, 'If a clay particle were a grain of teff, sand would be a football', 10.5, GREEN)
    return f


def f_structure():
    f = Fig(340, 230)
    cells = [('Single grain', 'sand dunes'), ('Granular / crumb', 'topsoil, rich in humus'), ('Platy', 'horizontal plates'),
             ('Prismatic', 'flat tops, B horizon'), ('Columnar', 'rounded tops, sodic B'), ('Blocky', 'cubes, humid B')]
    for i, (t, d) in enumerate(cells):
        x, y = 8 + (i % 3) * 110, 8 + (i // 3) * 112
        f.rect(x, y, 104, 70, GREY, 1, '#F7F1E6', 6)
        cx, cy = x + 52, y + 35
        if i == 0:
            for j in range(18):
                f.circle(x + 12 + (j % 6) * 16, y + 14 + (j // 6) * 20, 5, INK, 0.8, '#E8CF96')
        elif i == 1:
            for j in range(10):
                f.circle(x + 14 + (j % 5) * 19, y + 20 + (j // 5) * 28, 8, INK, 0.9, '#8B6A4A')
        elif i == 2:
            for j in range(5):
                f.rect(x + 10 + (j % 2) * 8, y + 8 + j * 12, 76, 8, INK, 0.9, '#B08B66', 3)
        elif i in (3, 4):
            for j in range(4):
                xx = x + 10 + j * 22
                if i == 3:
                    f.rect(xx, y + 10, 18, 52, INK, 0.9, '#A0663B')
                else:
                    f.path(f'M{xx} {y + 62} L{xx} {y + 18} Q{xx + 9} {y + 6} {xx + 18} {y + 18} L{xx + 18} {y + 62}Z', INK, 0.9, '#A0663B')
        else:
            for j in range(8):
                f.rect(x + 10 + (j % 4) * 22, y + 10 + (j // 4) * 26, 19, 22, INK, 0.9, '#9C6B43', 2)
        f.text(cx, y + 86, t, 11.5, INK).text(cx, y + 100, d, 10, GREY, 'middle', False)
    return f


def f_water():
    f = Fig(340, 230)
    x0, w = 30, 280
    f.rect(x0, 40, w, 46, INK, 1.2, '#FFFFFF', 4)
    segs = [(0, 0.28, '#9CC3E6', 'Gravitational', 'drains away'), (0.28, 0.72, WATER, 'Available water', 'plants use it'),
            (0.72, 1.0, '#C9B9A6', 'Unavailable', 'held too tightly')]
    for a, b, c, t, d in segs:
        f.rect(x0 + a * w, 40, (b - a) * w, 46, None, 0, c)
        tlines(f, x0 + (a + b) / 2 * w, 63, [t, d], 10, INK if c != WATER else '#FFFFFF')
    for k, lab in ((0, 'Saturation'), (0.28, 'Field capacity'), (0.72, 'Wilting point'), (1.0, 'Oven dry')):
        x = x0 + k * w
        f.line(x, 30, x, 96, RED, 1.8)
        f.text(x, 24 if k in (0, 0.72) else 110, lab, 11, RED, 'start' if k == 0 else ('end' if k == 1.0 else 'middle'))
    f.arrow(x0 + w, 126, x0, 126, GREY, 1.6, 7)
    f.text(x0 + w / 2, 142, 'more water in the soil  ←', 11, GREY, 'middle', False)
    f.text(170, 168, 'Saturation: every pore full of water', 11, INK, 'middle', False)
    f.text(170, 186, 'Field capacity: after free water has drained (1–3 days)', 11, INK, 'middle', False)
    f.text(170, 204, 'Wilting point: roots can no longer take water', 11, INK, 'middle', False)
    f.text(170, 222, 'Clay holds more water than sand at the same potential', 11, GREEN)
    return f


def f_ph():
    f = Fig(340, 190)
    cols = ['#D7301F', '#E8562F', '#F08A3C', '#F4B24A', '#F2D45C', '#C8D96A', '#8DC56C', '#5BAF77', '#3E9A8E', '#3A7FA6', '#3E5FA8', '#4B4AA0', '#5A3D94', '#5E2F82']
    for i in range(14):
        f.rect(16 + i * 22, 40, 22, 30, None, 0, cols[i])
        f.text(27 + i * 22, 86, str(i + 1), 11, INK)
    f.text(16, 30, 'acidic', 12, RED, 'start').text(170, 30, 'neutral 7', 12, GREEN).text(324, 30, 'alkaline', 12, PURPLE, 'end')
    f.rect(16 + 6 * 22, 96, 11, 10, GREEN, 1.2, FILL[GREEN], 2)
    f.text(16 + 6.25 * 22, 120, '"neutral" soils 6.5–7: best for most crops', 10.5, GREEN)
    items = [(4.6, 'high-rainfall soils (leached)', RED, 146), (8.2, 'calcareous soils (CaCO₃)', BLUE, 162), (9.6, 'sodic soils, Na₂CO₃ (up to 10.5)', PURPLE, 178)]
    for v, t, c, y in items:
        x = 16 + (v - 0.5) * 22
        f.line(x, 72, x, y - 10, c, 1.2, dash='3 3')
        f.text(x, y, t, 10.5, c, 'middle' if 60 < x < 280 else ('start' if x <= 60 else 'end'))
    return f


def f_nutrient():
    return cycle(['Plants take up nutrients', 'Residues, manure, dead roots', 'Soil organic matter (SOM)', 'Microbes decompose → humus',
                  'Mineral nutrients N, P, K, S'], w=340, h=270, bw=118, bh=42, size=11, centre='Nutrient cycle',
                 cols=(GREEN, BROWN, ORANGE, PURPLE, BLUE))


def f_hydro():
    f = Fig(340, 240)
    f.rect(0, 0, 340, 240, None, 0, '#F4F9FD')
    f.path('M0 170 L70 170 L130 90 L180 70 L230 100 L280 150 L340 160 L340 240 L0 240Z', '#7D5233', 1.2, '#C9A57A')
    f.rect(0, 170, 70, 70, None, 0, '#9CC3E6').text(36, 200, 'Red Sea', 11, BLUE)
    f.path('M0 214 Q120 208 340 206', BLUE, 1.6, dash='5 4')
    f.text(250, 226, 'groundwater (aquifer)', 10.5, BLUE)
    cloud(f, 150, 34, 1.2, rain=True)
    cloud(f, 260, 40, 0.9)
    sun(f, 36, 30, 12)
    f.arrow(40, 160, 70, 60, '#D79A1E', 1.8, 7).text(26, 110, 'evaporation', 10.5, ORANGE, 'start')
    tree(f, 205, 94, 36)
    f.arrow(205, 56, 222, 34, GREEN, 1.6, 6).text(228, 30, 'transpiration', 10.5, GREEN, 'start')
    f.path('M140 92 Q110 130 76 168', BLUE, 2.4).arrow(86, 158, 74, 170, BLUE, 2, 7)
    f.text(118, 132, 'runoff', 10.5, BLUE, 'end')
    f.arrow(176, 100, 176, 196, BLUE, 1.6, 7).text(182, 150, 'infiltration', 10.5, BLUE, 'start')
    f.text(150, 76, 'rain on highlands', 10.5, INK)
    f.text(170, 236, '80–87% of the rain is lost to evaporation + transpiration', 10.5, RED)
    return f


def f_basins():
    f = Fig(340, 230)
    f.title('Five river basins: area (km²) and runoff', 12.5)
    data = [('Red Sea', 44690, '730'), ('Barka-Anseba', 39510, '360'), ('Mereb-Gash', 23200, '480–760'), ('Danakil', 10530, '136'), ('Setit', 4045, '5 800–8 000')]
    for i, (name, a, r) in enumerate(data):
        y = 34 + i * 36
        f.text(98, y + 15, name, 11.5, INK, 'end')
        f.rect(104, y + 3, a / 44690 * 150, 18, None, 0, BLUE if name != 'Setit' else GREEN, 3)
        f.text(108 + a / 44690 * 150, y + 16, f'{a:,}'.replace(',', ' '), 10.5, INK, 'start', False)
        f.text(334, y + 16, r, 10.5, ORANGE, 'end')
    f.text(334, 30, 'runoff, million m³', 10, ORANGE, 'end', False)
    f.text(170, 222, 'Setit: smallest basin in Eritrea, but the only perennial river', 11, GREEN)
    return f


def f_aez():
    p = Plot(0, 1200, 0, 3200, unit=0.24, uy=0.072, pad=36, grid=False, every=200, yevery=1000, xlab='', ylab='')
    zones = [('Semi-desert 39%', 0, 200, 0, 1355, '#F3E2B3'), ('Arid lowland 34%', 200, 500, 400, 1600, '#E8C27A'),
             ('Moist lowland 16%', 500, 800, 500, 1600, '#9CCB7A'), ('Arid highland 3%', 200, 500, 1600, 2600, '#C9B9A6'),
             ('Moist highland 7%', 500, 700, 1600, 3018, '#6FAF6A'), ('Sub-humid escarpment 1%', 700, 1100, 600, 2600, '#3E8E6E')]
    for name, r0, r1, a0, a1, c in zones:
        p.poly([(p.X(r0), p.Y(a1)), (p.X(r1), p.Y(a1)), (p.X(r1), p.Y(a0)), (p.X(r0), p.Y(a0))], INK, 1.2, c, op=0.85)
    for name, r0, r1, a0, a1, c in zones:
        lines = wrap(name, 10)
        tlines(p, (p.X(r0) + p.X(r1)) / 2, (p.Y(a0) + p.Y(a1)) / 2, lines, 10, '#FFFFFF' if c in ('#3E8E6E', '#6FAF6A') else INK)
    p.text(p.X(600), p.h - 6, 'annual rainfall (mm)', 11, GREY, 'middle', False)
    p.text(p.X(0) + 4, p.Y(3200) - 6, 'altitude (m)', 11, GREY, 'start', False)
    return p


def f_landcover():
    f = Fig(340, 230)
    f.title('How Eritrea\'s land is covered (Table 2.14)', 12.5)
    data = [('Bush land', 42.7, '#B5A06A'), ('Wooded grassland', 20.3, '#9CCB7A'), ('Barren land', 14.4, ROCK), ('Open woodland', 7.6, '#6FAF6A'),
            ('Cultivated land', 6.8, ORANGE), ('Closed woodland', 3.6, '#3E8E6E'), ('All forests', 2.4, '#2A6A4A')]
    for i, (n_, v, c) in enumerate(data):
        y = 32 + i * 27
        f.text(118, y + 14, n_, 11, INK, 'end')
        f.rect(124, y + 3, v * 4.2, 16, None, 0, c, 3)
        f.text(128 + v * 4.2, y + 15, f'{v}%', 11, INK, 'start')
    f.text(170, 226, 'Only about 7% of the land is cultivated', 11, ORANGE)
    return f


DIAGRAMS = {
    'instruments': (f_instruments(), 'Meteorological instruments and what each one measures (Figure 2.1)', 39),
    'altitude': (f_altitude(), 'Temperature falls as altitude rises: the Table 2.1 equations drawn as lines', 41),
    'soilroles': (f_roles(), 'The five major ecological roles of soil (Figure 2.2)', 45),
    'formation': (f_formation(), 'From rock to soil: weathering and the five soil-forming factors', 46),
    'profile': (f_profile(), 'A soil profile with its master horizons (Figure 2.3)', 49),
    'composition': (f_composition(), 'Volume composition of a good loam topsoil (Figure 2.4)', 51),
    'triangle': (f_triangle(), 'The soil texture triangle (Figure 2.6), with the worked example 60% sand, 30% silt, 10% clay', 56),
    'sizes': (f_sizes(), 'Sand, silt and clay by particle size', 55),
    'structure': (f_structure(), 'Types of soil structure (Table 2.5)', 57),
    'soilwater': (f_water(), 'Soil water: gravitational, available and unavailable (Figure 2.7)', 59),
    'ph': (f_ph(), 'The pH scale and typical soil values (Figure 2.8)', 65),
    'nutrient': (f_nutrient(), 'A simple nutrient cycle (Figure 2.9)', 71),
    'hydro': (f_hydro(), 'The hydrological cycle over Eritrea (Figure 2.10)', 85),
    'basins': (f_basins(), 'The five major river basins (Table 2.12)', 88),
    'aez': (f_aez(), 'The six agro-ecological zones by altitude and rainfall (Table 2.13)', 95),
    'landcover': (f_landcover(), 'Land cover of Eritrea (Table 2.14)', 96),
}

# ------------------------------------------------------------------ 2.1 climate
L1 = [
    T('intro', 'Climate: the factor the farmer cannot change', 38,
      'In Unit 1 you met three groups of yield factors. **Climate is a yield-defining factor**: a farmer cannot change it, but he must know it to choose the right crop, variety, sowing date and breed.',
      'The climate elements that matter most for plants are **temperature, rainfall, relative humidity, solar radiation and light (day length), wind (air movement) and evaporation**. They act together.',
      'Farmers and extension workers need daily records of: rainfall; maximum and minimum temperature; relative humidity; sunshine hours and intensity; wind speed and direction.'),
    DG('instr-fig', 'Meteorological instruments', 39, 'instruments',
       'Record data at the same time every day (before 8:00 a.m.) so that the numbers can be compared.'),
    TB('=agri11-u2-tbl1', 'Instruments, what they measure and the unit', 39, ['Instrument', 'Measures', 'Unit', 'Use on the farm'],
       [['Standard rain gauge', 'Rainfall', 'mm', 'Sowing date; when to irrigate'],
        ['Maximum–minimum thermometer', 'Highest and lowest temperature', '°C', 'Frost risk; heat stress at flowering'],
        ['Thermo-hygrograph', 'Temperature and relative humidity (continuous record)', '°C, %', 'Warns of fungal diseases (downy mildew)'],
        ['Cup anemometer', 'Wind speed', 'm/s or km/h', 'Timing of spraying; windbreaks'],
        ['Wind vane', 'Wind direction', 'compass direction', 'Where to plant windbreaks'],
        ['Evaporation pan', 'Water evaporated', 'mm per day', 'How much irrigation water to give'],
        ['Sunshine recorder', 'Hours of bright sunshine', 'hours per day', 'Crop-growth and drying forecasts'],
        ['Barograph', 'Air pressure (continuous record)', 'mbar / hPa', 'Weather forecasting']], layout='cards'),
    T('=agri11-u2-c02', '2.1.1 Temperature', 40,
      'Temperature is one of the most important factors deciding **where** plants and animals live and **how much** they produce. Both **too low** and **too high** temperatures slow growth and development.',
      'Useful temperature measures: mean yearly temperature, mean monthly temperature, the coldest and warmest months, mean daily temperature and the **daily range** (day minus night).',
      '**Isotherms** are lines on a map joining places with the same mean temperature (for example the 20 °C or 25 °C yearly isotherm).',
      '**In Eritrea temperature is controlled mainly by altitude.** The textbook gives straight-line (linear) equations (Table 2.1), with altitude h in metres above sea level:',
      '- Minimum temperature (°C) = 25.3 − 0.007 h',
      '- Maximum temperature (°C) = 36.8 − 0.005 h',
      '- Mean temperature (°C) = 31.0 − 0.006 h',
      '- Mean potential evapotranspiration (mm/year) = 2069 − 0.198 h'),
    DG('alt-fig', 'Higher means cooler', 41, 'altitude',
       'Every 1000 m of climbing lowers the minimum temperature by 7 °C. That is why Massawa is hot and Asmara is cool even though they are only about 65 km apart.'),
    WK('wk-alt1', 'Worked example — Activity 2.2 Q1 and Q2', 41,
       'Estimate (a) the minimum temperature and potential evapotranspiration (PET) at 1000 m, and (b) the maximum temperature at 2000 m.',
       ['(a) Minimum: 25.3 − 0.007 × 1000 = 25.3 − 7 = **18.3 °C**.',
        '(a) PET: 2069 − 0.198 × 1000 = 2069 − 198 = **1871 mm per year**.',
        '(b) Maximum: 36.8 − 0.005 × 2000 = 36.8 − 10 = **26.8 °C**.'],
       '(a) 18.3 °C and 1871 mm/year; (b) 26.8 °C.'),
    WK('wk-alt2', 'Worked example — Asmara (2325 m)', 41,
       'Asmara is at about 2325 m. Estimate its minimum, maximum and mean temperature and PET.',
       ['Minimum: 25.3 − 0.007 × 2325 = 25.3 − 16.3 = **9.0 °C**.',
        'Maximum: 36.8 − 0.005 × 2325 = 36.8 − 11.6 = **25.2 °C**.',
        'Mean: 31.0 − 0.006 × 2325 = 31.0 − 14.0 = **17.0 °C**.',
        'PET: 2069 − 0.198 × 2325 = 2069 − 460 = **1609 mm per year**.',
        'Meaning: cool nights → barley, wheat and highland pulses do well; tropical crops such as sesame and cotton do not.'],
       'About 9 °C minimum, 25 °C maximum, 17 °C mean, PET about 1609 mm/year.'),
    T('=agri11-u2-c03', '2.1.2 Relative humidity', 41,
      '**Relative humidity (RH)** = the amount of water vapour in the air compared with the amount the air could hold when **saturated**, written as a **percentage**.',
      'Why farmers care: many diseases and insects respond directly to RH. For example **downy mildew** on grapes and onions spreads in humid weather. **Temperature affects RH**: when air warms up its RH falls (it can hold more vapour); at night it cools and RH rises, which is why dew forms at dawn.'),
    T('=agri11-u2-c04', '2.1.3 Rainfall', 42,
      'Water is part of every living process; **water stress** (from a small drop in water potential up to fatal drying) limits growth. Temperature and rainfall act **together**.',
      '**The key balance:** compare rainfall with potential evapotranspiration (PET). If **rainfall < PET**, the area has a **water deficit** and crops need moisture conservation or irrigation.',
      '**Example:** Massawa gets about 200 mm of rain but PET near sea level is about 2069 mm, a huge deficit; crops there need spate or other irrigation. In the moist highlands rainfall (500–700 mm) is still below PET, so timing of sowing and water harvesting matter.'),
    T('=agri11-u2-c05', '2.1.4 Solar radiation', 42,
      'Solar radiation is a range of **electromagnetic** waves (radio waves, ultraviolet, visible light, X-rays, gamma rays) with different energies.',
      'When radiation hits a surface (a leaf, the soil) three things can happen: it is **reflected**, **absorbed** or **transmitted**. Leaves absorb part of the visible light for **photosynthesis**, which builds biomass (yield).'),
    T('=agri11-u2-c06', '2.1.5 Light and day length', 42,
      'Light is essential for photosynthesis. **Day length (photoperiod)** controls the stages of crop development from germination to seed setting: it triggers growth, **flowering**, and hardening against cold as the seasons change.',
      '**Example:** many local sorghum varieties flower only when days begin to shorten after August, so they flower at the end of the rains whatever the sowing date.'),
    T('=agri11-u2-c07', '2.1.6 Topography', 43,
      '**Topography** = the relief of the land (hilltops, slopes, valleys). It affects light received, wind speed and direction, rainfall, **runoff and erosion**.',
      '- Soil is **eroded from slopes and hilltops** and **deposited in valleys**, so valley soils are **deeper and richer** and good for crops.',
      '- But cold air sinks into valleys at night, so valley floors are more exposed to **frost** in the cold months.',
      '- Topography also shapes drainage and temperature, and so the local vegetation and wildlife.',
      '**Eritrean example:** the eastern escarpment faces the Red Sea and catches moist air, so it has a wetter, sub-humid climate than the land behind it.'),
    WK('wk-ex21', 'Worked example — Exercise 2.1 Q2', 43,
       'How do relative humidity and topography affect the agricultural yield of an area?',
       ['RH: high RH favours fungal diseases (downy mildew) and some insects → yield loss; very low RH increases transpiration → water stress.',
        'Topography: slopes lose soil and water by runoff → shallow, poor soils, low yields; valleys collect soil and water → higher yields but frost risk.',
        'Aspect and height change light, wind and rainfall, so the same crop yields differently on different slopes.'],
       'High humidity raises disease; low humidity raises water stress. Slopes lose soil and water; valleys gain them but risk frost.'),
]

# ------------------------------------------------------------------ 2.2 soil
L2 = [
    T('soilwhat', 'What soil is and why it matters', 44,
      'Soil is **not just dust**: it is loose earth material formed from rocks (parent material) together with organic matter, water, air and living things. A mining engineer sees debris over rock, a road engineer sees a base for a road, a **farmer sees a home for plants**.',
      '**Soil science** studies the origin (genesis), form (morphology), properties and management of soil. Three kinds of process go on in soil: **chemical, physical and biological**.',
      'Almost everything we use comes from soil: all our food crops, the grass livestock eat, fibres such as cotton and flax, timber, and building materials such as bricks.'),
    DG('roles-fig', 'Five ecological roles of soil', 45, 'soilroles',
       'Soil also filters pollutants and links the carbon cycle: plants fix CO₂ into organic matter and soil microbes release it again.'),
    T('=agri11-u2-c11', '2.2.1 Soil formation', 46,
      'Two ways to study soil:',
      '- **Pedology** — the soil\'s origin, classification and description (useful to farmers and road engineers).',
      '- **Edaphology** — soil **from the plant\'s point of view**: properties in relation to plant production and how to improve productivity.',
      '**Weathering** is the physical breakdown and chemical alteration of rock by air, water and living things. The three rock groups that soils form from:',
      '- **Igneous** (from molten magma): granite, diorite, gabbro, basalt. Dark gabbro and basalt (rich in iron and magnesium) weather **faster** than light granite.',
      '- **Sedimentary** (weathered material deposited and re-cemented): sandstone (from quartz sand), shale (from clay), limestone, dolomite, conglomerate.',
      '- **Metamorphic** (other rocks changed by heat and pressure): gneiss (often from granite), schist, quartzite (from sandstone), slate (from shale), marble (from limestone or dolomite).',
      'In pedology soil is a three-dimensional natural body formed by **five soil-forming factors**.'),
    DG('form-fig', 'Rock becomes soil — slowly', 46, 'formation'),
    TB('factors', 'The five soil-forming factors (Table 2.2)', 47, ['Factor', 'How it shapes the soil'],
       [['Parent material', 'Different rocks weather into different regolith and soils, depending on their minerals (basalt → dark clay soils; granite → sandy soils).'],
        ['Climate', 'Temperature controls the speed of chemical reactions and decomposition; rainfall carries reactions, leaches nutrients or draws salts up to the surface.'],
        ['Organisms (biota)', 'Micro-organisms, larger animals and plants break down rock and organic matter and mix the soil.'],
        ['Topography', 'Elevation, aspect and slope control erosion, deposition and drainage.'],
        ['Time', 'Young soils differ from old soils formed under the same conditions; 1 cm of soil takes 120–400 years.']], layout='terms'),
    MN('mn-cl', 'Memory trick — "Cl-ORPT"', 47,
       '**Cl**imate, **O**rganisms, **R**elief (topography), **P**arent material, **T**ime. Say "clorpt".'),
    T('=agri11-u2-c12', '2.2.2 Soil profile description', 48,
      'A **soil profile** is a vertical section through the soil, from the surface down into the parent material. Its layers, roughly parallel to the surface, are **horizons**, each fairly uniform in its properties.',
      '- **O horizon:** organic litter (leaves, roots) on the surface; common under forest and grassland.',
      '- **A horizon (topsoil):** mineral soil mixed with **humus**; dark, full of roots and life.',
      '- **B horizon (subsoil):** where clay, iron, aluminium and organic matter washed down from above **accumulate** (**illuviation**), or where the rock structure has weathered away.',
      '- **C horizon:** loose or weakly consolidated weathered parent material that still shows rock structure (river alluvium, wind-blown silt, beach sand).',
      '- **R:** hard bedrock below.',
      '**Regolith** = all the loose material above solid rock. The upper, biologically weathered part of the regolith (O, A and B) is the **solum** — the true soil, which supports plant growth.',
      '**How fast?** Profiles develop where water can move through the soil: sandy parent materials (few soluble minerals, fast drainage) show a mature profile quickly; clays drain slowly and develop slowly. Replacing **1 cm** of lost soil takes **120–400 years**, so a 20 cm topsoil needs **2400–8000 years**. Soil lost to erosion is lost for our lifetime.'),
    ST('prof-st', 'Walk down a soil profile', 49, 'profile',
       [('O: fallen leaves and roots, slowly turning into humus.', 'hO'), ('A: the dark topsoil where most roots and soil organisms live.', 'hA'),
        ('B: the subsoil, where clay and iron washed down from the A horizon collect.', 'hB'), ('C: weathered rock that still shows its rock structure.', 'hC'),
        ('R: the solid bedrock the soil formed from.', 'hR')]),
    T('=agri11-u2-c13', '2.2.3 Soil composition: a three-phase system', 50,
      'Soil has **three phases**:',
      '- **Solid** — mineral particles (sand, silt, clay) and organic matter (humus). Solids plus the pores between them form the **soil matrix**.',
      '- **Liquid** — water with dissolved substances = the **soil solution**.',
      '- **Gas** — the **soil air** (soil atmosphere).',
      'Soil is like a **sponge** full of tiny winding pores, and a chemical factory: living organisms make enzymes, sugars, proteins and DNA that are used up and remade all the time.'),
    DG('comp-fig', 'What is in a good topsoil?', 51, 'composition',
       'In a good loam about half the volume is solid (45 % minerals + 5 % organic matter) and half is pore space shared by water and air. After rain, water fills more pores; as the soil dries, air takes their place.'),
    T('density', 'Bulk density, particle density and porosity', 52,
      '- **Bulk density (BD)** = mass of oven-dry soil ÷ **total** volume (solids + pores). Typical values 1.1–1.6 g/cm³.',
      '- **Particle density (PD)** = mass of oven-dry soil ÷ volume of **solids only**. For most mineral soils about **2.65 g/cm³**.',
      '- **Porosity (f)** = volume of **pores** ÷ total volume = 1 − BD/PD (as a % multiply by 100).',
      'A **high bulk density** means few pores: the soil is **compacted** (by tractors, trampling, or ploughing at the same depth year after year), roots struggle and water soaks in slowly.',
      '**Correction:** the textbook example writes "1.33 mg/cm³" and "f = Vs/Vt". The unit should be **g/cm³**, and porosity uses the volume of **pores** (Vp), not of solids: f = Vp/Vt. In its own example both volumes are 0.5 cm³, so the answer 50 % is still right.'),
    WK('wk-bd', 'Worked example — the textbook cube', 52,
       'A 1 cm³ soil sample contains 1.33 g of oven-dry solids, and the solids occupy 0.5 cm³. Find the bulk density, particle density and porosity.',
       ['Bulk density = 1.33 g ÷ 1 cm³ = **1.33 g/cm³**.',
        'Particle density = 1.33 g ÷ 0.5 cm³ = **2.66 g/cm³**.',
        'Pore volume = 1 − 0.5 = 0.5 cm³, so porosity = 0.5 ÷ 1 = **0.50 = 50 %**.',
        'Check with the formula: 1 − 1.33/2.66 = 1 − 0.5 = 0.5 ✓.'],
       'BD = 1.33 g/cm³, PD = 2.66 g/cm³, porosity = 50 %.'),
    T('=agri11-u2-c14', '2.2.4 Soil properties: physical', 53,
      'Soil has **physical, chemical and biological** properties. The physical ones are: **texture, structure, consistency**, the liquid phase (water), the gas phase (air) and others such as **temperature, depth and colour**.',
      '**Soil texture** = the size range of the particles, i.e. the relative proportions of **sand, silt and clay** (the soil separates). Feel: coarse and gritty (sandy) or fine and smooth (clayey).'),
    DG('size-fig', 'Sand, silt and clay', 55, 'sizes'),
    TB('sep', 'Sand, silt and clay compared', 55, ['Property', 'Sand', 'Silt', 'Clay'],
       [['Diameter', '0.05–2.00 mm', '0.002–0.05 mm', 'less than 0.002 mm'],
        ['Feel when moist', 'Gritty, rough', 'Smooth, floury', 'Sticky, plastic, smooth'],
        ['Water holding', 'Low — drains fast', 'Medium', 'High — can waterlog'],
        ['Nutrient holding', 'Low', 'Medium', 'High (colloids)'],
        ['Air and drainage', 'Very good', 'Medium', 'Poor when wet'],
        ['Tillage', 'Easy ("light" soil)', 'Medium; crusts', 'Hard ("heavy"); cracks when dry']], layout='compare'),
    TB('classes', 'When is a soil "sandy", "silty" or "clayey"? (Table 2.3)', 54, ['Class group', 'Rule'],
       [['Sandy soils', 'At least 70 % sand and 15 % or less clay'],
        ['Silty soils', 'At least 80 % silt and 12 % or less clay'],
        ['Clayey soils', 'At least 35 % clay (includes sandy clay and silty clay)'],
        ['Loam', 'A balanced mixture of sand, silt and clay — the best agricultural soil']], layout='terms'),
    T('=agri11-u2-c15', '2.2.5 Methods of soil texture determination', 54,
      '**a) The feel method** — quick, in the field. Moisten a small sample and rub it between thumb and forefinger:',
      '- **Sand:** rough and gritty; will not form a ribbon.',
      '- **Silt loam:** forms aggregates with some roughness; smooth like flour.',
      '- **Clay:** smooth, sticky, makes a long ribbon, no gritty feeling.',
      '**b) Mechanical analysis** — in the laboratory the sand, silt and clay fractions are separated and weighed using the **hydrometer** or **pipette** method.',
      '**Using the soil texture triangle:** find the % **clay** on its side and follow the line inward (horizontal), do the same for % **silt** and % **sand**; the textural class is the region where the three lines meet.'),
    ST('tri-st', 'Using the texture triangle step by step', 56, 'triangle',
       [('A soil from a farm near Hamelmalo has 60 % sand, 30 % silt and 10 % clay. Start with clay: the 10 % clay line runs straight across.', 'k1'),
        ('Silt: the 30 % silt line runs parallel to the left (sand–clay) side.', 'k2'),
        ('Sand: the 60 % sand line runs parallel to the right (silt–clay) side.', 'k3'),
        ('The three lines meet in the **sandy loam** region. Two lines are enough; the third is a check (60 + 30 + 10 = 100).', 'k4')]),
    T('=agri11-u2-c16', '2.2.6 Soil structure', 56,
      '**Soil structure** = how the primary particles (sand, silt, clay) are grouped into larger units called **peds** or **aggregates**, classified by size, shape and how distinct they are.',
      '**What builds good structure:** organic matter and cations such as **Ca²⁺, Mg²⁺, Fe³⁺, Al³⁺** cause **flocculation** (binding) and stable aggregates. **Sodium (Na⁺) disperses** aggregates, so sodic soils have unstable structure.',
      '**Soil crusting:** raindrops on bare soil smash aggregates and seal the surface pores, so water runs off and seedlings cannot push through. Reduce it with **surface cover (mulch, residues)** and **light tillage**.'),
    DG('str-fig', 'Six shapes of structure', 57, 'structure'),
    TB('structtbl', 'Soil structure groups (Table 2.5)', 57, ['Type', 'Shape', 'Where found'],
       [['Apedal (structureless)', 'Single grains, no peds (or one solid mass)', 'Sand dunes'],
        ['Spheroidal: granular and crumb', 'Small rounded peds; crumb is very porous', 'A horizons rich in organic matter — ideal seedbed'],
        ['Platy', 'Horizontal plates', 'Inherited from parent material or made by compaction'],
        ['Prism-like: prismatic and columnar', 'Vertical columns; flat tops (prismatic) or rounded tops (columnar)', 'B horizons of arid soils (columnar in sodic, natric B) and poorly drained soils'],
        ['Block-like: angular and sub-angular blocky', 'Cube-like blocks', 'B horizons of humid regions']], layout='cards'),
    T('consist', 'Soil consistency', 58,
      '**Consistency** describes how the soil resists pressure or handling. It matters for **tillage** and **compaction by machines** and is judged in three moisture states:',
      '- **Dry:** soft, hard or cemented.',
      '- **Moist:** loose, friable (crumbles easily — best for ploughing) or firm.',
      '- **Wet:** sticky and plastic.',
      '**Practical rule:** plough a clay soil (for example the black cracking soils near Tesseney and Goluj) when it is **moist and friable**: when wet it smears and sticks to the maresha; when dry it is hard as brick.'),
    T('liquid', 'The soil liquid phase and water movement', 58,
      'Water in soil dissolves nutrients, carries them to roots, and controls soil air and temperature.',
      'Water moves because of differences in **energy**. **Soil-water potential** compares the free energy of soil water with that of pure water; water moves from **higher to lower** potential (from wet soil to drier soil, and from soil into roots). Kinetic energy matters for flowing water, e.g. erosion.',
      '- The **drier** the soil, the more tightly the remaining water is held: water content and the tension holding it are **inversely related**.',
      '- **Clay** holds much more water than **sand** at the same potential.',
      '- **Compacted** soil holds less water because its large pores are crushed.'),
    DG('water-fig', 'Water the plant can and cannot use', 59, 'soilwater'),
    T('fcwp', 'Saturation, field capacity and wilting point', 59,
      '- **Saturation:** all pores are full of water (just after heavy rain or irrigation). No air — roots suffocate if it lasts.',
      '- **Field capacity (FC):** the water left after free **gravitational water** has drained away (usually 1–3 days after soaking). The soil holds the most water it can **against gravity**.',
      '- **Permanent wilting point (PWP):** the soil is so dry that roots can no longer take up water and plants wilt and do not recover.',
      '- **Available water = FC − PWP.** Water between saturation and FC drains away; water below PWP is held too tightly.',
      '**Correction:** the textbook says field capacity is "when the surface layer is at or near saturation". Saturation and field capacity are **different**: field capacity is reached **after** the excess (gravitational) water has drained out.'),
    T('=agri11-u2-c17', '2.2.7 Measuring soil water', 59,
      'Soil-water content can be measured **directly** or **indirectly**.',
      '**Gravimetric (direct) method — steps:**',
      '- 1. Put a soil sample of known volume in a container.',
      '- 2. Weigh sample + container.',
      '- 3. Dry in an oven at about **105 °C** (the textbook says 104 °C) for **24 hours**.',
      '- 4. Cool and weigh again.',
      '- 5. Calculate: WC % = (W1 − W2) ÷ W1 × 100, where W1 = mass before drying and W2 = mass after drying (the textbook formula, on a **wet-mass basis**).',
      'Soil scientists usually divide by the **dry** mass: WC % = (W1 − W2) ÷ W2 × 100. Always say which one you use.',
      '**Indirect methods:** **electrical resistance** blocks (a probe in the soil; wetter soil conducts better) and the **neutron probe** (neutron scattering by the hydrogen in water).'),
    WK('wk-wc', 'Worked example — gravimetric water content', 60,
       'A soil sample weighs 40 g before drying and 30 g after 24 hours in the oven. Find its water content.',
       ['Water lost = 40 − 30 = 10 g.',
        'Textbook (wet basis): 10 ÷ 40 × 100 = **25 %**.',
        'Dry basis: 10 ÷ 30 × 100 = **33 %**.',
        '25 % lies in the 20–30 % range of a good loam (Figure 2.4), so moisture is adequate for plants.'],
       '25 % on the textbook (wet-mass) basis; 33 % on a dry-mass basis.'),
    T('=agri11-u2-c18', '2.2.8 Soil-water potential and water movement', 61,
      'Measure soil-water potential with a **tensiometer** in the field (0 to 0.8 bar) or in the laboratory with a **tension plate** (up to about 0.8 bar) and a **pressure plate** (from 1 bar upwards).',
      'Three kinds of water movement:',
      '- **Saturated flow** — all pores full; typical of groundwater flow; fastest.',
      '- **Unsaturated flow** — pores partly full; the normal case in field soils; slower.',
      '- **Vapour movement** — water moving as vapour inside pores and from the surface by evaporation; small, but important for drought-resistant plants in dry soils.'),
    T('=agri11-u2-c19', '2.2.9 The soil gaseous phase (soil air)', 61,
      '**Soil aeration** = the rate of gas exchange between soil air and the atmosphere. Air enters only after water drains out of the pores.',
      'Soil air compared with the atmosphere:',
      '- almost **100 % humidity**;',
      '- **CO₂** 5–10 times higher, sometimes up to 10 %;',
      '- **O₂** a little under 20 % near the surface, but 5 % or less deep down in poorly drained soils with few large pores (macropores).',
      'Most plants need **more than 10 % oxygen** in soil air. Roots and most soil organisms respire aerobically; in waterlogged soil they suffocate.'),
    T('=agri11-u2-c20', '2.2.10 Other physical properties: temperature, depth, colour', 62,
      '**Temperature:** controls physical, chemical and biological processes and especially **seed germination**. Dark soils absorb more heat than light soils; heat is lost at night by long-wave radiation. Below about 50 cm daily temperature hardly changes. Eritrean farmers cover seedbeds with **stubble, grass or branches** to keep them moist and help germination.',
      '**Depth:** decides how much water and nutrient the roots can reach; at least **30 cm** is needed for good root growth.',
      '**Colour** (described with the **Munsell** chart: hue, value, chroma) tells us about the soil:'),
    TB('colour', 'What soil colour tells you', 63, ['Colour', 'Meaning'],
       [['Black / dark brown', 'Organic matter (humus) — fertile topsoil'], ['Reddish-brown', 'Well-drained, iron oxides'],
        ['Grey', 'Iron removed — poor drainage, waterlogging'], ['Whitish crust', 'Salts — arid and semi-arid areas, e.g. near the coast']], layout='terms'),
    T('=agri11-u2-c21', '2.2.11 Chemical properties: colloids and cation exchange', 63,
      'The key chemical properties are **soil colloids**, **soil reaction (pH)** and **salinity**.',
      '**Colloids** ("glue-like"): very small particles (mostly < 2 μm = 0.002 mm) with a huge surface area — 1 g of clay has at least **1000 times** the surface of 1 g of sand. They are the most chemically active part of soil. **Inorganic** colloids = clay; **organic** colloids = **humus** (mainly C, H and O with some N, P, S).',
      'Physical behaviour of clay colloids: **plasticity, cohesion, swelling and shrinking, dispersion and flocculation**.',
      '**Charge:** colloids carry negative (and some positive) charges; some are permanent, some change with pH (more negative at high pH, more positive at low pH). Negative sites hold **cations**: Ca²⁺, Mg²⁺, K⁺, NH₄⁺, Na⁺ (basic cations, common in alkaline soils) and H⁺, Al³⁺ (acidic cations, common in acid soils).',
      '**Cation exchange:** held cations swap with cations in the soil solution, e.g. colloid–Ca²⁺ + 2NH₄⁺ ⇌ colloid–2NH₄⁺ + Ca²⁺. The total amount a soil can hold is its **cation exchange capacity (CEC)** (about 2–60 cmol(+)/kg). High CEC = a good nutrient "bank".'),
    T('reaction', 'Soil reaction: acidity and alkalinity', 65,
      '**pH = −log[H⁺]**. Each unit up means **10 times fewer** H⁺ ions: a solution with [H⁺] = 10⁻⁵ mol/L has pH 5.',
      'pH < 7 acidic; pH 7 neutral; pH > 7 alkaline. For soils "neutral" usually means **pH 6.5–7**.',
      '**Acid soils** form where **high rainfall** leaches the basic cations (Ca, Mg, K) below the root zone. They are corrected by **liming** (adding ground limestone, CaCO₃), which neutralises H⁺ and adds calcium.',
      '**Alkaline soils** occur in **dry areas** with high base saturation, where rain is too little to leach salts. They are **calcareous** (calcite, CaCO₃), **dolomitic** (CaCO₃·MgCO₃) or **sodic** (Na₂CO₃, pH 9–10, up to 10.5).'),
    DG('ph-fig', 'The pH scale for soils', 65, 'ph'),
    T('salinity', 'Salinity and salt-affected soils', 66,
      'Three effects of salt on plants:',
      '- **direct toxicity** (sodium, chloride, boron);',
      '- **ionic imbalance** in the plant;',
      '- **less water uptake** because salt lowers the osmotic potential — called **physiological drought**: the plant suffers from lack of water although the soil is wet.',
      '**Sodicity is worse than salinity alone.** At an exchangeable sodium percentage (ESP) of 10–15 % clay soils swell and disperse and structure collapses. **Calcium** protects soil structure and defends plants against sodium.',
      '**Management:** calcareous or dolomitic alkaline soils are not neutralised (it would need far too much acid); grow **tolerant crops** and use **suitable fertilizers**. Saline or sodic soils must be **reclaimed** before irrigated cropping.'),
    TB('salt', 'Salt-affected soils and how to reclaim them (Tables 2.6 and 2.7)', 67, ['Soil', 'EC (dS/m)', 'ESP', 'pH', 'Sign in the field', 'Reclamation'],
       [['Saline', '> 4', '< 15 %', '< 8.5', 'White salt crust (Na, Ca, Mg chlorides and sulphates)', 'Leach salts below the root zone with good-quality water (with drainage)'],
        ['Sodic', '< 4', '> 15 %', '> 8.5', 'Dark, sticky, dispersed; poor infiltration', 'Gypsum (CaSO₄) on the surface: Ca²⁺ replaces Na⁺; plant grass or forage to rebuild structure'],
        ['Saline-sodic', '> 4', '> 15 %', '< 8.5', 'Salty and sodic together', 'Gypsum first (keeps Ca high), then leach']], layout='cards'),
    MN('mn-salt', 'Memory trick — 4, 15, 8.5', 67,
       'Saline: **EC above 4**. Sodic: **ESP above 15**. Sodic soils have **pH above 8.5**. Gypsum fixes sodium; water fixes salt.'),
    T('=agri11-u2-c22', '2.2.12 Biological properties', 68,
      'A healthy hectare can hold about **20 000 kg** of living organisms (as heavy as about 40 horses), although they make up only about **5 %** of soil organic matter.',
      '- **Roots** take up water and nutrients and release **exudates** that feed microbes. The **rhizosphere** is the busy zone around roots: lower pH, less O₂, more CO₂, many more microbes.',
      '- **Earthworms** mix organic matter into mineral soil. Their **casts** are richer in nutrients (N, P, K, trace elements, about 50 % organic matter) than the surrounding soil. Worms like moist, non-acid soil with organic matter and calcium.',
      '- **Other animals:** parasitic nematodes (attack tomato, carrot, potato, peas, alfalfa, fruit trees), centipedes (predators), millipedes (eat decaying plants), fly and beetle larvae (eat roots), ants, termites, slugs, snails and burrowing mammals.',
      '- **Fungi** decompose organic matter, even tough lignin in wood; they dominate in acid forest soils.',
      '- **Bacteria** are the most numerous: 1–10 million per gram. **Autotrophs** fix CO₂; **heterotrophs** decompose organic matter. Free-living bacteria fix nitrogen; **Rhizobium** fixes nitrogen in the root nodules of legumes (beans, peas, chickpea, grass pea, alfalfa). Some make sticky substances that build aggregates; others clean pollutants (**bioremediation**: herbicides, heavy metals, petroleum).',
      '- **Actinomycetes** — thread-like bacteria that break down tough **cellulose** and **chitin**, even at high pH; some fix nitrogen with non-legume plants.'),
    T('decomp', 'Decomposition, humus and nutrient cycling', 70,
      'Microbes decompose organic matter fastest when the soil is about **20 °C**, moisture is **50–70 % of water-holding capacity**, there is enough **oxygen** and fresh organic matter as food.',
      '**Humus** (the stable end product) supplies N, P and S, raises the **CEC**, holds a lot of water, and binds particles into aggregates — improving structure, infiltration and resistance to erosion.',
      '**Green manure / cover crops** are grown and then ploughed in to add organic matter; they also protect the soil from wind and water erosion.',
      '**Soil quality** = the soil\'s ability to support crop growth without degrading or harming the environment.'),
    DG('nut-fig', 'Round and round: the nutrient cycle', 71, 'nutrient',
       'Losses leave the cycle by leaching, erosion and crop removal; inputs come from manure, fertilizer and nitrogen fixation. Burning dung for fuel breaks the cycle.'),
    T('=agri11-u2-c23', '2.2.13 Soil types of Eritrea', 71,
      'Early classifications used texture or parent material; modern ones use **diagnostic horizons**. Soil maps are based on properties that do not change easily: **texture, degree of leaching and CEC**. Eritrea has **13 major soil groups**.'),
    TB('types', 'The 13 soil groups of Eritrea (Table 2.8)', 72, ['Soil group', 'Main feature'],
       [['Lithosol', 'Shallow, weakly developed (over rock)'], ['Regosol', 'Weakly developed, finer than sandy loam'],
        ['Fluvisol', 'On river deposits, layered (alluvial)'], ['Arenosol', 'Sandy or loamy-sand texture'],
        ['Vertisol', 'Clay that cracks widely when dry and swells when wet'], ['Cambisol', 'Moderately developed, cambic B horizon'],
        ['Nitisol', 'Deep clay-rich subsoil with shiny ped faces'], ['Lixisol', 'Clay-rich subsoil, low CEC, high base saturation'],
        ['Solonchak', 'Salt accumulation dominates'], ['Solonetz', 'Dominated by sodium'],
        ['Gypsisol', 'Gypsum crystals or layers'], ['Calcisol', 'Lime (calcium carbonate) powder or nodules'],
        ['Luvisol', 'Clay-rich subsoil, high CEC, high base saturation']], layout='terms'),
    WK('wk-acid', 'Worked example — Exercise 2.2 Q5–Q7', 72,
       'Where is soil acidity common, how are acid soils reclaimed, and how are alkaline soils managed?',
       ['Acidity: in **high-rainfall** areas where basic cations are leached below the root zone.',
        'Reclaiming acid soils: apply **agricultural lime** (ground limestone, CaCO₃, or dolomite) to raise pH; add organic matter.',
        'Alkaline (calcareous) soils: do not try to neutralise them; grow **tolerant crops** and use **suitable (acid-forming) fertilizers**.',
        'Saline or sodic soils: leach salts with good water and drainage; apply **gypsum** to sodic soils.'],
       'Acidity: high-rainfall, leached soils → lime. Alkaline: tolerant crops + suitable fertilizer; saline → leach; sodic → gypsum.'),
]

# ------------------------------------------------------------------ 2.3 biodiversity
L3 = [
    T('=agri11-u2-c24', '2.3 Biodiversity and 2.3.1 terrestrial biodiversity', 74,
      '**Biodiversity** is the variety of life from all sources — land, sea and other water ecosystems — at three levels: **within species** (genetic), **between species**, and **of ecosystems**.',
      '**Terrestrial biodiversity** = life on land dominated by natural habitats, described at **ecosystem** and **species** level.',
      '**a) Forest biodiversity** is concentrated in three areas:',
      '- the **Eastern Escarpment** — relatively high rainfall; a distinct forest type (e.g. around Filfil);',
      '- the **riverine forests of the Western Lowlands** — along the Gash, Setit and Barka; raw materials for local industry, grazing and browsing;',
      '- small pockets in the **Northern Highlands** — the last fairly large stands of **Olea africana** (wild olive, awlie) and **Juniperus procera** (tsihdi), which once probably covered the highlands.',
      '**b) Woodland biodiversity:** woodlands cover almost **65 %** of the land and shelter wildlife such as elephants, leopards and plains game.',
      '**Flora** = all plant forms from algae and fungi to mosses, ferns and flowering plants. Higher plants are well documented in Eritrea; lower plants are not yet studied at species level.'),
    TB('themes', 'Eritrea\'s 10 biodiversity themes', 76, ['Theme', 'Meaning'],
       [['Integrated management', 'Use several methods together to conserve'], ['Sustainable use', 'Use resources without exhausting them'],
        ['Alien invasive species', 'Manage introduced species (e.g. Prosopis juliflora)'], ['Pollution management', 'Protect biodiversity from pollution'],
        ['In-situ conservation', 'Conserve on farmers\' fields or in protected areas'], ['Ex-situ conservation', 'Conserve seeds in gene banks'],
        ['Taxonomic knowledge', 'Identify and classify species'], ['Information', 'Collect and store data'],
        ['Public awareness', 'Education'], ['Legal and institutional', 'Laws and capacity building']], layout='terms'),
    T('=agri11-u2-c25', '2.3.2 Importance of biodiversity', 76,
      '**a) Source of crops and crop genes.** Biodiversity is a **gene pool**: new varieties that resist drought and pests, or yield more, come from new genes. Over the last 50 years war, drought and pests have caused **genetic loss**, countered by:',
      '- **Ex-situ** conservation — in **gene banks** (seed stores) away from the natural place;',
      '- **In-situ** conservation — on **farmers\' fields** and in **enclosures** where the plants grow naturally.',
      'Eritrea is part of the **Abyssinian centre of diversity** (Vavilov): barley, wheat, oats, linseed, safflower, chickpea, lentil, grass pea, field pea, faba bean, rapeseed and mustard are very diverse here, and **teff (taff)** and **Niger seed (nihug)** were domesticated here.',
      '**Landraces** are local varieties selected by farmers over generations and adapted to local conditions. They differ in seed colour, plant height, drought resistance and **earliness**; some are preferred for food; tall, late landraces need more water.',
      '**b) Source of livestock breeds** (see the table), well adapted to local conditions — traits that can be lost by careless cross-breeding.',
      '**c) Raw materials:** timber, fibre, gums, resins, perfumes, fur. **d) Medicine:** traditional and modern drugs. **e) Income:** unspoiled habitats attract tourists and create jobs.'),
    TB('breeds', 'Eritrea\'s local livestock (p. 77–78)', 77, ['Species', 'Breeds / types', 'Note'],
       [['Cattle', 'Barka, Arado, Arebo (Aden); Dewhin on the Sudan border; Holstein-Friesian introduced', 'Barka moving into the highlands; pure Arebo now rare'],
        ['Goats', 'Hassani (Shukria), Sudanese Desert (Barka / Tsa\'adi), Worre, Afar', 'Hassani: good milk, often twins and triplets'],
        ['Sheep', 'Akele Guzai (Shimejana), Rashaidi, Adali (Afar), Arrit, Barka, Sudan Desert (Aral, Hamale)', 'Many fat-tailed types'],
        ['Camels', 'All one-humped: Ariri, Arho, Rashaidi', 'Gash-Barka, Anseba, Northern and Southern Red Sea'],
        ['Donkeys', 'Lowland (Rifai) and Highland', 'Rifai is taller and slimmer — riding and transport'],
        ['Poultry', 'Indigenous chickens of many sizes, plumages and combs', 'Most of Eritrea\'s birds'],
        ['Bees', 'Mostly in the highlands and on the eastern and western escarpments', 'Traditional hives; modern hives being introduced']], layout='cards'),
    T('=agri11-u2-c26', '2.3.3 The status of Eritrean biodiversity', 79,
      'Land degradation, climate change and other human pressures are the greatest threats.',
      '**Crops:** genetic loss comes from **drought** (tall, high-yielding, late landraces have disappeared), **changing practices** (one crop replaced by another) and **land degradation** (varieties once grown on fertile soils are no longer grown).',
      '**Livestock:** threatened by drought (survivors after a drought are not the same population — older people remember Barka cattle being larger and more docile 30–40 years ago), **uncontrolled interbreeding** (the four cattle breeds look more and more alike, helped by roads and markets), and **changing distribution and numbers** (Barka advancing into the highlands and diluting Arado; Butana and Dewhin from Sudan mixing with Barka).',
      '**Wildlife:** about **126 mammal** species (9 marine), **577 bird** species (about 320 resident; about 150 Palaearctic migrants from Europe; no national endemic bird, about 13 regional endemics), **90 reptile** and **19 amphibian** species.'),
    TB('wild', 'Status of some wild mammals (Table 2.11)', 82, ['Status', 'Examples'],
       [['Common', 'Warthog, Soemmerring\'s gazelle, dugong'], ['Rare', 'Elephant, African wild ass'],
        ['Endangered', 'Hartebeest, red-fronted gazelle, Nubian ibex'], ['Critical', 'African wild dog, lion'],
        ['Extinct (in Eritrea)', 'Gelada, Ethiopian wolf, Walia ibex, black rhinoceros'], ['Unknown', 'Three bat species']], layout='terms'),
    TB('insitu', 'In-situ and ex-situ conservation compared', 77, ['Feature', 'In-situ', 'Ex-situ'],
       [['Where', 'On farmers\' fields, enclosures, protected areas', 'Gene banks, seed stores, botanical gardens'],
        ['Example', 'Farmers in Hamasien keep growing their own barley landraces', 'Seeds of sorghum landraces stored cold in the national gene bank'],
        ['Advantage', 'Plants keep evolving with the local climate and pests', 'Safe from drought, war and fire; many samples in little space'],
        ['Limitation', 'Can be lost in a drought or by land-use change', 'Plants stop adapting; needs electricity and skilled staff']], layout='compare'),
    WK('wk-hf', 'Worked example — Exercise 2.3 Q2', 83,
       'Can the Holstein-Friesian breed pose a risk to Eritrea\'s local cattle? Give reasons.',
       ['Yes, if crossing is uncontrolled: repeated crossing with Holstein bulls (or semen) dilutes local genes.',
        'Local breeds (Arado, Barka) carry **adaptations**: heat and tick tolerance, disease resistance, walking long distances, surviving on poor feed.',
        'If pure local animals disappear these genes are lost, and future breeders cannot use them when the climate becomes harsher.',
        'Solution: controlled breeding, keeping pure local herds (in-situ) and storing semen or embryos (ex-situ).'],
       'Yes — uncontrolled crossing can erase adapted local genes; keep pure local herds and gene banks.'),
]

# ------------------------------------------------------------------ 2.4 water
L4 = [
    T('water-intro', 'Water resources: why they decide farming', 85,
      'Water (H₂O) is the universal solvent. It covers about three-quarters of the Earth\'s surface, but most is **salty** and useless for farming without desalination. **Fresh water** is renewable through rain, but finite and unevenly spread.',
      'Where rain is **too much**, land needs **drainage**; where it is **too little**, crops need **supplementary irrigation** from wells, canals, ponds and tanks, by **gravity** or by **pumping**, plus moisture conservation. Without these, moisture stress cuts or destroys the yield.'),
    DG('hydro-fig', 'The water cycle', 85, 'hydro',
       'Rain that falls can evaporate, run off, or infiltrate. In Eritrea about 80–87 % evaporates or is transpired before it reaches streams or aquifers — so every drop held on the field counts.'),
    T('=agri11-u2-c27', '2.4.1 Groundwater', 86,
      'Groundwater is described by its **depth, quantity, quality and use**. It is stored in **aquifers**. In Eritrea the main aquifers are **loose alluvial deposits in riverbeds**.',
      '- The riverbeds of the **Barka, Gash and Anseba** have substantial potential for **irrigation from shallow wells**.',
      '- Limited groundwater lies along riverbeds of the northern Red Sea coast, where **salinity** is a problem. Salinity increases with **well depth**, **distance from the river channel** and **closeness to the sea**.',
      '- In mid- and low-altitude parts of the eastern and western escarpments groundwater rises as **springs**, seasonal or permanent, and flows on underground to the aquifers of the eastern and western flood plains.',
      '- Underground flow through the base rock is the **main water supply for rural communities** in the highlands and midlands.',
      'Groundwater movement depends on **topography, soil characteristics and geology**.'),
    T('=agri11-u2-c28', '2.4.2 Surface water', 87,
      'Surface water = intermittent rivers, streams, and runoff stored in **reservoirs** (dams, ponds). Its advantages: it can be **collected and stored**, and used for **domestic needs, irrigation and livestock**. Rain from roofs can be stored in **cisterns**.',
      '**Eritrean examples:** micro-dams and ponds built since independence store runoff for irrigation and livestock; the Gerset dam on the Gash supports irrigated farming.'),
    T('=agri11-u2-c29', '2.4.3 The major river basins', 88,
      'Eritrea has **five major basins**: **Setit, Mereb-Gash, Barka-Anseba, Red Sea and Danakil Depression**. All rivers are **ephemeral** (seasonal) **except the Setit**.',
      '- **Setit:** rises in central Ethiopia and forms the south-western border; flow is highly seasonal — over 900 m³/s in July–September, falling to a base flow of 5–10 m³/s; **perennial**.',
      '- **Mereb-Gash:** a narrow, westward basin south of the central highlands; rainfall 350–700 mm; mean annual flow 480–760 million m³; flows strongly July–September. Its upper basin is badly eroded, leaving sands and gravels in the valleys — the riverbed now stores groundwater for irrigation.',
      '- **Barka-Anseba:** both rivers rise around Asmara, flow north-west and meet near the Sudan border; rainfall from 500 mm (highlands) to below 200 mm; spate floods in July–September; runoff about 360 million m³, much of it soaking into lowland alluvium.',
      '- **Red Sea:** many small basins. North of the Gulf of Zula rivers come down the eastern escarpment (about 730 million m³ a year reaches the sea); south of the gulf they flow from the Danakil ridge. Used for **spate irrigation** and recharge of coastal wells.',
      '- **Danakil:** the driest basin (< 100 mm rain); short, irregular floods; the Ramod and Regale rivers give about 136 million m³; the **Bada** spate scheme lies where they meet.'),
    DG('basin-fig', 'Basin sizes and runoff', 88, 'basins'),
    TB('basintbl', 'The five basins (Table 2.12)', 88, ['Basin', 'Area (km²)', 'Runoff (million m³)', 'Rainfall (mm)', 'Remember'],
       [['Setit', '4 045', '5 800–8 000', '900', 'Smallest, only perennial'], ['Mereb-Gash', '23 200 (16 730 in Eritrea)', '480–760', '350–700', 'Eroded upper basin; riverbed aquifer'],
        ['Barka-Anseba', '39 510', '360', '200–500', 'Rises near Asmara; spate floods'], ['Red Sea', '44 690', '730', '50–1 100', 'Largest; spate irrigation'],
        ['Danakil', '10 530', '136', '< 100', 'Driest; Bada spate scheme']], layout='cards'),
    WK('wk-ex24', 'Worked example — Exercise 2.4 Q1 and Q3', 90,
       'Name the largest and smallest basins. What effect does highland rainfall have on lowland groundwater?',
       ['Compare areas: Red Sea 44 690 km² is the **largest**; Setit 4 045 km² is the **smallest**.',
        'Highland rain runs off and infiltrates; water moves **down-slope underground** through rock and riverbeds.',
        'It **recharges** the alluvial aquifers of the eastern and western lowlands, which feed wells and irrigation there — so conserving water in the highlands also helps lowland farmers.'],
       'Largest: Red Sea; smallest: Setit. Highland rain recharges lowland aquifers through underground flow.'),
]

# ------------------------------------------------------------------ 2.5 agro-ecological zones
L5 = [
    T('=agri11-u2-c30', '2.5 What an agro-ecological zone is; the Sudano-Sahelian region', 91,
      'An **agro-ecological zone (AEZ)** is an area with a definable range of **climate, landform, soil and vegetation**, so it has a fairly uniform set of **constraints and potentials** for farming.',
      '**2.5.1** Eritrea lies in the **Sudano-Sahelian region**, which stretches from Eritrea in the east to Senegal in the west. The **Sahelian** part is drier and poorer in plants and animals than the **Sudanian** part.',
      'Africa has **20 major centres of endemism**; **five** meet in Eritrea: the **Sahelian**, **Sudanian**, **Afromontane**, **Somali-Masai** regions and the **Sahara transitional zone** — one reason for Eritrea\'s rich biodiversity in a small country.'),
    DG('aez-fig', 'Six zones by altitude and rainfall', 95, 'aez',
       'Zones overlap in altitude; rainfall, temperature and slope separate them. The two "arid" zones and the semi-desert cover 76 % of the land.'),
    TB('=agri11-u2-c31', '2.5.2 The six agro-ecological zones (Table 2.13 and p. 92–94)', 92, ['Zone', 'Where', 'Rain (mm)', 'Altitude (m)', 'Crops', 'Livestock', 'Area'],
       [['Moist highland', 'Central and southern highlands', '500–700', '1600–3018', 'Barley (0.5–2 t/ha), wheat, teff, sorghum, maize, pulses', 'Sheep, goats, cattle', '7 %'],
        ['Arid highland', 'Northern highlands; steep escarpments, dissected plateaus', '200–500', '1600–2600', 'Sorghum, barley (0.05–0.6 t/ha)', 'Cattle, goats, sheep, camels', '3 %'],
        ['Moist lowland', 'South-west and upper Mereb valley; savannah woodland', '500–800', '500–1600', 'Sorghum (2.5–3 t/ha), sesame, cotton, pearl millet, maize', 'Cattle, goats, sheep, camels', '16 %'],
        ['Arid lowland', 'North and lower eastern escarpment; doum palm on riverbanks', '200–500', '400–1600', 'Sorghum (0.5–1.5 t/ha), pearl millet', 'Goats, cattle, camels, sheep', '34 %'],
        ['Sub-humid escarpment', 'Central eastern escarpment; juniper and olive forest', '700–1100', '600–2600', 'Maize, sorghum, coffee, barley — limited by steep slopes, shallow soils', 'Cattle, goats', '1 %'],
        ['Semi-desert', 'Coast, islands, north-west of the Barka–Sawa rivers', '< 200', '< 100–1355', 'Maize and sorghum under spate irrigation (1.5–2 t/ha)', 'Goats, camels, sheep, cattle', '39 %']], layout='cards'),
    TB('aezclim', 'Climate figures of the zones (Table 2.13)', 95, ['Zone', 'Temp (°C)', 'PET (mm)', 'Growing period (days, dependable–median)'],
       [['Sub-humid', '16–27', '1600–2000', '60–210 / 90–240'], ['Arid highland', '15–21', '1600–1800', '0–30 / 30–60'],
        ['Moist highland', '15–21', '1600–1800', '60–110 / 90–120'], ['Moist lowland', '21–28', '1800–2000', '50–90 / 60–120'],
        ['Arid lowland', '21–29', '1800–2000', '0–30 / 30–60'], ['Semi-desert', '24–32', '1800–2100', '0 / < 30']], layout='cards'),
    MN('mn-aez', 'Memory trick — sizes from biggest to smallest', 95,
       '**S**emi-desert 39, **A**rid lowland 34, **M**oist lowland 16, **M**oist highland 7, **A**rid highland 3, **S**ub-humid 1: "**SAM MAS**" — and the numbers add up to 100.'),
    T('=agri11-u2-c32', '2.5.3 Major agricultural land-use practices', 95,
      '**Land use** = how land is developed and used (agriculture, homes, industry) and what may be built on it.',
      'Traditionally each village is divided into **grazing, farming, forest, water and settlement** areas. In the highlands farmland is graded **fertile, medium and poor**, and **fertile land is never used for houses** — it is the village breadbasket.',
      'Cultivated land is only about **7 %** of Eritrea (Table 2.14). Grazing land is not demarcated, so there is no clear boundary between farmland and grazing land.'),
    DG('land-fig', 'Land cover', 96, 'landcover'),
    WK('wk-aez', 'Worked example — choosing a zone', 93,
       'An investor wants to grow rain-fed sesame and cotton. Which zone should he choose, and why not the moist highland?',
       ['Sesame and cotton are **warm-season** crops needing heat and 500 mm or more of rain.',
        'Moist lowland: 21–28 °C, 500–800 mm, growing period 60–120 days, sorghum 2.5–3 t/ha — it already grows sesame and cotton.',
        'Moist highland: only 15–21 °C — too cool for good sesame and cotton.',
        'So the **moist lowland** (south-west, e.g. around Tesseney and Barentu, and the upper Mereb valley).'],
       'The moist lowland — warm and wet enough; the moist highland is too cool.'),
    WK('wk-match', 'Worked example — Exercise 2.5 matching', 97,
       'Match: 1 Semi-desert, 2 Central and southern highlands, 3 Northern highlands, 4 Coastal plain zone, 5 South-western part — with A Arid highland, B Spate irrigation, C Moist highland, D Moist lowland, E Halophytic plants (Acacia mellifera, A. nubica).',
       ['1 Semi-desert → **E** (its vegetation is halophytic scrub).',
        '2 Central and southern highlands → **C** moist highland.',
        '3 Northern highlands → **A** arid highland.',
        '4 Coastal plain → **B** spate irrigation (maize and sorghum).',
        '5 South-western part → **D** moist lowland.'],
       '1-E, 2-C, 3-A, 4-B, 5-D.'),
]

LESSONS = {'agri11-u2-l2-1': L1, 'agri11-u2-l2-2': L2, 'agri11-u2-l2-3': L3, 'agri11-u2-l2-4': L4, 'agri11-u2-l2-5': L5}
DROP = ['agri11-u2-c01', 'agri11-u2-c10']  # decorative picture; mis-titled summary ("Soil in one page" about climate and water)

# ------------------------------------------------------------------ practice
a = QSet('2.1 Practice — climate', 's21')
a.M(39, 'Which instrument measures wind speed?', ['Wind vane', 'Cup anemometer', 'Barograph', 'Hygrometer'], 'B',
    ['Step 1: An anemometer\'s cups spin faster in stronger wind.', 'Step 2: A wind vane shows direction, not speed.'], 'Anemo- = wind; -meter = measure.', [('Which instrument shows wind direction?', 'The wind vane.')])
a.M(39, 'An evaporation pan is used to', ['record air pressure', 'measure water lost by evaporation', 'measure rainfall intensity only', 'record sunshine hours'], 'B',
    ['Step 1: The pan holds water; the drop in level per day is the evaporation (mm/day).', 'Step 2: Farmers use it to estimate irrigation needs.'], 'Pan = open water surface.', [('Which instrument records sunshine hours?', 'The sunshine recorder.')])
a.S(41, 'Using Table 2.1, estimate the maximum temperature at Keren (about 1460 m).', 'About 29.5 °C',
    ['Step 1: Maximum = 36.8 − 0.005 × h.', 'Step 2: 0.005 × 1460 = 7.3.', 'Step 3: 36.8 − 7.3 = 29.5 °C.'], 'Multiply first, then subtract.', [('Minimum at Keren?', '25.3 − 0.007 × 1460 = 15.08 ≈ 15.1 °C.')])
a.S(41, 'Estimate the mean temperature and PET of a place at 1500 m.', 'Mean 22 °C; PET 1772 mm per year',
    ['Step 1: Mean = 31.0 − 0.006 × 1500 = 31.0 − 9.0 = 22.0 °C.', 'Step 2: PET = 2069 − 0.198 × 1500 = 2069 − 297 = 1772 mm.'], 'Same pattern: constant − slope × altitude.', [('PET at 2000 m?', '2069 − 396 = 1673 mm.')])
a.S(41, 'At what altitude would the minimum temperature be 4.3 °C according to Table 2.1?', '3000 m',
    ['Step 1: 4.3 = 25.3 − 0.007 h.', 'Step 2: 0.007 h = 21.0.', 'Step 3: h = 21.0 ÷ 0.007 = 3000 m.'], 'Work backwards: rearrange for h.', [('At what altitude is the maximum 26.8 °C?', '2000 m.')])
a.M(41, 'Relative humidity is expressed as', ['grams', 'millimetres', 'a percentage', 'degrees Celsius'], 'C',
    ['Step 1: RH compares the vapour present with the vapour at saturation.', 'Step 2: A ratio × 100 = a percentage.'], 'Relative = compared → %.', [('Name a disease favoured by high humidity.', 'Downy mildew of grapes or onions.')])
a.TF(42, 'True or false: a water deficit exists when rainfall is greater than potential evapotranspiration.', 'False',
    ['Step 1: A deficit means the plant needs more water than the rain supplies.', 'Step 2: That happens when rainfall is LESS than PET.'], 'Deficit = demand > supply.', [('If rainfall is 400 mm and PET 1800 mm, is there a deficit?', 'Yes, 1400 mm.')])
a.M(43, 'Valley soils are usually deeper and richer than hilltop soils because', ['valleys get more sunlight', 'soil eroded from slopes is deposited in valleys', 'valleys never have frost', 'rocks in valleys are younger'], 'B',
    ['Step 1: Water carries soil down-slope.', 'Step 2: It settles where the slope flattens.', 'Step 3: Valleys may even get MORE frost.'], 'Erosion up, deposition down.', [('Why are valley floors at risk of frost?', 'Cold, heavy air drains down and collects there at night.')])
a.S(42, 'Explain how day length (photoperiod) controls a crop.', 'Day length triggers stages of development — especially flowering — and the hardening of plants before cold seasons; it regulates the crop from germination to seed setting.',
    ['Step 1: Plants "measure" the length of day or night.', 'Step 2: When it passes a threshold they switch from leaf growth to flowering.'], 'Photo = light; period = length.', [('Which process needs light energy directly?', 'Photosynthesis.')])

b = QSet('2.2 Practice — soil', 's22')
b.M(46, 'The study of soil in relation to plant production is', ['pedology', 'edaphology', 'geology', 'hydrology'], 'B',
    ['Step 1: Pedology = origin, classification, description.', 'Step 2: Edaphology = soil from the plant\'s point of view.'], 'Edaphology — think "eat": what the plant gets from soil.', [('Which approach classifies and maps soils?', 'Pedology.')])
b.M(46, 'Sandstone and shale are examples of', ['igneous rocks', 'sedimentary rocks', 'metamorphic rocks', 'soil horizons'], 'B',
    ['Step 1: Both form from deposited and re-cemented weathered material.', 'Step 2: Sandstone from sand; shale from clay.'], 'Sediment = settled material.', [('Marble is metamorphosed from which rock?', 'Limestone (or dolomite).')])
b.F(47, 'The five soil-forming factors are parent material, climate, organisms, topography and ____.', 'time', ['time', 'tillage', 'fertilizer', 'irrigation'],
    ['Step 1: Recall "ClORPT".', 'Step 2: T = time.'], 'ClORPT.', [('Which factor controls the speed of chemical reactions in soil?', 'Climate (temperature).')])
b.M(49, 'The horizon of accumulation (illuviation) of clay and iron is the', ['O horizon', 'A horizon', 'B horizon', 'C horizon'], 'C',
    ['Step 1: Materials washed out of A are deposited in B.', 'Step 2: C is weathered parent material.'], 'B = "below-the-topsoil, builds up".', [('Which horizon is dark with humus?', 'The A horizon.')])
b.S(48, 'How long does it take to form a 10 cm layer of soil, using 120–400 years per cm?', '1 200 to 4 000 years',
    ['Step 1: 10 × 120 = 1 200 years.', 'Step 2: 10 × 400 = 4 000 years.'], 'Multiply both ends of the range.', [('And 5 cm?', '600–2 000 years.')])
b.S(52, 'A soil core of 200 cm³ has an oven-dry mass of 280 g. Find its bulk density and porosity (particle density 2.65 g/cm³).', 'BD = 1.4 g/cm³; porosity ≈ 47 %',
    ['Step 1: BD = 280 ÷ 200 = 1.4 g/cm³.', 'Step 2: Porosity = 1 − 1.4/2.65 = 1 − 0.528 = 0.472.', 'Step 3: ≈ 47 %.'], 'Porosity = 1 − BD/PD.', [('BD 1.06 g/cm³, PD 2.65 g/cm³: porosity?', '60 %.')])
b.M(52, 'A rise in bulk density from 1.2 to 1.7 g/cm³ in a field most likely shows', ['more organic matter', 'compaction', 'better aggregation', 'higher porosity'], 'B',
    ['Step 1: Higher BD = more mass per volume = fewer pores.', 'Step 2: Fewer pores = compacted soil.'], 'High BD → low porosity → compaction.', [('Name two causes of compaction.', 'Heavy machines and trampling by animals (also ploughing at the same depth).')])
b.M(55, 'Particles with a diameter of 0.01 mm are', ['sand', 'silt', 'clay', 'gravel'], 'B',
    ['Step 1: Silt is 0.002–0.05 mm.', 'Step 2: 0.01 mm lies inside that range.'], 'Sand > 0.05 > silt > 0.002 > clay.', [('Is 0.001 mm sand, silt or clay?', 'Clay.')])
b.S(56, 'Use the texture triangle: a soil has 40 % sand, 40 % silt and 20 % clay. What class is it?', 'Loam',
    ['Step 1: Clay 20 % is in the 7–27 % band of loam.', 'Step 2: Silt 40 % is between 28 and 50 %.', 'Step 3: Sand 40 % is ≤ 52 %. → Loam.'], 'Two lines are enough; the third checks.', [('20 % sand, 20 % silt, 60 % clay?', 'Clay.')])
b.S(56, 'A soil has 10 % sand and 25 % clay. What is its silt content, and what is its class?', 'Silt = 65 %; silt loam',
    ['Step 1: Silt = 100 − 10 − 25 = 65 %.', 'Step 2: Silt ≥ 50 % and clay 12–27 % → silt loam.'], 'The three always add to 100.', [('70 % sand, 20 % silt — clay?', '10 %; sandy loam.')])
b.M(56, 'Which cation disperses soil aggregates and causes crusting?', ['Ca²⁺', 'Mg²⁺', 'Na⁺', 'Al³⁺'], 'C',
    ['Step 1: Ca, Mg, Fe and Al bind (flocculate) aggregates.', 'Step 2: Sodium disperses them.'], 'Sodium = soap: it spreads clay apart.', [('What is added to replace sodium?', 'Gypsum (calcium sulphate).')])
b.M(57, 'The best structure for a seedbed is', ['platy', 'granular / crumb', 'columnar', 'single grain'], 'B',
    ['Step 1: Crumb and granular peds are porous and rounded.', 'Step 2: They let air, water and roots in; found in humus-rich topsoil.'], 'Crumb like bread crumbs — soft and airy.', [('Where is columnar structure found?', 'In the B horizon of sodic (natric) arid soils.')])
b.M(58, 'A clay soil should be ploughed when it is', ['dry and hard', 'wet and sticky', 'moist and friable', 'flooded'], 'C',
    ['Step 1: Dry clay is hard; wet clay smears and sticks.', 'Step 2: Moist and friable crumbles well.'], 'Friable = crumbly.', [('Name the three wet-state consistency words.', 'Sticky and plastic.')])
b.S(59, 'Define field capacity and permanent wilting point; how do you calculate available water?', 'Field capacity: water held after gravitational water has drained (1–3 days after soaking). Wilting point: soil so dry that roots cannot take water and plants wilt permanently. Available water = FC − PWP.',
    ['Step 1: Saturation → drain → field capacity.', 'Step 2: Plants use water → wilting point.', 'Step 3: The water between is available.'], 'Draw the bar: gravitational | available | unavailable.', [('A soil holds 32 % at FC and 14 % at PWP. Available water?', '18 %.')])
b.S(60, 'A wet sample weighs 50 g; after oven drying it weighs 42 g. Find the water content by the textbook formula.', '16 %',
    ['Step 1: Water = 50 − 42 = 8 g.', 'Step 2: (8 ÷ 50) × 100 = 16 %.', 'Step 3: (On a dry basis: 8 ÷ 42 × 100 ≈ 19 %.)'], 'Textbook divides by W1 (wet mass).', [('W1 = 60 g, W2 = 45 g?', '25 % (wet basis).')])
b.M(61, 'Which type of water movement is most important for drought-resistant plants in very dry soil?', ['Saturated flow', 'Unsaturated flow', 'Vapour movement', 'Runoff'], 'C',
    ['Step 1: In very dry soil liquid films break.', 'Step 2: Water still moves as vapour.'], 'Dry soil → vapour.', [('Which flow is typical of groundwater?', 'Saturated flow.')])
b.M(62, 'Compared with the atmosphere, soil air usually has', ['less CO₂ and more O₂', 'more CO₂ and less O₂', 'the same composition', 'no water vapour'], 'B',
    ['Step 1: Roots and microbes use O₂ and release CO₂.', 'Step 2: Exchange with the air is slow, so CO₂ builds up (5–10 times).'], 'Respiration underground.', [('Minimum O₂ in soil air for most plants?', 'Above 10 %.')])
b.M(63, 'A grey subsoil colour usually indicates', ['high organic matter', 'good drainage', 'poor drainage (iron depletion)', 'salt accumulation'], 'C',
    ['Step 1: Grey = iron removed under waterlogged conditions.', 'Step 2: Red-brown = well drained; white = salts; black = humus.'], 'Grey = "gley" = wet.', [('What does a whitish surface crust show?', 'Salts — common in arid areas.')])
b.S(65, 'Soil A has pH 5 and soil B has pH 7. How many times more H⁺ does soil A have?', '100 times',
    ['Step 1: Each pH unit = 10 times.', 'Step 2: Difference = 2 units → 10 × 10 = 100.'], 'pH is a log scale.', [('pH 4 vs pH 7?', '1000 times.')])
b.M(67, 'A soil has EC 6 dS/m, ESP 8 % and pH 8.0. It is', ['saline', 'sodic', 'saline-sodic', 'normal'], 'A',
    ['Step 1: EC > 4 → saline.', 'Step 2: ESP < 15 → not sodic.', 'Step 3: So saline.'], 'Check EC first, then ESP.', [('EC 2, ESP 22, pH 9.2?', 'Sodic.')])
b.S(67, 'How is a sodic soil reclaimed? Explain the chemistry in one line.', 'Apply gypsum (CaSO₄) to the surface and leach; Ca²⁺ replaces exchangeable Na⁺ on the colloids, and the sodium is washed out; then grow grass or forage to rebuild structure.',
    ['Step 1: The problem is Na⁺ on the exchange sites.', 'Step 2: Ca²⁺ from gypsum exchanges with it.', 'Step 3: Leaching removes the released Na⁺.'], 'Gypsum for sodium.', [('How is a saline (non-sodic) soil reclaimed?', 'Leach the salts with good-quality water and drain.')])
b.S(66, 'What is "physiological drought"?', 'Salt in the soil solution lowers its osmotic potential, so roots cannot take up water and the plant suffers drought even though the soil contains enough water.',
    ['Step 1: Water moves from high to low water potential.', 'Step 2: Salty soil water has a low potential.', 'Step 3: Roots struggle to pull water in.'], 'Wet soil, thirsty plant.', [('Name the other two effects of salinity.', 'Direct toxicity (Na, Cl, B) and ionic imbalance.')])
b.M(69, 'Rhizobium bacteria are important because they', ['cause root rot', 'fix atmospheric nitrogen in legume nodules', 'decompose lignin', 'make soil acid'], 'B',
    ['Step 1: Rhizobium lives in root nodules of beans, peas, chickpea, grass pea, alfalfa.', 'Step 2: It turns N₂ into forms the plant can use.'], 'Rhizo = root.', [('Which organisms break down cellulose and chitin even at high pH?', 'Actinomycetes.')])
b.S(70, 'List four benefits of humus.', 'Supplies N, P and S; raises CEC (holds cations); holds a lot of water; binds particles into aggregates (better structure, infiltration and resistance to erosion).',
    ['Step 1: Nutrients.', 'Step 2: Exchange capacity.', 'Step 3: Water.', 'Step 4: Structure.'], 'N-C-W-S: nutrients, CEC, water, structure.', [('What are green manure crops?', 'Crops grown and ploughed in to add organic matter.')])
b.M(72, 'A clay soil that cracks widely when dry and swells when wet is a', ['Lithosol', 'Vertisol', 'Arenosol', 'Fluvisol'], 'B',
    ['Step 1: Vertisols have swelling clays.', 'Step 2: Arenosol = sandy; Fluvisol = river deposits; Lithosol = shallow.'], 'Vert- = turn: the soil turns over as it cracks.', [('Which soil group is dominated by salt accumulation?', 'Solonchak.')])

c = QSet('2.3–2.5 Practice — biodiversity, water and zones', 's23')
c.M(77, 'Conserving seeds in a gene bank is', ['in-situ conservation', 'ex-situ conservation', 'land reclamation', 'agroforestry'], 'B',
    ['Step 1: Ex-situ = outside the natural place.', 'Step 2: In-situ = on farm or in enclosures.'], 'Ex = out.', [('Farmers keeping their own landraces is…', 'In-situ conservation.')])
c.M(77, 'Which crops were domesticated in the Abyssinian centre of diversity?', ['Maize and potato', 'Teff and Niger seed', 'Rice and cassava', 'Sugar cane and cotton'], 'B',
    ['Step 1: The textbook names taff (teff) and Niger seed (nihug).', 'Step 2: Maize and potato came from the Americas.'], 'Teff + nihug = home-grown.', [('Name two other crops very diverse in this centre.', 'Barley and chickpea (also wheat, linseed, lentil, faba bean).')])
c.M(78, 'Which goat breed is known for milk and frequent twins and triplets?', ['Afar', 'Worre', 'Hassani (Shukria)', 'Barka'], 'C',
    ['Step 1: Page 78: Hassani — milk, twins and triplets.'], 'Hassani = "has many".', [('Name the two donkey types.', 'Lowland (Rifai) and highland.')])
c.M(82, 'In Table 2.11 the lion is listed as', ['common', 'rare', 'endangered', 'critical'], 'D',
    ['Step 1: Critical: African wild dog and lion.', 'Step 2: Rare: elephant, wild ass; endangered: hartebeest, red-fronted gazelle, Nubian ibex.'], 'Learn two examples per category.', [('Which status does the Nubian ibex have?', 'Endangered.')])
c.S(80, 'Give three reasons for the loss of crop landraces in Eritrea.', 'Drought (tall, late landraces disappeared), changes in agricultural practices (one crop replaced by another), and land degradation (loss of fertility).',
    ['Step 1: Climate: drought.', 'Step 2: Farmers\' choices: crop replacement.', 'Step 3: Land: degradation.'], 'Drought, choice, degradation.', [('Give two factors threatening livestock biodiversity.', 'Uncontrolled interbreeding and drought (also changing distribution).')])
c.M(86, 'Groundwater along the coast becomes more saline with', ['distance from the sea', 'closeness to river channels', 'greater well depth', 'higher altitude'], 'C',
    ['Step 1: Salinity rises with depth, distance from river channels, and closeness to the sea.'], 'Deep, far from river, near sea = salty.', [('Where are Eritrea\'s main aquifers?', 'In loose alluvial deposits of riverbeds (Barka, Gash, Anseba).')])
c.M(88, 'The only perennial river basin is the', ['Barka-Anseba', 'Mereb-Gash', 'Setit', 'Danakil'], 'C',
    ['Step 1: All the others are ephemeral.', 'Step 2: Setit rises in Ethiopia and flows all year.'], 'Setit = steady.', [('Which basin is the largest?', 'The Red Sea basin (44 690 km²).')])
c.S(88, 'The Setit runs at 900 m³/s in flood and 5 m³/s at base flow. How many times larger is the flood flow?', '180 times',
    ['Step 1: 900 ÷ 5 = 180.'], 'Ratio = big ÷ small.', [('With a base flow of 10 m³/s?', '90 times.')])
c.M(93, 'Which zone has the highest rainfall?', ['Moist highland', 'Sub-humid escarpment', 'Moist lowland', 'Arid highland'], 'B',
    ['Step 1: Sub-humid 700–1100 mm.', 'Step 2: Moist lowland 500–800; moist highland 500–700.'], 'Escarpment catches sea air.', [('Which zone is largest?', 'Semi-desert (39 %).')])
c.M(93, 'The dominant crop of the moist highland is', ['sorghum', 'barley', 'cotton', 'coffee'], 'B',
    ['Step 1: Moist highland: barley 0.5–2 t/ha, the dominant crop.', 'Step 2: Sorghum dominates the moist lowland.'], 'Highland = barley; lowland = sorghum.', [('Which crop is grown on the sub-humid escarpment but nowhere else on the list?', 'Coffee.')])
c.S(95, 'Eritrea\'s land area is about 125 700 km². Using 7 % cultivated, estimate the cultivated area.', 'About 8 800 km² (Table 2.14 gives 8 712 km²)',
    ['Step 1: 0.07 × 125 700 = 8 799 km².', 'Step 2: Close to the table value 8 712 km² (6.8 %).'], 'Percent of a total.', [('Barren land is 14.4 %; how many km²?', 'About 18 100 km² (table: 18 265).')])
c.S(94, 'Why is the potential of the sub-humid escarpment "moderate to high" yet limited?', 'Rainfall (700–1100 mm) and long growing periods favour crops, but steep slopes and shallow soils limit cultivation and cause erosion.',
    ['Step 1: Good: most rain, mild temperatures.', 'Step 2: Limits: steep land (8–100 % slope), shallow soil.'], 'Climate yes, land no.', [('Name two crops of that zone.', 'Maize and coffee (also sorghum, barley).')])
c.TF(96, 'True or false: in the traditional highland system, fertile land could be allocated for houses.', 'False',
    ['Step 1: Fertile land is the village breadbasket.', 'Step 2: It is never used for settlement.'], 'Breadbasket stays farmland.', [('Into what three classes is highland farmland graded?', 'Fertile, medium and poor.')])

QS = a.items + b.items + c.items

GLOSSARY = [
    ('Isotherm', 'A line on a map joining places with the same mean temperature.', 40),
    ('Potential evapotranspiration (PET)', 'The water that would evaporate and transpire if water were always available.', 41),
    ('Edaphology', 'The study of soil in relation to plant growth.', 46),
    ('Illuviation', 'The washing-in and accumulation of clay, iron, aluminium or humus in the B horizon.', 49),
    ('Solum', 'The upper, biologically weathered part of the regolith (O, A and B horizons).', 50),
    ('Porosity', 'The fraction of soil volume that is pore space: 1 − bulk density ÷ particle density.', 53),
    ('Field capacity', 'The water a soil holds after gravitational water has drained away.', 59),
    ('Permanent wilting point', 'Soil water content at which plants wilt and do not recover.', 59),
    ('Physiological drought', 'Water stress caused by salt in the soil, even when the soil is moist.', 66),
    ('Landrace', 'A local crop variety selected by farmers over generations.', 77),
    ('Aquifer', 'An underground layer of rock or sediment that stores and transmits water.', 86),
    ('Ephemeral river', 'A river that flows only for part of the year.', 88),
    ('Agro-ecological zone', 'An area with similar climate, landform, soil and vegetation, and so similar farming potential.', 91),
]
TIPS = [('Table 2.1: temperature falls 5–7 °C and PET about 200 mm for every 1000 m of altitude.', 41),
        ('Saline: EC > 4; sodic: ESP > 15 and pH > 8.5. Water for salt, gypsum for sodium.', 67),
        ('AEZ sizes: semi-desert 39, arid lowland 34, moist lowland 16, moist highland 7, arid highland 3, sub-humid 1.', 95)]
IDEAS = [('tri', 'Texture triangle', 'l2_2', 'agri11-u2-ad-tri-st'), ('avail', 'Available water = FC − PWP', 'l2_2', 'agri11-u2-ad-fcwp'),
         ('aez6', 'Six agro-ecological zones', 'l2_5', 'agri11-u2-ad-aez-fig')]

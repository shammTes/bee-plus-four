r"""Grade 12 Unit 3 — Soil and Water Conservation (pp. 158-208): importance, land degradation, erosion, SWC measures,
surveying, terraces and check dams, agronomic measures, water harvesting, irrigation and drainage."""
from common import set_unit, T, RM, MN, TB, DG, ST, WK, QSet
from svglib import Fig, INK, BLUE, RED, GREEN, PURPLE, ORANGE, GREY, FILL
from agrilib import (box, tlines, wrap, flow, hflow, cycle, leader, ground, grass_tufts, sorghum, person, cloud, sun, tree,
                     BROWN, SOIL, SOIL2, SOIL3, LEAF, LEAF2, STRAW, WATER, ROCK, SKY)

UID = 'agri12-u3'
set_unit(UID)
STONE = '#B8B0A4'


def fl(c):
    return FILL.get(c, '#F3E9DC')


# ------------------------------------------------------------------ figures
def f_soilloss():
    f = Fig(340, 214)
    f.title('Soil loss by water erosion (t/ha per year)', 12.5)
    rows = [('Highlands (estimate)', 75, '50–100', RED), ('Highlands (measured mean)', 42, '42', RED), ('Moist lowlands', 47, '47', ORANGE),
            ('Eastern escarpment', 37, '37', ORANGE), ('Croplands (net, national)', 12, '12', BROWN), ('Dry lowlands', 6, '6', GREEN)]
    for i, (nm, v, lab, c) in enumerate(rows):
        y = 30 + i * 28
        f.text(150, y + 14, nm, 10.5, INK, 'end')
        f.rect(156, y + 2, v * 1.8, 18, c, 1.2, fl(c), 3)
        f.text(160 + v * 1.8, y + 15, lab, 10.5, INK, 'start', False)
    f.text(170, 208, '42 t/ha ≈ 3–4 mm of topsoil a year', 10.5, GREY, 'middle', False)
    return f


def f_components():
    f = Fig(340, 190)
    box(f, 100, 6, 140, 30, 'Land degradation', RED, 12.5)
    items = [('Soil', 'erosion; physical, chemical, biological decline', BROWN), ('Vegetation', 'less biomass and ground cover', GREEN),
             ('Biodiversity', 'fewer genes, species, ecosystems', PURPLE), ('Water', 'less, dirtier water; downstream floods', BLUE)]
    for i, (a, b, c) in enumerate(items):
        x = 6 + i * 83
        box(f, x, 70, 78, 30, a, c, 11.5)
        f.line(170, 36, x + 39, 69, GREY, 1.1)
        tlines(f, x + 39, 132, wrap(b, 15), 10, INK, 'middle', False)
    f.text(170, 184, 'Immediate causes: over-cultivation, overgrazing, deforestation', 10.5, RED, 'middle', False)
    return f


def f_soildeg():
    f = Fig(340, 230)
    box(f, 90, 6, 160, 28, 'Soil degradation', BROWN, 12.5)
    cols = [('Physical', ['erosion (water, wind)', 'compaction, hard pans', 'crusting, poor structure'], ORANGE),
            ('Chemical', ['nutrient + organic matter loss', 'salinisation', 'nutrients fixed (alkaline)', 'laterisation'], BLUE),
            ('Biological', ['organic matter < 1 %', 'fewer soil fauna', 'less microbial life'], GREEN)]
    for i, (a, items, c) in enumerate(cols):
        x = 6 + i * 112
        box(f, x, 54, 104, 28, a, c, 12)
        f.line(170, 34, x + 52, 53, GREY, 1.1)
        for j, t in enumerate(items):
            tlines(f, x + 52, 104 + j * 30, wrap(t, 17), 10, INK, 'middle', False)
    return f


def f_causes():
    f = Fig(340, 236)
    f.rect(6, 6, 160, 224, ORANGE, 1.6, fl(ORANGE), 8)
    f.rect(174, 6, 160, 224, RED, 1.6, fl(RED), 8)
    f.text(86, 26, 'NATURAL', 12.5, ORANGE).text(254, 26, 'HUMAN-MADE', 12.5, RED)
    left = ['intense, erratic rain', 'steep slopes', 'erodible sandy / silty soils', 'drought, strong wind', 'shallow soils']
    right = ['over-cultivation, no fallow', 'overgrazing', 'deforestation', 'dung + residues burnt as fuel', 'ploughing up and down slope',
             'poverty, insecure tenure']
    for i, t in enumerate(left):
        f.text(86, 56 + i * 30, t, 10.5, INK, 'middle', False)
    for i, t in enumerate(right):
        f.text(254, 56 + i * 30, t, 10.5, INK, 'middle', False)
    return f


def f_erosion():
    f = Fig(340, 270)
    f.title('Four stages of water erosion', 13)
    for i, (nm, d) in enumerate([('Splash', 'raindrops knock soil loose'), ('Sheet', 'thin even layer washed off'),
                                 ('Rill', 'small channels; ploughing removes'), ('Gully', 'deep channels; plough cannot cross')]):
        x0 = 6 + (i % 2) * 168
        y0 = 30 + (i // 2) * 120
        f.rect(x0, y0, 160, 112, GREY, 1, '#F7FAFD', 6)
        f.text(x0 + 80, y0 + 16, nm, 12, BLUE)
        f.text(x0 + 80, y0 + 106, d, 9.5, INK, 'middle', False)
        f.path(f'M{x0 + 8} {y0 + 54} L{x0 + 152} {y0 + 78} L{x0 + 152} {y0 + 94} L{x0 + 8} {y0 + 94} Z', '#7A4E2D', 1, SOIL)
        if i == 0:
            for k in range(4):
                xx = x0 + 30 + k * 30
                yy = y0 + 58 + k * 5
                f.line(xx, yy - 26, xx, yy - 8, WATER, 2)
                for d_ in (-6, 6):
                    f.circle(xx + d_, yy - 6, 2, None, 0, SOIL3)
        elif i == 1:
            f.path(f'M{x0 + 8} {y0 + 52} L{x0 + 152} {y0 + 76}', WATER, 4, op=0.8)
            f.arrow(x0 + 100, y0 + 62, x0 + 140, y0 + 69, BLUE, 1.6, 6)
        elif i == 2:
            for k in range(3):
                xx = x0 + 40 + k * 40
                yy = y0 + 54 + (xx - x0 - 8) * 24 / 144
                f.path(f'M{xx - 4} {yy} L{xx} {yy + 6} L{xx + 4} {yy}', '#5A3A1E', 1.6, WATER)
        else:
            xx = x0 + 80
            yy = y0 + 54 + 72 * 24 / 144
            f.path(f'M{xx - 22} {yy} L{xx - 8} {yy + 26} L{xx + 8} {yy + 26} L{xx + 22} {yy + 2}', '#5A3A1E', 1.6, '#E8D6B8')
            f.path(f'M{xx - 8} {yy + 24} L{xx + 8} {yy + 24}', WATER, 3)
    return f


def f_wind():
    f = Fig(340, 180)
    f.title('Wind erosion: deflation and abrasion', 12.5)
    ground(f, 140, 0, 340, '#D9B98A', 40)
    for k in range(4):
        f.arrow(10, 50 + k * 18, 70, 50 + k * 18, BLUE, 1.6, 6)
    f.text(14, 42, 'wind', 11, BLUE, 'start')
    for k in range(9):
        x = 90 + k * 22
        f.path(f'M{x} 140 Q{x + 11} {104 - (k % 3) * 8} {x + 22} 140', ORANGE, 1, dash=True)
        f.circle(x + 11, 120 - (k % 3) * 4, 2.2, None, 0, SOIL3)
    f.text(170, 82, 'fine dust lifted and carried away (deflation)', 10.5, INK, 'middle', False)
    f.rect(296, 96, 30, 44, '#6E6A64', 1.2, STONE, 4)
    f.text(311, 88, 'abrasion', 10.5, RED)
    f.text(170, 166, 'Worst on the coast and north-western lowlands', 10.5, '#FFFFFF')
    return f


def f_dung():
    return hflow(['273 000 t of dung burned a year', '× 1.4 % N = 3 800 t N lost', '× 1.3 % P = 3 500 t P lost', 'Soils grow poorer'],
                 340, bh=58, size=10.5, rows=2, title='Dung as fuel: nutrients up in smoke')


def f_landscape():
    f = Fig(340, 260)
    f.title('Which measure goes where', 13)
    f.path('M0 70 L120 70 L200 150 L260 170 L300 210 L340 214 L340 260 L0 260 Z', '#7A4E2D', 1.2, SOIL)
    for k in range(4):
        x = 128 + k * 18
        y = 78 + k * 18
        f.path(f'M{x - 6} {y} L{x + 6} {y} L{x + 6} {y + 5}', '#5A3A1E', 2)
        tree(f, x, y, 14, LEAF2)
    f.text(8, 40, 'Hillside: enclosure, afforestation,', 10.5, GREEN, 'start').text(8, 53, 'terraces, micro-basins', 10.5, GREEN, 'start')
    for k in range(3):
        x = 206 + k * 18
        f.rect(x, 150 + k * 8, 10, 6, '#6E6A64', 0.8, STONE)
    for x in (214, 232, 250):
        f.line(x, 158 + (x - 214) / 3, x, 140 + (x - 214) / 3, LEAF, 1.6)
    f.text(334, 96, 'Cropland: stone bunds, grass', 10.5, ORANGE, 'end').text(334, 109, 'strips, mulch, rotation', 10.5, ORANGE, 'end')
    f.path('M290 210 C300 214 312 214 322 212', WATER, 6)
    f.rect(280, 196, 12, 10, '#6E6A64', 0.8, STONE).rect(280, 186, 12, 10, '#6E6A64', 0.8, STONE)
    f.text(250, 246, 'Riverbank: gabions + planting', 10.5, '#FFFFFF')
    f.text(70, 200, 'Gullies: check dams', 10.5, '#FFFFFF')
    return f


def f_slope():
    f = Fig(340, 220)
    f.title('Measuring slope', 13)
    A, B, C = (30, 170), (290, 170), (290, 70)
    f.poly([A, B, C], INK, 2, '#F3E9DC')
    f.right(B, A, C, 10)
    f.text(160, 188, 'HI = horizontal interval = 50 m', 11, BLUE)
    f.text(284, 124, 'VI = 10 m', 11, RED, 'end')
    f.angle(A, B, C, 40, ORANGE, 'θ')
    tlines(f, 110, 92, ['% slope = VI ÷ HI × 100', '= 10 ÷ 50 × 100 = 20 %', 'ratio 1 : 5,  θ ≈ 11.3°'], 11, INK, 'middle')
    f.text(170, 212, '0–8 % gentle · 8–30 % hilly · > 30 % steep', 10.5, GREY, 'middle', False)
    return f


def f_linelevel():
    f = Fig(340, 200)
    f.title('Line level: marking a contour', 12.5)
    f.path('M0 170 L340 140 L340 200 L0 200 Z', '#7A4E2D', 1, SOIL)
    xa, xb = 50, 290
    ya, yb = 170 - 50 * 30 / 340, 170 - 290 * 30 / 340
    for x, y in ((xa, ya), (xb, yb)):
        f.rect(x - 3, y - 90, 6, 90, '#6B4A2B', 1, STRAW)
        for k in range(10):
            f.line(x - 3, y - 12 - k * 7, x + 3, y - 12 - k * 7, '#6B4A2B', 0.8)
    yz = ya - 70
    f.line(xa, yz, xb, yz, INK, 1.4)
    f.rect(160, yz - 5, 20, 10, BLUE, 1.2, '#DCEBF7', 4)
    f.circle(170, yz, 2.4, None, 0, GREEN)
    f.text(170, yz - 12, 'spirit level, bubble centred', 10, BLUE)
    f.line(xa, 186, xb, 186, GREY, 1).text(170, 196, '10 m between sticks (string 10.5 m)', 10, '#FFFFFF', 'middle', False)
    f.text(xb + 6, yb - 92, '1.5 m', 10, GREY, 'start', False)
    f.text(xb - 8, yb - 30, 'slide the string', 10, ORANGE, 'end', False).text(xb - 8, yb - 18, 'until level', 10, ORANGE, 'end', False)
    return f


def f_tubelevel():
    f = Fig(340, 200)
    f.title('Flexible-tube (water) level', 12.5)
    f.path('M0 180 L340 150 L340 200 L0 200 Z', '#7A4E2D', 1, SOIL)
    xa, xb = 60, 280
    ya, yb = 180 - 60 * 30 / 340, 180 - 280 * 30 / 340
    wl = 72
    for x, y in ((xa, ya), (xb, yb)):
        f.rect(x - 4, y - 120, 8, 120, '#6B4A2B', 1, STRAW)
        f.rect(x + 5, wl, 5, y - wl, '#3F7FBF', 0.8, '#9CC3E6')
    f.path(f'M{xa + 7} {ya} C{xa + 40} {ya + 14} {xb - 40} {yb + 24} {xb + 7} {yb}', '#3F7FBF', 3)
    f.line(30, wl, 310, wl, RED, 1.2, dash=True)
    f.text(170, wl + 18, 'water stands at the same height', 10.5, RED).text(170, wl + 32, 'in both ends', 10.5, RED)
    f.text(170, 120, 'poles 2 m; water 1–1.5 m up;', 10, INK, 'middle', False).text(170, 133, 'tap out air bubbles', 10, INK, 'middle', False)
    return f


def f_contour():
    f = Fig(340, 220)
    f.title('Contours on a hill and terraces along them', 12)
    cx, cy = 110, 120
    for k, r in enumerate((80, 60, 40, 20)):
        f.ellipse(cx, cy, r * 1.15, r * 0.9, BROWN, 1.4)
        if k < 3:
            f.text(cx, cy - r * 0.9 + 11, f'{1900 + k * 20} m', 9, GREY, 'middle', False)
    f.text(cx, cy + 4, 'top', 10, INK)
    f.text(cx, 214, 'close lines = steep; wide = gentle', 10, GREY, 'middle', False)
    for y in (60, 100, 140):
        f.path(f'M210 {y} C240 {y - 6} 300 {y - 6} 330 {y}', GREEN, 3)
    f.text(270, 172, 'terraces follow contours,', 10.5, GREEN).text(270, 184, 'so water stays level', 10.5, GREEN)
    for y in (70, 110):
        f.arrow(270, y, 270, y + 18, BLUE, 1.4, 5)
    return f


def f_terraces():
    f = Fig(340, 300)
    f.title('Cross-sections of physical measures', 12.5)
    f.text(10, 40, 'Bench terrace (steps)', 11.5, BROWN, 'start')
    d = 'M10 120 L60 120 L60 100 L120 100 L120 80 L180 80 L180 60 L240 60 L240 46'
    f.path(d + ' L240 130 L10 130 Z', '#7A4E2D', 1, SOIL)
    f.path('M10 140 L240 40', GREY, 1, dash=True).text(250, 70, 'original slope', 9.5, GREY, 'start', False)
    for x in (30, 90, 150, 210):
        sorghum(f, x, 120 - (x - 30) / 3, 14)
    f.text(10, 166, 'Hillside terrace / stone bund', 11.5, BROWN, 'start')
    f.path('M10 280 L330 190 L330 290 L10 290 Z', '#7A4E2D', 1, SOIL)
    for x in (90, 190, 290):
        y = 280 - (x - 10) * 90 / 320
        for j in range(3):
            f.rect(x + j * 2, y - 10 - j * 7, 12, 7, '#6E6A64', 0.8, STONE)
        f.path(f'M{x - 26} {y + 6} L{x - 4} {y + 10} L{x} {y}', '#5A3A1E', 1.4, '#C9A27E')
        f.path(f'M{x - 22} {y + 6} L{x - 4} {y + 9}', WATER, 2)
    f.text(200, 286, 'stones on the lower side; water collects in the ditch above', 9.5, '#FFFFFF', 'middle', False)
    return f


def f_checkdam():
    f = Fig(340, 220)
    f.title('Check dam across a gully', 12.5)
    f.path('M20 60 L100 60 L130 190 L210 190 L240 60 L320 60 L320 210 L20 210 Z', '#7A4E2D', 1.2, SOIL)
    f.path('M100 60 L130 190 L210 190 L240 60 Z', None, 0, '#F7FAFD')
    for r in range(5):
        y = 180 - r * 16
        w = 80 + r * 26
        for k in range(int(w // 18)):
            f.rect(170 - w / 2 + k * 18, y, 17, 14, '#6E6A64', 0.8, STONE)
    f.rect(146, 108, 48, 10, None, 0, '#F7FAFD')
    f.path('M146 108 L146 118 L194 118 L194 108', '#5A3A1E', 1.4)
    f.text(170, 100, 'spillway (lower centre)', 10.5, BLUE)
    f.text(170, 206, 'sediment fills behind it → gully heals', 10.5, '#FFFFFF')
    f.text(278, 50, 'keyed into the banks', 10.5, BROWN)
    f.arrow(270, 54, 238, 96, GREY, 1.2, 5)
    return f


def f_microbasin():
    f = Fig(340, 190)
    f.title('Micro-basins on a hillside (plan view)', 12.5)
    for r in range(3):
        for c in range(4):
            x = 50 + c * 80 + (40 if r % 2 else 0)
            y = 50 + r * 46
            if x > 320:
                continue
            f.path(f'M{x - 26} {y - 6} C{x - 24} {y + 22} {x + 24} {y + 22} {x + 26} {y - 6}', BROWN, 3)
            f.circle(x, y + 4, 4, None, 0, LEAF)
    f.arrow(14, 40, 14, 170, BLUE, 1.6, 6)
    f.text(22, 180, 'downhill', 10, BLUE, 'start')
    f.text(200, 186, 'staggered so runoff missed by one is caught by the next', 9.5, GREY, 'middle', False)
    return f


def f_agronomic():
    f = Fig(340, 240)
    f.title('Agronomic (biological) measures on cropland', 12)
    items = [('Mulch', 'straw on the surface: less splash and evaporation'), ('Cover crop', 'legume covers bare soil'),
             ('Contour strips', 'grass strip, then crop, along contour'), ('Trash lines', 'crop residue lines on the contour'),
             ('Rotation / intercropping', 'cover and fertility'), ('Manure + fertiliser', 'more organic matter and growth')]
    for i, (a, b) in enumerate(items):
        x = 6 + (i % 2) * 168
        y = 30 + (i // 2) * 70
        f.rect(x, y, 160, 62, GREEN, 1.2, fl(GREEN), 6)
        f.text(x + 80, y + 18, a, 11.5, GREEN)
        tlines(f, x + 80, y + 38, wrap(b, 28), 10, INK, 'middle', False)
    return f


def f_dam():
    f = Fig(340, 200)
    f.title('Earth dam: cross-section', 12.5)
    f.rect(0, 170, 340, 30, None, 0, SOIL3)
    f.path('M10 170 L10 100 L120 100 L120 170 Z', None, 0, '#9CC3E6')
    f.text(60, 140, 'reservoir', 11, BLUE)
    f.path('M90 170 L160 60 L200 60 L290 170 Z', '#7A4E2D', 1.4, SOIL)
    f.path('M160 170 L172 60 L188 60 L200 170 Z', '#4A3A2A', 1, '#6E5A48')
    f.text(336, 44, 'impervious clay core', 10.5, INK, 'end')
    f.arrow(250, 50, 190, 90, GREY, 1.2, 5)
    f.text(336, 120, 'earth embankment', 10.5, INK, 'end')
    f.text(170, 190, 'spillway at the side carries floods safely', 10, '#FFFFFF')
    return f


def f_roof():
    f = Fig(340, 220)
    f.title('Roof water-harvesting', 13)
    f.poly([(40, 90), (150, 50), (150, 60), (40, 100)], '#555', 1.2, '#B9C2CC')
    f.rect(50, 100, 100, 80, '#7A6A58', 1.2, '#EFE6D6')
    f.rect(88, 140, 22, 40, '#6B4A2B', 1, '#A07A55')
    f.line(36, 104, 36, 150, '#555', 3).line(36, 150, 196, 150, '#555', 3)
    f.rect(196, 120, 90, 60, '#5A5A5A', 1.4, '#C9C9C9', 6)
    f.rect(200, 140, 82, 36, None, 0, '#9CC3E6')
    f.text(241, 112, 'concrete cistern', 10.5, INK)
    cloud(f, 100, 26, 0.7, rain=True)
    f.text(170, 202, 'Water = roof area × rainfall × 0.8 (losses)', 11, GREEN)
    f.text(170, 216, '60 m² × 0.5 m × 0.8 = 24 m³ = 24 000 L a year', 10.5, INK, 'middle', False)
    return f


def f_spate():
    f = Fig(340, 220)
    f.title('Spate irrigation (eastern lowlands)', 12)
    f.path('M0 30 L80 30 L60 80 L0 90 Z', '#7A6A58', 1, '#C8B79E')
    f.text(32, 54, 'highlands', 10, INK)
    f.path('M60 70 C120 90 160 110 180 140 C200 170 240 190 340 196', '#8A6A4A', 14)
    f.path('M60 70 C120 90 160 110 180 140 C200 170 240 190 340 196', WATER, 6)
    f.text(330, 168, 'seasonal river in flood', 10, BLUE, 'end')
    f.path('M150 104 L190 92', '#6E6A64', 6)
    f.text(150, 124, 'diversion bund', 10.5, BROWN, 'end')
    f.path('M170 98 C210 80 250 70 300 66', WATER, 3)
    for k in range(3):
        x = 220 + k * 34
        f.rect(x, 34, 30, 26, BROWN, 1.2, '#E9DDB6', 2)
        f.line(x + 15, 60, x + 15, 70 - k * 2, WATER, 2)
    f.text(330, 92, 'bunded fields flooded', 10.5, GREEN, 'end')
    f.text(170, 214, 'Flood water from highland rains, diverted to fields', 10, GREY, 'middle', False)
    return f


def f_subdam():
    f = Fig(340, 200)
    f.title('Sub-surface dam and well in a sandy riverbed', 12)
    f.rect(0, 70, 340, 110, None, 0, '#E8D6A8')
    f.rect(0, 180, 340, 20, None, 0, '#7D6A58')
    f.text(300, 194, 'rock', 10, '#FFFFFF')
    f.rect(0, 110, 230, 70, None, 0, '#B9D6EE')
    f.text(110, 150, 'water stored in the sand', 11, BLUE)
    f.rect(230, 70, 14, 110, '#4A3A2A', 1, '#6E5A48')
    f.text(336, 62, 'clay / masonry wall', 10.5, INK, 'end')
    f.rect(190, 40, 22, 140, '#555', 1.2, None)
    f.text(184, 34, 'well (upstream side)', 10.5, INK, 'end')
    f.arrow(30, 60, 90, 60, BLUE, 1.6, 6).text(34, 52, 'river flow', 10, BLUE, 'start')
    return f


def f_methods():
    f = Fig(340, 270)
    f.title('Irrigation methods and efficiency', 13)
    items = [('Furrow / basin', 'gravity flow; cheap', 45, ORANGE, '40–50 %'), ('Spate', 'diverted floods', 30, BROWN, 'variable'),
             ('Sprinkler', 'spray; water at night', 75, BLUE, '~75 %'), ('Drip', 'drops at the roots', 90, GREEN, 'up to ~90 %')]
    for i, (a, b, e, c, lab) in enumerate(items):
        y = 30 + i * 58
        f.text(10, y + 14, a, 12, c, 'start')
        f.text(10, y + 28, b, 9.5, GREY, 'start', False)
        f.rect(150, y + 4, 180, 22, GREY, 0.8, '#FFFFFF', 4)
        f.rect(150, y + 4, 180 * e / 100, 22, c, 1, fl(c), 4)
        f.text(156, y + 19, lab, 10.5, INK, 'start')
    f.text(170, 262, 'share of the water that reaches the crop', 10.5, GREY, 'middle', False)
    return f


def f_drip():
    f = Fig(340, 200)
    f.title('Simple drip system', 13)
    f.rect(10, 40, 50, 50, '#555', 1.4, '#C9C9C9', 4)
    f.rect(14, 56, 42, 30, None, 0, '#9CC3E6')
    f.text(35, 104, 'raised tank', 10, INK)
    f.text(35, 116, '+ filter', 10, INK)
    f.line(60, 80, 90, 80, '#333', 4).line(90, 50, 90, 180, '#333', 4)
    f.text(96, 44, 'main line', 10, INK, 'start')
    for k in range(4):
        y = 60 + k * 36
        f.line(90, y, 330, y, '#333', 1.8)
        for j in range(6):
            x = 120 + j * 36
            f.circle(x, y, 2.6, None, 0, BLUE)
            f.circle(x, y + 10, 6, LEAF, 1.2, fl(GREEN))
    f.text(250, 196, 'laterals with emitters at each plant', 10, INK, 'middle', False)
    return f


def f_pivot():
    f = Fig(340, 214)
    f.title('Centre-pivot irrigation', 12.5)
    f.circle(170, 112, 80, GREEN, 1.6, fl(GREEN))
    f.circle(170, 112, 4, None, 0, INK)
    f.line(170, 112, 230, 58, '#555', 3)
    for t in (0.3, 0.6, 0.9):
        f.circle(170 + 60 * t, 112 - 54 * t, 3.4, '#333', 1, '#FFF')
    f.text(336, 44, 'pipe on wheeled towers', 10.5, INK, 'end')
    f.text(170, 208, 'turns round the centre; sprinklers along the pipe', 10.5, GREY, 'middle', False)
    return f


def f_drains():
    f = Fig(340, 260)
    f.title('Four kinds of drainage', 13)
    for i, (nm, d) in enumerate([('Surface', 'open ditches; land shaped to slope'), ('Sub-surface', 'buried perforated pipes'),
                                 ('Vertical', 'pump from dug or tube wells'), ('Bio-drainage', 'thirsty trees, e.g. eucalyptus')]):
        x0 = 6 + (i % 2) * 168
        y0 = 28 + (i // 2) * 116
        f.rect(x0, y0, 160, 108, GREY, 1, '#F7FAFD', 6)
        f.text(x0 + 80, y0 + 16, nm, 12, BLUE)
        f.text(x0 + 80, y0 + 102, d, 9.5, INK, 'middle', False)
        f.rect(x0 + 6, y0 + 50, 148, 40, None, 0, SOIL)
        f.rect(x0 + 6, y0 + 74, 148, 16, None, 0, '#9CC3E6')
        if i == 0:
            for xx in (x0 + 40, x0 + 120):
                f.path(f'M{xx - 10} {y0 + 50} L{xx - 4} {y0 + 64} L{xx + 4} {y0 + 64} L{xx + 10} {y0 + 50}', '#5A3A1E', 1.4, '#9CC3E6')
        elif i == 1:
            for xx in (x0 + 40, x0 + 80, x0 + 120):
                f.circle(xx, y0 + 72, 5, '#333', 1.4, '#FFF')
        elif i == 2:
            f.rect(x0 + 74, y0 + 30, 12, 60, '#555', 1.2, '#C9C9C9')
            f.arrow(x0 + 80, y0 + 36, x0 + 80, y0 + 24, BLUE, 1.6, 5)
        else:
            for xx in (x0 + 50, x0 + 110):
                tree(f, xx, y0 + 50, 30, LEAF)
                f.path(f'M{xx} {y0 + 50} L{xx - 6} {y0 + 78} M{xx} {y0 + 50} L{xx + 6} {y0 + 80}', BROWN, 1.4)
    return f


def f_salt():
    f = Fig(340, 226)
    f.title('How irrigated soils become salty', 12.5)
    sun(f, 300, 34, 12)
    ground(f, 100, 0, 340, SOIL, 100)
    for k in range(6):
        x = 30 + k * 50
        f.arrow(x, 160, x, 106, BLUE, 1.4, 5)
        f.arrow(x + 10, 96, x + 10, 60, GREY, 1.2, 5, dash=True)
    f.rect(0, 92, 340, 8, None, 0, '#F2F2F2')
    f.text(170, 86, 'white salt crust left at the surface', 10.5, INK, 'middle')
    f.text(110, 52, 'water evaporates', 10.5, GREY)
    f.text(170, 182, 'salty water rises by capillarity', 10.5, '#FFFFFF')
    f.text(170, 220, 'Cure: leach with extra water + good drainage', 10.5, GREEN)
    return f


DIAGRAMS = {
    'soilloss': (f_soilloss(), 'Rates of soil loss in Eritrea', 173),
    'components': (f_components(), 'Components of land degradation', 162),
    'soildeg': (f_soildeg(), 'Types of soil degradation', 163),
    'causes': (f_causes(), 'Natural and human causes of land degradation', 168),
    'erosion': (f_erosion(), 'Splash, sheet, rill and gully erosion', 171),
    'wind': (f_wind(), 'Wind erosion', 173),
    'dung': (f_dung(), 'Nutrient loss from burning dung', 174),
    'landscape': (f_landscape(), 'SWC measures by site', 177),
    'slope': (f_slope(), 'Horizontal interval, vertical interval and slope', 178),
    'linelevel': (f_linelevel(), 'Line level', 180),
    'tubelevel': (f_tubelevel(), 'Flexible-tube level', 181),
    'contour': (f_contour(), 'Contours and contour terraces', 179),
    'terraces': (f_terraces(), 'Bench terrace, hillside terrace and stone bund', 185),
    'checkdam': (f_checkdam(), 'Check dam', 185),
    'microbasin': (f_microbasin(), 'Micro-basins', 185),
    'agronomic': (f_agronomic(), 'Agronomic SWC measures', 186),
    'dam': (f_dam(), 'Earth dam with impervious core', 191),
    'roof': (f_roof(), 'Roof water-harvesting', 194),
    'spate': (f_spate(), 'Spate irrigation', 199),
    'subdam': (f_subdam(), 'Sub-surface dam with a well', 193),
    'methods': (f_methods(), 'Irrigation methods compared', 198),
    'drip': (f_drip(), 'Drip irrigation layout', 200),
    'pivot': (f_pivot(), 'Centre-pivot irrigation', 201),
    'drains': (f_drains(), 'Surface, sub-surface, vertical and bio-drainage', 204),
    'salt': (f_salt(), 'Salinisation of irrigated soil', 204),
}


# ------------------------------------------------------------------ lessons
L1 = [
    T('=agri12-u3-c01', '3.1.1 What soil and water conservation means', 158,
      '**Soil and water conservation (SWC)** = all the human activities that **keep soil on the land** and **protect and maintain the water supply**: practical farming measures that stop land damage and water waste.',
      'Soil and water go together: a terrace that stops soil washing away also holds the rain so it soaks in. Some measures are mainly for water (ponds, dams), others mainly for soil (bunds, grass strips), but most do both.',
      '**Eritrean examples you can see:** stone bunds and terraces on the hillsides around Asmara and Mendefera, micro-basins with seedlings planted by students in the summer campaign, check dams in gullies, enclosures on steep slopes, ponds and small dams such as **Toker** near Asmara.'),
    T('=agri12-u3-c02', '3.1.2 Why SWC matters so much in Eritrea', 159,
      'Eritrea lies in the **Sudano-Sahelian** belt: rain is **low, erratic** and **badly distributed**; much of the country is too dry for rain-fed farming. Farming has gone on for thousands of years, and local SWC methods (terraces, bunds) are old.',
      '**The size of the problem:**',
      '- On poorly conserved land, soil is lost **20–40 times faster** than it forms.',
      '- Measured water erosion in the **highlands**: **3.4 to 84.5 t/ha a year**, mean **42 t/ha** (about 3–4 mm of topsoil a year, some 20 times the rate of formation). The highlands have the **greatest livestock density** and the worst degradation.',
      '- Erosion can cut yields by **30–90 %** on shallow soils; some Eritrean land has lost **50 %** of its productivity.',
      '- Nutrient depletion: about **22 kg N, 3 kg P and 15 kg K per hectare per year**.',
      '- Average cereal yield in Eritrea is only **0.74 t/ha**, while good soil management elsewhere has raised it from 1 to 5–6 t/ha.',
      '**Benefits of SWC:** more organic matter, so more water held and more infiltration, less runoff; **less silt in dams** (they last longer); ponds and dams allow **irrigation** and high-value crops; restored land can be farmed again; **higher productivity**.'),
    DG('soilloss-fig', 'How fast Eritrea loses soil', 173, 'soilloss',
       'The highlands lose the most: steep slopes, intense storms, many animals and little cover.'),
    WK('wk-mm', 'Turning t/ha into millimetres of soil', 159,
       'Soil loss is 42 t/ha per year and topsoil weighs about 1.3 t per m³. How many mm of soil is lost each year?',
       ['1 ha = 10 000 m², so 42 t/ha = 42 000 kg ÷ 10 000 m² = 4.2 kg per m².', 'Volume = 4.2 kg ÷ 1 300 kg/m³ ≈ 0.0032 m³ per m².',
        'Depth = 0.0032 m ≈ 3.2 mm a year.'],
       'About 3 mm a year (the textbook rounds to 4 mm); 1 cm of topsoil gone in about 3 years.'),
    RM('swc-err', 'Textbook check: bunds and organic matter', 160,
       'The textbook calls terraces and soil bunds "measures used to increase organic matter". They are **physical structures** that slow runoff and trap soil; organic matter is raised by **agronomic** measures such as manure, mulch and crop residues.'),
]

L2 = [
    T('=agri12-u3-c03', '3.2.1 Land degradation and its components', 162,
      '**Land degradation** = a fall in the present or future ability of land to produce goods and services. It is both a **process** (gradual weakening of the land) and a **result**: smaller farms per household, falling crop and livestock yields, lost vegetation, fuelwood shortage, lost topsoil.',
      '**Immediate causes:** **over-cultivation, overgrazing and deforestation**, made worse by drought.',
      '**Four components:** soil degradation, vegetation degradation, biodiversity degradation and water degradation (see figure).',
      '**Soil degradation** has three kinds:',
      '- **Physical**: **erosion** (the main one; water erosion everywhere, wind erosion on the coast and in the north-western lowlands), loss of structure because residues are burnt or fed to animals, **compaction** and hard pans, crusting.',
      '- **Chemical**: loss of **nutrients and organic matter** (harvests and residues removed and not replaced), nutrients **fixed** in strongly alkaline soils, **salinisation** (salt build-up, especially under irrigation with poor water, e.g. on the coast), acidification, sodication, laterisation.',
      '- **Biological**: organic matter down to **under 1 %** in many Eritrean soils; fewer earthworms, termites and microbes that build structure, fix nitrogen and decompose residues.'),
    DG('components-fig', 'Four components of land degradation', 162, 'components'),
    DG('soildeg-fig', 'Three kinds of soil degradation', 163, 'soildeg'),
    T('=agri12-u3-c04', '3.2.2 Causes of land degradation', 167,
      'Causes are **natural** and **human**, and they combine with social, economic and political factors.',
      '**Population:** one view blames population pressure for deforestation, overgrazing and farming of marginal land. But **it is what people do with the land that matters**: healthy, motivated farmers with secure rights can **reverse** degradation, and densely settled areas are often centres of land-care innovation (the terraced hills of the Eritrean highlands are an example). Poverty, illiteracy and insecure land tenure make degradation worse.'),
    DG('causes-fig', 'Natural and human causes', 168, 'causes'),
    T('=agri12-u3-c05', '3.2.3 Soil erosion', 169,
      '**Erosion** = soil and rock particles **detached and carried away** by water, wind, ice, gravity (creep) or living things, and deposited elsewhere. It is natural, but people speed it up greatly by clearing vegetation and ploughing. **Weathering** is different: it breaks rock down **in place**.',
      '**What controls the rate:**',
      '- **Climate**: amount and **intensity** of rain, wind, storms.',
      '- **Geology / soil**: rock and soil type, **porosity and permeability**, **slope**. Sandy and silty soils and steep slopes erode easily; clay resists more.',
      '- **Biology**: **ground cover** (the factor people change most) and land use. In a forest, litter and roots protect the soil; once trees are cut, infiltration falls and erosion rises.',
      'Erosion removes the fertile topsoil, exposes roots and fills dams and reservoirs with silt.'),
    DG('erosion-fig', 'Splash → sheet → rill → gully', 171, 'erosion',
       'The stages follow each other as water collects: drops, then a thin sheet, then small channels, then deep gullies.'),
    TB('erosion-tb', 'Types of erosion (Table 3.1)', 172, ['Type', 'What happens', 'Where / note'],
       [['Splash', 'Raindrops hit bare soil and throw particles into the air', 'Start of every storm on bare soil'],
        ['Sheet', 'Thin, even layer of topsoil washed off by overland flow', 'Gentle slopes, flat land; hard to see'],
        ['Rill', 'Small channels a few cm deep', 'Fields with poor cover; ploughing wipes them out'],
        ['Gully', 'Deep channels that tillage cannot remove', 'Advanced rills; need check dams'],
        ['Wind', 'Deflation (dust lifted) and abrasion (sand blasting)', 'Dry, bare land: coast, north-western lowlands']], layout='cards'),
    RM('gully-note', 'Note on gully depth', 172,
       'The textbook says gullies may be "75 to 150 metres" deep. Most gullies are **from about 0.5 m to a few tens of metres** deep; channels 100 m deep are canyons. Also, ice and snow-melt erosion do not occur in Eritrea.'),
    DG('wind-fig', 'Wind erosion', 173, 'wind'),
    T('soilloss-txt', 'Soil losses and their cost in Eritrea', 173,
      '- Net loss from **croplands**: about **12 t/ha a year**, because **fallowing and rotation** are used less and less, and farms get smaller as population grows.',
      '- Estimated loss: **highlands 50–100 t/ha**, **moist lowlands 47**, **eastern escarpment 37**, **dry lowlands 6 t/ha** a year.',
      '- Consequences: less organic matter, so less water stored and less infiltration; crops suffer more in drought; poor regrowth of vegetation; fertility decline.',
      '- **Dung burned as fuel** in the highlands: about **273 000 t a year**. With 1.4 % N and 1.3 % P, that is about **3 800 t of nitrogen and 3 500 t of phosphorus** lost every year.'),
    DG('dung-fig', 'Nutrients up in smoke', 174, 'dung'),
    WK('wk-dung', 'How much fertiliser does burnt dung equal?', 174,
       'Burnt dung loses 3 800 t of nitrogen a year. Urea contains 46 % N. How much urea would replace it?',
       ['Urea needed = N ÷ 0.46.', '3 800 ÷ 0.46 ≈ 8 260 t.'], 'About 8 300 t of urea every year, just for the nitrogen.'),
]

L3 = [
    T('swc-intro', '3.3 SWC measures: biological and physical', 176,
      'SWC measures are chosen for the **site** and its problem. Two broad groups, best used **together**:',
      '- **Biological (vegetative / agronomic)**: plants and farming practices: enclosures, afforestation, grass strips, cover crops, mulch, rotation, agroforestry.',
      '- **Physical (mechanical / structural)**: earth and stone works: terraces, stone bunds, check dams, diversion ditches, waterways, gabions.',
      'A stone bund protects a field at once; grass planted on it makes it stronger every year.'),
    DG('landscape-fig', 'The right measure in the right place', 177, 'landscape'),
    TB('sites-tb', 'Measures by site (Table 3.2)', 177, ['Site', 'Measures'],
       [['Uncultivated hillsides', 'Enclosures, afforestation, hillside (forest) terraces, micro-basins, check dams'],
        ['Cropland: agronomic', 'Fertiliser and manure, cover crops, rotation, intercropping, tillage practices, grass strips on the contour, parkland, windbreaks'],
        ['Cropland: physical', 'Terraces, stone bunds, diversion ditches, waterways, gully control, live fencing'],
        ['Riverbanks', 'Gabions and planting']], layout='cards'),
    RM('=agri12-u3-c07', 'Biological measures', 186,
       'Enclosures · afforestation · grass strips · cover crops · mulch · crop rotation and intercropping · manure · agroforestry · riverbank planting. They **cover the soil** and **add organic matter**.'),
    RM('=agri12-u3-c08', 'Physical measures', 185,
       'Hillside, bench and broad- or narrow-based terraces · stone and soil bunds · micro-basins · check dams · cut-off/diversion ditches · waterways · gabions · land levelling. They **shorten the slope** and **slow the water**.'),
    T('=agri12-u3-c09', '3.3.1 Surveying for SWC', 177,
      'Before building structures you must measure distances, heights and slopes and mark **contours**.',
      '- **Horizontal interval (HI)**: horizontal distance between two points (used on maps).',
      '- **Vertical interval (VI)**: difference in height between them.',
      '- **Slope** can be given as an **angle** (degrees), a **percentage** (VI ÷ HI × 100), a **ratio** 1 : n (vertical always 1) or **metres per metre** (e.g. 0.4 % = 0.004 m/m for a canal).',
      '- Slope classes: **0–8 %** level to gently undulating, **8–30 %** rolling to hilly, **over 30 %** steep to mountainous.',
      '- **Contour**: a line joining points of the **same height**. **Levelling**: measuring height differences; **profile levelling** at fixed distances along a line.',
      '**Instruments:** chain and tape (a surveyor\'s chain is **20 m or 30 m** long), **line level**, **clinometer** (hand-held, reads % slope and degrees), **flexible-tube (water) level**, **magnetic compass** (bearings: N 0°, E 90°, S 180°, W 270°), **telescopic level** (most accurate, most expensive).'),
    DG('slope-fig', 'HI, VI and slope', 178, 'slope'),
    WK('wk-slope', 'Expressing one slope four ways', 178,
       'Two pegs are 40 m apart horizontally, and one is 6 m higher. Give the slope as a percentage, a ratio, in m/m and as an angle, and classify it.',
       ['Percentage = VI ÷ HI × 100 = 6 ÷ 40 × 100 = 15 %.', 'Ratio = 6 : 40 = 1 : 6.7.', 'm/m = 6 ÷ 40 = 0.15 m/m.',
        'Angle: tan θ = 0.15, so θ ≈ 8.5°.', '15 % lies in 8–30 %: rolling to hilly.'],
       '15 %, 1 : 6.7, 0.15 m/m, about 8.5°; rolling to hilly land.'),
    RM('slope-note', 'Watch out: per cent is not degrees', 178,
       'A 100 % slope is **45°** (VI = HI), not vertical. Activity 3.5 (HI 60 m, VI 120 m) gives **200 %**, about **63°**: a cliff, not farmland, but the formula is the same.'),
    DG('contour-fig', 'Contours and terraces', 179, 'contour'),
    DG('linelevel-fig', 'Line level', 180, 'linelevel',
       'Two identical 1.5 m sticks, 10 m apart, joined by a cotton string tied at the 0 mark; a small spirit level hangs in the middle. Move the second stick up or down the slope until the bubble is centred: both pegs are then on the same contour.'),
    DG('tubelevel-fig', 'Water-tube level', 181, 'tubelevel',
       'Water finds its own level: when the two poles stand at the same height, the water in both ends is at the same mark.'),
    RM('survey-err', 'Textbook check: chain length and map scale', 179,
       '- The textbook says the metric chain is "30 **cm**" long. It is **20 m or 30 m**.',
       '- It says on a 1 : 1 000 map "1 cm = 1 000 **m**". Wrong: 1 cm on the map = 1 000 **cm** = **10 m** on the ground, so 3 cm = **30 m**, not 3 000 m.',
       '- "Much more expressive" for the telescopic level should read "much more **expensive**".'),
    WK('wk-scale', 'Map scale and area', 184,
       'On a 1 : 2 000 plan, a rectangular field measures 4 cm by 2.5 cm. Find its real size and area in hectares.',
       ['1 cm on the plan = 2 000 cm = 20 m.', 'Length = 4 × 20 = 80 m; width = 2.5 × 20 = 50 m.', 'Area = 80 × 50 = 4 000 m².', '4 000 ÷ 10 000 = 0.4 ha.'],
       '80 m × 50 m = 4 000 m² = 0.4 ha.'),
    RM('scale-rm', 'Large scale vs small scale', 184,
       '**Large-scale** map (1 : 1 000) = **small area, much detail** (a farm plan). **Small-scale** map (1 : 100 000) = **large area, little detail** (a zoba map). Big fraction = large scale.'),
    T('=agri12-u3-c10', '3.3.2 Physical SWC measures', 185,
      'Earthworks that **cut the slope into short sections**, so runoff is caught and slowed before it gains speed, soaks into the soil and recharges groundwater.',
      '- **Hillside terraces**: ditches or ridges on the contour for runoff control on uncultivated slopes.',
      '- **Bench terraces**: level steps, like a staircase, for crops on steep land.',
      '- **Broad-based** (gentle slopes, can be cropped over) and **narrow-based** terraces.',
      '- **Stone bunds**: stone walls on the contour; soil collects behind them and the field slowly becomes terraced. Very common on Eritrean farms.',
      '- **Micro-basins**: small half-moon basins round each seedling, staggered so runoff missed by one is caught by the next.',
      '- **Check dams**: walls of stone (or gabions, brushwood) across a gully; silt fills behind them and the gully heals. Key them into the banks and leave a lower spillway in the centre.',
      '- **Diversion (cut-off) ditches** lead runoff safely away from fields into **waterways**; **land levelling** for irrigation.'),
    DG('terraces-fig', 'Terraces and bunds in section', 185, 'terraces'),
    DG('checkdam-fig', 'Healing a gully', 185, 'checkdam'),
    DG('microbasin-fig', 'Micro-basins', 185, 'microbasin'),
    WK('wk-terrace', 'Spacing stone bunds', 185,
       'Bunds are placed so that the height difference between them (VI) is 1 m. On a 10 % slope, how far apart (HI) should they be? How many bunds fit on a 200 m long slope?',
       ['% slope = VI ÷ HI × 100, so HI = VI × 100 ÷ % slope.', 'HI = 1 × 100 ÷ 10 = 10 m.', '200 ÷ 10 = 20 spaces, so about 20 bunds.'],
       'Every 10 m; about 20 bunds. (On a 20 % slope they would be 5 m apart: steeper land needs closer structures.)'),
    T('=agri12-u3-c11', '3.3.3 Biological SWC measures', 186,
      'Plants protect the soil with **cover** (no splash), **roots** (hold soil) and **organic matter** (more infiltration). Use them:',
      '- on **uncultivated hillsides**: **enclosures** and **afforestation**;',
      '- on **cropland**: **agronomic** measures and **agroforestry** (parkland trees, windbreaks, grass and shrubs planted on bunds);',
      '- on **riverbanks**: protect riverine vegetation and plant suitable species with **gabions**.'),
    T('=agri12-u3-c12', '3.3.4 Agronomic practices and good land husbandry', 186,
      '**Agronomic practices** = ways of managing crops that also conserve soil and water: **manure and fertiliser** (more growth = more cover), **cover crops**, **crop rotation and intercropping**, **crop-residue and organic-matter management**, **mulching**, appropriate **tillage**, **trash lines** and **contour strip-cropping**.',
      '- **Soil management** = all tillage, cropping, fertiliser and lime treatments applied to a soil.',
      '- **Water management** = conserving and using rain, flood and soil water with minimum waste.',
      '- **Land husbandry** = caring for, managing and improving land, like animal or crop husbandry.',
      '- **Conservation agriculture** = farming that keeps soil covered and disturbed as little as possible (rotation, cover crops, minimum or zero tillage, stubble mulch) to keep moisture all season; it suits Eritrea\'s dry areas.',
      'Major soil problems to manage: acidity, salinity, alkalinity, compaction, erosion, and swelling–shrinking clays.'),
    DG('agronomic-fig', 'Six agronomic measures', 186, 'agronomic'),
]

L4 = [
    T('wh-intro', '3.4 Water harvesting', 190,
      'Earth has plenty of water, but **fresh water** is scarce. **Water harvesting** = collecting and storing rain and runoff for people, animals and crops; it can turn rain-fed farming into irrigated farming.',
      'Options: **roof** harvesting, ponds and small dams on seasonal rivers, large dams on major rivers (without harming local communities), **diversion** of seasonal floods (**spate**), **fog harvesting** on the misty eastern escarpment, **desalination** of sea and brackish water, and **artificial groundwater recharge**. Households, community organisations, NGOs and government all have to invest.'),
    T('=agri12-u3-c13', '3.4.1 Dams', 191,
      'A **dam** blocks a river to store water in a **reservoir** for **drinking, livestock, irrigation, hydro-power and flood control**. Earth dams have an earth embankment with an **impervious clay core** to stop seepage, and a **spillway** to pass floods safely. Example: **Toker dam** near Asmara; many micro-dams across the highlands.',
      '**Disadvantages:** costly; silt fills the reservoir if the catchment is bare; water lost by evaporation; land flooded; still water can breed mosquitoes and snails (malaria, bilharzia).'),
    DG('dam-fig', 'Earth dam', 191, 'dam'),
    T('=agri12-u3-c14', '3.4.2 Ponds', 192,
      'A **pond** is made by digging a pit or by building a short embankment across a watercourse. In Eritrea ponds are small, about **500–5 000 m³**, and used for short periods, mostly in arid areas. On flat land dig; on a slope use the dug soil to build an embankment and store more.',
      'Uses: **livestock**, **household water**, **small-scale irrigation** of vegetables. Fence them and keep animals out to keep the water clean.'),
    WK('wk-pond', 'How long will a pond last?', 192,
       'A 3 000 m³ pond supplies 200 cattle (40 L each a day) and loses 5 mm of depth a day by evaporation over a surface of 1 500 m². About how many days will it last?',
       ['Cattle use 200 × 40 = 8 000 L = 8 m³ a day.', 'Evaporation = 1 500 m² × 0.005 m = 7.5 m³ a day.', 'Total ≈ 15.5 m³ a day.', '3 000 ÷ 15.5 ≈ 190 days.'],
       'About 190 days (around 6 months); evaporation uses almost half the water.'),
    T('=agri12-u3-c15', '3.4.3 River diversion', 192,
      'A **diversion structure** across a river sends a controlled amount of water into a **canal**. Examples: the diversion works at **Sheeb** (Northern Red Sea) and the canals around **Megolo** (Gash-Barka). Diversion is the heart of **spate irrigation**.'),
    DG('spate-fig', 'Spate irrigation', 199, 'spate'),
    T('=agri12-u3-c16', '3.4.4 Wells', 193,
      'Wells are a major source of water for irrigation and homes. **Open (hand-dug) wells** are dug in **riverbeds, valleys and flat land** (never on hilltops), and can be lined with stone and cement. **Drilled (tube) wells** with a pump are used mostly for homes and livestock.',
      'A **sub-surface dam** is a wall of clay or masonry built down to the rock across a sandy riverbed; it holds water in the sand where it does not evaporate. Put the **well on the upstream side, close to the dam**.'),
    DG('subdam-fig', 'Sub-surface dam with a well', 193, 'subdam'),
    RM('river-err', 'Textbook check: "no perennial rivers"', 193,
       'The textbook says Eritrea has "no perennial rivers". The **Setit (Tekeze)** on the south-western border flows all year; most other rivers (Gash, Barka, Anseba, Mereb) are **seasonal**. So: Eritrea has **very few** perennial rivers.'),
    T('=agri12-u3-c17', '3.4.5 Roof and rock-outcrop harvesting', 194,
      '**Concrete** and **corrugated-iron** roofs are excellent catchments: gutters lead the rain into a **concrete cistern** for drinking and small vegetable gardens. Bare **rock outcrops** can be used the same way, with low walls leading the runoff into a tank.',
      '**Rule of thumb:** water collected (m³) ≈ roof area (m²) × rainfall (m) × 0.8 (some water is lost by splashing and evaporation).'),
    DG('roof-fig', 'Roof harvesting', 194, 'roof'),
    WK('wk-roof', 'Sizing a cistern', 194,
       'A school roof is 12 m × 8 m. Asmara gets about 500 mm of rain a year. How much water can be collected, and how many 200 L drums would it fill?',
       ['Area = 12 × 8 = 96 m².', 'Rain = 500 mm = 0.5 m.', 'Water = 96 × 0.5 × 0.8 = 38.4 m³.', '38.4 m³ = 38 400 L; 38 400 ÷ 200 = 192 drums.'],
       'About 38 m³ (38 400 L) a year, enough for about 190 drums.'),
]

L5 = [
    T('=agri12-u3-c18', '3.5 Irrigation and drainage: the big picture', 195,
      'Water management on a farm means getting **enough water to the roots** (irrigation) and **taking away excess water and salt** (drainage). Both are needed: irrigation without drainage ends in waterlogging and salty soil.'),
    T('=agri12-u3-c19', '3.5.1 Irrigation', 195,
      '**Irrigation** = artificial application of water to the soil, carried from the source to the crop in open canals or pipes. Farming that depends only on rain is **rain-fed**. Irrigation is very old: evidence from Mesopotamia, Egypt and Iran goes back to the **6th millennium BCE**.',
      'Other uses: protecting crops from frost, controlling weeds, preventing soil consolidation.'),
    T('=agri12-u3-c20', '3.5.2 Why irrigation matters', 196,
      '- In arid and semi-arid areas it **extends cultivation**, **raises yields** and **insures against unreliable rain**; in humid areas **supplementary irrigation** covers dry spells at critical stages.',
      '- Water comes from **surface water** (rivers, dams) or **groundwater** (wells); groundwater also lowers a high water table.',
      '- Eritrea\'s potential irrigable area is **107 000–567 000 ha** (the upper figure counts all land that is topographically suitable).',
      '- Irrigation allows **multiple cropping**, a more varied diet (vegetables, fruit), better nutrition and health, income, rural jobs, and **cheaper food** for the urban poor.',
      '- **Risks:** waterlogging, salinity, water-borne diseases, high costs and conflicts over water: irrigation is not always beneficial unless well managed.'),
    T('=agri12-u3-c21', '3.5.3 Methods of irrigation', 198,
      'The aim is to wet the whole field **evenly**, neither too much nor too little.',
      '**Surface (traditional) irrigation**: water flows over the land by **gravity**. Cheap to build, but **labour-costly to run** and **inefficient** (40–50 %).',
      '- **Furrow**: water runs in furrows between ridges; widespread in Eritrea (e.g. banana farms near **Tesseney**).',
      '- **Basin**: level plots surrounded by earth bunds are flooded.',
      '- **Border strip**: long strips between low ridges.',
      '- **Spate**: diverts floods from highland rains into bunded fields; widely used in the **eastern lowlands** (Sheeb, Wadi Laba) and introduced in the western lowlands.',
      '**Modern (pressurised / localised)**: expensive to install, cheap to run, efficient.',
      '- **Sprinkler**: spray from pipes or rotating heads; about **75 %** reaches the crop; irrigate at **night** to cut evaporation.',
      '- **Drip (trickle)**: drops at each plant\'s roots; the most efficient (up to about 90 %); fertiliser can be added (**fertigation**); often combined with plastic mulch; high cost for subsistence farmers.',
      '- **Centre pivot**: a long sprinkler pipe on wheeled towers turning round a central point; on flat lowlands such as **Gerset** and **Fanko**.',
      '- **Sub-irrigation**: raising the water table so roots are wetted from below; used in greenhouses with nutrient solution recycled.'),
    DG('methods-fig', 'How efficient is each method?', 198, 'methods'),
    TB('methods-tb', 'Surface vs modern irrigation', 198, ['', 'Surface (furrow, basin, spate)', 'Modern (sprinkler, drip, pivot)'],
       [['Cost to install', 'Low', 'High'], ['Cost to run', 'High (labour)', 'Low'], ['Water-use efficiency', '40–50 %', '75–90 %'],
        ['Land', 'Needs levelled land', 'Works on uneven land too'], ['Skills', 'Traditional', 'Technical; filters, pumps']], layout='compare'),
    DG('drip-fig', 'Drip layout', 200, 'drip'),
    DG('pivot-fig', 'Centre pivot', 201, 'pivot'),
    WK('wk-eff', 'Water saved by changing method', 198,
       'A tomato plot needs 3 000 m³ of water to reach the roots in a season. How much water must be supplied with furrow (45 % efficient) and with drip (90 %)?',
       ['Water supplied = water needed ÷ efficiency.', 'Furrow: 3 000 ÷ 0.45 ≈ 6 670 m³.', 'Drip: 3 000 ÷ 0.90 ≈ 3 330 m³.', 'Saving ≈ 3 340 m³, half the water.'],
       'Furrow ≈ 6 670 m³, drip ≈ 3 330 m³: drip halves the water bill.'),
    T('=agri12-u3-c22', '3.5.4 Drainage', 202,
      '**Drainage** = removing **excess water** from the surface and the upper subsoil. Waterlogged soil has **no air**: roots suffocate, toxic substances build up, microbes stop working, the soil is hard to cultivate and is damaged by ploughing.',
      '**Causes of poor drainage:** heavy rain; **clay** soils that let water through slowly; permeable sand or gravel lying over an **impermeable clay layer**; **hard pans** in the subsoil.'),
    T('=agri12-u3-c23', '3.5.5 Why drainage matters, even in dry areas', 203,
      '- Even a **week** of waterlogging can kill fruit trees.',
      '- In dry areas, **irrigation water always carries salts**. Evaporation and transpiration remove the water and leave the salt, which can reach toxic levels (**salinisation**). Fields need occasional **extra irrigation to leach** salt below the roots, plus drainage to carry it away.',
      '- Salt sources: the soil itself, saline irrigation water, rising groundwater, seawater intrusion near the coast.',
      '**Benefits of drainage:** better **aeration**; a **deeper root zone**; **warmer** soil, so faster nutrient release; more **micro-organism** activity.'),
    DG('salt-fig', 'How salt builds up', 204, 'salt'),
    T('=agri12-u3-c24', '3.5.6 Types of drainage', 204,
      '- **Surface drainage**: shallow **open ditches** leading into bigger collector drains; fields are **graded** to slope towards them.',
      '- **Sub-surface drainage**: buried **perforated pipes** (laterals → collectors → mains → sump); used where natural drainage is poor, to **leach salts** and to **lower a shallow water table**.',
      '- **Vertical drainage**: **pumping** groundwater out of dug or tube wells; works where poorly permeable topsoil lies over deep permeable subsoil.',
      '- **Bio-drainage**: planting thirsty trees (e.g. **eucalyptus**) and crops that pump water out through transpiration.'),
    DG('drains-fig', 'Four drainage systems', 204, 'drains'),
]

LESSONS = {'agri12-u3-l3-1': L1, 'agri12-u3-l3-2': L2, 'agri12-u3-l3-3': L3, 'agri12-u3-l3-4': L4, 'agri12-u3-l3-5': L5}

DROP = []
PATCH = {}

# ------------------------------------------------------------------ practice
a = QSet('3.1–3.2 Practice — SWC and land degradation', 's31')
a.M(159, 'Which part of Eritrea has the greatest livestock density and the worst land degradation?', ['Dry lowlands', 'Highlands', 'Coastal plain', 'Western lowlands'], 'B',
    ['Step 1: The textbook names the highlands.', 'Step 2: Steep slopes, many animals and intense rain combine there.'], 'High land, high damage.', [('What is the mean measured soil loss in the highlands?', '42 t/ha a year.')])
a.S(159, 'How many times faster than it forms can soil be lost on poorly conserved land?', '20 to 40 times faster.',
    ['Step 1: Soil forms very slowly (fractions of a mm a year).', 'Step 2: Erosion removes mm every year.'], '20–40 ×.', [('What is Eritrea\'s average cereal yield?', '0.74 t/ha.')])
a.S(160, 'Give four benefits of soil and water conservation.', 'More organic matter and water retention; more infiltration, less runoff; less siltation of dams; ponds and dams allow irrigation; restored land for farming; higher productivity (any four).',
    ['Step 1: Soil benefits.', 'Step 2: Water benefits.', 'Step 3: Economic benefits.'], 'Soil, water, money.', [('How does SWC make dams last longer?', 'Less soil washes into them, so they silt up more slowly.')])
a.M(162, 'The immediate causes of land degradation are', ['over-cultivation, overgrazing and deforestation', 'irrigation and drainage', 'terracing and bunding', 'fallowing and rotation'], 'A',
    ['Step 1: These three remove cover and nutrients directly.'], 'Plough, graze, cut.', [('Which climatic factor speeds up degradation?', 'Drought.')])
a.M(163, 'Which is NOT chemical soil degradation?', ['Salinisation', 'Nutrient loss', 'Compaction', 'Nutrient fixation in alkaline soil'], 'C',
    ['Step 1: Compaction changes the physical structure.', 'Step 2: The others change soil chemistry.'], 'Squeeze = physical.', [('Give an example of biological degradation.', 'Organic matter below 1 %; loss of soil fauna.')])
a.M(169, 'Erosion differs from weathering because erosion', ['happens only in rock', 'moves particles away from their source', 'is always chemical', 'is caused only by people'], 'B',
    ['Step 1: Weathering breaks rock in place.', 'Step 2: Erosion detaches and transports.'], 'Weather = stay; erode = go.', [('Name three agents of erosion.', 'Water, wind, ice (also gravity, organisms).')])
a.M(170, 'Which factor affecting erosion can people change most easily?', ['Rainfall intensity', 'Rock type', 'Ground cover', 'Slope of the land'], 'C',
    ['Step 1: We cannot change rain or geology.', 'Step 2: We can keep vegetation and mulch on the soil.'], 'Cover is in our hands.', [('Which erodes more easily: clay or silt?', 'Silt.')])
a.M(172, 'Water flowing in narrow channels that ordinary ploughing cannot remove causes', ['sheet erosion', 'rill erosion', 'gully erosion', 'splash erosion'], 'C',
    ['Step 1: Rills are smoothed by tillage.', 'Step 2: Gullies are too deep.'], 'Gully = too deep to plough.', [('Which type removes a thin even layer of topsoil?', 'Sheet erosion.')])
a.TF(173, 'Wind erosion is most serious on the coast and in the north-western lowlands.', True,
     ['Step 1: These are the driest, least vegetated areas.', 'Step 2: Wind lifts fine dust (deflation) and blasts surfaces (abrasion).'], 'Dry + bare + wind.', [('What is deflation?', 'Lifting and removal of fine particles by wind.')])
a.S(174, 'Burnt dung amounts to 273 000 t a year and contains 1.3 % phosphorus. Calculate the phosphorus lost.', 'About 3 550 t of P a year (textbook: 3 500 t).',
    ['Step 1: 273 000 × 1.3 ÷ 100.', 'Step 2: = 3 549 t.'], 'Percentage × total.', [('How much nitrogen at 1.4 %?', 'About 3 800 t.')])
a.S(173, 'Give two reasons for the 12 t/ha net soil loss from Eritrean croplands.', 'Fallowing and crop rotation are practised less and less; and farms get smaller as population grows, so land is used more intensively.',
    ['Step 1: Traditional protection is disappearing.', 'Step 2: More pressure on less land.'], 'Less fallow, more people.', [('What is the estimated loss in the dry lowlands?', 'About 6 t/ha a year.')])

b = QSet('3.3 Practice — surveying and SWC measures', 's33')
b.S(178, 'Calculate the percentage slope when HI = 80 m and VI = 12 m, and classify it.', '15 %: rolling to hilly (8–30 %).',
    ['Step 1: 12 ÷ 80 = 0.15.', 'Step 2: × 100 = 15 %.', 'Step 3: 8–30 % = rolling to hilly.'], 'VI over HI.', [('Express 15 % as a ratio.', 'About 1 : 6.7.')])
b.S(179, 'Write a canal gradient of 0.5 % in metres per metre.', '0.005 m/m.',
    ['Step 1: 0.5 % = 0.5 ÷ 100.', 'Step 2: = 0.005 m of fall per m of canal.'], 'Divide by 100.', [('How much does such a canal fall in 200 m?', '1 m.')])
b.M(179, 'A line joining points of equal height is a', ['gradient', 'contour', 'bearing', 'profile'], 'B',
    ['Step 1: Definition of a contour.'], 'Con-tour = same level all round.', [('What does close spacing of contours show?', 'A steep slope.')])
b.M(180, 'In a line level, the bubble of the spirit level is centred when', ['the string is tight', 'both sticks stand at the same height', 'the sticks are 1.5 m apart', 'the slope is 10 %'], 'B',
    ['Step 1: The string is tied at the same mark on identical sticks.', 'Step 2: Level string = sticks at equal height = same contour.'], 'Bubble in the middle = level.', [('How far apart are the sticks of a line level?', '10 m (string about 10.5 m).')])
b.M(181, 'Why must air bubbles be tapped out of a flexible-tube level?', ['To make it lighter', 'They give false water levels', 'To colour the water', 'They slow evaporation'], 'B',
    ['Step 1: Trapped air breaks the column of water.', 'Step 2: Then the two ends no longer show the same level.'], 'Bubbles lie.', [('What principle does the tube level use?', 'Water finds its own level.')])
b.S(184, 'On a 1 : 1 000 map two wells are 3 cm apart. How far apart are they on the ground?', '30 m.',
    ['Step 1: 1 cm = 1 000 cm = 10 m.', 'Step 2: 3 × 10 = 30 m (the textbook\'s "3 000 m" is wrong).'], 'Same units: cm to cm.', [('On 1 : 50 000, what is 2 cm?', '100 000 cm = 1 km.')])
b.TF(184, 'A 1 : 100 000 map is a large-scale map.', False,
     ['Step 1: 1/100 000 is a small fraction.', 'Step 2: Small fraction = small scale = large area.'], 'Big fraction = large scale.', [('Give an example of a large-scale map ratio.', '1 : 1 000.')])
b.M(185, 'Which is NOT a physical SWC measure?', ['Check dam', 'Micro-basin', 'Land levelling', 'Afforestation'], 'D',
    ['Step 1: Afforestation uses plants: biological.'], 'Plants = biological.', [('Is a stone bund physical or biological?', 'Physical.')])
b.S(185, 'How do physical SWC measures reduce erosion?', 'They shorten the slope length and reduce its angle, intercepting runoff so it slows down, drops its soil and soaks in instead of forming rills and gullies.',
    ['Step 1: Speed of water grows with slope length and steepness.', 'Step 2: Structures break the slope into short level sections.'], 'Short slope, slow water.', [('Where should the spillway of a check dam be?', 'In the centre, lower than the sides.')])
b.S(185, 'Stone bunds are to be built with a 0.75 m vertical interval on a 15 % slope. How far apart should they be?', '5 m.',
    ['Step 1: HI = VI × 100 ÷ %.', 'Step 2: 0.75 × 100 ÷ 15 = 5 m.'], 'HI = 100 VI ÷ slope.', [('And on a 5 % slope?', '15 m.')])
b.M(185, 'Micro-basins on a hillside are staggered so that', ['they look neat', 'runoff missing one is caught by the next', 'goats can pass', 'they need fewer stones'], 'B',
    ['Step 1: Water flowing between basins in one row meets a basin in the row below.'], 'Zig-zag catches all.', [('What is planted in each micro-basin?', 'A tree seedling.')])
b.S(186, 'List four agronomic SWC practices.', 'Manure and fertiliser, cover crops, crop rotation, intercropping, mulching, crop-residue management, minimum tillage, contour strip-cropping, trash lines (any four).',
    ['Step 1: Think of what keeps the soil covered and rich.'], 'Cover + organic matter.', [('What is fertigation?', 'Adding fertiliser through drip irrigation water.')])
b.S(188, 'What is the main idea of conservation agriculture?', 'Keep the soil covered and disturb it as little as possible (minimum or zero tillage, mulch, cover crops, rotation) so moisture is kept and yields are reliable with fewer inputs.',
    ['Step 1: Less tillage.', 'Step 2: More cover.'], 'Cover and don\'t disturb.', [('Define land husbandry.', 'The care, management and improvement of land resources.')])

c = QSet('3.4–3.5 Practice — water harvesting, irrigation and drainage', 's34')
c.M(191, 'Dams are constructed to store water for', ['irrigation', 'hydro-electric power', 'flood control', 'all of these'], 'D',
    ['Step 1: The textbook lists all three, or any combination.'], 'Multi-purpose.', [('What stops seepage through an earth dam?', 'An impervious clay core.')])
c.S(191, 'Give two disadvantages of dams.', 'High cost; siltation; evaporation losses; flooding of land; breeding of malaria mosquitoes and bilharzia snails (any two).',
    ['Step 1: Cost and silt.', 'Step 2: Health and land.'], 'Cost, silt, sickness.', [('Name a dam near Asmara.', 'Toker dam.')])
c.M(192, 'Typical ponds in Eritrea hold about', ['5–50 m³', '500–5 000 m³', '50 000–500 000 m³', 'over 1 million m³'], 'B',
    ['Step 1: Textbook: 500–5 000 m³.'], 'Ponds are small.', [('Give two uses of pond water.', 'Livestock, household use, small-scale irrigation.')])
c.M(194, 'Where should a well be placed relative to a sub-surface dam?', ['Downstream, far away', 'Upstream, close to the dam', 'On a hilltop', 'In the spillway'], 'B',
    ['Step 1: Water collects in the sand behind (upstream of) the wall.'], 'Upstream = where the water is held.', [('Why are wells never dug on hilltops?', 'The water table is too deep there; water collects in valleys and riverbeds.')])
c.S(194, 'How much water can a 50 m² roof collect in a year with 400 mm of rain (use 0.8 for losses)?', '16 m³ (16 000 L).',
    ['Step 1: 400 mm = 0.4 m.', 'Step 2: 50 × 0.4 × 0.8 = 16 m³.'], 'Area × rain × 0.8.', [('How many litres is 1 m³?', '1 000 L.')])
c.M(199, 'Spate irrigation uses', ['groundwater pumped by wind', 'flood water from highland rains diverted to fields', 'water from desalination', 'drip lines'], 'B',
    ['Step 1: Spate = sudden seasonal flood.', 'Step 2: Diversion bunds lead it into bunded fields (Sheeb, eastern lowlands).'], 'Spate = flood.', [('Where is spate irrigation widely used in Eritrea?', 'The eastern lowlands.')])
c.M(198, 'Surface irrigation is', ['expensive to install, cheap to run, efficient', 'cheap to install, costly to run, less efficient', 'only for greenhouses', 'pressurised'], 'B',
    ['Step 1: Gravity, no pipes = cheap to build.', 'Step 2: Much labour and 40–50 % efficiency.'], 'Cheap now, costly later.', [('Why irrigate with sprinklers at night?', 'Less evaporation.')])
c.S(198, 'A field needs 1 800 m³ at the roots. How much must be supplied by sprinkler (75 % efficient)?', '2 400 m³.',
    ['Step 1: Supplied = needed ÷ efficiency.', 'Step 2: 1 800 ÷ 0.75 = 2 400 m³.'], 'Divide by efficiency.', [('And by furrow at 45 %?', '4 000 m³.')])
c.M(201, 'Centre-pivot irrigation in Eritrea is found on flat land at', ['Nakfa', 'Gerset and Fanko', 'Asmara', 'Massawa harbour'], 'B',
    ['Step 1: It needs large flat fields: the western lowlands (Gash-Barka).'], 'Pivot = flat lowlands.', [('What kind of irrigation is a centre pivot?', 'A form of sprinkler irrigation.')])
c.TF(200, 'Drip irrigation is the cheapest system for subsistence farmers to establish.', False,
     ['Step 1: Drip is the most water-efficient.', 'Step 2: But establishment and maintenance costs are high.'], 'Efficient ≠ cheap.', [('What is mixing fertiliser into drip water called?', 'Fertigation.')])
c.S(203, 'Why may irrigated land in a dry area need drainage?', 'Irrigation water contains salts; evaporation leaves them behind and they build up to toxic levels; extra water is needed to leach the salt below the roots and drains must carry it away.',
    ['Step 1: Salts in water.', 'Step 2: Evaporation concentrates them.', 'Step 3: Leach + drain.'], 'No drainage, more salt.', [('Name two sources of salinity.', 'Saline irrigation water; rising groundwater; seawater intrusion; salts in the soil.')])
c.M(205, 'Planting eucalyptus to dry out waterlogged land is', ['surface drainage', 'vertical drainage', 'bio-drainage', 'sub-irrigation'], 'C',
    ['Step 1: Bio = living plants remove the water by transpiration.'], 'Bio = trees as pumps.', [('Which drainage uses buried perforated pipes?', 'Sub-surface drainage.')])
c.S(203, 'List three causes of poor soil drainage.', 'Too much rain; clay soils; a permeable layer over an impermeable clay layer; hard pans in the subsoil (any three).',
    ['Step 1: Too much water in.', 'Step 2: Too slow out.'], 'In fast, out slow.', [('Give two benefits of drainage.', 'Better aeration, deeper roots, warmer soil, more microbial activity.')])

QS = a.items + b.items + c.items

GLOSSARY = [
    ('Soil and water conservation', 'Measures that keep soil on the land and protect the water supply.', 158),
    ('Land degradation', 'Fall in the land\'s present or future ability to produce goods and services.', 162),
    ('Salinisation', 'Build-up of soluble salts in soil, often under irrigation.', 163),
    ('Erosion', 'Detachment and transport of soil by water, wind, ice, gravity or organisms.', 169),
    ('Weathering', 'Breakdown of rock in place.', 169),
    ('Rill', 'Small erosion channel that ploughing removes.', 171),
    ('Gully', 'Erosion channel too deep to be removed by tillage.', 172),
    ('Deflation', 'Removal of fine particles by wind.', 173),
    ('Horizontal interval (HI)', 'Horizontal distance between two points.', 178),
    ('Vertical interval (VI)', 'Difference in height between two points.', 178),
    ('Contour', 'Line joining points of equal height.', 179),
    ('Clinometer', 'Hand-held instrument for measuring slope.', 181),
    ('Scale', 'Ratio of map distance to ground distance.', 184),
    ('Bench terrace', 'Level step cut into a slope for cropping.', 185),
    ('Check dam', 'Small barrier across a gully that traps sediment.', 185),
    ('Micro-basin', 'Small half-moon basin around a seedling to catch runoff.', 185),
    ('Conservation agriculture', 'Farming with minimum soil disturbance, permanent cover and rotation.', 188),
    ('Sub-surface dam', 'Underground wall across a sandy riverbed that holds water in the sand.', 193),
    ('Spate irrigation', 'Diverting seasonal floods onto bunded fields.', 199),
    ('Fertigation', 'Applying fertiliser through irrigation water.', 200),
    ('Drainage', 'Removal of excess water from the soil surface and subsoil.', 202),
    ('Bio-drainage', 'Using thirsty plants to lower a high water table.', 205),
]
TIPS = [('% slope = VI ÷ HI × 100; HI between bunds = VI × 100 ÷ % slope.', 178),
        ('Map scale: convert to the same unit first (1 : 1 000 → 1 cm = 10 m).', 184),
        ('Roof water ≈ area × rainfall (m) × 0.8.', 194),
        ('Water supplied = water needed ÷ efficiency.', 198)]
IDEAS = [('k_slope', 'HI, VI and % slope', 'l3_3', 'agri12-u3-ad-wk-slope'),
         ('k_structures', 'Terraces, bunds, check dams', 'l3_3', 'agri12-u3-c10'),
         ('k_harvest', 'Roof and pond harvesting', 'l3_4', 'agri12-u3-ad-wk-roof'),
         ('k_salinity', 'Salinity and leaching', 'l3_5', 'agri12-u3-ad-salt-fig')]

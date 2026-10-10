r"""Grade 11 Unit 3 — Crop Production (pp. 101-192): plant structure, growth factors, seed, field crops, cultural practices,
cropping systems and horticulture (nursery, propagation, garden layout, post-harvest)."""
import math
from common import set_unit, T, RM, MN, TB, DG, ST, WK, CK, QSet
from svglib import Fig, INK, BLUE, RED, GREEN, PURPLE, ORANGE, GREY, FILL, n
from agrilib import (box, tlines, wrap, flow, hflow, cycle, leader, ground, grass_tufts, sorghum, leaf, grass_leaf,
                     roots_fibrous, roots_tap, cow, person, maresha, sun, cloud, tree, BROWN, SOIL, SOIL2, SOIL3, LEAF,
                     LEAF2, STRAW, WATER)

UID = 'agri11-u3'
set_unit(UID)
DARK = '#3B6E2C'


# ------------------------------------------------------------------ figures
def mini_cereal(f, x, y, h=50):
    """light sorghum outline for small panels: stalk, two leaves, head"""
    f.path(f'M{x} {y} L{x} {y - h} M{x} {y - h * 0.35} Q{x + h * 0.3} {y - h * 0.55} {x + h * 0.42} {y - h * 0.38} M{x} {y - h * 0.6} Q{x - h * 0.3} {y - h * 0.8} {x - h * 0.42} {y - h * 0.62}', '#4E8B3A', 2.6)
    f.ellipse(x, y - h - 8, 5, 10, '#7A3E1D', 1, '#B5652E')
    return f


def few_roots(f, x, y, L=18):
    f.path(f'M{x} {y} q-6 {L * 0.6} -{L * 0.6} {L} M{x} {y} q0 {L * 0.6} 1 {L} M{x} {y} q6 {L * 0.6} {L * 0.6} {L}', BROWN, 1.2)
    return f


def bean_plant(f, x, y, h=150):
    """dicot (bean) plant on ground line y: tap root, stem with nodes, net-veined leaves, flower, pod"""
    f.path(f'M{x} {y} C{x - 2} {y - h * 0.4} {x + 3} {y - h * 0.7} {x} {y - h}', '#5E7F33', 3)
    for k, s in ((0.3, 1), (0.52, -1), (0.74, 1)):
        yy = y - h * k
        f.circle(x + 0.5, yy, 2.6, None, 0, '#46612A')
        f.line(x, yy, x + s * 22, yy - 10, '#5E7F33', 1.8)
        leaf(f, x + s * 22, yy - 10, 34, 90 - 60 * s, LEAF, 0.36)
        leaf(f, x + s * 22, yy - 10, 28, 90 - 15 * s, LEAF, 0.36)
    leaf(f, x, y - h, 26, 90, LEAF, 0.36)
    return f


def f_plant():
    f = Fig(340, 300)
    ground(f, 214, c='#E9D9BF', h=86)
    x, y = 120, 214
    bean_plant(f, x, y, 150)
    # flower and pod
    fx, fy = x - 24, y - 118
    f.line(x, y - 110, fx, fy, '#5E7F33', 1.4)
    for a in (0, 120, 240):
        t = math.radians(a)
        f.ellipse(fx + 5 * math.cos(t), fy + 5 * math.sin(t), 6, 4, PURPLE, 1, '#E7D5F2')
    f.line(x, y - 66, x + 18, y - 52, '#5E7F33', 1.4)
    f.path(f'M{x + 18} {y - 52} C{x + 34} {y - 50} {x + 44} {y - 36} {x + 46} {y - 22} C{x + 40} {y - 30} {x + 28} {y - 42} {x + 18} {y - 52}Z', '#6E7F2A', 1.3, '#C9D98A')
    for t in (0.3, 0.55, 0.8):
        f.circle(x + 18 + 26 * t, y - 52 + 28 * t, 2.6, '#6E7F2A', 0.8, '#E6EDB9')
    roots_tap(f, x, y, 60)
    leader(f, x, y - 150, 200, 26, 'shoot tip (terminal bud)', size=11)
    leader(f, fx - 6, fy, 56, 40, 'flower', size=11)
    leader(f, x + 40, y - 30, 220, 120, 'fruit (pod with seeds)', size=11)
    leader(f, x - 34, y - 110, 44, 84, 'leaf', size=11)
    leader(f, x + 0.5, y - 111, 220, 64, 'node (leaf joins stem)', size=11)
    leader(f, x + 1, y - 90, 220, 152, 'internode', size=11)
    leader(f, x, y - 30, 220, 184, 'stem', size=11)
    leader(f, x + 2, y + 34, 220, 240, 'tap root', size=11)
    leader(f, x + 14, y + 22, 220, 266, 'lateral roots', size=11)
    f.text(14, 206, 'shoot system', 11, GREEN, 'start').text(14, 232, 'root system', 11, BROWN, 'start')
    f.text(14, 296, 'Reproductive: flower, fruit, seed. Vegetative: root, stem, leaf, bud.', 10, GREY, 'start', False)
    return f


def f_monodicot():
    f = Fig(340, 330)
    f.text(92, 18, 'Monocot', 13, ORANGE).text(250, 18, 'Dicot', 13, GREEN)
    f.text(92, 32, '(sorghum, maize, barley)', 10, GREY, 'middle', False).text(250, 32, '(faba bean, chickpea)', 10, GREY, 'middle', False)
    rows = ['seed', 'leaf veins', 'flower parts', 'stem bundles', 'roots']
    for i, r in enumerate(rows):
        y = 44 + i * 57
        f.rect(4, y, 332, 54, GREY, 0.8, '#FBF8F3' if i % 2 else '#FFFFFF', 4)
        f.text(170, y + 12, r, 10.5, GREY)
    # seed
    y = 44 + 28
    f.ellipse(92, y + 4, 16, 22, '#B07A2A', 1.3, '#F3DE9C').path(f'M{86} {y + 18} C{80} {y + 8} {82} {y - 4} {90} {y - 10}', DARK, 2)
    f.text(130, y + 8, '1 cotyledon', 10.5, INK, 'start')
    f.ellipse(238, y + 4, 22, 15, '#7A4E2D', 1.3, '#EBD8B4').line(238, y - 11, 238, y + 19, '#7A4E2D', 1.2)
    f.text(266, y + 8, '2 cotyledons', 10.5, INK, 'start')
    # leaves
    y = 44 + 57 + 30
    f.path(f'M40 {y + 8} C70 {y - 12} 120 {y - 14} 150 {y - 6} C120 {y + 4} 70 {y + 10} 40 {y + 8}Z', DARK, 1.1, LEAF)
    for d in (-4, 0, 4):
        f.path(f'M44 {y + 7 + d * 0.3} C80 {y - 4 + d} 120 {y - 6 + d * 0.6} 146 {y - 6}', '#2F5A24', 0.7)
    f.text(92, y + 22, 'parallel', 10.5, INK)
    leaf(f, 196, y + 4, 84, 8, LEAF, 0.3, True)
    for t in (0.3, 0.5, 0.7):
        px, py = 196 + 84 * t * 0.99, y + 4 - 84 * t * 0.14
        f.line(px, py, px + 10, py - 9, '#2F5A24', 0.7).line(px, py, px + 6, py + 9, '#2F5A24', 0.7)
    f.text(238, y + 22, 'netted (reticulate)', 10.5, INK)
    # flower parts
    y = 44 + 114 + 30
    for k in range(3):
        t = math.radians(90 + 120 * k)
        f.ellipse(92 + 13 * math.cos(t), y - 13 * math.sin(t), 9, 6, ORANGE, 1, '#FCE3C4')
    f.circle(92, y, 4, None, 0, ORANGE).text(130, y + 4, 'in 3s', 10.5, INK, 'start')
    for k in range(5):
        t = math.radians(90 + 72 * k)
        f.ellipse(238 + 13 * math.cos(t), y - 13 * math.sin(t), 8, 6, PURPLE, 1, '#E7D5F2')
    f.circle(238, y, 4, None, 0, PURPLE).text(266, y + 4, 'in 4s or 5s', 10.5, INK, 'start')
    # stems
    y = 44 + 171 + 31
    f.circle(92, y, 18, DARK, 1.3, '#EAF2DF')
    for (dx, dy) in ((-8, -8), (6, -10), (10, 4), (-2, 2), (-10, 8), (4, 12), (-12, -1), (12, -4)):
        f.circle(92 + dx, y + dy, 2.2, None, 0, DARK)
    f.text(130, y + 4, 'scattered', 10.5, INK, 'start')
    f.circle(238, y, 18, DARK, 1.3, '#EAF2DF')
    for k in range(8):
        t = math.radians(45 * k)
        f.circle(238 + 11 * math.cos(t), y + 11 * math.sin(t), 2.4, None, 0, DARK)
    f.text(266, y + 4, 'in a ring', 10.5, INK, 'start')
    # roots
    y = 44 + 228 + 16
    roots_fibrous(f, 92, y, 30)
    f.text(130, y + 22, 'fibrous', 10.5, INK, 'start')
    roots_tap(f, 238, y, 34)
    f.text(266, y + 22, 'tap root', 10.5, INK, 'start')
    return f


def f_roots():
    f = Fig(340, 236)
    ground(f, 70, c='#E9D9BF', h=150)
    f.rect(0, 220, 340, 16, None, 0, '#FFFFFF')
    # tap (carrot)
    x = 56
    for a in (70, 90, 110):
        leaf(f, x, 70, 34, a, LEAF, 0.18, False)
    f.path(f'M{x - 10} 72 C{x - 8} 120 {x - 2} 160 {x} 190 C{x + 2} 160 {x + 8} 120 {x + 10} 72Z', '#B4561E', 1.3, '#F08A3C')
    f.text(x, 208, 'Tap root', 11.5, INK).text(x, 228, 'carrot', 10.5, GREY, 'middle', False)
    # tap with laterals (bean)
    x = 140
    f.line(x, 70, x, 30, '#5E7F33', 2.4)
    leaf(f, x, 34, 24, 40, LEAF, 0.35)
    leaf(f, x, 34, 24, 140, LEAF, 0.35)
    roots_tap(f, x, 72, 110)
    f.text(x, 208, 'Tap + laterals', 11.5, INK).text(x, 228, 'faba bean', 10.5, GREY, 'middle', False)
    # fibrous (sorghum)
    x = 224
    for a, L in ((60, 40), (100, 46), (125, 34)):
        grass_leaf(f, x, 70, L, a, 0.1)
    roots_fibrous(f, x, 72, 60)
    roots_fibrous(f, x, 72, 40)
    f.text(x, 208, 'Fibrous', 11.5, INK).text(x, 228, 'sorghum, teff', 10.5, GREY, 'middle', False)
    # adventitious prop/aerial roots (maize)
    x = 304
    f.line(x, 70, x, 14, '#5E7F33', 3)
    for dx in (-14, -7, 7, 14):
        f.path(f'M{x} 50 Q{x + dx * 0.5} 58 {x + dx} 74', BROWN, 1.6)
    roots_fibrous(f, x, 72, 36)
    f.text(x - 4, 208, 'Prop roots', 11.5, INK).text(x - 4, 228, 'maize', 10.5, GREY, 'middle', False)
    return f


def f_leafflower():
    f = Fig(360, 250)
    f.text(70, 18, 'Parts of a leaf', 12.5, GREEN).text(268, 18, 'Parts of a flower', 12.5, PURPLE)
    # leaf
    f.line(30, 228, 30, 120, '#5E7F33', 3)
    f.line(30, 170, 58, 150, '#5E7F33', 2)
    f.circle(36, 166, 3.6, '#46612A', 1, LEAF2)
    leaf(f, 58, 150, 100, 52, LEAF, 0.33, True)
    for t in (0.3, 0.5, 0.7):
        px, py = 58 + 100 * t * 0.62 * 0.98, 150 - 100 * t * 0.79 * 0.98
        f.line(px, py, px - 12, py - 6, '#2F5A24', 0.8).line(px, py, px + 10, py + 4, '#2F5A24', 0.8)
    leader(f, 100, 92, 126, 52, 'blade (lamina)', size=10.5)
    leader(f, 90, 110, 126, 80, 'midrib', size=10.5)
    leader(f, 106, 104, 126, 106, 'vein', size=10.5)
    leader(f, 46, 158, 96, 172, 'petiole', size=10.5)
    leader(f, 36, 166, 76, 196, 'axil + bud', size=10.5)
    leader(f, 30, 214, 58, 228, 'stem', size=10.5)
    # flower (section)
    cx, base = 268, 204
    f.line(cx, 246, cx, base, '#5E7F33', 3)
    for s in (-1, 1):
        f.path(f'M{cx + s * 18} {base} C{cx + s * 30} {base - 10} {cx + s * 26} {base - 20} {cx + s * 14} {base - 16} L{cx} {base - 4}Z', DARK, 1.1, LEAF)
        f.path(f'M{cx + s * 10} {base - 10} C{cx + s * 60} {base - 40} {cx + s * 60} {base - 110} {cx + s * 26} {base - 120} C{cx + s * 20} {base - 80} {cx + s * 14} {base - 40} {cx + s * 6} {base - 12}Z', PURPLE, 1.3, '#E7D5F2')
    f.ellipse(cx, base - 18, 9, 12, GREEN, 1.4, '#CFE6BF')
    f.circle(cx - 2, base - 20, 2, None, 0, GREEN).circle(cx + 3, base - 15, 2, None, 0, GREEN)
    f.line(cx, base - 30, cx, base - 84, GREEN, 2.2).ellipse(cx, base - 88, 6, 4, GREEN, 1.2, '#CFE6BF')
    for s in (-1, 1):
        f.path(f'M{cx + s * 6} {base - 14} C{cx + s * 16} {base - 40} {cx + s * 18} {base - 60} {cx + s * 18} {base - 70}', ORANGE, 1.6)
        f.ellipse(cx + s * 18, base - 74, 4, 7, ORANGE, 1.2, '#FCE3C4')
    leader(f, cx - 4, base - 89, 214, 44, 'stigma', size=10.5)
    leader(f, cx - 1, base - 56, 214, 140, 'style', size=10.5)
    leader(f, cx - 7, base - 16, 214, 224, 'ovary', size=10.5)
    leader(f, cx + 21, base - 78, 316, 44, 'anther', size=10.5)
    leader(f, cx + 17, base - 50, 316, 70, 'filament', size=10.5)
    leader(f, cx + 44, base - 64, 316, 110, 'petal', size=10.5)
    leader(f, cx + 24, base - 10, 316, 200, 'sepal', size=10.5)
    f.text(322, 140, 'stamen =', 10, ORANGE, 'start', False).text(322, 153, 'anther +', 10, ORANGE, 'start', False).text(322, 166, 'filament', 10, ORANGE, 'start', False)
    f.text(164, 244, 'pistil = stigma + style + ovary', 10, GREEN, 'start', False)
    return f


def f_photo():
    f = Fig(340, 250)
    ground(f, 196, c='#E9D9BF', h=54)
    sun(f, 36, 36, 16)
    for k in range(3):
        f.arrow(56 + k * 6, 54 + k * 10, 128 + k * 6, 96 + k * 10, '#D79A1E', 2, 8)
    f.text(10, 112, 'light energy', 11, '#B57D10', 'start')
    leaf(f, 150, 170, 150, 28, LEAF, 0.3, True)
    f.line(150, 196, 150, 170, '#5E7F33', 3)
    roots_fibrous(f, 150, 198, 34)
    tlines(f, 204, 144, ['chlorophyll', 'in the leaf'], 10.5, '#FFFFFF')
    f.arrow(320, 70, 270, 100, GREY, 2, 8)
    f.text(330, 62, 'CO₂ in', 11.5, INK, 'end')
    f.text(330, 76, '(stomata)', 10, GREY, 'end', False)
    f.arrow(230, 92, 262, 40, BLUE, 2, 8)
    f.text(266, 34, 'O₂ out', 11.5, BLUE, 'start')
    f.arrow(120, 232, 150, 206, WATER, 2, 7)
    f.text(10, 232, 'H₂O from soil', 11, BLUE, 'start')
    f.arrow(196, 160, 168, 186, ORANGE, 2, 7)
    f.text(186, 214, 'sugar moves to stem, roots,', 10.5, ORANGE, 'start')
    f.text(186, 228, 'grain (phloem)', 10.5, ORANGE, 'start')
    f.text(170, 248, 'CO₂ + H₂O + light  →  sugar + O₂', 12, GREEN)
    return f


def f_nutrients():
    f = Fig(340, 270)
    f.title('The 16 essential elements and where plants get them', 12)
    box(f, 6, 30, 160, 52, 'From AIR: carbon (C), oxygen (O)', BLUE, 11)
    box(f, 174, 30, 160, 52, 'From WATER: hydrogen (H), oxygen (O)', BLUE, 11)
    f.rect(6, 92, 328, 172, BROWN, 1.6, '#F6EEE3', 8)
    f.text(170, 110, 'From the SOIL (13 mineral elements)', 12, BROWN)
    box(f, 14, 120, 150, 56, 'Primary: N, P, K (needed most; in fertiliser)', RED, 11)
    box(f, 176, 120, 150, 56, 'Secondary: Ca, Mg, S', ORANGE, 11)
    box(f, 14, 186, 312, 50, 'Micronutrients (trace): Fe, Mn, Zn, Cu, B, Mo, Cl', GREEN, 11)
    f.text(170, 254, 'Macro = C, H, O + N, P, K + Ca, Mg, S (9)   Micro = 7', 10.5, INK)
    return f


def f_seed():
    f = Fig(340, 330)
    f.text(84, 16, 'Bean seed (dicot)', 12, GREEN).text(256, 16, 'Maize grain (monocot)', 12, ORANGE)
    cx, cy = 84, 64
    f.ellipse(cx, cy, 56, 36, '#7A4E2D', 2.4, '#EBD8B4')
    f.ellipse(cx, cy, 50, 30, '#B08A5A', 1, '#F5E8CC')
    f.path(f'M{cx - 34} {cy + 4} C{cx - 36} {cy - 10} {cx - 26} {cy - 18} {cx - 16} {cy - 12}', DARK, 2.4)
    f.path(f'M{cx - 34} {cy + 4} L{cx - 40} {cy + 16}', BROWN, 3)
    for k, (px, py, lab) in enumerate(((cx + 42, cy + 24, 'seed coat (testa)'), (cx + 18, cy + 8, 'cotyledon (food store)'),
                                         (cx - 18, cy - 12, 'plumule (young shoot)'), (cx - 40, cy + 16, 'radicle (young root)'))):
        ty = 118 + k * 15
        f.circle(px, py, 6.5, INK, 1, '#FFFFFF').text(px, py + 3.5, str(k + 1), 9, INK)
        f.circle(18, ty - 3.5, 6.5, INK, 1, '#FFFFFF').text(18, ty, str(k + 1), 9, INK).text(30, ty, lab, 10.5, INK, 'start')
    cx, cy = 256, 62
    f.path(f'M{cx - 28} {cy + 38} C{cx - 42} {cy} {cx - 28} {cy - 42} {cx} {cy - 44} C{cx + 28} {cy - 42} {cx + 42} {cy} {cx + 28} {cy + 38}Z', '#B07A2A', 2, '#F6E09A')
    f.path(f'M{cx - 18} {cy + 34} C{cx - 22} {cy + 6} {cx - 14} {cy - 12} {cx + 2} {cy - 6} C{cx + 6} {cy + 12} {cx + 2} {cy + 30} {cx - 6} {cy + 38}Z', ORANGE, 1.2, '#FBD38D')
    f.line(cx - 8, cy + 28, cx - 8, cy - 2, DARK, 2.2).line(cx - 8, cy + 28, cx - 10, cy + 36, BROWN, 2.4)
    for k, (px, py, lab) in enumerate(((cx + 20, cy - 20, 'endosperm (food store)'), (cx + 4, cy + 18, 'cotyledon (scutellum)'),
                                         (cx - 8, cy - 4, 'plumule'), (cx - 12, cy + 40, 'radicle'))):
        ty = 118 + k * 15
        f.circle(px, py, 6.5, INK, 1, '#FFFFFF').text(px, py + 3.5, str(k + 1), 9, INK)
        f.circle(190, ty - 3.5, 6.5, INK, 1, '#FFFFFF').text(190, ty, str(k + 1), 9, INK).text(202, ty, lab, 10.5, INK, 'start')
    ground(f, 252, c='#E9D9BF', h=78)
    f.text(84, 186, 'Epigeal', 12, GREEN).text(84, 200, 'cotyledons lifted above soil', 10, GREY, 'middle', False)
    f.text(84, 212, '(haricot bean, castor)', 10, GREY, 'middle', False)
    x = 84
    f.path(f'M{x} 306 C{x - 2} 280 {x + 2} 260 {x} 236', '#5E7F33', 2.6)
    f.ellipse(x - 10, 234, 10, 6, '#7A4E2D', 1.2, '#EBD8B4').ellipse(x + 10, 234, 10, 6, '#7A4E2D', 1.2, '#EBD8B4')
    leaf(f, x, 230, 16, 60, LEAF, 0.4)
    leaf(f, x, 230, 16, 120, LEAF, 0.4)
    roots_tap(f, x, 306, 18)
    f.text(256, 186, 'Hypogeal', 12, ORANGE).text(256, 200, 'cotyledons stay under soil', 10, GREY, 'middle', False)
    f.text(256, 212, '(faba bean, pea, maize, sorghum)', 10, GREY, 'middle', False)
    x = 256
    f.ellipse(x, 290, 12, 8, '#7A4E2D', 1.2, '#EBD8B4')
    f.path(f'M{x} 284 C{x - 2} 270 {x + 2} 256 {x} 230', '#5E7F33', 2.6)
    leaf(f, x, 232, 16, 60, LEAF, 0.4)
    leaf(f, x, 232, 16, 120, LEAF, 0.4)
    roots_tap(f, x, 296, 22)
    return f


def f_germtest():
    f = flow(['Count 100 seeds at random (do not pick out the bad ones)', 'Lay them on a damp paper towel, cover with a second towel',
              'Roll up, put in a closed plastic bag, keep at an even temperature', 'After the test period count seedlings with shoot > 4 cm and a strong root',
              'Germination % = germinated ÷ total × 100'], w=340, bh=38, gap=12, size=11)
    return f



def f_plough():
    f = Fig(340, 200)
    f.rect(0, 0, 340, 130, None, 0, '#F3F8FC')
    ground(f, 130, c='#C9A27A', h=70)
    for k in range(6):
        f.path(f'M0 {148 + k * 9} Q170 {142 + k * 9} 340 {148 + k * 9}', SOIL3, 0.9)
    f.path('M0 130 L340 130', SOIL3, 1.6)
    cow(f, 214, 130, 0.9, '#8B5A3C', face=1)
    cow(f, 244, 132, 0.9, '#5E3F2B', face=1)
    f.line(270, 88, 270, 82, '#6B4A2B', 3).line(190, 86, 296, 84, '#6B4A2B', 3.4)  # yoke
    maresha(f, 120, 132, 1.0, face=1)
    f.line(190, 104, 200, 86, '#6B4A2B', 2.4)
    person(f, 86, 132, 1.0, pose='plough')
    f.text(170, 16, 'Primary tillage with the maresha and a pair of oxen', 11.5, INK)
    leader(f, 128, 128, 120, 176, 'iron point (opens a furrow)', size=10.5, anchor='middle', dot=False)
    f.text(330, 194, 'ploughed 2–4 times on heavy soils', 10, '#FFFFFF', 'end', False)
    return f


def f_sowing():
    f = Fig(340, 190)
    titles = [('Broadcasting', 'seed scattered at random', ORANGE), ('Row planting', 'rows + spacing in the row', GREEN),
              ('Drilling', 'rows, seeds almost touching', BLUE)]
    import random
    rnd = random.Random(4)
    for k, (t, sub, c) in enumerate(titles):
        x0 = 6 + k * 112
        f.rect(x0, 34, 104, 110, c, 1.4, '#F6EEE3', 6)
        f.text(x0 + 52, 14, t, 11, c).text(x0 + 52, 27, sub, 8.2, GREY, 'middle', False)
        if k == 0:
            for _ in range(46):
                f.circle(x0 + 8 + rnd.random() * 88, 42 + rnd.random() * 94, 2.2, None, 0, BROWN)
        else:
            for r in range(4):
                xx = x0 + 16 + r * 24
                f.line(xx, 40, xx, 138, SOIL3, 0.8, dash='3 3')
                step = 16 if k == 1 else 5
                yy = 44
                while yy < 136:
                    f.circle(xx, yy, 2.2, None, 0, BROWN)
                    yy += step
    f.line(18 + 112, 152, 42 + 112, 152, INK, 1).text(30 + 112, 164, 'row spacing', 9.5, INK, 'middle', False)
    f.text(170, 176, 'Broadcasting needs the most seed;', 10, INK).text(170, 189, 'rows allow weeding and spraying between the lines', 10, INK)
    return f


def f_fertplace():
    f = Fig(340, 206)
    labs = [('Broadcast', 'on the surface, then mix in'), ('Row / band', 'in a line beside the seed row'), ('Sub-surface band', '5–20 cm deep, near the roots')]
    for k, (t, sub) in enumerate(labs):
        x0 = 6 + k * 112
        f.rect(x0, 66, 104, 100, None, 0, SOIL)
        f.line(x0, 66, x0 + 104, 66, SOIL3, 1.6)
        f.text(x0 + 52, 16, t, 11.5, INK)
        tlines(f, x0 + 52, 38, wrap(sub, 20), 9.5, GREY, 'middle', False)
        for sx in (x0 + 34, x0 + 74):
            f.path(f'M{sx} 66 L{sx} 56', '#5E7F33', 2.2)
            leaf(f, sx, 58, 9, 50, LEAF, 0.4, False)
            leaf(f, sx, 58, 9, 130, LEAF, 0.4, False)
            few_roots(f, sx, 68, 20)
        if k == 0:
            for j in range(18):
                f.circle(x0 + 6 + j * 5.4, 70 + (j % 3) * 2, 1.8, None, 0, '#FFFFFF')
        elif k == 1:
            for sx in (x0 + 34, x0 + 74):
                for j in range(4):
                    f.circle(sx + 12, 71 + j * 4, 1.8, None, 0, '#FFFFFF')
        else:
            for sx in (x0 + 34, x0 + 74):
                for j in range(5):
                    f.circle(sx + 8 + (j % 2) * 3, 108 + j * 3.4, 1.8, None, 0, '#FFFFFF')
            f.line(x0 + 98, 68, x0 + 98, 120, '#FFFFFF', 1).text(x0 + 96, 136, '5–20 cm', 9, '#FFFFFF', 'end', False)
    f.circle(14, 182, 3.6, INK, 0.8, '#FFFFFF')
    f.text(22, 186, '= fertiliser granules. Always cover fertiliser with soil;', 10, INK, 'start', False)
    f.text(22, 200, 'never let urea or DAP touch the seed (it burns it).', 10, INK, 'start', False)
    return f


def f_disease():
    f = Fig(340, 250)
    A, B, C = (170, 30), (40, 220), (300, 220)
    f.poly([A, B, C], GREEN, 3, '#EAF2DF')
    tlines(f, 170, 152, ['DISEASE', 'only where', 'all three meet'], 12.5, RED)
    box(f, 110, 6, 120, 34, 'Pathogen (fungus, bacterium, virus)', RED, 10.5)
    box(f, 4, 208, 130, 40, 'Susceptible host plant', GREEN, 10.5)
    box(f, 196, 208, 140, 40, 'Favourable environment (e.g. warm, humid)', BLUE, 10.5)
    f.text(70, 116, 'clean seed,', 10, GREY, 'middle', False).text(70, 129, 'rotation', 10, GREY, 'middle', False)
    f.text(272, 116, 'sowing date,', 10, GREY, 'middle', False).text(272, 129, 'drainage', 10, GREY, 'middle', False)
    f.text(170, 202, 'resistant variety', 10, GREY, 'middle', False)
    return f


def f_weeds():
    f = Fig(340, 206)
    f.text(56, 16, 'Broadleaf', 12, GREEN).text(170, 16, 'Grass', 12, ORANGE).text(284, 16, 'Sedge', 12, BLUE)
    ground(f, 150, c='#E9D9BF', h=16)
    x = 56
    f.line(x, 150, x, 70, '#5E7F33', 2.4)
    for yy, s in ((126, 1), (106, -1), (86, 1)):
        leaf(f, x, yy, 34, 90 - 55 * s, LEAF, 0.45)
    x = 170
    for a, L in ((60, 60), (80, 76), (100, 70), (120, 58), (140, 46)):
        grass_leaf(f, x, 150, L, a, 0.1, LEAF, 2.4)
    x = 284
    f.line(x, 150, x, 58, '#5E7F33', 2.6)
    for a in (60, 100, 140):
        grass_leaf(f, x, 150, 52, a, 0.05, LEAF, 2.2)
    for a in (40, 90, 140):
        t = math.radians(a)
        f.line(x, 58, x + 22 * math.cos(t), 58 - 22 * math.sin(t), '#5E7F33', 1.4)
    f.circle(x, 56, 5, '#7A4E2D', 1, '#A3784B')
    f.poly([(x - 8, 102), (x + 8, 102), (x, 88)], INK, 1.2, '#FFFFFF')
    f.text(x + 14, 100, 'triangle', 9.5, INK, 'start', False)
    f.text(56, 182, 'wide leaves, net veins', 10, INK, 'middle', False).text(56, 196, 'e.g. Amaranthus', 10, GREY, 'middle', False)
    f.text(170, 182, 'narrow leaves, round', 10, INK, 'middle', False).text(170, 196, 'hollow stem, e.g. Cynodon', 10, GREY, 'middle', False)
    f.text(284, 182, 'solid 3-sided stem', 10, INK, 'middle', False).text(284, 196, 'e.g. Cyperus', 10, GREY, 'middle', False)
    return f


def f_postharvest_grain():
    f = Fig(340, 270)
    f.title('Safe moisture for storing grain (Table 3.9)', 12)
    data = [('Wheat', 12), ('Barley', 13), ('Sorghum', 12), ('Maize', 13), ('Soybean', 11), ('Rice', 12)]
    for k, (c, m) in enumerate(data):
        y = 30 + k * 26
        f.text(70, y + 15, c, 11, INK, 'end')
        f.rect(76, y + 3, m * 14, 16, None, 0, STRAW, 3)
        f.text(80 + m * 14, y + 15, f'{m} %', 11, INK, 'start')
    f.text(170, 200, 'maximum moisture for safe storage; wetter grain moulds and heats', 9.5, RED, 'middle', False)
    box(f, 6, 214, 328, 50, 'Store pests multiply fastest at 28–33 °C and 60–80 % relative humidity: keep grain dry, cool and sealed.', ORANGE, 10.5)
    return f


def f_cropping():
    f = Fig(340, 300)
    panels = [('Mono-cropping', 'same crop every year'), ('Inter-cropping', '2 rows sorghum : 1 row cowpea'),
              ('Alley cropping', 'crops between pruned hedgerows'), ('Crop rotation', 'different crops in sequence')]
    for k, (t, sub) in enumerate(panels):
        x0, y0 = 6 + (k % 2) * 168, 6 + (k // 2) * 148
        f.rect(x0, y0, 160, 140, GREY, 1, '#FBF8F3', 6)
        f.text(x0 + 80, y0 + 16, t, 11.5, INK).text(x0 + 80, y0 + 29, sub, 9.5, GREY, 'middle', False)
        ground(f, y0 + 116, x0 + 4, x0 + 156, '#E9D9BF', 18)
        if k == 0:
            for j in range(6):
                mini_cereal(f, x0 + 22 + j * 23, y0 + 116, 50)
        elif k == 1:
            for j in range(6):
                xx = x0 + 22 + j * 23
                if j % 3 == 2:
                    for d in (-6, 6):
                        leaf(f, xx, y0 + 112, 16, 90 + d * 6, LEAF2, 0.45)
                    f.line(xx, y0 + 116, xx, y0 + 104, '#5E7F33', 2)
                else:
                    mini_cereal(f, xx, y0 + 116, 50)
        elif k == 2:
            for xx in (x0 + 24, x0 + 136):
                tree(f, xx, y0 + 116, 70, DARK)
            for j in range(4):
                mini_cereal(f, x0 + 52 + j * 19, y0 + 116, 42)
        else:
            cx, cy = x0 + 80, y0 + 76
            items = [('sorghum', ORANGE), ('chickpea', GREEN), ('barley', BLUE), ('lentil', PURPLE)]
            for j, (nm, c) in enumerate(items):
                a = math.radians(90 - j * 90)
                px, py = cx + 50 * math.cos(a), cy - 32 * math.sin(a)
                box(f, px - 30, py - 11, 60, 22, nm, c, 9.5)
            f.curve_arrow(cx + 34, cy - 36, cx + 52, cy - 14, -8, GREY, 1.6, 6)
            f.curve_arrow(cx + 52, cy + 14, cx + 34, cy + 36, -8, GREY, 1.6, 6)
            f.curve_arrow(cx - 34, cy + 36, cx - 52, cy + 14, -8, GREY, 1.6, 6)
            f.curve_arrow(cx - 52, cy - 14, cx - 34, cy - 36, -8, GREY, 1.6, 6)
            f.rect(x0 + 4, y0 + 116, 152, 18, None, 0, '#FBF8F3')
            f.text(x0 + 80, y0 + 130, 'cereal → pulse → cereal → pulse', 9.5, GREEN)
    return f



def f_hortsystems():
    f = Fig(340, 250)
    titles = [('Open field', 'natural soil and climate'), ('Greenhouse', 'climate controlled'),
              ('Low tunnel', 'partly controlled'), ('Hydroponics', 'no soil: roots in nutrient solution')]
    for k, (t, sub) in enumerate(titles):
        x0, y0 = 6 + (k % 2) * 168, 6 + (k // 2) * 122
        f.rect(x0, y0, 160, 116, GREY, 1, '#FBF8F3', 6)
        f.text(x0 + 80, y0 + 16, t, 11.5, INK).text(x0 + 80, y0 + 29, sub, 9.5, GREY, 'middle', False)
        gy = y0 + 98
        if k != 3:
            ground(f, gy, x0 + 4, x0 + 156, '#E9D9BF', 14)
        if k == 0:
            sun(f, x0 + 136, y0 + 46, 9)
            for j in range(5):
                xx = x0 + 22 + j * 26
                f.line(xx, gy, xx, gy - 18, '#5E7F33', 2)
                leaf(f, xx, gy - 12, 14, 40, LEAF, 0.4, False)
                leaf(f, xx, gy - 12, 14, 140, LEAF, 0.4, False)
                f.circle(xx + 5, gy - 22, 4, None, 0, RED)
        elif k == 1:
            f.path(f'M{x0 + 14} {gy} L{x0 + 14} {gy - 36} L{x0 + 80} {gy - 60} L{x0 + 146} {gy - 36} L{x0 + 146} {gy}', BLUE, 1.8, '#EAF3FA')
            for xx in (x0 + 47, x0 + 80, x0 + 113):
                f.line(xx, gy, xx, gy - 48 + abs(xx - x0 - 80) * 0.36, BLUE, 0.8)
            for j in range(4):
                xx = x0 + 34 + j * 30
                f.line(xx, gy, xx, gy - 26, '#5E7F33', 2)
                leaf(f, xx, gy - 16, 12, 40, LEAF, 0.4, False)
                leaf(f, xx, gy - 22, 12, 140, LEAF, 0.4, False)
        elif k == 2:
            f.path(f'M{x0 + 16} {gy} C{x0 + 16} {gy - 44} {x0 + 144} {gy - 44} {x0 + 144} {gy}', BLUE, 1.8, '#EAF3FA')
            for xx in (x0 + 40, x0 + 80, x0 + 120):
                f.path(f'M{xx - 8} {gy} C{xx - 8} {gy - 14} {xx + 8} {gy - 14} {xx + 8} {gy}', None, 0, LEAF)
            f.text(x0 + 80, gy - 40, 'plastic over hoops', 9.5, BLUE, 'middle', False)
        else:
            f.rect(x0 + 14, gy - 26, 132, 26, BLUE, 1.6, '#D4E7F6', 3)
            f.line(x0 + 14, gy - 26, x0 + 146, gy - 26, BLUE, 1.6)
            for j in range(4):
                xx = x0 + 32 + j * 32
                f.rect(xx - 6, gy - 32, 12, 8, GREY, 1, '#FFFFFF', 2)
                f.path(f'M{xx} {gy - 24} L{xx - 4} {gy - 6} M{xx} {gy - 24} L{xx + 3} {gy - 4} M{xx} {gy - 24} L{xx} {gy - 3}', BROWN, 1)
                leaf(f, xx, gy - 32, 18, 60, LEAF2, 0.45, False)
                leaf(f, xx, gy - 32, 18, 120, LEAF2, 0.45, False)
            f.text(x0 + 80, gy + 12, 'lettuce in a nutrient-solution tank', 9.5, BLUE, 'middle', False)
    return f


def f_beds():
    f = Fig(340, 200)
    f.text(86, 16, 'Raised bed', 12, BLUE).text(86, 30, 'wet areas: drains water', 10, GREY, 'middle', False)
    f.text(254, 16, 'Sunken bed', 12, ORANGE).text(254, 30, 'dry areas: holds water', 10, GREY, 'middle', False)
    gy = 120
    f.rect(0, gy, 340, 80, None, 0, SOIL)
    f.line(0, gy, 340, gy, SOIL3, 1.6)
    # raised
    f.path(f'M20 {gy} L30 {gy - 30} L142 {gy - 30} L152 {gy}Z', SOIL3, 1.4, SOIL2)
    for j in range(5):
        xx = 44 + j * 22
        f.line(xx, gy - 30, xx, gy - 44, '#5E7F33', 1.8)
        leaf(f, xx, gy - 40, 9, 45, LEAF, 0.45, False)
        leaf(f, xx, gy - 40, 9, 135, LEAF, 0.45, False)
    f.line(160, gy, 160, gy - 30, INK, 1).line(156, gy - 30, 164, gy - 30, INK, 1).line(156, gy, 164, gy, INK, 1)
    f.text(166, gy - 12, '15–20 cm', 9.5, INK, 'start', False)
    for j in range(4):
        f.arrow(20 + j * 40, gy + 10, 20 + j * 40 + (8 if j < 2 else -8), gy + 50, WATER, 1.4, 6)
    # sunken
    f.rect(190, gy - 1, 130, 22, None, 0, '#FFFFFF')
    f.path(f'M190 {gy} L198 {gy + 20} L312 {gy + 20} L320 {gy}', SOIL3, 1.4)
    f.rect(198, gy + 13, 114, 7, None, 0, WATER)
    for j in range(5):
        xx = 212 + j * 22
        f.line(xx, gy + 13, xx, gy - 2, '#5E7F33', 1.8)
        leaf(f, xx, gy + 2, 9, 45, LEAF, 0.45, False)
        leaf(f, xx, gy + 2, 9, 135, LEAF, 0.45, False)
    f.rect(190, gy + 20, 130, 60, None, 0, SOIL)
    f.line(326, gy, 326, gy + 20, INK, 1).text(330, gy + 38, '10–15 cm', 9.5, INK, 'end', False)
    f.text(170, 192, 'beds 1.0–1.2 m wide so you can reach the middle from the path', 10, '#FFFFFF')
    return f


def f_tbud():
    f = Fig(340, 230)
    f.title('Shield (T) budding, step by step', 12.5)
    xs = [44, 128, 212, 296]
    caps = ['1 Cut a T in the stock bark: 3–4 cm down, 1–2 cm across', '2 Slice a bud shield from the scion wood',
            '3 Lift the bark flaps and slide the shield in', '4 Wrap with tape, bud left uncovered']
    for k, x in enumerate(xs):
        f.g(' '.join(f'k{j}' for j in range(k + 1, 5)))
        if k != 1:
            f.rect(x - 9, 40, 18, 120, '#6B4A2B', 1.4, '#B98A5E', 6)
        if k == 0:
            f.line(x, 72, x, 106, INK, 1.8).line(x - 6, 72, x + 6, 72, INK, 1.8)
        elif k == 1:
            f.rect(x - 6, 36, 12, 128, '#6B4A2B', 1.4, '#B98A5E', 5)
            f.path(f'M{x + 6} 76 C{x + 14} 86 {x + 14} 104 {x + 6} 114', INK, 1.4, '#C9DBA4')
            f.path(f'M{x + 6} 92 L{x + 12} 88 L{x + 10} 96Z', DARK, 1, LEAF)
            f.arrow(x + 16, 96, x + 34, 96, GREY, 1.4, 6)
        elif k == 2:
            f.path(f'M{x} 72 L{x - 8} 82 L{x - 8} 106 L{x} 106Z M{x} 72 L{x + 8} 82 L{x + 8} 106 L{x} 106Z', '#6B4A2B', 1.2, '#D9B88E')
            f.path(f'M{x - 4} 80 L{x + 4} 80 L{x + 4} 104 L{x - 4} 104Z', DARK, 1, '#C9DBA4')
            f.circle(x, 90, 2.4, None, 0, DARK)
            f.line(x - 6, 72, x + 6, 72, INK, 1.6)
        else:
            for j in range(7):
                yy = 70 + j * 6
                if 86 <= yy <= 94:
                    continue
                f.line(x - 10, yy, x + 10, yy + 3, '#3E8E5E', 2.4)
            f.circle(x, 90, 3, None, 0, DARK)
            leaf(f, x, 90, 12, 40, LEAF, 0.4, False)
        f.end()
        tlines(f, x, 196, wrap(caps[k], 15), 9.5, INK, 'middle', False, 11.5)
    f.text(170, 228, 'Used for citrus and many tropical fruit trees', 10, GREEN)
    return f


def f_whip():
    f = Fig(340, 220)
    f.title('Whip (tongue) graft: match the cambium', 12.5)
    x = 70
    f.path(f'M{x - 8} 200 L{x - 8} 110 L{x + 8} 80 L{x + 8} 200Z', '#6B4A2B', 1.4, '#B98A5E')
    f.line(x - 2, 104, x + 4, 112, INK, 1.4)
    f.text(x, 214, 'stock (root part)', 10, INK)
    x2 = 128
    f.path(f'M{x2 - 8} 40 L{x2 - 8} 120 L{x2 + 8} 90 L{x2 + 8} 40Z', '#6B4A2B', 1.4, '#C9A678')
    f.line(x2 - 4, 108, x2 + 2, 100, INK, 1.4)
    for yy in (52, 72):
        f.path(f'M{x2 + 8} {yy} L{x2 + 14} {yy - 4} L{x2 + 8} {yy - 8}', DARK, 1.2, LEAF)
    f.text(x2, 30, 'scion: 2–3 buds', 10, INK)
    f.arrow(156, 120, 196, 120, GREY, 2, 8)
    x3 = 250
    f.path(f'M{x3 - 8} 200 L{x3 - 8} 40 L{x3 + 8} 40 L{x3 + 8} 200Z', '#6B4A2B', 1.4, '#B98A5E')
    f.path(f'M{x3 - 8} 140 L{x3 + 8} 110', INK, 1.2)
    for j in range(6):
        yy = 104 + j * 7
        f.line(x3 - 11, yy, x3 + 11, yy + 3, '#3E8E5E', 2.4)
    for yy in (52, 72):
        f.path(f'M{x3 + 8} {yy} L{x3 + 14} {yy - 4} L{x3 + 8} {yy - 8}', DARK, 1.2, LEAF)
    leader(f, x3 + 11, 126, 300, 150, 'tape', size=10)
    leader(f, x3 - 8, 120, 196, 168, 'cambium meets', size=10)
    f.text(x3, 214, 'same 6–12 mm thickness', 10, INK)
    return f


def f_layering():
    f = Fig(340, 220)
    f.text(86, 16, 'Air layering', 12, GREEN).text(254, 16, 'Simple layering', 12, ORANGE)
    # air layer
    f.path('M30 210 L36 120 L40 120 L44 210Z', None, 0, '#6B4A2B')
    f.path('M38 130 C70 112 110 96 150 70', '#6B4A2B', 4)
    for (px, py) in ((150, 70), (128, 82), (140, 66)):
        leaf(f, px, py, 18, 60, LEAF, 0.4, False)
        leaf(f, px, py, 16, 150, LEAF, 0.4, False)
    f.ellipse(96, 98, 18, 13, GREY, 1.4, '#D9E6F2')
    f.line(80, 92, 80, 104, INK, 1.4).line(112, 92, 112, 104, INK, 1.4)
    f.line(96, 111, 100, 136, GREY, 1.2)
    tlines(f, 116, 150, ['bark ring removed, moist', 'moss/compost + plastic wrap'], 9.5, INK)
    f.text(116, 178, 'cut free once roots show', 9.5, GREY, 'middle', False).text(116, 192, '(mango, croton)', 9.5, GREY, 'middle', False)
    # simple layer
    ground(f, 150, 176, 340, '#E9D9BF', 70)
    f.path('M200 150 L203 70 L207 70 L210 150Z', None, 0, '#6B4A2B')
    f.path('M206 100 C240 120 250 170 270 168 C290 166 300 140 312 110', '#6B4A2B', 3)
    leaf(f, 312, 110, 16, 60, LEAF, 0.4, False)
    leaf(f, 312, 110, 14, 140, LEAF, 0.4, False)
    leaf(f, 205, 70, 16, 60, LEAF, 0.4, False)
    leaf(f, 205, 70, 16, 120, LEAF, 0.4, False)
    roots_fibrous(f, 270, 170, 18)
    f.path('M262 154 L270 162 L278 154', INK, 1.4)
    f.text(258, 196, 'buried, wounded part roots', 9.5, INK)
    f.text(334, 140, 'tip stays out', 9.5, GREY, 'end', False)
    f.text(258, 212, '(climbing rose, jasmine)', 9.5, GREY, 'middle', False)
    return f


def f_garden():
    f = Fig(340, 258)
    f.title('School garden plan (plots 6 m wide)', 12.5)
    f.rect(6, 28, 328, 190, GREEN, 2, '#EAF2DF', 4)
    f.text(334, 256, 'fence/hedge all round', 9.5, GREEN, 'end', False)
    cols = [('Plot A', ORANGE), ('Plot B', BLUE), ('Plot C', PURPLE)]
    for k, (nm, c) in enumerate(cols):
        x0 = 16 + k * 106
        f.rect(x0, 38, 96, 170, c, 1.4, '#FFFFFF', 3)
        f.text(x0 + 48, 52, nm, 11, c)
        for j in range(4):
            xx = x0 + 6 + j * 23
            f.rect(xx, 60, 16, 140, None, 0, SOIL)
    f.line(16 + 6, 204, 16 + 22, 204, INK, 1).text(14, 244, 'bed 1.2 m', 9.5, INK, 'start', False)
    f.line(22, 204, 22, 236, GREY, 0.8)
    f.text(88, 244, 'path 60 cm', 9.5, INK, 'start', False).line(16 + 25, 204, 100, 236, GREY, 0.8)
    f.text(176, 244, 'grass path 1 m', 9.5, INK, 'start', False).line(117, 204, 190, 236, GREY, 0.8)
    return f


def f_doubledig():
    f = Fig(340, 210)
    f.title('Double digging: the bed is loosened 45–60 cm deep', 12)
    top, mid, bot = 50, 100, 150
    f.rect(0, top, 340, 160, None, 0, SOIL3)
    f.rect(0, top, 340, mid - top, None, 0, SOIL)
    f.line(0, top, 340, top, '#5A3A20', 1.6)
    for k in range(4):
        x0 = 20 + k * 76
        if k == 1:
            f.rect(x0, top, 70, bot - top, None, 0, '#FFFFFF')
            f.rect(x0, mid, 70, bot - mid, None, 0, '#C9A27A')
            for j in range(6):
                f.path(f'M{x0 + 6 + j * 11} {mid + 10} l4 -6 l4 6', '#5A3A20', 1)
            f.rect(x0, mid - 6, 70, 6, None, 0, '#6E4B2A')
            tlines(f, x0 + 35, top + 20, ['open', 'trench'], 10, INK)
        elif k == 0:
            f.rect(x0, top, 70, bot - top, None, 0, '#C9A27A')
            tlines(f, x0 + 35, top + 50, ['finished:', 'loose, manured'], 9.5, '#FFFFFF')
    f.curve_arrow(225, 70, 140, 70, 18, INK, 1.8, 7)
    f.text(232, 76, 'next topsoil', 9.5, INK, 'start', False)
    leader(f, 131, mid - 3, 96, 168, 'manure/compost on subsoil', size=9.5, anchor='middle', dot=False)
    leader(f, 160, mid + 30, 250, 168, 'subsoil loosened 15–30 cm', size=9.5, anchor='middle', dot=False)
    f.line(334, top, 334, mid, INK, 1).text(330, 80, '28–30 cm', 9, '#FFFFFF', 'end', False)
    f.text(170, 190, 'Topsoil of trench 1 fills the last trench.', 9.5, '#FFFFFF').text(170, 204, 'Repeat every 2–4 years (medium and clay soils).', 9.5, '#FFFFFF')
    return f


def f_pit():
    f = Fig(340, 220)
    f.title('Planting a fruit tree seedling in a pit', 12.5)
    ground(f, 70, c=SOIL, h=150)
    for k, (t, c) in enumerate((('1 Dig 60 × 60 × 60 cm; keep topsoil and subsoil apart', ORANGE),
                                ('2 Mix topsoil with manure/compost; refill', GREEN), ('3 Plant at nursery depth, firm, water, mulch', BLUE))):
        x0 = 10 + k * 110
        f.rect(x0 + 22, 70, 66, 70, None, 0, '#FFFFFF' if k == 0 else ('#9C6B43' if k == 1 else '#9C6B43'))
        if k == 0:
            f.path(f'M{x0 + 2} 70 Q{x0 + 12} 52 {x0 + 22} 70Z', None, 0, '#6E4B2A')
            f.path(f'M{x0 + 88} 70 Q{x0 + 98} 52 {x0 + 108} 70Z', None, 0, '#C9A27A')
        if k >= 1:
            for j in range(10):
                f.circle(x0 + 28 + (j * 13) % 60, 80 + (j * 7) % 54, 2, None, 0, '#4A2E18')
        if k == 2:
            f.line(x0 + 55, 70, x0 + 55, 30, '#6B4A2B', 2.4)
            leaf(f, x0 + 55, 36, 14, 50, LEAF, 0.4, False)
            leaf(f, x0 + 55, 44, 14, 140, LEAF, 0.4, False)
            roots_fibrous(f, x0 + 55, 72, 22)
            f.path(f'M{x0 + 26} 70 Q{x0 + 55} 62 {x0 + 84} 70', STRAW, 4)
        tlines(f, x0 + 55, 178, wrap(t, 18), 9.5, '#FFFFFF', 'middle', True, 11.5)
    f.text(170, 214, 'hardpan soil: dig 100 × 100 × 100 cm', 9.5, '#FFFFFF')
    return f


def f_postharvest():
    f = hflow(['Harvest at the right stage, cool hours', 'Clean', 'Sort: remove damaged', 'Grade by size', 'Pack: crates for tomato, sacks for potato',
               'Transport in shade, quickly'], w=340, rows=2, bh=52, size=10.5, title='Post-harvest handling of fruit and vegetables')
    return f



DIAGRAMS = {
    'plant': (f_plant(), 'Parts of a flowering plant: shoot and root systems (Figure 3.1)', 103),
    'monodicot': (f_monodicot(), 'Monocots and dicots compared (Table 3.1)', 102),
    'roots': (f_roots(), 'Types of root system (Figure 3.2)', 105),
    'leafflower': (f_leafflower(), 'Parts of a leaf and of a flower (Figure 3.3)', 106),
    'photo': (f_photo(), 'Photosynthesis: inputs and products (Figure 3.4)', 106),
    'nutrients': (f_nutrients(), 'The 16 essential elements and their sources (Figure 3.5)', 108),
    'seed': (f_seed(), 'Seed structure and the two types of germination (Figure 3.6)', 118),
    'germtest': (f_germtest(), 'The rolled-towel germination test (Assignment 3.5)', 119),
    'plough': (f_plough(), 'Primary tillage with the traditional ox-drawn maresha (Figure 3.7)', 129),
    'sowing': (f_sowing(), 'Broadcasting, row planting and drilling seen from above', 136),
    'fertplace': (f_fertplace(), 'Methods of fertiliser application', 134),
    'disease': (f_disease(), 'The disease triangle (Figure 3.11)', 141),
    'weeds': (f_weeds(), 'Weeds grouped by leaf form: broadleaves, grasses and sedges (Figure 3.8)', 138),
    'grainstore': (f_postharvest_grain(), 'Maximum moisture content for safe storage of grain (Table 3.9)', 146),
    'cropping': (f_cropping(), 'Cropping systems: mono-cropping, inter-cropping, alley cropping and rotation (Figures 3.15, 3.16)', 150),
    'hortsys': (f_hortsystems(), 'Horticultural production systems (Figures 3.20–3.23)', 156),
    'beds': (f_beds(), 'Raised and sunken nursery beds in cross-section (Figure 3.25)', 160),
    'tbud': (f_tbud(), 'Shield (T) budding (Figure 3.30)', 168),
    'whip': (f_whip(), 'Whip-and-tongue grafting (Figure 3.31)', 169),
    'layering': (f_layering(), 'Air layering and simple layering (Figures 3.38, 3.39)', 175),
    'garden': (f_garden(), 'A school garden plan with beds and paths (Figure 3.43)', 181),
    'doubledig': (f_doubledig(), 'The double-digging technique in cross-section', 183),
    'pit': (f_pit(), 'Pit preparation and planting of a tree seedling (Figure 3.44)', 184),
    'postharvest': (f_postharvest(), 'Post-harvest handling chain (Figures 3.45, 3.46)', 187),
}

# ------------------------------------------------------------------ 3.1 general principles
L1 = [
    T('intro', 'What a crop is and how a crop plant is built', 101,
      'A **crop** is any plant that people grow on purpose and harvest for food, feed, fibre, oil, medicine or beauty. Sorghum in the Gash-Barka, barley and taff around Mendefera, tomatoes in Keren gardens and roses in Asmara are all crops.',
      'Cultivated crops are divided into **field crops** (cereals, pulses, oil, fibre, root and forage crops grown on large areas) and **horticultural crops** (fruits, vegetables, flowers, spices, grown intensively). This unit covers both.',
      'Nearly all crops are **flowering plants (angiosperms)**. These fall into two groups, **monocots** and **dicots**, and the group tells you a lot about how the crop grows, how it is weeded and how it is propagated.'),
    T('=agri11-u3-c01', '3.1.1 Crops: monocots and dicots', 101,
      '**Monocots** have **one** seed leaf (**cotyledon**) in the seed. Most cereals are monocots: **sorghum, maize, barley, wheat, taff, pearl and finger millet**. Onion and banana are monocot horticultural crops.',
      '**Dicots** have **two** cotyledons. They include the pulses (**faba bean, chickpea, field pea, lentil, haricot bean**) and most vegetables and fruits (tomato, pepper, pumpkin, citrus, mango).',
      'Both groups have the same basic plan: a stem with **nodes** (where leaves join) and **internodes** (the stem between two nodes), leaves, buds, roots and flowers.',
      '**Careful:** there are exceptions to every single feature in the table below, so a botanist always looks at **several** features together before calling a plant a monocot or a dicot.'),
    DG('md-fig', 'Monocot or dicot? Five features to look at', 102, 'monodicot',
       'Hold a sorghum leaf to the light: the veins run side by side (parallel). A bean leaf shows a branching net of veins.'),
    TB('md-tb', 'Monocots versus dicots (Table 3.1)', 102, ['Feature', 'Monocot', 'Dicot'],
       [['Cotyledons in the embryo', 'One', 'Two'],
        ['Pollen', 'One furrow or pore', 'Three furrows or pores'],
        ['Flower parts', 'In threes or multiples of three', 'In fours or fives'],
        ['Main leaf veins', 'Parallel', 'Netted (reticulate)'],
        ['Vascular bundles in the stem', 'Scattered', 'In a ring'],
        ['Roots', 'Adventitious (fibrous), from the stem base', 'Develop from the radicle (tap root)'],
        ['Seed', 'Cannot be split into two halves', 'Splits into two equal halves'],
        ['Eritrean examples', 'Sorghum, taff, barley, maize, onion', 'Faba bean, chickpea, tomato, pumpkin']], layout='compare'),
    T('parts', 'Plant parts: reproductive and vegetative', 102,
      'The parts of a plant form two groups:',
      '- **Sexual reproductive parts:** flower buds, **flowers**, **fruits** and **seeds**. They make the next generation by seed.',
      '- **Vegetative parts:** **roots, stems, leaves** and **leaf buds**. They keep the plant alive and can also be used for **vegetative (asexual) propagation**, for example a stem cutting of grape or a potato tuber.',
      'A plant above ground is called the **shoot system** (stem, leaves, buds, flowers, fruits); below ground is the **root system**.'),
    DG('plant-fig', 'Parts of a flowering plant', 103, 'plant',
       'Faba bean: tap root with lateral roots, a stem divided into nodes and internodes, net-veined leaves, flowers and pods.'),
    T('stem', 'The stem', 103,
      'The stem **supports** the leaves, buds and flowers and **carries (translocates)** water, minerals and sugars between the roots and the leaves.',
      'Inside the stem are three main tissues:',
      '- **Xylem** carries water and dissolved minerals **up** from the roots to the leaves.',
      '- **Phloem** carries sugars made in the leaves to where they are used or stored (roots, growing tips, grain, fruit). Phloem flow can go up or down.',
      '- **Cambium** is a thin layer of dividing cells between xylem and phloem; it makes the stem thicker, and it is the tissue that must touch in **grafting**.',
      'Xylem and phloem together form the **vascular system**.'),
    TB('modstem', 'Modified stems and where you meet them', 103, ['Type', 'Position', 'What it is', 'Example'],
       [['Stolon (runner)', 'Above ground', 'Stem creeping on the surface, roots at nodes', 'Strawberry, Bermuda grass'],
        ['Crown', 'At ground level', 'Short compressed stem with buds', 'Strawberry, asparagus'],
        ['Spur', 'Above ground', 'Short fruiting shoot', 'Apple, pear'],
        ['Bulb', 'Below ground', 'Short stem with fleshy storage leaves', 'Onion, garlic'],
        ['Corm', 'Below ground', 'Short, solid, swollen stem base', 'Taro, gladiolus'],
        ['Rhizome', 'Below ground', 'Horizontal underground stem', 'Ginger, canna, couch grass'],
        ['Tuber', 'Below ground', 'Swollen tip of an underground stem, with "eyes" (buds)', 'Potato']], layout='cards'),
    RM('stem-err', 'Correction: ginger is a rhizome, not a corm', 103,
       'The textbook lists ginger as a corm. **Ginger is a rhizome** (a branching horizontal underground stem). Good corm examples are **taro** and **gladiolus**.',
       'How to tell them apart: a **potato tuber** has "eyes" (buds) spread all over it; an **onion bulb** is made of leaf layers; a **corm** is solid stem tissue; a **rhizome** grows sideways and branches.'),
    T('roots', 'Roots', 104,
      'Roots grow from the lower part of the plant or of a cutting. A root has a **root cap** at its tip, has **no nodes**, and **never bears leaves or flowers directly**.',
      '**Functions of roots:**',
      '- absorb water and mineral nutrients;',
      '- anchor the plant in the soil;',
      '- give physical support to the stem;',
      '- store food (carrot, sweet potato, beetroot);',
      '- propagate some plants (sweet potato, some fruit rootstocks).'),
    DG('roots-fig', 'Root systems', 105, 'roots',
       'Tap roots go deep for water (good for faba bean and chickpea on the residual moisture after the rains). Fibrous roots spread wide near the surface and bind the soil against erosion.'),
    TB('roots-tb', 'Types of roots compared', 104, ['Root type', 'How it forms', 'Strength', 'Example'],
       [['Primary root (radicle)', 'Grows from the lower end of the embryo', 'First root of every seedling', 'All seedlings'],
        ['Tap root', 'Primary root keeps growing downwards', 'Deep water, anchorage, storage', 'Carrot, faba bean, chickpea'],
        ['Lateral (secondary)', 'Branches from another root', 'Spreads the absorbing area', 'Side roots of beans'],
        ['Fibrous', 'Primary root stops; many roots from the stem base', 'Shallow and wide; best absorption; holds soil', 'Sorghum, taff, barley, grasses'],
        ['Aerial / prop roots', 'Grow from the stem above soil', 'Extra support (and moisture uptake in some plants)', 'Maize brace roots']], layout='cards'),
    T('leaves', 'Leaves', 104,
      'The main job of the leaf is **photosynthesis**: absorbing sunlight to make sugar. Leaves are flat and thin to catch as much light as possible. They are also where **gas exchange** (CO₂ in, O₂ and water vapour out, through **stomata**) happens, and some leaves store food (onion, cabbage).',
      'The leaf blade is held on the stem by a stalk called the **petiole**. The small angle between the petiole and the stem is the **leaf axil**; a bud (active or dormant) usually sits in the axil.',
      '**Venation:** monocots (sorghum, maize, wheat) have **parallel veins**; dicots (faba bean, field pea) have **netted veins** that branch from a midrib.'),
    T('flower', 'Flowers', 105,
      'The flower is the organ of **sexual reproduction**: it produces fruits and seeds. Its colour and scent are not there to please people; they attract **pollinators** (bees, other insects, birds) that carry pollen.',
      '- **Sepals** (green) protect the bud; **petals** (coloured) attract pollinators.',
      '- **Stamen** = male part: **anther** (makes pollen) on a **filament**.',
      '- **Pistil** = female part: **stigma** (receives pollen), **style**, and **ovary** containing **ovules**, which become seeds after fertilisation; the ovary becomes the **fruit**.',
      'Wind-pollinated crops such as maize and sorghum have small dull flowers and lots of light pollen.'),
    DG('lf-fig', 'Parts of a leaf and of a flower', 106, 'leafflower'),
    T('=agri11-u3-c02', '3.1.2 Photosynthesis', 106,
      'In **photosynthesis**, green plants change **light energy** from the sun into **chemical energy** stored in sugar. The green pigment **chlorophyll** in the leaves absorbs the light, mostly the **violet-blue** and **red** parts of the spectrum (green light is reflected, which is why leaves look green).',
      'Word equation: **carbon dioxide + water + light energy → sugar + oxygen** (with chlorophyll).',
      'Balanced chemical equation: **6 CO₂ + 6 H₂O → C₆H₁₂O₆ (glucose) + 6 O₂**, driven by light energy absorbed by chlorophyll.',
      '- CO₂ enters the leaf through the stomata; water comes from the soil through the roots and xylem.',
      '- Sugar moves in the phloem and is turned into starch (grain, tubers), cellulose (straw) and oil (sesame).',
      '- Only about **1 %** of the light energy that reaches a crop ends up as chemical energy, so good leaf cover matters.'),
    DG('photo-fig', 'Photosynthesis in a leaf', 106, 'photo'),
    T('light-demo', 'Demonstration: light is needed for photosynthesis', 107,
      '1. Keep a potted plant in the **dark for three days** so the leaves use up their starch.',
      '2. **Cover part of some leaves** with a light screen (black paper or foil).',
      '3. Put the plant in **sunlight** for a few hours.',
      '4. Test the leaves for **starch** with **iodine solution** (first boil the leaf briefly and remove the chlorophyll in warm alcohol, so the colour shows).',
      '**Result:** uncovered parts turn **blue-black** (starch was made); covered parts stay **brown** (no starch). **Conclusion:** without light there is no photosynthesis.'),
    T('=agri11-u3-c03', '3.1.3 Soil, water, atmosphere and plant', 107,
      'Soil keeps plants alive by giving **nutrients, water, air and support (anchorage)**. More than **80 %** of the essential nutrients come from the soil. Unwise use (no rest, no manure, erosion on slopes) lowers soil productivity.',
      '**Sixteen elements** are essential for healthy growth. Carbon (C) and oxygen (O) come from the **air**, hydrogen (H) and oxygen from **water**, and the other **13** from the **soil**.',
      '- **Macronutrients** (needed in large amounts), **9 elements**: C, H, O, N, P, K, Ca, Mg, S. Among these, **N, P and K** are the **primary nutrients** (most often lacking, supplied in fertiliser); **Ca, Mg, S** are **secondary nutrients**.',
      '- **Micronutrients** or **trace elements** (very small amounts), **7 elements**: iron (Fe), manganese (Mn), zinc (Zn), copper (Cu), boron (B), molybdenum (Mo), chlorine (Cl). Small amounts, but **just as essential**.'),
    DG('nut-fig', 'The essential elements and where they come from', 108, 'nutrients'),
    MN('nut-mn', 'Remember the nutrients', 108,
       '**"C HOPKNS CaFe Mg"** ("see Hopkins café, mighty good") lists C, H, O, P, K, N, S, Ca, Fe, Mg.',
       'Micronutrients: **"Boys Can Cook Zero Fried Meals, Mother"** = B, Cl, Cu, Zn, Fe, Mn, Mo.'),
    T('=agri11-u3-c04', '3.1.4 Functions of the macronutrients', 109,
      'Each nutrient has its own job, and a shortage shows as typical **deficiency symptoms**. A key rule: nutrients that can move inside the plant (**N, P, K, Mg**) show symptoms first on the **older, lower leaves**, because the plant moves them to the young growth. Calcium cannot move, so it shows on **young tips and root tips**.'),
    TB('mac', 'Macronutrients: job and deficiency signs (Table 3.3)', 110, ['Nutrient', 'Main job', 'Deficiency signs', 'Where first'],
       [['Nitrogen (N)', 'Leaf and stem growth; part of proteins and chlorophyll', 'Slow growth, pale yellow-green leaves', 'Older leaves'],
        ['Phosphorus (P)', 'Germination, root growth, flowers, fruit and seed', 'Small dull bluish-green leaves turning purple/bronze, scorched edges, early leaf drop', 'Older leaves'],
        ['Potassium (K)', 'Vigour, disease resistance, strong stems', 'Stunted, leaves close together; brown scorched tips and rolled edges', 'Older leaves'],
        ['Calcium (Ca)', 'Cell walls; root tips', 'Poor roots with weak tips; distorted hooked young leaves', 'Young leaves, root tips'],
        ['Magnesium (Mg)', 'Centre of the chlorophyll molecule; enzymes', 'Yellowing between veins with bright tints; sudden leaf drop', 'Older leaves'],
        ['Sulphur (S)', 'Proteins; chlorophyll formation', 'Slow growth; small stiff upward-rolling leaves; tip buds die', 'Young leaves']], layout='cards'),
    RM('n-excess', 'Too much nitrogen is also harmful', 110,
       'Heavy doses of concentrated N (urea) give fast, lush, **watery** growth that **lodges** and is attacked more by **insects and diseases**, and the excess N upsets the uptake of other nutrients. Give N in **split doses** (part at sowing, part at tillering or knee height).'),
    WK('wk-def', 'Worked example — diagnosing a deficiency', 110,
       'Barley near Adi Quala has small, dull bluish-green leaves with purple tints, and roots are poor. The young leaves look normal. Which nutrient is short, and why do the symptoms start on old leaves?',
       ['Purple/bronze colour and poor roots point to **phosphorus**.',
        'P is **mobile** in the plant: when short, the plant moves P from old leaves to young ones, so old leaves show it first.',
        'Correction: apply a phosphate fertiliser such as **DAP** or **TSP** at sowing, placed in the soil near the seed row (not touching the seed).'],
       'Phosphorus deficiency; old leaves first because P is mobile; band DAP/TSP at sowing.'),
    T('=agri11-u3-c05', '3.1.5 Soil factors', 111,
      'Six soil factors decide how well a crop grows: **soil water, soil air, soil temperature, organic matter, soil organisms and soil reaction (pH)**.',
      '- **Soil water:** water lost by transpiration is replaced only from the soil. Water keeps cells **turgid** (firm, upright), **cools** the plant and is the **solvent** that carries nutrients.',
      '- **Soil air (oxygen):** roots and soil microbes need it to breathe. It helps break down minerals into soluble forms, decomposes plant and animal remains, and drives **nitrification** and **nitrogen fixation** by bacteria. Waterlogged soil has no air and roots die.',
      '- **Soil temperature:** roots absorb water best between **20 °C and 30 °C**; below 20 °C uptake slows. Nitrification hardly starts until the soil reaches about **5 °C**.',
      '- **Organic matter** (dead roots, leaves, twigs, dung, dead animals) supplies nutrients and raises the **water-holding capacity** through its colloids.',
      '- **Soil organisms** (bacteria, fungi, protozoa, nematodes, algae, ants, beetles, earthworms, moles, rats) decompose organic matter; burrowers such as earthworms **aerate** the soil.',
      '- **Soil reaction:** neutral soils suit most crops. Too much **sodium** (sodic, alkaline soil) blocks iron and phosphorus uptake, forms a **hardpan** so water infiltrates poorly, and slows microbial activity.'),
    T('=agri11-u3-c06', '3.1.6 Water: three types of plants', 112,
      'Plants are grouped by how much water they need:',
      '- **Xerophytes** (desert plants) survive great water loss without damage: acacias and doum palm in the lowlands, cactus (beles, prickly pear) on the highland hillsides.',
      '- **Mesophytes** need a medium water supply: most crops, such as sorghum, barley, faba bean and tomato.',
      '- **Hydrophytes** grow best with plenty of water or in water: **rice**, water lilies.',
      '**Demonstration (Assignment 3.3):** grow two similar potted plants; water both for a few weeks, then stop watering one. The unwatered plant wilts, its leaves curl and yellow, and its growth stops. That shows water is needed for turgor, growth and nutrient uptake.'),
    T('=agri11-u3-c07', '3.1.7 Climatic factors', 113,
      '**Climate** is the general state of the atmosphere at a place over a long period. It sets the pattern of vegetation, soils and water, and so decides which crops an area can grow. The climate elements that matter most for crops are **rainfall, temperature, light, wind and humidity**.'),
    TB('rain-tb', 'Rainfall classes and what they mean for crops', 113, ['Zone', 'Annual rainfall', 'What the farmer needs'],
       [['Arid', 'Less than 250 mm', 'Irrigation (e.g. spate irrigation near Sheeb, Wadi Laba)'],
        ['Semi-arid', 'Less than 500 mm', 'Irrigation or water harvesting; drought-tolerant crops (sorghum, pearl millet)'],
        ['Humid', '1000–1500 mm', 'Enough rain in most years; supplementary irrigation in dry spells'],
        ['Wet', 'More than 1500 mm', 'Drainage; leaching of nutrients']], layout='cards'),
    T('temp', 'Temperature and crops', 113,
      'Each crop has a **minimum**, **optimum** and **maximum** temperature for each growth stage; most crops grow between **15 and 32 °C**. Temperature depends on **latitude** and especially on **altitude** (Unit 2).',
      '- High temperature speeds up growth (fast crops in the lowlands), but harm from heat is much worse when **water is short**. Hot dry winds can **desiccate maize tassels** so pollination fails.',
      '- **Pearl (bulrush) millet** tolerates heat and drought better than maize.',
      '- Low temperature limits crops mainly at high altitude; **frost** in the cold months (November–February in the highlands) can damage crops.',
      '- High day and low night temperatures in arid areas suit crops with a high photosynthetic capacity such as **maize, sorghum and millet**.',
      '**Hot-season crops:** tomato, eggplant, pepper, okra, sorghum, cowpea, haricot bean. **Cool-season crops:** lettuce, carrot, cabbage, wheat, barley, chickpea, field pea, lentil.'),
    TB('t34', 'Temperature (°C) needs of dryland crops (Table 3.4)', 115, ['Crop', 'Germination opt (min–max)', 'Growth opt (min–max)', 'Flowering opt (min–max)'],
       [['Millet', '34 (12–38)', '30 (18–42)', '27 (19–35)'],
        ['Sorghum', '34 (10–40)', '34 (16–35)', '25 (15–26)'],
        ['Groundnut', '27 (12–35)', '28 (15–38)', '28 (19–33)'],
        ['Cotton', '34 (13–39)', '27 (13–40)', '26 (19–38)']],
       'Read it like this: sorghum seed germinates best at 34 °C and not at all below 10 °C, which is why sorghum is sown only after the soil has warmed up.', layout='cards'),
    T('light', 'Light, day length and wind', 114,
      '**Light** drives photosynthesis and also controls germination, stem growth, flowering and fruiting. Very **low** light lowers photosynthesis; very **high** light raises respiration and water loss so the stomata close.',
      '**Day length (photoperiod)** controls flowering and the formation of bulbs and tubers:',
      '- **Short-day plants** develop (flower, form tubers) when the day is **shorter than about 12 hours** (many tropical sorghums, rice, soybean).',
      '- **Long-day plants** develop when the day is **longer than 12 hours** (wheat, barley in temperate lands). Growing a strict long-day plant in the tropics fails: it stays vegetative and never flowers.',
      '- **Day-neutral plants** are not affected by day length (tomato; many maize varieties, although tropical maize and pearl millet behave as weak short-day plants).',
      '- Some crops have both types of varieties: **onion** varieties for high latitudes are long-day, those for the tropics are short-day.',
      '**Wind** spreads pollen (maize, beet, spinach), seeds, fungus spores and insects. Strong, hot, dusty winds (common in the western and coastal lowlands) **sandblast** and bury seedlings, cause **lodging**, shatter grain and raise transpiration so stomata close. Windbreaks of trees reduce this.',
      '**Relative humidity** (Unit 2): the lower the RH, the faster the air takes up water from leaves and soil.'),
    T('=agri11-u3-c08', '3.1.8 Seed', 117,
      'A seed has three parts: the **embryo** (the baby plant), a **food store** and a protective **seed coat (testa)**.',
      '- The embryo has a **plumule** (grows into the shoot), a **radicle** (grows into the root) and one or two **cotyledons**.',
      '- In most **dicot** seeds (beans, peas) the **cotyledons** are the food store. In **monocot** grains (maize, sorghum, wheat) the food is stored in the **endosperm**. (A few dicots, such as castor, also keep an endosperm.)',
      '- If a seed does not germinate within its life span, the embryo dies. **Viability** varies: citrus seed dies within weeks; lotus seed can live for centuries.'),
    DG('seed-fig', 'Seed structure and germination', 118, 'seed'),
    TB('germ-tb', 'Epigeal and hypogeal germination compared', 117, ['', 'Epigeal', 'Hypogeal'],
       [['Cotyledons', 'Pushed above the soil', 'Stay below the soil'],
        ['Part that lengthens', 'Hypocotyl (stem below the cotyledons)', 'Epicotyl (stem above the cotyledons)'],
        ['Examples', 'Haricot bean, castor, cotton, pumpkin, sunflower', 'Faba bean, field pea, chickpea, maize, sorghum, wheat'],
        ['Sowing tip', 'Do not sow deep: the big cotyledons must be pushed up', 'Can be sown a little deeper']], layout='compare'),
    T('germreq', 'What a seed needs to germinate', 118,
      'Germination needs **water, oxygen, a suitable temperature** and (for some seeds) **light**.',
      '- **Water** softens the seed coat and starts the enzymes. Hard-coated seeds (some acacias, some legumes) let water in slowly.',
      '- **Oxygen** for respiration: seeds in waterlogged or crusted soil fail.',
      '- **Temperature:** germination happens between about **10 and 35 °C**; most seeds germinate best near **20 °C**.',
      '- **Light quality:** red light promotes germination of light-sensitive seeds, **far-red** light (about **730 nm**, not "mm" as printed in the textbook) inhibits it.',
      '**Seed quality** also matters: **broken** seed germinates poorly and gives weak, small plants; **immature** seed has little food and gives weak seedlings; **large, plump** seed gives vigorous seedlings that survive stress; **shrivelled** seed germinates badly.'),
    DG('gt-fig', 'Germination test, step by step', 119, 'germtest'),
    WK('wk-germ', 'Worked example — germination percentage', 119,
       'A farmer near Hagaz tests 100 sorghum seeds; 86 give strong seedlings (shoot longer than 4 cm and a good root). What is the germination percentage, and should he change his seed rate?',
       ['Germination % = (germinated ÷ total) × 100 = (86 ÷ 100) × 100 = **86 %**.',
        'If the recommended rate assumes about 100 % germination, he needs 100 ÷ 86 ≈ 1.16 times as much: a rate of 10 kg/ha becomes about **11.6 kg/ha**.',
        'Below about 80 % it is better to buy certified seed.'],
       '86 %; raise the seed rate by about 16 % (10 → 11.6 kg/ha).'),
    WK('wk-germ2', 'Worked example — a sample that is not 100 seeds', 119,
       'In a school test of 250 chickpea seeds, 205 germinate. Find the germination percentage.',
       ['Germination % = 205 ÷ 250 × 100.', '205 ÷ 250 = 0.82.', '0.82 × 100 = **82 %**.'],
       '82 %.'),
    T('seedsel', 'Choosing good seed', 120,
      'Good seed is the cheapest way to raise yield. Seed should be clean, free of disease and from a trusted source (for example NARI or a seed cooperative). When selecting a variety, check that it:',
      '- is **adapted** to the area (altitude, rainfall, length of season);',
      '- has the desired traits: **earliness**, quality, high yield;',
      '- is free from **pests and diseases**;',
      '- **resists** abiotic stress such as cold, frost, heat, **drought** and **salinity**;',
      '- has a **market demand**.'),
]


# ------------------------------------------------------------------ 3.2 field crops
L2 = [
    T('=agri11-u3-c11', '3.2.1 Field crops: origin and importance', 122,
      'Crop farming began about **10 000 years ago**, when people moved from hunting and gathering to a settled life with deliberate planting. Each crop was first domesticated in a limited area and later spread to other regions.',
      'The Russian scientist **N. I. Vavilov** divided the world into six to nine **centres of origin** of crops. He visited the **Eritrean highlands in 1927** and confirmed that the **Abyssinian plateau, including Eritrea**, is a **centre of diversity** for barley, emmer and other tetraploid wheats, oats, linseed, safflower, chickpea, lentil, grass pea, pea, faba (horse) bean, rapeseed and mustard. Later **Zhukovsky** raised the number of centres to **11**, one of them in Africa.',
      '**Crops domesticated in this region:** **taff** (its wild ancestor *Eragrostis pilosa* still grows here), **niger seed** (*Guizotia abyssinica*, once widely grown in the central highlands, now rare and threatened), and **sorghum** and **okra** were domesticated in north-east Africa. (The textbook also names sesame; most evidence now points to India as the home of cultivated sesame, although Africa has many wild relatives.) Other African crops: African rice, pearl millet, cowpea, bambara groundnut, Kersting\u2019s groundnut, yam, watermelon and melon.',
      '**Where diversity comes from:** **natural selection** (selfing and natural crossing produce many local types) and **artificial selection** (people explore, identify, characterise and domesticate plants; farmers and breeders keep selecting new varieties). Local landraces kept for generations carry useful traits such as drought tolerance, which breeders use to improve yields.'),
    RM('centre-note', 'Centre of origin or centre of diversity?', 122,
       'A **centre of origin** is where a crop was first domesticated (taff, niger seed here). A **centre of diversity** is where a crop shows great variation even if it was domesticated elsewhere: **barley, durum wheat, chickpea, faba bean and lentil** came from the Fertile Crescent of south-west Asia, but Eritrea and Ethiopia hold a huge range of local varieties of them.'),
    T('importance', 'Why field crops matter', 123,
      '**Field crops** are all crops other than vegetables and fruits that are grown on a field scale, such as grains, pulses, oil, fibre and forage crops.',
      '- **Food:** cereals are the main **carbohydrate** (energy) source; pulses supply **protein** and fight malnutrition; oil crops supply **fat**. Think of injera from taff, kitcha from wheat, shiro from chickpea or field pea, and sesame oil.',
      '- **Feed:** forage crops (alfalfa, elephant grass, oats-vetch) and crop residues (sorghum stover, barley and taff straw) feed livestock in the dry season.',
      '- **Industrial raw materials:** cotton and flax for textiles; sesame, sunflower and linseed for oil; **durum wheat** for pasta and macaroni; **bread wheat** for bread and pastry; **malting barley** for brewing. Sesame from the Gash-Barka is one of Eritrea\u2019s export crops.'),
    T('=agri11-u3-c12', '3.2.2 Classification of field crops', 124,
      'Field crops are classified in three ways: by **agronomic use**, by **special purpose** and by **growth habit**. One crop can belong to several groups: maize is a cereal (agronomic), can be a silage crop (special purpose) and is an annual (growth habit).'),
    TB('agro-tb', 'Agronomic classification', 124, ['Group', 'Grown for', 'Eritrean examples'],
       [['Cereals', 'Edible grain, rich in carbohydrate (staple food)', 'Sorghum, pearl millet, finger millet, taff, barley, wheat, maize'],
        ['Pulses', 'Edible seeds of legumes, rich in protein; fix nitrogen', 'Faba bean, chickpea, field pea, lentil, haricot bean, grass pea, cowpea'],
        ['Root and tuber crops', 'Thick fleshy underground storage organs (root or stem)', 'Potato (stem tuber), sweet potato and carrot (roots)'],
        ['Forage crops', 'Animal feed as hay, silage or pasture', 'Alfalfa, elephant grass, forage sorghum, oats-vetch'],
        ['Oil crops (industrial)', 'Oil in the seed', 'Sesame, groundnut, linseed, niger seed, sunflower'],
        ['Sugar crops (industrial)', 'Sugar in stem or root', 'Sugarcane, sugar beet'],
        ['Fibre crops (industrial)', 'Fibre for textiles and rope', 'Cotton, flax, sisal, kenaf']], layout='cards'),
    TB('special-tb', 'Special-purpose classification', 125, ['Type', 'What it does', 'Example'],
       [['Cover crop', 'Covers bare soil to stop erosion and leaching during fallow or between orchard trees', 'Cowpea, lablab, clover'],
        ['Green manure', 'Ploughed in while still green (before seed) to add N and organic matter', 'Alfalfa, vetch, cowpea, soybean, clover'],
        ['Catch (emergency) crop', 'Quick crop sown where the main crop failed', 'Pearl millet, short-season sorghum'],
        ['Soiling crop', 'Cut and fed green to livestock', 'Faba bean, field pea, forage sorghum, maize'],
        ['Silage crop', 'Chopped and preserved airtight by partial fermentation in a silo or pit', 'Maize, sorghum'],
        ['Companion crop', 'Grown with another crop so two products come from one field', 'Barley sown with clover or alfalfa'],
        ['Trap crop', 'Attracts pests or parasitic weeds away from the main crop', 'See the Striga note below']], layout='cards'),
    RM('striga', 'Note on Striga (parasitic witchweed) and "trap crops"', 125,
       'The textbook uses Sudan grass as a trap crop: it is sown, the parasitic weed (Striga) emerges on it, the stand is destroyed and the main crop (sorghum) is sown later. Strictly, a host such as Sudan grass used this way is a **catch crop**. A true **trap crop** makes Striga seeds germinate but **is not attacked**, so the Striga dies: **cotton, cowpea, groundnut, soybean** and the forage legume *Desmodium* are true trap crops for sorghum Striga.'),
    TB('habit-tb', 'Classification by growth habit', 126, ['Type', 'Life cycle', 'Examples'],
       [['Annual', 'Completes its life cycle in one season or year', 'Wheat, barley, taff, sorghum, tomato, potato'],
        ['Biennial', 'Needs two seasons: leaves and storage organ in the first, flowers and seed in the second', 'Sugar beet, turnip, carrot and cabbage grown for seed'],
        ['Perennial', 'Lives for several years, may flower and fruit every year', 'Sugarcane, coffee, alfalfa, clover, sisal, fruit trees']], layout='cards',
       ),
    'agri11-u3-c09', 'agri11-u3-c10',
    WK('wk-class', 'Worked example — classifying a farm\u2019s crops', 124,
       'A farmer near Barentu grows sorghum, sesame, cowpea, cotton and forage sorghum. Classify each crop agronomically and say which ones help the soil.',
       ['Sorghum = cereal; sesame = oil (industrial) crop; cowpea = pulse; cotton = fibre (industrial) crop; forage sorghum = forage crop.',
        'Cowpea is a legume: root-nodule bacteria fix nitrogen, so the next cereal benefits.',
        'Cowpea also covers the soil (cover crop) and is a true trap crop for Striga.'],
       'Cereal, oil, pulse, fibre, forage; cowpea improves the soil (N fixation, cover, Striga trap).'),
    WK('wk-seedrate', 'Worked example — why spacing and seed rate matter', 137,
       'A barley seed rate of 100 kg/ha is recommended. A farmer broadcasts 160 kg/ha "to be safe" in a dry year. Explain what happens.',
       ['Too many plants compete for the little soil moisture at the seedling stage.',
        'Each plant becomes thin and weak; many die or produce small heads.',
        'Yield is often **lower** than at the right rate, and 60 kg/ha of seed was wasted.',
        'Right density = enough plants to use light, water and nutrients fully, but not so many that they starve each other.'],
       'Over-dense stands compete for water, give weak plants and lower yield; use the recommended rate.'),
]


# ------------------------------------------------------------------ 3.3 cultural practices
L3 = [
    'agri11-u3-c13', 'agri11-u3-c14',
    T('=agri11-u3-c15', '3.3.1 Site selection', 127,
      'Site selection means choosing land that suits the crop. A crop yields best in the area it is **adapted** to. Check:',
      '- **Soil:** well drained and productive (deep, fertile, not saline).',
      '- **Previous crop:** do not plant the same species on the same field every season. This avoids pest and disease build-up and **mechanical mixtures** (volunteer plants of another variety contaminating seed).',
      '- **Climate and water:** a favourable climate and enough water, from rain or supplementary irrigation.',
      '- **Topography:** flat land if machines are used; on slopes, terraces and contour ploughing.'),
    T('=agri11-u3-c16', '3.3.2 Land preparation and tillage', 128,
      'Land preparation must be **timely** and of **good quality**. Poor or late preparation leads to weed problems and soil erosion.',
      '**Tillage** is every operation that prepares the seedbed: hoeing, ploughing, harrowing and inter-cultivation. It is done by hand, with animal-drawn implements such as the Eritrean **maresha** pulled by a pair of oxen, or with tractors.',
      '**Reasons for tillage:** prepare a seedbed for good seed-soil contact; **control weeds**; **bury** crop residues, manure and compost; **conserve soil and water** (rough surface, contour furrows); improve the soil\u2019s physical condition (aeration, infiltration).'),
    DG('plough-fig', 'Ploughing with the maresha', 129, 'plough',
       'In the highlands farmers usually plough two to four times before sowing barley, wheat or taff. Taff needs the finest, firmest seedbed because its seed is tiny.'),
    TB('till-tb', 'Types of tillage compared', 128, ['Type', 'What is done', 'Advantages', 'Problems'],
       [['Primary tillage', 'First, deep breaking of the soil (plough)', 'Breaks the crust, buries residues, raises infiltration, reduces runoff', 'Takes time and draught power; bare soil can erode'],
        ['Secondary tillage', 'Everything after primary tillage and before planting: harrowing, levelling, smoothing, weeding', 'Fine, level seedbed for even germination', 'Too fine a tilth crusts after rain'],
        ['Minimum tillage', 'Ploughing only once, e.g. a second pass only to cover the seed', 'Keeps soil moisture, better stand and rooting, saves labour', 'Weeds: need hand weeding, cultural control or herbicides'],
        ['No-till', 'Seed sown into unploughed soil in a narrow slot, trench or band', 'Keeps soil structure, controls erosion, saves moisture and cost, less CO\u2082 released', 'Clods, poor seed placement, stubble and weeds block the planter, traction problems, residues cannot be fed to animals']], layout='cards'),
    T('=agri11-u3-c17', '3.3.3 Fertilizer: why and what', 130,
      'Plants need all 16 essential elements. When the soil cannot supply one (naturally poor soil, **leaching**, or years of cropping without returning nutrients) it must be added as **fertiliser**.',
      '- **Inorganic (mineral) fertilisers** are factory products with a high, known nutrient content: **urea, DAP, TSP, CAN**. Easy to transport and store, quick acting, but they cost foreign currency and add no organic matter.',
      '- **Organic fertilisers** come from living things: **farmyard manure, compost**, oilseed cake, blood, bones, horn and hoof. They are bulky, hard to transport and in short supply, but they improve soil structure and water holding.',
      'Inorganic fertilisers are grouped by how many primary nutrients they carry:',
      '- **Straight:** one primary nutrient (urea = N; TSP = P).',
      '- **Mixed (incomplete):** two (DAP = N + P).',
      '- **Compound (complete):** all three, N + P + K (e.g. NPK 15-15-15).'),
    TB('fert-tb', 'Common inorganic fertilisers (Table 3.5)', 131, ['Fertiliser', 'N %', 'P\u2082O\u2085 %', 'Type'],
       [['Urea', '46', '0', 'Straight N'],
        ['Calcium ammonium nitrate (CAN)', '26', '0', 'Straight N'],
        ['Single superphosphate (SSP)', '0', '18', 'Straight P'],
        ['Triple superphosphate (TSP)', '0', '46', 'Straight P'],
        ['Di-ammonium phosphate (DAP)', '18', '46', 'Mixed N + P']], layout='grid'),
    WK('wk-fert1', 'Worked example — how much nitrogen is in a bag?', 131,
       'How many kilograms of N are in one 50 kg bag of urea, and in one 50 kg bag of DAP?',
       ['Urea: 46 % of 50 kg = 0.46 × 50 = **23 kg N**.',
        'DAP: 18 % of 50 kg = 0.18 × 50 = **9 kg N**, and 46 % P\u2082O\u2085 = 0.46 × 50 = **23 kg P\u2082O\u2085**.'],
       'Urea bag: 23 kg N. DAP bag: 9 kg N and 23 kg P\u2082O\u2085.'),
    WK('wk-fert2', 'Worked example — fertiliser for a recommendation', 131,
       'A wheat field of 0.5 ha needs **46 kg N per hectare** and **46 kg P\u2082O\u2085 per hectare**. Using DAP and urea, how much of each should the farmer buy?',
       ['For 0.5 ha: N needed = 23 kg; P\u2082O\u2085 needed = 23 kg.',
        'P comes only from DAP: DAP = 23 ÷ 0.46 = **50 kg** DAP (one bag).',
        'That DAP also gives N: 0.18 × 50 = 9 kg N.',
        'N still needed = 23 − 9 = 14 kg N. Urea = 14 ÷ 0.46 ≈ **30 kg** urea.',
        'Practice: DAP at sowing in the row; urea split, half at sowing and half at tillering.'],
       '50 kg DAP and about 30 kg urea.'),
    T('organic', 'Organic sources of nutrients', 131,
      '**Nitrogen sources:** plant by-products such as **oilseed cake** (sesame, groundnut, coconut: 7–8 % N); animal by-products from the abattoir: **blood** (11–25 % N), **horn and hoof** (about 13 % N), bones, condemned meat, gut contents. Animal by-products take longer to mineralise (release their nutrients).',
      '**Potassium fertilisers** (mineral, not organic as the textbook says): **sulphate of potash** (about 48–50 % K\u2082O, more expensive) and **muriate of potash** (potassium chloride, about 60 % K\u2082O), refined from potash salt deposits.',
      '**Phosphorus sources:** **rock phosphate** (crushed rock, 28–30 % P\u2082O\u2085, slow acting), superphosphates and phosphoric acid made by treating rock phosphate or bone with sulphuric acid, and **basic slag** from steelworks (8–18 % P\u2082O\u2085).'),
    RM('urine-err', 'Correction: urine is not 46 % nitrogen', 131,
       'The textbook says "urine consists of 46 per cent nitrogen". That figure belongs to **urea**, the factory fertiliser (46 % N). Animal urine contains urea, but fresh cattle urine has only about **0.5–1.5 % N**. Urine is still valuable: collect it with bedding or mix it into compost. Raw urea, like fresh urine, can harm germinating seed, so it must not be placed touching the seed.'),
    T('manure', 'Farmyard manure and compost', 133,
      '**Farmyard manure (FYM)** = solid and liquid excreta of livestock mixed with bedding (litter). **Compost** = partly decomposed plant and/or animal material.',
      'Both improve **soil structure** and keep soil fertile. Well-rotted FYM typically has about **0.5 % N, 0.2–0.3 % P\u2082O\u2085 and 0.5 % K\u2082O**, so 10 tonnes supply roughly **50 kg N, 20–30 kg P\u2082O\u2085 and 50 kg K\u2082O** (the textbook gives a lower estimate of 15 kg N, 20 kg P\u2082O\u2085 and 40 kg K\u2082O; real values vary widely with the feed and handling).',
      '**Good practice:**',
      '- Store manure **covered or in a pit** until well rotted; trampling by animals helps.',
      '- **Incorporate** it into the soil: manure left on the surface loses N as **ammonia gas**. In the soil, ammonium is held on the soil colloids.',
      '- **Poultry manure** is richer in N but low in K, and its ammonia can scorch crops: use less of it.',
      '- **Sewage sludge** may contain heavy metals (nickel, zinc, chromium, copper) that poison crops. **Seaweed** (near Massawa) adds N and organic matter but must be washed of salt (NaCl) before use on vegetables.'),
    T('fertmeth', 'Methods of fertiliser application', 134,
      '- **Broadcasting:** scatter evenly over the surface, then mix in. Quick; suits broadcast crops such as taff.',
      '- **Row (band) application:** place in a line beside the seed row; efficient for row-planted sorghum and maize.',
      '- **Sub-surface band:** place **5–20 cm** deep, depending on crop and nutrient, near the roots; good for P, which hardly moves in soil.',
      '- **Top-dressing:** urea placed beside the growing crop (e.g. at knee height of maize).',
      'Whatever the method, **cover the fertiliser with soil** and keep it from **touching the seed**. The textbook summary lists "hand placement" instead of sub-surface band; both mean putting fertiliser exactly where the roots will find it.'),
    DG('fp-fig', 'Where the fertiliser goes', 134, 'fertplace'),
    WK('wk-pot', 'Worked example — Assignment 3.7 pot experiment', 134,
       'A pot has a radius of 10 cm. How much fertiliser gives the rate of 1.5 g/m²?',
       ['Area = πr² = 3.14 × 0.10 m × 0.10 m = **0.0314 m²**.',
        'Fertiliser = 1.5 g/m² × 0.0314 m² = **0.047 g** (about 0.05 g, a few granules).',
        'Weigh it on a sensitive balance, or mix 1.5 g in 1 m² worth of soil and use the right fraction.'],
       'About 0.05 g per pot.'),
    T('=agri11-u3-c18', '3.3.4 Time of sowing', 135,
      'Sowing time is set by **rainfall, temperature, pests and diseases, and the market**.',
      '- **Precipitation:** sow when enough rain will follow. Moist soil gives quick germination, so sow within a few days of good rain. In semi-arid areas **early sowing** uses water best; **late** sowing meets water stress at grain filling. Calendar dates are unreliable: it is better to sow when soil moisture reaches about **15–20 %**, or after a set amount of cumulative rain. **Dry planting** (sowing before the rains) lets the crop use the whole short season, as with sorghum in the western lowlands.',
      '- **Temperature:** at high altitude wait until the soil is warm enough for quick germination; in hot dry lowlands very high soil temperature can kill emerging seedlings.',
      '- **Pests and diseases:** shift the sowing date so the crop is in the field when the pest is less common (crop **escape**).',
      '- **Marketing:** perishable vegetables are timed to be harvested when prices are good, e.g. tomatoes for the Asmara market in the dry season.'),
    T('=agri11-u3-c19', '3.3.5 Methods of sowing and seed rate', 136,
      '- **Broadcasting:** seed scattered at random on the surface and covered by a light ploughing or by branches dragged over it (common for taff, barley, wheat). Needs **more seed**.',
      '- **Row planting:** seed in rows with even spacing between and within rows. Saves seed, allows **inter-row cultivation and spraying** without damage, and usually gives **better yields** (e.g. sorghum and maize).',
      '- **Drilling:** seed in rows at a high rate, with almost no space between seeds in the row (wheat by seed drill).',
      '**Seed rate** = kilograms of seed per hectare. In dry areas farmers often sow too densely "for safety" against poor rain; the seedlings then compete for moisture and yields fall. The **optimum plant population** uses moisture, nutrients and light fully.',
      '**Plant density depends on:** **moisture** (less water → fewer plants; irrigated or humid → more), **nutrients** (high fertility supports more plants), and **light** (a leafy, healthy canopy and enough plants to intercept all the light).'),
    DG('sow-fig', 'Three ways of sowing', 136, 'sowing'),
    WK('wk-pop', 'Worked example — plant population from spacing', 137,
       'Sorghum is planted 75 cm between rows and 20 cm between plants. How many plants per hectare? How much seed for 1 ha if 1000 seeds weigh 30 g and two seeds are sown per hill?',
       ['Area per plant = 0.75 m × 0.20 m = 0.15 m².',
        'Plants per hectare = 10 000 m² ÷ 0.15 m² ≈ **66 700 plants**.',
        'Seeds = 2 × 66 700 = 133 400 seeds. Mass = 133 400 ÷ 1000 × 30 g ≈ 4000 g = **4 kg** (more if germination is below 100 %).'],
       'About 66 700 plants/ha and about 4 kg of seed.'),
    T('=agri11-u3-c20', '3.3.6 Weeds', 137,
      'A **weed** is any plant growing where and when it is **not wanted**, interfering with the use of land and water and harming crop production and human welfare. Sorghum plants coming up in a sesame field are weeds there. A plant is only a weed by place and time: Bermuda grass (*Cynodon dactylon*) is one of the worst grass weeds in crops, but a valuable hay grass elsewhere.',
      '**Harm done by weeds:** they **compete** with the crop for **nutrients, water, light and space**; lower yield and quality (weed seed in grain); harbour insects and disease organisms; cause human and animal health problems (poisonous weeds); contaminate water; and lower land value. Parasitic weeds such as **Striga** attach to sorghum and millet roots.',
      '**Benefits of some weeds:** animal feed, manure or compost material, medicine, oil, thatch for huts, and cover that holds soil on bunds and terraces.',
      '**Groups by leaf form:** **broadleaves** (wide net-veined leaves, e.g. Amaranthus), **grasses** (narrow parallel-veined leaves, round hollow stems), **sedges** (grass-like, but with a **solid, triangular stem**, e.g. *Cyperus*).'),
    DG('weed-fig', 'Broadleaves, grasses and sedges', 138, 'weeds',
       'Feel the stem: a sedge stem rolled between finger and thumb has three edges ("sedges have edges").'),
    T('pests', 'Pests, diseases and animal pests', 139,
      '**Pests** are insects and insect-like organisms (nematodes, mites, snails, slugs) that damage crops. Insects cause about **14 %** of estimated crop yield loss. Damage: chewing leaves (armyworm larvae), **sucking sap** (aphids, thrips), boring into stems and pods (stem borers in sorghum, pod borer in chickpea), galls, stunting, early leaf fall, wilting, and spreading **virus diseases** (aphids).',
      'A plant is **diseased** when its normal physiological functions are disrupted. Causes: **pathogens** (fungi, bacteria, viruses, nematodes) or harmful **environmental conditions** (too much or too little nutrient, water or light; toxic chemicals). Examples: **powdery mildew** (fungus), **Verticillium wilt** (caused by a **fungus**, not a bacterium as the textbook caption says), **mosaic** (virus).',
      '**Animal pests:** **birds** (quelea and weaver birds on ripening sorghum and millet) and **rodents** (rats in fields and stores). They also spread diseases and weed seeds.'),
    DG('dt-fig', 'The disease triangle', 141, 'disease',
       'Break any one side and there is no disease: clean seed and rotation remove the pathogen, a resistant variety removes the susceptible host, and the right sowing date or drainage removes the favourable environment.'),
    TB('ctrl-tb', 'Methods of pest control compared', 141, ['Method', 'Examples', 'Strength', 'Weakness'],
       [['Mechanical', 'Hand-picking, removing sick plants, yellow sticky traps, screens, hand weeding, hoeing', 'Cheap, safe', 'Labour; only small areas'],
        ['Crop management (cultural)', 'Sowing date, crop rotation, intercropping, clean seed, field sanitation', 'Cheap, prevents build-up', 'Needs planning; slow'],
        ['Biological', 'Natural enemies: parasitic wasps, ladybird beetles, insect-killing fungi, sterile-male release', 'Cheap once running, no harm to the environment', 'Less effective than chemicals; slow'],
        ['Resistant varieties', 'Varieties bred so pests do not attack them or they tolerate attack', 'The cheapest and best method; good yields', 'Breeding takes years; pests can adapt'],
        ['Chemical', 'Insecticides, fungicides, herbicides', 'Fast, powerful', 'Dangerous to people, livestock, bees and water: **use as a last choice**, with protective clothing and correct doses']], layout='cards'),
    T('=agri11-u3-c21', '3.3.7 Cultivation (inter-row tillage)', 143,
      '**Cultivation** is a light **inter-tillage** done when the crop has reached a certain stage, often **knee height**. Only the top layer of soil is loosened, between the rows, by machine, by an ox-drawn plough or by hoe. It is used in row crops such as **maize, sorghum, pearl millet and finger millet**.',
      '**Purposes:** mainly **weed control** in the open spaces; it also **promotes nitrification**, **conserves moisture** (breaks the crust so rain soaks in instead of running off) and **aerates** the soil, which helps bacterial and chemical activity.',
      'Its success depends on the **right timing**, the **number** of cultivations for that crop and the **soil type**.'),
    T('=agri11-u3-c22', '3.3.8 Harvesting', 143,
      '**Harvesting** is cutting or removing the useful part of the crop. Each crop has its proper **maturity stage**. Too early: shrivelled grain and low quality; too late: **shattering** (grain falls), bird damage and lodging.',
      '**Signs of maturity:** the plant turns **yellow or brown**; the grain is **hard** when bitten (soft grain is not ready).',
      '**Methods:** **manual**, cutting with a **sickle** and threshing later by oxen trampling (most common in Eritrea), and **mechanical**, with a **combine harvester** that cuts, threshes and cleans in one pass and drops the grain into a hopper, used on large flat farms.'),
    T('=agri11-u3-c23', '3.3.9 Threshing and storage', 145,
      '**Threshing** separates grain from straw. In Eritrea the cut crop is spread on a hard, clean threshing floor (**awdi**) and **oxen trample** it; then the grain is **winnowed** in the wind to remove chaff.',
      '**Storage** keeps the seed alive and the grain wholesome until planting or eating. Seed loses viability with age; good storage slows this. Storage life depends on the **kind and variety** of seed, its **initial quality** (sound seed keeps longer than damaged or deteriorated seed), its **moisture content**, the **relative humidity**, the **temperature** and the **oxygen** in the store.',
      '- **Moisture** is the key: the drier the seed, the slower it deteriorates. Dry grain to its safe level (table below).',
      '- Store pests develop best at **28–33 °C** and **60–80 % RH**; more oxygen lets insects and moulds multiply faster.',
      '**A good store:** one door, no windows (openings covered with wire mesh), smooth floor without cracks, sealed against insects and rodents, **cool, dry and ventilated**, clean (good sanitation), repaired bags, walls sprayed with insecticide about **once a year**, **first in, first out**, labels and records. Traditional sealed underground pits and mud-plastered bins limit oxygen and protect sorghum well when the grain is dry.'),
    DG('gs-fig', 'Safe moisture for storing grain', 146, 'grainstore'),
    WK('wk-dry', 'Worked example — drying grain to a safe moisture', 146,
       '1000 kg of maize is harvested at 20 % moisture. What will it weigh when dried to the safe 13 %?',
       ['Dry matter stays the same: 1000 × (1 − 0.20) = 800 kg of dry matter.',
        'At 13 % moisture, dry matter is 87 % of the weight: new weight = 800 ÷ 0.87 ≈ **920 kg**.',
        'So about **80 kg of water** must be removed by sun-drying before storage.'],
       'About 920 kg (80 kg of water removed).'),
]


# ------------------------------------------------------------------ 3.4 cropping systems
L4 = [
    T('=agri11-u3-c30', '3.4.1 Mono-cropping', 149,
      '**Mono-cropping** is growing the **same crop alone** (pure stand) on the same land **year after year**, e.g. sorghum after sorghum, or wheat after wheat.',
      'It is simple to manage, but yields fall over time because: the same nutrients are removed every year (**soil fertility drops**); the crop\u2019s own **diseases and insects** build up in the soil and stubble; and the **weeds** that suit it (Striga in sorghum) multiply.'),
    DG('crop-fig', 'Four cropping systems', 150, 'cropping'),
    T('=agri11-u3-c31', '3.4.2 Mixed cropping and inter-cropping', 150,
      '**Mixed cropping** = growing two or more crops on the same land in the same year **without any row arrangement** (seeds mixed and broadcast). **Inter-cropping** is the form with a **definite arrangement** (e.g. two rows of sorghum and one row of cowpea). Eritrean examples: **sorghum with beans or cowpea**, **maize with potato**, and barley with field pea.',
      '**Benefits:** a **yield advantage** (two crops use light, water and nutrients better than one), **greater yield stability** (if one fails, the other still gives food: insurance in a dry year), **diverse products** (grain for food, residues for feed), more income from selling several products, labour spread over the season, and **soil and water conservation** (better cover). When a **cereal is grown with a pulse**, the cereal benefits from the nitrogen fixed by the pulse.',
      '**What can vary in an intercrop:**',
      '- **Number of crops:** two up to as many as seven; mixing more than two is useful in drier areas.',
      '- **Spatial arrangement:** regular rows, alternate strips (2 rows maize : 1 row beans) or random.',
      '- **Timing:** sown together or one after the other (relay), with different maturity and harvest dates.'),
    WK('wk-ler', 'Worked example — is the intercrop better? (land equivalent ratio)', 151,
       'Sorghum alone gives 1.2 t/ha and cowpea alone 0.8 t/ha. Intercropped on one hectare they give 1.0 t sorghum and 0.4 t cowpea. Is the intercrop better?',
       ['Compare each crop in the mix with its pure yield: sorghum 1.0 ÷ 1.2 = 0.83; cowpea 0.4 ÷ 0.8 = 0.50.',
        'Land equivalent ratio (LER) = 0.83 + 0.50 = **1.33**.',
        'LER above 1 means the intercrop is more productive: you would need **1.33 ha** of pure stands to get what 1 ha of intercrop gives.'],
       'Yes: LER = 1.33, a 33 % land advantage.'),
    T('=agri11-u3-c32', '3.4.3 Alley cropping', 151,
      '**Alley cropping** is an **agroforestry** practice: fast-growing trees or shrubs are planted in **hedgerows** on cropland, and annual food crops are grown in the **alleys** between them.',
      '- The hedges are **pruned** before and during cropping so they do not **shade** the crop; the prunings are put on the soil as **green manure or mulch**.',
      '- Between cropping cycles the hedgerows grow freely and cover the land.',
      '- Benefits: mulch cuts **runoff and erosion**, roots and stems hold the soil, decomposing litter returns **nutrients**, and **leguminous** trees (e.g. leucaena, sesbania, gliricidia) add **nitrogen**. Prunings also give fodder and firewood.'),
    T('=agri11-u3-c33', '3.4.4 Fallowing', 152,
      '**Fallowing** is leaving land **uncropped for more than one year** so the soil can restore its fertility and structure (grass and shrubs grow, organic matter builds up, pests die out). It only works where there is enough land; with Eritrea\u2019s growing population fallow periods have become short or disappeared, so rotation with legumes and manure is needed instead.'),
    T('=agri11-u3-c34', '3.4.5 Crop rotation', 152,
      '**Crop rotation** is growing **different crops in a planned sequence** on the same land, in the same year or over several years. With perennials (fruit trees, alfalfa) a cycle can take several years; shifting cultivation, managed tree fallow and relay intercropping are related forms.',
      '**Benefits:** better **nutrient supply** (legumes add N; deep and shallow rooted crops use different layers), better **soil moisture** and structure, fewer **weeds** and fewer **diseases and insects** (their host disappears for a season).',
      '**Rules for a good rotation:** follow a **cereal with a legume**; do not follow a crop with one from the **same family** (tomato after potato shares diseases); alternate **deep and shallow rooted** crops; include a **soil-covering** crop.',
      '**Highland example:** barley → faba bean or field pea → wheat → chickpea or lentil. **Lowland example:** sorghum → cowpea or groundnut → pearl millet → sesame.'),
    WK('wk-rot', 'Worked example — designing a rotation', 152,
       'A farmer near Mendefera has grown wheat on the same field for five years; yields have fallen and weeds have increased. Suggest a four-year rotation and give reasons.',
       ['Year 1: faba bean (legume, fixes N, breaks the wheat disease cycle).',
        'Year 2: wheat or barley (uses the N left by the bean).',
        'Year 3: chickpea or lentil sown late on residual moisture (another legume, different weeds).',
        'Year 4: linseed or potato with manure (different family and rooting depth), then back to faba bean.',
        'Reasons: nutrients restored, disease and weed cycles broken, better soil structure.'],
       'Faba bean → wheat/barley → chickpea/lentil → linseed or potato.'),
    'agri11-u3-c24', 'agri11-u3-c25', 'agri11-u3-c26', 'agri11-u3-c27', 'agri11-u3-c28', 'agri11-u3-c29',
    TB('cs-tb', 'Cropping systems at a glance', 149, ['System', 'Crops in a season', 'Main benefit', 'Main risk'],
       [['Mono-cropping', 'One crop, same every year', 'Simple, easy mechanisation', 'Fertility loss, pests, weeds'],
        ['Mixed / inter-cropping', 'Two or more together', 'Higher total yield, insurance, N from pulses', 'Harder to mechanise and weed'],
        ['Alley cropping', 'Annual crops between tree hedgerows', 'Mulch, N, less erosion, fodder', 'Shading and root competition if hedges are not pruned'],
        ['Fallowing', 'None (land rests)', 'Fertility restored naturally', 'Needs spare land'],
        ['Crop rotation', 'Different crops in sequence', 'Nutrients, fewer pests, diseases and weeds', 'Needs planning and markets for all crops']], layout='cards'),
]


# ------------------------------------------------------------------ 3.5 horticulture
L5 = [
    T('=agri11-u3-c42', '3.5.1 Horticulture: meaning and importance', 153,
      '**Horticulture** is the branch of agriculture that produces and handles **fruits, vegetables, flowers, ornamental plants, spices and herbs**, and also cares for gardens and green spaces. Compared with field crops it is **intensive**: small areas, high value, more water, labour and care per hectare, and the crops are often first raised in a **nursery**.',
      '**Why it matters:**',
      '- **Nutrition:** fruits and vegetables are rich in **vitamins and minerals** (tomato, kale, carrot, orange, papaya, guava).',
      '- **Industry:** flowers for perfume; fruit and vegetables for canning (tomato paste), juice and jam.',
      '- **Medicine:** many herbs are used in modern and traditional medicine.',
      '- **Commerce:** fresh produce and cut flowers earn **foreign exchange**.',
      '- **Beauty (aesthetic value):** street trees and gardens in Asmara, parks and homes.',
      '- **Social value:** parks and gardens are places to meet; markets such as the Asmara vegetable market bring sellers and buyers together.'),
    TB('branch-tb', 'Branches of horticulture', 155, ['Branch', 'Deals with', 'Examples'],
       [['Pomology', 'Fruit crops', 'Banana, citrus, mango, guava, papaya, grape'],
        ['Olericulture', 'Vegetables', 'Tomato, onion, cabbage, kale, pepper, potato, lettuce'],
        ['Floriculture', 'Flowers and house plants', 'Roses, carnations'],
        ['Ornamental horticulture', 'Decorative trees, shrubs and herbs', 'Bougainvillea, jacaranda'],
        ['Landscape horticulture', 'Design and care of gardens, parks, roadsides', 'Asmara avenues and parks'],
        ['Spices and herbs', 'Aromatic and medicinal plants', 'Basil, rue, fenugreek, chilli']], layout='cards'),
    MN('branch-mn', 'Memory hooks', 155,
       '**Pomo-** = apple/fruit (pomme). **Oler-** = pot herb/vegetable. **Flori-** = flower. "**P**ick fruit, **O**lives in the pot, **F**lowers on the table."'),
    T('=agri11-u3-c43', '3.5.2 Production systems in horticulture', 156,
      '- **Open-field production:** crops grown outside in natural soil and climate (most vegetables around Keren, Asmara and along the Anseba).',
      '- **Protected production:** in **glasshouses (greenhouses), poly-tunnels** or under **plastic covers**. In a greenhouse temperature, light and humidity are **controlled**; in low tunnels and cloches they are only **partly regulated**. Used for high-value crops such as tomatoes, peppers and cut flowers.',
      '- **Hydroponics:** plants grown **without soil**, with all nutrients supplied **in a solution** (lettuce, onion, tomato).',
      'By scale, horticulture ranges from a few square metres in **home gardens** (best near towns, where the family can water and sell) to thousands of hectares on large farms.'),
    DG('hs-fig', 'Ways of growing horticultural crops', 156, 'hortsys'),
    T('nursery', '3.5.3 Nurseries and site selection', 158,
      'A **nursery** is a place where seedlings are raised with water, shade and protection, then moved to the field. Types:',
      '- **Peasant nursery:** rural farmers raise their own seedlings.',
      '- **Standard nursery:** produces seedlings on a **commercial** scale (e.g. Ministry of Agriculture forestry and fruit nurseries).',
      '- **Intermediate (temporary) nursery:** keeps mature seedlings from a standard nursery for a short time until they are distributed.',
      'By how plants are grown, nurseries are also **field nurseries** (in beds) or **container nurseries** (pots, poly-tubes).',
      '**Site selection:** suitable **climate** and protection from **wind**; **level** land; clean **water** free of salts; **fertile** soil; easy **road access**. Fence it from goats.',
      '**Steps to set up:** clear the site → level → lay out paths, beds and structures (shade, water tank, store) → prepare seedbeds and soil mix.'),
    T('=agri11-u3-c44', 'Seedbeds and soil mixes', 160,
      '**Tools:** hoes, spades or shovels, pickaxes, rakes, string and pegs.',
      '- **Raised beds:** **15–20 cm above** ground. Used where **drainage** is needed (wet areas, heavy soils, rainy season).',
      '- **Sunken beds:** **10–15 cm below** ground. Used to **conserve moisture** in dry, low-rainfall places; water is supplied by irrigation.',
      '**Soil mix:** plain field soil is either too **clayey** (tight, badly drained) or too **sandy** (holds little water). In a shallow pot or box the base stays wet because there is no soil below to draw water down, so use a **coarser, lighter mix** that drains and still holds moisture: for example **soil + sand + compost** (change the ratio to suit your soil: add more sand to a clay soil), or sand + compost, or well-decomposed manure.'),
    DG('beds-fig', 'Raised and sunken beds', 160, 'beds'),
    T('=agri11-u3-c45', '3.5.5 Routine nursery practices', 161,
      '1. **Sowing and mulching:** vegetables and annuals are sown in seedbeds, seed boxes or **plug trays** and later transplanted; tree seed is sown directly into containers or densely in beds and then pricked out. Cover the bed with grass **mulch** to help germination and stop weeds; **remove** it as soon as seedlings emerge.',
      '2. **Transplanting (pricking out):** water the bed first, lift seedlings with soil on the roots, hold them by the leaves, not the stem.',
      '3. **Shading:** young seedlings need shade (the "growth shade period"); reduce shade gradually before field planting (**hardening**). Straw is cheap and local; plastic netting gives even shade but costs more.',
      '4. **Weeding:** competition is severe in containers. Hand-weed while weeds are young; good **sanitation** is the cheapest control.',
      '5. **Thinning:** remove extra seedlings so the rest have enough space, light, water and nutrients.',
      '6. **Root and shoot pruning:** cut roots growing out of the container; balance the shoot to the root. Fruit trees get **formative pruning** (training) from the nursery stage.',
      '7. **Watering and protection:** water newly sown beds often; use a can with a **fine rose** so seeds are not washed out. Water less often in cool seasons and heavy soils; once or twice a day in hot weather. Watch for **damping-off** (seedlings collapse at soil level).',
      '8. **Grading:** discard weak, poor seedlings; about **10–20 %** culls is normal.'),
    MN('nur-mn', 'The nursery routine in order', 161, '**"Some Men Take Shade When The Proper Water Gets Hot"**: Sow, Mulch, Transplant, Shade, Weed, Thin, Prune, Water, Grade, Harden.'),
    T('=agri11-u3-c46', '3.5.6 Vegetative propagation: budding and grafting', 166,
      '**Vegetative propagation** uses roots, stems or leaves instead of seed. Methods: **cuttings, layering, division, budding and grafting**. The new plant is a **clone**: identical to the mother, so a good mango or orange variety stays true.',
      'A grafted fruit tree has two parts: the **rootstock (stock)**, which forms the root system (hardy, disease resistant, grown from seed, cuttings, suckers or layers), and the **scion**, the upper part that carries the **desired variety** (fruit quality).',
      '- **Grafting** joins a scion with **two or more buds** to a stock; used for new plants and to **top-work** (change the variety of) old trees, e.g. peach, mango.',
      '- **Budding** uses a scion of **a single bud** on a piece of bark; quick and easy, and the most common way to propagate **citrus**. Chip and shield (T) budding are the main tropical methods.',
      '**Key rule:** the **cambium** (the green growing layer between bark and wood) of stock and scion must touch. Both form **callus** cells that interlock and heal the union.'),
    ST('tbud-st', 'Shield (T) budding step by step', 167, 'tbud',
       [('Make a **vertical cut 3–4 cm** long through the bark of the stock, just to the wood.', 'k1'),
        ('Make a **horizontal cut 1–2 cm** across the top of it (a T; across the bottom for an inverted T).', 'k1'),
        ('Cut the bud **shield**: start about 1 cm below the bud and finish a little above it, taking a thin sliver of wood.', 'k2'),
        ('Open the bark flaps with the back of the knife and **push the shield in** until it is fully enclosed.', 'k3'),
        ('**Wrap** firmly with budding tape, leaving the bud exposed. Remove the tape once the bud has taken.', 'k4')]),
    T('graft', 'Grafting methods and tools', 169,
      '- **Whip (tongue) graft:** small stems **6–12 mm** thick, stock and scion of equal size. The scion is 5–15 cm long with 2–3 buds. Make matching **diagonal cuts of 3.5–5 cm**, then a **reverse "tongue" cut** a third of the way down each, half as long, so they interlock. Match the cambium on at least one side and wrap with tape.',
      '- **Side-veneer graft:** potted plants 6–12 mm thick; a 5–7 cm cut into the side of the stock with a notch at its base; the scion is cut to fit, inserted and wrapped. Cut back the stock once the scion grows.',
      '- **Bark** and **cleft grafts:** on **large stems**, for **top-working** an old tree to a new variety. **Wedge grafting** is a cleft graft on small stems.',
      '**Tools and materials:** **secateurs** (collect and trim wood), a sharp single-bladed **budding/grafting knife**, a **saw** (top-working), mallet and wedge for cleft grafts, **grafting wax** to seal cuts against drying and infection, **polyethylene tape**, cloth tape or rubber strips, labels, plastic or paper bags to protect scions, short nails for bark grafts.'),
    DG('whip-fig', 'Whip grafting', 169, 'whip'),
    T('=agri11-u3-c47', '3.5.7 Propagation by cuttings', 173,
      'A **cutting** is a piece of stem (sometimes root) that forms roots and becomes a new plant. Tools: cutting wood, secateurs, soil mix, pots. Easy plants: **lantana, grape, coleus**, rose, sugarcane setts, cassava. Cuttings are also used to raise clonal **rootstocks**.',
      '- **Softwood cuttings:** young soft shoots **10–15 cm** long; remove the leaves from the lower third; dip in **rooting hormone**; insert in a well-drained, **sterile** medium; keep under **intermittent mist** until rooted; then **harden off** by misting less or moving to shade in pots for some weeks.',
      '- **Semi-hardwood cuttings:** from the **matured part of this season\u2019s growth**; prepared the same way; misting less often.',
      '- **Hardwood cuttings:** dormant wood **6–20 mm** thick cut into **15–30 cm** pieces, the base cut **just below a node**; hormone; bundles stored **upside down** in moist sterile peat (callusing box) until a yellowish-white **callus** forms at the base; plant out before many roots form, burying all but the top bud.'),
    T('=agri11-u3-c48', '3.5.8 Propagation by layering', 174,
      '**Layering** makes roots form on a stem **while it is still attached to the mother plant**, which keeps feeding it. It suits plants that are hard to root by other methods, but gives only a **few** plants.',
      '- **Air layering** (hard stems, branches 1–2 cm thick): remove a **ring of bark 1–3 cm** wide, **15–30 cm** from the branch tip; apply hormone; wrap in a ball of **moist moss or compost** and cover with **polythene** or foil; when roots show, cut below the wrap and pot it. Mango, rubber plant, croton, camellia.',
      '- **Simple layering:** bend a low branch to the ground and **bury** part of it, leaving the tip out; wounding and hormone help. Climbing rose, jasmine, oleander.',
      '- **Serpentine (compound) layering:** a long flexible branch is pegged down at **several places**, giving several plants.',
      '- **Trench layering:** the whole branch is laid in a trench and nicked in several places; many shoots root along it (willow).',
      '- **Mound layering (stooling):** cut the plant back near the ground, heap soil over the new shoots, keep moist; when rooted, separate them. Apple rootstocks, croton, peach.'),
    DG('lay-fig', 'Air and simple layering', 175, 'layering'),
    'agri11-u3-c39',
    T('=agri11-u3-c49', '3.5.9 Propagation by division; hardening and transport', 177,
      '**Division** cuts a clump or underground storage organ into pieces, each with enough **stems, leaves, roots and buds** to survive transplanting. Used for plants with many stems or **offshoots**, **bulbs** (garlic, onion sets, narcissus), **corms** and **cormels**, **rhizomes** (canna, ginger), **tubers** (potato) and **suckers/offshoots** (**banana, date palm**, ferns, orchids, daylilies).',
      '**Hardening** prepares nursery seedlings for the shock of field planting: growth slows, food storage increases and tissues toughen, so hardened plants root faster and resist drought and temperature extremes. Start well **before** transplanting:',
      '- expose plants to cooler than optimum temperatures (cool areas) or warmer than optimum (hot areas);',
      '- **reduce watering gradually**, without letting the seedlings wilt;',
      '- move shaded seedlings into **full sun** step by step.',
      '**Transport:** container seedlings travel more easily than bare-root field seedlings; protect them from damage, wind and sun, especially on long trips.'),
    T('=agri11-u3-c50', '3.5.10 Site selection for a horticultural farm', 179,
      'Fruit trees are **perennial**: once an orchard is planted it cannot easily be moved, so assess the site fully first. Vegetables also need the right environment and market to be profitable.',
      '- **Climate:** each crop has its temperature, rainfall and light needs (citrus and mango in warm lowlands and the escarpment; apple, potato and cabbage in the cool highlands); plant **windbreaks** where needed.',
      '- **Terrain:** suitable altitude and slope.',
      '- **Soil and drainage:** the right soil type and drainage for the crop.',
      '- **Irrigation water:** essential in arid and semi-arid Eritrea.',
      '- **Economics:** check that the crop will be **profitable** (market distance, prices) before planting.'),
    T('=agri11-u3-c51', '3.5.11 Garden layout and land preparation', 180,
      'Draw a **plan** of the garden to record planting and harvest dates and the area of each crop. Mark out beds from the plan.',
      '- Beds **1.0–1.2 m wide**, so all work (weeding, harvesting) can be done from the path without stepping on the bed; length as convenient.',
      '- Example: plots **6 m wide**, separated by **1 m grass paths**, each divided into beds **1.2 m** across with **60 cm** temporary paths.',
      '- Put a **fence or hedge** around the garden against animals.',
      '- **Succession planting:** a crop calendar so one crop follows another and the garden is always producing. **Companion planting:** growing crops that suit each other together.',
      '- Commercial layout depends on the farm scale, crop, variety, equipment, season and technology.'),
    DG('garden-fig', 'Garden plan', 181, 'garden',
       'Dividing the garden into three plots makes rotation easy: e.g. leafy vegetables → fruit vegetables (tomato, pepper) → root crops and legumes.'),
    WK('wk-garden', 'Worked example — how many beds fit in a plot?', 181,
       'A plot is 6 m wide. Beds are 1.2 m wide with 60 cm paths between them. How many beds fit, and how much width is used?',
       ['Try 4 beds: 4 × 1.2 m = 4.8 m of beds, plus 3 paths × 0.6 m = 1.8 m. Total 6.6 m: too wide.',
        'Try 3 beds: 3 × 1.2 m = 3.6 m, plus 2 paths × 0.6 m = 1.2 m. Total **4.8 m**.',
        'So **3 beds** fit, leaving 1.2 m: either a fourth narrower bed or wider edge paths.'],
       '3 full beds (4.8 m used).'),
    T('prep', 'Preparing a home or school garden', 182,
      '**First preparation:**',
      '1. Wet the area (especially hard dry clay) and let it dry partly for two days.',
      '2. Loosen the soil to about **30 cm** with a spading fork; remove weeds.',
      '3. Water gently and rest one day; wait longer if there are big clods (sun, cool nights and water break them).',
      '4. Clay soil: mix in **not more than 2.5 cm** of sand (more lets soluble fertiliser wash through too fast).',
      '5. Add **8 cm** of compost or aged manure to poor (very sandy or very clayey) soils, **2.5 cm** to good soils; mix into the top 30 cm.',
      '6. Dig twice if the soil is heavy; water and rest a day.',
      '7. Level and shape the beds; add fertilisers and pH correctors: **lime** for acid soil; for alkaline soil, sulphur or acid-forming fertilisers such as ammonium sulphate.',
      '8. Plant or transplant.',
      '**Replanting:** dig after removing old crops, shape beds, water, add about 2.5 cm of compost and fertiliser, plant.'),
    T('dd', 'Double digging and pit preparation', 183,
      '**Double digging** (home and school gardens, medium and clay soils, every 3–4 years):',
      '1. Dig a trench **28–30 cm deep** and **56–70 cm wide** across the bed; carry that topsoil to the far end.',
      '2. Loosen the subsoil in the trench a further **15–30 cm**; spread manure or compost on it.',
      '3. Dig the topsoil of the next strip onto the manured subsoil of the first; loosen and manure the second strip\u2019s subsoil.',
      '4. Repeat to the end; fill the last trench with the soil from the first.',
      'Result: the bed is loosened **45–60 cm** deep and needs no double digging for **2–4 years**.',
      '**Pits for trees:** usually **60 × 60 × 60 cm**; **100 × 100 × 100 cm** in soil with a hardpan. Keep topsoil and subsoil apart, mix topsoil with manure to refill, plant at the nursery depth, water and **mulch**. For close-planted orchards dig a **furrow** along the row instead.'),
    DG('dd-fig', 'Double digging', 183, 'doubledig'),
    DG('pit-fig', 'Pit planting', 184, 'pit'),
    T('=agri11-u3-c52', '3.5.12 Sowing, transplanting and field care', 184,
      'Most horticultural crops are sown in a nursery and **transplanted**; **cucurbits** (pumpkin, watermelon, cucumber) are usually sown directly.',
      '- **Adapted varieties:** use varieties recommended for your area; do not use unknown seed for commercial growing, even if it is free.',
      '- **Germination test** before sowing: seed deteriorates fast in hot humid conditions, even in an opened can.',
      '- **Depth:** small seeds **0.6–1.2 cm** deep; too deep and they cannot emerge or they rot.',
      '- **Transplant** only healthy, vigorous, **stocky** seedlings with **4–6 true leaves**; this takes about **3–6 weeks** in warm climates (fastest: tomato, cabbage, broccoli, lettuce; slowest: pepper, eggplant). Tomato: 15–20 cm tall with a pencil-thick stem; cabbage: 6-leaf stage; eggplant: 10–12 cm. Old, overgrown seedlings suffer more transplant shock. Transplant in the **afternoon** or on cloudy days, with soil on the roots.',
      '- **Thinning** gives remaining plants room. **Mulching** with straw, banana leaves or plastic cuts evaporation and runoff, keeps soil temperature and moisture even, and suppresses weeds.',
      '- **Tree pruning** builds a strong framework, keeps trees healthy and of manageable size: formative pruning, removal of dead and diseased wood, size control, and stimulation of new fruiting wood.',
      '- **Watering:** the right amount at every stage; too little or too much lowers yield.',
      '- **Fertiliser:** manure, compost or mineral fertiliser by broadcasting, base-dressing, band placement, top-dressing, liquid or **foliar** feeding.'),
    T('=agri11-u3-c53', '3.5.13 Post-harvest handling', 187,
      '**Post-harvest handling** covers every operation from harvest to the consumer that affects quality and storage life. In developing countries up to **50 %** of fresh produce can be lost: of 100 kg of tomatoes harvested, 50 kg may never be eaten, because of bruising in transport and poor handling at markets.',
      '- **Highly perishable:** tomato, strawberry, guava, leafy vegetables. **Less perishable:** onion, potato, pumpkin.',
      '- Handle each crop to suit it: potatoes and onions can go in **sacks**; tomatoes need **boxes or crates**.',
      '- The chain: harvest at the right stage in the **cool** part of the day → **clean** → **sort** (remove damaged, diseased and green potato tubers) → **grade** by size → **pack** → transport quickly in shade → sell or store cool. NARI\u2019s seed potato work shows sorting, grading into boxes and packing in jute sacks.'),
    DG('ph-fig', 'From the field to the consumer', 187, 'postharvest'),
    WK('wk-loss', 'Worked example — value of reducing losses', 187,
       'A cooperative near Keren harvests 2000 kg of tomatoes and loses 40 % between field and market. With crates and shade the loss falls to 15 %. If tomatoes sell for 10 Nakfa per kg, how much more money does it earn?',
       ['Sold before: 2000 × 0.60 = 1200 kg → 12 000 Nakfa.',
        'Sold after: 2000 × 0.85 = 1700 kg → 17 000 Nakfa.',
        'Gain = **5000 Nakfa** (500 kg more tomatoes reach buyers).'],
       '5000 Nakfa more.'),
    'agri11-u3-c35', 'agri11-u3-c36', 'agri11-u3-c37', 'agri11-u3-c38', 'agri11-u3-c40',
]

LESSONS = {'agri11-u3-l3-1': L1, 'agri11-u3-l3-2': L2, 'agri11-u3-l3-3': L3, 'agri11-u3-l3-4': L4, 'agri11-u3-l3-5': L5}
DROP = ['agri11-u3-c41', 'agri11-u3-xtra2']  # a stray source line titled "Quiz 3"; a one-line worked "seed rate" now covered in full
PATCH = {
    'agri11-u3-c40': {'title': 'Post-harvest: produce is still alive'},
    'agri11-u3-chk2': {'q': 'Vavilov listed the Abyssinian plateau (including Eritrea) as a centre of diversity of several crops. Which of these is a **pulse** on that list?',
                       'why': '**Reasoning**\nVavilov (who visited the Eritrean highlands in 1927) named the Abyssinian plateau a centre of diversity for barley, tetraploid wheats, linseed, chickpea, lentil, pea, faba bean and others. Teff is a cereal (domesticated here), sesame is an oil crop and maize came from Central America. Chickpea was first domesticated in south-west Asia, but this region holds a great diversity of local chickpea types.\n\n**Conclusion**\nThe pulse is **Chickpea**.'},
    'agri11-u3-chk7': {'q': 'A school nursery uses a potting mix of garden soil, compost and sand. Which ratio is a common starting mix (to be adjusted to the local soil)?',
                       'why': '**Reasoning**\nThe textbook says to use a soil, sand and compost mix and to modify the ratio to suit your soil. A common starting point is 3 parts garden soil (body), 1 part compost (nutrients, water holding) and 1 part sand (drainage). Add more sand to a heavy clay soil. Pure straight soil drains badly in pots.\n\n**Conclusion**\n**3 parts soil : 1 part compost : 1 part sand** is the usual starting mix.'},
    'agri11-u3-wrk1': {'steps': [{'text': '**Reasoning**'}, {'text': 'Xylem is the vascular tissue that carries water and dissolved minerals absorbed by the roots **up** to the stems and leaves.'},
                                 {'text': 'Phloem carries sugars from the leaves to wherever they are used or stored; that flow can go up or down.'},
                                 {'text': '**Conclusion**'}, {'text': 'The answer is **to transport water and dissolved minerals from roots to leaves.**'}]},
}


# ------------------------------------------------------------------ practice
a = QSet('3.1 Practice — plants, growth factors and seed', 's31')
a.M(102, 'Which feature shows that sorghum is a monocot?', ['Netted leaf veins', 'Flower parts in fives', 'Parallel leaf veins', 'Vascular bundles in a ring'], 'C',
    ['Step 1: Monocots have parallel veins, scattered bundles and flower parts in threes.', 'Step 2: Netted veins, parts in fives and bundles in a ring are dicot features.'],
    'Look at the leaf first: parallel = monocot.', [('Which feature shows that chickpea is a dicot?', 'Its seed splits into two cotyledons (also netted veins, tap root).')])
a.M(103, 'Which of these is a modified underground stem with "eyes" (buds)?', ['Carrot', 'Potato tuber', 'Sweet potato', 'Onion bulb scale'], 'B',
    ['Step 1: Eyes are buds, and only stems bear buds at nodes.', 'Step 2: Carrot and sweet potato are storage roots; a bulb scale is a leaf.'],
    'Buds mean stem.', [('Is ginger a corm or a rhizome?', 'A rhizome (horizontal underground stem); taro is a corm.')])
a.M(103, 'The vascular system of a plant is made of', ['xylem and cambium', 'xylem and phloem', 'phloem and cambium', 'cortex and pith'], 'B',
    ['Step 1: Xylem carries water and minerals; phloem carries sugars.', 'Step 2: Cambium makes new xylem and phloem but is not a transport tissue.'],
    'Two pipes: X for water, P for food.', [('Which tissue must touch in a graft?', 'The cambium.')])
a.M(104, 'A fibrous root system is', ['deep with one main root', 'shallow, wide and good at holding soil', 'made only of aerial roots', 'typical of beans'], 'B',
    ['Step 1: In fibrous roots the primary root stops and many roots grow from the stem base.', 'Step 2: They are shallow, spread widely, absorb well and bind soil.'],
    'Fibrous = grasses and cereals.', [('Name a crop with a tap root used as food.', 'Carrot.')])
a.S(104, 'List four functions of roots.', 'Absorb water and nutrients; anchor the plant; support the stem; store food (carrot); propagate some plants (sweet potato).',
    ['Step 1: Think of what roots take in: water and minerals.', 'Step 2: What they do mechanically: anchor and support.', 'Step 3: Extra jobs: storage and propagation.'],
    'Absorb, Anchor, Support, Store, Spread.', [('Give two functions of leaves.', 'Photosynthesis and gas exchange (also food storage in some).')])
a.M(105, 'The part of the flower that receives pollen is the', ['anther', 'stigma', 'ovary', 'sepal'], 'B',
    ['Step 1: Anthers make pollen.', 'Step 2: The stigma at the top of the pistil catches it.', 'Step 3: The ovary later becomes the fruit.'],
    'Stigma = sticky landing pad.', [('Which flower part becomes the fruit?', 'The ovary.')])
a.S(106, 'Write the word equation for photosynthesis and state where each input comes from.', 'Carbon dioxide + water + light → sugar + oxygen. CO₂ from the air through the stomata; water from the soil through roots and xylem; light from the sun, absorbed by chlorophyll.',
    ['Step 1: Inputs: CO₂, H₂O, light energy (with chlorophyll).', 'Step 2: Products: sugar (glucose) and oxygen.', 'Step 3: Sources: air, soil, sun.'],
    'Air + water + sun → food + oxygen.', [('Which colours of light does chlorophyll absorb most?', 'Violet-blue and red.')])
a.M(107, 'In the iodine test, the covered part of a leaf stays brown because', ['iodine cannot reach it', 'no starch was made there without light', 'it has no chlorophyll', 'it lost water'], 'B',
    ['Step 1: The plant was destarched in the dark first.', 'Step 2: Only parts in light made new starch, which turns iodine blue-black.'],
    'Blue-black = starch = light received.', [('Why keep the plant in the dark for 3 days first?', 'To remove the starch already in the leaves.')])
a.M(108, 'Which group lists only primary nutrients?', ['N, P, S', 'P, B, Zn', 'N, P, K', 'N, B, P'], 'C',
    ['Step 1: Primary nutrients are needed most and supplied in fertiliser: N, P, K.', 'Step 2: S is secondary; B and Zn are micronutrients.'],
    'NPK on the fertiliser bag.', [('Name the three secondary nutrients.', 'Calcium, magnesium and sulphur.')])
a.S(108, 'How many essential elements are there, and how many are macronutrients and micronutrients?', '16 essential elements: 9 macronutrients (C, H, O, N, P, K, Ca, Mg, S) and 7 micronutrients (Fe, Mn, Zn, Cu, B, Mo, Cl).',
    ['Step 1: C, H, O come from air and water.', 'Step 2: The other 13 come from the soil: 6 macro + 7 micro.'], '16 = 9 + 7.',
    [('Which three essential elements do plants not take from the soil?', 'Carbon, hydrogen and oxygen (from air and water).')])
a.M(110, 'A crop has pale yellow-green older leaves while the young leaves are green. The most likely shortage is', ['calcium', 'nitrogen', 'sulphur', 'boron'], 'B',
    ['Step 1: Yellowing of old leaves first = a mobile nutrient.', 'Step 2: Pale yellow-green colour and slow growth = nitrogen.', 'Step 3: Calcium and boron show on young tissue.'],
    'Old leaves first → mobile N, P, K, Mg.', [('Brown scorched leaf edges and tips on older leaves suggest?', 'Potassium deficiency.')])
a.S(110, 'Why can too much nitrogen fertiliser be harmful?', 'It gives fast, lush, watery growth that lodges and is attacked more by insects and diseases; excess N upsets uptake of other nutrients; it is wasted by leaching.',
    ['Step 1: Soft tissue is easy for pests.', 'Step 2: Tall weak stems fall over (lodge).', 'Step 3: Unbalanced nutrition.'], 'Lush is not healthy.',
    [('How should urea be applied to reduce these problems?', 'In split doses at the right growth stages.')])
a.M(112, 'Rice, which grows best with abundant water, is a', ['xerophyte', 'mesophyte', 'hydrophyte', 'epiphyte'], 'C',
    ['Step 1: Hydro = water.', 'Step 2: Xerophytes are desert plants; mesophytes need medium water.'], 'Xero dry, meso middle, hydro wet.',
    [('Name an Eritrean xerophyte.', 'Acacia, doum palm or prickly pear cactus.')])
a.M(113, 'An area receiving less than 250 mm of rain a year is', ['semi-arid', 'arid', 'humid', 'wet'], 'B',
    ['Step 1: Arid < 250 mm; semi-arid < 500 mm.', 'Step 2: Humid 1000–1500; wet > 1500.'], '250 / 500 / 1000 / 1500.',
    [('Which zone receives more than 1500 mm?', 'A wet area.')])
a.M(114, 'Which are both cool-season crops?', ['Sorghum and okra', 'Barley and lentil', 'Tomato and pepper', 'Cowpea and haricot bean'], 'B',
    ['Step 1: Cool-season crops: lettuce, carrot, cabbage, wheat, barley, chickpea, field pea, lentil.', 'Step 2: The others are hot-season crops.'],
    'Highland crops are cool-season crops.', [('Give two hot-season vegetables.', 'Tomato, eggplant, pepper or okra.')])
a.M(115, 'A plant that flowers only when the day is shorter than about 12 hours is', ['a long-day plant', 'a short-day plant', 'day-neutral', 'a biennial'], 'B',
    ['Step 1: The name tells the day length that triggers flowering.'], 'Short day = flowers as days shorten.',
    [('Which is day-neutral: onion, radish, potato or tomato?', 'Tomato.')])
a.S(115, 'Using Table 3.4, at what temperature does sorghum seed germinate best, and what is the minimum?', 'Optimum 34 °C; minimum 10 °C (maximum 40 °C).',
    ['Step 1: Find the sorghum row, germination columns.', 'Step 2: opt 34, min 10, max 40.'], 'Read the row, then the column.',
    [('What is the optimum temperature for millet growth?', '30 °C.')])
a.M(117, 'In hypogeal germination', ['the cotyledons come above the soil', 'the cotyledons stay below the soil', 'there is no radicle', 'the seed has no food store'], 'B',
    ['Step 1: Hypo = below, epi = above, geal = earth.', 'Step 2: The epicotyl lengthens and the cotyledons stay underground.'],
    'Hypo = under.', [('Give an example of epigeal germination.', 'Haricot bean or castor.')])
a.M(117, 'In a maize grain the food is stored mainly in the', ['cotyledons', 'endosperm', 'radicle', 'seed coat'], 'B',
    ['Step 1: In monocot grains the endosperm is the store.', 'Step 2: In beans the two cotyledons are the store.'], 'Grain = endosperm; bean = cotyledons.',
    [('Name the part of the embryo that becomes the shoot.', 'The plumule.')])
a.S(119, 'In a germination test 72 of 80 seeds germinate. Find the germination percentage.', '90 %',
    ['Step 1: G% = germinated ÷ total × 100.', 'Step 2: 72 ÷ 80 = 0.9.', 'Step 3: 0.9 × 100 = 90 %.'], 'Divide first, then × 100.',
    [('If 45 of 60 germinate?', '75 %.')])
a.S(118, 'List four requirements for seed germination.', 'Water, oxygen, a suitable temperature (about 10–35 °C) and, for some seeds, light (red light).',
    ['Step 1: Water starts the process.', 'Step 2: Oxygen for respiration.', 'Step 3: Warmth for enzymes.', 'Step 4: Light for light-sensitive seeds.'],
    'W-O-T-L.', [('Why do broken seeds give poor stands?', 'Damaged embryos and food stores lower germination and give weak seedlings.')])
a.S(120, 'Give four things to check when selecting seed of a variety.', 'Adapted to the area; desirable traits (earliness, quality, yield); free from pests and diseases; tolerant of stresses such as drought, frost, heat or salinity; market demand.',
    ['Step 1: Will it grow here?', 'Step 2: Is it good?', 'Step 3: Is it clean?', 'Step 4: Can I sell it?'], 'Adapted, good, clean, sellable.',
    [('Where can Eritrean farmers get certified improved seed?', 'From NARI and Ministry of Agriculture seed programmes or seed cooperatives.')])

b = QSet('3.2 Practice — field crops', 's32')
b.F(122, 'The scientist who proposed the idea of centres of origin of crops was ____.', 'Vavilov', ['Vavilov', 'Darwin', 'Mendel', 'Zhukovsky'],
    ['Step 1: N. I. Vavilov, a Russian scientist, named the centres and visited Eritrea in 1927.', 'Step 2: Zhukovsky later increased the number to 11.'],
    'V for Vavilov, V for visited.', [('How many centres did Zhukovsky recognise?', '11.')])
b.M(122, 'Which crop was domesticated in the Abyssinian plateau (its wild ancestor grows there)?', ['Maize', 'Taff', 'Rice', 'Potato'], 'B',
    ['Step 1: The wild ancestor of taff, Eragrostis pilosa, grows here.', 'Step 2: Maize and potato came from the Americas; Asian rice from Asia.'],
    'Taff and niger seed are home-grown.', [('Which oil crop, once common in the central highlands, is now threatened?', 'Niger seed (Guizotia abyssinica).')])
b.F(123, 'The diversity of crops results from natural and ____ selection.', 'artificial', ['artificial', 'chemical', 'random', 'mechanical'],
    ['Step 1: Natural selection: selfing and natural crossing.', 'Step 2: Artificial: people choose and domesticate plants.'], 'Nature + people.',
    [('Who carries out artificial selection today?', 'Farmers and plant breeders.')])
b.M(124, 'Which group contains only pulses?', ['Sesame, groundnut, wheat', 'Faba bean, chickpea, lentil', 'Barley, taff, sorghum', 'Cotton, flax, sisal'], 'B',
    ['Step 1: Pulses are legumes with edible seeds.', 'Step 2: Sesame/groundnut are oil crops, cotton/flax fibre crops.'], 'Pulses go into shiro.',
    [('Which group are all oil crops?', 'Groundnut, sesame and rapeseed (linseed, niger seed).')])
b.S(124, 'Why are pulses important in a farming system?', 'They are rich in protein (food against malnutrition), fix atmospheric nitrogen through root nodules so the next cereal yields more, break cereal pest and disease cycles in rotation, and are a source of income and fodder.',
    ['Step 1: Food value: protein.', 'Step 2: Soil value: nitrogen fixation.', 'Step 3: Rotation value: break cycles.', 'Step 4: Money.'],
    'Protein, nitrogen, rotation, income.', [('Which crop group is the main carbohydrate source?', 'Cereals.')])
b.M(125, 'A crop ploughed into the soil while still green to add nitrogen is a', ['catch crop', 'green manure', 'silage crop', 'soiling crop'], 'B',
    ['Step 1: Green manure is incorporated before seed set.', 'Step 2: A soiling crop is cut and fed green to animals.'], 'Green manure feeds the soil; soiling crop feeds the cow.',
    [('What is a catch crop?', 'A quick crop such as millet sown where the main crop failed.')])
b.M(126, 'Crops that complete their life cycle in two seasons are', ['annuals', 'biennials', 'perennials', 'ephemerals'], 'B',
    ['Step 1: Bi = two.', 'Step 2: Sugar beet stores sugar in year 1 and flowers in year 2.'], 'Bi-cycle has two wheels.',
    [('Name two perennial crops.', 'Sugarcane, coffee, alfalfa or fruit trees.')])
b.S(124, 'Classify each crop: (a) sisal, (b) sweet potato, (c) alfalfa, (d) sugarcane.', '(a) fibre crop; (b) root crop; (c) forage crop (also a perennial legume); (d) sugar crop.',
    ['Step 1: Ask what part is used and for what.', 'Step 2: Fibre, storage root, animal feed, sugar.'], 'Classify by what you harvest.',
    [('Classify linseed.', 'Oil crop (industrial); also used for fibre (flax).')])
b.M(126, 'Malting barley, durum wheat and cotton are examples of field crops grown mainly for', ['animal feed', 'industrial use', 'soil cover', 'green manure'], 'B',
    ['Step 1: Malting barley → brewing; durum → pasta; cotton → textiles.'], 'Factory crops.', [('What is durum wheat used for?', 'Macaroni and pasta.')])

c = QSet('3.3 Practice — cultural practices', 's33')
c.M(128, 'The first, major operation that breaks up the soil before a crop is', ['secondary tillage', 'primary tillage', 'cultivation', 'harrowing'], 'B',
    ['Step 1: Primary tillage breaks the surface, buries residues and raises infiltration.', 'Step 2: Harrowing and levelling are secondary.'], 'Primary = first.',
    [('Name one problem of no-till.', 'Poor seed placement, clods, stubble blocking planters, or traction problems.')])
c.M(128, 'Poor and untimely land preparation may cause', ['soil erosion', 'serious weed problems', 'better growth', 'both soil erosion and weed problems'], 'D',
    ['Step 1: Late or rough preparation leaves weeds alive and soil exposed.'], 'Late = weedy and eroded.', [('Give two reasons for tillage.', 'Seedbed preparation and weed control (also burying residues, conservation).')])
c.S(129, 'Give three advantages and two problems of no-till.', 'Advantages: keeps soil structure and controls erosion; conserves moisture; lowers costs; less CO₂ released; can give higher yields. Problems: clods; poor seed placement; stubble and weeds block planting; traction problems; residues cannot be fed to animals.',
    ['Step 1: Soil stays covered and undisturbed → structure, water, less erosion.', 'Step 2: But the planter must cut through residues.'], 'Undisturbed soil, harder sowing.',
    [('What is the main problem of minimum tillage?', 'Weed infestation.')])
c.S(131, 'How much nitrogen is in 100 kg of urea, and in 100 kg of CAN?', 'Urea: 46 kg N; CAN: 26 kg N.',
    ['Step 1: Multiply the mass by the % N.', 'Step 2: 100 × 0.46 = 46; 100 × 0.26 = 26.'], 'kg nutrient = kg fertiliser × % ÷ 100.',
    [('How much P₂O₅ is in 50 kg of TSP?', '23 kg.')])
c.S(131, 'A field needs 23 kg of P₂O₅. How many kilograms of DAP supply this, and how much N comes with it?', '50 kg DAP, giving 9 kg N.',
    ['Step 1: DAP is 46 % P₂O₅: 23 ÷ 0.46 = 50 kg.', 'Step 2: N = 0.18 × 50 = 9 kg.'], 'Divide by the percentage to find the fertiliser mass.',
    [('How much urea gives 23 kg N?', '50 kg.')])
c.M(131, 'DAP is called a mixed fertiliser because it', ['contains N, P and K', 'contains two primary nutrients, N and P', 'is organic', 'contains only P'], 'B',
    ['Step 1: Straight = one, mixed = two, compound = all three.', 'Step 2: DAP = 18 % N + 46 % P₂O₅.'], 'Count the primary nutrients.',
    [('Give an example of a straight fertiliser.', 'Urea or TSP.')])
c.TF(131, 'True or false: animal urine contains about 46 % nitrogen.', 'False',
    ['Step 1: 46 % N is the figure for the fertiliser urea.', 'Step 2: Fresh cattle urine has only about 0.5–1.5 % N.'], 'Urea ≠ urine.',
    [('Why should urine be decomposed in the soil or compost before sowing?', 'Fresh urea/ammonia can damage germinating seed.')])
c.S(133, 'Why should farmyard manure be incorporated into the soil and not left on the surface?', 'On the surface it loses nitrogen as ammonia gas (volatilisation); in the soil the ammonium is held by soil colloids and microbes release nutrients to the roots.',
    ['Step 1: Ammonia escapes into the air from surface manure.', 'Step 2: Mixed into soil it is held and used.'], 'Bury it or lose it.',
    [('Why use poultry manure carefully?', 'It is concentrated and its ammonia can scorch crops.')])
c.M(134, 'Placing fertiliser 5–20 cm deep near the roots is called', ['broadcasting', 'sub-surface band placement', 'foliar feeding', 'top-dressing'], 'B',
    ['Step 1: Sub-surface band = below the surface, in a band.'], 'Band = a strip, deep = sub-surface.',
    [('Which method scatters fertiliser over the surface?', 'Broadcasting.')])
c.S(135, 'Explain "dry planting" and why it suits semi-arid areas.', 'Sowing before the rains start, so the seed germinates with the first rain and the crop uses the whole short rainy season.',
    ['Step 1: The season is short.', 'Step 2: Waiting for the soil to be wet wastes days of rain.'], 'Be ready before the rain.',
    [('Why is late sowing risky in semi-arid areas?', 'Water stress at the end of the season causes crop failure.')])
c.S(136, 'List three advantages of row planting over broadcasting.', 'Less seed needed; inter-row cultivation and spraying are possible without damaging plants; better yield (even spacing).',
    ['Step 1: Seed saving.', 'Step 2: Access between rows.', 'Step 3: Even competition → yield.'], 'Rows give room to work.',
    [('Which sowing method uses the most seed?', 'Broadcasting.')])
c.S(137, 'Maize is spaced 80 cm × 25 cm. How many plants per hectare?', '50 000 plants per hectare',
    ['Step 1: Area per plant = 0.80 × 0.25 = 0.20 m².', 'Step 2: 10 000 ÷ 0.20 = 50 000.'], 'Plants/ha = 10 000 ÷ (row × plant spacing in m).',
    [('Sorghum at 75 cm × 15 cm?', 'About 88 900 plants/ha.')])
c.M(137, 'Under irrigation or high fertility the optimum plant population is', ['lower than normal', 'higher than normal', 'unchanged', 'zero'], 'B',
    ['Step 1: More water and nutrients can support more plants.', 'Step 2: Where water is limited, use fewer plants.'], 'More resources, more plants.',
    [('Why is a very high seed rate bad under dry conditions?', 'Seedlings compete for scarce moisture; weak plants and low yield.')])
c.S(138, 'Give four harmful effects and two benefits of weeds.', 'Harmful: compete for nutrients, water, light and space (yield loss); harbour insects and diseases; reduce quality; health problems; water contamination; lower land value. Benefits: animal feed, compost/manure, medicine, oil, thatch, soil and water conservation.',
    ['Step 1: Competition and pests.', 'Step 2: Uses as feed and materials.'], 'Weeds are plants in the wrong place.',
    [('How do you recognise a sedge?', 'Grass-like leaves with a solid triangular stem.')])
c.M(141, 'The disease triangle shows that a disease needs', ['pathogen, host and favourable environment', 'water, light and soil', 'insect, bird and rodent', 'fertiliser, seed and labour'], 'A',
    ['Step 1: All three sides must be present.', 'Step 2: Remove one and there is no disease.'], 'Pathogen + host + weather.',
    [('Why are most plants not attacked by most pathogens?', 'One side of the triangle is missing: they are not susceptible hosts, or the environment is unfavourable.')])
c.M(141, 'Releasing natural enemies such as parasitic wasps to control a pest is', ['mechanical control', 'biological control', 'chemical control', 'cultural control'], 'B',
    ['Step 1: Bio = living agents.'], 'Living enemies = biological.', [('Which control method is recommended as the last choice?', 'Chemical control.')])
c.M(142, 'The cheapest and best long-term method of insect control in crops is', ['chemical sprays', 'resistant varieties', 'hand-picking', 'burning'], 'B',
    ['Step 1: Resistant varieties cost the farmer nothing extra each season.', 'Step 2: They also give good yield and quality.'], 'Breed it once, benefit every year.',
    [('Give two mechanical methods of pest control.', 'Yellow sticky traps, hand removal of infected plants, screens, hand weeding.')])
c.S(143, 'Why is inter-row cultivation done at about knee height in sorghum and maize?', 'To kill weeds growing in the open spaces before the canopy closes; it also loosens the crust so rain infiltrates, conserves moisture, aerates the soil and promotes nitrification.',
    ['Step 1: Weeds compete most early.', 'Step 2: Later the crop shades them out and cultivation would cut roots.'], 'Weed while you still can walk between rows.',
    [('Name three crops in which inter-row cultivation is done.', 'Maize, sorghum, pearl and finger millet.')])
c.S(144, 'How can a farmer tell that a cereal is ready for harvest, and what happens if harvest is late?', 'Plants turn yellow or brown and the grain is hard when bitten. Late harvest causes shattering, bird and rodent losses and lodging.',
    ['Step 1: Colour change.', 'Step 2: Bite test.', 'Step 3: Too late → losses.'], 'Hard grain, brown straw.',
    [('Distinguish traditional and modern harvesting.', 'Traditional: sickle and oxen trampling. Modern: combine harvester cuts, threshes and cleans at once.')])
c.M(146, 'What is the maximum safe moisture content for storing sorghum (Table 3.9)?', ['8 %', '12 %', '18 %', '25 %'], 'B',
    ['Step 1: Table 3.9: sorghum 12 %, wheat 12 %, barley and maize 13 %, soybean 11 %.'], 'Most cereals: 12–13 %.',
    [('Barley?', '13 %.')])
c.M(147, 'Which statement about seed storage is FALSE?', ['Storage life depends on the variety', 'Sound seed stores longer than deteriorated seed', 'Seed deteriorates faster as its moisture content decreases', 'High humidity and temperature shorten storage life'], 'C',
    ['Step 1: Drier seed keeps longer.', 'Step 2: So deterioration increases as moisture increases, not decreases.'], 'Dry and cool keeps seed alive.',
    [('At what temperature and humidity do store pests develop best?', '28–33 °C and 60–80 % RH.')])
c.S(146, '500 kg of sorghum at 18 % moisture is dried to 12 %. What is its new mass?', 'About 466 kg',
    ['Step 1: Dry matter = 500 × 0.82 = 410 kg.', 'Step 2: New mass = 410 ÷ 0.88 ≈ 466 kg.', 'Step 3: About 34 kg of water is removed.'], 'Dry matter does not change.',
    [('1000 kg of wheat at 16 % dried to 12 %?', 'About 955 kg.')])
c.S(147, 'List five features of a good seed store.', 'One door, no windows (openings covered by wire mesh); smooth crack-free floor; sealed against insects and rodents; cool, dry and ventilated; clean; walls sprayed about once a year; first in, first out; labels and records.',
    ['Step 1: Keep pests out.', 'Step 2: Keep it dry and cool.', 'Step 3: Manage stock.'], 'Sealed, dry, clean, recorded.', [('What does "first in, first out" mean?', 'Seed that entered first leaves first.')])

d = QSet('3.4 Practice — cropping systems', 's34')
d.S(149, 'Explain three negative effects of mono-cropping.', 'Soil fertility falls (same nutrients removed each year); diseases and insects of that crop build up; its typical weeds (e.g. Striga in sorghum) multiply; so yields decline.',
    ['Step 1: Nutrient depletion.', 'Step 2: Pest/disease build-up.', 'Step 3: Weed build-up.'], 'Same crop, same problems, every year.',
    [('Give a highland example of mono-cropping.', 'Wheat or barley on the same field every year.')])
d.M(150, 'Two rows of sorghum alternating with one row of cowpea is', ['mixed cropping', 'inter-cropping', 'mono-cropping', 'fallowing'], 'B',
    ['Step 1: Two crops together = mixed cropping in general.', 'Step 2: With a definite row arrangement = inter-cropping.'], 'Arrangement = inter-cropping.',
    [('What is mixed cropping without arrangement?', 'Seeds of two crops mixed and broadcast together.')])
d.S(150, 'List four advantages of inter-cropping.', 'Yield advantage; yield stability (insurance); diverse products; more income; labour spread; soil and water conservation; N from the pulse for the cereal.',
    ['Step 1: More total yield and less risk.', 'Step 2: Better use and protection of soil.'], 'Two baskets are safer than one.', [('Why mix more than two crops in dry areas?', 'To spread risk: some crop survives a drought.')])
d.S(151, 'Sole maize yields 3 t/ha and sole bean 1 t/ha. An intercrop gives 2.4 t maize and 0.5 t bean. Find the LER and say what it means.', 'LER = 2.4/3 + 0.5/1 = 0.8 + 0.5 = 1.3; the intercrop gives 30 % more than sole crops on the same land.',
    ['Step 1: Partial LERs: 0.8 and 0.5.', 'Step 2: Sum = 1.3 > 1.'], 'LER > 1 = intercrop wins.', [('What does LER = 0.9 mean?', 'The intercrop is less productive than sole crops.')])
d.M(151, 'In alley cropping, shading of the crop is prevented by', ['watering the trees', 'pruning the hedgerows before and during cropping', 'planting the crop under the trees', 'removing the crop'], 'B',
    ['Step 1: Hedges are cut back so light reaches the crop.', 'Step 2: Prunings become mulch/green manure.'], 'Prune and mulch.',
    [('Why use leguminous trees in alley cropping?', 'They add nitrogen to the soil.')])
d.M(152, 'Leaving land uncropped for more than one year to restore fertility is', ['crop rotation', 'fallowing', 'mulching', 'relay cropping'], 'B',
    ['Step 1: Fallow = rest.'], 'Fallow = resting land.', [('Why are fallow periods short in Eritrea today?', 'There is not enough land for the growing population.')])
d.S(152, 'Plan a three-year rotation for a lowland field and give two reasons for the order.', 'E.g. sorghum → cowpea or groundnut → sesame (then sorghum again). The legume adds N for the next crop; changing crop families breaks pest, disease and Striga cycles.',
    ['Step 1: Start with a cereal.', 'Step 2: Follow with a legume.', 'Step 3: Add a different family (oil crop).'], 'Cereal → legume → something different.',
    [('A highland rotation?', 'Barley → faba bean → wheat → chickpea.')])

e = QSet('3.5 Practice — horticulture', 's35')
e.M(153, 'Which is NOT a horticultural crop?', ['Onion', 'Orange', 'Taff', 'Rose'], 'C',
    ['Step 1: Onion = vegetable, orange = fruit, rose = flower.', 'Step 2: Taff is a field crop (cereal).'], 'Horticulture = fruit, veg, flowers, spices.',
    [('Which branch deals with vegetables?', 'Olericulture.')])
e.M(155, 'Pomology is the science of', ['flowers', 'fruits', 'cereals', 'vegetables'], 'B',
    ['Step 1: Pomme = apple/fruit.'], 'Pomo = fruit.', [('Floriculture deals with?', 'Flowers and house plants.')])
e.M(156, 'Growing lettuce with roots in a nutrient solution and no soil is', ['open-field production', 'hydroponics', 'a low tunnel', 'mulching'], 'B',
    ['Step 1: Hydro = water, ponos = work: plants grown in water solution.'], 'No soil = hydroponics.', [('In which system are temperature, light and humidity controlled?', 'A greenhouse (glasshouse).')])
e.M(158, 'A nursery that keeps seedlings from a standard nursery for a short time before distribution is', ['a peasant nursery', 'an intermediate (temporary) nursery', 'a commercial nursery', 'an orchard'], 'B',
    ['Step 1: Peasant = farmer\u2019s own; standard = commercial; intermediate = short-term holding.'], 'Intermediate = in between.', [('What is a peasant nursery?', 'Where rural farmers raise their own seedlings.')])
e.S(159, 'List five criteria for selecting a nursery site.', 'Suitable climate and shelter from wind; level land; clean water free of salts; fertile soil; easy road access (and a fence against animals).',
    ['Step 1: Weather and wind.', 'Step 2: Land and soil.', 'Step 3: Water and access.'], 'Climate, land, water, soil, access.',
    [('What is the first step in preparing a nursery site?', 'Site clearing, then levelling and layout.')])
e.M(160, 'In dry areas with little rain, nursery seedlings are best raised in', ['raised beds', 'sunken beds', 'hanging baskets', 'flooded basins'], 'B',
    ['Step 1: Sunken beds (10–15 cm below ground) hold water.', 'Step 2: Raised beds (15–20 cm up) drain water in wet areas.'], 'Sunken saves, raised drains.',
    [('How high is a raised bed?', '15–20 cm above ground.')])
e.S(163, 'Describe the damage weeds cause in a nursery and the cheapest way to control them.', 'They compete strongly for nutrients and water in small containers (and for light if left uncontrolled), and harbour pests; good sanitation is the cheapest control, with hand weeding of young weeds.',
    ['Step 1: Small soil volume → severe competition.', 'Step 2: Prevention by sanitation.'], 'Pull them young.',
    [('Why is grading done in a nursery?', 'To discard poor seedlings that would die or yield poorly; 10–20 % culls is normal.')])
e.M(166, 'In a grafted orange tree, the part that carries the desired fruit variety is the', ['rootstock', 'scion', 'callus', 'cambium'], 'B',
    ['Step 1: Scion = upper part, the variety.', 'Step 2: Rootstock = lower root system.'], 'Scion on top, stock below.',
    [('Which tissue must be matched for a graft to take?', 'The cambium.')])
e.S(167, 'Give the main steps of T-budding.', 'Make a vertical cut 3–4 cm and a horizontal cut 1–2 cm through the stock bark (a T); cut a bud shield with a thin sliver of wood; open the flaps and push in the shield; wrap with tape leaving the bud exposed.',
    ['Step 1: T-cut.', 'Step 2: Shield.', 'Step 3: Insert.', 'Step 4: Wrap.'], 'Cut, slice, slide, tie.',
    [('Which fruit is most commonly budded?', 'Citrus.')])
e.M(169, 'Whip grafting is suitable for stems about', ['1–2 mm thick', '6–12 mm thick', '5–10 cm thick', 'any size'], 'B',
    ['Step 1: Whip grafts join small stems of equal size, 6–12 mm.', 'Step 2: Large stems use bark or cleft grafts.'], 'Pencil-thick for whip.',
    [('Which grafts are used to top-work large trees?', 'Bark and cleft grafting.')])
e.S(173, 'Distinguish softwood and hardwood cuttings.', 'Softwood: young soft shoots 10–15 cm, leaves removed from the lower third, kept under mist. Hardwood: dormant wood 6–20 mm thick, 15–30 cm long, callused in moist peat (upside down) before planting.',
    ['Step 1: Age and softness of wood.', 'Step 2: Length and treatment.'], 'Soft needs mist; hard needs callus.', [('Name three plants easily raised from cuttings.', 'Lantana, grape and coleus.')])
e.M(175, 'Removing a ring of bark from a branch and wrapping it in moist moss and plastic is', ['simple layering', 'air layering', 'mound layering', 'trench layering'], 'B',
    ['Step 1: The branch roots in the air, still on the tree.'], 'Air layering = rooting in the air.',
    [('Which layering pegs a branch down at several points?', 'Serpentine (compound) layering.')])
e.M(178, 'Banana and date palm are usually propagated by', ['seed', 'division of suckers/offshoots', 'whip grafting', 'air layering'], 'B',
    ['Step 1: They form suckers/offshoots at the base.', 'Step 2: These are separated and planted.'], 'Offshoot = division.', [('Name two plants propagated by bulbs.', 'Garlic and onion (also narcissus).')])
e.S(179, 'Give three hardening practices for nursery seedlings.', 'Expose them to below-optimum temperatures (cool areas) or above-optimum (hot areas); reduce water gradually without wilting; move shaded seedlings gradually into full sun.',
    ['Step 1: Temperature.', 'Step 2: Water.', 'Step 3: Light.'], 'Toughen with temperature, water and sun.', [('Why harden seedlings?', 'So they survive transplant shock, root faster and resist drought.')])
e.S(180, 'Indicate the major factors in choosing a site for a horticultural farm.', 'Climate (temperature, rain, light, wind); terrain (altitude, slope); soil and drainage; availability of irrigation water; economics (profit, market).',
    ['Step 1: Physical factors.', 'Step 2: Water.', 'Step 3: Money.'], 'Climate, terrain, soil, water, money.',
    [('Why is site selection more critical for an orchard than for vegetables?', 'Fruit trees are perennial and cannot easily be moved.')])
e.S(183, 'In double digging, how deep is the bed loosened and how often is it repeated?', '45–60 cm deep; every 2–4 years (in medium and clay soils).',
    ['Step 1: Topsoil 28–30 cm + subsoil 15–30 cm.', 'Step 2: Repeat after 2–4 years.'], 'Two spade depths.', [('What pit size is used for most fruit trees?', '60 × 60 × 60 cm (100 cm in hardpan soil).')])
e.S(185, 'When is a tomato seedling ready to transplant?', 'At 4–6 true leaves, 15–20 cm tall with a pencil-thick stocky stem, after about 3–6 weeks in warm climates.',
    ['Step 1: Count true leaves.', 'Step 2: Check height and stem thickness.'], '4–6 true leaves.', [('Why are old seedlings not recommended?', 'Greater transplant shock; roots are damaged more.')])
e.S(186, 'Give three benefits of mulching.', 'Reduces evaporation and runoff; keeps soil temperature and moisture even; suppresses weeds (organic mulch also adds organic matter).',
    ['Step 1: Water saving.', 'Step 2: Temperature.', 'Step 3: Weeds.'], 'A blanket for the soil.', [('Give one organic and one inorganic mulch.', 'Straw (or banana leaves) and plastic sheet.')])
e.S(187, 'A farmer harvests 300 kg of tomatoes and loses 30 % on the way to market. How many kilograms reach the market?', '210 kg',
    ['Step 1: Loss = 0.30 × 300 = 90 kg.', 'Step 2: Left = 300 − 90 = 210 kg.'], 'Remaining = total × (1 − loss).',
    [('With only 10 % loss?', '270 kg.')])
e.S(187, 'How does post-harvest handling affect the quality and quantity of horticultural products?', 'Bad handling (bruising, heat, delay, wrong packing) causes losses up to 50 % and poor quality; good handling (harvest in cool hours, clean, sort, grade, pack in crates, quick shaded transport) keeps produce fresh and saleable.',
    ['Step 1: Produce is alive and perishable.', 'Step 2: Each step either protects or damages it.'], 'Gentle, cool and quick.',
    [('Which needs boxes rather than sacks: potato or tomato?', 'Tomato.')])

QS = a.items + b.items + c.items + d.items + e.items

GLOSSARY = [
    ('Monocot', 'A flowering plant with one cotyledon in the seed (cereals, onion).', 101),
    ('Dicot', 'A flowering plant with two cotyledons in the seed (pulses, tomato).', 101),
    ('Node', 'The point on a stem where a leaf and bud are attached.', 101),
    ('Cambium', 'Layer of dividing cells between xylem and phloem; must be matched in grafting.', 103),
    ('Rhizome', 'A horizontal underground stem, e.g. ginger.', 103),
    ('Leaf axil', 'The angle between the petiole and the stem, where a bud sits.', 104),
    ('Photoperiod', 'Day length, which controls flowering in many plants.', 115),
    ('Hypogeal germination', 'Germination in which the cotyledons stay below the soil.', 117),
    ('Epigeal germination', 'Germination in which the cotyledons are lifted above the soil.', 117),
    ('Viability', 'The ability of a seed to germinate.', 117),
    ('Centre of diversity', 'A region where a crop shows great genetic variation.', 122),
    ('Green manure', 'A crop ploughed in while green to improve the soil.', 125),
    ('Straight fertiliser', 'A fertiliser with only one primary nutrient, e.g. urea.', 131),
    ('Disease triangle', 'Pathogen + susceptible host + favourable environment = disease.', 141),
    ('Land equivalent ratio', 'Sum of intercrop yields divided by sole-crop yields; above 1 means the intercrop is better.', 151),
    ('Alley cropping', 'Crops grown in alleys between pruned hedgerows of trees or shrubs.', 151),
    ('Scion', 'The upper part of a graft that carries the desired variety.', 166),
    ('Rootstock', 'The lower part of a graft that forms the root system.', 166),
    ('Hardening', 'Gradually toughening seedlings before transplanting.', 178),
]
TIPS = [('Old leaves yellow first = a mobile nutrient (N, P, K, Mg); young leaves first = Ca, S or micronutrients.', 110),
        ('Fertiliser maths: kg of nutrient = kg of fertiliser × % ÷ 100; to find fertiliser, divide the nutrient by the %.', 131),
        ('Plants per hectare = 10 000 ÷ (row spacing × plant spacing, both in metres).', 137),
        ('Raised beds drain (wet areas); sunken beds save water (dry areas).', 160)]
IDEAS = [('npk', '16 essential elements; NPK primary', 'l3_1', 'agri11-u3-c03'), ('germ', 'Epigeal vs hypogeal', 'l3_1', 'agri11-u3-ad-germ-tb'),
         ('dtri', 'Disease triangle', 'l3_3', 'agri11-u3-ad-dt-fig'), ('graft', 'Scion on rootstock', 'l3_5', 'agri11-u3-c46')]



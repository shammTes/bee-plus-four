r"""Grade 12 Unit 2 — Forestry and Wildlife (pp. 88-157): forest–wildlife interactions, status, classification, roles,
deforestation, planting, enclosures, regeneration, parkland agroforestry, wildlife, conservation efforts, challenges."""
from common import set_unit, T, RM, MN, TB, DG, ST, WK, QSet
from svglib import Fig, INK, BLUE, RED, GREEN, PURPLE, ORANGE, GREY, FILL
from agrilib import (box, tlines, wrap, flow, hflow, cycle, leader, ground, grass_tufts, sorghum, cow, goat, camel, person,
                     sun, cloud, tree, BROWN, SOIL, LEAF, LEAF2, STRAW, WATER, ROCK)

UID = 'agri12-u2'
set_unit(UID)


# ------------------------------------------------------------------ figures
def f_interact():
    f = Fig(340, 262)
    f.title('How two species affect each other', 13)
    rows = [('Mutualism', '+', '+', 'sagla fig and its wasp pollinator'), ('Commensalism', '+', '0', 'a bird nesting in a tree'),
            ('Antagonism', '+', '−', 'tick on a cow; fox eating a lamb'), ('Neutralism', '0', '0', 'neither is affected'),
            ('Amensalism', '0', '−', 'one is harmed, the other unaffected'), ('Competition', '−', '−', 'weeds and crops for light, water')]
    f.text(124, 40, 'A', 12, INK).text(152, 40, 'B', 12, INK)
    for i, (nm, a, b, ex) in enumerate(rows):
        y = 50 + i * 34
        f.rect(6, y, 328, 28, GREY, 0.8, '#FBF7F0', 5)
        f.text(12, y + 18, nm, 11.5, INK, 'start')
        for x, v in ((124, a), (152, b)):
            c = GREEN if v == '+' else (RED if v == '−' else GREY)
            f.circle(x, y + 14, 10, c, 1.6, FILL.get(c, '#eee')).text(x, y + 19, v, 14, c)
        tlines(f, 170, y + 14, wrap(ex, 30), 10, INK, 'start', False)
    return f


def f_foodweb():
    f = Fig(340, 270)
    sun(f, 30, 30, 14)
    f.text(56, 34, 'sunlight', 11, ORANGE, 'start')
    box(f, 90, 56, 160, 34, 'Producers: acacia, sagla fig, grass', GREEN, 11.5)
    box(f, 20, 120, 140, 34, 'Herbivores: kudu, dik-dik, monkeys', ORANGE, 11)
    box(f, 180, 120, 140, 34, 'Seed + nectar eaters: birds, bees', ORANGE, 11)
    box(f, 90, 184, 160, 34, 'Carnivores: leopard, jackal, eagle', RED, 11.5)
    box(f, 90, 232, 160, 30, 'Decomposers: fungi, bacteria', BROWN, 11.5)
    f.arrow(48, 44, 120, 56, ORANGE, 1.6, 6)
    f.arrow(140, 90, 100, 119, INK, 1.5, 6).arrow(200, 90, 240, 119, INK, 1.5, 6)
    f.arrow(100, 154, 140, 183, INK, 1.5, 6).arrow(240, 154, 200, 183, INK, 1.5, 6)
    f.path('M90 247 L40 247 L40 74', BROWN, 1.4)
    f.arrow(40, 74, 88, 74, BROWN, 1.4, 6)
    f.text(46, 200, 'nutrients', 10, BROWN, 'start', False).text(46, 212, 'back to soil', 10, BROWN, 'start', False)
    return f


def f_cover():
    f = Fig(340, 220)
    f.title('Forest cover of Eritrea (% of land)', 13)
    data = [(1912, 30), (1952, 11), (1960, 5), (1997, 1)]
    base, x0 = 180, 50
    f.line(x0, base, 320, base, INK, 1.4).line(x0, base, x0, 34, INK, 1.4)
    for v in (10, 20, 30):
        y = base - v * 4.6
        f.line(x0 - 4, y, 320, y, '#E6E0D6', 1).text(x0 - 8, y + 4, str(v), 10, GREY, 'end', False)
    for i, (yr, v) in enumerate(data):
        x = 80 + i * 64
        h = v * 4.6
        f.rect(x, base - h, 40, h, GREEN, 1.4, FILL[GREEN], 2)
        f.text(x + 20, base - h - 6, f'{v} %', 12, GREEN).text(x + 20, base + 16, str(yr), 11, INK, 'middle', False)
    f.text(185, 212, 'Forests cover about 30 % of the world\'s land', 10.5, GREY, 'middle', False)
    return f


def f_veg():
    f = Fig(340, 300)
    f.title('Vegetation of Eritrea (% of land, Table 2.3)', 12.5)
    rows = [('Bushland', 42.7), ('Wooded grassland', 20.3), ('Barren land', 14.4), ('Open woodland', 7.6), ('Agricultural land', 6.8),
            ('Closed woodland', 3.6), ('Riverine forest', 1.5), ('Closed-medium forest', 0.5), ('Open forest', 0.3), ('Mangrove', 0.1)]
    for i, (nm, v) in enumerate(rows):
        y = 30 + i * 26
        f.text(128, y + 13, nm, 11, INK, 'end')
        w = max(2, v * 4.2)
        c = GREEN if 'forest' in nm or nm == 'Mangrove' else (ORANGE if 'Barren' in nm else (BROWN if 'Agri' in nm else LEAF2))
        f.rect(134, y + 2, w, 16, '#5E7F4A', 0.8, c if c.startswith('#') else FILL.get(c, '#ddd'), 3)
        f.text(138 + w, y + 14, f'{v}', 10.5, INK, 'start', False)
    f.text(170, 296, 'All true forest together: under 2.5 %', 11, RED)
    return f


def f_plants():
    f = Fig(340, 200)
    ground(f, 160, 0, 340, SOIL, 14)
    tree(f, 60, 160, 120, LEAF, kind='round')
    f.text(60, 186, 'TREE', 12, INK).text(60, 198, 'one main trunk + crown', 10, GREY, 'middle', False)
    for dx in (-14, -4, 6, 16):
        f.path(f'M{172 + dx * 0.4} 160 C{172 + dx} 130 {172 + dx * 1.6} 110 {172 + dx * 2} 96', '#6B4A2B', 2.2)
        f.circle(172 + dx * 2, 96, 13, None, 0, LEAF)
    f.text(172, 186, 'SHRUB', 12, INK).text(172, 198, 'several woody stems', 10, GREY, 'middle', False)
    grass_tufts(f, [270, 286, 302], 160, LEAF, 1.6)
    f.circle(286, 134, 5, None, 0, '#E6C23A')
    f.text(286, 186, 'HERB', 12, INK).text(286, 198, 'no woody stem', 10, GREY, 'middle', False)
    return f


def f_profile():
    f = Fig(340, 300)
    f.title('Forest types across Eritrea (west to east, sketch)', 12)
    pts = [(0, 200), (40, 196), (80, 190), (120, 160), (160, 110), (200, 70), (225, 66), (250, 90), (275, 150), (300, 196), (340, 204)]
    d = 'M0 222 ' + ' '.join(f'L{x} {y}' for x, y in pts) + ' L340 222 Z'
    f.path(d, '#8A6A4A', 1.4, '#E8D6B8')
    f.rect(304, 197, 36, 25, None, 0, '#9CC3E6')
    for x, y in ((24, 198), (96, 182)):
        tree(f, x, y, 26, '#8FAA5A', kind='acacia')
    f.path('M44 196 C48 190 56 190 60 196', WATER, 3)
    tree(f, 52, 194, 22, '#5E8F4A')
    for x, y in ((188, 82), (210, 68), (232, 70)):
        tree(f, x, y, 26, '#3E6B3A')
    for x, y in ((258, 100), (270, 126)):
        tree(f, x, y, 26, '#3F7F3A')
    for x in (310, 324):
        tree(f, x, 200, 12, '#2F7A4A')
    labels = [(50, 196, 74, 244, 'Western lowlands', 'acacia woodland, bush; doum', 'palm, tamarix by rivers', GREEN),
              (210, 70, 150, 274, 'Highlands', 'dry montane: juniper,', 'African olive', GREEN),
              (264, 112, 252, 244, 'Eastern escarpment', 'Semenawi Bahri', 'forest', GREEN),
              (318, 200, 300, 274, 'Coast', 'mangroves', '', BLUE)]
    for x, y, tx, ty, a, b, c, col in labels:
        f.line(x, y, tx, ty - 12, GREY, 0.9)
        f.text(tx, ty, a, 10.5, col)
        f.text(tx, ty + 12, b, 9.5, GREY, 'middle', False)
        if c:
            f.text(tx, ty + 23, c, 9.5, GREY, 'middle', False)
    return f


def f_classes():
    f = Fig(340, 290)
    f.title('Ways of classifying forests', 13)
    rows = [('Age', 'even-aged (regular) / uneven-aged'), ('Species', 'pure (monoculture) / mixed'), ('Regeneration', 'high (seed) / coppice / plantation'),
            ('Function', 'productive / protective / recreational'), ('Growing stock', 'normal / abnormal'), ('Logging', 'accessible / inaccessible'),
            ('Human influence', 'primary / secondary'), ('Canopy', 'closed / open')]
    for i, (a, b) in enumerate(rows):
        y = 26 + i * 32
        box(f, 6, y, 110, 26, a, [GREEN, BLUE, ORANGE, PURPLE, BROWN, GREY, RED, GREEN][i], 11)
        f.text(124, y + 17, b, 10.5, INK, 'start', False)
    return f


def f_canopy():
    f = Fig(340, 190)
    for k, (title, n_, r) in enumerate([('Closed forest', 22, 19), ('Open forest', 7, 15)]):
        x0 = 6 + k * 170
        f.rect(x0, 26, 158, 128, GREY, 1.2, '#F1E8C9' if k else '#E3EDD6', 6)
        f.text(x0 + 79, 18, title, 12.5, INK)
        import random
        rnd = random.Random(3 + k)
        if k == 0:
            pts = [(x0 + 18 + (i % 5) * 31 + (8 if (i // 5) % 2 else 0), 42 + (i // 5) * 26) for i in range(20)]
        else:
            pts = [(x0 + 30, 50), (x0 + 110, 60), (x0 + 60, 100), (x0 + 130, 128), (x0 + 28, 136)]
        for (x, y) in pts:
            f.circle(x, y, r, '#2F5F2A', 1, '#5E8F4A')
        if k:
            grass_tufts(f, [x0 + 20 + i * 24 for i in range(6)], 80, LEAF, 0.7)
    tlines(f, 85, 172, ['crowns touch; little grass'], 10.5, GREEN, 'middle', False)
    tlines(f, 255, 172, ['crowns cover ≥ 10 %;', 'continuous grass, fire risk'], 10.5, ORANGE, 'middle', False)
    return f


def f_water():
    f = Fig(340, 250)
    for k in range(2):
        x0 = 6 + k * 170
        f.rect(x0, 6, 158, 238, GREY, 1.2, '#F7FAFD', 6)
        f.text(x0 + 79, 22, 'Forested slope' if not k else 'Deforested slope', 12, GREEN if not k else RED)
        cloud(f, x0 + 79, 44, 0.7, rain=True)
        f.path(f'M{x0} 120 L{x0 + 158} 200 L{x0 + 158} 244 L{x0} 244 Z', '#7A4E2D', 1.2, SOIL if k else '#8E6B45')
        if not k:
            for i in range(4):
                tree(f, x0 + 20 + i * 36, 130 + i * 18, 34, LEAF, kind='round')
            for i in range(4):
                f.arrow(x0 + 30 + i * 34, 150 + i * 18, x0 + 30 + i * 34, 178 + i * 18, WATER, 1.6, 5)
            f.text(x0 + 79, 226, 'water soaks in;', 10, '#FFFFFF', 'middle', False)
            f.text(x0 + 79, 238, 'springs keep flowing', 10, '#FFFFFF', 'middle', False)
        else:
            for i in range(3):
                f.line(x0 + 30 + i * 40, 136 + i * 20, x0 + 54 + i * 40, 148 + i * 20, '#5A3A1E', 1.4)
            f.arrow(x0 + 20, 118, x0 + 150, 190, WATER, 3, 9)
            tlines(f, x0 + 70, 110, ['fast runoff', 'carries soil'], 10.5, BLUE)
            f.text(x0 + 79, 226, 'floods, then dry springs;', 10, '#FFFFFF', 'middle', False)
            f.text(x0 + 79, 238, 'silt fills dams', 10, '#FFFFFF', 'middle', False)
    return f


def f_roles():
    f = Fig(340, 280)
    f.rect(6, 6, 160, 268, BLUE, 1.6, FILL[BLUE], 8)
    f.rect(174, 6, 160, 268, GREEN, 1.6, FILL[GREEN], 8)
    f.text(86, 24, 'INTANGIBLE', 12.5, BLUE).text(86, 39, 'hard to price', 10.5, INK, 'middle', False)
    f.text(254, 24, 'TANGIBLE', 12.5, GREEN).text(254, 39, 'can be priced', 10.5, INK, 'middle', False)
    left = ['oxygen; absorb CO₂', 'clean the air', 'cool, shade, windbreak', 'sound barrier', 'soil + water conservation', 'wildlife habitat', 'sacred places, inspiration']
    right = ['timber, poles', 'firewood, charcoal', 'rivers for hydro-power', 'gums, resins, incense', 'fruits, honey', 'medicine, fibres', 'raw materials (paper)']
    for i, (a, b) in enumerate(zip(left, right)):
        y = 62 + i * 30
        f.text(86, y, a, 10.5, INK, 'middle', False)
        f.text(254, y, b, 10.5, INK, 'middle', False)
    return f


def f_defor():
    f = Fig(340, 300)
    f.title('Deforestation: causes and consequences', 12.5)
    causes = ['Clearing for farms', 'Firewood + charcoal', 'Wood for houses (hidmo)', 'Overgrazing', 'Over-harvesting gum, fruit', 'No tree tenure', 'Drought, climate change', 'War']
    for i, c in enumerate(causes):
        y = 28 + i * 33
        box(f, 6, y, 130, 27, c, RED if i < 6 else ORANGE, 10.5)
        f.arrow(137, y + 13, 162, 150, GREY, 1, 4)
    box(f, 164, 128, 60, 46, 'Forest loss', BROWN, 11.5)
    cons = ['Soil erosion', 'Floods, then dry springs', 'Silted dams', 'Lost species and habitats', 'Less fuelwood', 'Warmer, drier climate']
    for i, c in enumerate(cons):
        y = 40 + i * 40
        box(f, 236, y, 98, 32, c, PURPLE, 10.5)
        f.arrow(225, 151, 235, y + 16, GREY, 1, 4)
    return f


def f_affor():
    f = Fig(340, 200)
    for k, (title, a, b, c) in enumerate([('Afforestation', 'never forest, or bare for 20+ years', 'plant', 'new forest'),
                                          ('Reforestation', 'forest cut for timber', 'replant', 'forest again')]):
        y = 30 + k * 86
        f.text(10, y - 8, title, 12.5, GREEN if not k else BLUE, 'start')
        box(f, 6, y, 100, 50, a, GREY, 10.5)
        f.arrow(108, y + 25, 132, y + 25, INK, 1.6, 6).text(120, y + 17, b, 10, INK, 'middle', False)
        if k:
            for i in range(4):
                f.rect(146 + i * 16, y + 34, 6, 10, '#6B4A2B', 0, '#6B4A2B')
        for i in range(4):
            tree(f, 148 + i * 16, y + 46, 18 if not k else 14, LEAF2, kind='round')
        f.arrow(220, y + 25, 244, y + 25, INK, 1.6, 6)
        for i in range(3):
            tree(f, 262 + i * 26, y + 50, 44, LEAF, kind='round')
        f.text(290, y + 64, c, 10.5, GREEN, 'middle', False)
    f.text(170, 196, 'Stumps in the field = reforestation', 10.5, GREY, 'middle', False)
    return f


def f_seedling():
    f = Fig(340, 230)
    for k, (title) in enumerate(['Containerised (polypot)', 'Bare-root']):
        x = 85 + k * 170
        f.text(x, 20, title, 12, GREEN if not k else ORANGE)
        f.line(x, 120, x, 60, '#5A4128', 2.4)
        for s_ in (-1, 1):
            f.path(f'M{x} {80} C{x + s_ * 10} 70 {x + s_ * 22} 70 {x + s_ * 28} 78 C{x + s_ * 20} 84 {x + s_ * 10} 84 {x} 80Z', '#2F5F2A', 1, LEAF)
            f.path(f'M{x} {96} C{x + s_ * 10} 88 {x + s_ * 20} 88 {x + s_ * 24} 94 C{x + s_ * 18} 100 {x + s_ * 8} 100 {x} 96Z', '#2F5F2A', 1, LEAF)
        if not k:
            f.path(f'M{x - 26} 120 L{x - 22} 186 L{x + 22} 186 L{x + 26} 120 Z', '#333', 1.2, '#4A4A4A')
            f.path(f'M{x - 22} 124 L{x - 19} 182 L{x + 19} 182 L{x + 22} 124 Z', None, 0, '#8E6B45')
            for d in (-10, 0, 10):
                f.path(f'M{x} 124 C{x + d} 140 {x + d * 1.4} 160 {x + d} 178', '#E8D6B8', 1.2)
            f.text(x + 34, 160, 'root ball', 10, GREY, 'start', False).text(x + 34, 172, 'stays moist', 10, GREY, 'start', False)
        else:
            for d in (-18, -8, 0, 8, 18):
                f.path(f'M{x} 120 C{x + d * 0.5} 140 {x + d} 160 {x + d * 1.3} 186', '#8B5A2B', 1.6)
            f.text(x + 30, 150, 'roots in air:', 10, RED, 'start', False).text(x + 30, 162, 'dry out fast', 10, RED, 'start', False)
    tlines(f, 85, 214, ['higher survival on dry sites;', 'heavy, costlier'], 10.5, INK, 'middle', False)
    tlines(f, 255, 214, ['light, cheap, easy to transport;', 'lower survival'], 10.5, INK, 'middle', False)
    return f


def f_pit():
    f = Fig(340, 240)
    f.title('Planting pit and micro-basin on a slope', 12.5)
    f.path('M0 70 L340 190 L340 240 L0 240 Z', '#7A4E2D', 1.2, SOIL)
    f.path('M150 128 L150 160 C150 172 200 176 210 160 L210 150', '#5A3A1E', 1.6, '#C9A27E')
    f.path('M210 150 C240 156 250 178 240 186', '#5A3A1E', 3)
    f.line(240, 180, 270, 140, GREY, 0.9)
    f.text(266, 124, 'semi-circular', 10.5, BROWN, 'start').text(266, 136, 'earth bund', 10.5, BROWN, 'start')
    f.line(180, 160, 180, 120, '#5A4128', 2.2)
    for s_ in (-1, 1):
        f.path(f'M180 132 C{180 + s_ * 8} 124 {180 + s_ * 16} 124 {180 + s_ * 20} 130 C{180 + s_ * 14} 136 {180 + s_ * 6} 136 180 132Z', '#2F5F2A', 1, LEAF)
    f.path('M60 98 L150 130', WATER, 2.4, dash=True)
    f.text(70, 84, 'V-channel leads runoff in', 10.5, BLUE, 'start')
    f.line(150, 172, 210, 172, INK, 1).text(180, 186, '30 cm', 10.5, INK)
    f.line(222, 130, 222, 166, INK, 1).text(226, 148, '30 cm', 10.5, INK, 'start')
    f.text(20, 228, 'Pot 10 × 15 cm: pit 2 × pot height ≈ 30 × 30 cm', 10.5, '#FFFFFF', 'start')
    return f


def f_spacing():
    f = Fig(340, 220)
    f.title('Spacing and trees per hectare', 13)
    for k, (sp, n_) in enumerate([(2, 2500), (3, 1111)]):
        x0 = 20 + k * 170
        g = 20 if sp == 2 else 30
        cnt = 6 if sp == 2 else 4
        for i in range(cnt):
            for j in range(cnt):
                f.circle(x0 + i * g + 10, 44 + j * g, 5, '#2F5F2A', 1, LEAF)
        f.line(x0 + 10, 44 + cnt * g - 6, x0 + 10 + g, 44 + cnt * g - 6, RED, 1.4).text(x0 + 10 + g / 2, 44 + cnt * g + 8, f'{sp} m', 10.5, RED)
        f.text(x0 + 60, 196, f'{sp} m × {sp} m', 12, INK)
        f.text(x0 + 60, 212, f'10 000 ÷ {sp * sp} = {n_} trees/ha', 10.5, GREEN)
    return f


def f_succession():
    f = Fig(340, 210)
    f.title('Enclosure on a hillside: what happens', 12.5)
    stages = [('Year 0', 'bare, eroded; grazing stopped'), ('Year 1', 'grasses come back'), ('Year 2–3', 'bushes sprout; grass ready to cut'), ('Later', 'trees, more wildlife')]
    for i, (a, b) in enumerate(stages):
        x = 6 + i * 84
        f.path(f'M{x} 150 L{x + 80} 110 L{x + 80} 150 Z', '#7A4E2D', 1, SOIL)
        if i >= 1:
            grass_tufts(f, [x + 20, x + 40, x + 60], 140 - (i >= 1) * 0, LEAF, 0.8)
        if i >= 2:
            for xx in (x + 30, x + 56):
                f.circle(xx, 132 - (xx - x) * 0.3, 7, None, 0, LEAF2)
        if i >= 3:
            tree(f, x + 46, 128, 40, LEAF, kind='round')
            tree(f, x + 66, 118, 34, LEAF, kind='round')
        f.text(x + 42, 168, a, 11.5, INK)
        tlines(f, x + 42, 190, wrap(b, 15), 9.5, GREY, 'middle', False)
    return f


def f_stages():
    return cycle(['Seed', 'Germination: seedling', 'Sapling', 'Young (vegetative) tree', 'Flowering tree', 'Pollination and seed set',
                  'Seed dispersal'], 340, 350, bw=86, bh=42, size=9.5, centre='Light, moisture, nutrients and animals act at every step')


def f_seedtree():
    f = Fig(340, 240)
    f.title('Seed-tree method: where to leave trees', 12.5)
    f.arrow(10, 150, 60, 150, BLUE, 3, 9).text(14, 138, 'wind', 11, BLUE, 'start')
    for r in range(3):
        x = 90 + r * 100
        for j in range(4):
            tree(f, x, 96 + j * 40, 26, '#3E6B3A')
        if r < 2:
            f.line(x, 222, x + 100, 222, RED, 1.2).text(x + 50, 234, '2 × height (50 m)', 10, RED)
    f.line(306, 96, 306, 136, ORANGE, 1.2).text(312, 120, '1 × h', 10, ORANGE, 'start')
    f.text(190, 44, 'rows at right angles to the wind', 10.5, INK, 'middle', False)
    return f


def f_parkland():
    f = Fig(340, 220)
    f.title('Parkland agroforestry (Anseba / Debub)', 12.5)
    ground(f, 180, 0, 340, SOIL, 40)
    for x in range(12, 340, 16):
        f.line(x, 180, x, 140, '#5E8F4A', 1.6)
        f.path(f'M{x} 162 C{x - 6} 156 {x - 10} 158 {x - 12} 162 M{x} 152 C{x + 6} 146 {x + 10} 148 {x + 12} 152', '#5E8F4A', 1.4)
        f.ellipse(x, 135, 3.5, 7, '#7A4E2D', 0.8, '#B5651D')
    for x in (70, 250):
        f.path(f'M{x} 180 L{x} 110', '#6B4A2B', 5)
        for d in (-14, 14):
            f.path(f'M{x} 116 L{x + d} 96', '#6B4A2B', 3)
        f.ellipse(x, 90, 34, 16, '#2F5F2A', 1, '#6E9B4A')
    f.text(70, 66, 'Faidherbia albida', 10.5, GREEN).text(250, 66, 'Balanites (desert date)', 10.5, GREEN)
    f.text(160, 206, 'Now 10–20 trees/ha; target 40–60 trees/ha', 10.5, '#FFFFFF')
    return f


def f_wildclass():
    f = Fig(340, 250)
    box(f, 120, 6, 100, 26, 'Wildlife', GREEN, 12.5)
    box(f, 14, 50, 150, 28, 'Vertebrate animals', ORANGE, 11.5)
    box(f, 186, 50, 140, 28, 'Wild plants', LEAF, 11.5)
    f.line(170, 32, 89, 49, INK, 1.2).line(170, 32, 256, 49, INK, 1.2)
    for i, (a, b) in enumerate([('Mammals', 'leopard, kudu, elephant'), ('Birds', 'ostrich, bustard, eagles'), ('Reptiles', 'snakes, tortoises'), ('Amphibians', 'frogs, toads')]):
        y = 96 + i * 36
        box(f, 14, y, 76, 28, a, ORANGE, 10.5)
        f.text(96, y + 18, b, 9.5, INK, 'start', False)
    box(f, 200, 96, 120, 40, 'Non-vascular: algae, mosses', LEAF, 10.5)
    box(f, 200, 150, 120, 40, 'Vascular: ferns, trees, herbs', LEAF, 10.5)
    f.text(170, 244, 'By habitat: aquatic (fresh, marine) or terrestrial', 10.5, BLUE)
    return f


def f_decline():
    f = Fig(340, 250)
    f.title('Why wildlife declines', 13)
    items = [('Habitat loss', 'farms, settlements, fragmentation'), ('Hunting / overkill', 'faster than animals breed'),
             ('Illegal trade', 'pets, "medicine" parts'), ('Alien species', 'mesquite, beles crowd out natives'),
             ('War', 'fire, cutting, hunting, flight'), ('Cultural beliefs', 'e.g. killing snakes'),
             ('Recurrent drought', 'water sources dry up'), ('Chain extinction', 'one loss pulls down another')]
    for k, (a, b) in enumerate(items):
        x = 6 + (k % 2) * 168
        y = 28 + (k // 2) * 54
        box(f, x, y, 160, 26, a, RED if k < 6 else ORANGE, 10.5)
        f.text(x + 80, y + 40, b, 9.5, GREY, 'middle', False)
    return f

def f_dpsir():
    f = hflow(['Driving force: farmland expands', 'Pressure: habitat destroyed', 'State: wild area converted', 'Impact: wildlife lose home, raid crops',
               'Response: policy, awareness, protected areas'], 340, bh=56, size=10.5, rows=2, title='DPSIR chain (Figure 2.6)', steps=True)
    return f


def f_iucn():
    f = Fig(340, 270)
    f.title('Six IUCN categories of protected area', 12.5)
    rows = [('I', 'Strict nature reserve / wilderness', 'least human use'), ('II', 'National park', 'large ecosystems, visitors'),
            ('III', 'Natural monument', 'a cave, an ancient grove'), ('IV', 'Habitat / species management', 'active care of a species'),
            ('V', 'Protected landscape', 'people + nature over time'), ('VI', 'Sustainable-use area', 'resources used wisely')]
    for i, (a, b, c) in enumerate(rows):
        y = 28 + i * 40
        w = 320 - i * 22
        f.rect(10, y, w, 34, GREEN, 1.2, FILL[GREEN] if i % 2 == 0 else '#F3F8EE', 5)
        f.text(26, y + 22, a, 12, GREEN)
        f.text(48, y + 15, b, 11, INK, 'start')
        f.text(48, y + 28, c, 9.5, GREY, 'start', False)
    f.text(330, 266, 'lower = more use allowed', 10, GREY, 'end', False)
    return f


def f_stove():
    f = Fig(340, 200)
    f.title('Traditional and Adhanet improved stove', 12.5)
    for i, (nm, e, c) in enumerate([('Traditional (3 stones)', 10, ORANGE), ('Improved (Adhanet)', 21, GREEN)]):
        y = 44 + i * 50
        f.text(130, y + 18, nm, 11, INK, 'end')
        f.rect(136, y, e * 5.5, 28, c, 1.4, FILL[c], 4)
        f.text(140 + e * 5.5, y + 19, f'{e} % efficient', 11, c, 'start')
    f.text(170, 160, 'Same cooking with about half the wood', 11.5, INK)
    f.text(170, 180, 'Saves about 0.6 t of CO₂ per stove each year', 10.5, GREY, 'middle', False)
    return f


def f_map():
    f = Fig(340, 300)
    f.title('Protected areas (sketch map, not to scale)', 12)
    pts = [(36.44, 14.3), (36.55, 15.0), (36.97, 16.25), (37.0, 17.0), (38.0, 17.6), (38.6, 18.0), (39.1, 16.9), (39.25, 15.9), (39.45, 15.55),
           (39.73, 15.2), (40.0, 15.0), (40.5, 14.75), (41.2, 14.1), (41.7, 13.6), (42.3, 13.2), (42.7, 12.9), (43.12, 12.7), (42.4, 12.47),
           (41.6, 13.4), (40.8, 14.1), (40.1, 14.45), (39.5, 14.55), (38.9, 14.5), (38.4, 14.45), (37.9, 14.85), (37.5, 14.2), (37.1, 14.3)]
    X = lambda lo: 14 + (lo - 36.3) * 46
    Y = lambda la: 30 + (18.2 - la) * 46
    f.poly([(X(a), Y(b)) for a, b in pts], '#7A6A58', 1.4, '#F1E8D6')
    f.rect(X(39.1) + 4, Y(18.2), 340 - X(39.1) - 4, 40, None, 0, '#FFFFFF')
    f.text(250, 70, 'Red Sea', 12, BLUE)
    sites = [(37.3, 14.6, 'Gash-Setit: elephants', 'end'), (38.95, 15.55, 'Semenawi Bahri: forest', 'up'), (40.25, 15.0, 'Buri Peninsula: wild ass', 'start'),
             (38.4, 16.8, 'Yob + Nakfa: Nubian ibex', 'start')]
    for lo, la, t, an in sites:
        x, y = X(lo), Y(la)
        f.circle(x, y, 6, RED, 2, '#FFFFFF').circle(x, y, 2.4, None, 0, RED)
        f.text(x + 10, y + {'start': 4, 'end': 20, 'up': -8}[an], t, 10.5, RED, 'start')
    f.circle(X(38.93), Y(15.33), 3, None, 0, INK)
    f.text(X(38.93) - 6, Y(15.33) + 4, 'Asmara', 10, INK, 'end', False)
    f.circle(X(39.45), Y(15.61), 3, None, 0, INK)
    f.text(X(39.45) + 6, Y(15.61) + 14, 'Massawa', 10, INK, 'start', False)
    return f


DIAGRAMS = {
    'interact': (f_interact(), 'Types of interaction between species (Table 2.1)', 90),
    'foodweb': (f_foodweb(), 'Energy and nutrient flow in a forest', 89),
    'cover': (f_cover(), 'Decline of forest cover in Eritrea (Table 2.2)', 91),
    'veg': (f_veg(), 'Vegetation types of Eritrea (Table 2.3)', 93),
    'plants': (f_plants(), 'Tree, shrub and herb', 96),
    'profile': (f_profile(), 'Forest types of Eritrea from west to east', 99),
    'classes': (f_classes(), 'Criteria for classifying forests', 96),
    'canopy': (f_canopy(), 'Closed and open forest seen from above', 97),
    'roles': (f_roles(), 'Intangible and tangible roles of forests', 101),
    'water': (f_water(), 'Forests and the water cycle on a slope', 102),
    'defor': (f_defor(), 'Causes and consequences of deforestation', 105),
    'affor': (f_affor(), 'Afforestation and reforestation', 107),
    'seedling': (f_seedling(), 'Containerised and bare-root seedlings', 109),
    'pit': (f_pit(), 'Planting pit with micro-catchment', 112),
    'spacing': (f_spacing(), 'Spacing and number of trees per hectare', 112),
    'succession': (f_succession(), 'Recovery of an enclosure', 116),
    'stages': (f_stages(), 'Life stages of a tree (Figure 2.3)', 120),
    'seedtree': (f_seedtree(), 'Placing seed trees against the prevailing wind', 121),
    'parkland': (f_parkland(), 'Parkland agroforestry (Figure 2.4)', 123),
    'wildclass': (f_wildclass(), 'Classification of wildlife', 129),
    'decline': (f_decline(), 'Causes of wildlife decline', 132),
    'dpsir': (f_dpsir(), 'DPSIR analysis of human–wildlife conflict (Figure 2.6)', 138),
    'iucn': (f_iucn(), 'IUCN protected-area categories', 141),
    'stove': (f_stove(), 'Efficiency of improved stoves', 148),
    'map': (f_map(), 'Protected areas of Eritrea', 149),
}

# ------------------------------------------------------------------ 2.1 introduction
L1 = [
    T('=agri12-u2-c01', '2.1.1 Forests and wildlife depend on each other', 88,
      '**Forestry** = the art and science of managing forests, tree plantations and related resources so they can be used **sustainably** (without using them up). **Wildlife** = all wild (non-domesticated) animals, plants and other organisms.',
      '**Key words:**',
      '- **Habitat:** the place where a species lives (a gazelle in open bushland, colobus monkeys in the Semenawi Bahri forest).',
      '- **Niche:** the way of life of a population in its habitat: what it eats, when it is active and what eats it.',
      '- **Ecosystem:** a community of living things interacting with the non-living environment (water, heat, light, soil, air, landforms).',
      '**Energy and nutrients link them.** Green plants (**autotrophs**) trap sunlight in photosynthesis. Herbivores eat plants, carnivores eat herbivores, and **saprophytes** (fungi, bacteria) decompose dead matter, returning nutrients to the soil through the carbon and nitrogen cycles. The network of feeding links is the **food web**.',
      '**Animals help forests too:** birds and bats **pollinate** flowers and **disperse seeds**; dung fertilises the soil; predators keep herbivores from destroying young trees.'),
    DG('web-fig', 'A forest food web', 89, 'foodweb'),
    DG('int-fig', 'Six kinds of interaction', 90, 'interact',
       '+ = benefits, − = harmed, 0 = not affected. The sagla fig and its tiny wasps cannot live without each other.'),
    T('=agri12-u2-c02', '2.1.2 History and present status', 91,
      'Forests cover about **30 %** of the world\'s land, but **less than 1 %** of Eritrea. Cover fell from **30 % in 1912** to **11 % (1952)**, **5 % (1960)** and **about 1 % (1997)**.',
      '**Why it fell:** clearing land for crops, overgrazing, wood for building, timber for industry, firewood, and recurrent drought.',
      '**What remains** is scattered (fragmented): closed and open forest, riverine forest, mangroves, woodland, bushland, grassland, parkland on farms, and barren land (which still has fungi and algae).',
      'Closed to open forest survives mainly in **Semenawi Bahri** (the green belt of the eastern escarpment) and along rivers. **Bushland** is by far the largest type (42.7 %).',
      'When forest goes, wildlife lose their habitat and many species become **endangered** or **extinct**.'),
    DG('cover-fig', 'From 30 % to 1 % in 85 years', 91, 'cover'),
    DG('veg-fig', 'What covers Eritrea\'s land today', 93, 'veg'),
    TB('trees', 'Endangered indigenous trees and their uses (Table 2.4)', 93, ['Tree (Tigrinya)', 'Scientific name', 'Main uses'],
       [['Dma (baobab)', 'Adansonia digitata', 'fruit, medicine'], ['Mekie (desert date)', 'Balanites aegyptiaca', 'fruit, forage, firewood, soap, medicine'],
        ['Meker\' (frankincense)', 'Boswellia papyrifera', 'incense, fodder, medicine'], ['Awhi', 'Cordia africana', 'fruit, timber, bee forage, mulch, soil conservation'],
        ['Tambuk\'', 'Croton macrostachyus', 'firewood, tools, drums, bees'], ['Zwawe\'', 'Erythrina abyssinica', 'drums, mortars, hedges, bees'],
        ['Sagla', 'Ficus sycomorus', 'fruit, shade, beehives; village sacred tree'], ['Dae\'ro', 'Ficus vasta', 'shade, gum; village sacred tree'],
        ['Humer (tamarind)', 'Tamarindus indica', 'fruit, charcoal, furniture, medicine'], ['M\'leo', 'Ximenia americana', 'fruit, oil, soap, dye']], layout='cards'),
    WK('wk-cover', 'Worked example — how fast was the loss?', 91,
       'Forest cover fell from 30 % in 1912 to 11 % in 1952. What was the average loss per year, and what share of the 1912 forest was gone?',
       ['Loss = 30 − 11 = **19 percentage points** over 1952 − 1912 = **40 years**.', 'Per year = 19 ÷ 40 ≈ **0.5 points a year**.', 'Share lost = 19 ÷ 30 ≈ **63 %** of the 1912 forest gone in 40 years.'],
       'About 0.5 percentage points a year; nearly two-thirds of the 1912 forest was lost by 1952.'),
    'agri12-u2-tbl1', 'agri12-u2-wrk1', 'agri12-u2-wrk2', 'agri12-u2-chk1', 'agri12-u2-chk73', 'agri12-u2-l2-1-r3r1',
]

# ------------------------------------------------------------------ 2.2 forests
L2 = [
    'agri12-u2-c03', 'agri12-u2-c04',
    T('=agri12-u2-c05', 'Forest, tree, shrub and herb', 96,
      'A **forest** is a large area where trees grow densely, forming a complex community of plants and wild animals.',
      '- **Tree:** a perennial woody plant with **one main trunk** and a crown (e.g. juniper, sagla).',
      '- **Shrub:** a low woody perennial with **several stems** and no single trunk (e.g. many acacias on the escarpment).',
      '- **Herb:** a plant with **no permanent woody stem** (grasses, wild flowers).',
      'A **woodland** has trees more widely spaced than a forest, so the canopy is open and grass grows underneath.'),
    DG('plants-fig', 'Tree, shrub, herb', 96, 'plants'),
    T('=agri12-u2-c06', '2.2.1 Classifying forests', 96,
      'There is no single system; foresters use several criteria:',
      '- **Age:** even-aged (regular), where all trees have about the same age, or uneven-aged (irregular, a "selection forest").',
      '- **Species:** **pure** (mainly one species; a pure plantation is a **monoculture**, e.g. a eucalyptus woodlot) or **mixed**.',
      '- **Regeneration:** **high forest** (from seed), **coppice forest** (from shoots of cut stumps or root suckers) or **plantation** (from nursery seedlings).',
      '- **Function:** **productive** (wood and non-wood products), **protective** (stream flow, erosion, sand dunes) or **bio-aesthetic / recreational**.',
      '- **Growing stock:** **normal** (age classes give a sustained yield) or **abnormal** (stock is short, e.g. after drought or overgrazing).',
      '- **Logging:** **accessible** (reachable by road, rail, water or cableway) or **inaccessible**.',
      '- **Human influence:** **primary** (untouched, virgin) or **secondary** (regrown after cutting or disturbance, but still with native species).',
      '- **Canopy:** **closed** (crowns nearly touch) or **open** (crowns cover at least 10 %, with a continuous grass layer that allows grazing and fires).',
      'A **climax forest** is the final, stable stage of succession for that climate and soil. **Riparian** forests grow near water (lakes, swamps, springs); **riverine** forests grow along rivers.',
      'In **1978 UNESCO** made one integrated system: **closed forest**, **mixed forest–grassland** and **grassland** formations. Closed forests are either **climatic** (climax: set by climate, e.g. moist and dry montane forest) or **edaphic** (set by local soil or water, e.g. **mangrove** and swamp forest).'),
    DG('cls-fig', 'Eight ways to classify a forest', 96, 'classes'),
    DG('can-fig', 'Closed and open canopy', 97, 'canopy',
       'The textbook puts the closed/open boundary at a stand density of 20 %; FAO uses about 40 % crown cover for closed forest and 10–40 % for open forest.'),
    T('=agri12-u2-c07', '2.2.2 Forest types in Eritrea', 99,
      '**1. Highland forests:** mainly **dry montane forest**, with the conifer **Juniperus procera** (Tsihdi) mixed with broad-leaved **Olea africana** (African olive, Awlie).',
      '**2. Low- and medium-altitude forests:** dry deciduous forest and thickets:',
      '- **mixed woodlands** of acacia with other trees in the **western and south-western lowlands**;',
      '- **bush or shrub land**, short thorny acacia, the **most widespread cover** in Eritrea;',
      '- **grassland to wooded grassland** in the drier parts, with only scattered trees.',
      '**3. Riverine forests** along the **Gash, Barka, Setit and Anseba** rivers: **tamarix** (*Tamarix aphylla*) and **doum palm** (*Hyphaene thebaica*). Commercial farms are clearing them.',
      '**4. Mangroves** on the **Red Sea coast**: the largest are in the **Southern Red Sea** (around Assab), with others between **Tio and Massawa**.'),
    DG('prof-fig', 'From the lowlands to the coast', 99, 'profile'),
    T('=agri12-u2-c08', '2.2.3 The roles of forests', 101,
      '**Intangible roles** (hard to price):',
      '- **Climate:** trees absorb **CO₂** (the main greenhouse gas) and store the carbon in wood (**carbon sequestration**). One leafy tree makes as much **oxygen** in a season as 10 people breathe in a year.',
      '- **Clean air:** leaves trap dust and absorb CO, SO₂ and NO₂.',
      '- **Shade, cooling and windbreaks:** wind behind a row of trees is slower, so crops dry out less.',
      '- **Sound barrier;** trees can also raise house values by about 15 %.',
      '- **Soil and water conservation:** the canopy breaks the force of rain and roots hold the soil, so water **infiltrates slowly**, springs and streams keep flowing in the dry season, and floods and mudslides are reduced.',
      '- **Wildlife habitat** (colobus monkeys, bushbuck, bush pigs, duikers, civets, birds) and **sacred places** around churches and mosques.',
      '**Tangible roles** (can be priced): timber and poles; **firewood and charcoal**; rivers for **hydro-electric power**; non-wood products such as **gum, resin, incense** (frankincense from Boswellia), fruits, **honey**, fibres and medicine; and raw materials for paper and paint.'),
    DG('roles-fig', 'Tangible and intangible roles', 101, 'roles'),
    DG('water-fig', 'Why forested catchments keep springs flowing', 102, 'water'),
    T('=agri12-u2-c09', '2.2.4 Deforestation', 105,
      '**Deforestation** = removal of forest cover. Natural causes include volcanic eruptions and storms. In Eritrea the main causes are **anthropogenic** (human-made):',
      '- **farm expansion**, at first subsistence, then mechanised commercial farms; and population growth pushing farms onto **steep slopes**;',
      '- **wood extraction** for fuel, charcoal and traditional houses: a **hidmo** roof and walls need many poles;',
      '- **overgrazing**: livestock above the **carrying capacity** (the number of animals an area can support without damage) eat the seedlings, so trees do not regenerate;',
      '- **over-harvesting non-wood products** (gum, resin, incense, fruit, bark) faster than the trees can recover;',
      '- **lack of tree tenure**: if nobody owns the trees, nobody protects or plants them;',
      '- **climate change and drought**, less rain and higher temperatures, which kill stressed trees;',
      '- **war**: shelling and fires, and trees cut for firewood and trenches.'),
    DG('def-fig', 'Causes → forest loss → consequences', 105, 'defor'),
    T('=agri12-u2-c10', '2.2.5 Afforestation and reforestation', 107,
      '- **Afforestation:** planting trees to create a forest on land that has **not been forest recently** (no trees for about **20 years**) or never was.',
      '- **Reforestation:** **re-establishing** forest where trees were removed, for example after timber harvest.',
      'Planting is easier where there was forest before, because a **seed bank** in the soil and nearby seed trees help natural regeneration.',
      '**Why plant:** rehabilitate degraded land; restore indigenous vegetation; conserve soil and water; manage watersheds to cut **silt** in dams; and improve parks and riverbanks.',
      'In Eritrea, **students\' summer campaigns** and communities have built thousands of km of hillside terraces, check dams and micro-basins, and planted trees in watersheds above dams, along roads, in school compounds, around churches and mosques, and in martyrs\' cemeteries.'),
    DG('aff-fig', 'Afforestation or reforestation?', 107, 'affor'),
    TB('=agri12-u2-c11', '2.2.6 Containerised or bare-root seedlings?', 109, ['Point', 'Containerised (polypot)', 'Bare-root'],
       [['Survival on dry, poor sites', 'higher', 'lower'], ['Roots during transport', 'protected in the soil ball', 'dry out easily'],
        ['Time and space in nursery', 'less', 'more'], ['Weight and transport', 'heavy; fewer per vehicle', 'light; a planter carries many'],
        ['Cost and skill', 'dearer; root pruning needed', 'cheaper, simpler; good for machines'], ['Planting season', 'longer', 'short'],
        ['Disease', 'soil diseases spread slowly; leaf diseases worse (crowding)', 'root diseases build up in the same nursery soil']],
       '**For Eritrea\'s semi-arid hills, choose containerised seedlings.**', layout='compare'),
    DG('seed-fig', 'Root ball or bare roots', 109, 'seedling'),
    T('plant-steps', 'Planting seedlings step by step', 111,
      '**Plan the nursery first:** the type of nursery and seedlings, how many are needed, the site, equipment, good-quality seed, and the layout.',
      '**1. Site:** choose species that suit the local conditions. Farmers rarely give good cropland to trees, so trees usually go on **degraded, sloping land**.',
      '**2. Site preparation:** clear competing vegetation (less weeding later).',
      '**3. Spacing:** usually **2 m × 2 m = 2 500 trees per hectare**; up to **3 m × 3 m** (about 1 111 per ha) in dry areas, where trees compete for moisture.',
      '**4. Pitting:** dig pits in **semi-circular basins** or on the **contour of terraces**. The pit should be about **twice the pot height** and as wide as it is deep: a 10 × 15 cm pot needs about a **30 × 30 cm** pit. If you dig early, put the topsoil back loosely so rain does not wash it away.',
      '**5. Planting (2.2.7):** plant soon after the **rains start**. Water the seedlings well first. Slit the polythene down one side and keep the soil ball whole. Cut off the bottom 1–2 cm if the roots are coiled. Firm the soil and leave a small basin. On slopes, a V-shaped channel leads runoff into the basin.',
      '**6. Replacement planting:** keep **surplus seedlings** in the nursery and replace dead plants **once, within the first month**.',
      '**7. Care:** water valuable fruit or multipurpose trees in the first phase; avoid **nitrogen fertiliser on legumes** (it stops root nodulation and nitrogen fixation); **weed** around seedlings until they are established.'),
    DG('pit-fig', 'Pit and micro-basin', 112, 'pit'),
    DG('sp-fig', 'Spacing and trees per hectare', 112, 'spacing'),
    WK('wk-trees', 'Worked example — how many seedlings?', 112,
       'A school near Mendefera will plant a 0.6 ha hillside at 2 m × 2 m and keep 10 % extra for replacement. How many seedlings should it order?',
       ['Trees per hectare = 10 000 m² ÷ (2 × 2) m² = **2 500**.', 'For 0.6 ha: 2 500 × 0.6 = **1 500** seedlings.', 'Plus 10 % surplus: 1 500 × 1.10 = **1 650** seedlings.'],
       'About 1 650 seedlings (1 500 to plant plus 150 spare).'),
    T('=agri12-u2-c13', '2.2.8 Enclosures (closures)', 114,
      'An **enclosure** is an area given full or partial protection by stopping human activities such as grazing and cutting, usually on **steep slopes**, until the vegetation recovers. It can be **temporary** or **permanent**.',
      '**Objectives:** natural regeneration; pasture and wood for villagers; protect local plants and animals; less runoff and more infiltration; groundwater recharge; less erosion and less silt in dams downstream.',
      '**Choosing the site** (with the village\'s full consent): far from the settlement; on badly eroded land unsuitable for crops; enough grazing left elsewhere; at least **10 %** remnant vegetation; shallow soils (less than **25 cm**); and no risk of conflict with neighbours. The village council (**baito**) signs a written agreement with the local administration on boundaries and duties.',
      '**Permanent (forest) enclosure:** after **2–3 years** grasses and trees can be harvested. Mark the boundaries, make a **buffer zone**, plant valuable species in gaps, divide into **fire-break blocks**, and let villagers **cut and carry grass**, collect firewood, fruit and medicine, and keep **beehives**.',
      '**Temporary (grass) enclosure:** reseed with palatable grasses; cut **after the grass has seeded**; thin bushes where they shade out the grass; later allow rotational grazing.'),
    DG('succ-fig', 'An enclosure recovering', 116, 'succession'),
    T('=agri12-u2-c14', '2.2.9 Regeneration', 118,
      '**Regeneration** = replacing old plants with young ones of the same species, and their growth from **seed → seedling → sapling → vegetative tree → flowering tree**. Pollination, seed dispersal and germination link the stages, and light, moisture, nutrients and animals affect each one.',
      'Many people believe forests regenerate by themselves. Without management, though, we cannot control **which species** come back or **how long** it takes.',
      '**Natural regeneration:** suits conservation forests; disturb the ecosystem as little as possible.',
      '**Seed-tree method:** at harvest, leave selected **seed trees** that are tall, straight, healthy and good seeders. It suits **light-demanding** species. Control unwanted vegetation, and expose mineral soil for light seeds.',
      '- Leave trees **along the boundary facing the prevailing wind**, which carries the seed across the area.',
      '- Put rows **at right angles to the wind**, about **2 × tree height apart**, with trees in a row about **1 × height apart**. For 25 m junipers: rows 50 m apart, trees 25 m apart.',
      '- **Remove the seed trees** once regeneration is established, or they will suppress it.',
      '- **Avoid** the method where floods are common, on steep slopes or on very shallow soils, where the seed is washed or blown away. It works best on **level, moist land**.'),
    DG('stage-fig', 'Life stages of a tree', 120, 'stages'),
    DG('st-fig', 'Placing the seed trees', 121, 'seedtree'),
    WK('wk-seedtree', 'Worked example — spacing seed trees', 121,
       'Seed trees of Juniperus procera average 18 m tall. How far apart should the rows and the trees within a row be?',
       ['Rows: 2 × height = 2 × 18 = **36 m** apart, at right angles to the wind.', 'Within rows: 1 × height = **18 m** apart.', 'Start with the row on the windward boundary.'],
       'Rows about 36 m apart; trees 18 m apart within each row.'),
    T('=agri12-u2-c15', '2.2.10 Parkland agroforestry', 122,
      '**Agroforestry** combines **trees or shrubs with crops and/or livestock** on the same land, in a mixture or in sequence. It gives more products, more income and a wider range of ecological services, and supports more birds and insects than single-crop farming.',
      '**Parkland** is Eritrea\'s main traditional system: widely spaced, **pollarded** trees scattered across fields of sorghum, pearl millet and teff, with livestock grazing the stubble. Farmers keep **Faidherbia albida, Balanites aegyptiaca and Acacia tortilis** because crops and grass grow under them and they give firewood, fodder, fruit and shade.',
      '**Faidherbia albida** is special: it **drops its leaves in the rainy season**, so it does not shade the crops, and it fixes nitrogen. Yields are often higher under it.',
      '**The problem:** fields have only **10–20 trees per hectare**, against **40–60** needed. Farmers pollard branches for fences and fuel and cut trees for building, without planting new ones or protecting natural seedlings, so the parkland slowly collapses.',
      '**Reducing tree–crop competition:** control tree density, **prune** branches to let light through, and remember that tree roots go deeper than crop roots, although some competition for water and nutrients remains.'),
    DG('park-fig', 'Trees scattered in a sorghum field', 123, 'parkland'),
    TB('park', 'Parkland combinations in Eritrea (Table 2.6)', 124, ['Zoba', 'Trees with crops'],
       [['Anseba', 'Balanites aegyptiaca (desert date) with pearl millet'], ['Gash-Barka', 'Balanites with sorghum; Cordia africana with maize, sorghum, teff; Balanites + Acacia tortilis with teff, sorghum'],
        ['Debub', 'Balanites + Faidherbia albida with teff, finger millet; Faidherbia with teff, sorghum; Balanites with maize'],
        ['Northern Red Sea', 'Olea africana (African olive) with barley']], layout='cards'),
    'agri12-u2-chk74', 'agri12-u2-chk75', 'agri12-u2-wrk4', 'agri12-u2-l2-2-mx1', 'agri12-u2-l2-3-mx1', 'agri12-u2-chk2', 'agri12-u2-chk81', 'agri12-u2-wrk10',
]

# ------------------------------------------------------------------ 2.3 wildlife
L3 = [
    T('=agri12-u2-c16', '2.3.1 Why wildlife matters', 127,
      'People once lived entirely by hunting and gathering, and early hunters probably wiped out some species. Today wildlife gives:',
      '- **Tourism and ecotourism.** Ecotourism is "responsible travel to natural areas that conserves the environment and improves the well-being of local people". It is small-scale and educational, and the income goes to conservation and local communities.',
      '- **Research materials:** genes, medicines and micro-organisms for agriculture and medicine.',
      '- **Conservation education:** wildlife inspires people to protect nature.',
      '- **Heritage:** animals as national and religious symbols. Eritrea\'s camel is on the coat of arms, and sacred groves around churches and mosques are protected.',
      '- **Aesthetic value** and balanced ecosystems.'),
    TB('=agri12-u2-c17', '2.3.2 Classifying wildlife', 129, ['Basis', 'Groups', 'Eritrean examples'],
       [['Animals (vertebrates)', 'mammals, birds, reptiles, amphibians', 'leopard, greater kudu, Soemmerring\'s gazelle; ostrich, Arabian bustard, lesser kestrel; tortoises, snakes; frogs'],
        ['Plants', 'non-vascular (algae, mosses) and vascular (ferns, conifers, flowering plants)', 'algae in pools; juniper, sagla'],
        ['Habitat', 'aquatic (freshwater, marine) or terrestrial (forest, desert, savannah, mountain)', 'dugong and turtles in the Red Sea; Nubian ibex in the northern mountains']], layout='cards'),
    DG('wc-fig', 'Wildlife groups', 129, 'wildclass'),
    T('=agri12-u2-c18', '2.3.3 Causes of wildlife decline', 132,
      '- **Habitat destruction and fragmentation:** farms and settlements break wild land into small islands; populations become isolated and the **carrying capacity** falls.',
      '- **Recurrent drought:** water sources dry up and less-adapted species disappear.',
      '- **Illegal trade:** monkeys and parrots sold as pets; animal parts sold as "medicine".',
      '- **Hunting and overkill:** hunting faster than the population can breed. Slow breeders such as elephants are hit hardest.',
      '- **War:** habitat burnt and cut, animals hunted for food or fleeing across borders.',
      '- **Alien invasive species:** organisms living outside their natural range that upset the native balance. In Eritrea: **mesquite** (*Prosopis juliflora*), **beles** (prickly pear, *Opuntia ficus-indica*), **cocklebur** (*Xanthium*) and **tree tobacco** (*Nicotiana glauca*). Mesquite now chokes riverbanks and grazing land in the lowlands.',
      '- **Cultural beliefs:** for example, killing snakes as symbols of evil.',
      '- **Chain (domino) extinction:** losing one species pulls down those that depend on it.',
      'The textbook also lists the **Holocene mass extinction**: we are living through the sixth great extinction on Earth. This is really the **result** of the causes above, not a separate cause.'),
    DG('dec-fig', 'Eight causes of decline', 132, 'decline'),
    TB('endangered', 'Endangered or locally extinct animals (Table 2.9)', 133, ['Animal', 'Scientific name', 'Tigrinya'],
       [['African elephant', 'Loxodonta africana', 'Harmaz'], ['Leopard', 'Panthera pardus', 'Nebri'], ['African wild ass', 'Equus africanus', 'Adgi bereka'],
        ['Greater kudu', 'Tragelaphus strepsiceros', 'Agazen'], ['Soemmerring\'s gazelle', 'Nanger (Gazella) soemmerringii', 'Telebedu'],
        ['Dorcas gazelle', 'Gazella dorcas', 'Telebedu'], ['Beisa oryx', 'Oryx beisa', 'Salla'], ['Klipspringer', 'Oreotragus oreotragus', 'Sesha'],
        ['Ostrich', 'Struthio camelus', 'Seghen'], ['Dugong', 'Dugong dugon', 'Lam bahri']],
       'The textbook misprints some names: wild ass "Equus equus" (it is *Equus africanus*), oryx "Oryx gazelle" (the Eritrean oryx is *Oryx beisa*), "Gazella doecas" (*dorcas*) and "Ardeotis carabs" (*arabs*).', layout='cards'),
    T('=agri12-u2-c19', '2.3.4 Human–wildlife conflict and the DPSIR chain', 137,
      'As farms push into wild habitat, conflict follows: baboons, porcupines and warthogs raid crops, and hyenas and leopards take livestock. People respond by killing wildlife.',
      'To solve the conflict, look at the **chain of cause and effect** with **DPSIR**:',
      '- **D – Driving forces:** human activities and development, e.g. population growth and expanding farmland.',
      '- **P – Pressure:** what those activities do to the environment, e.g. habitat destruction.',
      '- **S – State:** the resulting condition, e.g. wild land converted to farms, land degradation.',
      '- **I – Impact:** effects on people and nature, e.g. wildlife lose habitat and raid crops; farmers lose harvests.',
      '- **R – Response:** what society does, e.g. land-use policy, awareness, protected areas, better farm productivity so less land is needed.',
      'A response can act at **any link** of the chain.'),
    DG('dp-fig', 'DPSIR chain', 138, 'dpsir'),
    'agri12-u2-chk76', 'agri12-u2-wrk5', 'agri12-u2-chk77', 'agri12-u2-wrk6', 'agri12-u2-l2-5-mx1',
]

# ------------------------------------------------------------------ 2.4 efforts
L4 = [
    T('=agri12-u2-c20', '2.4.1 Community forestry', 140,
      '**Community forestry** = forest management by a community united by common interest or place. The people **own, manage and benefit** from their forests, woodlots and enclosures: they harvest wood and non-wood products and use the income for village development.',
      'Its core is a **sense of ownership**. When villagers plan and benefit, they stop illegal cutting themselves. This **bottom-up** approach works better than orders from above.',
      'Extension workers **mobilise and sensitise** communities by linking conservation to everyday needs: water, fuel, fodder and income.'),
    T('=agri12-u2-c21', '2.4.2 Policies and law', 141,
      '- **1995: National Environment Management Plan for Eritrea (NEMP-E)**, prepared after wide public discussion. It led to hillside tree planting, agroforestry and soil and water conservation.',
      '- **Proclamation 155/2006:** forestry and wildlife conservation and development. It protects endangered and indigenous species, promotes afforestation and reforestation, sets up protected areas, encourages community participation and creates a **Forestry and Wildlife Advisory Board**. Cutting trees needs a **permit**; hunting is regulated; exotic tree imports and forest-product exports are controlled; community and private **woodlots** are encouraged.',
      '- **Proclamation 156/2006:** **plant quarantine**: control of plant pests and diseases, quarantine officers and laboratories, and a Plant Protection Committee.',
      '- **Legal notices:** regulations for forestry permits and wildlife permits. They note the damage done by colonial rule, the 30-year liberation war, recurrent drought and illegal trade.',
      '- **Other steps:** law enforcement; restricted trade in wild plants and animals; environmental education in schools and communities; zoos, animal orphanages and botanical gardens; and local participation.',
      'Note: the textbook first says "two proclamations and four legal notices", then lists **two** legal notices.'),
    DG('iucn-fig', 'IUCN categories', 141, 'iucn'),
    T('cites', 'International conventions: CITES', 143,
      '**CITES** (Convention on International Trade in Endangered Species of Wild Fauna and Flora) was drafted after a **1963** IUCN resolution, agreed in **1973** and came into force on **1 July 1975**. It protects more than **33 000 species**.',
      'Every import, export or re-export of a listed species needs a **permit**. Each member country names a **management authority** (issues the licences) and a **scientific authority** (advises whether the trade harms the species).'),
    TB('=agri12-u2-c22', '2.4.3 Alternative energy to save trees', 146, ['Source', 'Advantages', 'Disadvantages'],
       [['Wind', 'no pollution; renewable; land below can still be farmed; offshore possible', 'intermittent: no wind, no power; large farms spoil the view'],
        ['Solar', 'renewable; no air or water pollution; efficient for heating and lighting; little maintenance; cheap over time', 'little at night or under cloud; power stations are costly to build'],
        ['Geothermal ("earth heat")', 'no harmful by-products if done well; plant runs itself; small footprint', 'bad drilling can release harmful gases and minerals; sites have a limited life'],
        ['Kerosene, LPG, electricity', 'replace firewood and charcoal at home; rural electrification', 'cost; fossil fuels (except hydro or solar electricity)']],
       'Eritrea has strong sunshine and wind, especially on the Red Sea coast around Assab, and geothermal potential in the Danakil (Alid volcano area).', layout='cards'),
    T('stove', 'Improved stoves (Adhanet)', 148,
      'A traditional three-stone fire for baking injera is only **10 % efficient**. The improved **Adhanet** mogogo stove reaches about **21 %**, saving about **half the fuel** and about **0.6 t of CO₂ per stove each year**. By 2004 about **27 000** households in all zobas had them, and the women using them also suffer less smoke.'),
    DG('stove-fig', 'Traditional and improved stoves', 148, 'stove'),
    WK('wk-stove', 'Worked example — wood saved by improved stoves', 148,
       'A family burns 8 kg of wood a day on a 10 %-efficient fire. How much would it burn on a 21 % stove to deliver the same useful heat, and how much is saved in a year?',
       ['Useful heat now = 8 × 10 % = **0.8 kg-equivalent**.', 'With 21 %: wood = 0.8 ÷ 0.21 ≈ **3.8 kg a day**.', 'Saving = 8 − 3.8 = **4.2 kg a day** × 365 ≈ **1 530 kg a year** (about 1.5 t).'],
       'About 3.8 kg a day; about 1.5 tonnes of wood saved per family each year.'),
    T('=agri12-u2-c23', '2.4.4 Protected areas', 149,
      'Enclosures have been set up all over the country. **Cutting live trees, hunting or capturing wildlife and making charcoal are banned.** Communities and students plant trees on hillsides every year.',
      '**Protected areas:**',
      '- **Gash-Setit** (south-west): elephants;',
      '- **Semenawi Bahri** (eastern escarpment): remnant forest and its habitats;',
      '- **Buri Peninsula** (Northern Red Sea coast): **African wild ass**;',
      '- **Yob and Nakfa** (north): **Nubian ibex**.'),
    DG('map-fig', 'Where the protected areas are', 149, 'map'),
    'agri12-u2-chk78', 'agri12-u2-wrk7', 'agri12-u2-chk79', 'agri12-u2-wrk8', 'agri12-u2-l2-4-mx1',
]

# ------------------------------------------------------------------ 2.5 challenges
L5 = [
    T('=agri12-u2-c24', '2.5.1 Poverty', 150,
      'Poverty, population growth and the wish for more income push people to clear forests, cut firewood and overgraze. Agriculture employs most rural people but adds little to GDP because **productivity is low**.',
      '**Ways forward:**',
      '- improve **rural livelihoods** so people depend less on cutting trees;',
      '- **integrated watershed programmes** (terraces, check dams, enclosures, tree planting together);',
      '- change land use: grow cereals on **high-potential** land, and use marginal land for **forestry, beekeeping and high-value crops**;',
      '- fair markets, so farmers earn more from less land.',
      'Low savings and low export earnings limit investment, which is why low-cost, community-based solutions matter.'),
    T('=agri12-u2-c25', '2.5.2 Beliefs and attitudes', 152,
      'Traditional societies respect **sacred places**: the forests around churches and mosques are often the **last remnants** of indigenous vegetation and wildlife.',
      '**Modernisation** sometimes makes people see "wild" as backward, so they clear it. We need to value forests as home to species from microbes to large mammals, and to teach this from childhood. Institutions and laws should support a **culture of conservation**.'),
    T('=agri12-u2-c26', '2.5.3 Ownership and responsibility', 153,
      'A major barrier is weak **land and tree tenure**. The **1994 Land Law** replaced the traditional tenure systems, but much remains to be done to put it into practice, and doubts about who owns forests and wildlife lead to abuse.',
      'Where farmers do not own the trees they plant, they are **reluctant to plant or protect** them.',
      '**Key questions:** Who owns the forests and wildlife? Who manages them? Who benefits, and how? **Private and community ownership with clear rights** usually gives the best care.'),
    RM('u2-err', 'Slips in the Unit 2 textbook', 154,
       '- Table 2.2 is titled "1912–2007" but its data stop at 1997.',
       '- "2 m × 2 m spacing gives 2 500 **species** per hectare" should say 2 500 **trees (plants)**.',
       '- Scientific names: *Ficus sycomorus* (not "sycamorus"); *Tamarix aphylla* (not "apphylla"); *Hyphaene thebaica* (not "Hyphanae thabaica"); *Croton macrostachyus*; and in Table 2.9 *Equus africanus*, *Oryx beisa*, *Gazella dorcas*, *Ardeotis arabs*.',
       '- The legal-notices count is given as four, then two.',
       '- "Holocene mass extinction" is listed as a cause, but it is the outcome of the other causes.'),
    'agri12-u2-chk80', 'agri12-u2-wrk9', 'agri12-u2-l2-5-r2c1', 'agri12-u2-l2-5-r3r1',
]

LESSONS = {'agri12-u2-l2-1': L1, 'agri12-u2-l2-2': L2, 'agri12-u2-l2-3': L3, 'agri12-u2-l2-4': L4, 'agri12-u2-l2-5': L5}
DROP = ['agri12-u2-c12']  # 2.2.7 time for planting: merged into the step-by-step planting card
PATCH = {}

a = QSet('2.1 Practice — forests and wildlife together', 's21')
a.M(90, 'The relationship between the sagla fig and its wasp pollinators is', ['commensalism', 'mutualism', 'parasitism', 'competition'], 'B',
    ['Step 1: The wasp gets food and a place to breed inside the fig.', 'Step 2: The fig gets pollinated.', 'Step 3: Both benefit (+ +) = mutualism.'], 'Both win = mutualism.', [('A bird nesting in a tree that is not affected is…', 'Commensalism (+ 0).')])
a.M(90, 'Weeds and sorghum growing together for light and water show', ['mutualism', 'amensalism', 'competition', 'neutralism'], 'C',
    ['Step 1: Both lose some resources.', 'Step 2: − − = competition.'], 'Both lose = competition.', [('Which interaction is 0 −?', 'Amensalism.')])
a.F(89, 'The way of life of a population in its habitat (what it eats, when it is active) is its ____.', 'niche', ['niche', 'habitat', 'ecosystem', 'biome'],
    ['Step 1: Habitat = the address.', 'Step 2: Niche = the job or profession.'], 'Habitat = where; niche = how.', [('A community plus its non-living environment is a(n)…', 'Ecosystem.')])
a.S(91, 'Describe the trend of forest cover in Eritrea from 1912 to 1997.', 'It fell steadily: 30 % (1912), 11 % (1952), 5 % (1960) and about 1 % (1997).',
    ['Step 1: Quote the figures.', 'Step 2: State the trend: a fall of 29 points, losing about 97 % of the 1912 forest.'], 'Remember 30–11–5–1.', [('Give three causes of the decline.', 'Land clearing for farming, overgrazing, firewood and construction wood (also timber for industry, drought).')])
a.M(93, 'The most widespread vegetation type in Eritrea is', ['closed forest', 'mangrove', 'bushland', 'riverine forest'], 'C',
    ['Step 1: Table 2.3: bushland 42.7 %.', 'Step 2: Forests together are under 2.5 %.'], 'Bush is biggest.', [('Which type covers only about 0.1 %?', 'Mangrove.')])
a.S(89, 'Explain two ways in which wild animals help forests.', 'They pollinate flowers (bees, birds, bats) and disperse seeds (birds, monkeys, antelopes), so trees reproduce; their dung and bodies return nutrients to the soil.',
    ['Step 1: Reproduction help.', 'Step 2: Nutrient cycling.'], 'Pollinate, disperse, fertilise.', [('What role do saprophytes play?', 'They decompose dead matter and recycle nutrients.')])
a.S(91, 'Forest cover fell from 5 % in 1960 to 1 % in 1997. What fraction of the 1960 forest was lost?', '80 %.',
    ['Step 1: Loss = 5 − 1 = 4 points.', 'Step 2: 4 ÷ 5 = 0.8 = 80 %.'], 'Loss ÷ starting value.', [('And from 1912 to 1997?', '29 ÷ 30 ≈ 97 %.')])
a.M(93, 'Boswellia papyrifera (Meker\') is valued mainly for', ['incense (frankincense)', 'dates', 'timber for boats', 'rubber'], 'A',
    ['Step 1: Boswellia is the frankincense tree.', 'Step 2: Its gum resin is incense.'], 'Boswellia = incense.', [('Which tree is the village sacred tree giving fruit and shade?', 'Sagla (Ficus sycomorus); also Dae\'ro (Ficus vasta).')])

b = QSet('2.2 Practice — forests', 's22')
b.M(96, 'A woody plant with several stems and no single trunk is a', ['tree', 'shrub', 'herb', 'climber'], 'B',
    ['Step 1: Tree = one trunk.', 'Step 2: Herb = not woody.', 'Step 3: Shrub = several woody stems.'], 'Shrub = several stems.', [('Define a herb.', 'A plant lacking a permanent woody stem.')])
b.M(96, 'A forest regrowing from the shoots of cut stumps is a', ['high forest', 'coppice forest', 'plantation', 'primary forest'], 'B',
    ['Step 1: Coppice = regrowth from stumps or root suckers.', 'Step 2: High forest = from seed.'], 'Coppice = cut and come again.', [('A pure plantation of one species is called a…', 'Monoculture.')])
b.S(97, 'Distinguish between primary and secondary forests.', 'Primary forests are untouched by people or major disasters (virgin); secondary forests have regrown after cutting or disturbance and differ from the original, though they still contain indigenous species.',
    ['Step 1: Disturbed or not.', 'Step 2: Composition after regrowth.'], 'Primary = first growth.', [('What is a climax forest?', 'A forest at the final, stable stage of succession for that climate and soil.')])
b.M(98, 'In the UNESCO system, mangroves are an example of', ['climatic forest', 'edaphic forest', 'grassland formation', 'montane forest'], 'B',
    ['Step 1: Edaphic = controlled by local soil or water.', 'Step 2: Mangroves depend on salty coastal mud.'], 'Edaphic = soil-made.', [('Name an Eritrean climatic (climax) formation.', 'Dry montane forest of the highlands (juniper and olive).')])
b.M(100, 'The two main trees of the highland dry montane forest are', ['doum palm and tamarix', 'Juniperus procera and Olea africana', 'mangrove and acacia', 'eucalyptus and pine'], 'B',
    ['Step 1: Highland = juniper (conifer) and African olive (broad-leaved).', 'Step 2: Doum palm and tamarix are riverine.'], 'Highland = Tsihdi + Awlie.', [('Where are riverine forests found?', 'Along the Gash, Barka, Setit and Anseba rivers.')])
b.S(102, 'Explain how forests keep springs flowing in the dry season.', 'The canopy and litter break the force of rain and roots open the soil, so water soaks in slowly instead of running off; it recharges groundwater, which feeds springs and streams through the dry months.',
    ['Step 1: Interception.', 'Step 2: Infiltration.', 'Step 3: Groundwater recharge → spring flow.'], 'Soak in, not run off.', [('What happens downstream after deforestation?', 'Floods after rain, silted dams, then dry springs and streams.')])
b.S(101, 'Classify these as tangible or intangible roles of forests: honey, cooling shade, charcoal, carbon sequestration.', 'Tangible: honey, charcoal. Intangible: cooling shade, carbon sequestration.',
    ['Step 1: Tangible = can be sold or priced.', 'Step 2: Intangible = services hard to price.'], 'Can you sell it in a market?', [('What is carbon sequestration?', 'Trees absorbing CO₂ and storing the carbon in wood and soil.')])
b.M(105, 'Livestock numbers above what the land can support without damage exceed its', ['growing stock', 'carrying capacity', 'tree tenure', 'canopy cover'], 'B',
    ['Step 1: Carrying capacity = maximum sustainable number.', 'Step 2: Above it = overgrazing.'], 'Capacity = how much the land can carry.', [('How does overgrazing cause deforestation?', 'Animals eat the seedlings, so trees do not regenerate.')])
b.S(106, 'Why does a lack of tree tenure lead to deforestation?', 'If nobody owns the trees, nobody has a reason to protect or plant them; anyone can cut them, so they are overused.',
    ['Step 1: Ownership gives benefits.', 'Step 2: Benefits motivate care.'], 'No owner, no guardian.', [('Which law replaced traditional land tenure in Eritrea?', 'The 1994 Land Law.')])
b.M(107, 'Planting trees on land with no trees for the last 20 years is', ['reforestation', 'afforestation', 'coppicing', 'enclosure'], 'B',
    ['Step 1: Afforestation = new forest where none was recently.', 'Step 2: Reforestation = replanting after removal.'], 'A for "Absent" forest.', [('Replanting after a timber harvest is…', 'Reforestation.')])
b.S(110, 'Give three advantages of containerised seedlings for Eritrea\'s dry hills.', 'Higher survival on poor, dry sites; roots stay protected in moist soil during transport and planting; a longer planting period (also less nursery time and space).',
    ['Step 1: Survival.', 'Step 2: Root protection.', 'Step 3: Flexibility.'], 'Pot = protection.', [('Give two advantages of bare-root seedlings.', 'Cheaper, lighter to transport, simpler to grow, suited to machines.')])
b.S(112, 'How many trees are needed per hectare at 2.5 m × 2.5 m spacing?', '1 600 trees.',
    ['Step 1: Area per tree = 2.5 × 2.5 = 6.25 m².', 'Step 2: 10 000 ÷ 6.25 = 1 600.'], 'Trees/ha = 10 000 ÷ (spacing × spacing).', [('At 2 m × 2 m?', '2 500 trees/ha.')])
b.S(112, 'What size of pit is needed for a seedling in a 10 × 15 cm polypot, and why?', 'About 30 × 30 cm: the depth should be about twice the pot height, and the width about equal to the depth, so the roots have loose soil to grow into.',
    ['Step 1: 2 × 15 cm = 30 cm deep.', 'Step 2: As wide as it is deep = 30 cm.'], 'Twice the pot.', [('What should be done with coiled roots?', 'Cut off the bottom 1–2 cm of the root ball.')])
b.TF(113, 'Replacement planting should be done several times during the first year.', False,
     ['Step 1: The textbook says replace dead seedlings only once.', 'Step 2: Within the first month after planting.'], 'Once, in month one.', [('Why keep surplus seedlings in the nursery?', 'For replacement planting of dead or diseased plants.')])
b.TF(113, 'Nitrogen fertiliser should be avoided on leguminous tree seedlings.', True,
     ['Step 1: Extra nitrogen stops root nodulation.', 'Step 2: The tree then fixes less nitrogen.'], 'Legumes make their own N.', [('When should seedlings be planted?', 'Soon after the rains start, when more rain can be expected.')])
b.S(115, 'List four conditions for choosing an enclosure site.', 'Far from settlements; badly eroded land unsuitable for crops; enough grazing left elsewhere; at least 10 % remnant vegetation; shallow soils (under 25 cm); no conflict with neighbours; agreed by the village.',
    ['Step 1: Location.', 'Step 2: Land condition.', 'Step 3: Community needs.'], 'Far, eroded, agreed.', [('Who signs the enclosure agreement for the village?', 'The village council (baito), with the local authorities.')])
b.S(117, 'How can villagers benefit from a permanent enclosure without destroying it?', 'By cutting and carrying grass, collecting dead firewood, wild fruits and medicinal plants, and keeping beehives inside it.',
    ['Step 1: No free grazing.', 'Step 2: Controlled harvesting of products.'], 'Cut and carry, not graze.', [('After how many years can grass and trees be harvested?', 'About 2–3 years.')])
b.S(121, 'Seed trees are 20 m tall. How should they be arranged?', 'In rows at right angles to the prevailing wind, 40 m apart (2 × height), with trees 20 m apart in each row (1 × height), starting at the windward boundary.',
    ['Step 1: Rows = 2 × 20 = 40 m.', 'Step 2: In-row = 20 m.', 'Step 3: Windward side.'], '2h between rows, 1h within.', [('Why remove seed trees later?', 'They would suppress the young regeneration.')])
b.M(122, 'The seed-tree method should NOT be used', ['on level, moist land', 'on steep slopes and very shallow soils', 'for light-demanding species', 'in junipers'], 'B',
    ['Step 1: Seeds wash or blow away on steep, flood-prone or shallow sites.', 'Step 2: It works best on level, moist land.'], 'Flat and moist = yes.', [('What is regeneration?', 'Replacement of old plants by young ones of the same species.')])
b.TF(124, 'Most Eritrean parklands already have the recommended 40–60 trees per hectare.', False,
     ['Step 1: Usually only 10–20 trees/ha.', 'Step 2: Target 40–60.'], '10–20 now, 40–60 needed.', [('Why does the tree density keep falling?', 'Pollarding and cutting without planting or protecting new trees.')])
b.S(124, 'Why is Faidherbia albida ideal in sorghum and teff fields?', 'It sheds its leaves in the rainy season, so it does not shade the crops while they grow; it fixes nitrogen and its leaf fall adds organic matter; its pods feed livestock in the dry season.',
    ['Step 1: Reverse leaf phenology.', 'Step 2: Fertility.', 'Step 3: Fodder.'], 'Leafless when crops need light.', [('Name the parkland tree used with barley in Northern Red Sea.', 'Olea africana (African olive).')])
b.TF(157, 'Tree roots are deeper than crop roots, so there is no competition at all between trees and crops.', False,
     ['Step 1: Tree roots are mostly deeper.', 'Step 2: But some roots overlap, so there is still some competition; it is reduced, not removed.'], 'Watch words like "no" and "all".', [('How is light competition reduced?', 'By pruning or pollarding branches.')])

c = QSet('2.3 Practice — wildlife', 's23')
c.S(128, 'Define ecotourism.', 'Responsible travel to natural areas that conserves the environment and improves the well-being of local people.',
    ['Step 1: Travel to nature.', 'Step 2: Conservation.', 'Step 3: Local benefit.'], 'Eco + tourism + people.', [('Give two other values of wildlife.', 'Research materials, conservation education, heritage, aesthetic value.')])
c.M(129, 'Frogs and toads belong to the', ['reptiles', 'amphibians', 'mammals', 'birds'], 'B',
    ['Step 1: Amphibians live in water and on land, with moist skin.'], 'Amphi = both lives.', [('Mosses are ____ plants.', 'Non-vascular.')])
c.M(135, 'Which is an invasive alien tree in Eritrea?', ['Juniperus procera', 'Prosopis juliflora (mesquite)', 'Olea africana', 'Cordia africana'], 'B',
    ['Step 1: Mesquite comes from the Americas.', 'Step 2: It spreads fast and chokes riverbanks and pastures.'], 'Mesquite = alien.', [('Name another invasive plant in Eritrea.', 'Beles (Opuntia ficus-indica), cocklebur (Xanthium), tree tobacco (Nicotiana glauca).')])
c.S(134, 'Why are slow-breeding animals such as elephants most hurt by hunting?', 'Overkill happens when animals are killed faster than they reproduce; slow breeders replace losses slowly, so even moderate hunting makes their numbers fall.',
    ['Step 1: Compare hunting rate with breeding rate.', 'Step 2: Slow breeders have a low replacement rate.'], 'Kill rate > birth rate = decline.', [('What is a domino (chain) extinction?', 'Loss of one species causing the loss of others that depend on it.')])
c.S(132, 'Explain habitat fragmentation and its effect on wildlife.', 'Farms and settlements break a large wild area into small isolated patches; animals are confined to these islands, the carrying capacity falls, populations become small and inbred, and local extinction follows.',
    ['Step 1: Breaking up.', 'Step 2: Isolation.', 'Step 3: Decline.'], 'Fragment = break into pieces.', [('Which protected area is for the African wild ass?', 'Buri Peninsula.')])
c.M(137, 'In DPSIR, "loss of habitat" is an example of', ['driving force', 'pressure', 'response', 'impact'], 'B',
    ['Step 1: The textbook gives habitat loss as a pressure.', 'Step 2: Driving force = the human activity behind it (farm expansion).'], 'D-P-S-I-R in order.', [('Give an example of a response.', 'Policies, awareness campaigns, protected areas.')])
c.S(138, 'A farmer near Gash-Setit loses crops to elephants. Analyse with DPSIR.', 'D: population growth and farm expansion; P: clearing elephant habitat; S: wild land converted to fields; I: elephants raid crops, farmer loses income, elephants may be killed; R: land-use planning, buffer zones, compensation, awareness, protecting the Gash-Setit area.',
    ['Step 1: Name each link.', 'Step 2: Suggest responses that act at several links.'], 'Work along the chain.', [('Why can responses act at any link?', 'Removing any cause or pressure reduces the impact.')])
c.TF(136, 'The textbook\'s "Holocene mass extinction" is a separate cause of wildlife decline, independent of human activity.', False,
     ['Step 1: It is the name for today\'s high extinction rate.', 'Step 2: It results mainly from human causes such as habitat loss and hunting.'], 'An outcome, not a cause.', [('How many great extinctions has Earth had, counting today?', 'Six.')])

d = QSet('2.4–2.5 Practice — efforts and challenges', 's24')
d.S(140, 'What is the key principle of community forestry?', 'Developing a sense of ownership: local communities own, manage and benefit from their forests, so they protect them themselves (bottom-up).',
    ['Step 1: Ownership.', 'Step 2: Management.', 'Step 3: Benefit.'], 'Own it, manage it, gain from it.', [('Why is a bottom-up approach efficient?', 'People act on issues that affect their own lives and livelihoods.')])
d.M(144, 'Proclamation 155/2006 deals with', ['plant quarantine', 'forestry and wildlife conservation and development', 'water rights', 'livestock marketing'], 'B',
    ['Step 1: 155 = forestry and wildlife.', 'Step 2: 156 = plant quarantine.'], '155 forests, 156 pests.', [('When was the National Environment Management Plan prepared?', '1995.')])
d.M(143, 'CITES controls', ['logging inside a country', 'international trade in endangered species', 'carbon emissions', 'fishing quotas'], 'B',
    ['Step 1: Convention on International Trade in Endangered Species.', 'Step 2: Trade needs permits.'], 'T in CITES = Trade.', [('When did CITES come into force?', '1 July 1975.')])
d.M(142, 'An area set aside to protect a cave or ancient grove is a', ['national park', 'natural monument', 'wilderness area', 'protected landscape'], 'B',
    ['Step 1: Natural monuments protect specific features.', 'Step 2: They are usually small, with high visitor value.'], 'Monument = one special feature.', [('How many IUCN categories are there?', 'Six.')])
d.S(147, 'Give one advantage and one disadvantage each of wind and solar power.', 'Wind: renewable and pollution-free, but intermittent. Solar: renewable, clean and low-maintenance, but weak at night or under cloud, and costly to build.',
    ['Step 1: Both are renewable and clean.', 'Step 2: Both are intermittent in their own way.'], 'Clean but not constant.', [('What does geothermal mean?', 'Earth heat.')])
d.S(148, 'A village of 200 households changes from 10 % to 21 % efficient stoves, each household saving 4 kg of wood a day. How much wood is saved per year?', 'About 292 tonnes a year.',
    ['Step 1: 200 × 4 = 800 kg a day.', 'Step 2: 800 × 365 = 292 000 kg ≈ 292 t.'], 'Per day × days.', [('About how much CO₂ does one improved stove save each year?', 'About 0.6 t.')])
d.M(149, 'The Nubian ibex is protected at', ['Gash-Setit', 'Buri Peninsula', 'Yob and Nakfa', 'Dahlak'], 'C',
    ['Step 1: Gash-Setit = elephants.', 'Step 2: Buri = wild ass.', 'Step 3: Yob and Nakfa = Nubian ibex.'], 'Ibex likes the northern mountains.', [('What is protected at Semenawi Bahri?', 'Remnant forests and their habitats.')])
d.S(151, 'Explain why poverty is a challenge to conservation.', 'Poor households depend directly on forests for fuel, building wood, grazing and land; with low savings they cannot invest in alternatives (improved stoves, intensive farming), so they keep clearing and overusing forests.',
    ['Step 1: Dependence.', 'Step 2: No money for alternatives.'], 'Poverty → overuse.', [('Suggest a land-use change that helps.', 'Use marginal land for forestry and beekeeping instead of cereals.')])
d.S(152, 'Why are remnants of indigenous forest often found around churches and mosques?', 'Communities respect these sacred places and do not cut trees there, so they act as sanctuaries for old trees and wildlife.',
    ['Step 1: Belief → protection.', 'Step 2: Protection → survival of remnants.'], 'Sacred = protected.', [('How can modernisation threaten conservation?', 'It can make people see wild land as backward and clear it.')])
d.M(154, 'Which tenure usually gives the best care of trees?', ['open access', 'clear private or community ownership', 'no ownership', 'temporary use rights only'], 'B',
    ['Step 1: Secure rights give a reason to invest.', 'Step 2: Open access leads to overuse.'], 'Secure rights = care.', [('Name the 1994 law on land.', 'The Land Law (Proclamation 58/1994).')])

QS = a.items + b.items + c.items + d.items

GLOSSARY = [
    ('Niche', 'The way of life of a population in its habitat.', 89),
    ('Mutualism', 'Interaction in which both species benefit.', 90),
    ('Monoculture', 'Pure plantation of one species.', 96),
    ('Coppice forest', 'Forest regrown from stump shoots or root suckers.', 96),
    ('Climax forest', 'Final, stable stage of succession for a site.', 97),
    ('Edaphic formation', 'Vegetation controlled by local soil or water, e.g. mangrove.', 98),
    ('Carbon sequestration', 'Storage of carbon taken from the air in wood and soil.', 102),
    ('Carrying capacity', 'The number of animals an area can support without damage.', 106),
    ('Tree tenure', 'Ownership or use rights over trees.', 106),
    ('Afforestation', 'Creating forest where there was none for about 20 years or more.', 107),
    ('Reforestation', 'Re-establishing forest after removal.', 107),
    ('Enclosure', 'Area protected from grazing and cutting so vegetation recovers.', 114),
    ('Seed-tree method', 'Leaving selected trees at harvest to seed the next crop.', 119),
    ('Agroforestry', 'Growing trees together with crops and/or livestock.', 122),
    ('Pollarding', 'Cutting tree branches back to the trunk for wood and fodder.', 123),
    ('Ecotourism', 'Responsible travel to natural areas that conserves nature and helps local people.', 128),
    ('Alien invasive species', 'Organism established outside its home range that harms native ones.', 135),
    ('DPSIR', 'Driving forces – Pressure – State – Impact – Response chain.', 137),
    ('CITES', 'Convention controlling international trade in endangered species.', 143),
]
TIPS = [('Forest cover: 30 % (1912) → 11 → 5 → 1 % (1997).', 91),
        ('Trees per hectare = 10 000 ÷ (spacing × spacing).', 112),
        ('Seed trees: rows 2 × height apart, trees 1 × height apart, across the wind.', 121)]
IDEAS = [('cover', 'Forest cover 30 % → 1 %', 'l2_1', 'agri12-u2-ad-cover-fig'),
         ('plant', 'Plant at 2 × 2 m: 2 500 trees/ha', 'l2_2', 'agri12-u2-ad-plant-steps'),
         ('dpsir', 'DPSIR chain', 'l2_3', 'agri12-u2-ad-dp-fig'),
         ('protect', 'Protected areas of Eritrea', 'l2_4', 'agri12-u2-ad-map-fig'),
         ('tenure', 'Ownership drives conservation', 'l2_5', 'agri12-u2-ad-u2-err')]

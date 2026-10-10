r"""Grade 12 Unit 1 — Livestock Production (pp. 1-87): livestock in Eritrea, classification, digestive systems, breeding,
feeds and feeding, grazing, dairy / beef / poultry / small-ruminant / bee management, housing, restraint, animal health."""
from common import set_unit, T, RM, MN, TB, DG, ST, WK, QSet
from svglib import Fig, INK, BLUE, RED, GREEN, PURPLE, ORANGE, GREY, FILL
from agrilib import (box, tlines, wrap, flow, hflow, cycle, leader, ground, grass_tufts, cow, goat, sheep, camel, hen,
                     person, tree, BROWN, SOIL, LEAF, STRAW, WATER)

UID = 'agri12-u1'
set_unit(UID)
GUT = '#E9B8A3'


# ------------------------------------------------------------------ figures
def f_population():
    f = Fig(340, 262)
    f.title('Livestock in Eritrea (estimated head)', 13)
    rows = [('Goats', 5.0, '5 million', GREEN), ('Poultry', 2.5, '2.5 million', ORANGE), ('Sheep', 2.4, '2.4 million', BLUE),
            ('Cattle', 2.2, '2.2 million', BROWN), ('Donkeys', 0.575, '575 000', PURPLE), ('Camels', 0.368, '368 000', ORANGE),
            ('Mules', 0.009, '9 000', GREY), ('Horses', 0.005, '5 000', GREY)]
    for i, (nm, v, lab, c) in enumerate(rows):
        y = 32 + i * 26
        f.text(70, y + 13, nm, 12, INK, 'end')
        w = max(2, v / 5.0 * 180)
        f.rect(78, y + 2, w, 16, c, 1.2, FILL.get(c, '#ddd'), 3)
        f.text(82 + w, y + 14, lab, 11, INK, 'start', False)
    f.text(170, 248, 'Agriculture is 26 % of GDP; livestock is 15 % of that', 11, GREEN)
    return f


def _hoof(f, x, y, cloven):
    if cloven:
        f.path(f'M{x - 13} {y} C{x - 14} {y - 16} {x - 4} {y - 20} {x - 2} {y - 18} L{x - 2} {y}Z', INK, 1.4, '#6B4A36')
        f.path(f'M{x + 13} {y} C{x + 14} {y - 16} {x + 4} {y - 20} {x + 2} {y - 18} L{x + 2} {y}Z', INK, 1.4, '#6B4A36')
    else:
        f.path(f'M{x - 13} {y} C{x - 14} {y - 18} {x + 14} {y - 18} {x + 13} {y}Z', INK, 1.4, '#6B4A36')
    f.rect(x - 9, y - 34, 18, 16, INK, 1.2, '#C9A27E', 3)


def f_classify():
    f = Fig(340, 300)
    box(f, 110, 6, 120, 26, 'Kingdom Animalia', GREY, 11.5)
    box(f, 110, 44, 120, 26, 'Phylum Chordata', GREY, 11.5)
    f.arrow(170, 32, 170, 43, INK, 1.4, 5)
    box(f, 20, 86, 150, 30, 'Class Mammalia: hair, milk', BLUE, 11.5)
    box(f, 190, 86, 140, 30, 'Class Aves: feathers, eggs', ORANGE, 11.5)
    f.line(170, 70, 95, 85, INK, 1.4).line(170, 70, 260, 85, INK, 1.4)
    box(f, 6, 136, 160, 40, 'Artiodactyla: EVEN-toed (2 hooves)', GREEN, 11.5)
    box(f, 174, 136, 160, 40, 'Perissodactyla: ODD-toed (1 hoof)', PURPLE, 11.5)
    f.line(95, 116, 86, 135, INK, 1.4).line(95, 116, 254, 135, INK, 1.4)
    _hoof(f, 86, 222, True)
    _hoof(f, 254, 222, False)
    f.text(86, 240, 'cloven hoof', 11, GREY, 'middle', False).text(254, 240, 'single hoof', 11, GREY, 'middle', False)
    tlines(f, 86, 266, ['cattle, sheep, goats,', 'pigs, camels'], 11.5, GREEN)
    tlines(f, 254, 266, ['horses, donkeys,', 'mules'], 11.5, PURPLE)
    f.text(260, 128, 'chickens: Galliformes', 10.5, ORANGE, 'middle', False)
    f.text(170, 296, 'Correction: the textbook swaps "even" and "odd" here', 10.5, RED)
    return f


def f_ruminant():
    f = Fig(340, 262)
    f.title('Four-compartment stomach of a cow', 13)
    f.g('k1 k2 k3 k4 k5')
    f.path('M150 30 L174 66', '#8A5A44', 7)
    f.text(144, 34, 'oesophagus', 10.5, GREY, 'end', False)
    f.end()
    f.g(hl='k1')
    f.path('M30 90 C30 60 160 56 170 80 C182 120 176 196 120 206 C64 214 26 190 28 150 Z', '#7A4E2D', 2, '#E7C9A6')
    f.text(100, 132, 'RUMEN', 14, BROWN).text(100, 150, '80 % of adult stomach', 10.5, INK, 'middle', False)
    f.text(100, 164, 'microbes ferment fibre', 10.5, INK, 'middle', False)
    f.end()
    f.g(hl='k2')
    f.circle(206, 84, 22, '#7A4E2D', 2, '#F0D5B5')
    for i in range(3):
        for j in range(3):
            f.rect(193 + j * 9, 72 + i * 8, 8, 7, '#B88A66', 0.8)
    f.text(236, 66, 'reticulum', 11.5, BROWN, 'start').text(236, 80, 'honeycomb wall;', 10, GREY, 'start', False).text(236, 92, 'traps nails, wire', 10, GREY, 'start', False)
    f.end()
    f.g(hl='k3')
    f.ellipse(262, 144, 26, 20, '#7A4E2D', 2, '#E9C29C')
    for k in range(-2, 3):
        f.line(252 + k * 6, 128, 252 + k * 6 + 8, 160, '#A97A55', 0.9)
    f.text(262, 178, 'omasum: "many leaves",', 10.5, BROWN).text(262, 190, 'absorbs water', 10, GREY, 'middle', False)
    f.end()
    f.g(hl='k4')
    f.path('M200 214 C220 200 290 200 312 222 C318 236 296 246 270 242 C240 240 214 236 200 214 Z', '#B0503A', 2, '#F2B8A8')
    f.text(258, 228, 'ABOMASUM', 11.5, RED).text(258, 258, 'true stomach: acid + enzymes', 10.5, RED)
    f.end()
    f.g('k2 k5')
    f.curve_arrow(196, 58, 150, 24, -14, ORANGE, 1.8, 6)
    f.text(240, 34, 'cud back to the mouth', 10.5, ORANGE, 'middle', False)
    f.end()
    f.g('k3 k4 k5')
    f.arrow(222, 102, 244, 126, INK, 1.6, 6)
    f.arrow(262, 164, 262, 168, INK, 1.2, 1)
    f.arrow(282, 160, 290, 202, INK, 1.6, 6)
    f.end()
    f.g('k5')
    f.arrow(200, 222, 150, 236, INK, 1.6, 6).text(144, 246, 'to small intestine', 10.5, INK, 'end', False)
    f.end()
    return f


def f_calf():
    f = Fig(340, 210)
    f.title('Size of each compartment (% of total stomach)', 12.5)
    data = [('Newborn', [25, 5, 10, 60]), ('2–4 months', [65, 5, 10, 20]), ('Adult', [80, 5, 7.5, 7.5])]
    cols = ['#C99A6E', '#E0C08A', '#9CC3A0', '#D9786A']
    for i, (lab, v) in enumerate(data):
        y = 36 + i * 46
        f.text(78, y + 18, lab, 11.5, INK, 'end')
        x = 84
        for j, p in enumerate(v):
            w = p * 2.4
            f.rect(x, y, w, 28, '#fff', 1, cols[j])
            if p >= 10:
                f.text(x + w / 2, y + 18, f'{p:g}', 10.5, INK)
            x += w
    for j, nm in enumerate(['rumen', 'reticulum', 'omasum', 'abomasum']):
        f.rect(16 + j * 82, 180, 12, 12, '#fff', 1, cols[j])
        f.text(32 + j * 82, 190, nm, 10.5, INK, 'start', False)
    f.text(170, 206, 'Milk skips the rumen through the oesophageal groove', 10.5, GREEN)
    return f


def _tract(f, parts, y, x0=12, x1=328, h=26):
    """parts = [(label, rel width, colour)] laid left to right as one tube"""
    tot = sum(p[1] for p in parts)
    x = x0
    out = []
    for lab, w, c in parts:
        ww = (x1 - x0) * w / tot
        f.rect(x, y, ww, h, '#7A4E2D', 1.2, c, 5)
        out.append((x, ww))
        x += ww
    return out


def f_pig():
    f = Fig(340, 260)
    f.title('Pig: a monogastric (one-stomach) tract', 13)
    steps = [('Mouth', 'teeth chew; saliva starts starch digestion', '#F3D1C2'), ('Oesophagus', 'muscle waves push food', '#EAC0AE'),
             ('Stomach', 'acid + enzymes (cardiac / pyloric valves)', GUT), ('Duodenum', 'bile (liver) + pancreatic juice', '#E7A893'),
             ('Jejunum + ileum', 'most nutrients absorbed', '#E39C86'), ('Large intestine', 'caecum, colon: water absorbed', '#D9C3A0'),
             ('Rectum + anus', 'faeces leave the body', '#CDB794')]
    for i, (a, b, c) in enumerate(steps):
        y = 28 + i * 31
        f.rect(16, y, 120, 25, '#7A4E2D', 1.2, c, 6)
        f.text(76, y + 17, a, 11, INK)
        f.text(144, y + 17, b, 10.5, INK, 'start', False)
        if i:
            f.arrow(76, y - 6, 76, y - 1, INK, 1.3, 4)
    f.text(170, 252, 'Like humans: needs grain, little fibre', 11, GREEN)
    return f


def f_poultry():
    f = Fig(340, 260)
    f.title('Hen: digestive tract (no teeth)', 13)
    parts = [('Beak', 'picks food; no chewing', '#F2D49B'), ('Crop', 'stores food', '#F3D1C2'),
             ('Proventriculus', 'acid + pepsinogen', GUT), ('Gizzard', 'muscle + grit grind grain', '#C9876E'),
             ('Small intestine', 'bile, pancreatic juice; absorption', '#E39C86'), ('Two caeca', 'bacteria ferment leftovers', '#D9C3A0'),
             ('Short colon', 'water re-absorbed', '#CDB794'), ('Cloaca', 'faeces + urine leave together', '#BFAF95')]
    for i, (a, b, c) in enumerate(parts):
        y = 26 + i * 28
        f.rect(16, y, 120, 23, '#7A4E2D', 1.2, c, 6)
        f.text(76, y + 16, a, 11, INK)
        f.text(144, y + 16, b, 10.5, INK, 'start', False)
        if i:
            f.arrow(76, y - 5, 76, y - 1, INK, 1.3, 4)
    hen(f, 310, 64, 0.9)
    return f


def f_breeding():
    f = Fig(340, 270)
    box(f, 110, 6, 120, 28, 'Breeding', GREEN, 13)
    box(f, 6, 54, 156, 44, 'Selection: keep the best, CULL the poor', BLUE, 11.5)
    box(f, 178, 54, 156, 44, 'Cross-breeding: bring in better genes', ORANGE, 11.5)
    f.line(170, 34, 84, 53, INK, 1.4).line(170, 34, 256, 53, INK, 1.4)
    f.text(84, 112, 'first step; keeps adapted', 10.5, GREY, 'middle', False).text(84, 125, 'local breeds', 10.5, GREY, 'middle', False)
    f.text(256, 112, 'exotic bull or AI;', 10.5, GREY, 'middle', False).text(256, 125, 'must improve the environment', 10.5, GREY, 'middle', False)
    f.text(170, 152, 'Systems of mating', 12.5, INK)
    box(f, 6, 164, 156, 34, 'INbreeding: related animals', PURPLE, 11.5)
    box(f, 178, 164, 156, 34, 'OUTbreeding: unrelated', RED, 11.5)
    tlines(f, 84, 226, ['close-breeding', 'line-breeding'], 11, PURPLE, 'middle', False)
    tlines(f, 256, 230, ['out-crossing, grading up,', 'cross-breeding,', 'species hybridisation'], 11, RED, 'middle', False)
    return f


def f_cross():
    f = Fig(340, 200)
    cow(f, 70, 96, 0.95, '#A0663B', hump=True)
    f.text(70, 112, 'Barka cow (zebu, humped)', 11, BROWN)
    f.text(70, 126, 'hardy, low milk', 10.5, GREY, 'middle', False)
    cow(f, 260, 96, 0.95, '#2A2A2A', hump=False, face=-1)
    f.ellipse(258, 64, 10, 7, None, 0, '#FFFFFF')
    f.ellipse(282, 58, 7, 6, None, 0, '#FFFFFF')
    f.ellipse(236, 70, 6, 5, None, 0, '#FFFFFF')
    f.text(262, 112, 'Holstein-Friesian (or AI)', 11, INK)
    f.text(262, 126, 'high milk, needs good care', 10.5, GREY, 'middle', False)
    f.text(165, 72, '×', 26, RED)
    f.arrow(165, 132, 165, 152, INK, 1.8, 7)
    box(f, 70, 154, 190, 40, 'Cross: more milk than Barka, hardier than Holstein', GREEN, 11.5)
    return f


def f_nutrients():
    f = Fig(340, 236)
    box(f, 120, 6, 100, 28, 'Feed', BROWN, 13)
    box(f, 20, 54, 110, 28, 'Water', BLUE, 12)
    box(f, 190, 54, 130, 28, 'Dry matter (DM)', ORANGE, 12)
    f.line(170, 34, 75, 53, INK, 1.4).line(170, 34, 255, 53, INK, 1.4)
    box(f, 130, 104, 120, 40, 'Organic matter (contains C)', GREEN, 11.5)
    box(f, 258, 104, 76, 40, 'Inorganic: ash', GREY, 11.5)
    f.line(255, 82, 190, 103, INK, 1.4).line(255, 82, 296, 103, INK, 1.4)
    for i, (nm, d) in enumerate([('Carbohydrate', 'energy'), ('Protein', 'growth (N)'), ('Fat', '2.25 × energy'), ('Vitamins', 'tiny amounts')]):
        x = 6 + i * 82
        f.rect(x, 168, 78, 44, [ORANGE, RED, PURPLE, BLUE][i], 1.6, FILL[[ORANGE, RED, PURPLE, BLUE][i]], 8)
        f.text(x + 39, 186, nm, 11, INK).text(x + 39, 202, d, 10, GREY, 'middle', False)
        f.line(190, 144, x + 39, 167, GREY, 1.1)
    f.text(296, 162, 'minerals', 11, GREY)
    f.text(170, 230, 'Six nutrients: water + 5 in the DM', 11, GREEN)
    return f


def f_dm():
    f = Fig(340, 168)
    f.title('3 kg fresh alfalfa, 65 % water', 13)
    f.rect(20, 40, 300 * 0.65, 40, '#3F7FBF', 1.2, '#9CC3E6', 4)
    f.rect(20 + 300 * 0.65, 40, 300 * 0.35, 40, '#7A4E2D', 1.2, '#E8CF96', 4)
    f.text(20 + 300 * 0.325, 65, 'water 65 % = 1.95 kg', 11.5, INK)
    f.text(20 + 300 * 0.825, 59, 'DM 35 %', 11.5, INK).text(20 + 300 * 0.825, 73, '= 1.05 kg', 11.5, INK)
    f.text(170, 108, 'DM = fresh weight × (100 − moisture %) ÷ 100', 11.5, INK)
    f.text(170, 128, '= 3 × 35 ÷ 100 = 1.05 kg DM per day', 11.5, GREEN)
    f.text(170, 156, 'Compare feeds by their DM, not by fresh weight', 10.5, GREY, 'middle', False)
    return f


def f_feeds():
    f = Fig(340, 270)
    f.rect(6, 6, 160, 258, GREEN, 1.6, FILL[GREEN], 8)
    f.rect(174, 6, 160, 258, BROWN, 1.6, '#F3E9DC', 8)
    f.text(86, 26, 'CONCENTRATES', 12.5, GREEN).text(86, 42, 'fibre < 18 %, dense', 10.5, INK, 'middle', False)
    f.text(254, 26, 'ROUGHAGES', 12.5, BROWN).text(254, 42, 'fibre > 18 %, bulky', 10.5, INK, 'middle', False)
    for i, (a, b) in enumerate([('Energy-rich', 'grains: sorghum, maize, barley'), ('Protein-rich', 'oil-seed cakes: sesame, noug, cotton'),
                                ('Intermediate', 'wheat bran, middlings'), ('Supplements', 'salt, limestone, bone meal, fishmeal')]):
        y = 58 + i * 50
        f.text(16, y + 12, a, 11.5, INK, 'start')
        tlines(f, 16, y + 30, wrap(b, 26), 10.5, GREY, 'start', False)
    for i, (a, b) in enumerate([('Dry', 'straw (barley, wheat), stover (sorghum, millet), hay'), ('Succulent (fresh)', 'alfalfa, elephant grass, pasture'),
                                ('Browse', 'acacia, sesbania, leucaena leaves'), ('Used well only by', 'ruminants (rumen microbes)')]):
        y = 58 + i * 50
        f.text(184, y + 12, a, 11.5, INK, 'start')
        tlines(f, 184, y + 30, wrap(b, 26), 10.5, GREY, 'start', False)
    return f


def f_grazing():
    f = Fig(340, 236)
    f.title('Rotational grazing: four fenced paddocks', 12.5)
    for i in range(4):
        x = 12 + (i % 2) * 162
        y = 28 + (i // 2) * 92
        on = i == 0
        f.rect(x, y, 154, 84, BROWN, 1.6, '#DCEBC8' if not on else '#EFE3B8', 4)
        grass_tufts(f, [x + 20 + k * 28 for k in range(5)], y + 78, LEAF, 0.8 if on else 1.3)
        f.text(x + 77, y + 18, f'Paddock {i + 1}', 11.5, INK)
        f.text(x + 77, y + 34, 'grazed now' if on else f'resting: week {i} of regrowth', 10.5, RED if on else GREEN, 'middle', False)
        if on:
            cow(f, x + 60, y + 72, 0.42)
            cow(f, x + 110, y + 72, 0.42, '#C79A6B', face=-1)
    f.text(170, 218, 'Move the herd at early flowering; each paddock rests', 10.5, INK, 'middle', False)
    f.text(170, 231, 'Needs fenced land: concessions, not communal grazing', 10.5, GREY, 'middle', False)
    return f


def f_herd():
    f = Fig(340, 232)
    f.title('Classes on a dairy farm', 13)
    items = [('Calf', 'milk from a bucket; weaned at 2 months / 70–80 kg', BLUE), ('Heifer', 'mature female, not yet calved: the replacements', GREEN),
             ('Milking cow', 'milked 2 × a day, 12 h apart; dried off at 7 months pregnant', ORANGE),
             ('Bull', '1 bull for 30–40 cows; change him after 2 years', RED)]
    for i, (a, b, c) in enumerate(items):
        y = 28 + i * 50
        box(f, 8, y, 96, 40, a, c, 12.5)
        tlines(f, 112, y + 20, wrap(b, 34), 10.5, INK, 'start', False)
    return f


def f_conc():
    f = Fig(340, 220)
    f.title('Concentrate for a cow giving 14 L/day', 12.5)
    base = 190
    sc = 10
    f.line(40, base, 320, base, INK, 1.4)
    f.rect(60, base - 5 * sc, 70, 5 * sc, BROWN, 1.4, '#E8CF96', 3)
    f.text(95, base - 5 * sc + 18, '5 L', 12, INK).text(95, base + 14, 'from roughage', 10.5, GREY, 'middle', False)
    f.rect(60, base - 14 * sc, 70, 9 * sc, GREEN, 1.4, FILL[GREEN], 3)
    f.text(95, base - 9.5 * sc, '9 L extra', 12, GREEN)
    f.text(250, 70, '9 ÷ 1.5 = 6', 15, INK)
    f.text(250, 92, '6 kg concentrate', 13, GREEN)
    f.text(250, 112, 'per day', 11, GREY, 'middle', False)
    f.text(250, 150, 'Rule: 1 kg for every', 11, INK, 'middle', False).text(250, 165, '1.5 L above 5 L', 11, INK, 'middle', False)
    f.arrow(140, base - 9.5 * sc, 196, 80, GREY, 1.4, 6)
    return f


def f_milking():
    return flow(['Wash the udder with warm water (starts milk let-down)', 'Dry each teat; one towel per cow',
                 'Strip the first milk into a strip cup: clots = mastitis', 'Milk quickly by hand or machine (12 h apart)',
                 'Dip the teats in disinfectant, then release the cow'], 340, bh=36, gap=12, size=11.5,
                title='Hygienic milking, step by step', steps=True)


def f_castrate():
    f = Fig(340, 214)
    f.title('Three ways to castrate', 13)
    cols = [('Open (knife)', 'cut scrotum, remove testes', 'sure, but bleeds: fly and infection risk', RED),
            ('Burdizzo', 'crush the cords through the skin', 'bloodless; testes shrink', BLUE),
            ('Elastrator + ring', 'ring above the testes cuts blood', 'scrotum dries and drops off', GREEN)]
    for i, (a, b, c, col) in enumerate(cols):
        x = 6 + i * 112
        f.rect(x, 28, 106, 180, col, 1.6, FILL[col], 8)
        f.text(x + 53, 46, a, 11.5, col)
        cx, cy = x + 53, 100
        f.ellipse(cx - 9, cy + 6, 9, 13, INK, 1.2, '#E8B9A0').ellipse(cx + 9, cy + 6, 9, 13, INK, 1.2, '#E8B9A0')
        f.line(cx - 9, cy - 22, cx - 9, cy - 6, INK, 1.4).line(cx + 9, cy - 22, cx + 9, cy - 6, INK, 1.4)
        if i == 0:
            f.line(cx - 20, cy + 22, cx + 20, cy + 14, RED, 2.2)
        elif i == 1:
            f.rect(cx - 26, cy - 18, 52, 6, BLUE, 1.2, '#9CB7DA', 2)
        else:
            f.ellipse(cx, cy - 8, 20, 4, GREEN, 3)
        tlines(f, x + 53, 150, wrap(b, 18), 10.5, INK)
        tlines(f, x + 53, 186, wrap(c, 18), 10.5, GREY, 'middle', False)
    return f


def f_layer():
    f = Fig(340, 214)
    f.title('Life of a layer hen (White Leghorn)', 13)
    y = 104
    marks = [('day 1', 'chick from', 'hatchery'), ('16 wk', 'light up', 'to 14 h'), ('20 wk', 'move into', 'cages'),
             ('22–24 wk', 'first', 'eggs'), ('~80 wk', 'end of lay,', 'sold')]
    xs = [26, 98, 170, 242, 314]
    f.line(26, y, 314, y, INK, 2)
    f.rect(242, y - 4, 72, 8, GREEN, 0, FILL[GREEN])
    for (a, b, c), x in zip(marks, xs):
        f.circle(x, y, 5, ORANGE, 2, '#fff')
        f.text(x, y - 16, a, 11.5, INK)
        f.text(x, y + 22, b, 10, GREY, 'middle', False).text(x, y + 34, c, 10, GREY, 'middle', False)
    f.text(278, 64, 'lays 12–14 months', 10.5, GREEN)
    f.text(170, 172, '250–270 eggs a year, about one egg per 24 h', 11, INK, 'middle', False)
    f.text(170, 192, 'Local hen: about 40 eggs a year, then broods', 11, BROWN, 'middle', False)
    return f


def f_goatcal():
    f = Fig(340, 236)
    f.title('Goat breeding calendar', 13)
    rows = [('Heat cycle', 'every 17–21 days; she accepts the buck for 24–36 h'), ('First mating', 'at 3/4 of adult weight (19–23 kg)'),
            ('Gestation', '145–150 days (about 5 months)'), ('Last 2 months', 'stop milking; wean any suckling kids'),
            ('Last 6 weeks', 'extra protein and minerals'), ('Weaning', 'kids leave the dam at 3 months')]
    for i, (a, b) in enumerate(rows):
        y = 26 + i * 34
        box(f, 6, y, 100, 28, a, [RED, BLUE, GREEN, ORANGE, PURPLE, BROWN][i], 11)
        tlines(f, 114, y + 14, wrap(b, 36), 10.5, INK, 'start', False)
    return f


def _bee(f, x, y, L, w, label, sub, c):
    f.ellipse(x + L * 0.25, y, L * 0.32, w, INK, 1.2, '#E0A63A')
    for k in range(3):
        f.line(x + L * (0.06 + 0.13 * k), y - w * 0.95, x + L * (0.06 + 0.13 * k), y + w * 0.95, '#3A2A10', 2)
    f.ellipse(x - L * 0.12, y, L * 0.1, w * 0.75, INK, 1.2, '#6B4E1E')
    f.circle(x - L * 0.27, y, w * 0.55, INK, 1.2, '#4A3410')
    f.ellipse(x - L * 0.05, y - w * 1.25, L * 0.18, w * 0.55, '#7A8FA6', 1, '#DCE8F2')
    f.text(x, y + w + 22, label, 12, c)
    f.text(x, y + w + 36, sub, 10, GREY, 'middle', False)


def f_bees():
    f = Fig(340, 200)
    f.title('The three castes in one colony', 13)
    _bee(f, 60, 92, 86, 13, 'Queen', '1 per hive; lays eggs', RED)
    _bee(f, 170, 96, 56, 11, 'Worker', 'infertile female; most', GREEN)
    _bee(f, 280, 94, 70, 16, 'Drone', 'male; no sting', BLUE)
    f.text(170, 186, 'A colony: 20 000–80 000 bees', 11.5, INK)
    return f


def f_barn():
    f = Fig(340, 270)
    for k, (title, tail) in enumerate([('Head-to-head', False), ('Tail-to-tail', True)]):
        x0 = 6 + k * 170
        f.rect(x0, 26, 158, 210, GREY, 1.4, '#FBF7F0', 6)
        f.text(x0 + 79, 18, title, 12.5, INK)
        mid = x0 + 79
        f.rect(mid - 14, 30, 28, 202, BLUE if tail else GREEN, 0, FILL[BLUE if tail else GREEN])
        tlines(f, mid, 130, ['c', 'e', 'n', 't', 'r', 'e'] if False else [], 9)
        for side in (-1, 1):
            for r in range(5):
                y = 40 + r * 38
                xc = mid + side * 46
                f.rect(xc - 28, y, 56, 32, '#A08C78', 0.8, '#FFFFFF', 3)
                head_in = not tail
                hx = xc - side * 22 if head_in else xc + side * 22
                f.ellipse(xc, y + 16, 18, 9, '#5A3E2B', 1, '#C79A6B')
                f.circle(hx, y + 16, 5, '#5A3E2B', 1, '#8B5A3C')
            gx = mid + side * (16 if tail else 76)
            f.line(gx, 36, gx, 228, '#7A4E2D', 2.2, dash=True)
        f.text(mid, 250, 'centre: cleaning + milking' if tail else 'centre: feed alley', 10.5, BLUE if tail else GREEN)
        f.text(mid, 264, 'gutter (dashed) behind cows', 10, GREY, 'middle', False)
    return f


def f_phouse():
    f = Fig(340, 230)
    f.title('Poultry house: cross-section', 13)
    ground(f, 186, 0, 340, SOIL, 30)
    f.rect(40, 156, 260, 30, GREY, 1.4, '#D8D2C8')
    f.text(170, 176, 'concrete floor 30 cm above ground', 10.5, INK)
    f.path('M40 156 L40 92 L170 46 L300 92 L300 156', BROWN, 2)
    f.rect(40, 100, 12, 34, BLUE, 1, '#DCEBF7').rect(288, 100, 12, 34, BLUE, 1, '#DCEBF7')
    f.text(58, 114, 'wire-mesh', 10, BLUE, 'start', False).text(58, 126, 'vents', 10, BLUE, 'start', False)
    for xx in (110, 160, 210):
        hen(f, xx, 155, 0.8)
    f.arrow(40, 210, 300, 210, INK, 1.4, 6, both=True)
    f.text(170, 224, 'width at most 9 m (air and light reach the middle)', 10.5, INK)
    f.text(250, 58, 'length ≤ 30 m', 10.5, GREY, 'start', False)
    return f


def f_health():
    f = Fig(340, 224)
    f.title('Signs of a healthy cow', 13)
    cow(f, 160, 176, 1.6, '#B07A4C')
    leader(f, 248, 105, 334, 44, 'bright eyes, alert ears', GREEN, 10.5, 'end')
    leader(f, 258, 118, 334, 150, 'cool, moist muzzle', GREEN, 10.5, 'end')
    leader(f, 140, 96, 8, 44, 'glossy coat, lick marks', GREEN, 10.5, 'start')
    leader(f, 110, 170, 8, 206, 'walks freely; stays with herd', GREEN, 10.5, 'start')
    leader(f, 226, 132, 334, 200, 'eats well; chews the cud', GREEN, 10.5, 'end')
    return f


def f_causes():
    f = Fig(340, 280)
    box(f, 100, 6, 140, 28, 'Infectious disease', RED, 12.5)
    groups = [('Bacteria', 'TB, brucellosis, anthrax', BLUE), ('Viruses', 'FMD, rabies', PURPLE), ('Fungi', 'ringworm, moulds', ORANGE),
              ('Protozoa', 'babesiosis (ticks)', GREEN), ('Endoparasites', 'roundworms, tapeworms, flukes', BROWN),
              ('Ectoparasites', 'ticks, mites, lice, fleas, flies', GREY)]
    for i, (a, b, c) in enumerate(groups):
        x = 6 + (i % 2) * 168
        y = 50 + (i // 2) * 74
        box(f, x, y, 160, 30, a, c, 12)
        tlines(f, x + 80, y + 48, wrap(b, 28), 10.5, INK, 'middle', False)
    f.text(170, 274, 'Prevention is cheaper than cure', 11.5, GREEN)
    return f


def f_fluke():
    f = cycle(['Adult fluke in liver / bile duct', 'Eggs pass out in dung', 'Larva hatches in water',
               'Grows inside a water snail', 'Cysts stick to grass at the water edge', 'Sheep or cow eats the grass'],
              340, 300, bw=112, bh=42, size=10.5, centre='Liver fluke: the snail is the intermediate host')
    return f


def f_tape():
    f = cycle(['Moniezia tapeworm in small intestine', 'Ripe segments in dung (like rice grains)', 'Grass mites eat the eggs',
               'Larva grows in the mite', 'Lamb swallows mites with grass'],
              340, 320, bw=100, bh=44, size=10, centre='Break it: plough and re-sow')
    return f


def f_control():
    f = Fig(340, 290)
    f.title('Controlling an outbreak', 13)
    items = [('Isolation', 'separate sick or suspected animals'), ('Quarantine', 'hold NEW or exposed animals (e.g. 14 days)'),
             ('Disinfection', 'clean first, then disinfect for 24 h'), ('Destruction', 'animals that will not recover'),
             ('Disposal', 'bury deep or burn carcasses'), ('Notification', 'tell the veterinary office'), ('Immunisation', 'vaccinate the healthy herd')]
    for i, (a, b) in enumerate(items):
        y = 26 + i * 37
        box(f, 6, y, 108, 30, a, [RED, ORANGE, BLUE, PURPLE, BROWN, GREEN, GREEN][i], 11.5)
        tlines(f, 122, y + 15, wrap(b, 34), 10.5, INK, 'start', False)
    return f


def f_immunity():
    f = Fig(340, 220)
    f.rect(6, 6, 160, 208, BLUE, 1.6, FILL[BLUE], 8)
    f.rect(174, 6, 160, 208, ORANGE, 1.6, FILL[ORANGE], 8)
    f.text(86, 26, 'VACCINE', 13, BLUE).text(86, 42, 'gives ACTIVE immunity', 10.5, INK, 'middle', False)
    f.text(254, 26, 'ANTISERUM', 13, ORANGE).text(254, 42, 'gives PASSIVE immunity', 10.5, INK, 'middle', False)
    for i, (a, b) in enumerate([('contains antigen', 'contains ready antibodies'), ('body makes its own antibodies', 'borrowed antibodies'),
                                ('works after 10–14 days', 'works at once'), ('lasts long (months, years)', 'lasts a few weeks'),
                                ('before an outbreak', 'during an outbreak')]):
        y = 66 + i * 30
        tlines(f, 86, y, wrap(a, 22), 10.5, INK, 'middle', False)
        tlines(f, 254, y, wrap(b, 22), 10.5, INK, 'middle', False)
    f.text(170, 210, 'Colostrum = natural passive immunity', 10.5, GREEN)
    return f


def f_restrain():
    f = Fig(340, 178)
    f.title('Restraining cattle', 13)
    items = [('Nose ring', 'iron ring through the nasal septum; rope controls a bull'), ('Bull holder', 'clamp on the septum when there is no ring'),
             ("Milkman's rope", 'ties the hind legs (and tail) so the cow cannot kick'), ('Gag', 'keeps jaws open: dosing, stomach tube')]
    for i, (a, b) in enumerate(items):
        y = 26 + i * 37
        box(f, 6, y, 108, 30, a, [RED, ORANGE, BLUE, GREEN][i], 11.5)
        tlines(f, 122, y + 15, wrap(b, 34), 10.5, INK, 'start', False)
    return f


DIAGRAMS = {
    'population': (f_population(), 'Livestock population of Eritrea (p. 2)', 2),
    'classify': (f_classify(), 'Classification of farm animals by class and by hooves (Table 1.1)', 4),
    'ruminant': (f_ruminant(), 'The ruminant stomach: rumen, reticulum, omasum, abomasum (Figure 1.1)', 7),
    'calf': (f_calf(), 'Relative size of the stomach compartments with age (Table 1.2)', 6),
    'pig': (f_pig(), 'Digestive tract of a pig (Figure 1.2)', 9),
    'poultry': (f_poultry(), 'Digestive tract of a hen (Figure 1.3)', 11),
    'breeding': (f_breeding(), 'Breeding tools and systems of mating', 13),
    'cross': (f_cross(), 'Cross-breeding a local zebu with an exotic dairy breed (Figure 1.5)', 16),
    'nutrients': (f_nutrients(), 'The nutrients in a feed', 17),
    'dm': (f_dm(), 'Dry matter in fresh alfalfa (Activity 1.11)', 18),
    'feeds': (f_feeds(), 'Concentrates and roughages', 25),
    'grazing': (f_grazing(), 'Rotational grazing', 27),
    'herd': (f_herd(), 'Classes of dairy animal', 30),
    'conc': (f_conc(), 'Concentrate allowance for a milking cow', 32),
    'milking': (f_milking(), 'Hygienic milking routine', 32),
    'castrate': (f_castrate(), 'Open and closed castration', 35),
    'layer': (f_layer(), 'Management timeline of a layer hen', 40),
    'goatcal': (f_goatcal(), 'Goat breeding calendar', 42),
    'bees': (f_bees(), 'Queen, worker and drone', 45),
    'barn': (f_barn(), 'Conventional dairy barn: head-to-head and tail-to-tail', 49),
    'phouse': (f_phouse(), 'Design of a poultry house', 52),
    'restrain': (f_restrain(), 'Restraining equipment for cattle (Figures 1.16–1.19)', 54),
    'health': (f_health(), 'Outward signs of health', 57),
    'causes': (f_causes(), 'Causes of infectious disease with examples', 62),
    'fluke': (f_fluke(), 'Life cycle of the liver fluke', 72),
    'tape': (f_tape(), 'Life cycle of the Moniezia tapeworm', 71),
    'control': (f_control(), 'General measures to control an outbreak', 74),
    'immunity': (f_immunity(), 'Vaccine and antiserum compared', 77),
}

# ------------------------------------------------------------------ 1.1 introduction, classification, digestion, breeding
L1 = [
    'agri12-u1-c01', 'agri12-u1-c02',
    T('=agri12-u1-c04', '1.1.1 What livestock are', 1,
      '**Livestock** = any animal kept to produce **food, wool, skins or fur**, or to **work the land**. In Eritrea this means **cattle, sheep, goats, camels, pigs, poultry** and the **equines** (horses, mules and donkeys). Equines are kept mainly for **draught** (pulling) and **transport**.',
      '**Animal production (animal husbandry)** is the practice of raising animals for products such as **meat, milk, eggs, honey** and even **fish** from ponds.',
      '**A short history:** people began to domesticate animals more than **10 000 years ago**, starting with the **dog**. The first food animals were **ruminants** (cattle, sheep, goats), then pigs. Horses and cattle were also tamed for transport and draught.',
      '**Why domestication mattered:**',
      '- a **stable food supply**, so the human population could grow;',
      '- **division of labour**: once food was secure, some people could become smiths, potters, traders or priests (a feature of civilisation);',
      '- animals for **company, religious offerings** and **draught power**. In return the animals got protection and a regular food supply.'),
    DG('pop-fig', 'How many animals does Eritrea have?', 2, 'population',
       'Goats are the most numerous: they survive on browse in the dry lowlands where cattle and sheep struggle.'),
    T('=agri12-u1-c05', '1.1.2 Livestock status in Eritrea', 2,
      'Livestock matter in all **six zobas**. Most of Eritrea\'s animals are **indigenous** (local). The only exotic breeds found in large numbers are the **Holstein-Friesian** dairy cow and the **White Leghorn** layer hen. There are also several thousand **Large White** pigs.',
      'Agriculture gives about **26 %** of Eritrea\'s GDP, and livestock give **15 % of that** agricultural share.',
      '**Why output is still low:** most animals are kept in a **traditional, low-input** system. Three big constraints:',
      '- **feed shortage**: too little feed, and of poor quality, especially in the dry season;',
      '- **widespread diseases** and parasites;',
      '- **unimproved breeds** with low milk and meat yields.',
      'Animals also get little care in **feeding, health care and housing**, so Eritreans eat some of the lowest amounts of animal products per person in the world.'),
    TB('=agri12-u1-c06', '1.1.3 Values and uses of livestock', 3, ['Farming system', 'What livestock do there', 'Eritrean example'],
       [['Mixed crop–livestock (most of Eritrea)', 'Oxen plough; manure fertilises fields; crop residues become meat and milk; animals spread risk', 'Highland farmer near Mendefera: two oxen pull the maresha; cows eat barley straw'],
        ['Pastoral', 'The only livelihood: milk is food; animals sold to buy grain', 'Herders of Gash-Barka and the Northern Red Sea with camels and goats'],
        ['Peri-urban dairy and layer farms', 'Income from milk and eggs; jobs', 'Holstein farms around Asmara; layer farms near Keren'],
        ['Commercial farms and agro-industry', 'Employment, foreign currency', 'Export of live sheep, goats and camels; hides to tanneries'],
        ['Social role (all systems)', 'Store of wealth, status, dowry, ceremonies', 'Savings "on the hoof"; a sheep or goat slaughtered at holidays']], layout='cards'),
    DG('class-fig', 'Classifying farm animals', 4, 'classify',
       'Count the hooves: two (cloven) = Artiodactyla; one = Perissodactyla.'),
    T('=agri12-u1-c07', '1.1.4 Types and classification of livestock', 4,
      'All farm animals belong to **Kingdom Animalia** and **Phylum Chordata**. They split at the **class**: poultry are **Aves** (feathers, eggs), the others are **Mammalia** (hair, suckle their young with milk).',
      'Mammals are split into **orders by their hooves**:',
      '- **Artiodactyla = EVEN-toed** (two hooves, a cloven hoof): cattle, sheep, goats, pigs and camels.',
      '- **Perissodactyla = ODD-toed** (one hoof): horses, donkeys and mules.',
      'They are split further into **families** by their digestive system:',
      '- **Equines** are **hindgut fermenters**: microbes digest fibre in the **caecum and large intestine (colon)**.',
      '- **Bovidae** (cattle, sheep, goats) and **Camelidae** are **foregut fermenters**: fibre is fermented in the fore-stomach (rumen) before the true stomach. Camels have a three-compartment stomach with no separate omasum, so they are called pseudo-ruminants.',
      '- **Pigs and poultry** are **monogastric**, like humans.',
      '**Two species of cattle:** *Bos taurus* = **humpless** (European breeds such as Holstein-Friesian); *Bos indicus* = **humped zebu** (Eritrea\'s Barka and Arado). They can interbreed.'),
    RM('class-err', 'Correction: even-toed and odd-toed', 4,
       'The textbook says horses have an even number of toes and cattle, camels, goats and pigs an odd number. It is the **other way round**: **Artiodactyla** (artios = even) have **two** functional hooves; **Perissodactyla** (perissos = odd) have **one**. The order names in its Table 1.1 are right.',
       'The textbook also says equines digest mainly in the caecum and the **small** intestine. Fibre fermentation in equines happens in the **caecum and the large intestine (colon)**.'),
    TB('tax', 'Zoological classification (Table 1.1)', 4, ['Animal', 'Class', 'Order', 'Family', 'Genus species'],
       [['Horse', 'Mammalia', 'Perissodactyla', 'Equidae', 'Equus caballus'], ['Cattle', 'Mammalia', 'Artiodactyla', 'Bovidae', 'Bos taurus / B. indicus'],
        ['Sheep', 'Mammalia', 'Artiodactyla', 'Bovidae', 'Ovis aries'], ['Goat', 'Mammalia', 'Artiodactyla', 'Bovidae', 'Capra hircus'],
        ['Pig', 'Mammalia', 'Artiodactyla', 'Suidae', 'Sus scrofa'], ['Chicken', 'Aves', 'Galliformes', 'Phasianidae', 'Gallus domesticus']], layout='cards'),
    ST('rum-st', 'How a cow digests grass, step by step', 7, 'ruminant',
       [('**Rumen** (80 % of an adult stomach): the cow swallows grass with little chewing. Bacteria, fungi and protozoa make the enzyme **cellulase** and ferment cellulose into energy (volatile fatty acids).', 'k1'),
        ('**Reticulum**: has a honeycomb wall. It sorts the food and sends boluses (**cud**) back up to the mouth. The cow ruminates up to **8 hours a day**. It also traps nails and wire, which can cause "hardware disease".', 'k2'),
        ('**Omasum** ("many leaves"): its leaves squeeze the food and absorb water and minerals.', 'k3'),
        ('**Abomasum = true stomach**: acid and enzymes digest the food (and the rumen microbes) as in a pig or a person.', 'k4'),
        ('Then the **small intestine**: most digestion and absorption. Order to remember: **R-R-O-A**.', 'k5')]),
    RM('cellulase', 'Correction: cellulase, not "cellulose"', 7,
       'The textbook says the microbes have "a digestive enzyme called **cellulose**". Cellulose is the plant fibre. The enzyme that breaks it down is **cellulase**. The cow cannot make cellulase itself; only its rumen microbes can.'),
    DG('calf-fig', 'A calf\'s stomach grows up', 6, 'calf',
       'In a newborn the abomasum is the largest part (60 %), because milk is digested there. When the calf starts eating grass, the rumen grows to 80 %.'),
    T('calf', 'The newborn calf and colostrum', 6,
      'A newborn calf has an **undeveloped rumen** and lives on milk for the first weeks. When it suckles, a fold called the **oesophageal groove** closes and carries milk straight to the **abomasum**, past the rumen. Once the calf eats grass and hay, the rumen grows fast.',
      '**Colostrum** = the first milk after calving. Give it **as soon as possible**, within the first hours, because:',
      '- it is rich in **immunoglobulins** (antibodies). This is **passive immunity**: the calf receives ready-made antibodies from its mother;',
      '- it is very **nutritious**: high in fat, protein and vitamins, but low in lactose;',
      '- it is a **laxative**: it clears the first dung (meconium) from the gut.'),
    TB('colostrum', 'Colostrum compared with whole milk (Table 1.3)', 6, ['Milk', 'Dry matter %', 'Fat %', 'Protein %'],
       [['First-milking colostrum', '26.9', '6.0', '18.8'], ['Pooled excess colostrum', '16.0', '5.5', '5.5'], ['Whole milk', '12.9', '3.5', '3.1']],
       'First colostrum has about **six times** the protein of whole milk (18.8 ÷ 3.1 ≈ 6).'),
    DG('pig-fig', 'The pig: one stomach', 9, 'pig',
       'Mouth → oesophagus → stomach → small intestine (duodenum, jejunum, ileum) → large intestine → anus.'),
    T('pig', 'Digestion in pigs (monogastric)', 8,
      'Pigs have **one simple stomach**, like people (mono = one, gastric = stomach). They **cannot live on grass** and need grain and other low-fibre feeds.',
      '- **Mouth:** teeth chew; saliva softens food and starts starch digestion.',
      '- **Oesophagus:** muscle waves carry food down. The **cardiac valve** stops food coming back up.',
      '- **Stomach:** hydrochloric acid and enzymes. Food leaves through the **pyloric valve**.',
      '- **Duodenum:** **bile** (made in the liver and stored in the gall bladder) digests fat; **pancreatic juice** digests fat, starch and protein.',
      '- **Jejunum and ileum:** most nutrients are absorbed here.',
      '- **Caecum, large intestine and rectum:** water is absorbed and faeces form; they leave through the **anus**.'),
    DG('hen-fig', 'The hen: crop and gizzard instead of teeth', 11, 'poultry',
       'Grit (small stones) in the gizzard does the job of teeth.'),
    T('hen', 'Digestion in poultry', 11,
      'Poultry have a **short, simple tract**, and food passes through very fast.',
      '- **Beak and tongue:** no chewing; food is swallowed whole.',
      '- **Crop:** a stretchy pouch on the oesophagus that **stores** food.',
      '- **Proventriculus:** the glandular stomach. It adds acid and **pepsinogen** (which becomes pepsin) to digest protein.',
      '- **Gizzard:** a strong muscular stomach. With **grit** inside, it grinds grain. This is essential before proper digestion.',
      '- **Small intestine:** bile and pancreatic enzymes; absorption.',
      '- **Two caeca:** bacteria ferment leftovers. **Short colon:** absorbs water.',
      '- **Cloaca:** faeces and urine mix and leave together, so hen droppings have a white cap of uric acid.'),
    TB('dig-cmp', 'Comparing the four digestive types', 8, ['Feature', 'Ruminant (cow, sheep, goat)', 'Pig', 'Hen', 'Equine (donkey, horse)'],
       [['Stomach', '4 compartments', '1 simple', 'proventriculus + gizzard', '1 simple'],
        ['Fibre digested where?', 'rumen (before the stomach)', 'very little', 'a little in the caeca', 'caecum + colon (after)'],
        ['Chewing', 'chews again (cud)', 'chews', 'none: gizzard grinds', 'chews well'],
        ['Best feed', 'grass, straw, browse', 'grain, kitchen waste', 'grain, insects', 'grass, hay, straw'],
        ['Can use urea (NPN)?', 'yes, microbes make protein', 'no', 'no', 'a little']], layout='compare'),
    T('=agri12-u1-c08', '1.1.5 Breeding: improving the next generation', 12,
      'An animal\'s performance depends on its **environment** (feeding, health care, housing, management) **and** its **genetic make-up** (heredity). **Breeding** is the mating of a chosen male with a chosen female to get desired offspring.',
      'In traditional herds mating is often **unplanned** (any bull serves any cow), so the herd does not improve. **Planned breeding** improves chosen traits.',
      '**Tool 1: selection.** Keep the best animals of the breeds already in the country. Do this **first**, because (1) local animals vary a lot in milk, growth and fertility, and (2) local breeds are **adapted** to heat, disease and poor feed, and their genes must not be lost.',
      '**Selection criteria depend on the purpose.** A dairy farmer keeps daughters of high-milk cows that calve regularly and have large udders. A traditional goat keeper looks at milk, litter size (twins), disease resistance, kid survival, and birth and weaning weights.',
      '**Culling** = removing animals with undesirable traits: low milk, poor fertility, small kids or calves, frequent illness.',
      '**Tool 2: cross-breeding.** Bring in the genes of a more productive breed, using an **exotic sire** or **artificial insemination (AI)** with the semen of a high-quality bull. The offspring are called **crosses**. It is a **drastic** step. It works only if the **environment is improved at the same time**: without better feed, health care and housing, the costs outweigh the gains.',
      'Note: the textbook numbers this section "1.5", which is a printing slip. It belongs to 1.1.'),
    DG('breed-fig', 'Selection, cross-breeding and the systems of mating', 13, 'breeding'),
    TB('mating', 'Systems of mating', 15, ['System', 'Who is mated', 'Kinds', 'Use / risk'],
       [['Inbreeding', 'related animals of the same breed', 'close-breeding (brother × sister), line-breeding (to one famous ancestor)', 'fixes traits; too much causes weak, less fertile young'],
        ['Out-breeding', 'unrelated animals', 'out-crossing, grading up, cross-breeding, species hybridisation (horse × donkey = mule)', 'hybrid vigour; grading up turns a local herd into a near-exotic one over generations']], layout='cards'),
    DG('cross-fig', 'Cross-breeding a Barka cow with a Holstein bull', 16, 'cross'),
    TB('breeds', 'Breeds found in Eritrea', 15, ['Type', 'Meaning', 'Examples'],
       [['Indigenous (local)', 'native to the country, well adapted', 'Barka and Arado cattle; local sheep and goats; local chickens'],
        ['Exotic', 'brought in from outside', 'Holstein-Friesian, Jersey, Ayrshire; White Leghorn, Rhode Island Red, Fayoumi; Large White pig'],
        ['Cross-bred', 'from mating two breeds', 'Barka × Holstein-Friesian dairy cows']], layout='cards'),
    WK('wk-sel', 'Worked example — why select males?', 14,
       'Activity 1.8: In selection, does choosing better males or better females bring faster change?',
       ['A cow has about **one calf a year**. One bull (or AI semen) can sire **30–40 calves a year**, or thousands with AI.',
        'So each good bull spreads his genes to far more offspring than any one cow.',
        'Selecting the **male** therefore changes the herd much faster. Females are still culled for poor milk or fertility.'],
       'Selecting the male gives faster change, because one sire has many more offspring than one dam.'),
    WK('wk-env', 'Worked example — crossing without a better environment', 14,
       'Activity 1.9: What goes wrong if a farmer crosses his zebu cows with a Holstein bull but changes nothing else?',
       ['The cross needs **more feed** to give more milk, but gets only dry-season straw, so it cannot reach its potential.',
        'It has **less resistance** to heat, ticks and local diseases than the zebu, so more calves die and vet bills rise.',
        'Result: higher costs, little extra milk, and the adapted local genes are diluted.'],
       'The crosses cannot express their potential and suffer more disease and heat stress, so the disadvantages outweigh the gains.'),
    'agri12-u1-c03', 'agri12-u1-tbl1', 'agri12-u1-wrk1', 'agri12-u1-wrk2', 'agri12-u1-chk1', 'agri12-u1-chk2', 'agri12-u1-chk73',
]

# ------------------------------------------------------------------ 1.2 feeds and feeding
L2 = [
    T('=agri12-u1-c09', 'Feeds and feeding: the big picture', 17,
      'A **feed** is any material that an animal can eat, **digest, absorb and use**. "Feed" is used for animals and "food" for people, but they mean the same thing.',
      'Part of what an animal eats is **not digested** and leaves as faeces. The parts that are digested and used are the **nutrients**.',
      'In Eritrea the dry season is the hungry season: from about October to June animals live mainly on **straw, stover and browse**. Good feeding means giving **water first**, then enough energy and protein, plus salt and minerals.'),
    DG('nut-fig', 'The six nutrients', 17, 'nutrients',
       'Feed = water + dry matter. Dry matter = organic matter (carbohydrates, proteins, fats, vitamins) + inorganic matter (minerals, measured as ash).'),
    T('=agri12-u1-c10', '1.2.1 Feed composition and the nutrients', 17,
      '**Six nutrients:** water, carbohydrates, proteins, fats (lipids), vitamins and minerals.',
      '**Dry matter (DM)** = everything except water (the other five nutrients). The DM is split into **organic matter** (carbohydrates, proteins, fats, vitamins, which all contain carbon) and **inorganic matter** (the minerals, measured as **ash** after burning).',
      '**Water** is the most urgent nutrient: animals die faster from lack of water than from lack of any other nutrient. Water:',
      '- takes part in most body reactions (**hydrolysis**);',
      '- is the **solvent** that carries nutrients and wastes;',
      '- **controls body temperature**, because it makes up most of the body.',
      'The water content of feeds varies widely: fresh alfalfa is about 65–80 % water, while straw and grain are only about 10 %.'),
    DG('dm-fig', 'How much dry matter is in fresh alfalfa?', 18, 'dm'),
    WK('wk-dm', 'Worked example — dry matter (Activity 1.11)', 18,
       'Fresh alfalfa contains 65 % moisture. A farmer gives a cow 3 kg of fresh alfalfa a day. How much dry matter does the cow get?',
       ['DM % = 100 − 65 = **35 %**.', 'DM = 3 kg × 35 ÷ 100 = **1.05 kg**.', 'Check: water = 3 × 0.65 = 1.95 kg, and 1.95 + 1.05 = 3 kg. ✔'],
       '1.05 kg of dry matter per day.'),
    T('carb', 'Carbohydrates: the energy feeds', 18,
      'Carbohydrates are the **main energy source** and the **largest part of every ration**. They contain C, H and O, with H and O in the same 2 : 1 ratio as in water.',
      '- **Simple carbohydrates** (sugars and starch) are easily digested. Starch is stored in **grains and tubers** (sorghum, maize, barley, potato). Sugar-rich feeds are **molasses**, cane sugar and fruits.',
      '- **Complex (structural, fibrous) carbohydrates**, mainly **cellulose** in plant cell walls, are hard to digest. Only the enzymes of **microbes** (in the rumen, or in the caecum of a horse or donkey) can break them down.',
      'So a goat can live on straw and acacia leaves, but a hen cannot.'),
    T('prot', 'Proteins and amino acids', 19,
      'Proteins contain **C, H, O and N**. **Nitrogen is found only in proteins** (among the main nutrients), so feed protein is estimated from its nitrogen content.',
      'Proteins are long chains of **amino acids** (about 20 kinds). Digestion releases the single amino acids for absorption.',
      '**Functions:** building blocks for **growth, milk, eggs and pregnancy**; **enzymes and hormones**; **repair** of tissues; **immunoglobulins** for body defence.',
      '- **Essential amino acids** cannot be made in the body (or not fast enough), so **non-ruminants (pigs, poultry, people)** must get them from the feed. Example: lysine and methionine in a layer ration.',
      '- **Non-essential amino acids** can be made in the body from other amino acids by **transamination** (moving an amino group).',
      '- **Ruminants** do not need to worry about this: rumen microbes build all the amino acids from any nitrogen source, including **non-protein nitrogen (NPN)** such as **urea**. Non-ruminants cannot use NPN.'),
    TB('aa', 'Essential and non-essential amino acids (Table 1.4)', 20, ['Essential (must be in the feed)', 'Non-essential (body makes them)'],
       [['Arginine, histidine, isoleucine', 'Alanine, aspartic acid, citrulline'], ['Leucine, lysine, methionine', 'Cystine, glutamic acid, glycine'],
        ['Phenylalanine, threonine', 'Hydroxyproline, proline'], ['Tryptophan, valine', 'Serine, tyrosine']]),
    T('lip', 'Lipids (fats and oils)', 21,
      'Lipids contain C, H and O, like carbohydrates, but they give **2.25 times more energy** per kilogram. **Fats** are solid at room temperature; **oils** are liquid. They do not dissolve in water, only in organic solvents (ether, benzene, chloroform).',
      'Oil-seed cakes (sesame, noug, groundnut) still contain some oil, which raises their energy value.'),
    TB('min', 'Minerals: macro and micro (Table 1.5)', 22, ['Group', 'Minerals', 'Key jobs', 'Sources'],
       [['Macro (large amounts)', 'Ca, P, K, Na, Cl, S, Mg', 'Ca + P: bones and teeth (Ca most needed, then P); Na, Cl, K: water and acid–base balance', 'bone meal, fishmeal, limestone; common salt for Na and Cl'],
        ['Micro (trace)', 'Fe, Zn, Cu, Mo, Se, I, Mn, Co', 'Fe: haemoglobin (oxygen transport); Cu: helps use iron; I: thyroid hormone; Co: inside vitamin B12', 'mineral licks, mineral mixes']],
       'Both groups are **equally essential**. The names only tell you how much is needed.', layout='cards'),
    TB('vit', 'Vitamins (Table 1.6)', 23, ['Vitamin', 'Job', 'If short'],
       [['A (retinol)', 'body linings, night vision', 'night blindness, infections'], ['D (cholecalciferol)', 'absorbs Ca and P; bones; milk and eggs', 'weak bones; give it to animals kept indoors (sunlight makes it in the skin)'],
        ['E (tocopherol)', 'fertility; antioxidant', 'poor reproduction; not stored, so feed it regularly'], ['K (phylloquinone)', 'blood clotting', 'bleeding; rumen microbes make it'],
        ['B group, C (water-soluble)', 'many enzymes', 'not stored: non-ruminants need them in the feed; rumen microbes make the B vitamins']],
       '**Fat-soluble: A, D, E, K** (remember "ADEK"). Goats are seldom short of vitamins, except **vitamin A in the dry season** when there is no green feed.', layout='cards'),
    T('=agri12-u1-c11', '1.2.2 Sources and classes of feed', 24,
      '**Where feed comes from:** natural pasture; planted forages (**alfalfa, elephant grass**); crop residues (**straw** of barley, wheat and teff; **stover** of sorghum, maize and millet); by-products (wheat **bran** from mills, **molasses** from sugar, oil-seed **cakes**); and non-biological feeds such as **urea**.',
      '**Concentrates vs roughages**, by fibre content:',
      '- **Concentrates: fibre below 18 %.** They are dense, highly digestible and dry. **Energy-rich:** cereal grains. **Protein-rich:** oil-seed cakes. **Intermediate:** bran and middlings (less energy than grain, less protein than cake).',
      '- **Roughages: fibre above 18 %.** They are bulky and less digestible, and only ruminants (and equines) use them well.',
      '**Supplements** are small amounts added to improve the balance of the ration: protein (fishmeal, cake), energy (molasses), minerals (limestone for Ca, salt, bone meal) and vitamins (green leaves for vitamin A).',
      '**Succulent vs dry:** fresh alfalfa or elephant grass cut and fed green is **succulent**. The same forage dried as **hay**, or straw and stover, is **dry** feed.'),
    DG('feeds-fig', 'Concentrates and roughages side by side', 25, 'feeds'),
    TB('ration', 'Kinds of ration (feed for 24 hours)', 26, ['Ration', 'Meaning', 'Example'],
       [['Maintenance', 'keeps the animal alive at the same weight; no work or product', 'a dry cow resting in the dry season'],
        ['Production (additional)', 'extra feed on top of maintenance for milk, meat, eggs, wool or work', '1 kg concentrate per 1.5 L of milk above 5 L; extra feed for oxen before ploughing'],
        ['Balanced', 'gives all the nutrients in the right amounts for that animal\'s 24 hours', 'a mixed layer ration with grain, cake, limestone and salt']], layout='cards'),
    TB('graze', 'Grazing systems', 27, ['System', 'How it works', 'For / against'],
       [['Zero grazing (cut-and-carry)', 'cut forage at its best stage and carry it to the animals', 'used on irrigated alfalfa and elephant-grass plots of dairy farms; needs year-round water'],
        ['Tethering', 'rope or chain keeps the animal in one spot', 'cheap, little labour; can overgraze the spot'],
        ['Strip grazing', 'a new fenced strip each day', 'less selective grazing, less waste; needs private (fenced) land'],
        ['Rotational grazing', 'paddocks grazed in turn, then rested to regrow', 'graze at early flowering; needs fenced concession land'],
        ['Deferred grazing / enclosures', 'close an area so it grows standing hay for later', 'low-potential areas; in the highlands village enclosures are opened in the dry season for oxen and milking cows'],
        ['Wet-and-dry season and free range', 'move with the seasons over open range', 'low-potential rangelands']],
       'High-potential areas: zero grazing, tethering, strip and rotational grazing. Low-potential areas: deferred, wet-and-dry season and free-range grazing.', layout='cards'),
    DG('graze-fig', 'Rotational grazing in four paddocks', 27, 'grazing'),
    WK('wk-rough', 'Worked example — which carbohydrates only ruminants can use?', 19,
       'Activity 1.12: Name carbohydrate feeds that ruminants can get energy from but non-ruminants cannot.',
       ['Non-ruminants have no microbes that make cellulase **before** the small intestine.',
        'So feeds that are mostly **cellulose** are useful only to ruminants: **straw** (teff, barley, wheat), **stover** (sorghum, maize), **hay**, mature grass and browse.',
        'Grain starch and molasses can be used by both.'],
       'Fibrous feeds (straw, stover, hay, mature grass, browse), which are rich in cellulose.'),
    'agri12-u1-chk74', 'agri12-u1-chk75', 'agri12-u1-wrk4', 'agri12-u1-l1-2-mx1',
]

# ------------------------------------------------------------------ 1.3 routine management
L3 = [
    TB('=agri12-u1-c12', '1.3 Cattle: Bos taurus and zebu compared', 29, ['Feature', 'Bos taurus (humpless)', 'Bos indicus (zebu, humped)'],
       [['Examples', 'Holstein-Friesian, Jersey, Angus, Hereford', 'Barka, Arado, Brahman'], ['Size and feed', 'larger, eat more', 'smaller, eat less'],
        ['Milk and meat', 'more', 'less'], ['Heat, ticks, poor feed', 'suffer', 'survive well'], ['Climate', 'temperate / cool highlands', 'hot tropics, lowlands'],
        ['Specialised breeds', 'yes: dairy and beef breeds', 'local zebu are multi-purpose']],
       'Cattle types by function: **beef, dairy, dual-purpose and multi-purpose**. Eritrea\'s local cattle are **multi-purpose** (draught, milk, meat, manure, savings). Holstein-Friesians are kept specially for milk around Asmara and other towns.', layout='compare'),
    T('dairy', 'Dairy cattle', 29,
      'Dairy breeds: **Holstein-Friesian, Jersey, Guernsey, Brown Swiss, Ayrshire** and Milking Shorthorn.',
      'The **Holstein-Friesian** (black and white) was introduced by the Italians because the **cool highlands** suit it. It gives the **most milk and the most total butterfat** of any breed, although its fat % is lower than a Jersey\'s.'),
    DG('herd-fig', 'Who is who on a dairy farm', 30, 'herd'),
    T('dfeed', 'Feeding dairy cows: roughage plus concentrate', 31,
      '**Roughage keeps the rumen healthy.** Chewing and ruminating fibre make a lot of **saliva**, which contains **bicarbonate buffers** that keep the rumen pH near neutral. A cow lying and chewing the cud is a healthy cow. Fibre also keeps the **butterfat %** of milk up: too little roughage gives low-fat milk and acid rumen problems.',
      '**Concentrate is needed for high yields.** A cow can give about **5 L a day** from good roughage alone. For every **1.5 L above that**, give about **1 kg of concentrate**.',
      'Eritrea is not yet self-sufficient in grain for people, so dairy farms use **agro-industrial by-products** that people do not eat: oil-seed cakes (sesame, noug, cotton seed), wheat bran and middlings, and molasses.'),
    DG('conc-fig', 'Concentrate for a 14-litre cow', 32, 'conc'),
    WK('wk-conc', 'Worked example — concentrate allowance', 32,
       'A Holstein cow at a farm near Asmara gives 14 L of milk a day on good alfalfa hay. How much concentrate should she get?',
       ['Milk from roughage alone: about **5 L**.', 'Extra milk: 14 − 5 = **9 L**.', 'Concentrate: 9 ÷ 1.5 = **6 kg a day**, split between the two milkings.'],
       '6 kg of concentrate per day.'),
    ST('milk-st', 'Hygienic milking routine', 32, 'milking',
       [('Wash the udder with **warm water**. This cleans it and starts milk let-down (the hormone oxytocin).', 'k1'),
        ('Dry each teat with the cow\'s **own towel**, so mastitis germs do not pass between cows.', 'k2'),
        ('Squirt the first milk into a **strip cup**: clots or watery milk are signs of **mastitis**.', 'k3'),
        ('Milk **twice a day, about 12 hours apart**, by hand or machine.', 'k4'),
        ('**Dip the teats** in disinfectant to close out germs, then release the cow.', 'k5')]),
    T('beef', 'Beef production and fattening', 32,
      '**Beef** = meat of mature cattle; **veal** = meat of calves. Beef breeds include **Angus, Hereford, Simmental, Charolais, Limousin, Gelbvieh, Brahman and Shorthorn**.',
      '**Beef vs dairy type:** beef animals are **blocky**, shorter and well-muscled, with small udders, and turn feed into body weight. Dairy animals are **angular** (wedge-shaped) with large udders, and turn feed into milk.',
      '**Intensive beef** is common where there is surplus grain; **extensive beef** on wide rangelands is slower to reach market weight.',
      '**Fattening in Eritrea:** there is no specialised beef breed system. Instead, traders buy **thin adult animals** and feed them intensively for **4–6 months** near towns, using wheat bran, middlings, **sesame cake** and a little coarse grain. Gains are **0.6–1.2 kg a day**.'),
    WK('wk-fat', 'Worked example — fattening gain', 33,
       'An ox bought at 260 kg is fattened for 150 days and gains 0.8 kg a day. What is its final weight?',
       ['Total gain = 0.8 × 150 = **120 kg**.', 'Final weight = 260 + 120 = **380 kg**.', 'Check: 150 days ≈ 5 months, inside the usual 4–6 months.'],
       'About 380 kg.'),
    T('=agri12-u1-c13', 'Dehorning and castration', 33,
      '**Dehorning** removes the horns so animals cannot hurt each other or bruise the meat (bruised parts are cut off the carcass, or the whole carcass is condemned). Horned animals are also harder to handle. Do it in the **first two months** of life with a **dehorner**, a saw, an elastrator and rubber ring, or chemicals.',
      '**Castration** removes the testes or makes them useless. It makes males **calmer and easier to handle**, stops unwanted mating, and stops male (secondary sex) characters developing. Castrated oxen are the usual ploughing animals.',
      '- **Open castration:** a knife or scalpel cuts the bottom of the scrotum and the testes are removed (an emasculator may crush and cut the cord). It is sure, but the bleeding brings a risk of infection where flies are many.',
      '- **Closed (bloodless) castration:** the **Burdizzo** crushes the spermatic cords through the skin, and the testes shrink (atrophy). An **elastrator** puts a tight **rubber ring** above the testes, which cuts off the blood so the scrotum dries and drops off. Closed methods suit the tropics, but are a little less certain than the open method.'),
    DG('cast-fig', 'Open and closed castration', 35, 'castrate'),
    TB('poultry', 'Poultry: traditional and modern systems', 39, ['Feature', 'Traditional (local hens)', 'Modern (exotic)'],
       [['Feeding', 'scavenging, kitchen leftovers', 'balanced ration in confinement'], ['Eggs per year', 'up to about 40, then the hen broods', '250–270 (White Leghorn)'],
        ['Eggs', 'small, bright yellow yolk (liked by buyers)', 'larger, paler yolk'], ['Strengths', 'hardy, disease-resistant, cheap', 'high output for eggs or meat'],
        ['Breeds', 'local chickens', 'White Leghorn (layer), Rhode Island Red (dual-purpose, heavier), Fayoumi (from Egypt; intermediate, still scavenges)']],
       '**Poultry** = birds kept for human use that breed freely in captivity: chickens, ducks, turkeys, geese, guinea fowl, quails, pigeons and ostriches. A **broiler** is a young chicken raised for meat; the textbook\'s "broiler is the meat of poultry" is loosely worded.', layout='compare'),
    DG('layer-fig', 'Layer management timeline', 40, 'layer'),
    T('small', 'Small ruminants: sheep and goats', 41,
      '**Why smallholders like them:** they are cheap to buy and feed; they breed fast (twins are common); the loss is small if one dies; their milk is easily used or sold by the family; family labour (often children) can herd them; and they can be sold quickly for cash.',
      'Their digestive system is like a cow\'s, but they **graze closer to the ground**. A sheep has a **split upper lip** for very short grass. Goats both **graze and browse**: their mobile upper lip and **bipedal stance** (standing on the hind legs) let them pick leaves between acacia thorns.',
      'Tree leaves are **rich in protein**, so in the dry season lowland goats stay in better condition than sheep and cattle.'),
    DG('goat-fig', 'Goat breeding calendar', 42, 'goatcal'),
    T('goat', 'Breeding and feeding goats', 42,
      '- A doe must **kid** before she gives milk; the kids are the second income.',
      '- Usually **one kidding a year** in Eritrea; with good feeding, **three in two years**.',
      '- **First mating by weight, not age:** at **three-quarters of the adult weight**. If she is mated too small, she keeps growing during pregnancy, so milk and kid growth suffer.',
      '- A young **buck (billy goat)** can be fertile at **4 months** once both testes are in the scrotum. One buck serves **10–20 does**.',
      '- **Heat signs** (every 17–21 days, lasting 24–36 h): tail wagging, bleating, restlessness, mounting other goats, a red, swollen vulva, and urinating in front of the buck.',
      '- **Gestation: 145–150 days.** Stop milking **2 months** before kidding; give extra protein and minerals in the last **6 weeks**. **Wean** kids at **3 months**.',
      '- **Water:** 3–8 L a day. **Protein:** young grass, leaves of **leucaena, sesbania and acacia**, legumes, cakes, bran. **Minerals:** salt, Ca and P. A goat that eats soil may be short of minerals.'),
    WK('wk-goat', 'Worked example — when to mate a young doe', 43,
       'Adult local does in a village near Hagaz weigh about 28 kg. At what weight should a young doe be mated first?',
       ['Rule: first mating at **¾ of adult weight**.', '¾ × 28 = **21 kg**.', 'So weigh her (or use a weigh band) and mate her when she reaches about 21 kg, not at a fixed age.'],
       'At about 21 kg.'),
    T('bee', 'Beekeeping (apiculture)', 44,
      'Beekeeping produces **honey and wax**, and bees **pollinate** crops. A colony has **20 000–80 000** bees. The species: *Apis mellifera* (common honey bee), *A. dorsata* (giant), *A. laboriosa* (Himalayan giant), *A. cerana* (Indian) and *A. florea* (dwarf).',
      '**Castes:** one **queen** (the fertile female, who lays all the eggs); thousands of **workers** (infertile females that build comb, collect nectar and pollen, make wax and honey, feed the young and guard the hive); and **drones** (males). Drones only mate with young queens and die after mating; they have **no sting**.',
      'Bees communicate by **chemicals (smells) and dances** that show the direction and distance of food.',
      '**Advantages:** little capital, little land of any quality, suits men and women of any age, can be a sideline or a business, and does not compete with crops or livestock for resources.',
      '**Products:** honey, beeswax, pollen, **propolis** (bee glue from tree resins, used to seal cracks) and brood.'),
    DG('bee-fig', 'Queen, worker and drone', 45, 'bees'),
    TB('beeq', 'Beekeeping equipment', 45, ['Item', 'Use and tips'],
       [['Veil', 'the minimum protection; dark mesh is easiest to see through in sunlight'], ['Gloves', 'leather or heavy light-coloured cloth; confidence for beginners'],
        ['Clothing', 'loose, light-coloured, smooth: bees are less attracted to light colours'], ['Smoker', 'smoke makes bees fill up on honey and sting less; fuel: dry cow dung, maize cobs, rotten wood, dry leaves'],
        ['Water spray', 'cools and weighs down very defensive bees'], ['Hive tool', 'flat steel bar to prise the hive apart and scrape propolis; a blacksmith can make one']], layout='terms'),
    TB('ident', 'Identifying livestock', 47, ['Method', 'How', 'Notes'],
       [['Branding', 'hot iron or chemical marks numbers or letters on the skin', 'cattle, camels, horses'], ['Ear tag', 'metal or plastic tag fixed with tagging forceps', 'self-piercing tags, or non-piercing after punching a hole'],
        ['Tattoo', 'ink pricked into the ear', 'permanent; read up close'], ['Ear notch', 'notches cut in set positions code a number', 'pigs, sheep, goats']],
       'Identification lets the farmer **tell animals apart, certify them** (ownership, health) and **keep accurate records**. The textbook\'s list leaves out branding, although it then describes it.', layout='cards'),
    'agri12-u1-chk76', 'agri12-u1-wrk5', 'agri12-u1-chk77', 'agri12-u1-wrk6', 'agri12-u1-l1-3-mx1',
]

# ------------------------------------------------------------------ 1.4 housing and equipment
L4 = [
    T('=agri12-u1-c14', '1.4 Why we house animals', 48,
      '- **Climate control:** protection from cold, heat, rain and draughts. In Eritrea most farmers bring all stock in at night, even where the climate is mild.',
      '- **Control of breeding, health and feeding:** heat detection, mating and birth are easier to watch; diarrhoea and ticks are seen early; sick animals can be put in a **quarantine pen**.',
      '- **Safety** from **theft** and predators such as **hyenas**.',
      '- **Manure collection** for fertiliser or fuel.',
      'There is no single design. A house must let animals **live, eat and rest comfortably**, and let the farmer **work easily**.',
      '**Individual or group?** On a dairy farm keep milking cows, the bull, heifers and calves in **separate sections**: they are fed differently, the bull must not serve heifers that are too young, and the farmer must know which cow was mated. Calves are separated from their mothers soon after birth and fed from buckets. With only a few sheep or goats, **tethering** to a stake may be enough.'),
    TB('barns', 'Dairy housing: conventional and loose', 49, ['Feature', 'Conventional (tied stalls)', 'Loose housing'],
       [['How', 'cows tied by neck chain on a platform; fed and milked in the barn', 'cows free in a paddock with a shelter on one side; milked in a parlour'],
        ['Cost', 'higher', 'much lower; easy to expand'], ['Heat detection', 'harder', 'easy (cows mount each other)'],
        ['Exercise', 'little', 'plenty: better health'], ['Layout', 'one row if fewer than 10 cows; otherwise two rows, head-to-head or tail-to-tail', 'common water tank and mangers']], layout='compare'),
    DG('barn-fig', 'Head-to-head and tail-to-tail barns', 49, 'barn'),
    TB('h2h', 'Which two-row layout?', 50, ['Tail-to-tail: advantages', 'Head-to-head: advantages'],
       [['central passage makes cleaning and milking easy', 'feeding both rows from one alley is easy'], ['less spread of disease between cows', 'sunlight falls on the gutters, where it is most needed'],
        ['cows get more fresh air from outside', 'suits narrow barns'], ['milking is easy to supervise', 'cows enter their stalls more easily']]),
    T('other', 'Beef, sheep and goat housing', 50,
      '**Beef:** the simplest facilities. Cows can calve on pasture or in a lot near the farmstead; use open-fronted calving barns in the colder highlands. Keep separate lots for cows, heifers, bulls and calves. Every beef unit needs a **corral** with a **holding pen, working chute and head gate**, and good water.',
      '**Sheep:** no costly building, just protection from severe cold. It must be **dry, draught-free and well ventilated**, with **0.1 m² of window per 2 m² of floor**, doors **2.4 m wide**, **1.1–1.4 m²** per ewe, **38–46 cm** of feeder space per ewe and **30.5 cm** per lamb.',
      '**Dairy goats:** a small shed for a few goats; **loose pens** or **tie stalls** (often milking does in stalls, others loose). Confinement housing costs more but needs less bedding. House **bucks separately**.'),
    WK('wk-sheep', 'Worked example — planning a sheep house', 51,
       'A farmer near Adi Keyh plans a house for 40 ewes. Using 1.25 m² per ewe and 0.1 m² of window per 2 m² of floor, how much floor and window area does she need?',
       ['Floor = 40 × 1.25 = **50 m²**.', 'Window = 50 ÷ 2 × 0.1 = **2.5 m²**.', 'Feeder space at 40 cm per ewe = 40 × 0.40 = **16 m** of trough.'],
       '50 m² of floor, 2.5 m² of window and about 16 m of feeder.'),
    T('phouse', 'Poultry housing', 52,
      'Housing gives comfort and protection from weather and predators, and makes management easy. House **chicks, growers, layers, broilers and breeders separately**: they need different designs, and young birds catch diseases from older ones.',
      '- **Width at most 9 m**, so air and light reach the middle; **length at most 30 m**.',
      '- **Floor 30 cm above the ground**, to stop flooding and seepage; **concrete** is better than mud (easy to clean and disinfect, keeps rats out).',
      '- **Nests:** the textbook recommends one nest per hen (many farms use one nest for every 4–5 hens), each about **35 cm deep × 30 cm wide × 35–40 cm high**, with a 20–22 cm entrance.'),
    DG('ph-fig', 'Poultry house cross-section', 52, 'phouse'),
    TB('space', 'Space per bird (Tables 1.7 and 1.8)', 53, ['Age (weeks)', 'Floor, light breed (cm²)', 'Floor, heavy breed (cm²)', 'Water / feeder (cm)'],
       [['0–8', '700', '700', '1 / 5 (to 6 wk)'], ['9–12', '950', '950', '2 / 8 (7–16 wk)'], ['13–20', '1 900', '2 350', '2 / 8'], ['21 +', '2 300–2 800', '2 800–3 700', '3 / 12']],
       'One round drinker (35 cm rim) serves **70 birds** in a hot climate or **100** in a mild one. One round feeder with a 150 cm rim gives about **300 cm** of eating space.'),
    WK('wk-space', 'Worked example — floor area for layers', 53,
       'How much floor is needed for 500 White Leghorn layers (21 weeks old) at 2 500 cm² per bird?',
       ['Total = 500 × 2 500 = **1 250 000 cm²**.', '1 m² = 10 000 cm², so the area = 1 250 000 ÷ 10 000 = **125 m²**.', 'With the 9 m width limit: length = 125 ÷ 9 ≈ **14 m**.'],
       '125 m² (for example, a house 9 m wide and about 14 m long).'),
    T('restrain', 'Restraining animals', 54,
      '**Restraint** = controlling an animal so a job can be done safely (dosing, treating, milking). Approach calmly and confidently; never be harsh or hasty.',
      '- **Nose ring** (iron) through the nasal septum, made with a nose punch; a rope on the ring controls a bull.',
      '- **Bull holder:** a clamp with two half-rings that grips the septum when there is no ring.',
      '- **Milkman\'s rope:** tied round both hind legs (with the tail) so the cow cannot kick or upset the pail.',
      '- **Gags** keep the jaws apart for mouth checks, dosing or a stomach tube: **Drinkwater\'s gag** (aluminium, one for each side) or a wooden block with a hole and a strap.'),
    DG('rest-fig', 'Restraining equipment for cattle', 54, 'restrain'),
    'agri12-u1-l1-4-r3x1', 'agri12-u1-l1-4-r3x2', 'agri12-u1-l1-4-r3x3', 'agri12-u1-chk78', 'agri12-u1-wrk7', 'agri12-u1-chk79', 'agri12-u1-wrk8', 'agri12-u1-l1-4-r2c1',
]

# ------------------------------------------------------------------ 1.5 animal health
L5 = [
    T('=agri12-u1-c15', '1.5 Signs of health', 57,
      '**Health** = the structure (anatomy) and functioning (physiology) that are normal for the species. Knowing the normal state lets you spot sickness early.',
      '- **Appearance:** bright eyes; alert ears; a smooth, glossy coat with lick marks; loose skin that moves over the muscle; a **cool, moist muzzle**.',
      '- **Behaviour:** normal posture, head up, walks freely, **stays with the herd**, and lies down and gets up easily.',
      '- **Birds:** bright eyes; a smooth, glossy, **bright-red comb and wattles**; active, with the head held high and shiny feathers.',
      '- **Digestion:** normal appetite and drinking, no foul breath, eager for green forage. **Feed left in the trough** is a warning.',
      '- **Breathing:** easy and silent, moving both the chest and the belly.'),
    DG('health-fig', 'What a healthy cow looks like', 57, 'health'),
    TB('tpr', 'Normal temperature, pulse and breathing (Table 1.9)', 58, ['Animal', 'Temperature °C', 'Pulse / min', 'Breaths / min'],
       [['Cattle', '38.1–39.2', '60–70', '15–25'], ['Calves', '38.9–39.4', '70–90', '25–30'], ['Goats', '38.6–40.6', '70–80', '12–20'],
        ['Pigs', '38.6–39.7', '60–80', '10–20'], ['Dogs', '38.1–39.7', '70–120', '10–30'], ['Cats', '37.8–39.2', '100–130', '20–30']],
       'Temperature is higher in **young** animals, often in **females**, in the **evening**, in late **pregnancy**, and after **exercise, fear or excitement**. So let the animal rest and handle it gently first.'),
    T('thermo', 'Taking the temperature (Activity 1.23)', 59,
      'Use a **clinical rectal thermometer** (35–44 °C). A narrow neck stops the mercury running back until you shake it down.',
      '**Step 1:** shake the mercury down into the bulb. **Step 2:** grease the bulb with Vaseline. **Step 3:** lift the tail and insert the bulb gently into the rectum with a twisting movement, touching the wall. **Step 4:** wait **1 minute**, remove, wipe with cotton and read. **Step 5:** wash the thermometer in cold disinfectant (hot water would break it).',
      '**Pulse:** count the beats for one minute. It is higher with exercise, excitement, fever or inflammation, and lower with anaemia and weakness.',
      '**Breathing:** count the rise and fall of the flank (one rise + one fall = 1 breath), or feel the breath on your hand.'),
    WK('wk-temp', 'Worked example — reading a temperature', 58,
       'A goat in Tesseney has a rectal temperature of 41.4 °C at 8 a.m. after resting in the shade. Is it sick?',
       ['Normal goat range: **38.6–40.6 °C**.', '41.4 is **0.8 °C above** the top of the range.', 'Morning temperatures are normally the lowest of the day, and the goat had rested, so exercise does not explain it.', 'Conclusion: **fever**. Isolate it and call the veterinary assistant.'],
       'Yes: 41.4 °C is a fever for a goat.'),
    T('sick', 'Signs of sickness and what causes disease', 60,
      '**Disease** = any condition that upsets the normal working of the body (a lame cow is diseased). It can be **infectious** (caused by germs or parasites passed from another animal) or **non-infectious** (poisoning, injury, deficiency).',
      '**Signs of a sick animal:** dull, depressed or restless; thin, with a rough coat and bare patches; poor appetite or **pica** (eating soil, bones or dung); diarrhoea and soiled tail; a staggering gait or lameness; pale, dark or bluish membranes; dry, cracked nostrils; noisy breathing; dark or bloody urine; and **standing apart from the herd**.',
      '**Infection** = entry of a disease-causing micro-organism into the body.',
      '**Micro-organisms:** **viruses** (the smallest; electron microscope only; live only inside cells); **bacteria** (single cells; some make toxins); **fungi** (spore-formers: moulds as threads, yeasts as single round cells); **protozoa** (single cells, often in blood and spread by ticks and biting flies).'),
    DG('cause-fig', 'Causes of infectious disease', 62, 'causes'),
    TB('=agri12-u1-c16', '1.5.1 Major bacterial and viral diseases', 63, ['Disease', 'Cause', 'Spread', 'Signs', 'Control'],
       [['Tuberculosis (zoonosis)', 'bacterium Mycobacterium bovis', 'breath, saliva, nasal discharge, urine, milk; people mainly through raw milk', 'lung TB: hard dry cough, difficult breathing; gut TB: ulcers, diarrhoea, wasting', 'hygiene, no overcrowding, test and isolate; boil or pasteurise milk; sunlight and drying kill it'],
        ['Brucellosis (zoonosis; "undulant fever" in people)', 'Brucella abortus, B. melitensis, B. ovis, B. suis', 'semen of infected bulls, aborted foetus, afterbirth, discharges, milk', 'abortion at 5–8 months of pregnancy; infected joints and testes', 'vaccinate; burn or bury abortions; disinfect; remove infected animals; wear gloves'],
        ['Anthrax (zoonosis)', 'Bacillus anthracis (spores live for years in soil)', 'grazing, feed, water, breathing in, biting flies', 'fever 40.5–41.5 °C, convulsions, sudden death in hours or days', 'NEVER open the carcass; plug its openings; burn it or bury it deep with lime; disinfect; vaccinate'],
        ['Foot-and-mouth disease (FMD)', 'virus', 'very contagious: saliva, milk, dung, breath; on vehicles, boots and wind', 'fever 40–42 °C, drooling, blisters on tongue, lips and feet, lameness, milk drop', 'vaccinate; restrict movement; disinfect; NOTIFY the vet (notifiable disease)'],
        ['Rabies (zoonosis)', 'virus', 'bite or saliva of a rabid animal, mostly dogs; also foxes, jackals, monkeys', 'furious form: biting, wandering; dumb form: paralysed jaw, drooling; always fatal', 'yearly dog vaccination; wash a bite with plenty of soap and water and see a doctor at once']], layout='cards'),
    RM('zoon', 'Zoonoses', 63,
       'A **zoonosis** is a disease that passes between animals and people. In this unit: **TB, brucellosis, anthrax and rabies**. FMD affects all **cloven-hoofed** animals (cattle, sheep, goats, pigs), but not horses or donkeys.'),
    T('para', 'Parasites', 68,
      'A **parasite** lives on or in another organism (the **host**) at the host\'s expense. The host of the adult stage is the **final (definitive) host**; the host of the larval stage is the **intermediate host**.',
      '**Endoparasites** live inside: roundworms, tapeworms, flukes and protozoa. **Ectoparasites** live on the skin: ticks, mites, lice, fleas and flies.',
      '**How they get in:** with food and water (roundworm eggs, fluke larvae); while grazing (tapeworm larvae in mites); through the skin (blood-fluke larvae); by contact (mange mites); or by the bite of ticks, flies and mosquitoes (protozoa).',
      '**Harm they do:** steal food (worms); suck blood (hookworms, ticks); block the gut, bile ducts or blood vessels; make wounds through which germs enter; damage the liver and lungs; produce poisons; carry other germs (ticks carry babesia); and lower immunity.'),
    TB('worms', 'The three kinds of worm (helminths)', 70, ['Worm', 'Shape', 'Life cycle', 'Signs / control'],
       [['Roundworms (nematodes)', 'long, round, pointed ends; separate sexes', 'usually direct: eggs in dung → larvae on grass', 'poor appetite, diarrhoea, anaemia, stunting; clean housing, dispose of manure, deworm'],
        ['Tapeworms (cestodes)', 'flat ribbon of segments; each segment is male + female', 'indirect: mites, other arthropods', 'Moniezia: rice-like segments in dung; stunted lambs; plough and re-sow pastures'],
        ['Flukes (trematodes)', 'flat, leaf-like, one segment', 'indirect: water snails', 'liver fluke (Fasciola hepatica, F. gigantica): weight loss, anaemia; control snails, fence wet spots']], layout='cards'),
    DG('fluke-fig', 'Liver fluke life cycle', 72, 'fluke',
       'Animals that drink and graze at wet spots and spring areas in the highlands are most at risk.'),
    DG('tape-fig', 'Moniezia tapeworm life cycle', 71, 'tape'),
    T('ticks', 'Ticks and babesiosis', 73,
      '**Babesiosis (piroplasmosis)** is a protozoan disease spread by **ticks**. Signs in cattle: high fever and **red urine** (haemoglobin from burst red blood cells), with anaemia.',
      '**Tick control:**',
      '- build an **acaricide channel** round the cattle shed so ticks cannot cross from the bush;',
      '- treat **newly bought animals** with acaricide before they join the herd;',
      '- clear the vegetation round sheds regularly;',
      '- control **rodents**, which carry ticks;',
      '- **dip, spray or dust** the animals regularly.'),
    T('=agri12-u1-c17', '1.5.2 Preventing and controlling disease', 74,
      '**Prevention is cheaper than cure.** Well-fed, well-watered animals with shade or shelter, and not overworked, resist disease better. Adult animals often **carry** germs and parasites without signs (they became immune when young) and pass them to the young, so keep age groups apart.',
      'Clean and disinfect utensils, harnesses and equipment regularly.',
      '**During an outbreak:**',
      '- **Isolation:** sick or suspected animals go to a separate place with their own attendant and utensils, until they can no longer spread infection.',
      '- **Quarantine:** **apparently healthy** animals that may have been exposed, or **newly bought** animals, are kept apart for longer than the **incubation period** (for FMD about **14 days**).',
      '- **Disinfection:** keep people and animals out; remove dung; scrub with **hot 4 % washing soda**; apply disinfectant and leave it for **24 hours**. Do not graze infected pastures; **lime** them.',
      '- **Destruction and disposal:** kill animals that will not recover; **burn** the carcass or bury it **deep**.',
      '- **Notification:** inform the Animal Health Department and the local people.',
      '- **Immunisation:** vaccinate. It is the most effective method, but it does not replace the others.'),
    DG('ctrl-fig', 'Seven control measures', 74, 'control'),
    TB('disinf', 'Disinfectants and antiseptics', 75, ['Agent', 'Use', 'Strength'],
       [['Potassium permanganate', 'wounds; mouth and genital passages; general disinfectant', '1 : 1 000 to 1 : 500 for wounds; 1 : 4 000 for mouth and genital passages; 1 % as a disinfectant'],
        ['Iodine solution', 'antiseptic inside the uterus', '1 : 1 000 to 1 : 500'], ['Formaldehyde (formalin)', 'disinfecting buildings; footbath', '5 % solution; 1 : 400 footbath'],
        ['Washing soda', 'scrubbing floors and walls first', 'hot 4 %']],
       '**Disinfectant** = kills germs and spores on **places and things** (floors, utensils). **Antiseptic** = controls or kills germs on the **body** (wounds). Both fight micro-organisms; they differ in where they are used.', layout='cards'),
    WK('wk-dil', 'Worked example — making a 1 : 1 000 solution', 75,
       'How much potassium permanganate is needed to make 5 litres of a 1 : 1 000 wound wash?',
       ['1 : 1 000 means 1 g in 1 000 g, which is about 1 g per litre of water.', '5 L × 1 g/L = **5 g**.', 'Dissolve 5 g in 5 L of clean water; it should be pale pink-purple.'],
       '5 g in 5 litres.'),
    DG('imm-fig', 'Vaccine or antiserum?', 77, 'immunity'),
    T('vacc', 'Immunity and vaccines', 76,
      '**Immunity** = the power to resist infection or toxins. Some animals are **naturally immune** to some diseases: dogs and cats to FMD and rinderpest, and fowl to anthrax. An animal that **recovers** from an infection is usually immune afterwards, because its body has made **antibodies**. Young animals get antibodies from **colostrum**, milk and their mother\'s blood.',
      '**Vaccine:** contains the **antigen** (live, killed or weakened germs, or their products). The body responds by making its own antibodies, giving **active immunity** that lasts long but starts only after about **10–14 days**. Vaccinate **healthy** animals **before** an outbreak; vaccines prevent disease, they do not treat it.',
      '- **Live attenuated** (weakened) vaccines give strong, long immunity from one dose.',
      '- **Inactivated** (killed by heat, chemicals or radiation) vaccines are the safest, but give a weaker response and need repeat doses.',
      '**Antiserum** (inoculation): serum with **ready-made antibodies**. It protects **at once**, which is useful in an outbreak, but only for a short time (**passive immunity**).'),
    RM('u1-err', 'Other slips in the Unit 1 textbook', 80,
       '- Glossary: "gimmer = adult castrated male sheep" is wrong. A castrated male sheep is a **wether**; a **gimmer** is a young ewe, before her second shearing or first lamb.',
       '- Activity 1.23 refers to "Table 1.29". The temperatures are in **Table 1.9**.',
       '- The first page of 1.4 is headed "Agriculture for Grade 11", a printing slip.'),
    'agri12-u1-chk80', 'agri12-u1-wrk9', 'agri12-u1-chk81', 'agri12-u1-wrk10', 'agri12-u1-l1-5-mx1',
]

LESSONS = {'agri12-u1-l1-1': L1, 'agri12-u1-l1-2': L2, 'agri12-u1-l1-3': L3, 'agri12-u1-l1-4': L4, 'agri12-u1-l1-5': L5}

DROP = []
PATCH = {}

# ------------------------------------------------------------------ practice
a = QSet('1.1 Practice — livestock, classification, digestion and breeding', 's11')
a.M(4, 'Which pair are both odd-toed (Perissodactyla)?', ['Cattle and goat', 'Horse and donkey', 'Camel and pig', 'Sheep and horse'], 'B',
    ['Step 1: Perissodactyla have one functional hoof (odd).', 'Step 2: Horses, donkeys and mules have a single hoof.', 'Step 3: Cattle, goats, sheep, pigs and camels have a cloven (two-part) hoof, so they are Artiodactyla.'],
    'Count the hooves on one foot: 1 = odd, 2 = even.', [('To which order does a sheep belong?', 'Artiodactyla (even-toed).')])
a.M(4, 'Poultry differ from the other farm animals at the level of', ['kingdom', 'phylum', 'class', 'genus only'], 'C',
    ['Step 1: All are Animalia and Chordata.', 'Step 2: Poultry are class Aves; the rest are Mammalia.'], 'K-P-C-O-F-G-S: they split at C.', [('Which family do cattle, sheep and goats share?', 'Bovidae.')])
a.S(5, 'Explain the difference between a foregut fermenter and a hindgut fermenter, with an example of each.', 'A foregut fermenter (cow, sheep, goat, camel) ferments fibre in the fore-stomach (rumen) before the true stomach; a hindgut fermenter (horse, donkey) ferments it in the caecum and large intestine after the small intestine.',
    ['Step 1: Both depend on microbes to digest cellulose.', 'Step 2: The difference is where: before (rumen) or after (caecum/colon) the small intestine.', 'Step 3: Ruminants can also digest the microbes themselves in the abomasum, so they gain more protein.'],
    'Fore = front = rumen; hind = back = caecum.', [('Is a pig a foregut or a hindgut fermenter?', 'Neither in a big way: it is monogastric and digests little fibre.')])
a.M(7, 'In which order does food pass in a mature cow?', ['Rumen → omasum → reticulum → abomasum', 'Rumen → reticulum → omasum → abomasum', 'Reticulum → abomasum → rumen → omasum', 'Abomasum → rumen → reticulum → omasum'], 'B',
    ['Step 1: Swallowed food enters the rumen and reticulum (they work together).', 'Step 2: Then the omasum absorbs water.', 'Step 3: Last the abomasum (true stomach).'], 'R-R-O-A: "Real Rumens Only Accept grass".', [('Which compartment is called the true stomach?', 'The abomasum.')])
a.M(6, 'Milk drunk by a young calf goes straight to the abomasum through the', ['omasum', 'oesophageal groove', 'pyloric valve', 'caecum'], 'B',
    ['Step 1: The rumen of a newborn is not working.', 'Step 2: Suckling closes the oesophageal groove, a channel that bypasses the rumen.'], 'Groove = a shortcut for milk.', [('What percentage of a newborn calf\'s stomach is abomasum?', 'About 60 %.')])
a.F(7, 'Rumen microbes make the enzyme ____ that breaks down cellulose.', 'cellulase', ['cellulase', 'cellulose', 'pepsin', 'amylase'],
    ['Step 1: Enzyme names end in -ase.', 'Step 2: Cellulose is the fibre itself (the textbook confuses the two).'], 'Substrate -ose, enzyme -ase.', [('Which enzyme is formed from pepsinogen?', 'Pepsin.')])
a.S(6, 'Give three reasons why a newborn calf should get colostrum within the first hours.', 'It gives antibodies (immunoglobulins) for passive immunity; it is very nutritious (high protein, fat and vitamins); and it is a laxative that clears the first dung.',
    ['Step 1: Immunity: the calf is born with almost no antibodies.', 'Step 2: Nutrition: about 6 × the protein of normal milk.', 'Step 3: Laxative effect.', 'Step 4: The calf\'s gut absorbs antibodies well only in the first hours, so do not delay.'],
    'I-N-L: Immunity, Nutrition, Laxative.', [('Is the immunity from colostrum active or passive?', 'Passive: the antibodies are made by the mother.')])
a.M(11, 'The organ in a hen that grinds grain with grit is the', ['crop', 'proventriculus', 'gizzard', 'cloaca'], 'C',
    ['Step 1: The crop only stores.', 'Step 2: The proventriculus adds acid.', 'Step 3: The muscular gizzard grinds.'], 'Gizzard = grinder.', [('Where are faeces and urine mixed in a hen?', 'In the cloaca.')])
a.S(9, 'Why can a goat live on straw and browse while a pig cannot?', 'The goat\'s rumen microbes make cellulase and digest fibre, and even build protein from simple nitrogen; the pig has one simple stomach with no such microbes before the small intestine, so it needs grain and low-fibre feed.',
    ['Step 1: Straw is mostly cellulose.', 'Step 2: Only microbial enzymes break cellulose.', 'Step 3: The goat has them in the rumen; the pig does not.'], 'Rumen = fibre factory.', [('Name two feeds pigs do well on.', 'Grain (maize, sorghum) and kitchen or mill by-products such as bran.')])
a.M(13, 'Removing animals with undesirable traits from a herd is called', ['grading up', 'culling', 'line-breeding', 'quarantine'], 'B',
    ['Step 1: Culling = taking out the poor performers.', 'Step 2: It is the main tool of selection.'], 'Cull = remove.', [('Give two traits for which a dairy cow might be culled.', 'Low milk yield; failing to conceive or calve regularly (also frequent mastitis).')])
a.S(13, 'Why should selection within local breeds be the first step in a breeding programme in Eritrea?', 'Local animals vary widely in production, so good ones can be found and multiplied; and local breeds are adapted to heat, disease and poor feed, so their genes must not be lost.',
    ['Step 1: Variation means there is something to select.', 'Step 2: Adaptation is valuable and easily lost by careless crossing.'], 'Variation + adaptation.', [('What must accompany cross-breeding for it to succeed?', 'Improvement of the environment: feeding, housing, health care and management.')])
a.M(15, 'Mating a horse with a donkey to produce a mule is an example of', ['inbreeding', 'line-breeding', 'species hybridisation', 'grading up'], 'C',
    ['Step 1: Horse (Equus caballus) and donkey (Equus asinus) are different species.', 'Step 2: Crossing species = species hybridisation, a form of out-breeding.'], 'Two species → hybrid.', [('Mating brother with sister is…', 'Close-breeding (a form of inbreeding).')])
a.TF(14, 'Artificial insemination means mating local cows with an exotic bull brought into the village.', False,
     ['Step 1: AI uses the semen of a high-quality bull, put into the cow by a technician.', 'Step 2: Bringing in the bull itself is natural mating with an exotic sire.'], 'AI = semen, not the bull.', [('Name one advantage of AI.', 'One top bull can sire thousands of calves; no need to keep a costly bull; less spread of venereal diseases such as brucellosis.')])
a.M(2, 'Which exotic breeds are found in significant numbers in Eritrea?', ['Jersey cattle and Angus', 'Holstein-Friesian cattle and White Leghorn chickens', 'Merino sheep and Boer goats', 'Brahman and Fayoumi only'], 'B',
    ['Step 1: The textbook names Holstein-Friesian and White Leghorn, plus some Large White pigs.', 'Step 2: No exotic sheep, goat or beef breeds have been introduced.'], 'Black-and-white cow, white hen.', [('Which pig breed is found in Eritrea?', 'Large White.')])
a.S(2, 'Name three constraints that keep livestock output low in Eritrea.', 'Shortage of feed (quantity and quality), widespread diseases and parasites, and unimproved breeds; plus low inputs in feeding, health care and housing.',
    ['Step 1: Feed.', 'Step 2: Disease.', 'Step 3: Breed.', 'Step 4: Management inputs.'], 'F-D-B: Feed, Disease, Breed.', [('What share of GDP comes from agriculture?', 'About 26 %, and livestock give 15 % of that.')])

b = QSet('1.2 Practice — feeds and feeding', 's12')
b.M(17, 'Which nutrient is NOT part of the dry matter?', ['Protein', 'Minerals', 'Water', 'Vitamins'], 'C',
    ['Step 1: DM is what is left when water is removed.'], 'Dry = no water.', [('Which nutrients make up the organic matter?', 'Carbohydrates, proteins, fats and vitamins.')])
b.S(18, 'Fresh elephant grass is 80 % water. How much dry matter is in 25 kg of it?', '5 kg of dry matter.',
    ['Step 1: DM % = 100 − 80 = 20 %.', 'Step 2: 25 × 20 ÷ 100 = 5 kg.'], 'DM = fresh × (100 − water %) ÷ 100.', [('A cow needs 10 kg DM a day. How much fresh alfalfa at 65 % water is that?', '10 ÷ 0.35 ≈ 28.6 kg fresh.')])
b.M(19, 'The element found in protein but not in carbohydrates or fats is', ['carbon', 'hydrogen', 'oxygen', 'nitrogen'], 'D',
    ['Step 1: All three contain C, H, O.', 'Step 2: Only protein (amino acids) contains N.'], 'N for Nitrogen and for "New tissue".', [('How much more energy do lipids give than carbohydrates?', '2.25 times per unit weight.')])
b.M(21, 'Urea can be used as a protein source only by', ['pigs', 'poultry', 'ruminants', 'all farm animals'], 'C',
    ['Step 1: Urea is non-protein nitrogen (NPN).', 'Step 2: Rumen microbes turn NPN into microbial protein, then the animal digests the microbes.'], 'NPN needs microbes.', [('Why must urea be fed carefully?', 'Too much at once is poisonous (ammonia toxicity); mix small amounts well into the feed.')])
b.F(20, 'Making non-essential amino acids in the body is called ____.', 'transamination', ['transamination', 'fermentation', 'hydrolysis', 'rumination'],
    ['Step 1: An amino group is moved from one molecule to another.'], 'Trans = across, amine = NH₂.', [('Name two essential amino acids.', 'Lysine and methionine (also tryptophan, leucine…).')])
b.M(22, 'The mineral needed in the largest amount by farm animals is', ['iron', 'calcium', 'iodine', 'zinc'], 'B',
    ['Step 1: Bones are mostly calcium phosphate.', 'Step 2: Ca first, then P.'], 'Bones need Ca most.', [('Iodine is part of which hormone?', 'Thyroid hormone (thyroxine).')])
b.M(23, 'Cobalt is found inside vitamin', ['A', 'D', 'K', 'B12'], 'D',
    ['Step 1: Vitamin B12 is cobalamin, with cobalt at its centre.', 'Step 2: Rumen microbes need cobalt to make B12.'], 'Co-balamin.', [('Which vitamin is needed for blood clotting?', 'Vitamin K.')])
b.S(23, 'List the fat-soluble vitamins and give one job of each.', 'A: body linings and night vision; D: absorbing Ca and P for bones; E: fertility and antioxidant; K: blood clotting.',
    ['Step 1: Remember ADEK.', 'Step 2: Link each to one job.'], 'ADEK.', [('Which vitamin can the skin make in sunlight?', 'Vitamin D.')])
b.M(25, 'A feed with 30 % crude fibre is a', ['concentrate', 'roughage', 'supplement', 'balanced ration'], 'B',
    ['Step 1: The dividing line is 18 % fibre.', 'Step 2: 30 % > 18 %, so it is a roughage.'], '18 % is the line.', [('Classify wheat bran.', 'An intermediate concentrate (moderate energy and protein).')])
b.M(25, 'Which concentrate is richest in protein?', ['Sorghum grain', 'Sesame cake', 'Wheat bran', 'Molasses'], 'B',
    ['Step 1: Grains and molasses are energy feeds.', 'Step 2: Oil-seed cakes are the protein concentrates.', 'Step 3: Bran is intermediate.'], 'Cake = protein.', [('Give a calcium supplement.', 'Limestone (also bone meal).')])
b.S(26, 'Distinguish between a maintenance ration and a production ration.', 'A maintenance ration only keeps the animal alive at the same weight, with no work or products; a production ration is the extra feed given on top of it so the animal can give milk, meat, eggs, wool or work.',
    ['Step 1: Maintenance = stay the same.', 'Step 2: Production = extra for output.'], 'Production = additional.', [('What is a balanced ration?', 'One that supplies all nutrients in the right amounts for the animal\'s 24-hour needs.')])
b.M(27, 'A dairy farmer cuts irrigated alfalfa daily and carries it to cows kept in the barn. This is', ['tethering', 'strip grazing', 'zero grazing', 'deferred grazing'], 'C',
    ['Step 1: Animals do not go to the forage.', 'Step 2: The forage is cut and carried: zero grazing.'], 'Zero = the animal walks zero metres to graze.', [('What does zero grazing need throughout the year?', 'Water (usually irrigation) to grow forage.')])
b.S(28, 'Why can strip and rotational grazing not be practised on communal grazing land?', 'They need fenced land under one owner\'s control, so the herd can be moved in turn and other herds kept out; communal land is open to everyone.',
    ['Step 1: Both depend on fences and controlled resting.', 'Step 2: On communal land others would graze the resting paddocks.'], 'No fence, no rotation.', [('Where can they be practised in Eritrea?', 'On fenced concessions.')])
b.S(28, 'Describe how highland villages use deferred grazing.', 'Part of the rangeland is enclosed and no animals may graze there during the rains; in the dry season the enclosure is opened for ploughing oxen and milking cows, which need feed most.',
    ['Step 1: Close.', 'Step 2: Let the grass grow into standing hay.', 'Step 3: Open for priority animals in the dry season.'], 'Defer = save for later.', [('When is the best time to graze pasture in rotational grazing?', 'At early flowering, when crude protein and fibre are in balance.')])
b.TF(24, 'Ruminants need vitamin K in their feed.', False,
     ['Step 1: Rumen microbes make vitamin K and the B vitamins.'], 'Microbes = vitamin factory.', [('Which vitamin is most likely short for goats in the dry season?', 'Vitamin A (no green feed).')])

c = QSet('1.3 Practice — routine management', 's13')
c.M(29, 'Barka and Arado cattle are', ['Bos taurus', 'Bos indicus', 'Holstein crosses', 'specialised beef breeds'], 'B',
    ['Step 1: They are humped.', 'Step 2: Humped cattle = zebu = Bos indicus.'], 'Hump = indicus.', [('Name a humpless dairy breed.', 'Holstein-Friesian (also Jersey, Ayrshire).')])
c.S(32, 'A cow gives 11 L of milk a day on good hay. How much concentrate should she receive?', '4 kg a day.',
    ['Step 1: Roughage alone supports about 5 L.', 'Step 2: Extra = 11 − 5 = 6 L.', 'Step 3: 6 ÷ 1.5 = 4 kg.'], 'Subtract 5, divide by 1.5.', [('And a cow giving 20 L?', '(20 − 5) ÷ 1.5 = 10 kg.')])
c.S(31, 'Why must dairy cows always get enough roughage, even when fed concentrate?', 'Chewing and rumination of fibre produce saliva with bicarbonate buffers that keep the rumen pH near neutral; fibre also keeps the butterfat % of the milk up. Without it the rumen becomes acid and milk fat falls.',
    ['Step 1: Fibre → chewing → saliva.', 'Step 2: Saliva → buffer → healthy rumen.', 'Step 3: Fibre → milk fat.'], 'No cud, no buffer.', [('What does a cow that stops chewing the cud tell you?', 'It may be sick.')])
c.M(30, 'One bull is enough for about', ['5–10 cows', '30–40 cows', '100 cows', '200 cows'], 'B',
    ['Step 1: The textbook gives 30–40 cows per bull.', 'Step 2: Replace him after 2 years to avoid inbreeding with his daughters.'], 'Thirty to forty.', [('Why change the bull after two years?', 'His daughters become ready for mating, and mating them to him would be inbreeding.')])
c.M(32, 'The strip cup is used to', ['measure milk yield', 'detect mastitis', 'dip teats', 'feed calves'], 'B',
    ['Step 1: The first squirts of milk go into the cup.', 'Step 2: Clots or watery milk show mastitis.'], 'Strip to spot.', [('Why does each cow have her own towel?', 'So mastitis germs are not carried from cow to cow.')])
c.S(33, 'Give three differences between beef and dairy breeds.', 'Beef animals are blocky and well-muscled, dairy animals angular; beef animals are shorter; beef animals turn feed into body weight, dairy animals into milk; dairy animals have bigger udders.',
    ['Step 1: Shape.', 'Step 2: Height.', 'Step 3: What feed becomes.', 'Step 4: Udder.'], 'Block vs wedge.', [('What is veal?', 'Meat from calves.')])
c.S(33, 'Thin oxen are fattened for 120 days and gain 1.0 kg a day. If each starts at 250 kg, what is the final weight of each?', '370 kg.',
    ['Step 1: Gain = 1.0 × 120 = 120 kg.', 'Step 2: 250 + 120 = 370 kg.'], 'Gain × days, then add.', [('Name two by-products used in fattening.', 'Wheat bran and sesame cake (also middlings).')])
c.M(36, 'Which tool crushes the spermatic cords without cutting the skin?', ['Scalpel', 'Burdizzo', 'Dehorner', 'Ear-tag forceps'], 'B',
    ['Step 1: Bloodless castration crushes the cords.', 'Step 2: The Burdizzo is the crushing clamp; the elastrator uses a rubber ring.'], 'Burdizzo = bloodless.', [('Why is open castration risky in hot areas?', 'The wound bleeds and attracts flies, so infection is more likely.')])
c.S(34, 'Give three reasons for castrating male animals.', 'Castrated males are calmer and easier to handle (good oxen); unwanted mating by poor males is prevented; male sex characters do not develop, giving better meat and quieter animals.',
    ['Step 1: Temper.', 'Step 2: Breeding control.', 'Step 3: Meat quality and handling.'], 'Calm, controlled, carcass.', [('Why are animals dehorned?', 'To stop them injuring each other and bruising the carcass, and to make handling easier.')])
c.M(40, 'At what age is the day length raised to 14 hours for pullets?', ['4 weeks', '16 weeks', '30 weeks', '52 weeks'], 'B',
    ['Step 1: Light stimulates laying.', 'Step 2: At 16 weeks, light goes up to 14 h; at 20 weeks into cages; first eggs at 22–24 weeks.'], '16 → light, 20 → cage, 22–24 → eggs.', [('About how long does it take a hen to form one egg?', 'About 24 hours.')])
c.S(39, 'Compare local and exotic chickens: give two advantages of each.', 'Local: hardy and disease-resistant, cheap (they scavenge), and their bright yellow yolks are preferred. Exotic: far more eggs (250–270 a year against about 40) and bigger eggs or more meat.',
    ['Step 1: Local = toughness.', 'Step 2: Exotic = output.'], 'Local survive; exotic produce.', [('Which introduced breed can still scavenge well?', 'The Fayoumi.')])
c.S(43, 'Adult does weigh 32 kg. At what weight should young does be mated first, and why not earlier?', 'At about 24 kg (¾ of 32). If mated smaller she keeps growing while pregnant, so milk yield and kid growth suffer.',
    ['Step 1: ¾ × 32 = 24 kg.', 'Step 2: Growth and pregnancy compete for nutrients.'], 'Three-quarters rule.', [('How long is a goat\'s gestation?', '145–150 days.')])
c.M(43, 'How often does a non-pregnant goat come on heat?', ['Every 7 days', 'Every 17–21 days', 'Every 60 days', 'Once a year'], 'B',
    ['Step 1: The heat cycle is 17–21 days.', 'Step 2: She accepts the buck for 24–36 hours.'], 'About three weeks.', [('Give two signs of heat in a doe.', 'Tail wagging, bleating, mounting others, a red swollen vulva.')])
c.S(44, 'Why do goats stay in better condition than sheep and cattle in the lowland dry season?', 'They browse trees and shrubs, using their mobile lips and bipedal stance, and tree leaves are rich in protein; sheep and cattle depend on dry grass.',
    ['Step 1: Browse is available when grass is gone.', 'Step 2: Browse has more protein.'], 'Goats eat "up", others eat "down".', [('What helps sheep graze very short grass?', 'Their split upper lip.')])
c.M(45, 'The fertile female in a bee colony is the', ['worker', 'drone', 'queen', 'nurse bee'], 'C',
    ['Step 1: Workers are infertile females.', 'Step 2: Drones are males.'], 'One queen, many workers.', [('Do drones sting?', 'No, drones have no sting.')])
c.S(46, 'Why does a beekeeper use a smoker?', 'Smoke makes the bees fill up on honey so they fly and sting less, and it drives them away from the part of the hive being worked.',
    ['Step 1: Bees gorge on honey.', 'Step 2: Calm, less defensive bees.'], 'Smoke = calm.', [('Why wear light-coloured clothing?', 'Bees are less attracted to light colours.')])
c.M(47, 'Fixing a numbered plastic label to the ear with forceps is', ['branding', 'tattooing', 'tagging', 'ear-notching'], 'C',
    ['Step 1: Tags are metal or plastic labels.', 'Step 2: They are fixed with tagging forceps.'], 'Tag = label.', [('Which method uses a hot iron?', 'Branding.')])

d = QSet('1.4 Practice — housing and equipment', 's14')
d.S(48, 'Give four reasons for housing animals.', 'Protection from bad weather; easier control of breeding, feeding and health (heat detection, spotting diarrhoea and ticks, isolation); safety from theft and predators such as hyenas; and easy collection of manure.',
    ['Step 1: Climate.', 'Step 2: Control.', 'Step 3: Safety.', 'Step 4: Manure.'], 'C-C-S-M.', [('Why are stock housed at night in Eritrea even in mild areas?', 'Mainly for safety from theft and hyenas, and to collect manure.')])
d.M(50, 'In which barn layout do cows face a central feed alley?', ['Tail-to-tail', 'Head-to-head', 'Loose housing', 'Single row'], 'B',
    ['Step 1: Head-to-head = heads towards the middle.', 'Step 2: Both rows are fed from one alley.'], 'Heads meet over the food.', [('Which layout makes milking easiest to supervise?', 'Tail-to-tail.')])
d.S(50, 'State three advantages of loose housing.', 'It is cheaper to build and easy to expand; heat is easy to detect; cows get more exercise and are healthier (better overall management).',
    ['Step 1: Cost.', 'Step 2: Heat detection.', 'Step 3: Exercise.'], 'Loose = cheap, free, fit.', [('Where are cows milked in loose housing?', 'In a separate milking parlour.')])
d.S(51, 'A sheep house has 60 m² of floor. How much window area does it need?', '3 m².',
    ['Step 1: 0.1 m² of window per 2 m² of floor.', 'Step 2: 60 ÷ 2 × 0.1 = 3 m².'], 'Window = floor ÷ 20.', [('How wide should sheep-house doors be?', '2.4 m.')])
d.M(52, 'The maximum width of a poultry house should be', ['3 m', '9 m', '20 m', '30 m'], 'B',
    ['Step 1: Width ≤ 9 m for even ventilation and light.', 'Step 2: Length ≤ 30 m.'], 'Nine wide, thirty long.', [('How high above the ground should the floor be?', '30 cm.')])
d.S(53, 'How many round drinkers (35 cm rim) are needed for 700 birds in hot Massawa?', '10 drinkers.',
    ['Step 1: In a hot climate one drinker serves 70 birds.', 'Step 2: 700 ÷ 70 = 10.'], 'Hot 70, mild 100.', [('And in the mild highlands?', '700 ÷ 100 = 7 drinkers.')])
d.S(53, 'What floor area is needed for 300 heavy-breed growers aged 13–20 weeks?', '70.5 m².',
    ['Step 1: Heavy breed, 13–20 weeks: 2 350 cm² per bird.', 'Step 2: 300 × 2 350 = 705 000 cm².', 'Step 3: ÷ 10 000 = 70.5 m².'], 'cm² ÷ 10 000 = m².', [('Floor per bird for light breeds aged 0–8 weeks?', '700 cm².')])
d.M(55, "The milkman's rope is tied to the", ['horns', 'neck', 'hind legs', 'nose'], 'C',
    ['Step 1: It stops kicking during milking.', 'Step 2: It is tied round both hind legs, including the tail.'], 'Kicks come from the hind legs.', [('What is a gag used for?', 'Keeping the jaws apart for examination, dosing or passing a stomach tube.')])
d.TF(54, 'A nose ring is fitted through the nasal septum of a bull.', True,
     ['Step 1: A hole is punched in the septum with a nose punch.', 'Step 2: The iron ring goes through it and a rope is attached.'], 'Septum = the wall between the nostrils.', [('What is used when a bull has no nose ring?', 'A bull holder.')])

e = QSet('1.5 Practice — animal health', 's15')
e.M(58, 'The normal rectal temperature of cattle is about', ['35.0–36.0 °C', '38.1–39.2 °C', '40.5–41.5 °C', '42–44 °C'], 'B',
    ['Step 1: Table 1.9 gives 38.1–39.2 °C.', 'Step 2: 40.5–41.5 °C is the anthrax fever range.'], 'Cattle ≈ 38.5 °C.', [('Normal breathing rate of cattle?', '15–25 per minute.')])
e.S(59, 'Give four things that raise an animal\'s temperature without disease.', 'Young age, late pregnancy, evening time, exercise, fear or excitement (also hot weather; females are often slightly higher).',
    ['Step 1: Body state: age, sex, pregnancy.', 'Step 2: Time: evening.', 'Step 3: Activity: exercise, excitement.'], 'Rest the animal first.', [('Why wash the thermometer in cold disinfectant, not hot water?', 'Heat would expand the mercury and could break it.')])
e.S(60, 'A calf breathes 45 times a minute and has a temperature of 40.5 °C. Interpret.', 'Both are above normal for calves (25–30 breaths, 38.9–39.4 °C), so the calf has a fever and fast breathing, possibly pneumonia; isolate it and call the vet.',
    ['Step 1: Compare with the calf row of Table 1.9.', 'Step 2: Both values are high.', 'Step 3: Act: isolate and get treatment.'], 'Always compare with the right species and age.', [('What does a low pulse with weakness suggest?', 'Anaemia or weakness.')])
e.M(62, 'The smallest disease-causing organisms, seen only with an electron microscope, are', ['bacteria', 'fungi', 'viruses', 'protozoa'], 'C',
    ['Step 1: Viruses are far smaller than bacteria.', 'Step 2: They live only inside cells.'], 'Virus = very small.', [('Which germs are often spread by ticks?', 'Protozoa (e.g. babesia).')])
e.M(65, 'The carcass of an animal that died of anthrax should be', ['skinned for the hide', 'opened to find the cause', 'burned or buried deep without opening', 'fed to dogs'], 'C',
    ['Step 1: Opening it lets the bacteria form spores that live for years.', 'Step 2: Plug the openings, then burn it or bury it deep.'], 'Anthrax: never open.', [('Which workers are most at risk of anthrax?', 'Tannery and wool workers, and people carrying meat from infected carcasses.')])
e.M(65, 'FMD affects', ['only horses', 'cloven-hoofed animals', 'only poultry', 'only humans'], 'B',
    ['Step 1: Cattle, sheep, goats, pigs and buffalo.', 'Step 2: It spreads very fast and is notifiable.'], 'Foot-and-mouth: split feet.', [('Name two signs of FMD.', 'Fever, drooling, blisters on tongue, lips and feet, lameness, drop in milk.')])
e.S(63, 'How do people usually catch bovine tuberculosis, and how can it be prevented?', 'Mainly by drinking raw milk from infected cows (also by breath); prevent it by boiling or pasteurising milk, testing cattle and isolating reactors, good hygiene and no overcrowding.',
    ['Step 1: Source: milk.', 'Step 2: Break the chain: heat the milk.', 'Step 3: Control in the herd.'], 'Boil the milk.', [('What kills TB bacteria in the environment?', 'Direct sunlight and drying.')])
e.S(64, 'Which disease causes abortion in cows at 5–8 months of pregnancy, and what is it called in people?', 'Brucellosis; in people it is called undulant fever.',
    ['Step 1: Brucella abortus attacks the uterus.', 'Step 2: Humans catch it from milk and aborted material.'], 'Brucella → abortion.', [('Name one Brucella species.', 'B. abortus (also B. melitensis, B. ovis, B. suis).')])
e.M(68, 'An intermediate host carries', ['the adult parasite', 'the larval stage', 'only the eggs', 'no parasites'], 'B',
    ['Step 1: Final host = adult stage.', 'Step 2: Intermediate host = larval stage.'], 'Intermediate = in-between stage.', [('Intermediate host of the liver fluke?', 'Water snails.')])
e.S(72, 'Explain how controlling snails protects sheep from liver fluke.', 'The fluke larva must develop inside a water snail before it can form cysts on grass; with fewer snails (draining or fencing wet areas, clearing vegetation at watering points) fewer infective cysts reach the grass that sheep eat.',
    ['Step 1: Snail = essential link.', 'Step 2: Remove the link and the cycle breaks.'], 'Break the weakest link.', [('How are animals infected with Moniezia tapeworm?', 'By eating grass mites that carry the larvae.')])
e.M(73, 'Red urine and high fever in a cow with many ticks suggest', ['anthrax', 'babesiosis', 'rabies', 'brucellosis'], 'B',
    ['Step 1: Ticks transmit babesia.', 'Step 2: Babesia burst red blood cells, so haemoglobin colours the urine.'], 'Ticks + red water = babesiosis.', [('Give two ways of controlling ticks.', 'Dipping or spraying with acaricide; treating new animals; clearing vegetation; controlling rodents.')])
e.S(75, 'Distinguish between isolation and quarantine.', 'Isolation separates animals that are known or suspected to be sick; quarantine separates apparently healthy animals that may have been exposed (or are newly bought) until the incubation period has passed.',
    ['Step 1: Who: sick vs apparently healthy.', 'Step 2: How long: until recovery vs longer than the incubation period.'], 'Isolate the sick, quarantine the newcomer.', [('How long is quarantine for FMD?', 'About 14 days.')])
e.S(75, 'What is the difference between a disinfectant and an antiseptic?', 'Both kill or control micro-organisms; a disinfectant is used on places and objects (floors, utensils) and also kills spores, while an antiseptic is used on the living body (wounds).',
    ['Step 1: Similarity: anti-germ.', 'Step 2: Difference: where used.'], 'Disinfect things, antiseptic skin.', [('What strength of formalin is used for a footbath?', '1 in 400.')])
e.S(75, 'How much potassium permanganate makes 2 L of a 1 : 500 wound wash?', '4 g.',
    ['Step 1: 1 : 500 = 1 g in 500 mL, i.e. 2 g per litre.', 'Step 2: 2 L × 2 g/L = 4 g.'], '1 : 1 000 ≈ 1 g/L.', [('How much for 10 L of 1 : 1 000?', '10 g.')])
e.M(77, 'Which gives immediate but short protection in an outbreak?', ['Live vaccine', 'Inactivated vaccine', 'Antiserum', 'Deworming'], 'C',
    ['Step 1: Antiserum contains ready-made antibodies.', 'Step 2: No waiting for the body to respond, but they wear off.'], 'Serum = ready; vaccine = wait.', [('Which type of immunity does a vaccine give?', 'Active immunity.')])
e.TF(77, 'Vaccines are used to treat animals that are already sick.', False,
     ['Step 1: Vaccines prevent disease.', 'Step 2: They work best in healthy animals, given before an outbreak.'], 'Vaccinate the healthy.', [('Which vaccines are safest but give a weaker response?', 'Inactivated (killed) vaccines.')])

QS = a.items + b.items + c.items + d.items + e.items

GLOSSARY = [
    ('Artiodactyla', 'Even-toed hoofed mammals: cattle, sheep, goats, pigs, camels.', 4),
    ('Perissodactyla', 'Odd-toed hoofed mammals: horses, donkeys, mules.', 4),
    ('Abomasum', 'The fourth, "true" stomach of a ruminant, with acid and enzymes.', 7),
    ('Oesophageal groove', 'Fold that carries a suckling calf\'s milk straight to the abomasum.', 6),
    ('Colostrum', 'First milk after birth; rich in antibodies, a laxative.', 6),
    ('Cellulase', 'Enzyme made by microbes that digests cellulose.', 7),
    ('Gizzard', 'Muscular stomach of birds that grinds food with grit.', 11),
    ('Culling', 'Removing animals with undesirable traits from a herd.', 14),
    ('Dry matter', 'Everything in a feed except water.', 17),
    ('Non-protein nitrogen (NPN)', 'Simple nitrogen compounds such as urea that rumen microbes turn into protein.', 21),
    ('Concentrate', 'Dense feed with less than 18 % fibre.', 25),
    ('Roughage', 'Bulky feed with more than 18 % fibre.', 25),
    ('Ration', 'The total feed given to an animal in 24 hours.', 26),
    ('Zero grazing', 'Cutting forage and carrying it to housed animals.', 27),
    ('Heifer', 'Mature female that has not yet given birth.', 30),
    ('Weaning', 'Stopping a young animal from suckling.', 31),
    ('Burdizzo', 'Clamp that crushes the spermatic cords for bloodless castration.', 36),
    ('Bipedal stance', 'Standing on the hind legs, as goats do to browse.', 41),
    ('Propolis', 'Bee glue made from tree resins.', 46),
    ('Zoonosis', 'A disease passed between animals and humans.', 63),
    ('Intermediate host', 'Host that carries the larval stage of a parasite.', 68),
    ('Quarantine', 'Keeping apparently healthy, exposed or new animals apart for longer than the incubation period.', 75),
    ('Antiserum', 'Serum with ready-made antibodies giving immediate, short (passive) immunity.', 77),
    ('Wether', 'Castrated male sheep.', 80),
]
TIPS = [('Hooves: 2 = Artiodactyla (cattle, goats, camels), 1 = Perissodactyla (horse, donkey).', 4),
        ('Concentrate allowance: (milk − 5 L) ÷ 1.5 = kg of concentrate.', 32),
        ('Isolate the sick; quarantine the newcomer.', 75)]
IDEAS = [('rroa', 'Rumen → reticulum → omasum → abomasum', 'l1_1', 'agri12-u1-ad-rum-st'),
         ('feed18', '18 % fibre: concentrate vs roughage', 'l1_2', 'agri12-u1-ad-feeds-fig'),
         ('conc', '1 kg concentrate per 1.5 L above 5 L', 'l1_3', 'agri12-u1-ad-wk-conc'),
         ('barn', 'Head-to-head vs tail-to-tail', 'l1_4', 'agri12-u1-ad-barn-fig'),
         ('ctrl', 'Seven control measures', 'l1_5', 'agri12-u1-ad-ctrl-fig')]

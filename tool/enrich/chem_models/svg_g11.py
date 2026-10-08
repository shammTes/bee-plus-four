"""Grade 11 diagrams: Le Chatelier (pressure, concentration), forms of carbon, activity series, ideal and real gases."""
import math

from svglib import BLUE, GLASS, GREEN, INK, ORANGE, RED, arrow, circ, g, line, path, poly, rect, svg, t

NO2 = '#b5651d'


def _no2(x, y):
    return circ(x, y, 6, NO2, '#7a3e10', 1)


def _n2o4(x, y):
    return circ(x - 5, y, 6, '#f1e3c6', '#a08050', 1) + circ(x + 5, y, 6, '#f1e3c6', '#a08050', 1)


def lechat_pressure():
    """states a equilibrium, b squeezed, c new equilibrium"""
    o = [t(170, 16, 'Pressure and equilibrium: N₂O₄(g) ⇌ 2NO₂(g)', 12, weight='bold'),
         t(170, 34, 'colourless ⇌ brown', 10, fill=GLASS)]

    def syringe(x_end, mols, key, caption, sub):
        # barrel 40..300, plunger at x_end
        p = [rect(40, 56, 260, 70, '#ffffff', GLASS, 2, 4), rect(x_end, 56, 8, 70, '#8a9a94'), line(x_end + 8, 91, 330, 91, '#8a9a94', 6),
             rect(302, 74, 4, 34, '#8a9a94')]
        tint = {'a': '#f8efe6', 'b': '#efd9c4', 'c': '#f4e6d6'}[key]
        p.append(rect(42, 58, x_end - 44, 66, tint))
        for kind, x, y in mols:
            p.append(_no2(x, y) if kind == 'n' else _n2o4(x, y))
        p.append(t(170, 146, caption, 10, weight='bold'))
        p.append(t(170, 160, sub, 10, fill=GLASS))
        return g(p, s=key)
    a = [('n', 70, 72), ('n', 150, 108), ('n', 230, 74), ('n', 260, 110), ('d', 110, 80), ('d', 196, 100)]
    b = [('n', 58, 72), ('n', 98, 110), ('n', 140, 74), ('n', 156, 104), ('d', 80, 92), ('d', 128, 90)]
    c = [('n', 60, 76), ('n', 142, 106), ('d', 84, 104), ('d', 118, 72), ('d', 150, 82)]
    o.append(syringe(290, a, 'a', 'at equilibrium: 4 NO₂ + 2 N₂O₄ = 6 gas particles', 'brown colour steady'))
    o.append(syringe(170, b, 'b', 'squeezed to half the volume: pressure doubles', 'same particles, more crowded → darker at first'))
    o.append(syringe(170, c, 'c', 'new equilibrium: 2 NO₂ + 3 N₂O₄ = 5 gas particles', 'shifts to the side with FEWER gas moles (left)'))
    return svg(340, 168, '\n'.join(o))


def lechat_conc():
    """steps: n2 added, h2, nh3"""
    o = [t(170, 16, 'Adding N₂ to N₂ + 3H₂ ⇌ 2NH₃ at equilibrium', 12, weight='bold')]
    x0, y0, x1 = 44, 196, 320
    o.append(line(x0, y0, x1, y0, INK, 1.4) + line(x0, y0, x0, 30, INK, 1.4) + t(182, 216, 'time →', 10) +
             t(20, 112, 'concentration', 10, extra=' transform="rotate(-90 20 112)"'))
    o.append(line(150, 36, 150, y0, GLASS, 1, '4 3') + t(150, 32, 'N₂ added', 9, fill=GLASS) + t(97, 210, 'equilibrium 1', 9, fill=GLASS) +
             t(262, 210, 'equilibrium 2', 9, fill=GLASS))
    o.append(g([path(f'M{x0} 120 L150 120 L150 60 Q176 82 214 88 L{x1} 88', BLUE, w=2.4), t(x1 - 2, 82, 'N₂', 11, 'end', 'bold', BLUE)], hl='n2'))
    o.append(g([path(f'M{x0} 80 L150 80 Q176 104 214 110 L{x1} 110', GREEN, w=2.4), t(x1 - 2, 124, 'H₂ (used up)', 10, 'end', 'bold', GREEN)], hl='h2'))
    o.append(g([path(f'M{x0} 160 L150 160 Q176 140 214 136 L{x1} 136', RED, w=2.4), t(x1 - 2, 150, 'NH₃ (more made)', 10, 'end', 'bold', RED)], hl='nh3'))
    return svg(340, 222, '\n'.join(o))


def diamond():
    o = [t(170, 16, 'Diamond: giant 3-D covalent network', 13, weight='bold')]
    # a 2-D projection of the diamond lattice: puckered hexagonal rings, every atom bonded to 4
    pts = {}
    for i in range(5):
        for j in range(4):
            x = 50 + i * 60 + (30 if j % 2 else 0)
            y = 52 + j * 40
            pts[(i, j)] = (x, y)
    bonds = []
    for (i, j), (x, y) in pts.items():
        for di, dj in ((0, 1), (1, 1) if j % 2 else (-1, 1)):
            q = (i + di, j + dj)
            if q in pts:
                bonds.append(((x, y), pts[q]))
        if (i + 1, j) in pts and j % 2 == 0:
            pass
    for (a, b) in bonds:
        o.append(line(a[0], a[1], b[0], b[1], '#7a8a84', 3))
    for j in range(4):
        for i in range(5):
            x, y = pts[(i, j)]
            o.append(line(x, y, x, y - 18 if j == 0 else y, '#7a8a84', 0) if False else '')
    # up-down bonds into the page shown as short dashed stubs
    for (i, j), (x, y) in pts.items():
        o.append(line(x, y, x + 14, y - 14, '#a7b5af', 2, '3 2'))
    for (i, j), (x, y) in pts.items():
        o.append(circ(x, y, 7, '#34495e'))
    o.append(t(170, 208, 'each C atom: 4 strong covalent bonds in a tetrahedral network, 109.5°', 9.5, fill=GLASS))
    o.append(t(170, 222, 'no free electrons → hardest natural substance, non-conductor', 9.5, fill=GLASS))
    return svg(340, 230, '\n'.join(o))


def _hex_layer(cx, cy, n, s, sy, fill_dots=True):
    """a row of flattened hexagons (a graphite sheet seen at an angle)"""
    o = []
    w = s * math.sqrt(3)
    for k in range(n):
        x = cx + (k - (n - 1) / 2) * w
        pts = [(x + s * math.cos(math.radians(30 + 60 * a)), cy + s * math.sin(math.radians(30 + 60 * a)) * sy) for a in range(6)]
        o.append(poly(pts, 'none', '#34495e', 2))
    return ''.join(o)


def graphite():
    o = [t(170, 16, 'Graphite: flat layers of hexagons', 13, weight='bold')]
    ys = [60, 112, 164]
    for k, y in enumerate(ys):
        o.append(_hex_layer(170 + (16 if k % 2 else 0), y, 5, 22, 0.45))
    for x in (96, 150, 204, 258):
        o.append(line(x, 72, x, 100, ORANGE, 1.4, '3 3') + line(x + 12, 124, x + 12, 152, ORANGE, 1.4, '3 3'))
    o.append(t(300, 90, 'weak forces', 9, fill=ORANGE) + t(300, 101, 'between layers', 9, fill=ORANGE))
    o.append(t(28, 64, 'layer', 9, fill=GLASS) + t(28, 116, 'layer', 9, fill=GLASS) + t(28, 168, 'layer', 9, fill=GLASS))
    o.append(t(170, 202, 'each C: 3 strong bonds in its layer (120°); 4th electron is delocalised', 9.5, fill=GLASS))
    o.append(t(170, 216, '→ conducts electricity; layers slide → soft, slippery (pencil “lead”)', 9.5, fill=GLASS))
    return svg(340, 224, '\n'.join(o))


def c60():
    o = [t(170, 16, 'Buckminsterfullerene, C₆₀: a “buckyball”', 13, weight='bold')]
    cx, cy, rp = 170, 112, 22
    pent = [(cx + rp * math.cos(math.radians(-90 + 72 * k)), cy + rp * math.sin(math.radians(-90 + 72 * k))) for k in range(5)]
    o.append(circ(cx, cy, 92, '#f4f6fa', '#9aa9b8', 1.5))
    for k in range(5):
        p, q = pent[k], pent[(k + 1) % 5]
        s = math.dist(p, q)
        mx, my = (p[0] + q[0]) / 2, (p[1] + q[1]) / 2
        nx, ny = mx - cx, my - cy
        ln = math.hypot(nx, ny)
        nx, ny = nx / ln, ny / ln
        hc = (mx + nx * s * math.sqrt(3) / 2, my + ny * s * math.sqrt(3) / 2)
        a0 = math.atan2(p[1] - hc[1], p[0] - hc[0])
        hexp = [(hc[0] + s * math.cos(a0 + math.radians(60 * j)), hc[1] + s * math.sin(a0 + math.radians(60 * j))) for j in range(6)]
        o.append(poly(hexp, '#ffffff', '#34495e', 2))
        # outer pentagon hinted beyond each hexagon corner pair
        far = hexp[3]
        o.append(line(far[0], far[1], cx + (far[0] - cx) * 1.45, cy + (far[1] - cy) * 1.45, '#34495e', 2))
    o.append(poly(pent, '#f6d58b', '#34495e', 2))
    o.append(t(170, 222, '60 C atoms: 12 pentagons + 20 hexagons, like a football', 9.5, fill=GLASS))
    o.append(t(170, 236, 'separate molecules → soft, dissolves in some organic solvents', 9.5, fill=GLASS))
    return svg(340, 244, '\n'.join(o))


ACT = [('K', 'potassium'), ('Na', 'sodium'), ('Ca', 'calcium'), ('Mg', 'magnesium'), ('Al', 'aluminium'), ('(C)', 'carbon'), ('Zn', 'zinc'), ('Fe', 'iron'),
       ('Sn', 'tin'), ('Pb', 'lead'), ('(H)', 'hydrogen'), ('Cu', 'copper'), ('Hg', 'mercury'), ('Ag', 'silver'), ('Au', 'gold'), ('Pt', 'platinum')]


def activity():
    """steps: water, acid, extract"""
    o = [t(180, 16, 'Activity (reactivity) series of metals', 13, weight='bold')]
    top, h = 30, 20
    for k, (sym, name) in enumerate(ACT):
        y = top + k * h
        ref = sym.startswith('(')
        o.append(rect(40, y, 96, h - 2, '#eef2f0' if ref else '#dbe8f5', None, 0, 4))
        o.append(t(58, y + 14, sym, 11, weight='bold', fill=GLASS if ref else INK) + t(76, y + 14, name, 9, 'start', fill=GLASS))
    yb = top + len(ACT) * h
    o.append(arrow(22, yb - 4, 22, top + 4, RED, 2, 7) + t(14, 180, 'more reactive', 10, weight='bold', fill=RED, extra=' transform="rotate(-90 14 180)"'))

    def brace(x, k0, k1, c):
        y0, y1 = top + k0 * h + 1, top + (k1 + 1) * h - 3
        return path(f'M{x} {y0} L{x + 6} {y0} L{x + 6} {y1} L{x} {y1}', c, w=1.6)

    def note(x, k0, k1, c, lines):
        ym = top + (k0 + k1 + 1) * h / 2
        return brace(x, k0, k1, c) + ''.join(t(x + 12, ym + 4 + (i - (len(lines) - 1) / 2) * 11, s_, 9, 'start', fill=c) for i, s_ in enumerate(lines))
    o.append(g([note(142, 0, 2, BLUE, ['react with cold water', '→ hydroxide + H₂']), note(142, 3, 7, BLUE, ['react with steam', '→ oxide + H₂']),
                note(142, 8, 15, BLUE, ['no reaction with', 'water or steam'])], hl='water'))
    o.append(g([note(262, 0, 9, RED, ['above H: give', 'H₂ with dilute', 'acids']), note(262, 11, 15, RED, ['below H: no', 'H₂ with dilute', 'acids'])], hl='acid'))
    o.append(g([rect(150, yb + 4, 200, 54, '#fffaf0', '#c98a14', 1, 6), t(158, yb + 18, 'extraction:', 9, 'start', 'bold', '#7a4b12'),
                t(158, yb + 30, 'K → Al: electrolysis of molten compound', 9, 'start', fill='#7a4b12'),
                t(158, yb + 41, 'Zn → Cu: reduce oxide with C or CO', 9, 'start', fill='#7a4b12'),
                t(158, yb + 52, 'Ag, Au, Pt: found native (uncombined)', 9, 'start', fill='#7a4b12')], hl='extract'))
    o.append(t(88, yb + 18, 'a metal displaces any', 9, fill=GLASS) + t(88, yb + 30, 'metal BELOW it from', 9, fill=GLASS) + t(88, yb + 42, 'a solution of its salt', 9, fill=GLASS))
    return svg(360, yb + 64, '\n'.join(o))


def idealgas():
    """steps: b boyle, c charles, a avogadro, comb, pv, d density"""
    o = [t(180, 16, 'Building the ideal gas equation', 13, weight='bold')]

    def box(x, y, w, h, l1, l2, fill, key):
        return g([rect(x, y, w, h, fill, '#7a8a84', 1.2, 8), t(x + w / 2, y + 18, l1, 11, weight='bold'), t(x + w / 2, y + 32, l2, 9, fill=GLASS)], hl=key)
    o.append(box(8, 30, 108, 42, 'Boyle: V ∝ 1/P', 'n, T fixed', '#e3f1f8', 'b'))
    o.append(box(126, 30, 108, 42, 'Charles: V ∝ T', 'n, P fixed', '#fde6df', 'c'))
    o.append(box(244, 30, 108, 42, 'Avogadro: V ∝ n', 'P, T fixed', '#dff0e4', 'a'))
    for x in (62, 180, 298):
        o.append(arrow(x, 72, 180 + (x - 180) * 0.25, 98, INK, 1.4, 6))
    o.append(box(110, 100, 140, 40, 'V ∝ nT / P', 'all three together', '#fff4d6', 'comb'))
    o.append(arrow(180, 140, 180, 158, INK, 1.4, 6))
    o.append(box(90, 160, 180, 42, 'PV = nRT', 'R = 8.314 J/(mol·K) = 0.0821 L·atm/(mol·K)', '#efe4f7', 'pv'))
    o.append(arrow(180, 202, 180, 218, INK, 1.4, 6))
    o.append(box(70, 220, 220, 42, 'n = m/M, d = m/V  →  PM = dRT', 'density of a gas from P, T and M', '#f3f3f3', 'd'))
    return svg(360, 268, '\n'.join(o))


def realgas():
    """states i ideal, v volume correction, p attraction correction"""
    o = [t(170, 16, 'Ideal gas vs real gas (van der Waals)', 13, weight='bold')]
    o.append(rect(30, 36, 170, 130, '#ffffff', GLASS, 2, 4))
    pts = [(60, 60), (120, 54), (170, 70), (80, 110), (140, 100), (180, 130), (60, 150), (120, 146)]
    o.append(g([''.join(circ(x, y, 2, BLUE) for x, y in pts), t(276, 70, 'ideal model:', 10, weight='bold'), t(276, 86, 'particles are points', 9, fill=GLASS),
                t(276, 100, 'no attractions', 9, fill=GLASS), t(276, 120, 'PV = nRT', 11, weight='bold', fill=BLUE)], s='i'))
    o.append(g([''.join(circ(x, y, 11, '#cfe0f2', '#6c8fb3', 1) for x, y in pts), t(276, 64, 'real particles', 10, weight='bold'),
                t(276, 80, 'take up space', 9, fill=GLASS), t(276, 94, 'free volume = V − nb', 10, weight='bold', fill=ORANGE),
                t(276, 112, 'matters at HIGH P', 9, fill=GLASS), t(276, 124, '(little empty space)', 9, fill=GLASS)], s='v'))
    o.append(g([''.join(circ(x, y, 6, '#cfe0f2', '#6c8fb3', 1) for x, y in pts), circ(190, 100, 6, '#f6d58b', '#c98a14', 1.5),
                arrow(186, 100, 160, 100, RED, 1.4, 5), arrow(188, 104, 172, 124, RED, 1.4, 5), arrow(188, 96, 174, 76, RED, 1.4, 5),
                t(276, 64, 'neighbours pull a', 9, fill=GLASS), t(276, 76, 'particle back from', 9, fill=GLASS), t(276, 88, 'the wall → lower P', 9, fill=GLASS),
                t(276, 106, 'P + an²/V²', 11, weight='bold', fill=RED), t(276, 124, 'matters at LOW T', 9, fill=GLASS)], s='p'))
    o.append(rect(20, 176, 300, 30, '#f7f3fb', '#ddd0ea', 1, 6))
    o.append(t(170, 196, '(P + an²/V²)(V − nb) = nRT', 13, weight='bold', fill='#7d3c98'))
    return svg(340, 214, '\n'.join(o))


ALL = {
    'press': (lechat_pressure, 'Effect of pressure on N₂O₄ ⇌ 2NO₂', 23),
    'conc': (lechat_conc, 'Effect of concentration on N₂ + 3H₂ ⇌ 2NH₃', 22),
    'diamond': (diamond, 'Structure of diamond', 72),
    'graphite': (graphite, 'Structure of graphite', 72),
    'c60': (c60, 'Buckminsterfullerene, C₆₀', 73),
    'activity': (activity, 'Activity series of metals', 120),
    'ideal': (idealgas, 'Deriving PV = nRT', 177),
    'real': (realgas, 'Real gases: van der Waals corrections', 188),
}

"""Grade 9 Unit 1 (1.4.3 Separating mixtures): one small diagram per separation method."""
import random

from svglib import (BLUE, GLASS, INK, MUD, OIL, RED, WATER, WATER2, arrow, beaker, burner, circ, dots, flame, g, label, line, path, poly, rect, svg,
                    t, tripod)


def _scatter(seed, n, x0, y0, x1, y1):
    rnd = random.Random(seed)
    return [(round(rnd.uniform(x0, x1)), round(rnd.uniform(y0, y1))) for _ in range(n)]


def sediment():
    """states s0 stirred -> s1 settling -> s2 settled -> s3 decanting"""
    o = [t(170, 16, 'Sedimentation, then decantation', 13, weight='bold')]
    bx, by, bw, bh = 40, 58, 100, 112
    o.append(beaker(bx, by, bw, bh))
    o.append(beaker(210, by, bw, bh))
    o.append(t(90, 188, 'beaker 1', 10, fill=GLASS))
    o.append(t(260, 188, 'beaker 2', 10, fill=GLASS))
    # s0: muddy everywhere
    o.append(g([rect(bx + 1, 80, bw - 2, 89, '#c9a77a'), dots(_scatter(1, 28, bx + 5, 84, bx + bw - 5, 166), 2.2, '#7a5a30'),
                t(90, 74, 'just stirred', 10, fill=GLASS)], s='s0'))
    # s1: settling
    o.append(g([rect(bx + 1, 80, bw - 2, 89, '#dccfb8'), dots(_scatter(2, 24, bx + 5, 118, bx + bw - 5, 166), 2.2, '#7a5a30'),
                arrow(64, 92, 64, 112, '#7a5a30', 1.4, 6), arrow(116, 92, 116, 112, '#7a5a30', 1.4, 6), t(90, 74, 'particles sink (gravity)', 10, fill=GLASS)], s='s1'))
    # s2: settled
    o.append(g([rect(bx + 1, 80, bw - 2, 74, WATER), rect(bx + 1, 154, bw - 2, 15, MUD), label(120, 160, 'sediment', 150, 132),
                label(110, 100, 'clear water', 150, 96), t(90, 74, 'settled', 10, fill=GLASS)], s='s2'))
    # s3: decanting into beaker 2
    o.append(g([rect(bx + 1, 128, bw - 2, 26, WATER), rect(bx + 1, 154, bw - 2, 15, MUD),
                path('M142 60 Q190 30 236 96', WATER2, w=5), rect(211, 120, bw - 2, 49, WATER),
                t(260, 112, 'decantate', 10, fill=BLUE), label(120, 160, 'sediment stays', 148, 148), t(175, 40, 'pour gently', 10, fill=GLASS)], s='s3'))
    return svg(340, 196, '\n'.join(o))


def filtration():
    """steps: m pour, p paper, r residue, f filtrate"""
    o = [t(170, 16, 'Filtration', 13, weight='bold')]
    # stand
    o.append(line(40, 40, 40, 236, '#6f7d78', 3) + line(26, 236, 90, 236, '#6f7d78', 4) + line(40, 92, 124, 92, '#6f7d78', 2.5))
    # funnel cone + stem
    o.append(path('M110 60 L230 60 L176 128 L176 170 L164 170 L164 128 Z', GLASS, '#f4f8f6', 2))
    o.append(g([path('M120 64 L220 64 L170 124 Z', '#b9a77a', '#fffdf5', 1.4, dash='4 3'),
                label(212, 70, 'filter paper (tiny pores)', 236, 58, 10)], hl='p'))
    o.append(g([path('M146 106 L194 106 L170 124 Z', None, MUD), dots(_scatter(3, 10, 150, 96, 190, 108), 2.2, '#7a5a30'),
                label(186, 112, 'residue (sand, mud)', 236, 120, 10)], hl='r'))
    # glass rod + mixture beaker
    o.append(g([line(118, 26, 160, 92, '#8aa39b', 3), path('M70 20 L104 12 L108 30 L76 40 Z', GLASS, '#c9a77a', 1.5),
                path('M106 24 Q114 30 118 36', '#b08850', w=3), t(70, 54, 'muddy water', 10, 'middle', fill=GLASS),
                t(70, 66, 'down a glass rod', 10, 'middle', fill=GLASS)], hl='m'))
    # beaker + filtrate
    o.append(beaker(124, 176, 92, 60))
    o.append(g([rect(125, 208, 90, 27, WATER), circ(170, 182, 2.5, WATER2), circ(170, 194, 2.5, WATER2),
                label(205, 220, 'filtrate (clear liquid)', 236, 214, 10)], hl='f'))
    return svg(340, 244, '\n'.join(o))


def magnetic():
    """states s0 mixed, s1 magnet passes, s2 separated"""
    o = [t(170, 16, 'Magnetic separation: iron + sulphur', 13, weight='bold')]
    fe = _scatter(4, 11, 70, 152, 270, 166)
    s_ = _scatter(5, 12, 70, 152, 270, 166)
    o.append(g([path('M50 170 Q170 182 290 170', GLASS, '#eef2f0', 2), dots(fe, 2.6, '#4a4f55'), dots(s_, 2.8, '#e8c62f'),
                t(170, 196, 'grey iron filings mixed with yellow sulphur powder', 10, fill=GLASS)], s='s0'))
    # magnet (bar, red/blue halves)
    mag = [rect(120, 52, 50, 22, RED, rx=3), rect(170, 52, 50, 22, BLUE, rx=3), t(145, 67, 'N', 11, fill='#fff', weight='bold'), t(195, 67, 'S', 11, fill='#fff', weight='bold')]
    stuck = _scatter(6, 10, 124, 78, 216, 88)
    o.append(g(mag + [dots(stuck, 2.6, '#4a4f55'), path('M50 170 Q170 182 290 170', GLASS, '#eef2f0', 2), dots(fe[:4], 2.6, '#4a4f55'), dots(s_, 2.8, '#e8c62f'),
                      arrow(100, 140, 130, 96, '#4a4f55', 1.3, 6), arrow(240, 140, 210, 96, '#4a4f55', 1.3, 6),
                      t(170, 196, 'iron is attracted; sulphur is not', 10, fill=GLASS)], s='s1'))
    o.append(g([path('M30 170 Q90 180 150 170', GLASS, '#eef2f0', 2), dots(_scatter(7, 11, 60, 154, 120, 166), 2.6, '#4a4f55'),
                path('M190 170 Q250 180 310 170', GLASS, '#eef2f0', 2), dots(_scatter(8, 12, 220, 154, 280, 166), 2.8, '#e8c62f'),
                t(90, 140, 'iron', 11, weight='bold'), t(250, 140, 'sulphur', 11, weight='bold'),
                t(170, 196, 'two pure components — no heating needed', 10, fill=GLASS)], s='s2'))
    return svg(340, 204, '\n'.join(o))


def evaporation():
    """states s0 solution, s1 boiling off, s2 crystals"""
    o = [t(170, 16, 'Evaporation: salt from salt water', 13, weight='bold')]
    o.append(tripod(170, 120, 90, 56))
    o.append(path('M118 96 Q170 140 222 96', GLASS, '#f4f8f6', 2.2))
    o.append(flame(170, 168, 30) + burner(170, 168))
    o.append(g([path('M124 100 Q170 134 216 100 Z', None, WATER2), t(170, 76, 'salt solution', 11, fill=BLUE)], s='s0'))
    o.append(g([path('M140 112 Q170 130 200 112 Z', None, WATER2),
                path('M150 92 q-6 -10 0 -20 q6 -10 0 -20', '#9aa9a3', w=1.5), path('M170 90 q-6 -10 0 -20 q6 -10 0 -20', '#9aa9a3', w=1.5),
                path('M190 92 q-6 -10 0 -20 q6 -10 0 -20', '#9aa9a3', w=1.5), t(262, 60, 'water vapour', 10, fill=GLASS), t(262, 72, 'escapes', 10, fill=GLASS)], s='s1'))
    cr = _scatter(9, 14, 146, 112, 194, 120)
    o.append(g([''.join(rect(x, y, 4, 4, '#ffffff', '#8a9a94', 0.8) for x, y in cr), label(196, 116, 'salt crystals (residue)', 236, 100, 10),
                t(70, 60, 'all water gone', 10, fill=GLASS)], s='s2'))
    o.append(t(170, 202, 'Massawa and Assab salt pans use the sun instead of a flame', 10, fill=GLASS))
    return svg(340, 210, '\n'.join(o))


def sep_funnel():
    """states s0 shaken, s1 layers, s2 lower layer out, s3 upper layer"""
    o = [t(170, 16, 'Separating funnel: oil and water', 13, weight='bold')]
    o.append(line(80, 30, 80, 236, '#6f7d78', 3) + line(66, 236, 120, 236, '#6f7d78', 4) + line(80, 70, 140, 70, '#6f7d78', 2.5))
    body = 'M150 40 Q130 60 132 96 Q136 140 166 150 L166 168 L174 168 L174 150 Q204 140 208 96 Q210 60 190 40 Z'
    o.append(rect(160, 30, 20, 10, '#8a9a94', rx=2))
    o.append(path(body, GLASS, '#f4f8f6', 2))
    o.append(rect(160, 162, 20, 6, '#6f7d78') + line(170, 168, 170, 196, GLASS, 3))
    o.append(beaker(140, 196, 60, 40))
    o.append(g([path('M136 70 Q134 96 138 120 Q150 146 170 148 Q190 146 202 120 Q206 96 204 70 Z', None, '#d9e7c8'),
                dots(_scatter(10, 16, 148, 80, 192, 134), 3, OIL), t(262, 96, 'cloudy: tiny oil', 10, fill=GLASS), t(262, 108, 'drops in water', 10, fill=GLASS)], s='s0'))
    o.append(g([path('M136 70 Q134 90 135 100 L205 100 Q206 90 204 70 Z', None, OIL), path('M135 100 Q138 140 170 148 Q202 140 205 100 Z', None, WATER2),
                label(204, 86, 'oil (less dense) — top', 214, 70, 10), label(200, 126, 'water (denser) — bottom', 214, 140, 10)], s='s1'))
    o.append(g([path('M135 104 L205 104 Q204 118 198 126 L142 126 Q136 118 135 104 Z', None, OIL), path('M142 126 L198 126 Q190 146 170 148 Q150 146 142 126 Z', None, WATER2),
                rect(141, 220, 58, 15, WATER2), line(170, 170, 170, 218, WATER2, 2.5), t(262, 186, 'tap open: lower', 10, fill=GLASS),
                t(262, 198, 'layer runs out', 10, fill=GLASS)], s='s2'))
    o.append(g([path('M140 118 Q150 146 170 148 Q190 146 200 118 Z', None, OIL), rect(141, 220, 58, 15, OIL),
                t(262, 180, 'tap closed, beaker', 10, fill=GLASS), t(262, 192, 'changed, then oil', 10, fill=GLASS), t(262, 204, 'run out', 10, fill=GLASS)], s='s3'))
    return svg(340, 244, '\n'.join(o))


def _flask(cx, cy, rad, liquid, neck_h=34):
    o = [circ(cx, cy, rad, '#f4f8f6', GLASS, 2)]
    if liquid:
        o.append(path(f'M{cx - rad + 3} {cy + 4} A{rad - 3} {rad - 3} 0 0 0 {cx + rad - 3} {cy + 4} Z', None, liquid))
    o.append(rect(cx - 7, cy - rad - neck_h + 2, 14, neck_h, '#f4f8f6', GLASS, 2))
    return ''.join(o)


def distillation():
    """steps h heat, t thermometer, c condenser, d distillate, r residue"""
    o = [t(170, 16, 'Simple distillation: pure water from salt water', 13, weight='bold')]
    # condenser (drawn first, under the flask neck): from (90,64) down to (276,128)
    o.append(g([path('M100 56 L280 116 L274 132 L94 72 Z', GLASS, '#e3f1f8', 2), line(94, 64, 284, 127, GLASS, 3),
                t(196, 74, 'water out', 9, fill=BLUE), t(250, 148, 'cold water in', 9, fill=BLUE), arrow(258, 134, 246, 124, BLUE, 1.2, 5), arrow(118, 64, 110, 50, BLUE, 1.2, 5),
                t(160, 108, 'condenser', 10, weight='bold', fill=BLUE)], hl='c'))
    o.append(g([_flask(70, 120, 30, WATER2), line(70, 120, 70, 150, '#ffffff', 0), tripod(70, 152, 56, 40), flame(70, 186, 22), t(70, 214, 'heat', 10, fill=GLASS)], hl='h'))
    o.append(g([rect(66, 30, 8, 54, '#ffffff', GLASS, 1.2, rx=3), circ(70, 84, 4, RED), line(70, 84, 70, 52, RED, 2), t(40, 36, '100 °C', 10, fill=RED)], hl='t'))
    o.append(g([label(86, 134, 'salt stays behind', 108, 162, 9, 'start'), dots(_scatter(11, 6, 54, 128, 86, 140), 1.6, '#ffffff')], hl='r'))
    o.append(g([beaker(270, 150, 50, 46), rect(271, 176, 48, 19, WATER), line(280, 128, 290, 152, WATER2, 2.5), t(296, 212, 'distillate', 10, fill=BLUE),
                t(296, 224, '(pure water)', 10, fill=BLUE)], hl='d'))
    return svg(340, 230, '\n'.join(o))


def fractional():
    """states k1 ethanol distils at 78 °C, k2 water distils at 100 °C"""
    o = [t(170, 16, 'Fractional distillation: ethanol + water', 13, weight='bold')]
    o.append(circ(70, 178, 24, '#f4f8f6', GLASS, 2))
    o.append(path('M49 184 A21 21 0 0 0 91 184 Z', None, '#d6eaf3'))
    o.append(flame(70, 226, 18))
    # column with beads
    o.append(rect(62, 60, 16, 96, '#f4f8f6', GLASS, 2))
    o.append(''.join(circ(66 + (i % 2) * 8, 70 + i * 8, 3, '#ffffff', '#9aa9a3', 1) for i in range(11)))
    o.append(t(30, 104, 'column', 9, fill=GLASS) + t(30, 115, 'with glass', 9, fill=GLASS) + t(30, 126, 'beads', 9, fill=GLASS))
    # thermometer
    o.append(rect(66, 28, 8, 40, '#ffffff', GLASS, 1.2, rx=3) + circ(70, 66, 3.5, RED))
    # condenser
    o.append(path('M84 52 L260 110 L254 124 L78 66 Z', GLASS, '#e3f1f8', 2) + line(80, 60, 262, 120, GLASS, 3))
    o.append(t(176, 124, 'condenser', 10, weight='bold', fill=BLUE))
    o.append(beaker(236, 150, 40, 40) + beaker(290, 150, 40, 40))
    o.append(t(256, 204, 'flask 1', 9, fill=GLASS) + t(310, 204, 'flask 2', 9, fill=GLASS))
    o.append(g([line(70, 66, 70, 44, RED, 2), t(108, 36, '78 °C', 11, weight='bold', fill=RED), line(262, 122, 256, 152, '#c9a0dc', 2.5),
                rect(237, 172, 38, 17, '#e9d8f2'), t(170, 246, 'ethanol (b.p. 78 °C) reaches the top first → flask 1', 10, fill=GLASS)], s='k1'))
    o.append(g([line(70, 66, 70, 34, RED, 2), t(108, 36, '100 °C', 11, weight='bold', fill=RED), rect(237, 172, 38, 17, '#e9d8f2'),
                line(262, 122, 306, 150, WATER2, 2.5), rect(291, 174, 38, 15, WATER), t(170, 246, 'ethanol gone; temperature rises → water → flask 2', 10, fill=GLASS)], s='k2'))
    return svg(340, 254, '\n'.join(o))


ALL = {
    'sed': (sediment, 'Sedimentation and decantation', 28),
    'filt': (filtration, 'Filtration', 29),
    'mag': (magnetic, 'Magnetic separation', 31),
    'evap': (evaporation, 'Evaporation', 30),
    'funnel': (sep_funnel, 'Separating funnel', 33),
    'dist': (distillation, 'Simple distillation', 32),
    'frac': (fractional, 'Fractional distillation', 33),
}

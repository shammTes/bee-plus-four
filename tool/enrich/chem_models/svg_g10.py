"""Grade 10 diagrams: polarity, London forces, colligative properties, concentration map, acid-base definitions, energy diagrams."""
import math

from svglib import BLUE, GLASS, GREEN, INK, ORANGE, RED, WATER, WATER2, arrow, circ, g, label, line, path, poly, rect, svg, t

ATOM = {'H': ('#f4f6f5', 9), 'Cl': ('#4caf50', 15), 'O': ('#e74c3c', 14), 'C': ('#34495e', 13)}


def atom(x, y, el, size=None):
    fill, rad = ATOM[el]
    rad = size or rad
    tc = INK if el == 'H' else '#ffffff'
    return circ(x, y, rad, fill, '#7a8a84', 1) + t(x, y + 4, el, 11 if len(el) == 1 else 10, weight='bold', fill=tc)


def dipole(x1, y1, x2, y2, c=BLUE):
    """chemist's dipole arrow: crossed tail at the δ+ end, head at the δ- end"""
    a = math.atan2(y2 - y1, x2 - x1)
    px, py = -math.sin(a) * 4, math.cos(a) * 4
    cx, cy = x1 + math.cos(a) * 5, y1 + math.sin(a) * 5
    return arrow(x1, y1, x2, y2, c, 1.8, 6) + line(cx - px, cy - py, cx + px, cy + py, c, 1.8)


def polar():
    """steps: hcl, h2o, co2, ch4"""
    o = [t(180, 16, 'Polar or non-polar? Add the bond dipoles', 13, weight='bold')]
    # HCl
    o.append(g([rect(6, 26, 170, 122, '#f7fbff', '#cfdce8', 1, 8), t(91, 44, 'HCl — polar', 12, weight='bold', fill=RED), line(64, 92, 112, 92, '#7a8a84', 4),
                atom(64, 92, 'H'), atom(116, 92, 'Cl'), t(64, 72, 'δ+', 12, fill=RED), t(116, 68, 'δ−', 12, fill=BLUE), dipole(56, 120, 128, 120),
                t(91, 140, 'one polar bond, no partner to cancel it', 9, fill=GLASS)], hl='hcl'))
    # H2O bent
    o.append(g([rect(184, 26, 170, 122, '#f7fbff', '#cfdce8', 1, 8), t(269, 44, 'H₂O — polar', 12, weight='bold', fill=RED),
                line(269, 82, 237, 116, '#7a8a84', 4), line(269, 82, 301, 116, '#7a8a84', 4), atom(269, 82, 'O'), atom(237, 116, 'H'), atom(301, 116, 'H'),
                t(294, 72, 'δ−', 12, fill=BLUE), t(222, 134, 'δ+', 11, fill=RED), t(316, 134, 'δ+', 11, fill=RED), t(269, 116, '104.5°', 9, fill=GLASS),
                dipole(331, 110, 331, 64, ORANGE), t(331, 124, 'net', 9, fill=ORANGE), t(269, 142, 'bent: bond dipoles add up', 9, fill=GLASS)], hl='h2o'))
    # CO2 linear
    o.append(g([rect(6, 154, 170, 122, '#f9fbf7', '#d6e2cf', 1, 8), t(91, 172, 'CO₂ — non-polar', 12, weight='bold', fill=GREEN),
                line(40, 214, 142, 214, '#7a8a84', 4), atom(40, 214, 'O'), atom(91, 214, 'C'), atom(142, 214, 'O'), dipole(78, 240, 40, 240), dipole(104, 240, 142, 240),
                t(91, 266, 'linear: equal dipoles cancel', 9, fill=GLASS)], hl='co2'))
    # CH4 symmetric
    o.append(g([rect(184, 154, 170, 122, '#f9fbf7', '#d6e2cf', 1, 8), t(269, 172, 'CH₄ — non-polar', 12, weight='bold', fill=GREEN),
                line(269, 182, 269, 250, '#7a8a84', 3), line(235, 216, 303, 216, '#7a8a84', 3), atom(269, 216, 'C'), atom(269, 186, 'H'), atom(269, 247, 'H'),
                atom(237, 216, 'H'), atom(301, 216, 'H'), t(269, 268, 'symmetrical: no net dipole', 9, fill=GLASS)], hl='ch4'))
    return svg(360, 282, '\n'.join(o))


def _cloud(cx, cy, shift, label_left, label_right, key):
    o = [path(f'M{cx - 34 + shift} {cy} a{34} 24 0 1 0 68 0 a34 24 0 1 0 -68 0', '#6c8fb3', '#cfe0f2', 1.4), circ(cx, cy, 6, '#c0392b'),
         t(cx, cy + 4, '+', 10, weight='bold', fill='#fff')]
    if label_left:
        o.append(t(cx - 30, cy - 28, label_left, 12, fill=BLUE if label_left == 'δ−' else RED))
    if label_right:
        o.append(t(cx + 30, cy - 28, label_right, 12, fill=BLUE if label_right == 'δ−' else RED))
    return ''.join(o)


def london():
    """states a even, b instantaneous dipole, c induced dipole + attraction"""
    o = [t(170, 16, 'London (dispersion) forces between two non-polar atoms', 12, weight='bold')]
    o.append(t(100, 112, 'atom 1', 10, fill=GLASS) + t(240, 112, 'atom 2', 10, fill=GLASS))
    o.append(g([_cloud(100, 70, 0, '', '', 'a'), _cloud(240, 70, 0, '', '', 'a'), t(170, 136, 'electrons spread evenly: no dipole', 10, fill=GLASS)], s='a'))
    o.append(g([_cloud(100, 70, -10, 'δ−', 'δ+', 'b'), _cloud(240, 70, 0, '', '', 'b'), t(170, 136, 'for an instant atom 1’s electrons crowd to one side', 10, fill=GLASS),
                t(170, 150, '→ temporary (instantaneous) dipole', 10, fill=GLASS)], s='b'))
    o.append(g([_cloud(100, 70, -10, 'δ−', 'δ+', 'c'), _cloud(240, 70, -10, 'δ−', 'δ+', 'c'), line(140, 60, 200, 60, ORANGE, 2, '5 3'),
                t(170, 52, 'attraction', 10, weight='bold', fill=ORANGE), t(170, 136, 'atom 1 induces a dipole in atom 2: δ+ attracts δ−', 10, fill=GLASS),
                t(170, 150, 'weak, short-lived, but always present', 10, fill=GLASS)], s='c'))
    return svg(340, 158, '\n'.join(o))


def bpe():
    """steps: p pure solvent curve, s solution curve, d ΔTb"""
    o = [t(170, 16, 'Why a solution boils at a higher temperature', 13, weight='bold')]
    x0, y0 = 50, 200
    o.append(line(x0, y0, 320, y0, INK, 1.5) + line(x0, y0, x0, 34, INK, 1.5) + t(186, 226, 'temperature →', 10) +
             t(20, 120, 'vapour', 10, extra=' transform="rotate(-90 20 120)"') + t(32, 120, 'pressure', 10, extra=' transform="rotate(-90 32 120)"'))
    o.append(line(x0, 70, 316, 70, GLASS, 1.2, '5 4') + t(84, 64, '1 atm', 10, fill=GLASS))
    o.append(g([path('M60 190 Q170 180 236 70 Q250 50 262 36', BLUE, w=2.4), t(118, 156, 'pure water', 10, fill=BLUE), line(236, 70, 236, y0, BLUE, 1, '3 3'),
                t(236, 214, '100 °C', 10, fill=BLUE)], hl='p'))
    o.append(g([path('M70 194 Q200 186 268 70 Q280 52 292 40', RED, w=2.4), t(250, 150, 'solution', 10, fill=RED), t(250, 162, '(lower v.p.)', 9, fill=RED),
                line(268, 70, 268, y0, RED, 1, '3 3'), t(278, 214, '100.52 °C', 9, fill=RED)], hl='s'))
    o.append(g([arrow(236, 186, 268, 186, ORANGE, 1.8, 6, both=True), t(252, 180, 'ΔTb', 11, weight='bold', fill=ORANGE)], hl='d'))
    return svg(340, 232, '\n'.join(o))


def osmosis():
    """states a start, b after osmosis (height h), c pressure pi applied"""
    o = [t(170, 16, 'Osmosis and osmotic pressure', 13, weight='bold')]
    # U-tube: left arm x 90-130, right arm 210-250, bottom 150-190
    tube = 'M90 40 L90 170 Q90 196 116 196 L224 196 Q250 196 250 170 L250 40'
    inner = 'M130 40 L130 156 L210 156 L210 40'
    o.append(t(110, 214, 'pure water', 10, fill=BLUE) + t(230, 214, 'sugar solution', 10, fill=RED))

    def fill(lh, rh):
        # lh / rh = liquid top y in left / right arm
        return (path(f'M91 {lh} L91 170 Q91 195 116 195 L170 195 L170 156 L130 156 L130 {lh} Z', None, WATER) +
                path(f'M170 195 L224 195 Q249 195 249 170 L249 {rh} L210 {rh} L210 156 L170 156 Z', None, WATER2) +
                ''.join(circ(x, y, 2.2, '#8e44ad') for x, y in [(224, rh + 14), (236, rh + 30), (220, 176), (240, 184), (190, 184), (230, rh + 50)]))
    o.append(g([fill(80, 80), t(170, 60, 'start: same level', 10, fill=GLASS)], s='a'))
    o.append(g([fill(108, 52), arrow(150, 176, 186, 176, BLUE, 1.6, 6), line(256, 52, 290, 52, GLASS, 1, '3 3'), line(256, 108, 290, 108, GLASS, 1, '3 3'),
                arrow(284, 104, 284, 56, ORANGE, 1.6, 6, both=True), t(300, 84, 'h', 12, weight='bold', fill=ORANGE),
                t(170, 36, 'water moves into the solution', 10, fill=GLASS)], s='b'))
    o.append(g([fill(80, 80), rect(212, 66, 36, 12, '#8a9a94'), line(230, 66, 230, 40, '#6f7d78', 4), arrow(230, 24, 230, 60, RED, 2, 7),
                t(270, 32, 'π', 14, weight='bold', fill=RED), t(140, 36, 'push with π: osmosis stops', 10, fill=GLASS)], s='c'))
    o.append(path(tube, GLASS, w=2.2) + path(inner, GLASS, w=2.2))
    o.append(line(170, 157, 170, 195, '#8e44ad', 2.5, '3 3') + label(170, 176, 'semi-permeable membrane', 196, 232, 9, 'start'))
    return svg(340, 240, '\n'.join(o))


def concmap():
    """steps: n moles, M molarity, m molality, p percent, N normality"""
    o = [t(180, 16, 'Concentration map: every unit goes through moles', 13, weight='bold')]

    def box(x, y, w, h, title, sub, fill, key):
        return g([rect(x, y, w, h, fill, '#7a8a84', 1.2, 8), t(x + w / 2, y + 18, title, 11, weight='bold'), t(x + w / 2, y + 32, sub, 9, fill=GLASS)], hl=key)
    o.append(box(10, 40, 108, 42, 'mass of solute', 'grams (g)', '#fff4d6', 'n'))
    o.append(box(140, 40, 90, 42, 'moles, n', 'mol', '#dff0e4', 'n'))
    o.append(arrow(118, 61, 138, 61, INK, 1.4, 6) + t(64, 96, '÷ molar mass → moles', 9, fill=GLASS))
    o.append(box(250, 30, 104, 42, 'Molarity M', 'n ÷ V solution (L)', '#e3f1f8', 'M'))
    o.append(arrow(230, 56, 248, 52, INK, 1.4, 6))
    o.append(box(250, 98, 104, 42, 'Normality N', 'M × n-factor', '#fde6df', 'N'))
    o.append(arrow(302, 72, 302, 96, INK, 1.4, 6) + t(296, 88, '× n', 9, 'end', fill=GLASS))
    o.append(box(250, 166, 104, 42, 'Molality m', 'n ÷ kg of solvent', '#efe4f7', 'm'))
    o.append(arrow(196, 82, 248, 178, INK, 1.4, 6))
    o.append(box(10, 166, 140, 42, 'mass % / volume %', 'part ÷ whole × 100', '#f3f3f3', 'p'))
    o.append(g([rect(10, 112, 176, 40, '#ffffff', '#c98a14', 1, 6), t(98, 128, 'bridge: solution mass =', 9.5, fill='#7a4b12'),
                t(98, 142, 'density × volume', 9.5, fill='#7a4b12')], hl='M m p'))
    o.append(t(180, 226, 'solvent mass = solution mass − solute mass', 10, fill='#7a4b12'))
    return svg(360, 234, '\n'.join(o))


def acidbase():
    """steps: ar Arrhenius, bl Brønsted–Lowry with conjugate pairs, lw Lewis"""
    o = [t(180, 16, 'Three ways to define acids and bases', 13, weight='bold')]
    o.append(g([rect(6, 26, 348, 56, '#fff8f0', '#ead8c4', 1, 8), t(14, 44, 'Arrhenius (in water)', 11, 'start', 'bold', RED),
                t(95, 62, 'acid: HCl → H⁺ + Cl⁻', 11), t(260, 62, 'base: NaOH → Na⁺ + OH⁻', 11), t(180, 76, 'acid gives H⁺, base gives OH⁻ in water', 9, fill=GLASS)], hl='ar'))
    o.append(g([rect(6, 88, 348, 108, '#f3f8fd', '#cfdce8', 1, 8), t(14, 106, 'Brønsted–Lowry (proton transfer)', 11, 'start', 'bold', BLUE),
                t(46, 140, 'HCl', 13, weight='bold'), t(84, 140, '+', 13), t(120, 140, 'H₂O', 13, weight='bold'), t(166, 140, '⇌', 14), t(206, 140, 'Cl⁻', 13, weight='bold'),
                t(244, 140, '+', 13), t(286, 140, 'H₃O⁺', 13, weight='bold'),
                t(46, 124, 'acid', 9, fill=RED), t(120, 124, 'base', 9, fill=BLUE), t(206, 124, 'conj. base', 9, fill=BLUE), t(286, 124, 'conj. acid', 9, fill=RED),
                path('M46 146 L46 154 L206 154 L206 146', RED, w=1.4), t(163, 166, 'pair 1: HCl / Cl⁻', 9, fill=RED),
                path('M120 146 L120 174 L286 174 L286 146', BLUE, w=1.4), t(203, 188, 'pair 2: H₂O / H₃O⁺', 9, fill=BLUE),
                arrow(58, 130, 106, 130, ORANGE, 1.2, 5), t(82, 122, 'H⁺', 9, weight='bold', fill=ORANGE)], hl='bl'))
    o.append(g([rect(6, 202, 348, 70, '#f7f3fb', '#ddd0ea', 1, 8), t(14, 220, 'Lewis (electron pair)', 11, 'start', 'bold', '#7d3c98'),
                t(70, 250, 'H₃N:', 13, weight='bold'), t(116, 250, '+', 13), t(156, 250, 'BF₃', 13, weight='bold'), t(196, 250, '→', 13), t(268, 250, 'H₃N→BF₃', 13, weight='bold'),
                path('M78 238 Q110 218 150 236', '#7d3c98', w=1.4), poly([(150, 236), (142, 234), (146, 228)], '#7d3c98'),
                t(70, 266, 'base: gives a pair', 9, fill=BLUE), t(156, 266, 'acid: accepts it', 9, fill=RED), t(268, 266, 'coordinate bond', 9, fill=GLASS)], hl='lw'))
    return svg(360, 278, '\n'.join(o))


def energy():
    """steps: exo, endo, ea, cat"""
    o = [t(180, 16, 'Energy level diagrams', 13, weight='bold')]

    def panel(x0, exo, key):
        top, bot = 50, 170
        rh, ph = (80, 140) if exo else (140, 80)
        c = RED if exo else BLUE
        p = [line(x0, bot + 10, x0, top - 10, INK, 1.4) + line(x0, bot + 10, x0 + 160, bot + 10, INK, 1.4),
             t(x0 - 6, 108, 'energy', 9, extra=f' transform="rotate(-90 {x0 - 6} 108)"'), t(x0 + 80, bot + 24, 'progress of reaction →', 9, fill=GLASS),
             t(x0 + 80, top - 18, 'EXOTHERMIC' if exo else 'ENDOTHERMIC', 11, weight='bold', fill=c),
             line(x0 + 8, rh, x0 + 46, rh, INK, 2.5), t(x0 + 27, rh + 14, 'reactants', 9),
             line(x0 + 114, ph, x0 + 154, ph, INK, 2.5), t(x0 + 134, ph + 14, 'products', 9),
             path(f'M{x0 + 46} {rh} C{x0 + 62} {rh} {x0 + 68} {top} {x0 + 80} {top} C{x0 + 92} {top} {x0 + 98} {ph} {x0 + 114} {ph}', GLASS, w=1.8)]
        hx = x0 + 150 if exo else x0 + 12
        p.append(g([arrow(hx, rh, hx, ph, c, 2, 7), t(hx + (-14 if exo else 14), (rh + ph) / 2 + 4, 'ΔH', 10, 'end' if exo else 'start', 'bold', c),
                    t(x0 + 80, bot + 38, 'ΔH negative: heat given out' if exo else 'ΔH positive: heat taken in', 9, weight='bold', fill=c)], hl=key))
        p.append(g([line(x0 + 46, rh, x0 + 86, rh, ORANGE, 1, '3 2'), arrow(x0 + 80, rh, x0 + 80, top + 2, ORANGE, 1.4, 6),
                    t(x0 + 84, (rh + top) / 2 + 4, 'Ea', 10, 'start', 'bold', ORANGE)], hl='ea'))
        p.append(g([path(f'M{x0 + 46} {rh} C{x0 + 64} {rh} {x0 + 70} {top + 34} {x0 + 80} {top + 34} C{x0 + 90} {top + 34} {x0 + 96} {ph} {x0 + 114} {ph}', GREEN, w=1.6, dash='5 3'),
                    t(x0 + 80, top + 28, 'catalyst', 8, fill=GREEN)], s='cat'))
        return ''.join(p)
    o.append(g(panel(20, True, 'exo'), hl='exo'))
    o.append(g(panel(200, False, 'endo'), hl='endo'))
    return svg(370, 228, '\n'.join(o))


ALL = {
    'polar': (polar, 'Polar and non-polar molecules', 47),
    'london': (london, 'London (dispersion) forces', 54),
    'bpe': (bpe, 'Boiling point elevation', 103),
    'osmosis': (osmosis, 'Osmosis and osmotic pressure', 106),
    'concmap': (concmap, 'Concentration units map', 75),
    'acidbase': (acidbase, 'Arrhenius, Brønsted–Lowry and Lewis', 115),
    'energy': (energy, 'Exothermic and endothermic energy diagrams', 161),
}

"""Diagrams for the chem_oct10 notes (flat 2-D vector, a few KB each; plain shapes and text only, rendered by flutter_svg).

data-s="k" shows a group only on step/state k; data-hl="k" dims it on the other steps (see lib/high/notes/jr/notes/svg_prep.dart).
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'chem_models'))
from svglib import BLUE, GLASS, GREEN, INK, ORANGE, RED, WATER, WATER2, arrow, beaker, circ, g, line, path, rect, svg, t  # noqa: E402

GREY = '#7a8a84'
PALE = '#f4f8f6'
YEL = '#f3d36b'


def box(x, y, w, h, title, sub=None, fill=PALE, stroke='#9fb5ab', tc=INK, size=10):
    o = [rect(x, y, w, h, fill, stroke, 1.4, 6), t(x + w / 2, y + (h / 2 + 4 if not sub else h / 2 - 2), title, size, weight='bold', fill=tc)]
    if sub:
        o.append(t(x + w / 2, y + h / 2 + 11, sub, 8.5, fill=GLASS))
    return ''.join(o)


# ---------------------------------------------------------------------------------------------------- Grade 9
def neutral():
    """states: atom (Na, neutral) / ion (Na+, one electron lost)"""
    o = [t(170, 16, 'Counting charges: sodium atom vs sodium ion', 12, weight='bold')]
    cx, cy = 110, 112

    def shells(n_out):
        p = [circ(cx, cy, 22, '#fde3dc', RED, 1.2), t(cx, cy - 2, '11 p⁺', 9, weight='bold', fill=RED), t(cx, cy + 9, '12 n', 8.5, fill=GLASS)]
        for rad in (36, 54, 72):
            p.append(circ(cx, cy, rad, 'none', '#b8c7c0', 1))
        import math
        for rad, n in ((36, 2), (54, 8), (72, n_out)):
            for i in range(n):
                a = 2 * math.pi * i / max(n, 1) - math.pi / 2
                p.append(circ(cx + rad * math.cos(a), cy + rad * math.sin(a), 4.2, BLUE))
        return p
    o.append(g(shells(1) + [t(266, 60, 'Na atom', 12, weight='bold'), t(266, 82, 'protons: +11', 10, fill=RED), t(266, 98, 'electrons: −11', 10, fill=BLUE),
                            line(222, 106, 310, 106, INK, 1), t(266, 122, 'total: 0', 11, weight='bold'), t(266, 138, 'electrically neutral', 9.5, fill=GREEN),
                            t(266, 160, '2, 8, 1', 10, fill=GLASS)], s='atom'))
    o.append(g(shells(0) + [circ(cx + 96, cy - 64, 4.2, BLUE), arrow(cx + 62, cy - 40, cx + 90, cy - 60, BLUE, 1.2, 5), t(cx + 96, cy - 74, 'e⁻ lost', 8.5, fill=BLUE),
                            t(266, 60, 'Na⁺ ion', 12, weight='bold'), t(266, 82, 'protons: +11', 10, fill=RED), t(266, 98, 'electrons: −10', 10, fill=BLUE),
                            line(222, 106, 310, 106, INK, 1), t(266, 122, 'total: +1', 11, weight='bold', fill=RED), t(266, 138, 'not neutral: an ion', 9.5, fill=RED),
                            t(266, 160, '2, 8', 10, fill=GLASS)], s='ion'))
    o.append(t(170, 204, 'Protons never change in a chemical reaction; only electrons move.', 9.5, fill=GLASS))
    return svg(340, 212, '\n'.join(o))


def balance_flow():
    """steps: skel, count, coef, check"""
    o = [t(170, 16, 'Balancing an equation: the flow chart', 12, weight='bold')]
    steps = [('skel', 'Write the skeleton', 'correct formulas, never change them'), ('count', 'Count atoms', 'each element, left and right'),
             ('coef', 'Add coefficients', 'big numbers in front only'), ('check', 'Check and reduce', 'equal counts, lowest ratio')]
    y = 30
    for i, (k, a, b) in enumerate(steps):
        o.append(g([box(70, y, 200, 40, f'{i + 1}. {a}', b, fill='#eef5ff' if i % 2 == 0 else PALE)], hl=k))
        if i < 3:
            o.append(arrow(170, y + 41, 170, y + 55, INK, 1.4, 6))
        y += 56
    o.append(path('M270 160 C318 160 318 76 270 76', ORANGE, w=1.4, dash='4 3') + t(322, 122, 'not equal?', 8.5, 'end', fill=ORANGE) +
             t(322, 133, 'adjust again', 8.5, 'end', fill=ORANGE))
    o.append(t(170, 262, 'N₂ + 3H₂ → 2NH₃ : N 2 = 2, H 6 = 6 (balanced)', 10.5, weight='bold', fill=GREEN))
    return svg(340, 272, '\n'.join(o))


# ---------------------------------------------------------------------------------------------------- Grade 10
def metallic():
    """states: sea (the model), slide (a force moves the layers, bonding stays)"""
    o = [t(170, 16, 'Metallic bonding: cations in a “sea” of electrons', 12, weight='bold'), rect(30, 30, 280, 136, '#fdf6e3', '#d8c79a', 1.2, 6)]

    def ions(rows, dx):
        c = ''.join(f'<circle cx="{64 + col * 44 + dx}" cy="{50 + row * 32}" r="11"/>' for row in rows for col in range(6))
        p = ''.join(f'<text x="{64 + col * 44 + dx}" y="{54 + row * 32}">+</text>' for row in rows for col in range(6))
        return [f'<g fill="#f0b27a" stroke="#b9770e" stroke-width="1">{c}</g>',
                f'<g font-size="11" font-weight="bold" text-anchor="middle" fill="#7e5109">{p}</g>']
    o += ions((2, 3), 0)
    e = [(44, 40), (90, 66), (132, 38), (176, 70), (220, 42), (262, 64), (300, 40), (62, 98), (110, 128), (154, 100), (196, 130), (240, 98), (284, 126),
         (44, 150), (88, 158), (140, 156), (186, 162), (232, 154), (276, 160), (300, 96), (86, 130), (250, 128)]
    o.append(f'<g fill="{BLUE}">' + ''.join(f'<circle cx="{x}" cy="{y}" r="2.6"/>' for x, y in e) + '</g>')
    o.append(g(ions((0, 1), 0) + [t(170, 186, 'positive metal ions (cations) fixed in layers;', 9.5, fill=GLASS),
                                  t(170, 200, 'valence electrons delocalised — free to move anywhere', 9.5, fill=BLUE)], s='sea'))
    o.append(g(ions((0, 1), 22) + [arrow(4, 66, 32, 66, RED, 2, 7), t(4, 58, 'force', 9, 'start', fill=RED),
                                   t(170, 186, 'hammering slides the top layers along;', 9.5, fill=GLASS),
                                   t(170, 200, 'the electron sea still holds them → malleable, not brittle', 9.5, fill=GREEN)], s='slide'))
    return svg(340, 208, '\n'.join(o))


def titration():
    """steps: burette, flask, end"""
    o = [t(170, 16, 'Acid–base titration set-up', 12, weight='bold')]
    o.append(g([line(70, 30, 70, 250, GREY, 3), rect(46, 250, 120, 8, '#9aa8a2', rx=2), line(70, 70, 106, 70, GREY, 3)], hl=None))
    # burette
    o.append(g([rect(100, 30, 16, 150, '#ffffff', GLASS, 1.6, 3), rect(102, 50, 12, 128, '#dbeefe'), line(116, 60, 122, 60, GLASS, 1),
                line(116, 80, 122, 80, GLASS, 1), line(116, 100, 122, 100, GLASS, 1), t(126, 64, '0', 8, 'start', fill=GLASS), t(126, 104, '20', 8, 'start', fill=GLASS),
                rect(104, 180, 8, 14, GLASS), rect(96, 184, 24, 5, '#555', rx=2), line(108, 194, 108, 204, GLASS, 2),
                t(200, 50, 'burette: base of known', 9.5, 'start', fill=BLUE), t(200, 62, 'concentration (titrant)', 9.5, 'start', fill=BLUE),
                line(198, 54, 118, 70, GREY, 1), t(200, 182, 'tap: add drop by drop', 9.5, 'start'), line(198, 178, 122, 186, GREY, 1)], hl='burette'))
    # conical flask
    o.append(g([path('M98 208 L98 220 L76 250 L140 250 L118 220 L118 208 Z', GLASS, '#ffffff', 1.6),
                path('M86 236 L130 236 L140 249 L76 249 Z', None, '#f6f6f6'),
                t(200, 226, 'conical flask: acid (pipette,', 9.5, 'start', fill=RED), t(200, 238, '25.0 mL) + 2–3 drops indicator', 9.5, 'start', fill=RED),
                line(198, 232, 136, 238, GREY, 1), rect(150, 262, 16, 6, '#ffffff', GREY, 1)], hl='flask'))
    o.append(g([path('M86 236 L130 236 L140 249 L76 249 Z', None, '#f7c6dc'), t(200, 262, 'end point: first permanent', 9.5, 'start', fill='#b0306e'),
                t(200, 274, 'pale pink (phenolphthalein)', 9.5, 'start', fill='#b0306e'), line(198, 266, 132, 246, GREY, 1),
                t(36, 278, 'white tile shows the colour change', 8.5, 'start', fill=GLASS)], s='end'))
    return svg(340, 286, '\n'.join(o))


def salt_choice():
    """steps: q1, sol, insol"""
    o = [t(170, 16, 'Which method makes this salt?', 12, weight='bold')]
    o.append(g([box(95, 28, 150, 36, 'Is the salt soluble', 'in water? (solubility table)', fill='#fff7e6', stroke='#e0b860')], hl='q1'))
    o.append(arrow(140, 64, 80, 92, INK, 1.4, 6) + t(96, 80, 'yes', 9, 'end', fill=GREEN) + arrow(200, 64, 262, 92, INK, 1.4, 6) + t(246, 80, 'no', 9, 'start', fill=RED))
    o.append(g([box(8, 94, 156, 36, 'Acid + metal / base /', 'oxide / carbonate', fill='#eef8f1', stroke='#8fc4a2'),
                t(86, 146, '1 excess solid into warm acid', 9, fill=GLASS), t(86, 159, '2 filter off the excess', 9, fill=GLASS),
                t(86, 172, '3 evaporate, crystallise', 9, fill=GLASS), t(86, 192, 'Na, K, NH₄ salts: titrate', 9, fill=BLUE),
                t(86, 204, 'alkali + acid (no excess solid)', 9, fill=BLUE)], hl='sol'))
    o.append(g([box(178, 94, 156, 36, 'Precipitation', '(double decomposition)', fill='#fdecec', stroke='#e09a9a'),
                t(256, 146, '1 mix two soluble salts', 9, fill=GLASS), t(256, 159, '2 filter off the precipitate', 9, fill=GLASS),
                t(256, 172, '3 wash with water, dry', 9, fill=GLASS), t(256, 192, 'e.g. BaCl₂ + Na₂SO₄ →', 9, fill=BLUE),
                t(256, 204, 'BaSO₄↓ + 2NaCl', 9, fill=BLUE)], hl='insol'))
    return svg(340, 212, '\n'.join(o))


PH_COL = [('#d7263d', '1–4', 'red'), ('#f28c28', '5', 'orange'), ('#f4d03f', '6', 'yellow'), ('#3fa34d', '7', 'green'),
          ('#2a9d8f', '8', 'bluish-green'), ('#2e6fd8', '9', 'blue'), ('#5b4bb7', '10', 'bluish-purple'), ('#7b2d8e', '11–14', 'purple')]


def ph_scale():
    """steps: col, ex"""
    o = [t(170, 16, 'Universal indicator colours (textbook Table 4.7)', 12, weight='bold')]
    x = 10
    widths = [64, 36, 36, 36, 36, 36, 36, 40]
    for (c, ph, name), w in zip(PH_COL, widths):
        o.append(rect(x, 30, w, 34, c) + t(x + w / 2, 52, ph, 10, weight='bold', fill='#ffffff' if ph != '6' else INK))
        x += w
    o.append(g([t(42, 78, 'red', 8.5, fill=GLASS), t(92, 78, 'orange', 8.5, fill=GLASS), t(128, 78, 'yellow', 8.5, fill=GLASS), t(164, 78, 'green', 8.5, fill=GREEN),
                t(200, 78, 'b-green', 8.5, fill=GLASS), t(236, 78, 'blue', 8.5, fill=GLASS), t(272, 78, 'b-purple', 8.5, fill=GLASS), t(310, 78, 'purple', 8.5, fill=GLASS)], hl='col'))
    o.append(arrow(14, 96, 150, 96, RED, 1.6, 7) + t(82, 110, 'more acidic (more H⁺)', 9, fill=RED) + arrow(326, 96, 186, 96, BLUE, 1.6, 7) +
             t(256, 110, 'more alkaline (more OH⁻)', 9, fill=BLUE) + t(168, 100, 'neutral', 8.5, fill=GREEN))
    ex = [(20, 'battery acid ≈ 0–1'), (50, 'lemon / orange juice ≈ 2–3'), (80, 'acid rain 2–5, coffee ≈ 5'), (110, 'milk ≈ 6.5'),
          (140, 'pure water 7, blood 7.4'), (170, 'baking soda ≈ 8–9'), (200, 'ammonia solution ≈ 11'), (230, 'bleach ≈ 12–13')]
    o.append(g([t(14, 132 + i * 13, s, 9.5, 'start') for i, (_, s) in enumerate(ex)], hl='ex'))
    o.append(t(230, 150, 'A colour gives a range;', 9.5, fill=GLASS) + t(230, 163, 'a pH meter gives a number', 9.5, fill=GLASS) +
             t(230, 176, '(e.g. 6.84).', 9.5, fill=GLASS))
    return svg(340, 240, '\n'.join(o))


def bond_steps():
    """steps: break, make, net"""
    o = [t(170, 16, 'H₂ + Cl₂ → 2HCl: break bonds, then make bonds', 12, weight='bold')]
    o.append(line(30, 40, 30, 196, INK, 1.4) + t(18, 120, 'enthalpy H', 10, extra=' transform="rotate(-90 18 120)"'))
    o.append(line(44, 150, 120, 150, INK, 2.4) + t(82, 166, 'H₂ + Cl₂', 10, weight='bold'))
    o.append(line(150, 56, 226, 56, INK, 2.4) + t(188, 50, '2H + 2Cl (atoms)', 10, weight='bold'))
    o.append(line(250, 178, 326, 178, INK, 2.4) + t(288, 194, '2HCl', 10, weight='bold'))
    o.append(g([arrow(100, 148, 168, 60, RED, 1.8, 7), t(126, 90, 'break: +436 +243', 9.5, 'end', fill=RED), t(126, 102, '= +679 kJ (in)', 9.5, 'end', fill=RED)], hl='break'))
    o.append(g([arrow(214, 60, 268, 174, BLUE, 1.8, 7), t(256, 120, 'make 2 H–Cl:', 9.5, 'start', fill=BLUE), t(256, 132, '2 × 432 = 864 kJ', 9.5, 'start', fill=BLUE),
                t(256, 144, '(out)', 9.5, 'start', fill=BLUE)], hl='make'))
    o.append(g([line(120, 150, 326, 150, GREY, 1, '4 3'), arrow(314, 151, 314, 177, GREEN, 2, 6), t(196, 214, 'ΔH = 679 − 864 = −185 kJ', 10.5, weight='bold', fill=GREEN),
                t(196, 228, 'products lower than reactants → exothermic', 9, fill=GREEN)], hl='net'))
    o.append(t(196, 246, '(levels drawn to scale)', 8.5, fill=GLASS))
    return svg(340, 254, '\n'.join(o))


# ---------------------------------------------------------------------------------------------------- Grade 11
def _cell(o, label_l='−  cathode', label_r='anode  +', liquid=WATER):
    o.append(beaker(60, 70, 220, 120))
    o.append(rect(62, 100, 216, 89, liquid))
    o.append(rect(96, 50, 16, 120, '#5d6d68') + rect(228, 50, 16, 120, '#5d6d68'))
    o.append(line(104, 50, 104, 34, INK, 1.4) + line(104, 34, 236, 34, INK, 1.4) + line(236, 34, 236, 50, INK, 1.4))
    o.append(rect(150, 26, 40, 16, '#ffffff', INK, 1.2) + line(166, 29, 166, 39, INK, 2) + line(174, 31, 174, 37, INK, 1.2) + t(170, 22, 'd.c.', 8.5, fill=GLASS))
    o.append(t(104, 206, label_l, 9.5, weight='bold', fill=BLUE) + t(236, 206, label_r, 9.5, weight='bold', fill=RED))


def brine():
    """states: dilute, conc"""
    o = [t(170, 14, 'NaCl(aq), inert electrodes: which ion is discharged?', 11, weight='bold')]
    _cell(o)
    o.append(t(170, 120, 'Na⁺  H⁺', 10, fill=GLASS) + t(170, 136, 'Cl⁻  OH⁻', 10, fill=GLASS) + arrow(150, 150, 118, 150, BLUE, 1.2, 5) + arrow(190, 150, 222, 150, RED, 1.2, 5))
    for k in ('dilute', 'conc'):
        right = 'O₂ (OH⁻ discharged)' if k == 'dilute' else 'Cl₂ (Cl⁻ discharged)'
        o.append(g([circ(108, 150 - i * 14, 3, '#ffffff', GLASS, 1) for i in range(3)] + [circ(232, 150 - i * 14, 3, '#ffffff', GLASS, 1) for i in range(3)] +
                   [t(104, 224, 'H₂ (H⁺ discharged)', 9, fill=BLUE), t(244, 224, right, 9, fill=RED),
                    t(170, 244, 'dilute: OH⁻ is easier to discharge → O₂' if k == 'dilute' else 'concentrated (brine): far more Cl⁻ → Cl₂ wins', 9.5, weight='bold', fill=INK),
                    t(170, 258, 'solution left: more concentrated NaCl' if k == 'dilute' else 'solution left: NaOH(aq) — industrial NaOH', 9, fill=GLASS)], s=k))
    return svg(340, 266, '\n'.join(o))


def cuso4():
    """states: inert, copper"""
    o = [t(170, 14, 'CuSO₄(aq): the anode material changes the anode product', 10.5, weight='bold')]
    o.append(beaker(60, 70, 220, 120) + rect(62, 100, 216, 89, '#bcd9f7'))
    o.append(line(104, 50, 104, 34, INK, 1.4) + line(104, 34, 236, 34, INK, 1.4) + line(236, 34, 236, 50, INK, 1.4) + rect(150, 26, 40, 16, '#ffffff', INK, 1.2) +
             line(166, 29, 166, 39, INK, 2) + line(174, 31, 174, 37, INK, 1.2))
    o.append(rect(96, 50, 16, 120, '#b87333') + rect(94, 110, 2, 60, '#8e4b1d') + rect(112, 110, 2, 60, '#8e4b1d'))
    o.append(t(104, 206, '− cathode: Cu²⁺ + 2e⁻ → Cu', 9, fill=BLUE) + t(104, 218, '(pink-brown copper coats it)', 8.5, fill=GLASS))
    o.append(g([rect(228, 50, 16, 120, '#5d6d68')] + [circ(232, 150 - i * 14, 3, '#ffffff', GLASS, 1) for i in range(3)] +
               [t(250, 206, 'graphite/Pt anode: O₂ given off', 9, fill=RED), t(250, 218, '4OH⁻ → 2H₂O + O₂ + 4e⁻', 8.5, fill=RED),
                t(170, 240, 'blue colour fades (Cu²⁺ used up); solution turns acidic (H₂SO₄)', 9, weight='bold')], s='inert'))
    o.append(g([rect(228, 50, 16, 120, '#b87333'), rect(230, 140, 12, 30, '#d39a6a')] +
               [t(250, 206, 'copper anode dissolves:', 9, fill=RED), t(250, 218, 'Cu → Cu²⁺ + 2e⁻ (no gas)', 8.5, fill=RED),
                t(170, 240, 'blue colour stays: Cu²⁺ made at anode = Cu²⁺ used at cathode', 9, weight='bold')], s='copper'))
    return svg(340, 250, '\n'.join(o))


def plating():
    """steps: anode, cathode, ions"""
    o = [t(170, 14, 'Electroplating a spoon with silver', 12, weight='bold')]
    o.append(beaker(60, 70, 220, 120) + rect(62, 100, 216, 89, '#e8eef2'))
    o.append(line(104, 50, 104, 34, INK, 1.4) + line(104, 34, 236, 34, INK, 1.4) + line(236, 34, 236, 50, INK, 1.4) + rect(150, 26, 40, 16, '#ffffff', INK, 1.2) +
             line(166, 29, 166, 39, INK, 2) + line(174, 31, 174, 37, INK, 1.2) + t(146, 30, '−', 10, 'end', fill=BLUE) + t(194, 30, '+', 10, 'start', fill=RED))
    o.append(g([path('M104 50 L104 120', '#8a9a94', w=5) + path('M104 120 C86 124 86 168 104 172 C122 168 122 124 104 120 Z', '#8a9a94', '#c9d1d4', 1.4),
                t(104, 206, 'cathode (−): the spoon', 9.5, weight='bold', fill=BLUE), t(104, 219, 'Ag⁺ + e⁻ → Ag (silver layer)', 8.5, fill=BLUE)], hl='cathode'))
    o.append(g([rect(228, 50, 16, 120, '#d5dbe0', '#9aa5ab', 1), t(236, 206, 'anode (+): pure silver', 9.5, weight='bold', fill=RED),
                t(236, 219, 'Ag → Ag⁺ + e⁻ (dissolves)', 8.5, fill=RED)], hl='anode'))
    o.append(g([t(170, 128, 'Ag⁺(aq)', 10, weight='bold', fill=GLASS), arrow(212, 146, 130, 146, GLASS, 1.4, 6), t(170, 164, 'electrolyte: AgNO₃(aq)', 8.5, fill=GLASS),
                t(170, 240, 'Ag⁺ leaving the solution = Ag⁺ entering it → concentration stays the same', 9, weight='bold')], hl='ions'))
    return svg(340, 248, '\n'.join(o))


def refine():
    """steps: anode, cathode, mud"""
    o = [t(170, 14, 'Purifying (refining) copper by electrolysis', 12, weight='bold')]
    o.append(beaker(60, 70, 220, 120) + rect(62, 100, 216, 89, '#bcd9f7'))
    o.append(line(104, 50, 104, 34, INK, 1.4) + line(104, 34, 236, 34, INK, 1.4) + line(236, 34, 236, 50, INK, 1.4) + rect(150, 26, 40, 16, '#ffffff', INK, 1.2) +
             line(166, 29, 166, 39, INK, 2) + line(174, 31, 174, 37, INK, 1.2) + t(146, 30, '−', 10, 'end', fill=BLUE) + t(194, 30, '+', 10, 'start', fill=RED))
    o.append(g([rect(98, 50, 12, 120, '#c9824e'), t(104, 206, 'cathode (−): thin pure Cu', 9.5, weight='bold', fill=BLUE),
                t(104, 219, 'Cu²⁺ + 2e⁻ → Cu (grows)', 8.5, fill=BLUE)], hl='cathode'))
    o.append(g([rect(222, 50, 28, 120, '#9c6a3f'), circ(230, 80, 2, '#555'), circ(242, 110, 2, '#555'), circ(232, 140, 2, '#555'),
                t(236, 206, 'anode (+): impure Cu', 9.5, weight='bold', fill=RED), t(236, 219, 'Cu → Cu²⁺ + 2e⁻ (thins)', 8.5, fill=RED)], hl='anode'))
    o.append(g([path('M200 188 Q236 178 272 188 Z', '#6b5b4b', '#6b5b4b', 1), t(300, 160, 'anode mud:', 8.5, 'end', fill='#6b5b4b'), t(300, 171, 'Ag, Au, Pt', 8.5, 'end', fill='#6b5b4b'),
                t(170, 240, 'electrolyte CuSO₄(aq) + H₂SO₄; impurities fall or stay dissolved', 9, weight='bold')], hl='mud'))
    o.append(t(170, 128, 'Cu²⁺', 10, weight='bold', fill=GLASS) + arrow(212, 146, 124, 146, GLASS, 1.4, 6))
    return svg(340, 248, '\n'.join(o))


def series():
    """steps: q, ag, ni"""
    o = [t(170, 14, 'Faraday’s second law: two cells in series', 12, weight='bold')]
    for x, sol, k, lab in ((40, '#e8eef2', 'ag', 'AgNO₃(aq)'), (190, '#cdeccf', 'ni', 'Ni(NO₃)₂(aq)')):
        o.append(g([beaker(x, 70, 110, 100), rect(x + 2, 96, 106, 73, sol), rect(x + 20, 56, 10, 96, '#5d6d68'), rect(x + 80, 56, 10, 96, '#5d6d68'),
                    t(x + 55, 190, lab, 9.5, weight='bold'),
                    t(x + 55, 204, 'Ag⁺ + e⁻ → Ag' if k == 'ag' else 'Ni²⁺ + 2e⁻ → Ni', 9, fill=BLUE),
                    t(x + 55, 218, '1 mol e⁻ → 1 mol Ag (108 g)' if k == 'ag' else '1 mol e⁻ → ½ mol Ni (29.5 g)', 8.5, fill=GLASS)], hl=k))
    o.append(g([line(65, 56, 65, 36, INK, 1.4), line(65, 36, 150, 36, INK, 1.4), rect(150, 28, 40, 16, '#ffffff', INK, 1.2), line(190, 36, 275, 36, INK, 1.4),
                line(275, 36, 275, 56, INK, 1.4), line(125, 56, 125, 46, INK, 1.4), line(125, 46, 210, 46, INK, 1.4), line(210, 46, 210, 56, INK, 1.4),
                t(170, 24, 'same current, same time → same charge Q', 9, fill=GLASS),
                t(170, 240, 'mass₁ : mass₂ = equivalent mass₁ : equivalent mass₂', 9.5, weight='bold')], hl='q'))
    return svg(340, 248, '\n'.join(o))


def carbon_cycle():
    """steps: photo, resp, burn, sea"""
    o = [t(170, 14, 'The carbon cycle', 12, weight='bold')]
    o.append(box(120, 120, 100, 40, 'CO₂ in air', '≈ 0.04 % by volume', fill='#eef5ff', stroke='#8fb2d6'))
    o.append(box(10, 30, 96, 36, 'Green plants', fill='#eef8f1', stroke='#8fc4a2') + box(234, 30, 96, 36, 'Animals', fill='#fff7e6', stroke='#e0b860'))
    o.append(box(10, 214, 96, 36, 'Fossil fuels', 'coal, oil, gas', fill='#f2eee9', stroke='#b9a58f') + box(234, 214, 96, 36, 'Oceans, rocks', 'H₂CO₃, CaCO₃', fill='#e7f3fb', stroke='#8fb2d6'))
    o.append(arrow(106, 48, 234, 48, INK, 1.2, 6) + t(170, 42, 'eating (food)', 8.5, fill=GLASS))
    o.append(g([arrow(140, 120, 80, 68, GREEN, 2, 7), t(56, 96, 'photosynthesis', 9, 'start', fill=GREEN), t(56, 107, '(removes CO₂)', 8.5, 'start', fill=GREEN)], hl='photo'))
    o.append(g([arrow(70, 68, 124, 122, RED, 1.6, 6), arrow(268, 68, 210, 122, RED, 1.6, 6), t(282, 96, 'respiration', 9, 'end', fill=RED),
                t(282, 107, '(adds CO₂)', 8.5, 'end', fill=RED), arrow(40, 68, 40, 212, GREY, 1.2, 6, '3 3'), t(46, 150, 'dead plants and', 8, 'start', fill=GLASS),
                t(46, 160, 'animals buried for', 8, 'start', fill=GLASS), t(46, 170, 'millions of years', 8, 'start', fill=GLASS)], hl='resp'))
    o.append(g([arrow(106, 220, 150, 162, ORANGE, 2, 7), t(132, 200, 'burning', 9, 'start', fill=ORANGE), t(132, 211, '(combustion)', 8.5, 'start', fill=ORANGE)], hl='burn'))
    o.append(g([arrow(212, 162, 256, 212, BLUE, 1.6, 6), arrow(270, 212, 222, 160, BLUE, 1.2, 6, '4 3'), t(236, 184, 'dissolves', 8.5, 'end', fill=BLUE),
                t(300, 196, 'released', 8.5, 'end', fill=BLUE)], hl='sea'))
    return svg(340, 258, '\n'.join(o))


def nitrogen_cycle():
    """steps: fix, nitrify, plants, denit"""
    o = [t(10, 14, 'The nitrogen cycle', 12, 'start', 'bold')]
    o.append(box(110, 26, 120, 34, 'N₂ in air (78 %)', fill='#eef5ff', stroke='#8fb2d6'))
    o.append(box(10, 140, 100, 36, 'Plant proteins', fill='#eef8f1', stroke='#8fc4a2') + box(10, 236, 100, 36, 'Animal proteins', fill='#fff7e6', stroke='#e0b860'))
    o.append(box(124, 236, 92, 36, 'NH₃ / NH₄⁺', 'in soil', fill='#f2eee9', stroke='#b9a58f') + box(262, 140, 100, 36, 'Nitrates NO₃⁻', 'in soil', fill='#f2eee9', stroke='#b9a58f'))
    o.append(g([arrow(140, 60, 64, 138, GREEN, 1.6, 6), t(88, 92, 'fixing bacteria', 8.5, 'end', fill=GREEN), t(88, 103, '(legume roots)', 8, 'end', fill=GREEN),
                arrow(222, 60, 300, 138, ORANGE, 1.6, 6), t(272, 84, 'lightning:', 8, 'start', fill=ORANGE), t(272, 95, 'N₂ + O₂ → 2NO', 8, 'start', fill=ORANGE),
                t(272, 106, '→ HNO₃ in rain', 8, 'start', fill=ORANGE), arrow(170, 60, 170, 234, GREY, 1.2, 6, '4 3'),
                t(164, 196, 'Haber process', 8, 'end', fill=GLASS), t(164, 206, 'N₂ + 3H₂ ⇌ 2NH₃', 8, 'end', fill=GLASS), t(164, 216, '(fertilisers)', 8, 'end', fill=GLASS)], hl='fix'))
    o.append(g([arrow(216, 250, 290, 178, BLUE, 1.6, 6), t(262, 226, 'nitrifying bacteria', 8.5, 'start', fill=BLUE), t(262, 237, 'NH₄⁺ → NO₂⁻ → NO₃⁻', 8, 'start', fill=BLUE),
                arrow(110, 254, 122, 254, INK, 1.2, 5), arrow(60, 176, 60, 234, INK, 1.2, 6), t(64, 210, 'eating', 8.5, 'start', fill=GLASS),
                t(116, 290, 'death, waste → decomposers → ammonia', 8.5, fill=GLASS)], hl='nitrify'))
    o.append(g([arrow(262, 158, 112, 158, GREEN, 1.8, 7), t(222, 152, 'roots absorb NO₃⁻', 8.5, fill=GREEN)], hl='plants'))
    o.append(g([path('M350 140 L350 22 L246 22', RED, w=1.8), arrow(250, 22, 232, 34, RED, 1.8, 7), t(254, 36, 'denitrifying bacteria:', 8.5, 'start', fill=RED),
                t(254, 47, 'NO₃⁻ → N₂ (back to air)', 8.5, 'start', fill=RED)], hl='denit'))
    return svg(370, 298, '\n'.join(o))


def frasch():
    """steps: water, air, up"""
    o = [t(170, 14, 'Frasch process: three pipes, one inside another', 12, weight='bold')]
    o.append(rect(0, 70, 340, 200, '#efe7d6') + rect(0, 70, 340, 4, '#8c7a5b') + t(330, 88, 'clay, sand, rock', 8.5, 'end', fill='#8c7a5b'))
    o.append(rect(0, 210, 340, 60, '#f6e27a') + t(330, 262, 'sulphur deposit (deep underground)', 8.5, 'end', fill='#8a6d00'))
    o.append(g([rect(130, 30, 80, 210, '#d6ecfa', GLASS, 1.4), t(110, 50, 'superheated water', 9, 'end', fill=BLUE), t(110, 61, '≈ 170 °C, under pressure', 8.5, 'end', fill=BLUE),
                arrow(116, 44, 136, 44, BLUE, 1.4, 6), arrow(138, 120, 138, 200, BLUE, 1.6, 6), arrow(202, 120, 202, 200, BLUE, 1.6, 6),
                t(64, 236, 'hot water melts S', 9, fill=BLUE), t(64, 247, '(m.p. ≈ 115 °C)', 8.5, fill=BLUE)], hl='water'))
    o.append(g([rect(148, 30, 44, 216, '#fff3b0', '#b59a1c', 1.2), t(232, 40, 'molten sulphur + water', 9, 'start', fill='#8a6d00'), t(232, 51, '+ air froth comes up', 8.5, 'start', fill='#8a6d00'),
                arrow(170, 200, 170, 34, '#b8860b', 1.8, 7), arrow(192, 44, 228, 44, '#b8860b', 1.2, 6), t(232, 62, '→ cooled: ≈ 99.5 % pure S', 8.5, 'start', fill='#8a6d00')], hl='up'))
    o.append(g([rect(164, 18, 12, 236, '#ffffff', GLASS, 1.2), t(170, 26, '', 8), t(236, 120, 'hot compressed air', 9, 'start', fill=RED), t(236, 131, '(smallest, inner pipe)', 8.5, 'start', fill=RED),
                line(234, 124, 176, 124, GREY, 1), arrow(170, 150, 170, 252, RED, 1.4, 6)], hl='air'))
    return svg(340, 272, '\n'.join(o))


def contact():
    """steps: burn, conv, abs, dil"""
    o = [t(170, 14, 'Contact process for sulphuric acid', 12, weight='bold')]
    o.append(g([box(4, 40, 68, 40, 'Burner', 'S + O₂ → SO₂', fill='#fff1e6', stroke='#e0a060'), t(38, 96, 'sulphur + dry air', 8.5, fill=GLASS),
                arrow(72, 60, 88, 60, INK, 1.4, 6), box(88, 40, 58, 40, 'Purifier', 'dust, H₂O out', fill=PALE)], hl='burn'))
    o.append(g([arrow(146, 60, 162, 60, INK, 1.4, 6), box(162, 30, 78, 60, 'Converter', 'V₂O₅ catalyst', fill='#eef5ff', stroke='#8fb2d6'),
                t(201, 102, '≈ 450 °C, 1–2 atm', 8.5, fill=BLUE), t(201, 114, '2SO₂ + O₂ ⇌ 2SO₃', 9, weight='bold', fill=BLUE),
                t(201, 126, 'ΔH = −197 kJ', 8.5, fill=BLUE)], hl='conv'))
    o.append(g([arrow(240, 60, 256, 60, INK, 1.4, 6), box(256, 24, 80, 72, 'Absorber', 'in 98 % H₂SO₄', fill='#fdecec', stroke='#e09a9a'),
                t(296, 108, 'SO₃ + H₂SO₄ → H₂S₂O₇', 8.5, fill=RED), t(296, 120, '(oleum)', 8.5, fill=RED)], hl='abs'))
    o.append(g([arrow(296, 128, 296, 160, INK, 1.4, 6), box(220, 160, 116, 44, 'Diluter', 'water added slowly', fill='#eef8f1', stroke='#8fc4a2'),
                t(278, 220, 'H₂S₂O₇ + H₂O → 2H₂SO₄', 8.5, fill=GREEN), arrow(220, 182, 150, 182, GREEN, 1.6, 7), t(84, 178, '98 % H₂SO₄', 10, weight='bold', fill=GREEN),
                t(84, 192, '(part returns to absorber)', 8.5, fill=GLASS)], hl='dil'))
    o.append(t(110, 240, 'Never SO₃ straight into water: a fine acid mist forms.', 8.5, fill=RED))
    return svg(340, 250, '\n'.join(o))


ALL = {
    'neutral': (neutral, 'Charge count: Na atom (neutral) vs Na⁺ ion', 50),
    'balance': (balance_flow, 'Flow chart for balancing an equation (textbook Fig. 3.4)', 124),
    'metallic': (metallic, 'Metallic bonding: cations in a sea of delocalised electrons', 50),
    'titration': (titration, 'Titration set-up: burette, conical flask, indicator', 138),
    'salts': (salt_choice, 'Choosing a method to prepare a salt', 142),
    'ph': (ph_scale, 'Universal indicator colours and everyday pH values', 149),
    'bonds': (bond_steps, 'Bond breaking and bond making: ΔH for H₂ + Cl₂ → 2HCl', 158),
    'brine': (brine, 'Electrolysis of dilute and concentrated NaCl(aq)', 52),
    'cuso4': (cuso4, 'CuSO₄(aq) with inert and with copper anodes', 54),
    'plating': (plating, 'Electroplating with silver (textbook Fig. 2.6)', 56),
    'refine': (refine, 'Electrolytic refining of copper (textbook Fig. 2.7)', 57),
    'series': (series, 'Two electrolytic cells in series', 61),
    'ccycle': (carbon_cycle, 'The carbon cycle (textbook Fig. 3.5)', 83),
    'ncycle': (nitrogen_cycle, 'The nitrogen cycle (textbook Fig. 3.11)', 98),
    'frasch': (frasch, 'The Frasch process (textbook Fig. 3.12)', 101),
    'contact': (contact, 'The Contact process (textbook Fig. 3.15)', 108),
}

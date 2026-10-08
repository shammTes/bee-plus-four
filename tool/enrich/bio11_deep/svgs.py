"""Small hand-made SVG diagrams for the Grade 11 Biology deep expansion (vector, a few KB each, drawn by flutter_svg).
Groups with data-hl="k" are highlighted one at a time by a steps card (others dimmed); data-s="a b" shows a group only on those steps."""
F = 'font-family="sans-serif"'
INK, MUTE = '#1b2b25', '#55665f'


def svg(w, h, body):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}">\n{body}\n</svg>\n'


def t(x, y, s, size=11, anchor='middle', weight='normal', fill=INK, extra=''):
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{size}" font-weight="{weight}" fill="{fill}" {F}{extra}>{s}</text>'


def box(x, y, w, h, fill, stroke, rx=8, sw=1.5):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'


def line(x1, y1, x2, y2, c=MUTE, w=1.6, extra=''):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="{w}"{extra}/>'


def arrow(x1, y1, x2, y2, c=MUTE, w=1.6, dash=False):
    import math
    a = math.atan2(y2 - y1, x2 - x1)
    hx1, hy1 = x2 - 7 * math.cos(a - .45), y2 - 7 * math.sin(a - .45)
    hx2, hy2 = x2 - 7 * math.cos(a + .45), y2 - 7 * math.sin(a + .45)
    d = ' stroke-dasharray="4 3"' if dash else ''
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="{w}"{d}/>'
            f'<path d="M{x2:.1f} {y2:.1f} L{hx1:.1f} {hy1:.1f} L{hx2:.1f} {hy2:.1f} Z" fill="{c}"/>')


def g(key, *parts):
    return f'<g data-hl="{key}">' + ''.join(parts) + '</g>'


def lbox(x, y, w, h, fill, stroke, lines, size=10.5, bold_first=True):
    out = [box(x, y, w, h, fill, stroke)]
    n = len(lines)
    y0 = y + h / 2 - (n - 1) * (size + 2) / 2 + size * .35
    for i, s in enumerate(lines):
        out.append(t(x + w / 2, round(y0 + i * (size + 2), 1), s, size, weight='bold' if (i == 0 and bold_first) else 'normal'))
    return ''.join(out)


# ------------------------------------------------------------------ Unit 1
def feedback(title, rel, trop, gland, horm, effect, note):
    """Hypothalamus -> pituitary -> gland -> hormone, with the negative-feedback arrows (steps keys k1..k5)."""
    out = [t(190, 16, title, 12.5, weight='bold')]
    out.append(g('k1', lbox(110, 28, 160, 34, '#efe7fb', '#6c3fa0', ['Hypothalamus', 'senses the blood level'])))
    out.append(g('k1', arrow(190, 62, 190, 86, '#6c3fa0'), t(198, 78, rel, 10, 'start', fill='#6c3fa0')))
    out.append(g('k2', lbox(110, 88, 160, 34, '#e6f0fb', '#2c6aa0', ['Anterior pituitary', 'releases the tropic hormone'])))
    out.append(g('k2', arrow(190, 122, 190, 146, '#2c6aa0'), t(198, 138, trop, 10, 'start', fill='#2c6aa0')))
    out.append(g('k3', lbox(110, 148, 160, 34, '#e5f5e7', '#2f7a3e', [gland, 'makes its own hormone'])))
    out.append(g('k3', arrow(190, 182, 190, 206, '#2f7a3e'), t(198, 198, horm, 10, 'start', fill='#2f7a3e')))
    out.append(g('k4', lbox(110, 208, 160, 34, '#fff4d6', '#c98a14', ['Target cells', effect])))
    fb = '#a03a3a'
    out.append(g('k5', f'<path d="M110 225 C40 225 40 105 108 105" fill="none" stroke="{fb}" stroke-width="1.6" stroke-dasharray="4 3"/>',
                 arrow(100, 105, 109, 105, fb), f'<path d="M110 232 C18 232 18 45 108 45" fill="none" stroke="{fb}" stroke-width="1.6" stroke-dasharray="4 3"/>',
                 arrow(100, 45, 109, 45, fb), t(30, 140, '−', 18, weight='bold', fill=fb), t(190, 262, note, 10, fill=fb)))
    out.append(t(190, 280, 'dashed red = high hormone level switches the top glands OFF', 9.5, fill=MUTE))
    return svg(380, 288, '\n'.join(out))


def fb_thyroid():
    return feedback('Thyroxine: negative feedback', 'TRH', 'TSH', 'Thyroid gland', 'thyroxine (T4)', 'metabolic rate ↑', 'too much T4 → less TRH and TSH')


def fb_gonad():
    return feedback('Sex hormones: negative feedback', 'GnRH', 'FSH + LH', 'Testis / ovary', 'testosterone / oestrogen', 'sex characters, gametes', 'high sex hormone → less GnRH, FSH, LH')


def pituitary():
    out = [t(200, 16, 'Hypothalamus and the two lobes of the pituitary', 12.5, weight='bold')]
    out.append(box(80, 26, 240, 40, '#efe7fb', '#6c3fa0'))
    out.append(t(200, 42, 'HYPOTHALAMUS', 11, weight='bold', fill='#6c3fa0'))
    out.append(t(200, 57, 'makes releasing hormones + ADH, oxytocin', 9.5))
    # stalk
    out.append('<path d="M190 66 L186 96 L214 96 L210 66 Z" fill="#f1e8fb" stroke="#6c3fa0" stroke-width="1.2"/>')
    # lobes
    out.append(g('ant', '<ellipse cx="160" cy="122" rx="54" ry="30" fill="#e6f0fb" stroke="#2c6aa0" stroke-width="1.6"/>',
                 t(160, 118, 'ANTERIOR', 10.5, weight='bold', fill='#2c6aa0'), t(160, 131, 'makes 6 hormones', 9.5),
                 arrow(176, 70, 160, 92, '#2c6aa0', 1.2, True), t(118, 82, 'blood vessels', 8.5, fill='#2c6aa0')))
    out.append(g('post', '<ellipse cx="250" cy="122" rx="40" ry="28" fill="#fbe6e6" stroke="#a03a3a" stroke-width="1.6"/>',
                 t(250, 118, 'POSTERIOR', 10.5, weight='bold', fill='#a03a3a'), t(250, 131, 'stores 2', 9.5),
                 arrow(210, 70, 244, 94, '#a03a3a', 1.2), t(282, 82, 'nerve fibres', 8.5, fill='#a03a3a')))
    ant = [('GH', 'bones, muscles'), ('TSH', 'thyroid'), ('ACTH', 'adrenal cortex'), ('Prolactin', 'breasts'), ('FSH', 'ovary / testis'), ('LH', 'ovary / testis')]
    rows = []
    for i, (h, tg) in enumerate(ant):
        y = 172 + i * 17
        rows.append(t(18, y, h, 10.5, 'start', 'bold', '#2c6aa0') + t(80, y, '→ ' + tg, 10, 'start'))
    out.append(g('ant', *rows))
    post = [('ADH', 'kidney tubules'), ('Oxytocin', 'uterus, breasts')]
    rows = []
    for i, (h, tg) in enumerate(post):
        y = 172 + i * 17
        rows.append(t(222, y, h, 10.5, 'start', 'bold', '#a03a3a') + t(284, y, '→ ' + tg, 10, 'start'))
    out.append(g('post', *rows))
    out.append(t(200, 286, 'anterior: “FLAT PG” · posterior: “ADH + OXY” (made in the hypothalamus)', 9.5, fill=MUTE))
    return svg(400, 294, '\n'.join(out))


def adrenal():
    out = [t(190, 16, 'Adrenal gland: two glands in one', 12.5, weight='bold')]
    # kidney + cap
    out.append('<path d="M40 120 C40 70 110 70 110 120 C110 170 40 170 40 120 Z" fill="#f3d9c9" stroke="#8b5a2b" stroke-width="1.5"/>')
    out.append(t(75, 128, 'kidney', 10))
    out.append('<path d="M48 82 Q75 40 104 82 Q75 70 48 82 Z" fill="#f6e08a" stroke="#b08a12" stroke-width="1.5"/>')
    out.append(t(75, 46, 'adrenal', 10, weight='bold'))
    out.append(arrow(112, 70, 170, 70, MUTE, 1.2, True))
    # section
    out.append(g('cx', '<circle cx="250" cy="110" r="70" fill="#f6e08a" stroke="#b08a12" stroke-width="1.6"/>',
                 t(250, 56, 'CORTEX (outer)', 10.5, weight='bold', fill='#7a5a00')))
    out.append(g('md', '<circle cx="250" cy="116" r="34" fill="#f2b8a0" stroke="#a03a3a" stroke-width="1.6"/>',
                 t(250, 113, 'MEDULLA', 10, weight='bold', fill='#a03a3a'), t(250, 126, '(inner)', 9)))
    out.append(g('cx', t(250, 200, 'cortex: steroids — cortisol, aldosterone, sex steroids', 10, fill='#7a5a00'),
                 t(250, 214, 'controlled by ACTH (cortisol) and Na⁺/K⁺ level (aldosterone)', 9.5, fill='#7a5a00')))
    out.append(g('md', t(250, 232, 'medulla: amines — adrenaline, noradrenaline', 10, fill='#a03a3a'),
                 t(250, 246, 'controlled by nerve impulses (fight or flight)', 9.5, fill='#a03a3a')))
    return svg(380, 256, '\n'.join(out))


def glucose():
    out = [t(200, 16, 'Blood glucose: insulin and glucagon pull in opposite directions', 12, weight='bold')]
    out.append(lbox(130, 120, 140, 40, '#e5f5e7', '#2f7a3e', ['NORMAL', 'about 100 mg / 100 cm³']))
    out.append(g('hi', lbox(20, 34, 150, 34, '#fbe6e6', '#a03a3a', ['Glucose HIGH', 'after a meal']),
                 arrow(95, 68, 95, 84, '#a03a3a'), lbox(20, 84, 150, 30, '#fff', '#a03a3a', ['β-cells → INSULIN'], 10),
                 arrow(170, 99, 228, 99, '#a03a3a'), lbox(230, 34, 160, 80, '#fff', '#a03a3a', ['Liver + muscle', 'take glucose in;', 'glucose → glycogen;', 'cells respire more'], 9.5),
                 arrow(300, 114, 250, 124, '#a03a3a'), t(330, 130, 'level falls', 9.5, fill='#a03a3a')))
    out.append(g('lo', lbox(20, 212, 150, 34, '#e6f0fb', '#2c6aa0', ['Glucose LOW', 'fasting, exercise']),
                 arrow(95, 212, 95, 196, '#2c6aa0'), lbox(20, 166, 150, 30, '#fff', '#2c6aa0', ['α-cells → GLUCAGON'], 10),
                 arrow(170, 181, 228, 181, '#2c6aa0'), lbox(230, 166, 160, 80, '#fff', '#2c6aa0', ['Liver', 'glycogen → glucose;', 'glucose released', 'into the blood'], 9.5),
                 arrow(300, 166, 250, 158, '#2c6aa0'), t(330, 156, 'level rises', 9.5, fill='#2c6aa0')))
    out.append(t(200, 266, 'Insulin puts glucose IN store · glucaGON = glucose GONE, bring it back', 9.5, fill=MUTE))
    return svg(400, 274, '\n'.join(out))


# ------------------------------------------------------------------ Unit 2
def male_path():
    out = [t(200, 16, 'Path of sperm and where the fluids join', 12.5, weight='bold')]
    steps = [('Testis', 'makes sperm', 'p1'), ('Epididymis', 'stores, matures', 'p2'), ('Vas deferens', 'carries sperm', 'p3'), ('Urethra', 'semen out', 'p5')]
    xs = [12, 108, 204, 300]
    for (n, d, k), x in zip(steps, xs):
        out.append(g(k, lbox(x, 40, 88, 40, '#e6f0fb', '#2c6aa0', [n, d], 10)))
    for x in xs[:-1]:
        out.append(arrow(x + 88, 60, x + 96 + 2, 60, '#2c6aa0'))
    glands = [('Seminal vesicles', 'alkaline fluid, sugar,', 'prostaglandins', 10), ('Prostate gland', 'thin, milky, alkaline:', 'neutralises acid', 140), ("Cowper's glands", 'mucus that', 'lubricates', 270)]
    for n, a, b, x in glands:
        out.append(g('p4', lbox(x, 118, 120, 50, '#fff4d6', '#c98a14', [n, a, b], 9.5), arrow(x + 60, 118, 344 - (2 - glands.index((n, a, b, x))) * 14, 82, '#c98a14', 1.2, True)))
    out.append(t(200, 192, 'sperm + fluids = SEMEN (fluid gives food, alkali and a medium to swim in)', 10, fill=MUTE))
    out.append(t(200, 208, 'Scrotum keeps testes 3–5 °C cooler · Penis delivers semen into the vagina', 10, fill=MUTE))
    return svg(400, 216, '\n'.join(out))


def sperm():
    out = [t(200, 16, 'Human sperm cell (about 0.05 mm long)', 12.5, weight='bold')]
    out.append(g('h', '<ellipse cx="70" cy="70" rx="40" ry="24" fill="#e6f0fb" stroke="#2c6aa0" stroke-width="1.6"/>',
                 '<path d="M34 58 Q30 70 34 82 Q24 70 34 58 Z" fill="#f2b8a0" stroke="#a03a3a"/>', '<ellipse cx="76" cy="70" rx="24" ry="14" fill="#9cb8dc"/>',
                 t(76, 74, 'nucleus', 9.5), t(30, 112, 'acrosome', 10, fill='#a03a3a'), t(74, 112, 'HEAD', 10, weight='bold')))
    out.append(g('m', box(110, 62, 70, 16, '#fff4d6', '#c98a14', 6), *[f'<path d="M{114 + i * 11} 62 q4 8 0 16" fill="none" stroke="#c98a14" stroke-width="1.4"/>' for i in range(6)],
                 t(145, 112, 'MIDDLE PIECE', 10, weight='bold'), t(145, 126, 'mitochondria', 9.5, fill='#7a5a00')))
    out.append(g('t', '<path d="M180 70 C210 50 230 90 260 70 C290 50 310 90 340 70 C360 58 372 76 388 70" fill="none" stroke="#2c6aa0" stroke-width="2.2"/>',
                 t(290, 112, 'TAIL (flagellum)', 10, weight='bold'), t(290, 126, 'lashes to swim', 9.5)))
    out.append(t(200, 150, 'head = genes + entry enzymes · middle = energy · tail = movement', 10, fill=MUTE))
    return svg(400, 158, '\n'.join(out))


def female():
    out = [t(200, 16, 'Female reproductive organs (front view, simplified)', 12.5, weight='bold')]
    out.append(g('ut', '<path d="M160 70 L240 70 Q244 140 214 170 L186 170 Q156 140 160 70 Z" fill="#fbe6e6" stroke="#a03a3a" stroke-width="1.6"/>',
                 '<path d="M176 82 L224 82 Q224 136 206 156 L194 156 Q176 136 176 82 Z" fill="#f6c9c9" stroke="none"/>', t(200, 110, 'uterus', 10.5, weight='bold'),
                 t(200, 124, 'lining =', 9), t(200, 135, 'endometrium', 9)))
    out.append(g('tb', '<path d="M160 76 C130 60 100 60 78 78" fill="none" stroke="#c98a14" stroke-width="5"/>', '<path d="M240 76 C270 60 300 60 322 78" fill="none" stroke="#c98a14" stroke-width="5"/>',
                 *[f'<line x1="78" y1="78" x2="{66 + i * 5}" y2="{92 + (i % 2) * 4}" stroke="#c98a14" stroke-width="2"/>' for i in range(5)],
                 *[f'<line x1="322" y1="78" x2="{314 + i * 5}" y2="{92 + (i % 2) * 4}" stroke="#c98a14" stroke-width="2"/>' for i in range(5)],
                 t(120, 52, 'fallopian tube (oviduct)', 9.5, fill='#7a5a00'), t(396, 52, 'funnel with fimbriae', 9, 'end', fill='#7a5a00')))
    out.append(g('ov', '<ellipse cx="88" cy="112" rx="22" ry="14" fill="#efe7fb" stroke="#6c3fa0" stroke-width="1.6"/>',
                 '<ellipse cx="312" cy="112" rx="22" ry="14" fill="#efe7fb" stroke="#6c3fa0" stroke-width="1.6"/>', t(88, 142, 'ovary', 10, weight='bold', fill='#6c3fa0'),
                 t(88, 155, 'ova + hormones', 9, fill='#6c3fa0'), line(110, 112, 166, 104, '#6c3fa0', 1, ' stroke-dasharray="3 3"'), t(140, 98, 'ligament', 8.5, fill='#6c3fa0')))
    out.append(g('cx', box(188, 170, 24, 14, '#f2b8a0', '#a03a3a', 4), t(250, 181, '← cervix (neck)', 9.5, 'start', fill='#a03a3a')))
    out.append(g('vg', '<path d="M190 184 L184 246 L216 246 L210 184 Z" fill="#fde9ef" stroke="#a03a3a" stroke-width="1.4"/>',
                 t(250, 220, '← vagina (10–15 cm)', 9.5, 'start', fill='#a03a3a'), t(200, 262, 'vulva (outside): labia, clitoris, openings', 9.5, fill=MUTE)))
    out.append(t(200, 280, 'egg route: ovary → funnel → tube (fertilised here) → uterus (implants)', 9.5, fill=MUTE))
    return svg(400, 288, '\n'.join(out))


def ovum():
    out = [t(190, 16, 'Human ovum (egg cell, about 0.1 mm — just visible)', 12.5, weight='bold')]
    for i in range(14):
        import math
        a = i * 2 * math.pi / 14
        out.append(f'<circle cx="{120 + 70 * math.cos(a):.1f}" cy="{100 + 70 * math.sin(a):.1f}" r="9" fill="#fff4d6" stroke="#c98a14" stroke-width="1"/>')
    out.append('<circle cx="120" cy="100" r="58" fill="#efe7fb" stroke="#6c3fa0" stroke-width="5" stroke-opacity=".35"/>')
    out.append('<circle cx="120" cy="100" r="52" fill="#fbf3fb" stroke="#6c3fa0" stroke-width="1.4"/>')
    out.append('<circle cx="128" cy="96" r="16" fill="#c9b3e6" stroke="#6c3fa0" stroke-width="1.2"/>')
    for x, y in ((100, 120), (140, 130), (96, 84), (150, 112), (110, 66)):
        out.append(f'<circle cx="{x}" cy="{y}" r="2.4" fill="#c98a14"/>')
    labels = [(163, 46, 'follicle cells'), (164, 63, 'jelly coat (zona pellucida)'), (172, 100, 'cell membrane'), (140, 100, 'nucleus (23 chromosomes)'), (140, 130, 'cytoplasm + yolk (food)')]
    for i, (x, y, s) in enumerate(labels):
        ly = 40 + i * 32
        out.append(line(x, y, 236, ly, MUTE, 1))
        out.append(t(240, ly + 4, s, 10, 'start'))
    out.append(t(190, 196, 'no tail — the ovum is moved by cilia and muscle of the oviduct', 10, fill=MUTE))
    return svg(380, 204, '\n'.join(out))


def cycle():
    out = [t(200, 16, 'The 28-day menstrual cycle (ovulation about day 14)', 12.5, weight='bold')]
    x0, w = 20, 360
    seg = [(1, 5, '#f2b8a0', 'menstrual', 'm'), (5, 14, '#f6e08a', 'proliferative / follicular', 'f'), (14, 28, '#bfe3c7', 'secretory / luteal', 'l')]
    for a, b, c, n, k in seg:
        xa, xb = x0 + (a - 1) * w / 27, x0 + (b - 1) * w / 27
        out.append(g(k, box(round(xa, 1), 40, round(xb - xa, 1), 30, c, MUTE, 4, 1), t(round((xa + xb) / 2, 1), 59, n, 9.5, weight='bold')))
    for d in (1, 5, 14, 21, 28):
        x = round(x0 + (d - 1) * w / 27, 1)
        out.append(line(x, 70, x, 76, MUTE, 1) + t(x, 88, f'day {d}', 9))
    xo = round(x0 + 13 * w / 27, 1)
    out.append(g('o', f'<circle cx="{xo}" cy="40" r="6" fill="#6c3fa0"/>', t(xo, 32, 'ovulation (LH surge)', 9.5, weight='bold', fill='#6c3fa0')))
    rows = [('ovary', 'follicle grows → oestrogen', 'corpus luteum → progesterone'),
            ('uterus', 'lining shed, then rebuilt', 'lining thick, glands secrete')]
    for i, (a, b, c) in enumerate(rows):
        y = 112 + i * 22
        out.append(t(20, y, a, 10, 'start', 'bold') + t(78, y, b, 9.5, 'start') + t(380, y, c, 9.5, 'end'))
    out.append(t(200, 160, 'no pregnancy → corpus luteum dies → progesterone falls → lining shed (day 1)', 9.5, fill='#a03a3a'))
    return svg(400, 172, '\n'.join(out))


# ------------------------------------------------------------------ Unit 3
def bone_tree():
    out = [t(200, 16, 'Counting the 206 bones of an adult', 12.5, weight='bold')]
    out.append(lbox(150, 26, 100, 28, '#f3e0c0', '#8b5a2b', ['206 bones'], 11))
    out.append(g('ax', line(200, 54, 100, 70), lbox(40, 70, 120, 28, '#e6f0fb', '#2c6aa0', ['AXIAL 80'], 11)))
    out.append(g('ap', line(200, 54, 300, 70), lbox(240, 70, 120, 28, '#fbe6e6', '#a03a3a', ['APPENDICULAR 126'], 11)))
    ax = [('Skull', '8 cranial + 14 facial = 22'), ('Ear ossicles', '3 + 3 = 6'), ('Hyoid (neck)', '1'), ('Vertebral column', '26 (33 in a child)'), ('Sternum', '1'), ('Ribs', '12 pairs = 24')]
    ap = [('Pectoral girdle', '2 clavicles + 2 scapulae = 4'), ('Arms', '30 + 30 = 60'), ('Pelvic girdle', '2 hip bones'), ('Legs', '30 + 30 = 60')]
    for i, (a, b) in enumerate(ax):
        y = 118 + i * 24
        out.append(g('ax', t(16, y, a, 10, 'start', 'bold', '#2c6aa0'), t(16, y + 11, b, 9.2, 'start')))
    for i, (a, b) in enumerate(ap):
        y = 118 + i * 24
        out.append(g('ap', t(220, y, a, 10, 'start', 'bold', '#a03a3a'), t(220, y + 11, b, 9.2, 'start')))
    out.append(t(310, 236, '22+6+1+26+1+24 = 80', 9.5, fill='#2c6aa0'))
    out.append(t(310, 252, '4+60+2+60 = 126', 9.5, fill='#a03a3a'))
    out.append(t(200, 272, 'each arm: 1+1+1+8+5+14 = 30 · each leg: 1+1+1+1+7+5+14 = 30', 9.5, fill=MUTE))
    return svg(400, 280, '\n'.join(out))


def spine():
    out = [t(190, 16, 'Vertebral column: 33 vertebrae in five regions', 12.5, weight='bold')]
    regs = [('Cervical', 7, '#e6f0fb', '#2c6aa0', 'neck; atlas (C1) nods, axis (C2) turns', 'c'), ('Thoracic', 12, '#e5f5e7', '#2f7a3e', 'chest; each carries a pair of ribs', 'th'),
            ('Lumbar', 5, '#fff4d6', '#c98a14', 'lower back; biggest, carry most weight', 'lu'), ('Sacral', 5, '#fbe6e6', '#a03a3a', 'fused → 1 sacrum; joins the hip girdle', 's'),
            ('Caudal (coccygeal)', 4, '#efe7fb', '#6c3fa0', 'fused → 1 coccyx (vestigial tail)', 'co')]
    y = 30
    for n, k, fill, st, note, key in regs:
        hh = k * 6.4
        parts = []
        for i in range(k):
            parts.append(box(40, round(y + i * 6.4, 1), 40, 5.4, fill, st, 2, 1))
        parts.append(t(92, round(y + hh / 2 - 2, 1), f'{n}: {k}', 10.5, 'start', 'bold', st))
        parts.append(t(92, round(y + hh / 2 + 11, 1), note, 9.5, 'start'))
        out.append(g(key, *parts))
        y += hh + 6
    out.append(t(190, y + 12, 'child 7+12+5+5+4 = 33 · adult 7+12+5+1+1 = 26 bones', 10, fill=MUTE))
    out.append(t(190, y + 26, 'discs of cartilage between vertebrae absorb shock', 9.5, fill=MUTE))
    return svg(380, round(y + 34), '\n'.join(out))


# ------------------------------------------------------------------ Unit 6
def phototropism():
    out = [t(200, 16, 'Phototropism: auxin makes the shoot bend to light', 12.5, weight='bold')]
    for i in range(3):
        x = 30 + i * 130
        for j in range(3):
            out.append(arrow(x - 22, 50 + j * 16, x - 4, 50 + j * 16, '#e0a800', 1.6))
    def shoot(x, bend, k, cap):
        p = [f'<g data-hl="{k}">']
        if bend:
            p.append(f'<path d="M{x + 30} 150 Q{x + 30} 90 {x + 12} 60" fill="none" stroke="#2f7a3e" stroke-width="12" stroke-linecap="round"/>')
        else:
            p.append(f'<line x1="{x + 30}" y1="150" x2="{x + 30}" y2="60" stroke="#2f7a3e" stroke-width="12" stroke-linecap="round"/>')
        p.append(box(x, 150, 60, 14, '#c9a27a', '#8b5a2b', 3, 1))
        p.append(t(x + 30, 182, cap[0], 9.5, weight='bold'))
        p.append(t(x + 30, 195, cap[1], 9.2))
        p.append('</g>')
        return ''.join(p)
    out.append(shoot(20, False, 'a', ('1 light from left', 'tip makes auxin')))
    out.append(g('b', ''.join(f'<circle cx="{190 + (i % 2) * 4}" cy="{74 + i * 9}" r="2.6" fill="#a03a3a"/>' for i in range(7))))
    out.append(shoot(150, False, 'b', ('2 auxin moves to', 'the SHADED side')))
    out.append(shoot(280, True, 'c', ('3 shaded side grows', 'longer → bends to light')))
    out.append(t(200, 214, 'red dots = auxin (IAA). More auxin → cells elongate more on that side.', 9.5, fill=MUTE))
    return svg(400, 222, '\n'.join(out))


def apical():
    out = [t(200, 16, 'Apical dominance: the tip keeps side buds asleep', 12.5, weight='bold')]
    def plant(x, cut):
        p = [line(x, 170, x, 50 if not cut else 80, '#2f7a3e', 6)]
        for y in (140, 115, 90):
            side = 30 if cut else 6
            p.append(line(x, y, x + side, y - (side * .7), '#2f7a3e', 3))
            p.append(line(x, y, x - side, y - (side * .7), '#2f7a3e', 3))
        if cut:
            p.append(t(x, 50, '✂ tip removed', 10, weight='bold', fill='#a03a3a'))
        else:
            p.append('<circle cx="%d" cy="46" r="7" fill="#e0a800"/>' % x)
            p.append(t(x + 12, 40, 'tip: auxin ↓', 9.5, 'start', fill='#a03a3a'))
        p.append(box(x - 30, 170, 60, 14, '#c9a27a', '#8b5a2b', 3, 1))
        return ''.join(p)
    out.append(g('a', plant(100, False), t(100, 200, 'intact: tall, few branches', 10)))
    out.append(g('b', plant(300, True), t(300, 200, 'decapitated: side buds grow', 10), t(300, 213, '(bushy — like pruning)', 9.5)))
    return svg(400, 222, '\n'.join(out))


def root_tip():
    out = [t(190, 16, 'Root tip (long section): four regions', 12.5, weight='bold')]
    zones = [('cap', 'ROOT CAP', 'protects the tip; cells worn away', '#f2d7b0', '#8b5a2b', 238, 262),
             ('div', 'CELL DIVISION', 'small cube cells, big nuclei, mitosis', '#fbe6e6', '#a03a3a', 196, 238),
             ('elo', 'ELONGATION', 'cells take in water, vacuoles join, cells lengthen', '#fff4d6', '#c98a14', 128, 196),
             ('mat', 'MATURATION (root hairs)', 'cells differentiate; root hairs absorb', '#e5f5e7', '#2f7a3e', 34, 128)]
    for k, n, d, fill, st, y1, y2 in zones:
        parts = []
        if k == 'cap':
            parts.append(f'<path d="M60 {y1} L120 {y1} Q120 {y2 + 4} 90 {y2 + 6} Q60 {y2 + 4} 60 {y1} Z" fill="{fill}" stroke="{st}" stroke-width="1.5"/>')
        else:
            parts.append(box(64, y1, 52, y2 - y1, fill, st, 2))
            rows = (y2 - y1) // (8 if k == 'div' else 16)
            for r in range(1, rows):
                parts.append(line(64, y1 + r * (y2 - y1) / rows, 116, y1 + r * (y2 - y1) / rows, st, .6))
        if k == 'mat':
            for y in range(46, 120, 14):
                parts.append(line(64, y, 38, y - 6, st, 1.4) + line(116, y, 142, y - 6, st, 1.4))
        my = (y1 + y2) / 2
        parts.append(line(146, my, 160, my, st, 1))
        parts.append(t(164, round(my - 2, 1), n, 10.5, 'start', 'bold', st))
        parts.append(t(164, round(my + 11, 1), d, 9.2, 'start'))
        out.append(g(k, *parts))
    out.append(t(190, 288, 'growth in length happens only in the bottom few millimetres', 9.5, fill=MUTE))
    return svg(380, 296, '\n'.join(out))


def stems():
    out = [t(200, 16, 'Stem cross-sections: dicot (sunflower) vs monocot (maize)', 12, weight='bold')]
    # dicot
    out.append(g('d', '<circle cx="100" cy="120" r="80" fill="#f4fbf2" stroke="#2f7a3e" stroke-width="3"/>',
                 '<circle cx="100" cy="120" r="34" fill="#fbfbf3" stroke="#c8d8c0" stroke-width="1"/>',
                 *[f'<g transform="rotate({a} 100 120)"><path d="M100 56 Q111 60 108 70 L92 70 Q89 60 100 56 Z" fill="#f6c9c9" stroke="#a03a3a" stroke-width="1"/><path d="M92 72 L108 72 L102 84 L98 84 Z" fill="#9cb8dc" stroke="#2c6aa0" stroke-width=".8"/></g>' for a in range(0, 360, 45)],
                 '<circle cx="100" cy="120" r="49" fill="none" stroke="#c98a14" stroke-width="1" stroke-dasharray="3 2"/>',
                 t(100, 124, 'pith', 10, weight='bold'), t(100, 216, 'DICOT: bundles in a RING', 10.5, weight='bold', fill='#2f7a3e'),
                 t(100, 230, 'cambium ✓ · pith ✓ · cortex ✓', 9.5)))
    # monocot
    import random
    rnd = random.Random(7)
    dots = []
    for _ in range(26):
        while True:
            x, y = rnd.uniform(-66, 66), rnd.uniform(-66, 66)
            if x * x + y * y < 66 * 66:
                break
        dots.append(f'<ellipse cx="{300 + x:.0f}" cy="{120 + y:.0f}" rx="6" ry="5" fill="#f6c9c9" stroke="#a03a3a" stroke-width=".8"/>')
    out.append(g('m', '<circle cx="300" cy="120" r="80" fill="#f4fbf2" stroke="#2f7a3e" stroke-width="3"/>', *dots,
                 t(300, 216, 'MONOCOT: bundles SCATTERED', 10.5, weight='bold', fill='#2f7a3e'), t(300, 230, 'no cambium · no clear pith', 9.5)))
    out.append(t(200, 252, 'red = phloem side / bundle · blue = xylem · dashed = cambium ring · outer line = epidermis', 9, fill=MUTE))
    return svg(400, 260, '\n'.join(out))


def leaf_ts():
    out = [t(200, 16, 'Leaf transverse section: the layers from top to bottom', 12.5, weight='bold')]
    y = 30
    out.append(g('cu', box(30, y, 230, 6, '#f6e08a', '#b08a12', 2, 1), t(270, y + 6, 'waxy cuticle', 10, 'start', 'bold')))
    y += 7
    out.append(g('ue', *[box(30 + i * 23, y, 23, 16, '#ffffff', '#55665f', 2, 1) for i in range(10)], t(270, y + 12, 'upper epidermis (clear)', 10, 'start', 'bold')))
    y += 17
    pal = [box(30 + i * 14.4, y, 13, 44, '#bfe3c7', '#2f7a3e', 5, 1) for i in range(16)]
    pal += [f'<circle cx="{36 + i * 14.4:.1f}" cy="{y + 10 + (j * 12)}" r="2.6" fill="#2f7a3e"/>' for i in range(16) for j in range(3)]
    out.append(g('pa', *pal, t(270, y + 20, 'palisade mesophyll', 10, 'start', 'bold'), t(270, y + 33, 'most chloroplasts', 9.5, 'start')))
    y += 46
    sp = [f'<ellipse cx="{44 + (i % 8) * 28 + (14 if (i // 8) % 2 else 0)}" cy="{y + 12 + (i // 8) * 18}" rx="12" ry="8" fill="#dcefe0" stroke="#2f7a3e" stroke-width="1"/>' for i in range(24) if 44 + (i % 8) * 28 + (14 if (i // 8) % 2 else 0) < 252]
    out.append(g('sp', *sp, t(270, y + 22, 'spongy mesophyll', 10, 'start', 'bold'), t(270, y + 35, 'air spaces for gases', 9.5, 'start')))
    out.append(g('vb', '<circle cx="150" cy="%d" r="16" fill="#fbe6e6" stroke="#a03a3a" stroke-width="1.4"/>' % (y + 28),
                 '<path d="M136 %d A16 16 0 0 1 164 %d Z" fill="#9cb8dc"/>' % (y + 26, y + 26), t(270, y + 52, 'vein (xylem + phloem)', 9.5, 'start', 'bold')))
    y += 66
    le = [box(30 + i * 23, y, 23, 12, '#ffffff', '#55665f', 2, 1) for i in range(10)]
    out.append(g('le', *le, '<path d="M115 %d q8 -8 16 0 q-8 8 -16 0 Z" fill="#bfe3c7" stroke="#2f7a3e"/>' % (y + 6), t(134, y + 30, 'stoma between 2 guard cells', 9.5, 'start'),
                 t(270, y + 9, 'lower epidermis', 10, 'start', 'bold'), t(270, y + 22, 'many stomata', 9.5, 'start')))
    out.append(arrow(123, y + 44, 123, y + 16, '#2c6aa0', 1.4))
    out.append(t(150, y + 50, 'CO₂ in, O₂ and water vapour out', 9.5, 'start', fill='#2c6aa0'))
    return svg(400, y + 58, '\n'.join(out))


def flower():
    out = [t(200, 16, 'Flower (long section): four whorls on a receptacle', 12.5, weight='bold')]
    out.append(line(200, 260, 200, 214, '#2f7a3e', 5) + t(214, 252, 'pedicel (stalk)', 9.5, 'start'))
    out.append('<path d="M168 214 Q200 196 232 214 Z" fill="#cfe8c4" stroke="#2f7a3e"/>' + t(250, 214, 'receptacle', 9.5, 'start'))
    out.append(g('ca', '<path d="M170 212 Q130 205 118 176 Q150 186 178 204 Z" fill="#9ccf8a" stroke="#2f7a3e"/>', '<path d="M230 212 Q270 205 282 176 Q250 186 222 204 Z" fill="#9ccf8a" stroke="#2f7a3e"/>',
                 t(104, 196, 'sepal', 10, 'end', 'bold', '#2f7a3e'), t(104, 208, '(calyx)', 9, 'end')))
    out.append(g('co', '<path d="M176 204 Q100 170 96 92 Q150 120 186 196 Z" fill="#f8c8dc" stroke="#b03a6a"/>', '<path d="M224 204 Q300 170 304 92 Q250 120 214 196 Z" fill="#f8c8dc" stroke="#b03a6a"/>',
                 t(90, 86, 'petal (corolla)', 10, 'end', 'bold', '#b03a6a')))
    out.append(g('an', line(184, 198, 166, 118, '#c98a14', 2), line(216, 198, 234, 118, '#c98a14', 2), '<ellipse cx="166" cy="112" rx="7" ry="11" fill="#f6e08a" stroke="#c98a14"/>',
                 '<ellipse cx="234" cy="112" rx="7" ry="11" fill="#f6e08a" stroke="#c98a14"/>', t(318, 106, 'anther (pollen)', 10, 'start', 'bold', '#7a5a00'),
                 line(242, 110, 314, 104, MUTE, .8), t(318, 140, 'filament', 10, 'start', fill='#7a5a00'), line(228, 150, 314, 138, MUTE, .8),
                 t(318, 154, '= STAMEN (male)', 9.5, 'start', fill='#7a5a00')))
    out.append(g('gy', '<path d="M186 204 Q182 172 200 168 Q218 172 214 204 Z" fill="#e6d3f2" stroke="#6c3fa0" stroke-width="1.4"/>', line(200, 168, 200, 92, '#6c3fa0', 3),
                 '<ellipse cx="200" cy="88" rx="12" ry="6" fill="#c9b3e6" stroke="#6c3fa0"/>', '<circle cx="196" cy="190" r="4" fill="#fff" stroke="#6c3fa0"/>', '<circle cx="205" cy="183" r="4" fill="#fff" stroke="#6c3fa0"/>',
                 t(200, 54, 'stigma (sticky)', 10, weight='bold', fill='#6c3fa0'), line(200, 58, 200, 80, MUTE, .8), t(214, 66, 'style', 9.5, 'start', fill='#6c3fa0'),
                 t(318, 196, 'ovary + ovules', 10, 'start', 'bold', '#6c3fa0'), line(214, 190, 314, 192, MUTE, .8), t(318, 210, '= PISTIL (female)', 9.5, 'start', fill='#6c3fa0')))
    out.append(t(200, 280, 'outside → centre: sepals → petals → stamens → pistil', 10, fill=MUTE))
    return svg(400, 288, '\n'.join(out))


def double_fert():
    out = [t(200, 16, 'Double fertilisation inside the ovule', 12.5, weight='bold')]
    out.append('<ellipse cx="150" cy="140" rx="96" ry="104" fill="#f7f0fb" stroke="#6c3fa0" stroke-width="1.6"/>')
    out.append('<ellipse cx="150" cy="140" rx="60" ry="76" fill="#fffdf6" stroke="#c98a14" stroke-width="1.2"/>')
    out.append(t(150, 30, 'ovule (integuments outside)', 9.5, fill='#6c3fa0') + t(150, 228, 'embryo sac', 9.5, fill='#7a5a00'))
    out.append(g('p', '<path d="M150 0 L150 52 Q150 62 146 70" fill="none" stroke="#2c6aa0" stroke-width="5" stroke-linecap="round"/>', t(160, 46, 'pollen tube via micropyle', 9.5, 'start', fill='#2c6aa0')))
    out.append(g('e', '<circle cx="150" cy="86" r="9" fill="#f6c9c9" stroke="#a03a3a"/>', t(150, 89, 'egg', 7.5),
                 '<circle cx="128" cy="80" r="6" fill="#eee" stroke="#999"/>', '<circle cx="172" cy="80" r="6" fill="#eee" stroke="#999"/>', t(118, 66, 'synergids', 8.5, 'end')))
    out.append(g('pn', '<circle cx="140" cy="140" r="7" fill="#f6e08a" stroke="#c98a14"/>', '<circle cx="160" cy="140" r="7" fill="#f6e08a" stroke="#c98a14"/>', t(150, 160, '2 polar nuclei', 9)))
    out.append(''.join(f'<circle cx="{x}" cy="206" r="5" fill="#ddd" stroke="#999"/>' for x in (136, 150, 164)) + t(150, 196, 'antipodals (3)', 8.5))
    out.append(g('e', lbox(262, 52, 132, 50, '#fbe6e6', '#a03a3a', ['male nucleus 1 + egg', '→ ZYGOTE (2n)', '→ embryo'], 9.5), arrow(262, 78, 162, 86, '#a03a3a', 1.2)))
    out.append(g('pn', lbox(262, 118, 132, 50, '#fff4d6', '#c98a14', ['male nucleus 2 + 2 polar', '→ ENDOSPERM (3n)', '→ food store'], 9.5), arrow(262, 142, 170, 140, '#c98a14', 1.2)))
    out.append(t(328, 196, 'then: ovule → seed', 10, weight='bold') + t(328, 212, 'ovary → fruit', 10, weight='bold'))
    out.append(t(200, 252, 'two fusions at once = double fertilisation (flowering plants only)', 9.5, fill=MUTE))
    return svg(400, 284, out[0] + '\n<g transform="translate(0,24)">\n' + '\n'.join(out[1:]) + '\n</g>')


U1 = {'fb_thy': (fb_thyroid, 'Thyroxine negative feedback loop', 7), 'fb_gon': (fb_gonad, 'Sex hormone negative feedback loop', 12),
      'pit': (pituitary, 'Hypothalamus and pituitary lobes', 3), 'adr': (adrenal, 'Adrenal cortex and medulla', 9), 'glu': (glucose, 'Insulin–glucagon control of blood glucose', 11)}
U2 = {'mpath': (male_path, 'Path of sperm and accessory glands', 28), 'sperm': (sperm, 'Human sperm cell', 29), 'fem': (female, 'Female reproductive organs', 33),
      'ovum': (ovum, 'Human ovum', 34), 'cycle': (cycle, 'Menstrual cycle timeline', 36)}
U3 = {'bones': (bone_tree, 'Bone count tree (206)', 59), 'spine': (spine, 'Vertebral column regions', 61)}
U6 = {'photo': (phototropism, 'Phototropism and auxin', 110), 'apical': (apical, 'Apical dominance', 110), 'root': (root_tip, 'Root tip regions', 118),
      'stems': (stems, 'Dicot and monocot stem sections', 123), 'leaf': (leaf_ts, 'Leaf transverse section', 126), 'flower': (flower, 'Flower long section', 128),
      'dfert': (double_fert, 'Double fertilisation', 130)}

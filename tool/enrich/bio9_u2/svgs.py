"""Small hand-drawn SVG diagrams for Unit 2 (vector, a few KB each, rendered natively by flutter_svg)."""
F = 'font-family="sans-serif"'


def svg(w, h, body):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}">\n{body}\n</svg>\n'


def t(x, y, s, size=12, anchor='middle', weight='normal', fill='#1b2b25', extra=''):
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{size}" font-weight="{weight}" fill="{fill}" {F}{extra}>{s}</text>'


def box(x, y, w, h, fill, stroke, rx=8, extra=''):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="1.5"{extra}/>'


def line(x1, y1, x2, y2, c='#55665f', w=1.6, extra=''):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="{w}"{extra}/>'


def pyramid():
    ranks = [('Kingdom', 'Animalia', 'e.g. all animals'), ('Phylum', 'Chordata', 'backbone'), ('Class', 'Mammalia', 'hair, milk'), ('Order', 'Primates', ''),
             ('Family', 'Hominidae', ''), ('Genus', 'Homo', ''), ('Species', 'sapiens', 'one kind')]
    cols = ['#2f6f4e', '#3f8a5f', '#5aa173', '#79b68a', '#9ccaa6', '#bfdcc4', '#e0efe2']
    out = [t(200, 18, 'The seven ranks — human as the example', 13, weight='bold')]
    top, h = 46, 34
    for i, (r, ex, note) in enumerate(ranks):
        y = top + i * h
        half = 170 - i * 20
        fill = cols[i]
        tc = '#ffffff' if i < 4 else '#1b2b25'
        out.append(f'<rect x="{200 - half}" y="{y}" width="{2 * half}" height="{h - 4}" rx="6" fill="{fill}"/>')
        out.append(t(200, y + 20, f'{r}: <tspan font-style="italic">{ex}</tspan>' if i >= 5 else f'{r}: {ex}', 12, fill=tc, weight='bold'))
    y = top + 7 * h + 6
    out.append(t(6, 40, 'biggest group', 10, 'start', fill='#2f6f4e'))
    out.append(t(394, y - 16, 'smallest,', 10, 'end', fill='#2f6f4e'))
    out.append(t(394, y - 4, 'most alike', 10, 'end', fill='#2f6f4e'))
    out.append(t(200, y + 8, 'King Philip Came Over For Good Soup', 11, fill='#7a4b12', weight='bold'))
    return svg(400, y + 16, '\n'.join(out))


def key():
    # couplets as a tree; each couplet node has data-hl so the steps card highlights one couplet at a time
    out = [t(210, 16, 'Dichotomous key: six animals, five couplets', 13, weight='bold')]
    nodes = [(1, 110, 40, 'gills or lungs?', 'Fish (F)'), (2, 165, 90, 'wings?', 'Bat (B)'), (3, 220, 140, 'flesh or plants?', 'Hyena (D)'),
             (4, 275, 190, 'hoof divided?', 'Donkey (A)'), (5, 330, 240, 'taller than 1.5 m?', 'Cow (C)')]
    for n, x, y, qn, leaf in nodes:
        k = f'k{n}'
        g = [f'<g data-hl="{k}">', box(x - 55, y - 14, 110, 26, '#fff4d6', '#c98a14'), t(x, y + 4, f'{n}. {qn}', 11, weight='bold'),
             line(x - 30, y + 12, x - 50, y + 32, '#c98a14'), box(x - 100, y + 30, 80, 22, '#dff0e4', '#2f6f4e', 6), t(x - 60, y + 45, leaf, 11)]
        if n < 5:
            g.append(line(x + 30, y + 12, x + 55, y + 36, '#c98a14'))
        else:
            g += [line(x + 30, y + 12, x + 40, y + 32, '#c98a14'), box(x, y + 30, 70, 22, '#dff0e4', '#2f6f4e', 6), t(x + 35, y + 45, 'Goat (E)', 11)]
        g.append('</g>')
        out += g
    out.append(t(210, 300, 'left branch = YES (name found) · right branch = NO (go on)', 10, fill='#55665f'))
    return svg(420, 310, '\n'.join(out))


def kingdoms():
    ks = [('Monera', '#e6f0fb', '#2c6aa0', ['prokaryote', 'unicellular', 'wall: not cellulose', 'auto- or heterotroph', 'bacteria']),
          ('Protista', '#f1e8fb', '#6c3fa0', ['eukaryote', 'mostly 1 cell', 'wall: some', 'auto- or heterotroph', 'Amoeba, Euglena']),
          ('Fungi', '#fbf0e3', '#9a5b16', ['eukaryote', 'hyphae; yeast 1 cell', 'wall: chitin', 'absorb food', 'mushroom, yeast']),
          ('Plantae', '#e5f5e7', '#2f7a3e', ['eukaryote', 'multicellular', 'wall: cellulose', 'photosynthesis', 'moss, maize']),
          ('Animalia', '#fbe6e6', '#a03a3a', ['eukaryote', 'multicellular', 'no wall', 'ingest food', 'sponge, human'])]
    out = [t(180, 16, 'Five kingdoms (Whittaker, 1969)', 13, weight='bold')]
    for i, (name, fill, st, rows) in enumerate(ks):
        r, c = divmod(i, 3)
        x = 4 + c * 118 + (59 if r else 0)
        y = 26 + r * 150
        out.append(box(x, y, 114, 142, fill, st))
        out.append(f'<rect x="{x}" y="{y}" width="114" height="24" rx="8" fill="{st}"/>')
        out.append(t(x + 57, y + 17, name, 12.5, weight='bold', fill='#ffffff'))
        for j, row in enumerate(rows):
            out.append(t(x + 57, y + 44 + j * 21, row, 11, fill=st if j == 4 else '#1b2b25', weight='bold' if j == 4 else 'normal'))
    out.append(t(180, 336, 'simple → complex: Many People Find Plants Amazing', 10.5, fill='#55665f'))
    return svg(360, 344, '\n'.join(out))


def protista():
    out = [t(200, 16, 'Kingdom Protista', 13, weight='bold'), box(140, 24, 120, 26, '#f1e8fb', '#6c3fa0'), t(200, 42, 'simple eukaryotes', 11, weight='bold')]
    gs = [('Protozoa', 'animal-like', 'ingest food', ['Sarcodina: pseudopodia', 'Ciliophora: cilia', 'Mastigophora: flagella', 'Sporozoa: none']),
          ('Algae', 'plant-like', 'photosynthesis', ['simple: diatoms, Euglena', 'dinoflagellates', 'complex: red, brown,', 'green (Spirogyra, Volvox)']),
          ('Slime moulds', 'fungus-like', 'absorb food', ['acellular: one big', 'multinucleate mass', 'cellular: amoebae →', 'slug → spores'])]
    for i, (n, like, food, rows) in enumerate(gs):
        x = 8 + i * 130
        out.append(line(200, 50, x + 60, 66))
        out.append(box(x, 66, 124, 150, '#ffffff', '#6c3fa0'))
        out.append(t(x + 62, 84, n, 12, weight='bold', fill='#6c3fa0'))
        out.append(t(x + 62, 100, f'{like} · {food}', 9.5, fill='#55665f'))
        for j, r in enumerate(rows):
            out.append(t(x + 62, 124 + j * 22, r, 9.5))
    return svg(400, 224, '\n'.join(out))


def fungi():
    out = [t(200, 16, 'Fungi: yeast budding and a mushroom basidium', 13, weight='bold')]
    # yeast budding
    out += [f'<ellipse cx="70" cy="80" rx="34" ry="28" fill="#fbf0e3" stroke="#9a5b16" stroke-width="1.5"/>', f'<circle cx="70" cy="80" r="8" fill="#9a5b16"/>',
            f'<ellipse cx="112" cy="58" rx="14" ry="12" fill="#fbf0e3" stroke="#9a5b16" stroke-width="1.5"/>', f'<circle cx="112" cy="58" r="4" fill="#9a5b16"/>',
            t(80, 130, 'yeast: bud grows, then', 10), t(80, 144, 'breaks off (budding)', 10)]
    # ascus with 8 spores
    out.append(box(170, 40, 34, 90, '#fff8ee', '#9a5b16', 16))
    for j in range(8):
        out.append(f'<circle cx="187" cy="{50 + j * 10}" r="4" fill="#c98a14"/>')
    out += [t(187, 146, 'ascus: 8', 10), t(187, 160, 'ascospores', 10)]
    # basidium club with 4 spores
    out.append('<path d="M290 130 L290 80 Q290 60 305 60 Q320 60 320 80 L320 130 Z" fill="#fff8ee" stroke="#9a5b16" stroke-width="1.5"/>')
    for x in (292, 302, 312, 322):
        out += [line(x - 2 if x < 307 else x - 4, 62, x - 4, 48, '#9a5b16', 1.2), f'<circle cx="{x - 4}" cy="44" r="5" fill="#c98a14"/>']
    out += [t(305, 146, 'basidium (club):', 10), t(305, 160, '4 basidiospores', 10)]
    out.append(t(200, 184, 'Sac holds 8, club holds 4 — Ascomycota vs Basidiomycota', 10.5, fill='#55665f'))
    return svg(400, 192, '\n'.join(out))


def altgen():
    out = [t(180, 16, 'Alternation of generations', 13, weight='bold')]
    pts = [(180, 50, 'SPOROPHYTE (2n)', '#2f7a3e'), (300, 130, 'spores', '#55665f'), (180, 210, 'GAMETOPHYTE (n)', '#7a4b12'), (60, 130, 'gametes → zygote', '#55665f')]
    for x, y, s, c in pts:
        w = 130 if 'PHYTE' in s else 110
        out.append(box(x - w / 2, y - 14, w, 26, '#ffffff', c))
        out.append(t(x, y + 4, s, 11, weight='bold', fill=c))
    arrows = [(240, 62, 290, 112, 'makes'), (290, 148, 240, 196, 'grow into'), (120, 196, 70, 148, 'makes'), (70, 112, 120, 62, 'fertilisation')]
    for x1, y1, x2, y2, lab in arrows:
        out.append(line(x1, y1, x2, y2, '#55665f', 1.8))
        out.append(f'<circle cx="{x2}" cy="{y2}" r="3.5" fill="#55665f"/>')
        out.append(t((x1 + x2) / 2 + (14 if x2 > x1 else -14), (y1 + y2) / 2, lab, 9.5, 'start' if x2 > x1 else 'end', fill='#55665f'))
    out.append(t(180, 246, 'moss: gametophyte dominant · fern, pine, maize: sporophyte dominant', 9.5, fill='#55665f'))
    return svg(360, 254, '\n'.join(out))


def plants():
    steps = [('Bryophytes', 'mosses, liverworts', 'no vessels, no seeds', '#c7e3c9'), ('Pteridophytes', 'ferns', '+ vessels (true roots, stems, leaves)', '#a9d5ad'),
             ('Gymnosperms', 'pine, cycads', '+ seeds (naked, on cones)', '#86c18c'), ('Angiosperms', 'maize, teff, beans', '+ flowers and fruits', '#5ea866')]
    out = [t(200, 16, 'Plant groups: each step adds a new feature', 13, weight='bold')]
    for i, (n, ex, add, c) in enumerate(steps):
        x, y = 10 + i * 20, 160 - i * 44
        out.append(box(x, y, 380 - 2 * i * 20, 38, c, '#2f7a3e', 6))
        out.append(t(x + 10, y + 16, n, 12, 'start', 'bold'))
        out.append(t(x + 10, y + 31, ex, 10, 'start', fill='#244a2a'))
        out.append(t(370 - i * 20, y + 24, add, 10, 'end', fill='#16351c'))
    out.append(t(200, 214, 'Brave Pupils Get A’s · gametophyte gets smaller at every step', 10, fill='#55665f'))
    return svg(400, 222, '\n'.join(out))


def symmetry():
    out = [t(200, 16, 'Body symmetry', 13, weight='bold')]
    out.append('<path d="M40 60 Q70 40 95 62 Q120 90 92 118 Q60 140 42 112 Q20 85 40 60 Z" fill="#f5e7c8" stroke="#9a5b16" stroke-width="1.5"/>')
    out += [t(70, 160, 'asymmetrical', 11, weight='bold'), t(70, 174, 'sponge', 10, fill='#55665f')]
    cx, cy = 200, 90
    out.append(f'<circle cx="{cx}" cy="{cy}" r="38" fill="#e6f0fb" stroke="#2c6aa0" stroke-width="1.5"/>')
    for a in range(0, 180, 45):
        import math
        dx, dy = 48 * math.cos(math.radians(a)), 48 * math.sin(math.radians(a))
        out.append(line(cx - dx, cy - dy, cx + dx, cy + dy, '#2c6aa0', 1.2, ' stroke-dasharray="4 3"'))
    out += [t(200, 160, 'radial', 11, weight='bold'), t(200, 174, 'Hydra, jellyfish, starfish', 10, fill='#55665f')]
    out.append('<path d="M330 50 Q350 50 352 70 L356 120 Q340 136 330 136 Q320 136 304 120 L308 70 Q310 50 330 50 Z" fill="#fbe6e6" stroke="#a03a3a" stroke-width="1.5"/>')
    out.append(line(330, 40, 330, 146, '#a03a3a', 1.4, ' stroke-dasharray="4 3"'))
    out += [t(330, 160, 'bilateral', 11, weight='bold'), t(330, 174, 'worms, insects, humans', 10, fill='#55665f')]
    out.append(t(200, 196, 'dashed lines = planes that give identical halves', 10, fill='#55665f'))
    return svg(400, 204, '\n'.join(out))


def insect():
    out = [t(200, 16, 'Insect body · metamorphosis', 13, weight='bold')]
    out += ['<ellipse cx="70" cy="70" rx="18" ry="16" fill="#fff1c9" stroke="#7a4b12" stroke-width="1.5"/>',
            '<ellipse cx="120" cy="70" rx="28" ry="20" fill="#ffe3a3" stroke="#7a4b12" stroke-width="1.5"/>',
            '<ellipse cx="196" cy="70" rx="46" ry="22" fill="#fff1c9" stroke="#7a4b12" stroke-width="1.5"/>',
            line(62, 56, 48, 34, '#7a4b12', 1.4), line(70, 55, 74, 32, '#7a4b12', 1.4)]
    for x in (104, 120, 136):
        out.append(line(x, 88, x - 10, 112, '#7a4b12', 1.4))
    out += ['<path d="M112 52 Q130 18 168 30 Q140 44 124 54 Z" fill="#dbeefa" stroke="#2c6aa0" stroke-width="1.2"/>',
            t(52, 126, 'head', 10, weight='bold'), t(52, 138, 'antennae,', 9), t(52, 149, 'eyes', 9), t(124, 126, 'thorax', 10, weight='bold'), t(124, 138, '6 legs,', 9), t(124, 149, 'wings', 9),
            t(196, 126, 'abdomen', 10, weight='bold'), t(196, 138, 'spiracles', 9)]
    out += [box(260, 30, 132, 50, '#e5f5e7', '#2f7a3e'), t(326, 48, 'incomplete (grasshopper)', 9.5, weight='bold'), t(326, 66, 'egg → nymph → adult', 10),
            box(260, 90, 132, 50, '#fbe6e6', '#a03a3a'), t(326, 108, 'complete (butterfly, fly)', 9.5, weight='bold'), t(326, 126, 'egg → larva → pupa → adult', 9.5)]
    return svg(400, 158, '\n'.join(out))


def fission():
    out = [t(200, 16, 'Binary fission in a bacterium', 13, weight='bold')]
    def cell(x, w, s, extra=''):
        return f'<g data-s="{s}"><rect x="{x}" y="40" width="{w}" height="36" rx="18" fill="#e6f0fb" stroke="#2c6aa0" stroke-width="1.5"/>{extra}</g>'
    dna = lambda x: f'<path d="M{x} 58 q6 -8 12 0 q6 8 12 0" fill="none" stroke="#a03a3a" stroke-width="2"/>'
    out.append(cell(20, 60, 'f1 f2 f3 f4', dna(38)))
    out.append(t(50, 96, '1 grow', 10))
    out.append(f'<g data-s="f2 f3 f4">{box(110, 40, 80, 36, "#e6f0fb", "#2c6aa0", 18)}{dna(120)}{dna(156)}{t(150, 96, "2 copy DNA", 10)}</g>')
    out.append(f'<g data-s="f3 f4">{box(210, 40, 80, 36, "#e6f0fb", "#2c6aa0", 18)}{line(250, 40, 250, 76, "#2c6aa0", 2)}{dna(220)}{dna(256)}{t(250, 96, "3 split", 10)}</g>')
    out.append(f'<g data-s="f4">{box(310, 30, 36, 24, "#e6f0fb", "#2c6aa0", 12)}{box(352, 30, 36, 24, "#e6f0fb", "#2c6aa0", 12)}{box(310, 62, 36, 24, "#e6f0fb", "#2c6aa0", 12)}{box(352, 62, 36, 24, "#e6f0fb", "#2c6aa0", 12)}{t(349, 100, "4 divide again", 10)}{t(349, 112, "every 20–30 min", 10)}</g>')
    return svg(400, 120, '\n'.join(out))


ALL = {'pyramid': (pyramid, 'Hierarchy pyramid (human)', 54), 'key': (key, 'Dichotomous key tree', 59), 'kingdoms': (kingdoms, 'Five kingdom cards', 62),
       'protista': (protista, 'Protista groups', 67), 'fungi': (fungi, 'Yeast, ascus and basidium', 79), 'altgen': (altgen, 'Alternation of generations', 82),
       'plants': (plants, 'Plant group ladder', 83), 'symmetry': (symmetry, 'Body symmetry', 87), 'insect': (insect, 'Insect body and metamorphosis', 99),
       'fission': (fission, 'Binary fission', 64)}

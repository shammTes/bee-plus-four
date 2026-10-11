r"""Grade 12 Unit 4 — Farm Management (pp. 209-258): farm and farm manager, factors of production, production function,
TP/AP/MP and the three stages, MVP = price, costs and revenue, MC = MR, iso-quants, production possibility, records,
depreciation, balance sheet, income and cash-flow statements, planning and budgeting, co-operatives and CBOs."""
from common import set_unit, T, RM, MN, TB, DG, ST, WK, QSet
from svglib import Fig, INK, BLUE, RED, GREEN, PURPLE, ORANGE, GREY, FILL
from agrilib import box, tlines, wrap, flow, hflow, cycle, BROWN

UID = 'agri12-u4'
set_unit(UID)


def fl(c):
    return FILL.get(c, '#F3E9DC')


class Ax:
    """simple chart axes: data (x, y) -> pixels"""
    def __init__(self, f, x0, y0, w, h, xmax, ymax, xt=(), yt=(), xl='', yl='', xmin=0, ymin=0):
        self.f, self.x0, self.y0, self.w, self.h = f, x0, y0, w, h
        self.xmin, self.xmax, self.ymin, self.ymax = xmin, xmax, ymin, ymax
        f.line(x0, y0, x0 + w, y0, INK, 1.4).line(x0, y0, x0, y0 - h, INK, 1.4)
        for v in xt:
            X = self.X(v)
            f.line(X, y0, X, y0 + 4, INK, 1).text(X, y0 + 15, str(v), 9.5, GREY, 'middle', False)
        for v in yt:
            Y = self.Y(v)
            f.line(x0 - 4, Y, x0, Y, INK, 1).text(x0 - 6, Y + 3.5, str(v), 9.5, GREY, 'end', False)
            f.line(x0, Y, x0 + w, Y, GREY, 0.4)
        if xl:
            f.text(x0 + w, y0 + 28, xl, 10, INK, 'end', False)
        if yl:
            f.text(x0 + 2, y0 - h - 8, yl, 10, INK, 'start', False)

    def X(self, x):
        return self.x0 + (x - self.xmin) / (self.xmax - self.xmin) * self.w

    def Y(self, y):
        return self.y0 - (y - self.ymin) / (self.ymax - self.ymin) * self.h

    def line(self, pts, c=BLUE, w=2.4, dash=False, dots=True):
        P = [(round(self.X(x), 1), round(self.Y(y), 1)) for x, y in pts]
        self.f.path('M' + ' L'.join(f'{a} {b}' for a, b in P), c, w, dash=dash)
        if dots:
            for a, b in P:
                self.f.circle(a, b, 2.6, None, 0, c)
        return P

    def smooth(self, fn, a, b, c=BLUE, w=2.4, n=40, dash=False):
        P = [(self.X(a + (b - a) * i / n), self.Y(fn(a + (b - a) * i / n))) for i in range(n + 1)]
        self.f.path('M' + ' L'.join(f'{x:.1f} {y:.1f}' for x, y in P), c, w, dash=dash)
        return P


# ------------------------------------------------------------------ figures
def f_resources():
    return hflow(['Resources: land, labour, capital, management', 'Production process: farm, processing', 'Goods and services: food, wool, hides'],
                 340, bh=64, size=10.5, title='From resources to products (Figure 4.1)')


def f_factors():
    f = Fig(340, 236)
    f.title('Factors of production on an Eritrean farm', 12)
    items = [('Land', 'fields, grazing, water; owned, rented or village land', GREEN, 'rent'),
             ('Labour', 'family, hired (wage), contract, collective (wenfera)', BLUE, 'wages'),
             ('Capital', 'oxen, maresha, pump, store, seed, fertiliser, cash', ORANGE, 'interest'),
             ('Management', 'the farmer who plans, decides and takes the risk', PURPLE, 'profit')]
    for i, (a, b, c, r) in enumerate(items):
        y = 30 + i * 51
        f.rect(4, y, 332, 45, c, 1.3, fl(c), 6)
        f.text(14, y + 19, a, 12, c, 'start')
        tlines(f, 14, y + 34, [b], 9.5, INK, 'start', False)
        f.text(328, y + 19, f'reward: {r}', 9.5, GREY, 'end', False)
    return f


def f_capital():
    f = Fig(340, 200)
    f.title('Fixed and working capital', 12.5)
    f.rect(6, 28, 160, 166, ORANGE, 1.5, fl(ORANGE), 8)
    f.rect(174, 28, 160, 166, BLUE, 1.5, fl(BLUE), 8)
    f.text(86, 48, 'FIXED', 12.5, ORANGE).text(86, 62, 'used for many years', 9.5, GREY, 'middle', False)
    f.text(254, 48, 'WORKING', 12.5, BLUE).text(254, 62, 'used up in one season', 9.5, GREY, 'middle', False)
    for i, t in enumerate(['tractor, pump', 'buildings, stores', 'milking machine', 'irrigation works', 'breeding stock', '(all depreciated)']):
        f.text(86, 86 + i * 18, t, 10.5, INK, 'middle', i == 5)
    for i, t in enumerate(['seed', 'fertiliser, pesticide', 'fuel, feed', 'wages', 'cash for daily costs', '(in variable costs)']):
        f.text(254, 86 + i * 18, t, 10.5, INK, 'middle', i == 5)
    return f


def f_prodfn():
    f = Fig(340, 230)
    f.title('Wheat yield and nitrogen (Table 4.1)', 12.5)
    ax = Ax(f, 44, 190, 270, 150, 100, 35, (0, 20, 40, 60, 80, 100), (0, 10, 20, 30), 'N fertiliser (kg/ha)', 'yield (quintals/ha)')
    ax.line([(0, 2), (20, 5), (40, 11), (60, 18), (80, 25), (100, 31)], GREEN)
    f.text(120, 70, 'y = f(x)', 12, GREEN)
    f.text(120, 86, 'output depends on input', 9.5, GREY, 'middle', False)
    return f


def f_stages():
    f = Fig(340, 270)
    f.title('TP, AP, MP and the three stages (maize, Table 4.2)', 11.5)
    tp = [(0, 10), (1, 14), (2, 20), (3, 28), (4, 32), (5, 35), (6, 36), (7, 35)]
    X = lambda v: 40 + v * 40
    f.rect(X(0), 40, X(3) - X(0), 110, None, 0, '#FBF1E2')
    f.rect(X(3), 40, X(6) - X(3), 110, None, 0, '#E6F3EC')
    f.rect(X(6), 40, X(7) - X(6), 110, None, 0, '#FBE6E0')
    ax = Ax(f, 40, 150, 280, 110, 7, 40, range(8), (0, 20, 40), '', 'TP (kg/ha)')
    ax.line(tp, GREEN)
    f.text(ax.X(1.5), 138, 'Stage I', 10, ORANGE).text(ax.X(4.5), 138, 'Stage II', 10, GREEN).text(ax.X(6.5), 138, 'III', 10, RED)
    ap = [(1, 14), (2, 10), (3, 9.3), (4, 8), (5, 7), (6, 6), (7, 5)]
    mp = [(1, 4), (2, 6), (3, 8), (4, 4), (5, 3), (6, 1), (7, -1)]
    bx = Ax(f, 40, 250, 280, 70, 7, 15, range(8), (0, 5, 10, 15), 'fertiliser (kg/ha)', 'AP, MP', ymin=-2)
    bx.line(ap, BLUE)
    bx.line(mp, RED)
    f.text(bx.X(1.2), bx.Y(14) - 4, 'AP', 10, BLUE, 'start').text(bx.X(3.1), bx.Y(8) - 6, 'MP', 10, RED, 'start')
    return f


def f_mvp():
    f = Fig(340, 230)
    f.title('Where MVP = price of fertiliser (Table 4.3)', 12)
    data = [(1, 20), (2, 30), (3, 40), (4, 20), (5, 15), (6, 5), (7, -5)]
    ax = Ax(f, 44, 180, 270, 140, 7.5, 45, (1, 2, 3, 4, 5, 6, 7), (0, 15, 30, 45), 'kg of fertiliser per ha', 'Nakfa', ymin=-10)
    for x, v in data:
        c = GREEN if v > 15 else (ORANGE if v == 15 else RED)
        y0, y1 = ax.Y(0), ax.Y(v)
        f.rect(ax.X(x) - 11, min(y0, y1), 22, abs(y1 - y0), c, 1.1, fl(c), 2)
    f.line(ax.X(0), ax.Y(15), ax.X(7.5), ax.Y(15), RED, 1.6, dash=True)
    f.text(ax.X(7.4), ax.Y(15) - 5, 'price = 15', 10, RED, 'end')
    f.text(ax.X(5), ax.Y(15) - 22, 'optimum', 10, ORANGE)
    f.text(170, 224, 'MVP = MP × 5 Nakfa per kg of maize', 10, GREY, 'middle', False)
    return f


def f_costs():
    f = Fig(340, 226)
    f.title('Total cost curves', 12.5)
    ax = Ax(f, 40, 180, 250, 140, 10, 100, (), (), 'output (e.g. maize)', 'cost (Nakfa)')
    tfc = 25
    tvc = lambda q: 9 * q - 0.9 * q * q + 0.06 * q ** 3
    ax.smooth(lambda q: tfc, 0, 10, ORANGE, 2.2)
    ax.smooth(tvc, 0, 10, BLUE, 2.2)
    ax.smooth(lambda q: tfc + tvc(q), 0, 10, RED, 2.6)
    f.text(ax.X(10) + 2, ax.Y(tfc) + 4, 'TFC', 10, ORANGE, 'start')
    f.text(ax.X(10) + 2, ax.Y(tvc(10)) + 4, 'TVC', 10, BLUE, 'start')
    f.text(ax.X(9.4), ax.Y(tfc + tvc(9.4)) - 6, 'TC', 10, RED, 'end')
    f.text(170, 222, 'TC = TFC + TVC; fixed costs exist even at zero output', 10, GREY, 'middle', False)
    return f


def f_unitcost():
    f = Fig(340, 226)
    f.title('Per-unit cost curves', 12.5)
    ax = Ax(f, 40, 180, 250, 140, 10, 30, (), (), 'output (quantity)', 'Nakfa per unit')
    tfc = 25
    tvc = lambda q: 9 * q - 0.9 * q * q + 0.06 * q ** 3
    mc = lambda q: 9 - 1.8 * q + 0.18 * q * q
    ax.smooth(lambda q: tfc / q, 1, 10, ORANGE, 2)
    ax.smooth(lambda q: tvc(q) / q, 0.3, 10, BLUE, 2)
    ax.smooth(lambda q: (tfc + tvc(q)) / q, 1.1, 10, RED, 2.4)
    ax.smooth(mc, 0.3, 10, PURPLE, 2.4)
    f.text(ax.X(10) + 2, ax.Y(tfc / 10) + 4, 'AFC', 10, ORANGE, 'start')
    f.text(ax.X(10) + 2, ax.Y(tvc(10) / 10) + 8, 'AVC', 10, BLUE, 'start')
    f.text(ax.X(10) + 2, ax.Y((tfc + tvc(10)) / 10) - 2, 'TAC', 10, RED, 'start')
    f.text(ax.X(9.6), ax.Y(mc(9.6)) - 4, 'MC', 10, PURPLE, 'end')
    f.text(170, 222, 'MC cuts AVC and TAC at their lowest points', 10, GREY, 'middle', False)
    return f


def f_profit():
    f = Fig(340, 230)
    f.title('Maximum profit where MR = MC', 12.5)
    ax = Ax(f, 40, 186, 250, 146, 13, 170, (), (), 'output', 'Nakfa')
    tfc = 25
    tc = lambda q: tfc + 9 * q - 0.9 * q * q + 0.06 * q ** 3
    p = 12
    ax.smooth(lambda q: p * q, 0, 13, GREEN, 2.4)
    ax.smooth(tc, 0, 13, RED, 2.4)
    import math
    q = (1.8 + math.sqrt(1.8 ** 2 - 4 * 0.18 * (9 - p))) / (2 * 0.18)
    f.line(ax.X(q), ax.Y(tc(q)), ax.X(q), ax.Y(p * q), INK, 1.6)
    f.text(ax.X(q) - 4, (ax.Y(tc(q)) + ax.Y(p * q)) / 2, 'biggest gap', 10, INK, 'end')
    f.text(ax.X(q) - 4, (ax.Y(tc(q)) + ax.Y(p * q)) / 2 + 12, '= max profit', 10, INK, 'end')
    f.text(ax.X(13) + 4, ax.Y(p * 13) + 4, 'TR', 10, GREEN, 'start')
    f.text(ax.X(13) + 4, ax.Y(tc(13)) + 4, 'TC', 10, RED, 'start')
    f.text(170, 224, 'here the slopes are equal: MR = MC', 10, GREY, 'middle', False)
    return f


def f_isoquant():
    f = Fig(340, 228)
    f.title('Iso-quants: same output, different mixes', 12)
    ax = Ax(f, 40, 180, 240, 140, 10, 10, (), (), 'labour', 'capital')
    ax.smooth(lambda L: 12 / L, 1.3, 9.5, BLUE, 2.4)
    ax.smooth(lambda L: 24 / L, 2.5, 9.5, GREEN, 2.4)
    f.text(ax.X(9.5) + 2, ax.Y(12 / 9.5) - 4, 'A: 30 q', 10, BLUE, 'start')
    f.text(ax.X(9.5) + 2, ax.Y(24 / 9.5) - 4, 'B: 50 q', 10, GREEN, 'start')
    for L, lab in ((2, 'x'), (5, 'y')):
        f.circle(ax.X(L), ax.Y(12 / L), 4, None, 0, RED)
        f.text(ax.X(L) + 6, ax.Y(12 / L) - 4, lab, 11, RED, 'start')
    f.text(170, 224, 'x to y: less capital, more labour, still 30 quintals', 10, GREY, 'middle', False)
    return f


def f_ppc():
    f = Fig(340, 250)
    f.title('Wheat or maize? (Table 4.5, prices 42 and 24 Nakfa/kg)', 11)
    pts = [(0, 1500), (200, 1400), (400, 1260), (600, 1060), (800, 790), (1000, 440), (1200, 0)]
    ax = Ax(f, 50, 206, 260, 160, 1400, 1600, (0, 400, 800, 1200), (0, 500, 1000, 1500), 'wheat (kg)', 'maize (kg)')
    P = ax.line(pts, BLUE)
    for (x, y), lab in zip(pts, 'ABCDEFG'):
        f.text(ax.X(x) + 5, ax.Y(y) - 5, lab, 10, BLUE, 'start')
    rev = 52560
    ax.line([((rev - 1600 * 24) / 42, 1600), (rev / 42, 0)], ORANGE, 1.6, dash=True, dots=False)
    f.text(ax.X(880), ax.Y(1380), 'iso-revenue line', 9.5, ORANGE, 'start').text(ax.X(880), ax.Y(1270), '52 560 Nakfa', 9.5, ORANGE, 'start')
    f.text(ax.X(250), ax.Y(450), 'inside: possible', 9.5, GREY, 'middle', False)
    f.text(170, 244, 'E and F both touch the highest revenue line', 10, INK, 'middle', False)
    return f


def f_products():
    f = Fig(340, 260)
    f.title('Five product–product relationships', 12.5)
    items = [('Competitive', 'compete for the same land/labour', 'barley vs wheat', RED),
             ('Joint', 'one cannot be made without the other', 'wheat + straw; beef + hide', BLUE),
             ('Complementary', 'more of one raises the other', 'beans before maize', GREEN),
             ('Supplementary', 'one does not affect the other', 'maize and poultry', ORANGE),
             ('Antagonistic', 'one harms the other', 'free-roaming goats and vegetables', PURPLE)]
    for i, (a, b, ex, c) in enumerate(items):
        y = 28 + i * 46
        f.rect(4, y, 332, 40, c, 1.2, fl(c), 6)
        f.text(12, y + 17, a, 11.5, c, 'start')
        f.text(12, y + 32, b, 9.5, INK, 'start', False)
        f.text(328, y + 24, ex, 9.5, GREY, 'end', False)
    return f


def f_deprec():
    f = Fig(340, 226)
    f.title('Straight-line depreciation of a pick-up', 12)
    ax = Ax(f, 56, 176, 250, 132, 5, 100, (0, 1, 2, 3, 4, 5), (0, 25, 50, 75, 100), 'years', 'book value (000 Nakfa)')
    ax.line([(t, 100 - 18 * t) for t in range(6)], ORANGE)
    for t in range(1, 6):
        f.text(ax.X(t) + 4, ax.Y(100 - 18 * t) - 6, str(100 - 18 * t), 9.5, INK, 'start', False)
    f.line(ax.X(0), ax.Y(10), ax.X(5), ax.Y(10), GREY, 1, dash=True)
    f.text(ax.X(0.1), ax.Y(10) - 4, 'salvage 10', 9.5, GREY, 'start', False)
    f.text(170, 218, '(100 000 − 10 000) ÷ 5 = 18 000 Nakfa a year', 10, ORANGE, 'middle')
    return f


def f_balance():
    f = Fig(340, 230)
    f.title('Balance sheet: Assets = Liabilities + Net worth', 11.5)
    f.rect(10, 34, 150, 156, BLUE, 1.5, fl(BLUE), 6)
    f.text(85, 52, 'ASSETS', 12, BLUE).text(85, 66, '(what the farm owns)', 9.5, GREY, 'middle', False)
    f.rect(20, 76, 130, 40, BLUE, 1, '#FFFFFF', 4)
    f.text(85, 92, 'Current', 10.5, INK).text(85, 106, 'cash, eggs, fertiliser', 9, GREY, 'middle', False)
    f.rect(20, 124, 130, 56, BLUE, 1, '#FFFFFF', 4)
    f.text(85, 146, 'Fixed (long-term)', 10.5, INK).text(85, 160, 'land, buildings,', 9, GREY, 'middle', False).text(85, 171, 'machinery', 9, GREY, 'middle', False)
    f.rect(180, 34, 150, 156, RED, 1.5, fl(RED), 6)
    f.text(255, 52, 'LIABILITIES', 12, RED).text(255, 66, '+ NET WORTH', 10.5, GREEN)
    f.rect(190, 76, 130, 40, RED, 1, '#FFFFFF', 4)
    f.text(255, 92, 'Current liabilities', 10, INK).text(255, 106, 'due within 1 year', 9, GREY, 'middle', False)
    f.rect(190, 124, 130, 26, RED, 1, '#FFFFFF', 4)
    f.text(255, 141, 'Long-term loans', 10, INK)
    f.rect(190, 154, 130, 26, GREEN, 1, fl(GREEN), 4)
    f.text(255, 171, 'Net worth (owner)', 10, GREEN)
    f.text(170, 118, '=', 20, INK)
    f.text(170, 212, 'Net worth = assets − liabilities; negative = insolvent', 10, GREY, 'middle', False)
    return f


def f_statements():
    f = Fig(340, 230)
    f.title('Three financial statements', 13)
    items = [('Balance sheet', 'a snapshot on ONE date', 'what is owned and owed; net worth', BLUE),
             ('Income statement', 'over a PERIOD', 'revenue − expenses = net income (profit)', GREEN),
             ('Cash-flow statement', 'month by month, CASH only', 'cash in − cash out = bank balance; no depreciation', ORANGE)]
    for i, (a, b, c_, c) in enumerate(items):
        y = 30 + i * 66
        f.rect(4, y, 332, 60, c, 1.3, fl(c), 6)
        f.text(12, y + 19, a, 12, c, 'start')
        f.text(328, y + 19, b, 9.5, INK, 'end', True)
        f.text(12, y + 42, c_, 10, INK, 'start', False)
    return f


def f_cycle():
    return cycle(['Plan + budget', 'Decide', 'Implement', 'Monitor (records)', 'Evaluate'], 340, 270, bw=110, bh=36, size=11,
                 centre='farm management cycle')


def f_budget():
    f = Fig(340, 230)
    f.title('Partial budget: new wheat variety on 1 ha', 12)
    rows = [('Seed', 400), ('Weeding', 1000), ('Fertiliser', 600), ('Pesticide', 400)]
    x = 20
    for nm, v in rows:
        w = v * 0.05
        f.rect(x, 50, w, 30, RED, 1, fl(RED), 2)
        x += w
    f.text(20, 44, 'extra costs 2 400 Nakfa', 10.5, RED, 'start')
    for i, (nm, v) in enumerate(rows):
        f.text(20 + i * 80, 98, f'{nm} {v}', 9.5, INK, 'start', False)
    f.rect(20, 130, 300, 30, GREEN, 1, fl(GREEN), 2)
    f.text(20, 124, 'extra revenue 6 000 Nakfa', 10.5, GREEN, 'start')
    f.rect(20 + 120, 166, 180, 22, BLUE, 1.4, fl(BLUE), 2)
    f.text(230, 182, 'net benefit 3 600', 10.5, BLUE)
    f.text(170, 214, 'adopt the change if extra revenue > extra cost', 10, GREY, 'middle', False)
    return f


def f_coop():
    f = Fig(340, 270)
    f.title('Seven co-operative principles', 13)
    items = ['Voluntary and open membership', 'Democratic control: one member, one vote', 'Member economic participation',
             'Autonomy and independence', 'Education, training, information', 'Co-operation among co-operatives', 'Concern for community']
    for i, t in enumerate(items):
        y = 30 + i * 33
        c = (BLUE, GREEN, ORANGE, PURPLE)[i % 4]
        f.circle(22, y + 13, 12, c, 1.4, fl(c))
        f.text(22, y + 17, str(i + 1), 11, c)
        f.text(42, y + 17, t, 11, INK, 'start')
    return f


DIAGRAMS = {
    'resources': (f_resources(), 'Resources, production process and products (Figure 4.1)', 213),
    'factors': (f_factors(), 'Factors of production and their rewards', 214),
    'capital': (f_capital(), 'Fixed and working capital', 214),
    'prodfn': (f_prodfn(), 'Production function of wheat (Table 4.1, Figure 4.2)', 216),
    'stages': (f_stages(), 'TP, AP, MP and the three stages of production (Table 4.2, Figure 4.3)', 219),
    'mvp': (f_mvp(), 'Optimum fertiliser where MVP equals price (Table 4.3)', 221),
    'costs': (f_costs(), 'TFC, TVC and TC (Figure 4.4)', 223),
    'unitcost': (f_unitcost(), 'Per-unit cost curves (Figure 4.5)', 224),
    'profit': (f_profit(), 'Profit is greatest where MR = MC', 225),
    'isoquant': (f_isoquant(), 'Iso-quants (Figure 4.7)', 226),
    'ppc': (f_ppc(), 'Production possibility curve and iso-revenue line (Table 4.5, Figure 4.10)', 230),
    'products': (f_products(), 'Product–product relationships', 227),
    'deprec': (f_deprec(), 'Straight-line depreciation', 235),
    'balance': (f_balance(), 'Structure of a balance sheet', 240),
    'statements': (f_statements(), 'Balance sheet, income statement and cash flow compared', 244),
    'cycle': (f_cycle(), 'Planning, decision, implementation, monitoring, evaluation', 247),
    'budget': (f_budget(), 'Partial budget (Table 4.9)', 249),
    'coop': (f_coop(), 'Co-operative principles', 253),
}


# ------------------------------------------------------------------ lessons
L1 = [
    T('=agri12-u4-c05', '4.1.1 Agriculture and the farm', 209,
      '**Agriculture** = an industry that organises **land, capital, labour and management** to produce food and non-food products (fibre, hides, wool, flowers).',
      'A **farm** = an economic unit (a business firm) that grows crops or raises livestock using land, capital, labour and management, aiming at **profit**, or, on a subsistence farm, at feeding the family.',
      '**Eritrean examples:** a 1 ha family farm near Adi Keyh growing barley and taff with two oxen; a commercial dairy near Asmara; a banana farm near Tesseney; a layer farm near Keren.'),
    T('=agri12-u4-c06', '4.1.2 Farm management', 210,
      '**Farm management** = the process by which a farmer **plans, organises, co-ordinates and controls** the farm\'s land, labour and capital to reach goals such as higher output or profit. In short: using **scarce resources with alternative uses** to get the best result year after year.',
      '**Functions of a farm manager:**',
      '- buy inputs and combine them; decide **what** crops and livestock to produce and **how**;',
      '- raise money (saving, borrowing); plan and co-ordinate work;',
      '- pay **wages, interest and rent**;',
      '- **keep records** and use them;',
      '- **innovate** (new varieties, methods);',
      '- **bear the risk** and uncertainty of success or failure.',
      '**Objectives:** a **commercial** farm maximises profit (or minimises cost per unit); a **subsistence** farm aims at **self-sufficiency** with few inputs.',
      '**Problems in Eritrea:** small farms, traditional methods, little capital, slow adoption of innovations, poor input supply, low managerial skills, weak communication and markets.'),
    T('=agri12-u4-c07', '4.1.3 Agriculture as an industry', 212,
      'Modern agriculture is more than farming: it includes the firms that **make and sell inputs** (seed, fertiliser, machinery), **process and market** products (dairies, mills, tanneries), and the services of **education, research, extension and market information**. In developing countries it is the **largest employer** and the main livelihood. It must also be **sustainable**: good for the environment as well as for income.'),
    T('=agri12-u4-c08', '4.1.4 Resources and factors of production', 213,
      '**Economics** = the study of how people use **limited resources** to satisfy **unlimited wants**. Every farmer must decide: **what** to produce, **how** to produce it, and **how much**.',
      '**Resources have three features:** they have **economic value** (you pay for them), they are **limited**, and they have **alternative uses** (so choosing one use means giving up another: the **opportunity cost**).',
      '**Factors of production:**',
      '- **Land**: the most important factor for a farmer.',
      '- **Labour**: physical and mental work; skilled labour is **human capital**. Its productivity depends on hours, climate, skill, organisation, equipment and pay. Forms: hired (wage), contract (per task), **family**, **collective** (neighbours working together in turn, as at harvest).',
      '- **Capital**: anything made by people and used in production: **fixed capital** lasts many years (tractor, store, milking machine); **working capital** is used up in one season (seed, fertiliser, cash for wages).',
      '- **Management / entrepreneurship**: organising the other factors, making decisions, trying new ideas, carrying the risk.',
      '**Resources vs resource services:** fertiliser, seed and water are **used up**; labour, implements and buildings give **services**. **Fixed resources** (buildings, machinery) do not change with output in the planning period; **variable resources** (seed, fertiliser) do.'),
    DG('resources-fig', 'Resources → production → products', 213, 'resources'),
    DG('factors-fig', 'Four factors and their rewards', 214, 'factors', 'Land earns rent, labour wages, capital interest, management profit.'),
    DG('capital-fig', 'Fixed or working capital?', 214, 'capital'),
    'agri12-u4-c01', 'agri12-u4-c03',
    T('=agri12-u4-c09', '4.1.5 The production function', 215,
      'A **production function** shows how output (**y**) depends on inputs (**x**) with a given technology. It can be shown as a **table**, a **graph** or an **equation**: y = f(x), or with many inputs y = f(x₁, x₂, …, xₙ). With **one variable input** the others are held fixed: y = f(x₁ | x₂, …, xₙ).',
      'Farming is a **biological** process: the farmer controls fertiliser, seed and land, but **not** rainfall or sunshine.',
      '**Key measures:**',
      '- **Total product (TP)**: total output.',
      '- **Average product (AP)** = TP ÷ x (output per unit of input).',
      '- **Marginal product (MP)** = ΔTP ÷ Δx (extra output from one more unit of input). MP decides the best input level.',
      '**Law of diminishing returns:** when more and more of one input is added to fixed amounts of others, the **extra output from each added unit eventually falls**.'),
    DG('prodfn-fig', 'A production function', 216, 'prodfn'),
    TB('maize-tb', 'Maize and fertiliser (Table 4.2)', 219, ['Fertiliser (kg/ha)', 'TP', 'AP = TP ÷ x', 'MP = ΔTP ÷ Δx'],
       [['0', '10', '–', '–'], ['1', '14', '14.0', '4'], ['2', '20', '10.0', '6'], ['3', '28', '9.3', '8'],
        ['4', '32', '8.0', '4'], ['5', '35', '7.0', '3'], ['6', '36', '6.0', '1'], ['7', '35', '5.0', '−1']], layout='grid'),
    WK('wk-apmp', 'Calculating AP and MP', 218,
       'From Table 4.1 (wheat), N = 40 kg gives 11 quintals and N = 60 kg gives 18 quintals. Find the AP at 60 kg and the MP between 40 and 60 kg.',
       ['AP = TP ÷ x = 18 ÷ 60 = 0.30 quintal per kg of N.', 'MP = ΔTP ÷ Δx = (18 − 11) ÷ (60 − 40) = 7 ÷ 20 = 0.35 quintal per kg.'],
       'AP = 0.30 q/kg; MP = 0.35 q/kg (each extra kg of N in that range adds 35 kg of grain).'),
    T('stages-txt', 'The three stages of production', 219,
      '- **Stage I** (from zero until **MP = AP**, where AP is highest): TP and AP rise; the input is **under-used**, so use more. Not rational to stop here.',
      '- **Stage II** (from MP = AP until **MP = 0**, where TP is highest): the **rational** stage; the best level lies here.',
      '- **Stage III** (**MP negative**): adding input **reduces** TP. Irrational even if the input were free: you lose output **and** pay for the input.',
      'In Table 4.2 MP rises up to the 3rd kg, then falls (diminishing returns from the 4th kg); MP is 0 a little after 6 kg and negative at 7 kg.'),
    DG('stages-fig', 'Stages on a graph', 219, 'stages'),
    T('mvp-txt', 'How much fertiliser pays best? MVP = price', 221,
      'The best point in Stage II depends on **prices**. **Marginal value product (MVP) = MP × price of output**: the extra money from one more unit of input.',
      '- MVP > price of input → **use more** (it pays).',
      '- MVP < price of input → **use less**.',
      '- **Profit is greatest where MVP = price of input.**',
      'With maize at 5 Nakfa/kg and fertiliser at 15 Nakfa/kg (Table 4.3), MVP = 15 at **5 kg/ha**, so apply 5 kg/ha.',
      'The same idea in output terms: produce up to where **marginal revenue (MR) = marginal cost (MC)**. MR = ΔTR ÷ ΔQ; for a small farm selling at the market price, MR = price.'),
    DG('mvp-fig', 'MVP and the price line', 221, 'mvp'),
    WK('wk-mvp', 'Finding the optimum fertiliser rate', 221,
       'Maize sells at 4 Nakfa/kg and fertiliser costs 16 Nakfa/kg. Using the MP column of Table 4.2 (4, 6, 8, 4, 3, 1, −1 for the 1st to 7th kg), how many kg should be applied?',
       ['MVP = MP × 4: 16, 24, 32, 16, 12, 4, −4.', 'Compare with 16 Nakfa: the 1st to 4th kg each earn at least 16; the 5th earns only 12.', 'So stop after the 4th kg (MVP = price at 4 kg).'],
       '4 kg/ha. A cheaper input or a dearer crop would push the optimum higher.'),
    T('costs-txt', 'Costs and revenue', 222,
      '- **Fixed costs (FC)** do not change with output and are paid even if nothing is produced: machinery and buildings (depreciation, interest, insurance), land tax, rent.',
      '- **Variable costs (VC)** change with output: seed, fertiliser, pesticide, fuel, hired labour.',
      '- **Total cost (TC) = FC + VC**. Per unit: **AFC = FC ÷ Q** (always falls), **AVC = VC ÷ Q**, **TAC (ATC) = TC ÷ Q**, **MC = ΔTC ÷ ΔQ**. AVC, TAC and MC first fall, reach a minimum and then rise; MC cuts AVC and TAC at their lowest points.',
      '- **Total revenue (TR) = quantity × price**: a straight line for a farm that sells at the market price.',
      '- **Net revenue (profit) = TR − TC.** It is greatest where **MR = MC**: produce one more unit while MC < MR; stop when MC > MR.'),
    DG('costs-fig', 'TFC, TVC, TC', 223, 'costs'),
    DG('unitcost-fig', 'Per-unit costs', 224, 'unitcost'),
    DG('profit-fig', 'MR = MC', 225, 'profit'),
    WK('wk-cost', 'Fixed or variable? Profit or loss?', 222,
       'A poultry farmer has yearly costs: depreciation of the house 6 000, interest on the loan for it 2 000, feed 30 000, chicks 8 000, vaccines 1 000, hired labour 9 000 Nakfa. He sells 9 000 trays of eggs at 7 Nakfa. Find FC, VC, TC and profit.',
       ['FC = depreciation + interest = 6 000 + 2 000 = 8 000.', 'VC = 30 000 + 8 000 + 1 000 + 9 000 = 48 000.', 'TC = 8 000 + 48 000 = 56 000.', 'TR = 9 000 × 7 = 63 000.', 'Profit = 63 000 − 56 000 = 7 000 Nakfa.'],
       'FC 8 000, VC 48 000, TC 56 000, profit 7 000 Nakfa.'),
    T('inputs-txt', 'How to produce: combining two inputs', 225,
      'Many mixes of two inputs can give the same output. An **iso-quant** joins all the combinations (for example of labour and capital) that give **one fixed output**. The rate at which one input can replace another is the **marginal rate of substitution**.',
      '**Least-cost (best) combination:** MP of input 1 ÷ its price = MP of input 2 ÷ its price, i.e. **MP₁/P₁ = MP₂/P₂**: the last Nakfa spent on each input brings the same extra output.',
      'In Table 4.4 (wage 50 Nakfa a day, capital rent 200 Nakfa a day) this happens at combination 5: MP of labour ÷ wage = 80 ÷ 50 = **1.6** = MP of capital ÷ rent = 320 ÷ 200.'),
    DG('isoquant-fig', 'Iso-quants', 226, 'isoquant'),
    T('products-txt', 'What to produce: two products', 227,
      'With fixed resources a farmer can shift land and labour between products. The **production possibility curve (PPC)** shows all combinations of two products that the resources can produce. Points **on** or **inside** it are possible; points **outside** are not.',
      '**Marginal rate of product substitution (MRPS)** = how much of one product must be given up to get one more unit of the other.',
      '**Best combination:** where the PPC just touches the highest **iso-revenue line** (all combinations giving the same TR = Qₘ × Pₘ + Q_w × P_w); algebraically, where the amount of maize given up per kg of extra wheat equals the price ratio P_wheat ÷ P_maize.'),
    DG('products-fig', 'Five relationships between products', 227, 'products'),
    DG('ppc-fig', 'Choosing the product mix', 230, 'ppc'),
    WK('wk-ppc', 'Checking Table 4.5 with revenue', 230,
       'Wheat sells at 42 and maize at 24 Nakfa/kg. Compare the total revenue of plans D (600 wheat, 1 060 maize), E (800, 790), F (1 000, 440) and G (1 200, 0).',
       ['D: 600 × 42 + 1 060 × 24 = 25 200 + 25 440 = 50 640.', 'E: 33 600 + 18 960 = 52 560.', 'F: 42 000 + 10 560 = 52 560.', 'G: 50 400 + 0 = 50 400.'],
       'E and F tie at 52 560 Nakfa, the highest. The textbook picks F because there the substitution rate (1.75) equals the price ratio 42 ÷ 24 = 1.75; moving from E to F leaves revenue unchanged.'),
    RM('u4-err1', 'Textbook checks in 4.1', 217,
       '- Equation 4.3 is printed the same as 4.2. With one variable input it should read **y = f(x₁ | x₂, …, xₙ)** (x₂ … xₙ held fixed).',
       '- MRPS is defined once as ΔM/ΔW and once as ΔW/ΔM; Table 4.5 uses **Δmaize ÷ Δwheat**, compared with **P_wheat ÷ P_maize**.',
       '- In Table 4.2 maize yields 10 kg with no fertiliser, so AP at 1 kg (14) is higher than later; this is why AP falls from the start in that table.'),
    T('=agri12-u4-c02', 'Exam favourites from 4.1', 219,
      '- **Diminishing returns**: each extra bag of fertiliser adds less than the last.',
      '- **Opportunity cost**: the value of the best alternative given up.',
      '- **Stage II** is the rational stage; **MVP = price of input**; **MR = MC**.',
      '- **Fixed vs variable** costs: insurance, depreciation, rent are fixed; fuel, seed, fertiliser, casual labour are variable.',
      '- Production function → **how much**; iso-quant → **how** to produce; PPC → **what** to produce.'),
]

L2 = [
    T('=agri12-u4-c10', '4.2.1 Farm records and accounts', 234,
      '**Why keep records?** To see the farm\'s **strong and weak points**, find problems and correct them, show a lender that a loan can be repaid, help the farmer think and decide systematically, and give government data for policy.',
      '**Good records are** useful, correctly collected, designed for the user, and **simple**.',
      '**A complete set:** physical inventory, depreciation, accounts receivable and payable, receipts, expenditure, labour, machinery and production records.',
      '- **Inventory (asset register)**: a list, at least **once a year**, of everything the farm owns, with quantities and money values (land, buildings, machinery, livestock, stored grain, supplies), after depreciation.',
      '- **Depreciation**: loss of value of machinery, vehicles, tools and buildings through **age, wear and tear, and obsolescence**. It is a **non-cash cost** written off each year: **annual depreciation = (cost price − salvage value) ÷ expected life**.',
      '- **Income and expenditure**: keep farm and household money **separate**; record produce eaten at home or given as rations. Sources: bank statements, cash analysis book, petty cash book, wage book, cheque counterfoils, invoices and receipts.',
      '- **Journal**: the book in which **all transactions** are recorded **in date order**.'),
    DG('deprec-fig', 'Book value falls each year', 235, 'deprec'),
    WK('wk-deprec', 'Exercise 4.2: a diesel water pump', 238,
       'A pump costs 90 000 Nakfa, has a salvage value of 15 000 Nakfa and a life of 8 years. Find the annual depreciation and the book value after 4 years.',
       ['Annual depreciation = (90 000 − 15 000) ÷ 8 = 75 000 ÷ 8 = 9 375 Nakfa.', 'After 4 years: 4 × 9 375 = 37 500 written off.', 'Book value = 90 000 − 37 500 = 52 500 Nakfa.'],
       '9 375 Nakfa a year; book value 52 500 Nakfa after 4 years.'),
    TB('journal', 'A farm journal (Table 4.6, Alem Farm)', 238, ['Date (2009)', 'Item', 'Nakfa', 'Type'],
       [['4 Jan', 'Sprayer bought from government shop', '300', 'Expense'], ['10 Feb', 'Maize sold to a merchant', '700', 'Revenue'],
        ['19 Mar', '100 hens sold to Ato Berhe', '5 000', 'Revenue'], ['21 May', 'Poultry feed bought at the market', '1 000', 'Expense'],
        ['26 May', 'Five new baskets', '150', 'Expense']], 'Totals: revenue 5 700, expenses 1 450, so cash surplus 4 250 Nakfa for January–May.', layout='cards'),
    T('=agri12-u4-c11', '4.2.2 Production, labour and machinery records', 239,
      '- **Crop records**: field number, area, soil test, variety, seed, fertiliser, weeding, pest control, yield.',
      '- **Livestock records**: feed, medicine, dosing, marketing costs; for each animal milk yield, calving dates, weaning weight, weight gain, wool.',
      '- **Labour records**: workers, contracts, wages, rations, medical costs, loans, leave.',
      '- **Machinery records**: model, age, book value, repairs, services, hours worked, insurance.',
      'They show where yields or costs go wrong, e.g. a cow whose milk falls after every calving, or a field that always yields less.'),
    T('=agri12-u4-c12', '4.2.3 Financial statements', 239,
      'A full set = **balance sheet**, **income statement** and **cash-flow statement**.',
      '**Balance sheet**: the financial position on **one date** (e.g. 31 December). **Accounting equation: Assets = Liabilities + Capital (net worth).**',
      '- **Assets** (what the farm owns), by **liquidity**: **current** (cash, bank, unsold produce, supplies, debtors; turned into cash within 12 months) and **fixed / non-current** (land, buildings, machinery, orchards, breeding stock; most are depreciated).',
      '- **Liabilities** (what it owes): **current** (due within a year: accounts payable, interest, wages, tax) and **long-term** (loans for tractors, buildings).',
      '- **Net worth = assets − liabilities**: what the owner would keep after selling everything and paying all debts. Negative net worth = **insolvent**.',
      '**Income statement (profit and loss)**: revenue, expenses and **net income or loss** over a **period**. Only items that change capital count: a bank loan is **not** revenue; buying a tractor is **not** an expense (its depreciation is).',
      '**Cash-flow statement**: only **actual cash** in and out, month by month, in the month paid or received: operating, capital and non-farm income; operating and capital spending, debt repayments, household spending. **Depreciation is not included** (no cash moves).'),
    DG('balance-fig', 'Balance-sheet structure', 240, 'balance'),
    DG('statements-fig', 'Which statement shows what?', 244, 'statements'),
    TB('alem-bs', 'Balance sheet of Alem Farm, 31 Dec 2009 (Table 4.7)', 242, ['Item', 'Nakfa'],
       [['Current assets (cash 5 000, bank 2 000, eggs 5 000, fertiliser 4 000 + 5 000)', '21 000'], ['Long-term assets (building 50 000, machinery 20 000)', '70 000'],
        ['Total assets', '91 000'], ['Current liabilities (accrued 1 000, borrowed fertiliser 3 000, owed to MoA 6 000)', '10 000'],
        ['Long-term liabilities (building loan 20 000, tractor loan 40 000)', '60 000'], ['Total liabilities', '70 000'], ['Net worth = 91 000 − 70 000', '21 000']], layout='grid'),
    RM('bs-err', 'Textbook check: Table 4.7 net worth', 243,
       'Table 4.7 gives net worth as **31 000** Nakfa, but assets 91 000 − liabilities 70 000 = **21 000** Nakfa. (Its current assets also list "unused fertilizer" twice, 4 000 and 5 000; they are counted in the 21 000 total.)'),
    WK('wk-bs', 'Activity 4.4: build a balance sheet', 243,
       'Cash 4 500; bank 3 000; wheat unsold 2 450; stored feed 1 500; building (last year\'s book value 55 000, depreciation 12 000); tractor (25 000, depreciation 7 000); accrued expenses 1 400; borrowed fuel 2 700; owed to the co-operative 4 000; building loan 10 000; tractor loan 20 000. Find net worth.',
       ['Current assets = 4 500 + 3 000 + 2 450 + 1 500 = 11 450.', 'Fixed assets = (55 000 − 12 000) + (25 000 − 7 000) = 43 000 + 18 000 = 61 000.', 'Total assets = 72 450.',
        'Current liabilities = 1 400 + 2 700 + 4 000 = 8 100; long-term = 30 000; total = 38 100.', 'Net worth = 72 450 − 38 100 = 34 350 Nakfa.'],
       'Net worth 34 350 Nakfa: the farm is solvent.'),
    WK('wk-is', 'An income statement', 244,
       'In January Alem Farm sold crops for 2 000 Nakfa and paid rent 500, salaries 200 and fertiliser 200. It also borrowed 1 000 from the bank and bought a 3 000 Nakfa pump (life 10 years, no salvage). Find the net income for January.',
       ['Revenue = crop sales = 2 000 (the loan is not revenue).', 'Expenses = 500 + 200 + 200 = 900, plus one month of pump depreciation = 3 000 ÷ 10 ÷ 12 = 25.', 'Net income = 2 000 − 925 = 1 075 Nakfa.'],
       '1 075 Nakfa (the textbook\'s 1 100 leaves out the pump). The 3 000 pump purchase appears in the cash flow, not as an expense.'),
    RM('u4-err2', 'Textbook checks in 4.2', 244,
       '- Under "Expenses" the text says "the **revenue** is equal to the value of goods and services used up"; it means the **expense**.',
       '- In cash flow, expenditure is recorded in the month of **payment** (the text says "receipt").',
       '- Long-term liabilities are given as debts of "more than five years". Usually any debt due after **more than one year** is non-current (1–5 years is sometimes called intermediate).'),
]

L3 = [
    T('=agri12-u4-c13', '4.3.1 Planning and budgeting', 247,
      'Farming is complex, so it must be **planned**. Three parts:',
      '- **List resources and needs**: **land** (ownership: village, government or private; fertility; cultivable area; distance to market), **labour** in **person-days** (1 person-day = an average person working **8 hours**), **capital** (available vs required; the gap may be borrowed), **management** (experience, training, interest).',
      '- **Land-use plan**: which land is for crops, vegetables, livestock, woodlot.',
      '- **Budget**: a written plan in **physical and money terms**, based on forecasts, past records and experience. It is a **management aid**, not a rigid rule; update it when prices or rain change.',
      '**Partial budget**: for a **small change** (a new variety on 1 ha); includes **only the costs and returns that change**. Adopt the change if the extra income is greater than the extra cost.',
      '**Complete budget**: for the **whole farm** or a whole enterprise; useful when starting a farm or comparing enterprises.'),
    DG('budget-fig', 'Partial budget', 249, 'budget'),
    TB('complete', 'Complete budget per hectare (Table 4.10)', 250, ['Item', 'Maize', 'Potato'],
       [['Yield (kg)', '800', '1 000'], ['Price (Nakfa/kg)', '1.50', '1.00'], ['Revenue', '1 200', '1 000'],
        ['Seed + fertiliser + labour + tools', '300 + 200 + 100 + 100 = 700', '200 + 100 + 100 + 50 = 450'], ['Net return', '500', '550']],
       'Potato gives the higher net return per hectare, even though maize earns more revenue.', layout='compare'),
    WK('wk-partial', 'A full partial budget', 249,
       'A farmer puts 1 ha of his barley land under a new wheat variety: extra costs 2 400, wheat revenue 6 000 Nakfa (Table 4.9). The hectare used to give barley worth 2 500 Nakfa with costs of 900 Nakfa. Is the change worthwhile?',
       ['Gains: new revenue 6 000 + barley costs saved 900 = 6 900.', 'Losses: new costs 2 400 + barley revenue given up 2 500 = 4 900.', 'Net change = 6 900 − 4 900 = +2 000 Nakfa.'],
       'Yes: profit rises by 2 000 Nakfa. Table 4.9 shows +3 600 because it leaves out the barley given up; a real partial budget counts both what is gained and what is lost.'),
    T('=agri12-u4-c14', '4.3.2 Decision-making', 250,
      'The purpose of planning and budgeting is **better decisions**. A decision based on a written plan beats a guess. In Table 4.9 the extra revenue (6 000) exceeds the extra cost (2 400) by **3 600 Nakfa**, so the change is accepted.'),
    T('=agri12-u4-c15', '4.3.3 Implementation', 251,
      'Carry out the plan: get the seed and fertiliser in time, organise labour (family, hired, wenfera), follow the calendar of operations.'),
    T('=agri12-u4-c16', '4.3.4 Monitoring', 251,
      'Watch the work as it happens and **keep records** (dates, inputs, costs, yields) so the results can be compared with the plan.'),
    T('=agri12-u4-c17', '4.3.5 Evaluation and appraisal', 251,
      'At the end of the season **compare planned and actual profit**, find the reasons for any gap (rain, prices, pests, management) and use the lessons in next year\'s plan.'),
    DG('cycle-fig', 'The management cycle', 247, 'cycle'),
    WK('wk-labour', 'Person-days for weeding', 248,
       'Weeding 1 ha of sorghum takes 25 person-days. A family has 3 adults working 6 days a week and must weed 2 ha within 3 weeks. Is hired labour needed?',
       ['Needed = 2 × 25 = 50 person-days.', 'Available = 3 people × 6 days × 3 weeks = 54 person-days.', '54 ≥ 50.'],
       'No: the family can just manage (4 person-days to spare), but a sick day would make it tight.'),
]

L4 = [
    T('=agri12-u4-c18', '4.4.1 Community-based organisations', 251,
      'Farmers have always pooled work at **sowing, weeding, harvest and threshing**: in Eritrea neighbours help each other in turn (**wenfera**). **Community-based organisations (CBOs)** are membership groups of people, usually living near each other, who join for **common interests**: women\'s groups, savings and credit groups, youth clubs, farmer co-operatives.',
      '**At village level** CBOs pool resources for shared goals: building **roads, schools, clinics and dams**, **soil and water conservation** (terraces, enclosures), clean water projects. They make development **owned, open and accountable** to the community.'),
    T('=agri12-u4-c19', '4.4.2 Co-operatives', 252,
      'A **co-operative** = an **autonomous association** of people who unite **voluntarily** to meet common economic, social and cultural needs through a **jointly owned, democratically controlled** enterprise. It is owned and run by and for its members; it is **not a charity** and **not state-directed**.',
      '**Values:** self-help, self-responsibility, democracy, equality, solidarity; members value honesty, openness, social responsibility and caring for others.',
      '**Benefits:** jobs and steady income, local investment, informed local leaders, less migration, bargaining power, cheaper inputs.',
      '**Types:**',
      '- **Producer**: owned by producers (vegetable growers).',
      '- **Consumer**: shops selling to members at fair prices.',
      '- **Marketing**: members sell together for better prices (onion or banana producers\' associations).',
      '- **Credit unions (savings and credit)**: members save monthly and borrow at low interest in proportion to their savings.',
      '- **Service**: bulk purchase of feed, fertiliser, seed and chemicals, sold to members at fair prices.'),
    DG('coop-fig', 'Seven principles', 253, 'coop'),
    RM('coop-err', 'Note on surplus sharing', 253,
       'The textbook says members share the surplus "based on the size of the investment". In the international co-operative principles, capital gets only **limited** interest; the surplus is shared mainly **in proportion to each member\'s business with the co-operative** (how much milk or produce they sold through it, or bought from it). That is what makes a co-operative different from a company.'),
    TB('coop-vs', 'Co-operative vs private company', 252, ['', 'Co-operative', 'Private company'],
       [['Owners', 'Members who use its services', 'Investors (shareholders)'], ['Voting', 'One member, one vote', 'One share, one vote'],
        ['Main aim', 'Serve members', 'Profit for owners'], ['Surplus', 'Mainly by use (patronage)', 'By shares held']], layout='compare'),
    WK('wk-coop', 'Sharing a dairy co-operative surplus', 253,
       'A dairy co-operative near Asmara has a surplus of 60 000 Nakfa to share by milk delivered. Members delivered 30 000 L in total. Selam delivered 4 500 L. What is her share?',
       ['Surplus per litre = 60 000 ÷ 30 000 = 2 Nakfa.', 'Selam = 4 500 × 2 = 9 000 Nakfa (or 4 500 ÷ 30 000 = 15 % of 60 000).'],
       '9 000 Nakfa.'),
]

LESSONS = {'agri12-u4-l4-1': L1, 'agri12-u4-l4-2': L2, 'agri12-u4-l4-3': L3, 'agri12-u4-l4-4': L4}

DROP = ['agri12-u4-c04']
PATCH = {}

# ------------------------------------------------------------------ practice
a = QSet('4.1 Practice — farm management and production economics', 's41')
a.M(210, 'Which is NOT a function of a farm manager?', ['Buying and combining inputs', 'Keeping records', 'Bearing risk', 'Fixing the national price of fertiliser'], 'D',
    ['Step 1: Managers decide inside their farm.', 'Step 2: National prices are set by markets/government.'], 'Inside the farm gate.', [('What is the main aim of a subsistence farm?', 'Self-sufficiency (feeding the family).')])
a.M(214, 'Which is working capital?', ['Tractor', 'Store building', 'Fertiliser', 'Milking machine'], 'C',
    ['Step 1: Working capital is used up within a season.', 'Step 2: Fertiliser is used up; the others last years.'], 'Used up = working.', [('What is human capital?', 'The skills and education of workers.')])
a.M(214, 'Labour from neighbours who help each other in turn at harvest is', ['hired labour', 'contract labour', 'collective labour', 'capital'], 'C',
    ['Step 1: Shared, reciprocal work = collective (wenfera).'], 'Together = collective.', [('Name the reward for land.', 'Rent.')])
a.S(213, 'State the three characteristics of resources.', 'They have economic value (must be paid for), their supply is limited, and they have alternative uses.',
    ['Step 1: Value.', 'Step 2: Scarcity.', 'Step 3: Alternatives → opportunity cost.'], 'V-L-A.', [('Define opportunity cost.', 'The value of the best alternative given up.')])
a.M(215, 'The relationship between inputs and output is the', ['budget', 'production function', 'balance sheet', 'iso-revenue line'], 'B',
    ['Step 1: y = f(x) links input to output.'], 'Function = depends on.', [('Name three ways to show it.', 'Table, graph, equation.')])
a.S(218, 'TP rises from 20 to 28 kg when fertiliser rises from 2 to 3 kg. Find the MP and the AP at 3 kg.', 'MP = 8 kg per kg of fertiliser; AP = 28 ÷ 3 ≈ 9.3 kg.',
    ['Step 1: MP = (28 − 20) ÷ (3 − 2) = 8.', 'Step 2: AP = 28 ÷ 3 ≈ 9.3.'], 'MP = change; AP = total ÷ input.', [('Is it diminishing returns when MP falls from 8 to 4?', 'Yes.')])
a.M(220, 'A rational farmer produces in', ['Stage I', 'Stage II', 'Stage III', 'any stage'], 'B',
    ['Step 1: Stage I under-uses the input.', 'Step 2: Stage III lowers output.', 'Step 3: Stage II (MP between AP and 0) is rational.'], 'Two is true.', [('In which stage is MP negative?', 'Stage III.')])
a.TF(220, 'In Stage III the farmer should add more input if it is free.', False,
     ['Step 1: In Stage III each extra unit reduces TP.', 'Step 2: Even free input loses output.'], 'Negative MP = stop.', [('Where does Stage II end?', 'Where MP = 0 (TP at its maximum).')])
a.S(221, 'Maize sells at 5 Nakfa/kg; fertiliser costs 15 Nakfa/kg. The 5th kg of fertiliser adds 3 kg of maize. Should it be applied?', 'Yes, just: MVP = 3 × 5 = 15 Nakfa = price of fertiliser, so this is the optimum (the 6th kg, MVP 5, would not pay).',
    ['Step 1: MVP = MP × Po.', 'Step 2: Compare with Pi.'], 'MVP = Pi is the target.', [('What if MVP > Pi?', 'Use more of the input.')])
a.M(222, 'Which is a fixed cost?', ['Fuel', 'Seed', 'Insurance of machinery', 'Casual labour for weeding'], 'C',
    ['Step 1: Insurance is paid whatever the output.'], 'Paid even at zero output = fixed.', [('Classify fertiliser expense.', 'Variable.')])
a.S(222, 'A farm has FC 8 000 and VC 12 000 Nakfa and produces 4 000 kg. Find TC, AFC, AVC and TAC.', 'TC = 20 000; AFC = 2 Nakfa/kg; AVC = 3 Nakfa/kg; TAC = 5 Nakfa/kg.',
    ['Step 1: TC = FC + VC.', 'Step 2: Divide each by 4 000.'], 'Per unit = ÷ Q.', [('What happens to AFC as output grows?', 'It keeps falling.')])
a.TF(225, 'Profit rises when MR is less than MC.', False,
     ['Step 1: If an extra unit costs more (MC) than it brings (MR), profit falls.', 'Step 2: Expand only while MC < MR.'], 'MR > MC → grow; MR < MC → shrink.', [('At what point is profit greatest?', 'MR = MC.')])
a.M(225, 'Input combinations that give the same output are shown by', ['an iso-quant', 'an iso-revenue line', 'a PPC', 'a TC curve'], 'A',
    ['Step 1: Iso = equal, quant = quantity.'], 'Same quantity.', [('What is the least-cost rule?', 'MP₁/P₁ = MP₂/P₂.')])
a.S(226, 'MP of labour is 60 and wage 50; MP of capital is 120 and rent 200. Should the farmer use more labour or more capital?', 'More labour: 60/50 = 1.2 per Nakfa for labour vs 120/200 = 0.6 for capital, so a Nakfa spent on labour gives more output.',
    ['Step 1: Compare MP per Nakfa.', 'Step 2: Shift spending to the higher one until equal.'], 'Output per Nakfa.', [('In Table 4.4, at which combination are they equal?', 'Combination 5 (both 1.6).')])
a.M(227, 'Wheat grain and straw are', ['competitive', 'joint', 'supplementary', 'antagonistic'], 'B',
    ['Step 1: You cannot grow grain without straw.'], 'Joint = together.', [('Beans before maize are…', 'Complementary.')])
a.M(228, 'Points outside the production possibility curve are', ['efficient', 'attainable', 'unattainable with present resources', 'the optimum'], 'C',
    ['Step 1: The PPC is the limit of what resources allow.'], 'Outside = out of reach.', [('Which line is tangent to the PPC at the optimum?', 'The iso-revenue line.')])
a.S(230, 'With wheat at 42 and maize at 24 Nakfa/kg, find the revenue from 1 000 kg wheat + 440 kg maize.', '52 560 Nakfa.',
    ['Step 1: 1 000 × 42 = 42 000.', 'Step 2: 440 × 24 = 10 560.', 'Step 3: Total 52 560.'], 'TR = ΣQ × P.', [('And from 1 200 kg wheat only?', '50 400 Nakfa.')])

b = QSet('4.2 Practice — records and financial statements', 's42')
b.M(238, 'All transactions of a farm in date order are kept in the', ['inventory', 'journal', 'balance sheet', 'wage book'], 'B',
    ['Step 1: The journal is the chronological record.'], 'Journal = diary of money.', [('What is an inventory?', 'A list of all physical assets and their values.')])
b.S(235, 'A tractor costs 400 000 Nakfa, lasts 10 years and is worth 40 000 at the end. Find the annual depreciation and the book value after 3 years.', '36 000 a year; book value 292 000 Nakfa.',
    ['Step 1: (400 000 − 40 000) ÷ 10 = 36 000.', 'Step 2: 400 000 − 3 × 36 000 = 292 000.'], '(CP − SV) ÷ life.', [('Is depreciation a cash cost?', 'No, it is a non-cash cost.')])
b.M(240, 'A statement of the financial position of a farm on a specific date is the', ['income statement', 'cash-flow statement', 'balance sheet', 'journal'], 'C',
    ['Step 1: Balance sheet = snapshot on one date.'], 'Snapshot = balance sheet.', [('Which statement covers a period?', 'The income statement (and the cash flow).')])
b.S(240, 'A farm has assets of 150 000 and liabilities of 90 000 Nakfa. What is its net worth? What if liabilities were 170 000?', '60 000 Nakfa; with 170 000 liabilities, −20 000: the farm would be insolvent.',
    ['Step 1: Net worth = assets − liabilities.'], 'A = L + NW.', [('Write the accounting equation.', 'Assets = liabilities + capital (net worth).')])
b.M(241, 'Which is a current asset?', ['Land', 'Orchard', 'Unsold eggs', 'Tractor'], 'C',
    ['Step 1: Current = turned into cash within a year.'], 'Liquid = current.', [('Is breeding stock current or fixed?', 'Fixed (non-current).')])
b.TF(244, 'A loan received from the bank is revenue in the income statement.', False,
     ['Step 1: Revenue must increase capital.', 'Step 2: A loan is matched by a liability.'], 'Borrowed ≠ earned.', [('Where does the loan appear?', 'In the cash flow (cash in) and as a liability on the balance sheet.')])
b.M(246, 'Which is NOT recorded in a cash-flow statement?', ['Fertiliser bought for cash', 'Sale of a cow', 'Depreciation of the pump', 'Loan repayment'], 'C',
    ['Step 1: Cash flow shows only actual cash.', 'Step 2: Depreciation moves no cash.'], 'No cash, no entry.', [('Give the three parts of a cash-flow statement.', 'Income, expenditure, bank balance.')])
b.S(234, 'State the requirements of an effective record-keeping system.', 'It must be useful; the manager must know how to collect information correctly; it must fit the user\'s needs; it must be simple and easy to use.',
    ['Step 1: Useful.', 'Step 2: Correct.', 'Step 3: Fitted.', 'Step 4: Simple.'], 'U-C-F-S.', [('How do records help get credit?', 'They show the lender the farm\'s income, assets and ability to repay.')])
b.S(244, 'Sales 5 000; rent 800; wages 1 200; feed 1 500 Nakfa. Find the net income.', '1 500 Nakfa.',
    ['Step 1: Expenses = 800 + 1 200 + 1 500 = 3 500.', 'Step 2: 5 000 − 3 500 = 1 500.'], 'Revenue − expenses.', [('What if expenses were 5 600?', 'Net loss of 600 Nakfa.')])

c = QSet('4.3–4.4 Practice — planning and co-operatives', 's43')
c.M(249, 'A budget used for a small change in a farm plan is a', ['complete budget', 'partial budget', 'cash-flow budget', 'balance sheet'], 'B',
    ['Step 1: Partial = only the part that changes.'], 'Small change → partial.', [('When is a complete budget used?', 'When planning the whole farm or starting a new farm.')])
c.S(250, 'Using Table 4.10, which crop gives the higher net return per hectare and by how much?', 'Potato: 550 vs 500 Nakfa, by 50 Nakfa per ha.',
    ['Step 1: Maize 1 200 − 700 = 500.', 'Step 2: Potato 1 000 − 450 = 550.'], 'Net = revenue − costs.', [('Which has the higher revenue?', 'Maize (1 200 vs 1 000).')])
c.S(248, 'How many hours make one person-day?', '8 hours of work by an average person.',
    ['Step 1: Textbook definition.'], 'Day = 8 h.', [('How many person-days do 4 people working 5 days give?', '20.')])
c.M(251, 'Comparing planned and actual profit at the end of the season is', ['implementation', 'monitoring', 'evaluation', 'budgeting'], 'C',
    ['Step 1: Monitoring is during; evaluation is after.'], 'Evaluate = end.', [('Why are records needed for monitoring?', 'To compare actual results with the plan.')])
c.M(253, 'In a co-operative, each member has', ['votes in proportion to shares', 'one vote', 'no vote', 'votes set by government'], 'B',
    ['Step 1: Democratic member control: one member, one vote.'], 'Member, not money.', [('Name two other co-operative principles.', 'Voluntary open membership; autonomy; education; co-operation among co-operatives; concern for community.')])
c.M(254, 'Farmers who join to sell their onions together for better prices form a', ['consumer co-operative', 'marketing co-operative', 'credit union', 'company'], 'B',
    ['Step 1: Selling together = marketing.'], 'Sell together = marketing.', [('What does a credit union do?', 'Members save regularly and borrow at low interest.')])
c.TF(253, 'A true co-operative is run by the government for the members.', False,
     ['Step 1: Co-operatives are autonomous and member-controlled.', 'Step 2: They are not state-directed or charities.'], 'Owned and run by members.', [('List two co-operative values.', 'Self-help, democracy, equality, solidarity.')])
c.S(255, 'Give three activities that village CBOs in Eritrea carry out.', 'Building roads, schools, clinics and dams; soil and water conservation such as terraces and enclosures; clean water projects (any three).',
    ['Step 1: Infrastructure.', 'Step 2: Conservation.', 'Step 3: Water.'], 'Build, conserve, supply.', [('What is a CBO?', 'A membership organisation of people, usually neighbours, joined for common interests.')])

QS = a.items + b.items + c.items

GLOSSARY = [
    ('Farm management', 'Planning, organising, co-ordinating and controlling a farm\'s resources to reach its goals.', 210),
    ('Opportunity cost', 'Value of the best alternative given up.', 213),
    ('Fixed capital', 'Capital used over many years (tractor, building).', 214),
    ('Working capital', 'Capital used up in one season (seed, fertiliser, cash).', 214),
    ('Production function', 'Relationship between inputs and output, y = f(x).', 215),
    ('Marginal product', 'Extra output from one more unit of input (ΔTP ÷ Δx).', 218),
    ('Diminishing returns', 'Falling extra output as more of one input is added to fixed others.', 219),
    ('Marginal value product', 'MP × price of output.', 221),
    ('Fixed cost', 'Cost that does not change with output.', 222),
    ('Variable cost', 'Cost that rises and falls with output.', 222),
    ('Iso-quant', 'Curve of input combinations giving the same output.', 225),
    ('Production possibility curve', 'All combinations of two products possible with fixed resources.', 228),
    ('Depreciation', 'Yearly loss of value of an asset: (cost − salvage) ÷ life.', 235),
    ('Journal', 'Book of all transactions in date order.', 238),
    ('Balance sheet', 'Statement of assets, liabilities and net worth on one date.', 240),
    ('Net worth', 'Assets minus liabilities.', 240),
    ('Income statement', 'Revenue, expenses and net income for a period.', 244),
    ('Cash flow', 'Actual cash in and out, month by month.', 245),
    ('Partial budget', 'Budget of only the costs and returns that change.', 249),
    ('Person-day', 'Work of an average person for 8 hours.', 248),
    ('Co-operative', 'Voluntary, democratically controlled association owned by its members.', 252),
]
TIPS = [('AP = TP ÷ x; MP = ΔTP ÷ Δx.', 218), ('Optimum input: MVP = price of input.', 221), ('Profit is greatest where MR = MC.', 225),
        ('Assets = liabilities + net worth.', 240)]
IDEAS = [('k_stages', 'Three stages of production', 'l4_1', 'agri12-u4-ad-stages-fig'),
         ('k_mvp', 'MVP = price', 'l4_1', 'agri12-u4-ad-wk-mvp'),
         ('k_depreciation', 'Depreciation', 'l4_2', 'agri12-u4-ad-wk-deprec'),
         ('k_balance', 'Balance sheet', 'l4_2', 'agri12-u4-ad-wk-bs'),
         ('k_budget', 'Partial and complete budgets', 'l4_3', 'agri12-u4-ad-wk-partial'),
         ('k_coop', 'Co-operative principles', 'l4_4', 'agri12-u4-ad-coop-fig')]

"""Presentation fields for the bookkeeping table cards (read by the app's notes table renderer, lib/high/notes/jr/notes/ntable.dart).

Adds to a `table` card, without touching its figures:
  kind   journal | ledger | statement | t_account
  cols   one type per column: text | money | dr | cr | date | ref
  marks  one per row: head (section heading / T-account name), total (rule above the figures), final (rule above, double
         rule below), note (journal narration)
T-account tables ("Account | Debit side | Credit side [| Balance]") are re-laid out as real T-accounts: per account a `head`
row, then lines [Dr date, Dr particulars, Dr Nfa, Cr date, Cr particulars, Cr Nfa] with Balance c/d, the equal totals and
Balance b/d. Two-sided (account form) balance sheets are re-laid out in report form so they fit a phone.
Old app versions ignore the extra fields and still show head/rows as a plain table.
"""
import re
from fractions import Fraction

NUM = re.compile(r'^\s*(Nakfa\.?\s*)?[+\-−]?\s*\(?\s*(\d{1,3}(?:,\d{3})+|\d+)(\.\d+)?\s*\)?\s*$')
MONTH = r'(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|June?|July?|Aug(?:ust)?|Sept?(?:ember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\.?'
TOTAL = re.compile(r'^(totals?\b|total |net (income|loss|profit|sales|purchases)\b|gross profit\b|cost of goods (sold|purchased|available)\b|'
                   r'increase in capital\b|total assets\b|total liabilities\b)', re.I)


def is_num(s):
    return bool(NUM.match((s or '').replace('**', ''))) or (s or '').strip() in ('-0-', '—', '–')


def val(s):
    m = NUM.match((s or '').replace('**', ''))
    if not m:
        return None
    v = Fraction(m.group(2).replace(',', '') + (m.group(3) or ''))
    return -v if re.match(r'\s*[\-−(]', s) else v


def fmt(v, cents):
    v = abs(v)
    s = f'{int(v):,}'
    if cents:
        s += f'.{int(round((v - int(v)) * 100)):02d}'
    return s


def col_types(head, rows, kind):
    out = []
    for j, h in enumerate(head):
        hl = h.lower().strip()
        cells = [r[j].strip() for r in rows if j < len(r) and r[j].strip() not in ('', '?')]
        nums = [c for c in cells if is_num(c)]
        if re.search(r'(^|— )date\b|^date', hl):
            out.append('date')
        elif re.fullmatch(r'(p\s*/\s*r\.?|p\.?\s*r\.?|post\.? ?ref\.?|ref\.?|no\.?|cheq no\.?|invoice no\.?|lf|l\.f\.)', hl) or hl.endswith('post. ref.') or (j == 0 and hl == '' and cells and all(re.fullmatch(r'\d{1,2}', c) for c in cells)):
            out.append('ref')
        elif re.search(r'\bdebit\b|\bdr\.?(\s|$)|\(dr\.?\)', hl) and not re.search(r'\bcredit\b|\bcr\.?(\s|$)', hl):
            out.append('dr')
        elif re.search(r'\bcredit\b|\bcr\.?(\s|$)|\(cr\.?\)', hl) and not re.search(r'\bdebit\b|\bdr\.?(\s|$)', hl):
            out.append('cr')
        elif cells and len(nums) >= .6 * len(cells):
            out.append('money')
        elif re.search(r'\b(nakfa|nfa|amount|balance|book value)\b', hl) and nums:
            out.append('money')
        else:
            out.append('text')
    return out


def row_marks(head, rows, cols, kind, worksheet=False):
    marks = []
    figs = [j for j, t in enumerate(cols) if t in ('money', 'dr', 'cr')]
    last_col = figs[-1] if figs else None
    POST = re.compile(r'^\(\s*[\w√]{1,4}\s*\)$')  # posting references under the column totals: (11) (√)
    def refs_only(r):
        cells = [r[j].strip() for j in figs if r[j].strip()]
        return bool(cells) and all(POST.match(c) for c in cells)
    last_fig = max((i for i, r in enumerate(rows) if any(r[j].strip() for j in figs) and not refs_only(r)), default=-1)
    for i, r in enumerate(rows):
        label = ' '.join(r[j] for j, t in enumerate(cols) if t == 'text').strip()
        has = any(r[j].strip() for j in figs)
        ll = label.lower()
        m = ''
        if refs_only(r):
            m = 'note'
        elif has and label == '' and i == last_fig and kind == 'journal' and i > 0:
            m = 'final'  # a special journal's unlabeled column totals
        elif has and TOTAL.match(label):
            net = ll.startswith('net ')
            if net and (worksheet or (last_col is not None and not r[last_col].strip())):
                m = ''  # a net income in a middle column (capital statement) or the worksheet's net income line
            else:
                m = 'final' if i == last_fig else 'total'
        elif has and i == last_fig and kind == 'statement' and (label == '' or re.match(r'.*\bcapital,', ll)):
            m = 'final'
        elif has and label == '' and kind == 'statement' and i > 0:
            m = 'total'  # an unlabeled subtotal line
        elif not has and label.startswith('(') and label.endswith(')') and kind == 'journal':
            m = 'note'
        elif not has and label and kind == 'statement' and (label.endswith(':') or ll in HEADS):
            m = 'head'
        marks.append(m)
    return marks


HEADS = {'assets', 'liabilities', 'capital', 'revenues', 'revenue', 'expenses', 'operating expenses', 'operating expense', 'cost of goods sold',
         'liabilities and capital', 'current assets', 'fixed assets', 'owner’s equity'}


# ---------------------------------------------------------------- T-accounts
def t_items(cell):
    """'Jan. 1 Bal 18,000; Jan. 31 (Adj.) 16,500' -> [(date, particulars, amount)]"""
    out = []
    for piece in [x.strip() for x in (cell or '').split(';') if x.strip()]:
        if 'new balance' in piece.lower():
            continue
        m = re.search(r'(\d{1,3}(?:,\d{3})+|\d+)(\.\d\d)?\s*$', piece)
        if not m:
            continue
        rest = piece[:m.start()].strip()
        d = re.match(rf'^({MONTH}\s*\d{{1,2}})\b\s*', rest)
        date = d.group(1) if d else ''
        part = rest[d.end():].strip() if d else rest
        out.append((date, part or ('' if date else 'Balance'), m.group(0).strip()))
    return out


def t_account(card, practice=False):
    rows_in = card['rows']
    accts = []
    for r in rows_in:
        name = r[0]
        dr, cr = t_items(r[1]), t_items(r[2] if len(r) > 2 else '')
        bal_cell = r[3] if len(r) > 3 else ''
        accts.append((name, dr, cr, bal_cell))
    dated = any(x[0] for _, dr, cr, _ in accts for x in dr + cr)
    rows, marks = [], []

    def line(d, c):
        d = d or ('', '', '')
        c = c or ('', '', '')
        return list(d) + list(c) if dated else [d[1], d[2], c[1], c[2]]

    for name, dr, cr, bal_cell in accts:
        w = 6 if dated else 4
        rows.append([name] + [''] * (w - 1))
        marks.append('head')
        n = max(len(dr), len(cr))
        for i in range(n):
            rows.append(line(dr[i] if i < len(dr) else None, cr[i] if i < len(cr) else None))
            marks.append('')
        vals_d = [val(x[2]) for x in dr if val(x[2]) is not None]
        vals_c = [val(x[2]) for x in cr if val(x[2]) is not None]
        if len(dr) + len(cr) < 2:
            continue  # a single figure: it is the balance
        sd, sc = sum(vals_d, Fraction(0)), sum(vals_c, Fraction(0))
        cents = any('.' in x[2] for x in dr + cr)
        bd = re.match(rf'^\s*({MONTH}\s*\d{{1,2}})', bal_cell or '')
        bdate = bd.group(1) if bd else ''
        q = practice  # the practice card leaves the balance, totals and b/d for the student
        bal = sd - sc
        if bal != 0:
            amt = '?' if q else fmt(bal, cents)
            cd = (bdate, 'Balance c/d', amt)
            # c/d goes on the smaller side, in the first free line
            side_rows = len(rows) - n
            small = cr if bal > 0 else dr
            k = len(small)
            if k < n:
                r = rows[side_rows + n - 1]  # the last line of the shorter side, just above the totals
                if bal > 0:
                    r[-3 if dated else -2:] = list(cd) if dated else [cd[1], cd[2]]
                else:
                    r[:3 if dated else 2] = list(cd) if dated else [cd[1], cd[2]]
            else:
                rows.append(line(cd, None) if bal < 0 else line(None, cd))
                marks.append('')
        tot = '?' if q else fmt(max(sd, sc), cents)
        rows.append(line(('', '', tot), ('', '', tot)))
        marks.append('final')
        if bal != 0:
            bdl = ('', 'Balance b/d', '?' if q else fmt(bal, cents))
            rows.append(line(bdl, None) if bal > 0 else line(None, bdl))
            marks.append('')
    head = ['Date', 'Particulars', 'Nfa', 'Date', 'Particulars', 'Nfa'] if dated else ['Particulars', 'Nfa', 'Particulars', 'Nfa']
    card['head'], card['rows'], card['marks'] = head, rows, marks
    card['kind'] = 't_account'
    card['cols'] = ['date', 'text', 'money', 'date', 'text', 'money'] if dated else ['text', 'money', 'text', 'money']
    return card


# ---------------------------------------------------------------- balance sheet in report form
def account_form(head, rows):
    h = [x.lower() for x in head]
    return len(head) in (4, 5) and h[0].startswith('assets') and any(x.startswith('liabilities') for x in h[2:])


def report_form(card):
    head, rows = card['head'], card['rows']
    five = len(head) == 5  # Assets | detail | Nakfa | Liabilities and Capital | Nakfa
    left = [[r[0], r[1], r[2]] if five else [r[0], '', r[1]] for r in rows]
    right = [[r[3], '', r[4]] if five else [r[2], '', r[3]] for r in rows]
    rh = head[3] if five else head[2]
    out, marks = [['Assets', '', '']], ['head']
    for r in left:
        if any(r):
            out.append(r)
            marks.append('total' if TOTAL.match(r[0]) else '')
    out.append([rh, '', ''])
    marks.append('head')
    for r in right:
        if not any(r):
            continue
        lab = r[0]
        if lab in ('Liabilities', 'Capital') and not r[2]:
            out.append(r)
            marks.append('head')
            continue
        out.append(r)
        marks.append('total' if TOTAL.match(lab) else '')
    # the last total is the final one
    for i in range(len(marks) - 1, -1, -1):
        if marks[i] == 'total':
            marks[i] = 'final'
            break
    # total assets also gets the double rule
    for i, r in enumerate(out):
        if r[0].lower().startswith('total assets'):
            marks[i] = 'final'
    card['head'] = ['', 'Nakfa', 'Nakfa']
    card['rows'] = out
    card['marks'] = marks
    card['kind'] = 'statement'
    card['cols'] = ['text', 'money', 'money']
    card['body'] = ['Shown in **report form** (assets first, then liabilities and capital) so it fits a phone screen. In the textbook the same figures stand side by side: assets on the left, liabilities and capital on the right.']
    return card


KIND = {'journal': 'journal', 'special': 'journal', 'ledger': 'ledger', 'trial': 'statement', 'worksheet': 'statement', 'statement': 'statement',
        'crossfoot': 'statement', 'equation': 'statement', 'schedule': 'statement', 'missing': 'statement', 'chart': 'table', 'dc': 'statement'}


def decorate(card, kind, practice=False):
    """add kind / cols / marks to a bookkeeping table card (in place) and return it"""
    head, rows = card['head'], card['rows']
    if kind == 'taccount':
        if len(head) >= 3 and head[1].lower().startswith('debit'):
            return t_account(card, practice)
    if kind in ('statement',) and account_form(head, rows):
        return report_form(card)
    k = KIND.get(kind, 'table')
    if k == 'statement' and head and head[0].strip() and not any(h.strip() for h in head[1:]) and len(head) > 1:
        # "Revenues | | |": the first section heading was printed in the header line
        card['rows'] = rows = [[head[0]] + [''] * (len(head) - 1)] + rows
        card['head'] = head = [''] * len(head)
    if practice and head[-1].lower().startswith('debit or credit'):
        k = 'journal' if head[0].lower() == 'date' else 'statement'
    cols = col_types(head, rows, k)
    if k == 'table' and not any(c in ('money', 'dr', 'cr') for c in cols):
        return card
    card['kind'] = k
    card['cols'] = cols
    marks = row_marks(head, rows, cols, k, worksheet=kind == 'worksheet')
    if any(marks):
        card['marks'] = marks
    return card

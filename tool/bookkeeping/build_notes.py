#!/usr/bin/env python3
"""Put every bookkeeping table of Business & Economics G10 Unit 3 and G11 Unit 2 into the notes as native table cards.

For each table in tool/bookkeeping/tables.json it writes, into the lesson that covers the table's page:
  1. a `table` card with the figures exactly as printed,
  2. a `worked` card that explains, step by step, how every entry is posted / where every figure comes from,
  3. a practice `table` card (same layout, amounts doubled, the cells to work out shown as ?), and
  4. a `worked` card in `try` mode with the full answer, revealed one step at a time.
Idempotent: cards it made before (ids `<unit>-bk...`) are removed first.

  python3 tool/bookkeeping/build_notes.py && python3 tool/split_notes.py && python3 tool/build_tutor_index.py
"""
import json, os, re
from fractions import Fraction

ROOT = os.path.join(os.path.dirname(__file__), '..', '..')
TABLES = os.path.join(os.path.dirname(__file__), 'tables.json')
BOOKS = {'10': ('assets/high/notes/notes/business_economics_10.json', 'be10-u3'),
         '11': ('assets/high/notes/notes/business_economics_11.json', 'be11-u2')}
SRC = 'bookkeeping_tables'

# ---------------------------------------------------------------- numbers
NUM = re.compile(r'^\s*(Nakfa\.?\s*)?([+\-−]?)\s*\(?\s*(\d{1,3}(?:,\s?\d{3})+|\d+)(\.\d+)?\s*\)?\s*$')


def num(s):
    """'1,105,000.00' -> Fraction; '-0-', '—', '0.00' -> 0; otherwise None"""
    s = (s or '').strip().replace('_', '')
    if s in ('-0-', '—', '–', '-'):
        return Fraction(0)
    m = NUM.match(s)
    if not m:
        return None
    v = Fraction(m.group(3).replace(',', '').replace(' ', '') + (m.group(4) or ''))
    if m.group(2) in ('-', '−') or (s.strip().startswith('(') and s.strip().endswith(')')):
        v = -v
    return v


def money(v, cents=None):
    neg = v < 0
    v = abs(v)
    if cents is None:
        cents = v.denominator != 1
    s = f'{float(v):,.2f}' if cents else f'{int(v):,}'
    return ('-' if neg else '') + s


def has_cents(s):
    return bool(re.search(r'\.\d\d\s*\)?$', s or ''))


def dbl(s):
    """double every amount in a cell, keep its style; dates, refs, account numbers stay"""
    v = num(s)
    if v is None:
        s = re.sub(r'(?<![\d.,])(\d{1,3})\.(\d{3})(?![\d,])', r'\1,\2', s or '')
        return re.sub(r'(?<![\d.,/])(\d{1,3}(?:,\d{3})+|\d+(?=\.\d\d))(\.\d\d)?(?![\d,])', lambda m: money(2 * Fraction(m.group(1).replace(',', '') + (m.group(2) or '')), bool(m.group(2))), s or '')
    if not re.search(r'\d', s):
        return s
    if re.fullmatch(r'\d{1,2}', s.strip()):  # day / account number
        return s
    pre = 'Nakfa ' if s.strip().startswith('Nakfa') else ''
    sign = '+' if s.strip().startswith('+') else ''
    out = money(2 * v, has_cents(s))
    if s.strip().startswith('(') and v < 0:
        out = '(' + money(-2 * v, has_cents(s)) + ')'
    return pre + sign + out


# ---------------------------------------------------------------- accounts
def acct_type(name, ctx=''):
    n = name.lower()
    if 'income summary' in n or 'income and expense summary' in n:
        return 'summary'
    if 'accumulated' in n or 'accu.' in n or 'acc dep' in n:
        return 'contra_asset'
    if 'drawing' in n or 'withdrawal' in n:
        return 'drawing'
    if 'sales return' in n or 'sales discount' in n:
        return 'contra_revenue'
    if 'purchase return' in n or 'purchase discount' in n or 'purchases return' in n:
        return 'contra_purchases'
    if 'capital' in n:
        return 'capital'
    if 'payable' in n or 'loan' in n or 'bank' in n and 'cash' not in n and 'commercial' in n:
        return 'liability'
    if 'expense' in n or 'exp.' in n or n.endswith(' exp') or n.startswith('purchases') or n == 'purchases' or 'freight' in n:
        return 'expense'
    if any(w in n for w in ('earned', 'revenue', 'fees', 'commission', 'sales', 'income')):
        return 'revenue'
    if any(w in n for w in ('cash', 'suppl', 'auto', 'furniture', 'equipment', 'equip', 'receivable', 'inventory', 'inventor', 'prepaid',
                            'land', 'building', 'truck', 'library', 'machine', 'tools', 'house', 'clothes', 'books', 'bicycle', 'mobile', 'money')):
        return 'asset'
    if ctx == 'payable':
        return 'creditor'
    if ctx == 'receivable':
        return 'debtor'
    return 'other'


TYPE_TXT = {'asset': 'an asset', 'liability': 'a liability', 'capital': 'the owner’s capital', 'drawing': 'the owner’s drawing account',
            'revenue': 'a revenue account', 'expense': 'an expense account', 'contra_asset': 'a contra-asset (it reduces an asset)',
            'contra_revenue': 'a contra-revenue account (it reduces sales)', 'contra_purchases': 'a contra-purchases account (it reduces purchases)',
            'summary': 'the Income Summary (a temporary clearing account)', 'creditor': 'a creditor’s account in the accounts payable subsidiary ledger',
            'debtor': 'a customer’s account in the accounts receivable subsidiary ledger', 'other': 'an account'}
NORMAL = {'asset': 'Dr', 'expense': 'Dr', 'drawing': 'Dr', 'contra_revenue': 'Dr', 'debtor': 'Dr',
          'liability': 'Cr', 'capital': 'Cr', 'revenue': 'Cr', 'contra_asset': 'Cr', 'contra_purchases': 'Cr', 'creditor': 'Cr'}


def why_side(name, side, ctx=''):
    t = acct_type(name, ctx)
    nb = NORMAL.get(t)
    if t == 'summary':
        return ('Income Summary is debited here: it collects the expenses (and, in the inventory adjustment, the beginning inventory).' if side == 'Dr'
                else 'Income Summary is credited here: it collects the revenues (and, in the inventory adjustment, the ending inventory).')
    if not nb:
        return f'{name} is written on the {"debit" if side == "Dr" else "credit"} side.'
    up = side == nb
    return (f'{name} is {TYPE_TXT[t]} (normal balance: {"debit" if nb == "Dr" else "credit"}), so a '
            f'{"debit" if side == "Dr" else "credit"} {"increases" if up else "decreases"} it.')


REF = [(r'^CPJ(\d+)', 'the cash payments journal, page {}'), (r'^CRJ(\d+)', 'the cash receipts journal, page {}'),
       (r'^PJ(\d+)', 'the purchases journal, page {}'), (r'^SJ(\d+)', 'the sales journal, page {}'),
       (r'^GJ(\d+)', 'the general journal, page {}'), (r'^J(\d+)', 'the general journal, page {}'), (r'^C(\d+)', 'the cash journal, page {}')]


def ref_txt(r):
    r = (r or '').strip()
    for pat, txt in REF:
        m = re.match(pat, r)
        if m:
            return f'{r} = {txt.format(m.group(1))}'
    return f'reference {r}' if r else 'no posting reference written'


# ---------------------------------------------------------------- table kinds
def col(head, *words, avoid=()):
    for j, h in enumerate(head):
        hl = h.lower()
        if all(w in hl for w in words) and not any(a in hl for a in avoid):
            return j
    return None


def kind_of(t):
    if t.get('kind'):
        return t['kind']
    h = ' | '.join(t['head']).lower()
    if any(c == '?' or re.fullmatch(r'\([a-j]\)', c) for r in t['rows'] for c in r):
        return 'missing'
    if 'jan' in h and 'feb' in h:
        return 'schedule'
    if 'adjustments' in h or 'trial balance — debit' in h or 'income statement — debit' in h:
        return 'worksheet'
    if 'assets =' in h:
        return 'equation'
    if 'balance' in h and 'debit' in h and 'credit' in h:
        return 'ledger'
    if 'account number' in h or 'chart' in t['title'].lower():
        return 'chart'
    if ('cash debit' in h or 'cash (dr.)' in h or 'cash cr.' in h or 'purchases dr.' in h or 'sales cr.' in h or 'accounts receivable dr' in h
            or 'purchase dr' in h):
        return 'special'
    if 'debit' in h and 'credit' in h and ('date' in h or 'description' in h):
        return 'journal'
    if 'debit' in h and 'credit' in h:
        return 'trial'
    return 'statement'


def money_cols(t):
    return [j for j in range(len(t['head'])) if any(num(r[j]) is not None and re.search(r'\d{2}', r[j]) and not re.fullmatch(r'\d{1,2}', r[j].strip())
                                                    for r in t['rows'])]


# ---------------------------------------------------------------- explanations
def label(r, t):
    for j, c in enumerate(r):
        if c and num(c) is None and not re.fullmatch(r'[\d./ ]+|C/Y.*|Current.*|\(?[√✓]\)?', c):
            return c
    return ''


def explain_journal(t):
    h = t['head']
    jd = col(h, 'debit') if col(h, 'debit') is not None else len(h) - 2
    jc = col(h, 'credit') if col(h, 'credit') is not None else len(h) - 1
    ja = col(h, 'account') if col(h, 'account') is not None else (col(h, 'description') if col(h, 'description') is not None else 1)
    jp = col(h, 'p/') if col(h, 'p/') is not None else (col(h, 'ref') if col(h, 'ref') is not None else col(h, 'pr'))
    steps, entry, date, n = [], [], '', 0
    tot_d = tot_c = Fraction(0)

    def flush():
        nonlocal entry, n
        if not entry:
            return
        n += 1
        dr = [(a, v, p) for a, v, s, p in entry if s == 'Dr']
        cr = [(a, v, p) for a, v, s, p in entry if s == 'Cr']
        note = [a for a, v, s, p in entry if s == 'note']
        when = date if not re.fullmatch(r'\d{1,2}', date or '') else f'day {date} of the month'
        lines = []
        for a, v, p in dr:
            lines.append(f'Debit **{a}** {money(v, True)} (Debit column). {why_side(a, "Dr")}'
                         + (f' P/R {p} shows it has been posted to account {p}.' if p and p not in ('√', '-') else ''))
        for a, v, p in cr:
            lines.append(f'Credit **{a}** {money(v, True)} (indented, Credit column). {why_side(a, "Cr")}'
                         + (f' P/R {p} shows it has been posted to account {p}.' if p and p not in ('√', '-') else ''))
        sd, sc = sum(v for _, v, _ in dr), sum(v for _, v, _ in cr)
        tail = ''
        if dr and cr:
            tail = (f' Check: debits {money(sd, True)} = credits {money(sc, True)}.' if sd == sc else
                    f' Check: debits add to {money(sd, True)} but credits to {money(sc, True)}; they must be equal, so one printed amount is a slip.')
        if note:
            tail += ' Explanation line: ' + '; '.join(note) + ' (the source document).'
        head = f'**Entry {n}{" — " + when if when else ""}:** '
        if len(lines) <= 2:
            steps.append(head + ' '.join(lines) + tail)
        else:
            steps.append(head + lines[0])
            steps.extend(lines[1:-1])
            steps.append(lines[-1] + tail)
        entry = []
        return
        steps.append(' '.join(lines))
        entry = []

    for r in t['rows']:
        a = r[ja] if ja is not None else ''
        d, c = num(r[jd]) if jd is not None else None, num(r[jc]) if jc is not None else None
        p = r[jp] if jp is not None else ''
        dt = ' '.join(x for x in r[:ja] if x).strip() if ja else ''
        if d is not None and c is not None and not a:
            flush()
            steps.append(f'**Totals:** the Debit column adds to {r[jd]} and the Credit column to {r[jc]}. '
                         + ('Equal totals prove the journal is in balance.' if tot_d == tot_c else
                            f'Adding the entries gives {money(tot_d, True)} debits and {money(tot_c, True)} credits.'))
            continue
        if d is not None and d != 0:
            if entry and any(s == 'Cr' for _, _, s, _ in entry):
                flush()
            if dt:
                date = dt
            entry.append((a or 'the account', d, 'Dr', p)); tot_d += d
        elif c is not None and c != 0:
            entry.append((a or 'the account', c, 'Cr', p)); tot_c += c
        elif a:
            entry.append((a, None, 'note', p))
            if a.startswith('(') or 'Closing' in a or 'record' in a.lower():
                flush()
    flush()
    intro = ('A general journal entry is written in four parts: (1) the date, (2) the debit account at the left edge of the Account Title column with its amount '
             'in the Debit column, (3) the credit account, indented, with its amount in the Credit column, (4) a short explanation or the source document. '
             'The P/R (post reference) column stays empty until the line is posted to the ledger; then the account number is written there.')
    return [intro] + steps


def explain_ledger(t):
    h = t['head']
    jd, jc, jb = col(h, 'debit'), col(h, 'credit'), col(h, 'balance')
    jr = col(h, 'ref') if col(h, 'ref') is not None else (col(h, 'p/') if col(h, 'p/') is not None else col(h, 'pr'))
    title = re.sub(r'^(Account Title:\s*_*|General Ledger — |Accounts (Payable|Receivable) Subsidiary Ledger — )', '', t['title'])
    name = re.sub(r'[_]+', ' ', re.split(r'Account Number|—|\(', title)[0]).strip(' :')
    name = re.sub(r'\s+\d{1,3}$', '', name).strip()
    refs = ' '.join(r[jr] for r in t['rows'] if jr is not None)
    ctx = 'payable' if re.search(r'PJ|CPJ', refs) and 'Receivable' not in t['title'] else ('receivable' if re.search(r'SJ|CRJ', refs) else '')
    if 'Payable Subsidiary' in t['title']:
        ctx = 'payable'
    if 'Receivable Subsidiary' in t['title']:
        ctx = 'receivable'
    typ = acct_type(name, ctx)
    nb = NORMAL.get(typ, 'Dr')
    steps = [f'**{name}** is {TYPE_TXT.get(typ, "an account")}; its normal balance is a {"debit" if nb == "Dr" else "credit"}. '
             f'So in the Balance column a {"debit" if nb == "Dr" else "credit"} is added and a {"credit" if nb == "Dr" else "debit"} is subtracted.']
    bal = None
    for r in t['rows']:
        d = num(r[jd]) if jd is not None else None
        c = num(r[jc]) if jc is not None else None
        b = num(r[jb]) if jb is not None else None
        date = ' '.join(x for x in r[:2] if x and num(x) is None or (x and re.fullmatch(r'\d{1,2}', x))).strip() or 'Same date'
        item = r[1] if len(r) > 1 and r[1] and num(r[1]) is None else ''
        ref = r[jr] if jr is not None else ''
        src = ref_txt(ref)
        if d is None and c is None and b is not None:
            steps.append(f'**{date}**: {item or "Opening balance"} of {r[jb]} is brought in (no amount is posted, so the balance column simply shows it).')
            bal = b
            continue
        amt, side = (d, 'Dr') if d not in (None, Fraction(0)) else (c, 'Cr')
        if amt is None:
            continue
        line = f'**{date}**{" (" + item + ")" if item and item not in ("Bal", "Bal.", "Balance") else ""}: posted from {src}. '
        line += f'{"Debit" if side == "Dr" else "Credit"} column: {r[jd] if side == "Dr" else r[jc]}. '
        if bal is None:
            calc = amt
            line += f'It is the first amount in the account, so the balance is {money(calc, has_cents(r[jb] if jb is not None else ""))}.'
            if item in ('Balance', 'Bal', 'Bal.'):
                line += ' (The word “Balance” in the Item column shows it is the opening balance carried from the opening entry.)'
        else:
            calc = bal + amt if side == nb else bal - amt
            op = '+' if side == nb else '−'
            line += f'New balance = {money(bal, True)} {op} {money(amt, True)} = {money(calc, True)}.'
        if b is not None and b != calc:
            line += f' (The printed balance is {r[jb]}; the arithmetic gives {money(calc, True)}, so the printed figure is a slip — use {money(calc, True)}.)'
            bal = calc
        else:
            bal = calc
        if calc == 0:
            line += ' The account is now closed (zero balance), shown as -0- or a dash.'
        steps.append(line)
    if bal is not None:
        steps.append(f'**Final balance:** {money(bal, True)} on the {"debit" if (bal >= 0) == (nb == "Dr") else "credit"} side. '
                     'This is the figure that goes to the trial balance.')
    return steps


def explain_trial(t):
    h = t['head']
    jd, jc = col(h, 'debit'), col(h, 'credit')
    ja = 0
    steps = ['A trial balance lists every ledger account with its balance: debit balances in the Debit column, credit balances in the Credit column. '
             'If the two totals agree, the debits and credits in the ledger are equal.']
    sd = sc = Fraction(0)
    wrong = []
    for r in t['rows']:
        a = r[ja]
        d, c = num(r[jd]) if jd is not None else None, num(r[jc]) if jc is not None else None
        if not a or a.lower().startswith('total'):
            if d is not None or c is not None:
                steps.append(f'**Totals row:** printed Debit {r[jd] or "—"}, Credit {r[jc] or "—"}. Adding the column gives Debit {money(sd, True)} and Credit {money(sc, True)}.'
                             + (' They agree, so the trial balance is in balance.' if sd == sc else ' They do not agree, so the trial balance is not in balance.'))
            continue
        side = 'Dr' if d not in (None, Fraction(0)) else ('Cr' if c not in (None, Fraction(0)) else None)
        if side is None:
            steps.append(f'{a}: no balance (shown blank or as a dash), so nothing is added.')
            continue
        v = d if side == 'Dr' else c
        sd += v if side == 'Dr' else 0
        sc += v if side == 'Cr' else 0
        t_ = acct_type(a)
        nb = NORMAL.get(t_)
        msg = f'{a}: {money(v, True)} in the {"Debit" if side == "Dr" else "Credit"} column. {why_side(a, side).split(". ")[0]}.'
        if nb and nb != side:
            msg += f' Careful: its normal balance is a {"debit" if nb == "Dr" else "credit"}, so it belongs in the {"Debit" if nb == "Dr" else "Credit"} column.'
            wrong.append((a, v, nb))
        steps.append(msg)
    if wrong:
        cd = sd - sum(v for a, v, nb in wrong if nb == 'Cr') + sum(v for a, v, nb in wrong if nb == 'Dr')
        cc = sc - sum(v for a, v, nb in wrong if nb == 'Dr') + sum(v for a, v, nb in wrong if nb == 'Cr')
        steps.append(f'**Correcting the sides:** move {", ".join(a for a, _, _ in wrong)} to their normal-balance columns. '
                     f'The corrected totals are Debit {money(cd, True)} and Credit {money(cc, True)}' + (' — now equal.' if cd == cc else '.'))
    return steps


def explain_worksheet(t):
    h = t['head']
    ja = col(h, 'account') if col(h, 'account') is not None else 0
    steps = ['The worksheet has pairs of Debit/Credit columns: ' + ', '.join(dict.fromkeys(x.split(' — ')[0] for x in h if '—' in x)) +
             '. Each account’s balance starts in the trial balance columns, is changed by any adjustment, and is then extended to the Income Statement '
             'columns (revenues and expenses) or the Balance Sheet columns (assets, liabilities, capital, drawing).']
    for r in t['rows']:
        a = r[ja]
        parts = [f'{h[j].replace(" — ", " ")} {r[j]}' for j in range(len(h)) if j != ja and r[j] and num(r[j].split(') ')[-1]) is not None and h[j]]
        if not parts:
            continue
        typ = acct_type(a) if a else ''
        where = {'asset': 'Balance Sheet Debit', 'drawing': 'Balance Sheet Debit', 'liability': 'Balance Sheet Credit', 'capital': 'Balance Sheet Credit',
                 'contra_asset': 'Balance Sheet Credit', 'revenue': 'Income Statement Credit', 'contra_purchases': 'Income Statement Credit',
                 'expense': 'Income Statement Debit', 'contra_revenue': 'Income Statement Debit'}.get(typ)
        line = f'**{a or "Column totals"}**: ' + '; '.join(parts) + '.'
        adj = [r[j] for j in range(len(h)) if 'adjust' in h[j].lower() and 'trial' not in h[j].lower() and r[j]]
        if adj:
            line += f' Adjustment {", ".join(adj)}: the letter links the debit and the credit of the same adjusting entry.'
        if where and not a.lower().startswith(("net income", "net loss", "income summary")):
            line += f' {a} is {TYPE_TXT[typ]}, so its (adjusted) balance is extended to the {where} column.'
        if a.lower().startswith('net income'):
            line += ' Net income is the difference between the two Income Statement columns; it is added to the smaller Income Statement column and to the Balance Sheet Credit column (it increases capital), so each pair of columns balances.'
        if a.lower().startswith('total') or not a:
            line += ' Each pair of columns must have equal totals (after net income is added).'
        steps.append(line)
    return steps


def explain_equation(t):
    h = t['head']
    names = [x.split(' — ')[-1] for x in h]
    steps = ['Every transaction changes at least two columns, and after each one the equation Assets = Liabilities + Capital must still hold.']
    prev = None
    for r in t['rows']:
        lab = r[0]
        vals = r[1:]
        if lab.lower().startswith('ba'):
            nums = [num(v) or Fraction(0) for v in vals]
            na = sum(nums[:5]) if len(nums) >= 8 else None
            line = '**Balance line:** ' + ', '.join(f'{n} {v}' for n, v in zip(names[1:], vals) if v) + '.'
            if na is not None:
                nl = sum(nums[5:])
                line += f' Check: assets {money(na)} and liabilities + capital {money(nl)}' + (' — equal.' if na == nl else ' (the printed row leaves a cell blank or slips; the columns should still add up).')
            steps.append(line)
            prev = nums
        else:
            ch = [f'{n} {v}' for n, v in zip(names[1:], vals) if v]
            steps.append(f'**Transaction {lab}** ' + ', '.join(ch) + '. A “+” increases the column and a “−” decreases it; add the change to the balance above to get the next balance line.')
    return steps


def explain_crossfoot(t):
    r = t['rows'][0]
    h = t['head']
    v = [num(x) for x in r]
    return ['Cross-footing means adding the column totals across the page to prove that the debit columns equal the credit columns before anything is posted.',
            f'**Debit columns:** {h[0]} {r[0]} + {h[1]} {r[1]} = {money(v[0] + v[1], True)}.',
            f'**Credit columns:** {h[2]} {r[2]} + {h[3]} {r[3]} + {h[4]} {r[4]} = {money(v[2] + v[3] + v[4], True)}.',
            'Both sides are equal, so the cash receipts journal is in balance and the column totals can be posted.']


def t_items(cell):
    out = []
    for piece in [x.strip() for x in (cell or '').split(';') if x.strip()]:
        if 'new balance' in piece.lower() or 'as printed' in piece.lower():
            continue
        m = re.findall(r'\d{1,3}(?:[,.]\d{3})+(?:\.\d\d)?|\d+(?:\.\d\d)?', piece)
        if m:
            out.append((piece, num(m[-1].replace('.', ',', 1) if re.fullmatch(r'\d{1,3}\.\d{3}', m[-1]) else m[-1])))
    return out


def explain_taccount(t):
    h = t['head']
    steps = ['A T-account has a left (debit) side and a right (credit) side. To post, put each debit amount on the left of the account named and each credit amount on the right; '
             'the balance is the difference between the two sides, written on the larger side.']
    for r in t['rows']:
        a = r[0]
        dr, cr = t_items(r[1]), t_items(r[2] if len(r) > 2 else '')
        typ = acct_type(a)
        line = f'**{a}** — debit side: ' + ('; '.join(p for p, _ in dr) or 'nothing') + '; credit side: ' + ('; '.join(p for p, _ in cr) or 'nothing') + '.'
        sd, sc = sum(v for _, v in dr if v), sum(v for _, v in cr if v)
        if dr and cr:
            bal = sd - sc
            line += f' Debits {money(sd, True)} − credits {money(sc, True)} = {money(abs(bal), True)} ' + ('debit balance.' if bal > 0 else 'credit balance.' if bal < 0 else '— the account is closed (zero balance).')
        if typ in NORMAL:
            line += f' {a.split(" (")[0]} is {TYPE_TXT[typ]}, so it normally has a {"debit" if NORMAL[typ] == "Dr" else "credit"} balance.'
        nb = re.search(r'new balance ([\d,]+)', ' '.join(r[1:3]))
        if nb:
            line += f' New balance: {" + ".join(p for p, _ in (dr or cr))} = {nb.group(1)}.'
        if len(r) > 3 and r[3]:
            line += f' Balance shown: {r[3]}.'
            if dr and cr and num(r[3]) is not None and abs(sd - sc) != num(r[3]):
                line += ' The printed amounts on this account do not add up to that balance, so one of them is a printing slip; the balance shown is the correct result of the closing entries.'
        steps.append(line)
    return steps


def practice_taccount(t, D):
    h = t['head']
    rows, ans = [], []
    for r in D:
        rr = list(r)
        dr, cr = t_items(r[1]), t_items(r[2] if len(r) > 2 else '')
        sd, sc = sum(v for _, v in dr if v), sum(v for _, v in cr if v)
        if len(h) > 3:
            rr[3] = '?' if r[3] else ''
        ans.append(f'**{r[0]}**: debits ' + (' + '.join(money(v, True) for _, v in dr) or '0') + f' = {money(sd, True)}; credits ' +
                   (' + '.join(money(v, True) for _, v in cr) or '0') + f' = {money(sc, True)}; balance = {money(abs(sd - sc), True)} ' +
                   ('debit.' if sd > sc else 'credit.' if sc > sd else '(closed).'))
        rows.append(rr)
    return ('Every amount is doubled. Post the amounts to the correct side of each T-account and work out each balance.', h, rows, ans)


def explain_special(t):
    h = t['head']
    mcs = money_cols(t)
    dr = [j for j in mcs if re.search(r'debit|\bdr\b|dr\.|\(dr', h[j].lower()) and not re.search(r'cr\.?\)?$', h[j].lower())]
    cr = [j for j in mcs if j not in dr]
    ja = col(h, 'account')
    jdate = col(h, 'date')
    steps = ['A special (multi-column) journal gives each frequent account its own column, so one line records a whole entry and only the column totals are posted. '
             'Debit columns here: ' + (', '.join(h[j] for j in dr) or '—') + '. Credit columns: ' + (', '.join(h[j] for j in cr) or '—') + '.']
    if len(mcs) == 1:
        steps = [f'This journal has a single amount column, “{h[mcs[0]]}”. Every amount in it is at the same time a debit to the first account named and a credit to the second, '
                 'so one line is a complete double entry; the name in the account column tells which subsidiary-ledger account (customer or creditor) to post to.']
    rows = t['rows']
    i = 0
    while i < len(rows):
        r = rows[i]
        filled = [(j, r[j]) for j in mcs if r[j]]
        a = r[ja] if ja is not None else ''
        date = r[jdate] if jdate is not None else ''
        if not filled:
            i += 1
            continue
        if all(re.fullmatch(r'\([\d√ ]+\)', v) for _, v in filled):
            steps.append('**Posting references under the totals:** ' + ', '.join(f'{h[j]} {v}' for j, v in filled) +
                         ' — a number is the ledger account the column total was posted to; (√) means that column’s total is not posted, because each amount in it was posted on its own.')
            i += 1
            continue
        is_total = a.lower().startswith('total') or (not a and not date and i >= len(rows) - 2 and len(filled) >= 1 and i > 0)
        if is_total:
            sd = sum(num(v) for j, v in filled if j in dr and num(v) is not None)
            sc = sum(num(v) for j, v in filled if j in cr and num(v) is not None)
            line = '**Column totals (footing):** ' + ', '.join(f'{h[j]} {v}' for j, v in filled) + '.'
            for j, v in filled:
                col_sum = sum(num(rr[j]) for rr in rows[:i] if num(rr[j]) is not None and not re.fullmatch(r'\(.*\)', rr[j]))
                if num(v) is not None and col_sum and col_sum != num(v):
                    line += f' (Adding the {h[j]} column gives {money(col_sum, True)}; the printed total is {v}.)'
            if dr and cr:
                line += (f' Cross-foot: debit columns {money(sd, True)} = credit columns {money(sc, True)}, so the journal is proved.' if sd == sc else
                         f' Cross-foot: debit columns {money(sd, True)}, credit columns {money(sc, True)}.')
            else:
                line += ' The one total is posted twice — as a debit to the first account in the column heading and as a credit to the second (see the account numbers written under it).'
            steps.append(line)
            i += 1
            continue
        # a group: following rows with no date and a single General amount belong to the same cheque/receipt
        grp = [r]
        k = i + 1
        while k < len(rows) and not (rows[k][jdate] if jdate is not None else '') and ja is not None and rows[k][ja] and not rows[k][ja].lower().startswith('total') \
                and len([j for j in mcs if rows[k][j]]) == 1:
            grp.append(rows[k]); k += 1
        who = a or ('no account title needed: the amount has its own special column' if a == '' else a)
        line = f'**{("Date " + date + ": ") if date else ""}{who}** — ' + ', '.join(f'{h[j]} {v}' for j, v in filled) + '.'
        if len(grp) > 1:
            parts = [(g[ja], next(g[j] for j in mcs if g[j])) for g in grp]
            tot = sum(num(x) for _, x in parts if num(x) is not None)
            line = (f'**{("Date " + date + ": ") if date else ""}several payments on one line group** — ' + ', '.join(f'{x} {v}' for x, v in parts) +
                    f'. Each expense is debited in the General Debit column; together they are {money(tot, True)}, and the Cash Credit column shows the cash paid: '
                    + ', '.join(f'{h[j]} {v}' for j, v in filled if j in cr) + '.')
            if any(num(v) is not None and num(v) != tot for j, v in filled if j in cr):
                line += f' (The cash credit and the debits should be equal; the printed figures differ, so one of them is a slip.)'
        elif a and any('general' in h[j].lower() or 'sundry' in h[j].lower() for j, _ in filled):
            line += f' {a} has no special column of its own, so its amount goes in the General (Sundry) column and is posted separately to the {a} account.'
        elif not a or a in ('√', '-'):
            line += ' No account title is needed (a dash or √): the amount sits in a special column whose total is posted at the end of the month.'
        refs = [r[j] for j in range(len(h)) if j not in mcs and ('ref' in h[j].lower() or h[j].lower() in ('pr', 'p/r')) and r[j]]
        if refs:
            line += f' Post. Ref. {" ".join(refs)}: the account number written after posting (√ = posted to a customer or creditor in a subsidiary ledger).'
        steps.append(line)
        i = k
    return steps


TOTAL_WORDS = ('total', 'net ', 'net income', 'net sales', 'net purchases', 'gross', 'cost of goods', 'increase', 'book value', 'capital, ', 'balance')


def segments(t):
    """split a two-sided statement (Assets | Liabilities and Capital) into [text col + its amount cols]"""
    h, mcs = t['head'], set(money_cols(t))
    txt = [j for j in range(len(h)) if j not in mcs and any(r[j] and num(r[j]) is None for r in t['rows'])]
    if len(txt) <= 1:
        return [list(range(len(h)))]
    return [list(range(j, txt[k + 1] if k + 1 < len(txt) else len(h))) for k, j in enumerate(txt)]


def sub(t, cols):
    return dict(t, head=[t['head'][j] for j in cols], rows=[[r[j] for j in cols] for r in t['rows'] if any(r[j] for j in cols)])



def computed(t):
    """{(row, col): explanation} for derived figures (totals, nets, book values), segment- and column-aware"""
    out = {}
    for cols in segments(t):
        st = sub(t, cols)
        idx = [i for i, r in enumerate(t['rows']) if any(r[j] for j in cols)]
        mcs = money_cols(st)
        stack = {c: [] for c in mcs}   # per column: list of (label, value)
        allv = []                      # every amount in the segment, any column: (row, label, value)
        for i, r in enumerate(st['rows']):
            lab = label(r, st) or ''
            low = lab.lower()
            here = [(c, num(r[c])) for c in mcs if r[c].strip() and num(r[c]) is not None]
            if not here:
                continue
            exp = ''
            c, v = here[-1]
            av = abs(v)
            if low.startswith('less') and len(here) == 2 and allv:
                x = abs(here[0][1]); p = allv[-1][2]
                if p - x == av:
                    exp = f'Book value = {money(p, True)} − {money(x, True)} = {money(av, True)}.'
            elif any(w in low for w in TOTAL_WORDS) or not lab:
                items = stack[c]
                # look for a run at the end of this column that adds or subtracts to v
                for k in range(len(items) - 2, -1, -1):
                    run = items[k:]
                    tot = sum(x for _, x in run)
                    if tot == av:
                        exp = 'It adds the amounts above: ' + ' + '.join(money(x, True) for _, x in run) + f' = {money(av, True)}.'
                    elif run[0][1] - sum(x for _, x in run[1:]) == av:
                        exp = f'It is {money(run[0][1], True)} − ' + ' − '.join(money(x, True) for _, x in run[1:]) + f' = {money(av, True)}.'
                    if exp:
                        stack[c] = items[:k]
                        break
                if not exp:  # try the column to the left (sub-column feeding a total)
                    for c2 in mcs:
                        if c2 < c and len(stack[c2]) >= 2:
                            for k in range(len(stack[c2]) - 2, -1, -1):
                                run = stack[c2][k:]
                                if sum(x for _, x in run) == av:
                                    exp = 'It adds the amounts in the inner column: ' + ' + '.join(money(x, True) for _, x in run) + f' = {money(av, True)}.'
                                elif run[0][1] - sum(x for _, x in run[1:]) == av:
                                    exp = f'It is {money(run[0][1], True)} − ' + ' − '.join(money(x, True) for _, x in run[1:]) + f' = {money(av, True)}.'
                                if exp:
                                    stack[c2] = stack[c2][:k]
                                    break
                        if exp:
                            break
                if not exp and 'total' in low and stack[c]:
                    tot = sum(x for _, x in stack[c])
                    exp = (f'Adding the amounts listed in this column gives ' + ' + '.join(money(x, True) for _, x in stack[c]) + f' = {money(tot, True)}'
                           + ('.' if tot == av else f'; the printed figure is {money(av, True)}, so check it against the other side of the statement.'))
                    stack[c] = []
            for cc, x in here[:-1] if exp else here:
                stack[cc].append((lab, abs(x)))
            if exp:
                stack[c].append((lab, av))
                out[(idx[i], cols[c])] = exp
            allv.append((i, lab, av))
    return out


def explain_generic(t):
    comp = computed(t)
    out = []
    segs = segments(t)
    mcs_all = set(money_cols(t))
    for cols in segs:
        st = sub(t, cols)
        idx = [i for i, r in enumerate(t['rows']) if any(r[j] for j in cols)]
        if len(segs) > 1:
            out.append(f'**{st["head"][0] or "Next"} side** — read it from top to bottom:')
        for k, r in enumerate(st['rows']):
            lab = label(r, st)
            vals = [r[c] for c in range(len(cols)) if cols[c] in mcs_all and r[c]]
            if not vals and not lab:
                continue
            line = f'**{lab or "(total line)"}**: ' + (', '.join(vals) if vals else 'a heading; the amounts below belong to it.')
            why = [comp[(idx[k], j)] for j in cols if (idx[k], j) in comp]
            if why:
                line += ' ' + ' '.join(why)
            elif vals and lab and not lab.lower().startswith(('less', 'total')):
                side = (st['head'][0] or '').lower()
                ty = 'L' if re.search(r'owe|liabil', side) and 'capital' not in side else 'A' if re.search(r'own|asset', side) else acct_type(lab)
                if ty in NORMAL:
                    line += f' — {lab} is {TYPE_TXT[ty]}, so it is listed with its ledger balance.'
            out.append(line)
    return out


def amounts(row, mcs, upto=None):
    return [num(row[c]) for c in mcs if (upto is None or c <= upto) and num(row[c]) is not None and row[c].strip()]


def find_sum(t, i, mcs):
    """explain a computed line (total, net, less, book value) from the lines above it"""
    r = t['rows'][i]
    lab = (label(r, t) or '').lower()
    here = [(c, num(r[c])) for c in mcs if r[c].strip() and num(r[c]) is not None]
    if not here:
        return ''
    if lab.startswith('less') and len(here) == 2 and i > 0:
        prev = amounts(t['rows'][i - 1], mcs)
        x, y = abs(here[0][1]), here[1][1]
        if prev and prev[-1] - x == y:
            return f'Book value = {money(prev[-1], True)} − {money(x, True)} = {money(y, True)}.'
    if not (any(w in lab for w in TOTAL_WORDS) or not lab):
        return ''
    c, v = here[-1]
    v = abs(v)
    items = []
    for k in range(i - 1, -1, -1):
        got = [x for cc, x in ((cc, num(t['rows'][k][cc])) for cc in mcs if t['rows'][k][cc].strip()) if x is not None]
        if not got:
            if items:
                continue
            continue
        items.append((label(t['rows'][k], t) or 'subtotal', abs(got[-1])))
        tot = sum(x for _, x in items)
        if tot == v and len(items) >= 2:
            return 'It adds the amounts above: ' + ' + '.join(money(x, True) for _, x in reversed(items)) + f' = {money(v, True)}.'
        if len(items) >= 2:
            first, rest = items[-1][1], sum(x for _, x in items[:-1])
            if first - rest == v:
                return f'It is {money(first, True)} − {money(rest, True)} = {money(v, True)}.'
            if first + rest - 2 * items[0][1] == v - items[0][1]:
                pass
        if len(items) >= 2 and abs(items[1][1] - items[0][1]) == v:
            a_, b_ = items[1][1], items[0][1]
            return f'It is {money(max(a_, b_), True)} − {money(min(a_, b_), True)} = {money(v, True)}.'
        if len(items) > 16:
            break
    return ''


def explain_chart(t):
    steps = ['A chart of accounts lists every account with its number. The first digit tells the group — 1 assets, 2 liabilities, 3 capital, 4 revenue, 5 (or 6) expenses — '
             'and the second digit is the account’s place in that group, so accounts are kept in balance-sheet order and are easy to find in the ledger.']
    for r in t['rows']:
        cells = [c for c in r if c]
        pairs = []
        k = 0
        while k < len(r):
            a = r[k]
            nxt = r[k + 1] if k + 1 < len(r) else ''
            if a and re.fullmatch(r'\d{2}', nxt or ''):
                pairs.append((a, nxt)); k += 2; continue
            m = re.fullmatch(r'(.*\D)\s+(\d{2})', a or '')
            if m:
                pairs.append((m.group(1), m.group(2)))
            k += 1
        for a, n in pairs:
            steps.append(f'{a} — number {n}: first digit {n[0]}, so it is in group {n[0]} ({TYPE_TXT.get(acct_type(a), "an account")}).')
        if not pairs and cells:
            steps.append('Group heading: ' + ' / '.join(cells) + '.')
    return steps


def explain_schedule(t):
    h, r = t['head'], t['rows'][0]
    m, tot = r[0], r[-1]
    return [f'The yearly amount {tot} is spread evenly over the 12 months: {tot} ÷ 12 = {money(num(tot) / 12, True)}, rounded to {m} a month.',
            f'Each month column shows {m}. Twelve months × {m} = {money(12 * num(m))} — rounding makes this differ slightly from {tot}, which is why the Total column is the yearly figure.',
            'Only one month (September) belongs to the period of the worksheet, so the adjusting entry records just one month’s amount.']


def explain_missing(t):
    h = t['head']
    steps = []
    if len(h) == 3 or 'Liabilities' in h:
        ja = {'a': None}
        cols = [j for j, x in enumerate(h) if num(x) is None]
        for r in t['rows']:
            cells = r[-3:]
            vals = [Fraction(0) if c.lower() == 'none' else num(c) for c in cells]
            nm = r[0] + ': ' if len(r) > 3 else ''
            if vals.count(None) != 1:
                continue
            k = vals.index(None)
            a, l, c = vals
            if k == 0:
                ans = l + c; steps.append(f'{nm}Assets = Liabilities + Capital = {money(l, True)} + {money(c, True)} = **{money(ans, True)}**.')
            elif k == 1:
                ans = a - c; steps.append(f'{nm}Liabilities = Assets − Capital = {money(a, True)} − {money(c, True)} = **{money(ans, True)}**.')
            else:
                ans = a - l; steps.append(f'{nm}Capital = Assets − Liabilities = {money(a, True)} − {money(l, True)} = **{money(ans, True)}**.')
        return ['Use the accounting equation, Assets = Liabilities + Capital, and rearrange it for the missing item ("None" means 0).'] + steps
    # income statement tabulation: Sales, Returns, Net sales, Beg inv, Net purch, End inv, COGS, Gross profit
    steps = ['Three relationships fill every gap: Net sales = Sales − Sales returns; Cost of goods sold = Beginning inventory + Net purchases − Ending inventory; '
             'Gross profit = Net sales − Cost of goods sold.']
    for i, r in enumerate(t['rows']):
        v = [num(c) for c in r]
        S, R, N, B, P, E, C, G = v
        out = []
        for _ in range(3):
            if N is None and S is not None and R is not None: N = S - R; out.append(f'Net sales = {money(S)} − {money(R)} = {money(N)}')
            if R is None and S is not None and N is not None: R = S - N; out.append(f'Sales returns = {money(S)} − {money(N)} = {money(R)}')
            if C is None and N is not None and G is not None: C = N - G; out.append(f'Cost of goods sold = {money(N)} − {money(G)} = {money(C)}')
            if G is None and N is not None and C is not None: G = N - C; out.append(f'Gross profit = {money(N)} − {money(C)} = {money(G)}')
            if E is None and None not in (B, P, C): E = B + P - C; out.append(f'Ending inventory = {money(B)} + {money(P)} − {money(C)} = {money(E)}')
            if B is None and None not in (E, P, C): B = C + E - P; out.append(f'Beginning inventory = {money(C)} + {money(E)} − {money(P)} = {money(B)}')
            if C is None and None not in (B, P, E): C = B + P - E; out.append(f'Cost of goods sold = {money(B)} + {money(P)} − {money(E)} = {money(C)}')
        steps.append(f'**Row {i + 1}:** ' + '; '.join(out) + '.')
    return steps


def explain_dc(t):
    known = {'repairs income': ('Cash', 'Repairs Income'), 'rent': ('Rent Expense', 'Cash'), 'advertising': ('Advertising Expense', 'Cash'),
             'electricity': ('Electricity (Utilities) Expense', 'Cash'), 'telephone': ('Telephone (Utilities) Expense', 'Cash'),
             'postage': ('Miscellaneous Expense', 'Cash'), 'supplies': ('Supplies', 'Cash')}
    steps = ['For each transaction ask: which two accounts change, is each one up or down, and on which side does that change go?']
    for r in t['rows']:
        tx = r[1].lower()
        for k, (d, c) in known.items():
            if k in tx:
                steps.append(f'**{r[0]} {r[1]}** Debit {d}, credit {c}. {why_side(d, "Dr")} {why_side(c, "Cr")}')
                break
    return steps


EXPLAIN = {'taccount': explain_taccount, 'crossfoot': explain_crossfoot, 'journal': explain_journal, 'ledger': explain_ledger, 'trial': explain_trial, 'worksheet': explain_worksheet, 'equation': explain_equation,
           'special': explain_special, 'chart': explain_chart, 'schedule': explain_schedule, 'missing': explain_missing, 'dc_exercise': explain_dc}


# ---------------------------------------------------------------- practice
def practice(t, kind):
    """-> (instruction, head, rows with ?, answer steps)"""
    h = t['head']
    D = [[dbl(c) for c in r] for r in t['rows']]
    if kind == 'ledger':
        jb = col(h, 'balance')
        rows = []
        for r in D:
            rr = list(r)
            if (num(r[col(h, 'debit')]) not in (None, Fraction(0))) or (num(r[col(h, 'credit')]) not in (None, Fraction(0))):
                rr[jb] = '?'
            rows.append(rr)
        tt = dict(t, rows=D)
        ans = explain_ledger(dict(tt, rows=[r[:] for r in D]))[1:]
        return ('Every amount has been doubled. Work out each “?” in the Balance column, line by line.', h, rows, ans)
    if kind in ('journal',):
        jd, jc = col(h, 'debit'), col(h, 'credit')
        ja = col(h, 'account') if col(h, 'account') is not None else (col(h, 'description') if col(h, 'description') is not None else 1)
        rows, ans = [], []
        for r in D:
            d, c = num(r[jd]), num(r[jc])
            if d is not None and c is not None and not r[ja]:
                continue
            amt = r[jd] or r[jc]
            if amt and num(amt):
                rows.append([' '.join(x for x in r[:ja] if x), r[ja].strip(), amt, '?'])
                side = 'Dr' if r[jd] else 'Cr'
                ans.append(f'{r[ja].strip() or "The account"} {amt}: **{"Debit" if side == "Dr" else "Credit"}**. {why_side(r[ja].strip() or "It", side)}')
            elif r[ja]:
                rows.append([' '.join(x for x in r[:ja] if x), r[ja], '', ''])
        sd = sum(num(r[jd]) for r in D if num(r[jd]) is not None and r[ja])
        sc = sum(num(r[jc]) for r in D if num(r[jc]) is not None and r[ja])
        ans.append(f'Total debits {money(sd, True)} = total credits {money(sc, True)}' + (' — the journal balances.' if sd == sc else '.'))
        return ('Every amount has been doubled and the Debit/Credit columns removed. For each account decide: Debit or Credit? Then check that the totals agree.',
                ['Date', 'Account', 'Amount', 'Debit or Credit?'], rows, ans)
    if kind == 'trial':
        jd, jc = col(h, 'debit'), col(h, 'credit')
        rows, ans = [], []
        sd = sc = Fraction(0)
        for r in D:
            a = r[0]
            if not a or a.lower().startswith('total'):
                continue
            v = num(r[jd]) if num(r[jd]) not in (None, Fraction(0)) else num(r[jc])
            if v in (None, Fraction(0)):
                continue
            nb = NORMAL.get(acct_type(a)) or ('Dr' if num(r[jd]) not in (None, Fraction(0)) else 'Cr')
            rows.append([a, money(v, has_cents(r[jd] or r[jc])), '?'])
            sd += v if nb == 'Dr' else 0
            sc += v if nb == 'Cr' else 0
            ans.append(f'{a} {money(v, True)} → **{"Debit" if nb == "Dr" else "Credit"}** column ({TYPE_TXT.get(acct_type(a), "account")}; normal balance {"debit" if nb == "Dr" else "credit"}).')
        ans.append(f'Totals: Debit {money(sd, True)}, Credit {money(sc, True)}' + (' — equal, so the trial balance balances.' if sd == sc else '.'))
        return ('The balances below are doubled. Put each one in the correct column of a trial balance (by its normal balance) and find the two totals.',
                ['Account Title', 'Balance (Nakfa)', 'Debit or Credit?'], rows, ans)
    if kind == 'worksheet':
        keep = [j for j, x in enumerate(h) if not re.search(r'income statement|balance sheet', x.lower()) or 'trial' in x.lower()]
        hide = [j for j in range(len(h)) if j not in keep]
        if not hide:
            hide = [j for j, x in enumerate(h) if 'adjusted' in x.lower()]
        rows = [[('?' if j in hide and r[j] else r[j]) for j in range(len(h))] for r in D]
        ans = explain_worksheet(dict(t, rows=D))[1:]
        return ('Every amount is doubled. Fill each “?” by extending the balances to the correct columns, then total the columns and find the net income.', h, rows, ans)
    if kind == 'equation':
        rows = [[r[0]] + (['?' if c else '' for c in r[1:]] if r[0].lower().startswith('ba') and i > 0 else r[1:]) for i, r in enumerate(D)]
        ans = explain_equation(dict(t, rows=D))[1:]
        return ('Every amount is doubled. Work out each balance line (“?”) by applying the transactions in order.', h, rows, ans)
    if kind == 'missing':
        rows = [[dbl(c) if c not in ('?', 'None', 'none') and not re.fullmatch(r'\([a-j]\)', c) else c for c in r] for r in t['rows']]
        ans = EXPLAIN['missing'](dict(t, rows=rows))[1:]
        return ('The same exercise with every given amount doubled. Find each missing item.', h, rows, ans)
    if kind == 'schedule':
        rows = [[dbl(c) for c in r] for r in t['rows']]
        r = rows[0]
        rows = [['?'] * (len(r) - 1) + [r[-1]]]
        ans = [f'Monthly amount = {D[0][-1]} ÷ 12 = {money(num(D[0][-1]) / 12, True)}, rounded to {money(round(num(D[0][-1]) / 12))} for each month.']
        return ('The yearly amount is doubled. What goes in each month?', h, rows, ans)
    if kind == 'chart':
        rows, ans = [], []
        for r in t['rows']:
            k = 0
            while k < len(r):
                a, nxt = r[k], (r[k + 1] if k + 1 < len(r) else '')
                m = re.fullmatch(r'(.*\D)\s+(\d{2})', a or '')
                if a and re.fullmatch(r'\d{2}', nxt or ''):
                    rows.append([a, '?']); ans.append(f'{a}: group {nxt[0]} ({TYPE_TXT.get(acct_type(a), "account")}), number {nxt}.'); k += 2; continue
                if m:
                    rows.append([m.group(1), '?']); ans.append(f'{m.group(1)}: group {m.group(2)[0]} ({TYPE_TXT.get(acct_type(m.group(1)), "account")}), number {m.group(2)}.')
                k += 1
        return ('Without looking at the chart above: which group does each account belong to, and what is its account number?', ['Account', 'Group and number'], rows, ans)
    if kind == 'dc_exercise':
        return ('Fill in the Debit and Credit account for every transaction.', h, [[r[0], r[1], '?', '?'] for r in t['rows']], explain_dc(t)[1:])
    if kind == 'taccount':
        return practice_taccount(t, D)
    if kind == 'special':
        mcs = money_cols(t)
        ja = col(h, 'account')
        rows = []
        tot_i = [i for i, r in enumerate(D) if (ja is not None and r[ja].lower().startswith('total')) or (i == len(D) - 1 and any(r[j] for j in mcs))
                 or (i == len(D) - 2 and any(r[j] for j in mcs) and all(re.fullmatch(r'\(.*\)', D[-1][j]) or not D[-1][j] for j in mcs))]
        tot_i = [i for i in tot_i if not all(re.fullmatch(r'\(.*\)', D[i][j]) or not D[i][j] for j in mcs)][:1]
        for i, r in enumerate(D):
            rows.append([('?' if (i in tot_i and j in mcs and r[j]) else r[j]) for j in range(len(h))])
        ans = []
        for i in tot_i:
            for j in mcs:
                if D[i][j]:
                    items = [rr[j] for rr in D[:i] if num(rr[j]) is not None and rr[j]]
                    ans.append(f'**{h[j]}** total = ' + ' + '.join(items) + f' = {money(sum(num(x) for x in items), True)}.')
        dr = [j for j in mcs if re.search(r'debit|\bdr\b|dr\.|\(dr', h[j].lower())]
        if tot_i and dr and len(dr) < len(mcs):
            i = tot_i[0]
            sd = sum(num(D[i][j]) for j in dr if num(D[i][j]) is not None)
            sc = sum(num(D[i][j]) for j in mcs if j not in dr and num(D[i][j]) is not None)
            ans.append(f'Cross-foot: debit totals {money(sd, True)} and credit totals {money(sc, True)}' + (' — equal, so the journal is proved.' if sd == sc else '.'))
        return ('Every amount is doubled. Foot (add) each amount column to fill the “?” totals, then cross-foot: total of the debit columns = total of the credit columns.', h, rows, ans)
    # statements, T-accounts, other: hide computed cells
    mcs = money_cols(t)
    comp = computed(dict(t, rows=D))
    rows = [list(r) for r in D]
    ans = []
    hidden = 0
    for (i, j), exp in sorted(comp.items()):
        rows[i][j] = '?'
        hidden += 1
        lab = next((D[i][c] for c in range(j, -1, -1) if D[i][c] and num(D[i][c]) is None), '') or 'Total line'
        ans.append(f'**{lab}**: ' + exp.replace('the printed figure is', 'the doubled printed figure would be'))
    if not hidden and mcs:  # nothing derived: ask for the doubled figures' total of the main amount column
        j = mcs[-1]
        s = sum(num(r[j]) for r in D if num(r[j]) is not None)
        rows = D + [['Total'] + [''] * (len(h) - 2) + ['?']] if len(h) >= 2 else D
        if len(h) >= 2:
            rows[-1][j] = '?'
            ans = [f'Add the {h[j] or "amount"} column: ' + ' + '.join(r[j] for r in D if num(r[j]) is not None) + f' = **{money(s, True)}**.']
    return ('Every amount is doubled and the figures that are worked out are shown as “?”. Find them.', h, rows, ans)


# ---------------------------------------------------------------- titles & build
def short_title(t, kind):
    tt = t['title'].strip(' —')
    if not tt:
        h = ' '.join(t['head']).lower()
        tt = {'schedule': 'Depreciation spread over twelve months', 'worksheet': 'Partial worksheet', 'trial': 'Trial balance',
              'journal': 'General Journal — ' + ('closing entries' if 'closing' in h else 'adjusting entries' if 'adjusting' in h else 'entries'),
              'statement': 'Statement figures', 'special': 'Special journal'}.get(kind, 'Bookkeeping table')
        if kind == 'statement' and t['rows'] and t['rows'][0][0].startswith('Zebib'):
            tt = 'Zebib’s account balances (prepare a trial balance)'
        elif kind == 'statement' and 'owned' in h:
            tt = 'What Dehab’s taxi business owns and owes'
        elif kind == 'statement' and t['head'][:2] == ['Assets', 'Liabilities']:
            tt = 'Delina Office Management Services — assets and liabilities'
        elif kind == 'trial' and 'income statement' in h:
            tt = 'Selam Super Market — worksheet data (Problem 3)'
    tt = re.sub(r'Account Title:\s*_*\s*', 'Ledger: ', tt)
    tt = re.sub(r'_+', '', tt)
    tt = re.sub(r'\s+', ' ', tt).strip()
    return tt


def main():
    data = json.load(open(TABLES))
    counts = {}
    for g, (path, uid) in BOOKS.items():
        p = os.path.join(ROOT, path)
        book = json.load(open(p))
        unit = next(u for u in book['units'] if u['id'] == uid)
        for l in unit['lessons']:
            l['cards'] = [c for c in l['cards'] if not str(c.get('id', '')).startswith(uid + '-bk')]
        lessons = unit['lessons']

        def lesson_for(pg):
            for l in lessons:
                a, b = l['pages']
                if a <= pg <= b:
                    return l
            return lessons[0] if pg < lessons[0]['pages'][0] else lessons[-1]
        n = 0
        for t in data[g]:
            kind = kind_of(t)
            n += 1
            bid = f'{uid}-bk{n:03d}'
            title = short_title(t, kind)
            steps = EXPLAIN.get(kind, explain_generic)(t)
            if len(steps) < 2:
                steps = steps + explain_generic(t)
            ins, ph, prows, ans = practice(t, kind)
            if not ans:
                ans = ['Work each “?” exactly as in the explanation above, using the doubled amounts.']
            pg = int(t['page'])
            src = f'textbook p.{pg}'

            def chunks(xs):
                xs = list(xs) if len(xs) >= 2 else list(xs) + ['Check your answer by working the same figure out a second way (for example, from the other column or the other side).']
                k = (len(xs) + 9) // 10
                size = (len(xs) + k - 1) // k
                return [xs[i:i + size] if len(xs[i:i + size]) >= 2 else xs[i - 1:i + size] for i in range(0, len(xs), size)]
            how, tries = chunks(steps), chunks(ans)
            cards = [{'id': bid, 'type': 'table', 'title': f'Table {n}: {title}', 'page': pg, 'src': src, 'head': t['head'], 'rows': t['rows']}]
            for k, part in enumerate(how):
                cards.append({'id': bid + '-how' + (f'{k + 1}' if len(how) > 1 else ''), 'type': 'worked',
                              'title': f'How Table {n} is built, step by step' + (f' (part {k + 1} of {len(how)})' if len(how) > 1 else ''), 'page': pg, 'src': src,
                              'problem': f'Where does every figure in Table {n} ({title}) come from, and how is each entry posted?' if k == 0 else f'Table {n}, continued.',
                              'steps': [{'text': x} for x in part],
                              'answer': f'Every figure in Table {n} follows from the double-entry rules: each debit has an equal credit, and each balance is the previous balance plus or minus the amount posted.'})
            cards.append({'id': bid + '-pt', 'type': 'table', 'title': f'Practice {n}: {title}', 'page': pg, 'src': src, 'head': ph, 'rows': prows})
            for k, part in enumerate(tries):
                cards.append({'id': bid + '-pa' + (f'{k + 1}' if len(tries) > 1 else ''), 'type': 'worked', 'mode': 'try',
                              'title': f'Practice {n} — try it, then check each step' + (f' (part {k + 1} of {len(tries)})' if len(tries) > 1 else ''),
                              'page': pg, 'src': src, 'problem': ins if k == 0 else f'Practice {n}, continued.',
                              'steps': [{'text': x} for x in part], 'answer': part[-1]})
            lesson_for(pg)['cards'].extend(cards)
        counts[uid] = n
        raw = json.dumps(book, ensure_ascii=False, indent=2) + '\n'
        open(p, 'w').write(raw)
    print(counts)


if __name__ == '__main__':
    main()

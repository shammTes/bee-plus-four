"""Business notes (G10–G12): study-friendly layouts for the text tables, and two textbook comparison tables.

Idempotent: re-running it leaves the JSON unchanged. Bookkeeping tables (ids ...-bkNNN) get their layouts from
tool/bookkeeping/present.py via build_notes.py; this script only touches the hand-written tables.

  python3 tool/biz_tables/study_layouts.py && python3 tool/split_notes.py && python3 tool/build_tutor_index.py
"""
import json, os, re

ROOT = os.path.join(os.path.dirname(__file__), '..', '..')
BOOK = os.path.join(ROOT, 'assets/high/notes/notes/business_economics_{}.json')

# G10 textbook pp.17–19 (printed), 1.2 Business Organizations
FORMS = {
    'id': 'be10-u1-tbo1', 'type': 'table', 'title': 'Forms of business organization compared', 'page': 17,
    'src': 'textbook pp.17–19', 'enriched': True, 'layout': 'compare',
    'head': ['Feature', 'Sole proprietorship', 'Partnership', 'Corporation'],
    'rows': [
        ['Owners', 'One individual', 'Two or more owners', 'Shareholders (stockholders)'],
        ['Managed by', 'The owner, who makes all managerial decisions', 'The partners, sharing management by skill and knowledge',
         'Hired professional managers, overseen by a board of directors'],
        ['Liability', '**Unlimited**: the owner’s personal assets can be sold to pay the firm’s debts',
         '**Unlimited**: each partner is liable for all the firm’s debts', '**Limited** to the amount each owner invested'],
        ['Capital comes from', 'The proprietor’s own capital', 'The pooled financial resources of the partners', 'Selling shares (stocks) to the public'],
        ['Profit', 'All kept by the owner (after tax)', 'Shared among the partners', 'Divided among the shareholders as **dividends**'],
        ['Life span', 'Limited: may stop when the owner dies or is ill for a long time', 'Easily dissolved when a partner dies or withdraws',
         'Continues: the death of owners or the sale of shares does not end it'],
        ['Examples / types', 'Hairdresser, retail shop, restaurant, shoe making firm', 'Law, medical and accounting services',
         'Closed (private) and open (public) corporations'],
    ],
    'key_point': 'Liability is the big difference: owners of a sole proprietorship or a partnership have **unlimited liability**; shareholders of a corporation risk only what they invested.',
}
PROS = {
    'id': 'be10-u1-tbo2', 'type': 'table', 'title': 'Advantages and disadvantages of each form', 'page': 18,
    'src': 'textbook pp.18–19', 'enriched': True, 'layout': 'proscons',
    'head': ['Form', 'Advantages', 'Disadvantages'],
    'rows': [
        ['Sole proprietorship', 'Easy to start and to end; The owner is his/her own boss; Keeps all the profit (after tax)',
         'Unlimited liability; Limited growth; Limited life span; Longer working hours'],
        ['Partnership', 'Easy to start and to end; Shared management and pooled resources; Builds trust among partners',
         'Unlimited liability, also for the partners’ mistakes; Disagreement among partners; Easy to dissolve'],
        ['Corporation', 'Limited liability; Continuity; Can grow into a large-scale business; Easy to employ professional employees',
         'Double taxation (on corporate profit, then on dividends); Large initial cost; Possible conflict between managers and owners'],
    ],
    'key_point': 'A corporation’s limited liability and continuity come at a price: **double taxation** and a large initial cost.',
}

# hand-written text tables: layout (+ optional key point drawn from the card's own rows)
LAYOUT = {
    'be10-u1-tblE1': ('cards', None),
    'be10-u2-tblE1': ('terms', None),
    'be10-u3-tblE1': ('cards', None),
    'be10-u3-tb2-t1': ('cards', None),
    'be10-u3-tb5-t1': ('cards', 'Assets, expenses and drawing increase on the **debit** side; liabilities, capital and revenue increase on the **credit** side.'),
    'be10-u3-tb7b': ('compare', None),
    'be10-u3-tb10-t1': ('cards', None),
    'be10-u3-tb12-t1': ('cards', None),
    'be11-u1-c15': ('grid', None),
    'be11-u2-tblE1': ('compare', None),
    'be11-u2-tb2-t1': ('compare', None),
    'be11-u2-tb5-t1': ('cards', None),
    'be11-u2-tb8-t1': ('cards', None),
    'be11-u2-tb11-t1': ('cards', None),
    'be11-u2-tb14-t1': ('cards', None),
    'be12-u2-tblE1': ('cards', None),
}


def plain_maths(cell):
    """'$$1,500$$' / '$$12\\text{ months}$$' -> '1,500' / '12 months': plain amounts typeset as display maths broke the line"""
    return re.sub(r'\$\$([\d,.]+)(?:\\text\{([^}]*)\})?\$\$', lambda m: m.group(1) + (m.group(2) or ''), cell)


def main():
    for g in ('10', '11', '12'):
        path = BOOK.format(g)
        raw = open(path).read()
        d = json.loads(raw)
        for u in d['units']:
            for l in u['lessons']:
                cards = l['cards']
                if l['id'] == 'be10-u1-l1-2':
                    ids = [c.get('id') for c in cards]
                    at = ids.index('be10-u1-c08') + 1
                    for new in (FORMS, PROS):
                        if new['id'] in ids:
                            cards[ids.index(new['id'])] = dict(new)
                        else:
                            cards.insert(at, dict(new))
                            ids.insert(at, new['id'])
                        at = ids.index(new['id']) + 1
                for c in cards:
                    if c.get('type') == 'table' and c.get('id') in LAYOUT:
                        c['rows'] = [[plain_maths(x) for x in r] for r in c['rows']]
                        lay, kp = LAYOUT[c['id']]
                        c['layout'] = lay
                        if kp:
                            c['key_point'] = kp
        out = json.dumps(d, ensure_ascii=False, indent=2) + ('\n' if raw.endswith('\n') else '')
        if out != raw:
            open(path, 'w').write(out)
            print('updated', os.path.basename(path))


if __name__ == '__main__':
    main()

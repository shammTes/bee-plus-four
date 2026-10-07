import json,re
def numfix(c):
    s=c.strip()
    m=re.fullmatch(r'([+\-]?)\s*([\d,]+(?: [\d,]+)+)',s)
    if m and re.search(r'\d \d',s):
        toks=m.group(2).split(' '); sign=m.group(1)
        cents=None
        if len(toks)>=2 and toks[-1] in('00','50') and len(toks[-2].replace(',',''))>=1 and (len(toks)>2 or len(toks[-2])>=3):
            cents=toks[-1]; toks=toks[:-1]
        d=''.join(toks).replace(',','')
        if d.isdigit(): return sign+f'{int(d):,}'+('.'+cents if cents else '')
    m=re.fullmatch(r'([\d,]+) (00|50)',s)
    if m: return m.group(1)+'.'+m.group(2)
    m=re.fullmatch(r'([\d,]+)\.(\d) (\d)',s)
    if m: return f'{m.group(1)}.{m.group(2)}{m.group(3)}'
    s=re.sub(r'(\d),(\d) (\d)',r'\1,\2\3',s)
    s=re.sub(r'^(\d+),(\d)\s(\d\d,\d{3}(?:\.\d\d)?)$',lambda m: m.group(1)+','+m.group(2)+m.group(3),s)
    return s
def fmt_join(parts):
    ps=[p for p in parts if p]
    if not ps: return ''
    if all(re.fullmatch(r'[\d,]+',p) for p in ps):
        if len(ps)>=2 and ps[-1] in ('00','50') and len(ps[-1])==2:
            return f"{int(''.join(ps[:-1]).replace(',','')):,}.{ps[-1]}"
        return f"{int(''.join(ps).replace(',','')):,}"
    return ' '.join(ps)
def clean_table(t):
    head=list(t['head']); rows=[list(r) for r in t['rows']]
    # merge adjacent identical non-empty headers
    groups=[];
    for j,h in enumerate(head):
        if groups and h and h==head[groups[-1][0]]: groups[-1].append(j)
        else: groups.append([j])
    head=[head[g[0]] for g in groups]; rows=[[fmt_join([r[j] for j in g]) if len(g)>1 else r[g[0]] for g in groups] for r in rows]
    # merge cents-only columns into previous
    j=1
    while j<len(head):
        vals=[r[j] for r in rows if r[j]]
        if vals and all(re.fullmatch(r'\d\d',v) for v in vals) and not head[j]:
            for r in rows:
                if r[j]: r[j-1]=(r[j-1].replace(' ','')+'.'+r[j]) if r[j-1] else r[j]
            del head[j]; [r.pop(j) for r in rows]
        else: j+=1
    rows=[[numfix(c) for c in r] for r in rows]
    t=dict(t,head=head,rows=rows); return t
def messy(t):
    cells=[c for r in t['rows'] for c in r]+t['head']
    return any(re.search(r'\d \d',c) for c in cells) or any(re.match(r'(Account Title|Acc|Date Item|Date\b.*Debit)',r[0] or '') for r in t['rows']) or any(re.fullmatch(r'[a-z].*',h) for h in t['head'] if h) or (t['head'] and all(not h for h in t['head']) and len(t['head'])>3)
if __name__=='__main__':
    d=json.load(open('/tmp/raw_tables.json'))
    for g in d:
        d[g]=[clean_table(t) for t in d[g]]
        print(g,[ (i,t['page']) for i,t in enumerate(d[g]) if messy(t)])
    json.dump(d,open('/tmp/clean_tables.json','w'),ensure_ascii=False,indent=1)

import pdfplumber,json,re,sys
def isnum(s): return bool(re.fullmatch(r'[\d,.()\-]+',s or '')) and any(c.isdigit() for c in s)
def clean(s): return re.sub(r'\s+',' ',(s or '').replace('Þ','fi').replace('ß','fl')).strip()
def fmt_digits(parts):
    ps=[p for p in parts if p]
    if not ps: return ''
    if all(re.fullmatch(r'\d+',p) for p in ps) and len(ps)>1:
        cents=None
        if len(ps[-1])==2 and len(ps)>=2 and all(len(p)==1 for p in ps[:-1]): cents=ps[-1]; ps=ps[:-1]
        if all(len(p)==1 for p in ps):
            n=int(''.join(ps)); return f'{n:,}'+('.'+cents if cents else '')
    return ' '.join(clean(p) for p in ps)
def process(pdfpath,pages,printed_off):
    pdf=pdfplumber.open(pdfpath); out=[]
    for pn in pages:
        page=pdf.pages[pn-1]
        for ti,tb in enumerate(page.find_tables()):
            t=tb.extract(); W=len(t[0])
            titles=[];i=0
            while i<len(t) and t[i][0] and all(c is None for c in t[i][1:]): titles.append(clean(t[i][0])); i+=1
            # header rows: until a row containing a number in a non-first col
            hdr=[]
            while i<len(t) and not any(isnum(clean(c)) for c in t[i][1:] if c) :
                if any(c for c in t[i]): hdr.append(t[i])
                i+=1
                if len(hdr)>4: break
            data=[r for r in t[i:] if any(c and c.strip() for c in r)]
            if not data or not any(isnum(clean(c)) for r in data for c in r if c): continue
            # groups from header rows: owner = last non-None col to the left in the deepest header row covering
            base=hdr[-1] if hdr else [ '' ]*W
            owner=[];cur=0
            for j in range(W):
                if base[j] is not None: cur=j
                owner.append(cur)
            groups=sorted(set(owner))
            def hname(g):
                names=[]
                for h in hdr:
                    # nearest non-None at or left of g
                    k=g
                    while k>0 and h[k] is None: k-=1
                    v=clean(h[k])
                    if v and v not in names: names.append(v)
                return ' — '.join(names) if names else ''
            head=[hname(g) for g in groups]
            rows=[]
            for r in data:
                cells=[]
                for g in groups:
                    parts=[clean(r[j]) for j in range(W) if owner[j]==g and r[j] is not None]
                    cells.append(fmt_digits(parts))
                rows.append(cells)
            # drop empty columns
            keep=[k for k in range(len(head)) if head[k] or any(r[k] for r in rows)]
            head=[head[k] for k in keep]; rows=[[r[k] for k in keep] for r in rows]
            # caption: text just above table
            x0,top,x1,bot=tb.bbox
            above=page.crop((0,max(0,top-40),page.width,top)).extract_text() or ''
            cap=[clean(l) for l in above.split('\n') if clean(l)]
            out.append({'pdf_page':pn,'page':pn-printed_off,'idx':ti,'titles':titles,'head':head,'rows':rows,'above':cap[-2:]})
    return out
if __name__=='__main__':
    a=process('/workspace/textbooks/textbook_business_economics_10.pdf',range(68,159),6)
    b=process('/workspace/textbooks/textbook_business_economics_11.pdf',range(68,146),5)
    json.dump({'10':a,'11':b},open('/tmp/raw_tables.json','w'),ensure_ascii=False,indent=1)
    print(len(a),len(b))

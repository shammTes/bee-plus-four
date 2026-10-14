import asyncio
from playwright.async_api import async_playwright
DUMP=r"""[...document.querySelectorAll('flt-semantics')].map(e=>{const r=e.getBoundingClientRect();const t=(e.getAttribute('aria-label')||(e.childElementCount?'':e.textContent)||'').replace(/\s+/g,' ').slice(0,70);return t.trim()?`${t} @${r.x|0},${r.y|0} ${r.width|0}x${r.height|0}`:''}).filter(Boolean).join('\n')"""
async def start(p, state=None):
    b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox','--use-gl=angle'])
    c=await b.new_context(viewport={'width':360,'height':780},device_scale_factor=1.5,storage_state=state)
    pg=await c.new_page(); pg.on('console',lambda m: print('CON',m.text[:300]) if 'GL Driver' not in m.text else None)
    await pg.goto('http://localhost:8765/'); await pg.wait_for_timeout(8000)
    await sem(pg)
    return b,c,pg
async def sem(pg):
    await pg.evaluate("document.querySelector('flt-semantics-placeholder')?.click()"); await pg.wait_for_timeout(800)
async def dump(pg): return await pg.evaluate(DUMP)
import hmac,hashlib,time,secrets,json,re
def code(dev):
    n=secrets.token_hex(4).upper(); ts=str(int(time.time()*1000))
    body=f"BEE1|{dev}|H|{n}|{ts}"
    return body+"|"+hmac.new(b'BEE-PLUS-OFFLINE-SECRET-v1-ET-2026-SHAM',body.encode(),hashlib.sha256).hexdigest()[:24]
async def find(pg,txt,nth=0):
    els=await pg.evaluate(r"""(t)=>[...document.querySelectorAll('flt-semantics')].filter(e=>{const s=(e.getAttribute('aria-label')||(e.childElementCount?'':e.textContent)||'');return s.replace(/\s+/g,' ').includes(t)}).map(e=>{const r=e.getBoundingClientRect();return [r.x+r.width/2,r.y+r.height/2,r.width,r.height]})""",txt)
    els=[e for e in els if e[2]>0]
    return els[nth] if len(els)>nth else None
async def find2(pg,txt,nth=0):
    for _ in range(8):
        e=await find(pg,txt,nth)
        if e: return e
        await pg.wait_for_timeout(500); await sem(pg)
async def tap(pg,txt,nth=0,wait=1200,dy=0):
    e=await find2(pg,txt,nth)
    for _ in range(6):
        if not e or 70<e[1]<680: break
        await pg.mouse.move(180,400); await pg.mouse.wheel(0,e[1]-380); await pg.wait_for_timeout(700); e=await find2(pg,txt,nth)
    if not e: raise Exception('notfound '+txt)
    y=e[1]-e[3]/2+dy if dy else e[1]
    await pg.mouse.click(e[0],y); await pg.wait_for_timeout(wait); return e

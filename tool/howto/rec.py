import asyncio, base64, json, os, sys, time
from playwright.async_api import async_playwright
import h
VW, VH = 360, 700
NAV_Y = VH - 54
TABS = {'home': 50, 'notes': 120, 'exercise': 186, 'matric': 248, 'tutor': 310}
OVL = r"""
window.__tap=(x,y)=>{const d=document.createElement('div');d.style.cssText=`position:fixed;left:${x-24}px;top:${y-24}px;width:48px;height:48px;border-radius:50%;background:rgba(232,98,58,.35);border:3px solid #E8623A;z-index:99999;pointer-events:none;transform:scale(.4);transition:transform .35s ease-out,opacity .5s`;document.body.appendChild(d);requestAnimationFrame(()=>{d.style.transform='scale(1)'});setTimeout(()=>{d.style.opacity='0'},900);setTimeout(()=>d.remove(),1500)};
window.__hl=(x,y,w,h,ms)=>{const d=document.createElement('div');d.style.cssText=`position:fixed;left:${x-5}px;top:${y-5}px;width:${w+10}px;height:${h+10}px;border-radius:18px;border:3px solid #E8623A;box-shadow:0 0 0 4000px rgba(0,0,0,.18);z-index:99998;pointer-events:none;opacity:0;transition:opacity .3s`;document.body.appendChild(d);requestAnimationFrame(()=>{d.style.opacity='1'});setTimeout(()=>{d.style.opacity='0'},ms);setTimeout(()=>d.remove(),ms+400)};
window.__card=(n,t,ms)=>{const d=document.createElement('div');d.style.cssText=`position:fixed;inset:0;z-index:100000;background:#F6EFE4;display:flex;flex-direction:column;align-items:center;justify-content:center;font-family:Nunito,sans-serif;transition:opacity .4s;pointer-events:none`;d.innerHTML=`<div style="font-size:20px;font-weight:800;color:#C24E32;letter-spacing:1px">PART ${n}</div><div style="font-size:30px;font-weight:900;color:#2B2118;text-align:center;padding:10px 24px;line-height:1.2">${t}</div>`;document.body.appendChild(d);setTimeout(()=>{d.style.opacity='0'},ms);setTimeout(()=>d.remove(),ms+500)};
"""
class R:
    def __init__(s, name): s.name=name; s.caps=[]; s.frames=[]; s.dir=f'rec/{name}'; os.makedirs(s.dir, exist_ok=True)
    async def open(s, p, state='state_tour.json', semantics=True):
        s.b = await p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox'])
        s.c = await s.b.new_context(viewport={'width': VW, 'height': VH}, device_scale_factor=1.5, storage_state=state)
        await s.c.grant_permissions(['clipboard-read','clipboard-write'], origin='http://localhost:8765')
        s.pg = await s.c.new_page()
        await s.pg.goto('http://localhost:8765/'); await s.pg.wait_for_timeout(8000)
        await s.pg.evaluate(OVL)
        s.semon = semantics
        if semantics: await h.sem(s.pg)
        s.cdp = await s.c.new_cdp_session(s.pg)
        s.cdp.on('Page.screencastFrame', s._frame)
        await s.cdp.send('Page.startScreencast', {'format': 'jpeg', 'quality': 88, 'maxWidth': 540, 'maxHeight': 1050, 'everyNthFrame': 1})
        await s.pg.wait_for_timeout(600)
        s.t0 = time.time()
    async def _frame(s, ev):
        i = len(s.frames); fn = f'{s.dir}/f{i:05d}.jpg'
        open(fn, 'wb').write(base64.b64decode(ev['data']))
        s.frames.append((ev['metadata'].get('timestamp', time.time()), fn))
        try: await s.cdp.send('Page.screencastFrameAck', {'sessionId': ev['sessionId']})
        except Exception: pass
    def cap(s, text): s.caps.append((time.time(), text))
    async def w(s, ms): await s.pg.wait_for_timeout(ms)
    async def sem(s): s.semon = True; await h.sem(s.pg)
    async def card(s, n, t, ms=1700): await s.pg.evaluate(f'__card({json.dumps(str(n))},{json.dumps(t)},{ms})'); await s.w(ms+500)
    async def xy(s, x, y, wait=1300, show=True):
        if show: await s.pg.evaluate(f'__tap({x},{y})'); await s.w(450)
        await s.pg.mouse.click(x, y); await s.w(wait)
    async def tap(s, label, nth=0, wait=1300, dy=0, dx=0):
        e = await s.find(label, nth)
        x = e[0] + dx; y = (e[1] - e[3]/2 + dy) if dy else e[1]
        await s.xy(x, y, wait)
    async def find(s, label, nth=0):
        e = await h.find2(s.pg, label, nth)
        for _ in range(8):
            if not e: break
            if 70 < e[1] < VH - 90: return e
            await s.scroll(e[1] - VH/2 + 40, slow=True); e = await h.find2(s.pg, label, nth)
        if not e:
            print('NOTFOUND', label); print(await h.dump(s.pg)); raise SystemExit(2)
        return e
    async def hl(s, label, ms=1600, nth=0):
        e = await s.find(label, nth)
        await s.pg.evaluate(f'__hl({e[0]-e[2]/2},{e[1]-e[3]/2},{e[2]},{e[3]},{ms})'); await s.w(ms+300)
    async def tab(s, t, wait=1600): await s.xy(TABS[t], NAV_Y, wait)
    async def scroll(s, dy, slow=True):
        await s.pg.mouse.move(VW/2, VH/2)
        n = max(1, int(abs(dy)//60)) if slow else 1
        for _ in range(n): await s.pg.mouse.wheel(0, dy/n); await s.w(40)
        await s.w(700)
        if s.semon: await h.sem(s.pg)
    async def type(s, text): await s.pg.keyboard.type(text, delay=70); await s.w(500)
    async def dump(s): print(await h.dump(s.pg))
    async def close(s):
        s.t1 = time.time()
        await s.w(300)
        await s.cdp.send('Page.stopScreencast'); await s.w(300)
        json.dump({'t0': s.t0, 't1': s.t1, 'caps': s.caps, 'frames': s.frames, 'cuts': [c for c in s.cuts if c[1]]}, open(f'{s.dir}/meta.json', 'w'))
        await s.b.close()
async def main(name, fn):
    async with async_playwright() as p:
        r = R(name)
        await fn(r, p)
        await r.close()
async def _hlr(s, x, y, w, h_, ms=1600): await s.pg.evaluate(f'__hl({x},{y},{w},{h_},{ms})'); await s.w(ms+300)
async def _point(s, x, y, ms=1200): await s.pg.evaluate(f'__tap({x},{y})'); await s.w(ms)
async def _drag(s, x1, y1, x2, y2, steps=25):
    await s.pg.evaluate(f'__tap({x1},{y1})'); await s.w(400)
    await s.pg.mouse.move(x1, y1); await s.pg.mouse.down()
    for i in range(1, steps+1): await s.pg.mouse.move(x1+(x2-x1)*i/steps, y1+(y2-y1)*i/steps); await s.w(40)
    await s.pg.mouse.up(); await s.w(800)
R.hlr=_hlr; R.point=_point; R.drag=_drag
async def _seek(s, label, step=350, tries=20):
    for _ in range(tries):
        e = await h.find(s.pg, label)
        if e and 70 < e[1] < VH - 90: return e
        await s.scroll(step)
    print('SEEKFAIL', label); print(await h.dump(s.pg)); raise SystemExit(2)
R.seek=_seek
async def _top(s, label, pad=90):
    e = await s.seek(label, step=500, tries=40)
    await s.scroll(e[1]-e[3]/2-pad); return await h.find(s.pg, label)
R.top=_top
def _pause(s): s.cuts.append([time.time(), None])
def _resume(s): s.cuts[-1][1] = time.time()
R.pause=_pause; R.resume=_resume
_oi = R.__init__
def _ni(s, name): _oi(s, name); s.cuts = []
R.__init__ = _ni
async def _blobs(s, rgb, tol=18, minpx=200):
    import numpy as np, io
    from PIL import Image
    from scipy import ndimage
    a = np.asarray(Image.open(io.BytesIO(await s.pg.screenshot())).convert('RGB')).astype(int)
    m = (np.abs(a - np.array(rgb)).max(axis=2) < tol)
    lab, n = ndimage.label(m)
    out = []
    for i in range(1, n+1):
        ys, xs = np.nonzero(lab == i)
        if len(ys) >= minpx: out.append((xs.mean()/1.5, ys.mean()/1.5, len(ys)))
    return sorted(out, key=lambda b: b[1])
R.blobs=_blobs

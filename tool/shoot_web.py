#!/usr/bin/env python3
"""Screenshots of the design reference (/workspace/high/design/reference.html) at 390x844 @2x, touch, in-app layout,
with a FIXED clock (2026-09-29 10:00 +03:00, same as the Flutter tests) -> compare/web/<scene>[_dark].png.
Also writes compare/seed_progress.json: the 'high:v1' record produced by the web app's own record() API, which the
Flutter screenshot test loads unchanged, so both sides compute every number from the same state.
    python3 tool/shoot_web.py [scene-filter]"""
import asyncio, datetime, json, os, sys
from playwright.async_api import async_playwright
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
URL = 'file:///workspace/high/design/reference.html?app=1'
OUT = os.path.join(HERE, 'compare', 'web')
FILT = sys.argv[1] if len(sys.argv) > 1 else ''
T0 = int(datetime.datetime(2026, 9, 29, 10, 0, tzinfo=datetime.timezone(datetime.timedelta(hours=3))).timestamp() * 1000)
CLOCK = """(() => { const T0 = %d, R = Date, s = R.now(); const now = () => T0 + (R.now() - s);
  class D extends R { constructor(...a) { if (a.length) super(...a); else super(now()); } static now() { return now(); } }
  window.Date = D; })();""" % T0
SEED = open(os.path.join(HERE, 'tool', 'seed_progress.js')).read()

def fresh(theme):
    return {'v': 2, 'name': 'Hana', 'theme': theme, 'cat': 'matric', 'answers': {}, 'bookmarks': [], 'mistakes': [], 'ev': [], 'study': {}, 'recent': [], 'attempts': [], 'daily': {}}

async def main():
    os.makedirs(OUT, exist_ok=True)
    errs = []
    async with async_playwright() as p:
        b = await p.chromium.launch()

        async def page(state, dark=False):
            ctx = await b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=2, is_mobile=True, has_touch=True,
                                      color_scheme='dark' if dark else 'light')
            await ctx.add_init_script(CLOCK)
            if state is not None:
                await ctx.add_init_script("if (!sessionStorage.getItem('seeded')) { localStorage.setItem('high:v1', %s); sessionStorage.setItem('seeded', '1'); }" % json.dumps(json.dumps(state)))
            pg = await ctx.new_page()
            pg.on('pageerror', lambda e: errs.append(str(e)))
            await pg.goto(URL)
            await pg.wait_for_timeout(600)
            return ctx, pg

        # 1) progress seed, made by the web app itself
        ctx, pg = await page(fresh('light'))
        await pg.evaluate(SEED)
        st = json.loads(await pg.evaluate("localStorage.getItem('high:v1')"))
        await ctx.close()
        st['daily'] = {}
        json.dump(st, open(os.path.join(HERE, 'compare', 'seed_progress.json'), 'w'), ensure_ascii=False)

        async def scene(name, state, dark, go=None, scroll=0, act=None, wait=1400):
            full = name + ('_dark' if dark else '')
            if FILT and FILT not in full:
                return
            s = dict(state); s['theme'] = 'dark' if dark else 'light'
            ctx, pg = await page(s, dark)
            if go:
                await pg.evaluate(f"APP.go('{go}', {{}}, {{push: false}})")
            if act:
                await pg.evaluate(act)
            await pg.wait_for_timeout(wait)
            if scroll:
                await pg.evaluate(f"(() => {{ const s = document.getElementById('screen'); s.style.scrollBehavior = 'auto'; s.scrollTop = {scroll}; }})()")
                await pg.wait_for_timeout(400)
            await pg.screenshot(path=os.path.join(OUT, full + '.png'))
            print('shot', full)
            await ctx.close()

        for dark in (False, True):
            await scene('home_fresh', fresh('light'), dark)
            await scene('home', st, dark)
            await scene('home_mid', st, dark, scroll=760)
            await scene('home_end', st, dark, scroll=1500)
            await scene('exams', st, dark, go='subjects')
            await scene('exams_list', st, dark, go='subjects', scroll=700)
            await scene('exams_rows', st, dark, go='subjects', scroll=1500)
            await scene('exams_model', dict(st, cat='model'), dark, go='subjects')
            await scene('settings', st, dark, go='settings')
        await b.close()
    for e in errs:
        print('PAGE ERROR', e)

asyncio.run(main())

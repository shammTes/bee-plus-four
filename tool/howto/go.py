import asyncio, sys
from ch import *
async def run(n):
    title, f, st, sm = CH[n]
    async with async_playwright() as p:
        r = R(n); await r.open(p, st, sm)
        try: await f(r)
        finally: await r.close()
asyncio.run(run(sys.argv[1]))

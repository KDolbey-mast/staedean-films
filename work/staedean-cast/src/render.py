import asyncio, pathlib
from rig import W, H, defs, paper_overlay


def wrap(art, view=None, seed=7, overlay=True):
    vb = view or (0, 0, W, H)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="{vb[0]} {vb[1]} {vb[2]} {vb[3]}">'
            + defs(seed, W / vb[2]) + f'<g filter="url(#wobble)">{art}</g>'
            + (f'<g transform="translate({vb[0]},{vb[1]}) scale({vb[2] / W},{vb[3] / H})">{paper_overlay()}</g>' if overlay else '')
            + '</svg>')


async def _render(items, out, workers=4):
    from playwright.async_api import async_playwright
    out = pathlib.Path(out); out.mkdir(parents=True, exist_ok=True)
    q = asyncio.Queue()
    for it in items: q.put_nowait(it)
    async with async_playwright() as p:
        br = await p.chromium.launch()
        async def work():
            pg = await br.new_page(viewport={"width": W, "height": H})
            while not q.empty():
                name, svg = q.get_nowait()
                await pg.set_content(f'<html><body style="margin:0;overflow:hidden">{svg}</body></html>')
                await pg.screenshot(path=str(out / f"{name}.png"))
                print("rendered", name, flush=True)
        await asyncio.gather(*[work() for _ in range(workers)])
        await br.close()


def render(items, out):
    asyncio.run(_render(list(items), out))

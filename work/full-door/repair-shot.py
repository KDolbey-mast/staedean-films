"""Re-render the corrected prototype-tool contact after the main export."""
import asyncio
import build
import director as d
from playwright.async_api import async_playwright
async def main():
    shot=next(s for s in d.SHOTS if s['name']=='V2_week2')
    async with async_playwright() as p:
        browser=await p.chromium.launch(executable_path=d.week1.BROWSER)
        page=await browser.new_page(viewport={'width':1280,'height':720})
        for n in range(round(shot['dur']*d.FPS)):
            d.film.NOW=n/d.FPS
            await page.set_content('<style>body{margin:0}svg{width:1280px;height:720px}</style>'+shot['draw'](n/d.FPS,n))
            await page.screenshot(path=str(build.WORK/'frames'/shot['name']/f'{n:04d}.png'))
        await browser.close()
asyncio.run(main())

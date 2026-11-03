import asyncio,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'work/full-door'))
import director as d,rb
from playwright.async_api import async_playwright
from PIL import Image,ImageDraw
async def main():
    async with async_playwright() as p:
        browser=await p.chromium.launch(executable_path=d.week1.BROWSER)
        page=await browser.new_page(viewport={'width':1600,'height':900})
        for style in ('wash','brush'):
            rb.STYLE=style
            await page.set_content('<style>body{margin:0}svg{width:1600px;height:900px}</style>'+d.week1.frame(3.5,42))
            await page.screenshot(path=str(ROOT/'outputs'/f'The-Door-{style}-study-frame.png'))
        await browser.close()
    sheet=Image.new('RGB',(1600,480),'white');ink=ImageDraw.Draw(sheet)
    for i,style in enumerate(('wash','brush')):
        im=Image.open(ROOT/'outputs'/f'The-Door-{style}-study-frame.png').resize((800,450))
        sheet.paste(im,(i*800,30));ink.text((i*800+12,10),'PREVIOUS STUDY' if i==0 else 'UNEVEN WASH + WHITE GAPS',fill='black')
    sheet.save(ROOT/'outputs'/'The-Door-brush-study-comparison.jpg',quality=95)
asyncio.run(main())

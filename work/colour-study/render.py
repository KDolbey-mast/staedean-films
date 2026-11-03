"""Render identical drawings in the established and proposed colour treatments."""
import sys,asyncio
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'work/full-door'))
import director as d,rb
from playwright.async_api import async_playwright
from PIL import Image,ImageDraw
async def main():
    out=ROOT/'outputs'
    async with async_playwright() as p:
        browser=await p.chromium.launch(executable_path=d.week1.BROWSER)
        page=await browser.new_page(viewport={'width':1600,'height':900})
        for label,draw,t in [('customer',d.week1.frame,3.5),('office',d.office,1),('visit',d.week3,2.5)]:
            for style in ('marker','wash'):
                rb.STYLE=style
                svg=draw(t,round(t*12))
                await page.set_content('<style>body{margin:0}svg{width:1600px;height:900px}</style>'+svg)
                await page.screenshot(path=str(out/f'colour-study-{label}-{style}.png'))
        await browser.close()
    sheet=Image.new('RGB',(1600,1410),'white');ink=ImageDraw.Draw(sheet)
    for row,label in enumerate(('customer','office','visit')):
        for col,style in enumerate(('marker','wash')):
            im=Image.open(out/f'colour-study-{label}-{style}.png');im.resize((800,450)).save(ROOT/'work/colour-study'/f'{label}-{style}.png')
            sheet.paste(im.resize((800,450)),(col*800,row*470+20))
            ink.text((col*800+15,row*470+4),'CURRENT COLOUR' if style=='marker' else 'INK + WASH STUDY',fill='#232323')
    sheet.save(out/'The-Door-colour-comparison.jpg',quality=94)
asyncio.run(main())

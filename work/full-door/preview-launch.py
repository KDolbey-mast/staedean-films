import asyncio,sys
from pathlib import Path
import director as d,launch_shot as l
from playwright.async_api import async_playwright
from PIL import Image,ImageDraw
async def main():
    folder=Path(__file__).parent/'launch-proof';folder.mkdir(exist_ok=True)
    frames=[0,12,18,24,25,28,40,49,60]
    async with async_playwright() as p:
        browser=await p.chromium.launch(executable_path=d.week1.BROWSER)
        page=await browser.new_page(viewport={'width':1280,'height':720})
        for n in frames:
            await page.set_content('<style>body{margin:0}svg{width:1280px;height:720px}</style>'+l.draw(n/12,n))
            await page.screenshot(path=str(folder/f'{n:04d}.png'))
        await browser.close()
    sheet=Image.new('RGB',(1200,735),'#f5f0e7');ink=ImageDraw.Draw(sheet)
    for i,n in enumerate(frames):
        im=Image.open(folder/f'{n:04d}.png');im.thumbnail((400,225));x=i%3*400;y=i//3*245
        sheet.paste(im,(x,y));ink.text((x+6,y+228),f'{n/12:.2f}s',fill='black')
    sheet.save(folder/'sheet.jpg')
asyncio.run(main())

import sys, glob
from PIL import Image, ImageDraw, ImageFont
pat = sys.argv[1]; out = sys.argv[2]; cols = int(sys.argv[3]) if len(sys.argv) > 3 else 3
fs = sorted(glob.glob(f'frames/{pat}*.png'))
tw, th, pad, lab = 640, 360, 20, 34
rows = (len(fs) + cols - 1) // cols
sheet = Image.new('RGB', (pad + cols * (tw + pad), pad + rows * (th + pad + lab)), '#e9e0cf')
d = ImageDraw.Draw(sheet)
font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 19)
for i, fp in enumerate(fs):
    im = Image.open(fp).convert('RGB').resize((tw, th), Image.LANCZOS)
    x = pad + (i % cols) * (tw + pad); y = pad + (i // cols) * (th + pad + lab)
    sheet.paste(im, (x, y)); d.rectangle([x - 1, y - 1, x + tw, y + th], outline='#2e2520', width=2)
    name = fp.split('/')[-1][:-4]
    d.text((x, y + th + 6), name.replace('_', ' ', 2).replace('_', ' '), fill='#2e2520', font=font)
sheet.save(out); print(out, sheet.size)

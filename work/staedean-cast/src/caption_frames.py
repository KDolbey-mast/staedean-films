import glob, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
from captions import CAP
os.makedirs("cframes", exist_ok=True)
font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSerifItalic.ttf", 44)
W, H = 1920, 1080
# paper background with a little grain, made once
rng = np.random.default_rng(3)
base = np.ones((H, W, 3)) * np.array([242, 232, 213])
grain = rng.normal(0, 5, (H // 4, W // 4))
grain = np.array(Image.fromarray(grain.astype(np.float32)).resize((W, H), Image.BICUBIC))
paper = Image.fromarray(np.clip(base + grain[..., None] * np.array([1, 0.9, 0.75]), 0, 255).astype(np.uint8))
iw, ih, ix, iy = 1744, 981, 88, 14
for fp in sorted(glob.glob("frames/*.png")):
    key = os.path.basename(fp)[:5]
    can = paper.copy()
    # soft shadow under the picture
    sh = Image.new("L", (W, H), 0); ImageDraw.Draw(sh).rectangle([ix + 6, iy + 8, ix + iw + 6, iy + ih + 8], fill=70)
    can.paste(Image.new("RGB", (W, H), (120, 100, 80)), (0, 0), sh.filter(ImageFilter.GaussianBlur(8)))
    can.paste(Image.open(fp).convert("RGB").resize((iw, ih), Image.LANCZOS), (ix, iy))
    d = ImageDraw.Draw(can)
    d.rectangle([ix - 1, iy - 1, ix + iw, iy + ih], outline=(46, 37, 32), width=3)
    t = CAP[key]
    if t:
        d.text((W / 2, 1043), t, font=font, fill=(46, 37, 32), anchor="mm")
    can.save(f"cframes/{os.path.basename(fp)}")
print("done")

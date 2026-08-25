from PIL import Image, ImageDraw, ImageFont
import os

OUT = r"D:\Projects\builds\binance-calculator"
BG = (11, 14, 17)       # --bg
GOLD = (240, 185, 11)   # --gold
DARK = (11, 14, 17)
font_path = r"C:\Windows\Fonts\msyh.ttc"

def make(size):
    img = Image.new("RGB", (size, size), BG)
    d = ImageDraw.Draw(img)
    # 圆角内描边方块
    m = int(size*0.12)
    r = int(size*0.22)
    d.rounded_rectangle([m, m, size-m, size-m], radius=r, outline=GOLD, width=max(3, int(size*0.025)))
    # 文字
    fsize = int(size*0.5)
    try:
        f = ImageFont.truetype(font_path, fsize)
    except Exception:
        f = ImageFont.load_default()
    txt = "开"
    bbox = d.textbbox((0,0), txt, font=f)
    tw, th = bbox[2]-bbox[0], bbox[3]-bbox[1]
    x = (size - tw)//2 - bbox[0]
    y = (size - th)//2 - bbox[1]
    d.text((x, y), txt, fill=GOLD, font=f)
    p = os.path.join(OUT, f"icon-{size}.png")
    img.save(p)
    print("saved", p)

make(192)
make(512)

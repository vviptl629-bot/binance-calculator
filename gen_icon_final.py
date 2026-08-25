from PIL import Image, ImageDraw

S = 512
img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
d = ImageDraw.Draw(img)

# 白底圆角盒子
margin = 0
radius = 70
d.rounded_rectangle([margin, margin, S - margin, S - margin], radius=radius, fill=(255, 255, 255, 255))

# 绿色 T
green = (38, 161, 123, 255)  # USDT green
# 横条
bar_h = int(S * 0.11)
bar_w = int(S * 0.42)
top = int(S * 0.30)
cx = S // 2
d.rectangle([cx - bar_w // 2, top, cx + bar_w // 2, top + bar_h], fill=green)
# 竖条
stem_w = int(S * 0.11)
stem_bottom = int(S * 0.70)
d.rectangle([cx - stem_w // 2, top, cx + stem_w // 2, stem_bottom], fill=green)

for sz in (192, 512):
    img.resize((sz, sz), Image.LANCZOS).save(f"icon-{sz}.png")
print("saved icon-192.png / icon-512.png")

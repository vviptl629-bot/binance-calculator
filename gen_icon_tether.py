"""
币安开仓计算器 · 应用图标复刻
参照 Tether (USDT) 官方 Logo 视觉:
  外层青绿底圆 → 白色高光圆 + 阴影 → 内部绿色六边形 → 白色 T(横+竖+圆环)
"""
from PIL import Image, ImageDraw, ImageFilter

# ---------- 调色板 ----------
BG_GREEN   = (38, 161, 123, 255)   # 外层青绿底 (#26A97B)
WHITE      = (255, 255, 255, 255)
SHADOW     = (0, 0, 0, 60)
HEX_GREEN  = (50, 181, 143, 255)   # 六边形绿色（比外底略亮，制造层次）


def draw_icon(size: int) -> Image.Image:
    # 用 4× 超采样画，最后 downscale，画质更干净
    S = size * 4
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    # 1) 外层青绿底圆（带轻微阴影）
    pad = int(S * 0.02)
    # 阴影层
    shadow = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.ellipse([pad + int(S * 0.015), pad + int(S * 0.03),
                S - pad + int(S * 0.015), S - pad + int(S * 0.03)],
               fill=SHADOW)
    shadow = shadow.filter(ImageFilter.GaussianBlur(radius=S * 0.012))
    img.alpha_composite(shadow)

    # 底圆
    d.ellipse([pad, pad, S - pad, S - pad], fill=BG_GREEN)

    # 2) 中间白色圆（带阴影 → 立体感）
    r = int(S * 0.36)             # 白色圆半径（相对 S）
    cx, cy = S // 2, S // 2
    # 白色圆阴影
    white_shadow = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    wsd = ImageDraw.Draw(white_shadow)
    wsd.ellipse([cx - r + int(S * 0.008), cy - r + int(S * 0.02),
                 cx + r + int(S * 0.008), cy + r + int(S * 0.02)],
                fill=(0, 0, 0, 70))
    white_shadow = white_shadow.filter(ImageFilter.GaussianBlur(radius=S * 0.012))
    img.alpha_composite(white_shadow)
    # 白色圆本体
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=WHITE)

    # 3) 内部绿色六边形（点朝上）
    # 六边形边长 / 半径比例：六边形外接圆 = 半径为 h 的圆
    # 朝上顶点: (cx, cy - h)，其余顶点围绕
    import math
    hex_h = int(S * 0.27)        # 六边形"半径"(中心到顶点)
    hex_pts = []
    for i in range(6):
        # 起始角 -90°（顶部），每 60°
        angle = math.radians(-90 + 60 * i)
        hex_pts.append((cx + hex_h * math.cos(angle),
                        cy + hex_h * math.sin(angle)))
    d.polygon(hex_pts, fill=HEX_GREEN)

    # 4) T 字形 + 圆环
    #   横条：宽 ~ 42%S，高 ~ 10%S，位于顶部
    #   竖条：宽 ~ 11%S，下沿到 ~ 70%S
    bar_w  = int(S * 0.42)
    bar_h  = int(S * 0.105)
    top_y  = int(S * 0.285)
    d.rectangle([cx - bar_w // 2, top_y,
                 cx + bar_w // 2, top_y + bar_h], fill=WHITE)

    stem_w = int(S * 0.105)
    stem_bottom = int(S * 0.66)
    d.rectangle([cx - stem_w // 2, top_y,
                 cx + stem_w // 2, stem_bottom], fill=WHITE)

    # 圆环（穿过竖条中部）
    ring_cx, ring_cy = cx, cy + int(S * 0.005)
    ring_rx = int(S * 0.165)
    ring_ry = int(S * 0.055)
    ring_w  = max(int(S * 0.012), 4)
    d.ellipse([ring_cx - ring_rx, ring_cy - ring_ry,
               ring_cx + ring_rx, ring_cy + ring_ry],
              outline=WHITE, width=ring_w)

    # 缩小到目标 size（高质量重采样）
    return img.resize((size, size), Image.LANCZOS)


if __name__ == "__main__":
    for sz in (192, 512):
        out = draw_icon(sz)
        path = f"icon-{sz}.png"
        out.save(path, optimize=True)
        print(f"saved {path}  ({out.size})")
from PIL import Image, ImageDraw

S = 1024
R = 230

def make_icon(name, draw_fn):
    # 1) gradient bg
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    c1, c2 = (24, 29, 38), (8, 11, 16)
    for y in range(S):
        t = y / S
        r = int(c1[0] + (c2[0] - c1[0]) * t)
        g = int(c1[1] + (c2[1] - c1[1]) * t)
        b = int(c1[2] + (c2[2] - c1[2]) * t)
        d.line([(0, y), (S, y)], fill=(r, g, b, 255))

    # 2) elements
    draw_fn(d, S)

    # 3) rounded mask
    mask = Image.new("L", (S, S), 0)
    md = ImageDraw.Draw(mask)
    md.rounded_rectangle([0, 0, S, S], radius=R, fill=255)

    # 4) composite
    out = Image.composite(img, Image.new("RGBA", (S, S), (0, 0, 0, 0)), mask)
    out.save(name)
    out.resize((192, 192), Image.LANCZOS).save(name.replace("512", "192"))


def cand_A(d, N):
    # green up candle
    gw = int(N * 0.085)
    top = int(N * 0.34)
    bot = int(N * 0.64)
    gx = int(N * 0.40)
    d.rectangle([gx - gw, top, gx + gw, bot], fill=(14, 203, 129, 255))
    d.line([(gx, int(N * 0.22)), (gx, int(N * 0.78))],
           fill=(14, 203, 129, 255), width=int(N * 0.018))

    # red down candle
    rw = int(N * 0.085)
    rh_top = int(N * 0.44)
    rh_bot = int(N * 0.70)
    rx = int(N * 0.60)
    d.rectangle([rx - rw, rh_top, rx + rw, rh_bot], fill=(246, 70, 93, 255))
    d.line([(rx, int(N * 0.34)), (rx, int(N * 0.82))],
           fill=(246, 70, 93, 255), width=int(N * 0.018))

    # yellow trend line
    d.line([(int(N * 0.20), int(N * 0.72)),
            (int(N * 0.50), int(N * 0.40)),
            (int(N * 0.80), int(N * 0.26))],
           fill=(240, 185, 11, 255), width=int(N * 0.022), joint="curve")


def coin_B(d, N):
    c = N // 2
    rad = int(N * 0.32)
    # yellow coin
    d.ellipse([c - rad, c - rad, c + rad, c + rad], fill=(240, 185, 11, 255))
    # inner lighter ring
    d.ellipse([c - rad + int(N * 0.03), c - rad + int(N * 0.03),
               c + rad - int(N * 0.03), c + rad - int(N * 0.03)],
              fill=(245, 200, 60, 255))
    # green up arrow
    w = int(N * 0.10)
    hw = int(N * 0.20)
    hh = int(N * 0.16)
    ay_top = int(N * 0.34)
    ay_bot = int(N * 0.66)
    arrow = [
        (c - w, ay_bot), (c - w, ay_top + hh), (c - hw, ay_top + hh),
        (c, ay_top), (c + hw, ay_top + hh), (c + w, ay_top + hh), (c + w, ay_bot)
    ]
    d.polygon(arrow, fill=(14, 203, 129, 255))


make_icon("icon-A-512.png", cand_A)
make_icon("icon-B-512.png", coin_B)
print("done")

from PIL import Image, ImageDraw

S = 1024
R = 230  # corner radius

def rounded_mask(size, radius):
    m = Image.new("L", (size, size), 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, size, size], radius=radius, fill=255)
    return m

def gradient(size, c1, c2, angle="vert"):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    r1, g1, b1 = c1
    r2, g2, b2 = c2
    for y in range(size):
        for x in range(size):
            t = (y / size) if angle == "vert" else (x / size)
            r = int(r1 + (r2 - r1) * t)
            g = int(g1 + (g2 - g1) * t)
            b = int(b1 + (b2 - b1) * t)
            d.point((x, y), fill=(r, g, b, 255))
    return img

def make_icon(name):
    # 1) dark rounded bg
    bg = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(bg)
    c1, c2 = (24, 29, 38), (8, 11, 16)
    for y in range(S):
        t = y / S
        r = int(c1[0] + (c2[0] - c1[0]) * t)
        g = int(c1[1] + (c2[1] - c1[1]) * t)
        b = int(c1[2] + (c2[2] - c1[2]) * t)
        d.line([(0, y), (S, y)], fill=(r, g, b, 255))

    cx, cy = S // 2, S // 2
    c_r = int(S * 0.32)          # white circle radius
    ring_w = int(S * 0.018)      # gradient ring thickness

    grad = gradient(S, (0, 198, 255), (255, 60, 172), "vert")

    # 2) white circle base
    circle_mask = Image.new("L", (S, S), 0)
    cd = ImageDraw.Draw(circle_mask)
    cd.ellipse([cx - c_r, cy - c_r, cx + c_r, cy + c_r], fill=255)
    white = Image.new("RGBA", (S, S), (245, 247, 250, 255))
    bg = Image.composite(white, bg, circle_mask)

    # 3) B shape mask
    bm = Image.new("L", (S, S), 0)
    bd = ImageDraw.Draw(bm)

    # B proportions
    w = int(c_r * 1.75)
    h = int(c_r * 2.15)
    left = cx - w // 2
    top = cy - h // 2
    right = left + w
    bottom = top + h
    bar_w = int(w * 0.20)
    mid_y1 = cy - int(h * 0.08)
    mid_y2 = cy + int(h * 0.08)

    # left vertical stroke
    bd.rectangle([left, top, left + bar_w, bottom], fill=255)

    # top right lobe
    tr_h = mid_y1 - top
    tr_r = tr_h // 2
    bd.rectangle([left + bar_w - 2, top, right - tr_r, mid_y1], fill=255)
    bd.ellipse([right - 2 * tr_r, top, right, mid_y1], fill=255)

    # bottom right lobe
    br_h = bottom - mid_y2
    br_r = br_h // 2
    bd.rectangle([left + bar_w - 2, mid_y2, right - br_r, bottom], fill=255)
    bd.ellipse([right - 2 * br_r, mid_y2, right, bottom], fill=255)

    # cutouts
    cut_h = int(h * 0.05)
    cut_x1 = left + int(bar_w * 0.55)
    cut_x2 = right - tr_r
    bd.rectangle([cut_x1, mid_y1 - cut_h // 2, cut_x2, mid_y1 + cut_h // 2], fill=0)
    bd.rectangle([cut_x1, mid_y2 - cut_h // 2, cut_x2, mid_y2 + cut_h // 2], fill=0)

    # apply gradient B onto white circle
    bg = Image.composite(grad, bg, bm)

    # 4) gradient ring around the white circle
    ring_mask = Image.new("L", (S, S), 0)
    rd = ImageDraw.Draw(ring_mask)
    rd.ellipse([cx - c_r, cy - c_r, cx + c_r, cy + c_r], fill=255)
    rd.ellipse([cx - c_r + ring_w, cy - c_r + ring_w, cx + c_r - ring_w, cy + c_r - ring_w], fill=0)
    bg = Image.composite(grad, bg, ring_mask)

    # 5) final rounded mask
    out = Image.composite(bg, Image.new("RGBA", (S, S), (0, 0, 0, 0)), rounded_mask(S, R))
    out.save(name)
    out.resize((192, 192), Image.LANCZOS).save(name.replace("512", "192"))


make_icon("icon-C-512.png")
print("done")

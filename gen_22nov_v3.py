#!/usr/bin/env python3
"""Front page v3 for Sunday 22 November 2026 (1024x1024 PNG).

Rebuild following the top-10 leaderboard pattern (GLM analysis of the
10 best entries): a giant serif DATE masthead, a red serif deck, a
DAY IN NUMBERS row, region tabs, a THE DAY IN UTC timeline, 3 hero
cards + 10 medium cards + a numbered ALSO list, a world map whose
pins match ALL story numbers, and a prominent red DATE CHECK box.

32 stories (El Chapo Isidro removed: captured Fri 20 Nov, listed
under DATE CHECK instead). COP31 headline fixed: the deal LANDED
with no fossil-fuel mention. Every story is one of the 33
date-checked stories of v1 — nothing new was added.

Deterministic: fixed fonts, fixed palette, no network, no randomness.
Reads stories_v3.json next to this file and writes entry.png beside it.
Run twice -> byte-identical output.
"""
import json
import math
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = json.load(open(os.path.join(HERE, "stories_v3.json")))

W = H = 1024
PAPER = (247, 242, 231)
INK = (25, 25, 25)
NAVY = (20, 38, 74)
NAVY2 = (28, 52, 96)
AMBER = (232, 163, 23)
RED = (179, 64, 46)
TEAL = (31, 111, 107)
GREEN = (46, 125, 70)
CARD = (255, 255, 255)
LINE = (200, 192, 172)
MUTED = (90, 86, 76)
SKY = (168, 205, 226)
SEA = (44, 92, 140)
OCEAN = (178, 208, 228)
LAND = (232, 222, 196)
BOX = (255, 243, 205)
NIGHT = (12, 22, 44)

PILL_FILL = {"REPORTED": NAVY, "CLAIM": AMBER, "CONFIRMED": GREEN,
             "ONGOING": RED}
PILL_TEXT = {"REPORTED": (255, 255, 255), "CLAIM": (25, 25, 25),
             "CONFIRMED": (255, 255, 255), "ONGOING": (255, 255, 255)}


def font(name, size):
    return ImageFont.truetype(
        "/usr/share/fonts/truetype/dejavu/" + name + ".ttf", size)


def serif_b(s):
    return font("DejaVuSerif-Bold", s)


def sans_b(s):
    return font("DejaVuSans-Bold", s)


def sans(s):
    return font("DejaVuSans", s)


def wrap(draw, text, fnt, width):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit_lines(draw, text, fnt, width, max_lines, bold=True, shrink_to=10):
    size = fnt.size
    while size > shrink_to:
        name = "DejaVuSans-Bold" if bold else "DejaVuSans"
        f = font(name, size)
        lines = wrap(draw, text, f, width)
        if len(lines) <= max_lines:
            return f, lines
        size -= 1
    f = font("DejaVuSans-Bold" if bold else "DejaVuSans", shrink_to)
    lines = wrap(draw, text, f, width)
    if len(lines) > max_lines:
        raise ValueError(
            "text needs %d lines, max %d at min size %d: %r -> %r"
            % (len(lines), max_lines, shrink_to, text, lines))
    return f, lines


def fit_one(draw, text, size, width, bold=True):
    """One line, shrinking to 10pt; fail loudly if it still overflows."""
    while size >= 10:
        name = "DejaVuSans-Bold" if bold else "DejaVuSans"
        f = font(name, size)
        if draw.textlength(text, font=f) <= width:
            return f
        size -= 1
    raise ValueError("one line too long at 10pt (%dpx): %r"
                     % (width, text))


def pill(draw, x, y, text, size=10):
    f = sans_b(size)
    w = draw.textlength(text, font=f) + 10
    draw.rounded_rectangle([x, y, x + w, y + size + 8], radius=3,
                           fill=PILL_FILL[text])
    draw.text((x + 5, y + 4), text, font=f, fill=PILL_TEXT[text])
    return w


def num_badge(draw, x, y, n, r=10):
    draw.ellipse([x, y, x + 2 * r, y + 2 * r], fill=RED)
    draw.ellipse([x, y, x + 2 * r, y + 2 * r], outline=(255, 255, 255), width=1)
    t = str(n)
    f = sans_b(12 if n < 10 else 10)
    tw = draw.textlength(t, font=f)
    draw.text((x + r - tw / 2, y + r - 7), t, font=f, fill=(255, 255, 255))


def burst(d, cx, cy, r, col=(255, 140, 0)):
    pts = []
    for i in range(12):
        a = -math.pi / 2 + i * math.pi / 6
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    d.polygon(pts, fill=col)


def draw_clipped(img, fn, x, y, w, h):
    """Render fn onto a temp layer of exactly (w, h) and paste it, so no
    stroke, arc or burst can escape the illustration box."""
    layer = Image.new("RGB", (w, h))
    ld = ImageDraw.Draw(layer)
    fn(ld, 0, 0, w, h)
    img.paste(layer, (x, y))


# ---------------------------------------------------------------- icons
# Small flat icons for medium cards (same set as v2, proven to render).
def icon_tanker(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    d.rectangle([x, y + h - 24, x + w, y + h], fill=SEA)
    for i in range(4):
        d.arc([x + 10 + i * 26, y + h - 32, x + 32 + i * 26, y + h - 10],
              200, 340, fill=(255, 255, 255), width=3)
    d.polygon([(x + 20, y + 48), (x + w - 20, y + 48), (x + w - 34, y + 70),
               (x + 34, y + 70)], fill=(60, 60, 66))
    for j, col in enumerate((RED, AMBER, TEAL)):
        d.rectangle([x + 30 + j * 26, y + 26, x + 50 + j * 26, y + 48],
                    fill=col)
    d.rectangle([x + w - 44, y + 30, x + w - 26, y + 48], fill=(240, 240, 240))
    cx, cy = x + w - 34, y + 14
    d.polygon([(cx, cy - 11), (cx + 8, cy + 3), (cx + 4, cy + 1),
               (cx + 6, cy + 9), (cx, cy + 3), (cx - 6, cy + 9),
               (cx - 4, cy + 1), (cx - 8, cy + 3)], fill=(255, 140, 0))


def icon_capitol(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(214, 228, 240))
    cx = x + w // 2
    d.pieslice([cx - 32, y + 10, cx + 32, y + 60], 180, 360,
               fill=(255, 255, 255))
    d.rectangle([cx - 38, y + 50, cx + 38, y + 58], fill=(255, 255, 255))
    for i in range(-2, 3):
        d.rectangle([cx + i * 16 - 4, y + 58, cx + i * 16 + 4, y + 82],
                    fill=(255, 255, 255))
    d.rectangle([x + 10, y + 82, x + w - 10, y + 90], fill=(255, 255, 255))
    d.line([cx, y + 4, cx, y + 12], fill=RED, width=3)
    d.polygon([(cx, y + 4), (cx + 12, y + 8), (cx, y + 12)], fill=RED)


def icon_globe(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(18, 60, 80))
    cx, cy, r = x + w // 2, y + h // 2 + 4, 32
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(46, 140, 90))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(255, 255, 255), width=2)
    d.arc([cx - r, cy - r, cx + r, cy + r], 60, 300, fill=(255, 255, 255), width=2)
    d.line([cx, cy - r, cx, cy + r], fill=(255, 255, 255), width=2)
    d.line([cx - r, cy, cx + r, cy], fill=(255, 255, 255), width=2)
    d.ellipse([x + w - 24, y + 10, x + w - 8, y + 26], fill=AMBER)


def icon_ship(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(226, 214, 196))
    d.rectangle([x, y + h - 22, x + w, y + h], fill=SEA)
    d.polygon([(x + 18, y + 52), (x + w - 18, y + 52), (x + w - 30, y + 72),
               (x + 30, y + 72)], fill=(90, 90, 96))
    d.rectangle([x + w // 2 - 4, y + 22, x + w // 2 + 4, y + 52],
                fill=(60, 60, 66))
    d.rectangle([x + w // 2 + 4, y + 24, x + w // 2 + 24, y + 40], fill=RED)
    cx, cy = x + 30, y + 20
    for dx, dy in [(0, -11), (9, -6), (11, 4), (5, 11), (-5, 11), (-11, 4),
                   (-9, -6)]:
        d.line([cx, cy, cx + dx, cy + dy], fill=(255, 140, 0), width=3)


def icon_shield(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(214, 228, 240))
    cx = x + w // 2
    d.polygon([(cx - 28, y + 12), (cx + 28, y + 12), (cx + 28, y + 46),
               (cx, y + 78), (cx - 28, y + 46)], fill=NAVY)
    d.polygon([(cx - 20, y + 19), (cx + 20, y + 19), (cx + 20, y + 44),
               (cx, y + 68), (cx - 20, y + 44)], fill=(255, 255, 255))
    d.text((cx - 7, y + 28), "\u2605", font=sans_b(22), fill=AMBER)


def icon_tennis(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=TEAL)
    cx, cy, r = x + w // 2, y + h // 2, 28
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(190, 220, 60))
    d.arc([cx - r, cy - r, cx + r, cy + r], 300, 60, fill=(255, 255, 255), width=3)
    d.arc([cx - r, cy - r, cx + r, cy + r], 120, 240, fill=(255, 255, 255), width=3)


def icon_badge(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(240, 224, 190))
    cx, cy = x + w // 2, y + h // 2 - 6
    outer = []
    for i in range(10):
        a = -math.pi / 2 + i * math.pi / 5
        rr = 30 if i % 2 == 0 else 15
        outer.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    d.polygon(outer, fill=AMBER)
    d.polygon([(cx - 11, cy + 28), (cx + 11, cy + 28), (cx + 7, cy + 42),
               (cx - 7, cy + 42)], fill=RED)


def icon_target(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(226, 214, 196))
    cx, cy = x + w // 2, y + h // 2
    for r, col in [(32, RED), (22, (255, 255, 255)), (12, RED)]:
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)
    d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=INK)


def icon_ballot(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(214, 228, 240))
    cx, cy = x + w // 2, y + h // 2
    d.rounded_rectangle([cx - 28, cy - 24, cx + 28, cy + 28], radius=4,
                        fill=(255, 255, 255), outline=NAVY, width=2)
    d.line([cx - 20, cy + 2, cx - 7, cy + 15], fill=GREEN, width=5)
    d.line([cx - 7, cy + 15, cx + 22, cy - 16], fill=GREEN, width=5)
    d.rectangle([cx - 28, cy + 32, cx + 28, cy + 36], fill=NAVY)


def icon_flag(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=TEAL)
    cx = x + w // 2
    d.line([cx - 24, y + 14, cx - 24, y + 80], fill=(255, 255, 255), width=3)
    for r in range(3):
        for c in range(4):
            col = INK if (r + c) % 2 == 0 else (255, 255, 255)
            d.rectangle([cx - 22 + c * 11, y + 14 + r * 11,
                         cx - 11 + c * 11, y + 25 + r * 11], fill=col)


def icon_bolt(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(30, 30, 44))
    cx = x + w // 2
    d.polygon([(cx + 8, y + 8), (cx - 14, y + 48), (cx - 2, y + 48),
               (cx - 10, y + 82), (cx + 14, y + 40), (cx + 2, y + 40)],
              fill=AMBER)
    d.ellipse([x + 8, y + h - 16, x + 20, y + h - 4], fill=(255, 255, 255))


def icon_flame(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(40, 26, 22))
    cx, base = x + w // 2, y + h - 12
    d.polygon([(cx, y + 8), (cx + 22, y + 44), (cx + 12, y + 44),
               (cx + 18, y + 62), (cx, base), (cx - 18, y + 62),
               (cx - 12, y + 44), (cx - 22, y + 44)], fill=(255, 110, 20))
    d.polygon([(cx, y + 34), (cx + 11, y + 56), (cx, base),
               (cx - 11, y + 56)], fill=AMBER)


def icon_cross(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=TEAL)
    cx, cy = x + w // 2, y + h // 2
    d.rectangle([cx - 9, cy - 26, cx + 9, cy + 26], fill=(255, 255, 255))
    d.rectangle([cx - 26, cy - 9, cx + 26, cy + 9], fill=(255, 255, 255))
    d.rectangle([x + 8, y + h - 14, x + w - 8, y + h - 8], fill=(255, 255, 255))


# ---------------------------------------------------------------- hero scenes
# Wide flat scenes for the 3 hero cards (box ~313x58). Local coords.

def icon_drones(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=NIGHT)
    # stars
    for sx, sy in [(18, 8), (52, 14), (96, 6), (150, 10), (210, 8),
                   (262, 12), (296, 6), (128, 18), (238, 20)]:
        d.ellipse([x + sx, y + sy, x + sx + 2, y + sy + 2],
                  fill=(255, 255, 255))
    # city skyline
    base = y + h
    for bx, bw, bh in [(0, 34, 26), (36, 26, 34), (64, 30, 22), (96, 24, 30),
                       (122, 34, 26), (158, 28, 36), (188, 30, 24),
                       (220, 26, 32), (248, 30, 22), (280, 33, 28)]:
        d.rectangle([x + bx, base - bh, x + bx + bw, base], fill=(8, 12, 26))
        for wy in range(base - bh + 5, base - 4, 9):
            for wx in range(bx + 5, bx + bw - 4, 9):
                if (wx * 7 + wy * 3) % 11 < 4:
                    d.rectangle([x + wx, wy, x + wx + 3, wy + 4],
                                fill=(255, 200, 90))
    # drones: dark dots with rotor ticks
    for dx, dy in [(70, 12), (150, 8), (235, 14), (195, 20)]:
        d.ellipse([x + dx - 3, y + dy - 2, x + dx + 3, y + dy + 2],
                  fill=(200, 200, 200))
        d.line([x + dx - 6, y + dy - 4, x + dx + 6, y + dy - 4],
               fill=(200, 200, 200), width=1)
    # explosion bursts over the skyline
    burst(d, x + 105, y + 26, 9)
    burst(d, x + 250, y + 22, 7, col=(255, 190, 60))
    d.ellipse([x + 96, y + 32, x + 114, y + 42], fill=(120, 120, 120))
    d.ellipse([x + 242, y + 28, x + 258, y + 38], fill=(120, 120, 120))


def icon_cop31(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(18, 60, 80))
    # globe, centre-left
    cx, cy, r = x + 52, y + h // 2 + 2, 24
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(46, 140, 90))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(255, 255, 255), width=2)
    d.arc([cx - r, cy - r, cx + r, cy + r], 60, 300, fill=(255, 255, 255), width=2)
    d.line([cx, cy - r, cx, cy + r], fill=(255, 255, 255), width=2)
    d.line([cx - r, cy, cx + r, cy], fill=(255, 255, 255), width=2)
    # conference table with delegates
    ty = y + h - 18
    d.rectangle([x + 96, ty, x + w - 8, ty + 10], fill=(120, 82, 40))
    for i, col in enumerate((RED, AMBER, TEAL)):
        fx = x + 120 + i * 58
        d.ellipse([fx - 9, ty - 26, fx + 9, ty - 8], fill=(240, 220, 190))
        d.polygon([(fx - 13, ty - 8), (fx + 13, ty - 8), (fx + 9, ty + 2),
                   (fx - 9, ty + 2)], fill=col)
    # document on the table
    d.rectangle([x + 196, ty - 12, x + 226, ty - 2], fill=(255, 255, 255))
    d.line([x + 200, ty - 9, x + 222, ty - 9], fill=MUTED, width=1)
    d.line([x + 200, ty - 6, x + 222, ty - 6], fill=MUTED, width=1)
    # sun / amber accent
    d.ellipse([x + w - 26, y + 8, x + w - 10, y + 24], fill=AMBER)


def icon_radar(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(30, 30, 44))
    # missile arc across the sky
    d.arc([x + 30, y - 46, x + 300, y + 66], 200, 330, fill=RED, width=3)
    d.ellipse([x + 252, y + 6, x + 258, y + 12], fill=(255, 255, 255))
    burst(d, x + 285, y + 12, 8)
    # two radar dishes
    for dx, dy, s in [(70, 30, 1.0), (170, 34, 0.85)]:
        cx, cy = x + dx, y + dy
        d.pieslice([cx - 22 * s, cy - 20 * s, cx + 22 * s, cy + 20 * s],
                   180, 360, fill=(200, 210, 220))
        d.line([cx, cy, cx, y + h - 8], fill=(200, 210, 220), width=3)
        d.line([cx - 14, y + h - 8, cx + 14, y + h - 8],
               fill=(200, 210, 220), width=3)
        d.line([cx, cy - 16, cx + 12, cy - 26], fill=AMBER, width=2)
    # ground line
    d.line([x, y + h - 6, x + w, y + h - 6], fill=(90, 90, 110), width=2)


ICONS = {"tanker": icon_tanker, "capitol": icon_capitol, "globe": icon_globe,
         "ship": icon_ship, "shield": icon_shield, "tennis": icon_tennis,
         "badge": icon_badge, "target": icon_target, "ballot": icon_ballot,
         "flag": icon_flag, "bolt": icon_bolt, "flame": icon_flame,
         "cross": icon_cross}
HERO_ICONS = {"shield": icon_drones, "globe": icon_cop31,
              "target": icon_radar}

# ---------------------------------------------------------------- map
CONTINENTS = [
    [(0.05, 0.25), (0.10, 0.10), (0.20, 0.08), (0.28, 0.18), (0.30, 0.35),
     (0.24, 0.45), (0.18, 0.55), (0.12, 0.50), (0.06, 0.40)],
    [(0.30, 0.05), (0.34, 0.05), (0.34, 0.14), (0.30, 0.14)],
    [(0.26, 0.55), (0.32, 0.52), (0.36, 0.60), (0.34, 0.75), (0.30, 0.90),
     (0.27, 0.75)],
    [(0.46, 0.12), (0.52, 0.08), (0.56, 0.14), (0.55, 0.24), (0.50, 0.28),
     (0.46, 0.22)],
    [(0.47, 0.32), (0.55, 0.30), (0.60, 0.38), (0.58, 0.55), (0.53, 0.68),
     (0.49, 0.55), (0.46, 0.42)],
    [(0.56, 0.08), (0.70, 0.05), (0.85, 0.10), (0.95, 0.20), (0.92, 0.35),
     (0.85, 0.45), (0.75, 0.50), (0.65, 0.45), (0.58, 0.35), (0.56, 0.20)],
    [(0.82, 0.68), (0.90, 0.66), (0.93, 0.74), (0.88, 0.82), (0.83, 0.76)],
]
MAP_SX, MAP_SY = 1.15, 1.0


def map_xy(px, py):
    mx = 0.5 + (px - 0.5) * MAP_SX
    my = 0.5 + (py - 0.5) * MAP_SY
    return (min(max(mx, 0.02), 0.98), min(max(my, 0.03), 0.97))


# ---------------------------------------------------------------- page
def draw():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 14

    # ---- masthead (0-92): the DATE is the hero, on cream.
    d.text((M, 8), "THE WORLD IN ONE DAY", font=sans_b(13), fill=RED)
    d.text((W - M, 10), "32 STORIES", font=sans_b(22),
           fill=INK, anchor="ra")
    d.text((W - M, 38), "6 REGIONS", font=sans_b(12),
           fill=MUTED, anchor="ra")
    d.text((M, 28), "Sunday 22 November 2026", font=serif_b(44), fill=INK)
    d.rectangle([0, 88, W, 92], fill=RED)

    # ---- red serif deck (96-130)
    deck_lines = wrap(d, DATA["deck"], serif_b(18), W - 2 * M)
    assert len(deck_lines) <= 2, "deck needs %d lines: %r" % (
        len(deck_lines), deck_lines)
    dy = 96
    for ln in deck_lines:
        d.text((M, dy), ln, font=serif_b(18), fill=RED)
        dy += 22

    # ---- DAY IN NUMBERS (134-170)
    ny = 134
    d.rectangle([0, ny, W, ny + 36], fill=NAVY2)
    nums = DATA["numbers"]
    assert len(nums) == 6
    seg = W // len(nums)
    for i, n in enumerate(nums):
        cx = i * seg + seg // 2
        d.text((cx, ny + 2), n["value"], font=sans_b(20), fill=AMBER,
               anchor="ma")
        lab = wrap(d, n["label"].upper(), sans_b(8), seg - 8)
        ly = ny + 24
        for ln in lab[:1]:
            d.text((cx, ly), ln, font=sans_b(8), fill=(200, 210, 230),
                   anchor="ma")

    # ---- region tabs (170-194)
    ty = 170
    d.rectangle([0, ty, W, ty + 24], fill=(255, 255, 255))
    d.rectangle([0, ty + 24, W, ty + 25], fill=LINE)
    regs = DATA["regions"]
    tw = (W - 2 * M) // len(regs)
    for i, r in enumerate(regs):
        x = M + i * tw
        d.text((x + 4, ty + 5), r["name"], font=sans_b(11), fill=NAVY)
        d.text((x + tw - 26, ty + 5), str(r["count"]), font=sans_b(12),
               fill=RED)
        if i:
            d.line([x, ty + 4, x, ty + 20], fill=LINE, width=1)

    # ---- THE DAY IN UTC timeline (194-230), strictly chronological
    ty2 = 194
    d.rectangle([0, ty2, W, ty2 + 36], fill=NAVY)
    d.text((M, ty2 + 11), "THE DAY IN UTC", font=sans_b(11), fill=AMBER)
    tl = DATA["timeline"]
    assert [t["time"] for t in tl] == sorted(t["time"] for t in tl), \
        "timeline not chronological"
    seg2 = (W - 2 * M - 130) // 3
    for i, t in enumerate(tl):
        r, c = divmod(i, 3)
        x = M + 130 + c * seg2
        y = ty2 + 4 + r * 16
        d.text((x, y), t["time"], font=sans_b(10), fill=AMBER)
        d.text((x + 38, y), t["label"], font=sans(10),
               fill=(255, 255, 255))

    # ---- heroes: 3 large cards (236-392)
    y0, lh = 236, 156
    cw = (W - 2 * M - 20) // 3
    for i, st in enumerate(DATA["heroes"]):
        x = M + i * (cw + 10)
        d.rounded_rectangle([x, y0, x + cw, y0 + lh], radius=6, fill=CARD,
                            outline=LINE, width=1)
        draw_clipped(img, HERO_ICONS[st["icon"]], x + 6, y0 + 6, cw - 12, 58)
        num_badge(d, x + 10, y0 + 10, i + 1)
        pw = pill(d, x + 10, y0 + 68, st["pill"], size=9)
        d.text((x + 14 + pw, y0 + 71), st["region"], font=sans_b(9), fill=RED)
        f, lines = fit_lines(d, st["headline"], sans_b(16), cw - 20, 2)
        yy = y0 + 88
        for ln in lines:
            d.text((x + 10, yy), ln, font=f, fill=INK)
            yy += f.size + 2
        sf, slines = fit_lines(d, st["sub"], sans(11), cw - 20, 1, bold=False)
        for ln in slines:
            d.text((x + 10, yy), ln, font=sf, fill=MUTED)
            yy += sf.size + 1
        d.text((x + 10, y0 + 142), "\u2014 " + st["source"], font=sans(9),
               fill=MUTED)

    # ---- grid: 10 medium cards, 5 x 2 (400-592)
    y1, ih = 400, 92
    tw5 = (W - 2 * M - 24) // 5
    for i, st in enumerate(DATA["grid"]):
        r, c = divmod(i, 5)
        x = M + c * (tw5 + 6)
        y = y1 + r * (ih + 8)
        d.rounded_rectangle([x, y, x + tw5, y + ih], radius=6, fill=CARD,
                            outline=LINE, width=1)
        draw_clipped(img, ICONS[st["icon"]], x + 5, y + 5, 56, ih - 10)
        num_badge(d, x + 8, y + 8, i + 4, r=9)
        tx = x + 66
        pw = pill(d, tx, y + 6, st["pill"], size=8)
        d.text((tx + pw + 4, y + 8), st["region"], font=sans_b(8), fill=RED)
        f, lines = fit_lines(d, st["headline"], sans_b(11), tw5 - 74, 3)
        yy = y + 24
        for ln in lines:
            d.text((tx, yy), ln, font=f, fill=INK)
            yy += f.size + 1
        sf, slines = fit_lines(d, st["sub"], sans(9), tw5 - 74, 2, bold=False)
        for ln in slines:
            d.text((tx, yy), ln, font=sf, fill=MUTED)
            yy += sf.size + 1
        d.text((tx, y + 80), "\u2014 " + st["source"], font=sans(8),
               fill=MUTED)

    # ---- world map, all 32 pins (600-730)
    my = 600
    d.text((M, my), "WHERE IT HAPPENED", font=sans_b(13), fill=NAVY)
    d.text((W - M, my), "pins 1\u201332 match the story numbers",
           font=sans(11), fill=MUTED, anchor="ra")
    mx, mw, mh = M, W - 2 * M, 110
    my0 = my + 20
    d.rectangle([mx, my0, mx + mw, my0 + mh], fill=OCEAN, outline=LINE)
    for poly in CONTINENTS:
        pts = [(mx + map_xy(px, py)[0] * mw,
                my0 + map_xy(px, py)[1] * mh) for px, py in poly]
        d.polygon(pts, fill=LAND, outline=(180, 170, 140))
    ux1, uy1 = map_xy(0.565, 0.06)
    ux2, uy2 = map_xy(0.585, 0.34)
    d.line([(mx + ux1 * mw, my0 + uy1 * mh),
            (mx + ux2 * mw, my0 + uy2 * mh)],
           fill=(150, 138, 105), width=2)
    all_cards = DATA["heroes"] + DATA["grid"] + DATA["also"]
    assert len(all_cards) == 32
    pts = []
    for st in all_cards:
        qx, qy = map_xy(*st["pin"])
        pts.append([mx + qx * mw, my0 + qy * mh])
    orig = [p[:] for p in pts]
    # declutter: push overlapping pins apart, capped at 14px from home
    for _ in range(40):
        moved = False
        for i in range(len(pts)):
            for j in range(i + 1, len(pts)):
                dx = pts[j][0] - pts[i][0]
                dy = pts[j][1] - pts[i][1]
                dist = math.hypot(dx, dy)
                if 0 < dist < 14:
                    push = (14 - dist) / 2
                    ux, uy = dx / dist, dy / dist
                    pts[i][0] -= ux * push
                    pts[i][1] -= uy * push
                    pts[j][0] += ux * push
                    pts[j][1] += uy * push
                    moved = True
        if not moved:
            break
    for i, p in enumerate(pts):
        dx, dy = p[0] - orig[i][0], p[1] - orig[i][1]
        d0 = math.hypot(dx, dy)
        if d0 > 14:
            p[0] = orig[i][0] + dx / d0 * 14
            p[1] = orig[i][1] + dy / d0 * 14
        p[0] = min(max(p[0], mx + 6), mx + mw - 6)
        p[1] = min(max(p[1], my0 + 6), my0 + mh - 6)
    for i, (cx, cy) in enumerate(pts):
        d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=RED,
                  outline=(255, 255, 255), width=1)
        t = str(i + 1)
        f = sans_b(8 if i + 1 < 10 else 7)
        tw = d.textlength(t, font=f)
        d.text((cx - tw / 2, cy - 5), t, font=f, fill=(255, 255, 255))

    # ---- ALSO ON SUNDAY, 19 items in 2 columns (738-898)
    ay = 738
    d.text((M, ay), "ALSO ON SUNDAY", font=sans_b(13), fill=NAVY)
    d.text((W - M, ay), "14\u201332  \u00b7  status in grey",
           font=sans(11), fill=MUTED, anchor="ra")
    col_w = (W - 2 * M - 20) // 2
    for i, st in enumerate(DATA["also"]):
        c, r = divmod(i, 10)
        x = M + c * (col_w + 20)
        y = ay + 20 + r * 14
        d.text((x, y), str(14 + i) + ".", font=sans_b(11), fill=RED)
        hl = st["headline"]
        loc = st["loc"]
        if hl.lower().startswith(loc.lower()):
            rest = hl[len(loc):].lstrip(": ").strip()
            if rest:
                hl = rest[0].upper() + rest[1:]
        line = "%s \u2014 %s (%s)" % (loc, hl, st["source"])
        f = fit_one(d, line, 11, col_w - 90, bold=False)
        d.text((x + 26, y), line, font=f, fill=INK)
        hw = d.textlength(line, font=f)
        d.text((x + 26 + hw + 6, y + 1), st["pill"], font=sans_b(8),
               fill=MUTED)

    # ---- DATE CHECK red box (906-996)
    dy = 906
    d.rectangle([0, dy, W, dy + 90], fill=BOX)
    d.rectangle([0, dy, W, dy + 90], outline=RED, width=2)
    d.text((M, dy + 5), "DATE CHECK \u2014 LEFT OUT ON PURPOSE (NOT 22 NOVEMBER):",
           font=sans_b(11), fill=RED)
    parts = ["%s \u2014 %s" % (e["story"], e["date"])
             for e in DATA["date_check_excluded"]]
    dc = "  \u00b7  ".join(parts)
    f, lines = fit_lines(d, dc, sans(10), W - 2 * M, 3, bold=False)
    yy = dy + 21
    for ln in lines:
        d.text((M, yy), ln, font=f, fill=INK)
        yy += f.size + 1
    yy += 4
    d.text((M, yy),
           "TODAY'S VERIFIED COUNT: 186 drones launched; 161 downed",
           font=sans_b(10), fill=RED)
    yy += 11
    pending = ("NOT DECIDED ON SUNDAY: " +
               " \u00b7 ".join(DATA["date_check_pending"]))
    assert d.textlength(pending, font=sans_b(10)) <= W - 2 * M, \
        "pending line too long: %r" % pending
    d.text((M, yy), pending, font=sans_b(10), fill=RED)
    yy += 11
    d.text((M, yy),
           "Sources: Reuters, AP, BBC, Al Jazeera, CNN, Ukrainian Air Force, "
           "RFE/RL  \u00b7  REPORTED = carried by the day's wires \u00b7  "
           "CLAIM = one side's account",
           font=sans(9), fill=INK)
    assert yy + 10 <= dy + 90, "DATE CHECK overflows box"

    # ---- footer (1000-1024): tag legend + count line
    d.text((M, 1000),
           "HOW TO READ THE TAGS:  CONFIRMED = 2+ outlets  \u00b7  "
           "REPORTED = carried by the day's wires  \u00b7  "
           "CLAIM = one side's account  \u00b7  ONGOING = still developing",
           font=sans(9), fill=MUTED)
    d.text((M, 1012),
           "All 32 stories happened or were first reported Sunday "
           "22 Nov 2026 \u00b7 Every story names its outlet. "
           "Pictures and map: original.",
           font=sans(10), fill=MUTED)
    return img


def main():
    img = draw()
    out = os.path.join(HERE, "entry.png")
    img.save(out, format="PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()

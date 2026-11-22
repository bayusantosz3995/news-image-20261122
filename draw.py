#!/usr/bin/env python3
"""Draw the news-image-20261122 entry: a one-page newspaper front page
summing up the world's news of Sunday 22 November 2026.

Run:  python3 draw.py
Writes entry.png (1024x1024, under 1 MiB) next to this file.

The graded entrypoint (main.py) only copies entry.png into /output,
because the grading sandbox has no network and no Pillow; this script
is the program that drew the image, kept in the repository so the
build is transparent. All artwork is drawn here in code with Pillow
primitives; no photos or external images are used.

Stories (all reported on 22 Nov 2026, cross-checked across several
news sources): the Gulf escalation (Iran strikes Bahrain, tankers hit
near Hormuz), Mexico's capture of cartel boss "El Chapo Isidro",
COP31 running into overtime in Antalya, the Trump-Xi-Putin meeting in
Shenzhen, the AI-led stock sell-off, the Russian missile strike on
Kryvyi Rih, and Leeds stunning Chelsea 4-1.
"""

import math
import os
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
W, H = 1024, 1024

# ---- palette ---------------------------------------------------------
PAPER = (246, 241, 227)      # warm newsprint
INK = (26, 26, 26)
NAVY = (18, 38, 58)          # masthead
RED = (179, 38, 30)          # date band, kickers
GOLD = (201, 162, 39)        # masthead accent
WHITE = (255, 255, 255)
PANEL = (255, 255, 255)
RULE = (26, 26, 26)
MUTED = (90, 86, 74)
SEA = (23, 68, 96)           # gulf map water
LAND = (214, 196, 150)       # gulf map land
FLAME = (242, 140, 40)
FLAME2 = (228, 87, 46)
GREEN = (27, 94, 60)         # sport strip
SKY = (43, 58, 85)           # ukraine panel sky

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_MAST = font("DejaVuSerif-Bold.ttf", 56)
F_MAST_SMALL = font("DejaVuSans-Bold.ttf", 14)
F_DATE = font("DejaVuSans-Bold.ttf", 36)
F_DATE_SIDE = font("DejaVuSans-Bold.ttf", 13)
F_LEAD = font("DejaVuSerif-Bold.ttf", 44)
F_LEAD_DECK = font("DejaVuSerif.ttf", 21)
F_FACT = font("DejaVuSans.ttf", 15)
F_KICK = font("DejaVuSans-Bold.ttf", 14)
F_H2 = font("DejaVuSerif-Bold.ttf", 27)
F_DECK2 = font("DejaVuSerif.ttf", 16)
F_H3 = font("DejaVuSerif-Bold.ttf", 21)
F_DECK3 = font("DejaVuSerif.ttf", 14)
F_SPORT = font("DejaVuSans-Bold.ttf", 18)
F_TICK = font("DejaVuSans.ttf", 14)
F_TICK_B = font("DejaVuSans-Bold.ttf", 14)
F_FOOT = font("DejaVuSans.ttf", 11)
F_MAP = font("DejaVuSans-Bold.ttf", 13)
F_MAP_S = font("DejaVuSans.ttf", 11)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def star_points(cx, cy, r_out, r_in, points=5, rot=-90.0):
    pts = []
    for i in range(points * 2):
        r = r_out if i % 2 == 0 else r_in
        ang = math.radians(rot + i * 180.0 / points)
        pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    return pts


def spaced(text, gap=" "):
    """Letterspaced caps for small labels."""
    return gap.join(list(text.replace(" ", "  ")))


# ---- illustrations (all drawn with Pillow primitives) -----------------

def draw_gulf(draw, x0, y0, w, h):
    """Stylised map of the Strait of Hormuz: land, sea, tankers, flames."""
    draw.rectangle([x0, y0, x0 + w, y0 + h], fill=SEA)
    # landmasses (top = Iran, bottom = Oman/UAE peninsula)
    draw.polygon([(x0, y0), (x0 + w, y0), (x0 + w, y0 + 52),
                  (x0 + w * 0.72, y0 + 78), (x0 + w * 0.55, y0 + 60),
                  (x0 + w * 0.38, y0 + 88), (x0 + w * 0.18, y0 + 64),
                  (x0, y0 + 84)], fill=LAND)
    draw.polygon([(x0, y0 + h), (x0 + w, y0 + h), (x0 + w, y0 + h - 46),
                  (x0 + w * 0.80, y0 + h - 74), (x0 + w * 0.62, y0 + h - 52),
                  (x0 + w * 0.40, y0 + h - 80), (x0 + w * 0.22, y0 + h - 56),
                  (x0, y0 + h - 70)], fill=LAND)
    # the strait: a lighter channel between the landmasses
    draw.polygon([(x0 + w * 0.47, y0 + 66), (x0 + w * 0.58, y0 + 74),
                  (x0 + w * 0.56, y0 + h - 58), (x0 + w * 0.47, y0 + h - 66)],
                 fill=(64, 130, 165))
    # tanker 1 (left, in the Gulf)
    tx, ty = x0 + 96, y0 + 138
    draw.rectangle([tx, ty, tx + 120, ty + 26], fill=(30, 30, 30))
    draw.rectangle([tx + 88, ty - 18, tx + 112, ty], fill=(30, 30, 30))
    draw.rectangle([tx, ty + 8, tx + 120, ty + 14], fill=RED)
    # tanker 2 (right, in the strait) with flames
    tx2, ty2 = x0 + 330, y0 + 168
    draw.rectangle([tx2, ty2, tx2 + 130, ty2 + 28], fill=(30, 30, 30))
    draw.rectangle([tx2 + 12, ty2 - 18, tx2 + 36, ty2], fill=(30, 30, 30))
    draw.rectangle([tx2, ty2 + 9, tx2 + 130, ty2 + 15], fill=RED)
    for fx, fy, s in [(tx2 + 60, ty2 - 6, 26), (tx2 + 88, ty2 - 2, 20),
                      (tx2 + 110, ty2 - 8, 16)]:
        draw.polygon(star_points(fx, fy, s, s * 0.45, points=6),
                     fill=FLAME)
        draw.ellipse([fx - s * 0.4, fy - s * 0.4, fx + s * 0.4, fy + s * 0.4],
                     fill=(255, 214, 90))
    # missile arcs (dashed red curves) from the top landmass
    for (ax, ay, bx, by) in [(x0 + 210, y0 + 70, tx + 60, ty - 4),
                             (x0 + 430, y0 + 66, tx2 + 70, ty2 - 10)]:
        mx, my = (ax + bx) / 2, min(ay, by) - 46
        steps = 24
        prev = None
        for i in range(steps + 1):
            t = i / steps
            px = (1 - t) ** 2 * ax + 2 * (1 - t) * t * mx + t ** 2 * bx
            py = (1 - t) ** 2 * ay + 2 * (1 - t) * t * my + t ** 2 * by
            if prev and (i % 2 == 0):
                draw.line([prev, (px, py)], fill=RED, width=3)
            prev = (px, py)
        draw.polygon([(bx, by), (bx - 10, by - 2), (bx - 2, by - 10)],
                     fill=RED)
    # Bahrain marker (left edge, in the Gulf)
    bx, by = x0 + 52, y0 + 208
    draw.ellipse([bx - 7, by - 7, bx + 7, by + 7], fill=RED,
                 outline=WHITE, width=2)
    draw.text((bx + 12, by - 9), "BAHRAIN", font=F_MAP, fill=WHITE)
    draw.text((x0 + 20, y0 + 100), "STRAIT OF HORMUZ",
              font=F_MAP_S, fill=(190, 220, 235))
    draw.text((x0 + w - 118, y0 + 14), "GULF REGION",
              font=F_MAP_S, fill=(120, 105, 70))
    # small flame at Bahrain
    draw.polygon(star_points(bx, by - 22, 12, 5, points=6), fill=FLAME)


def draw_badge(draw, x0, y0, w, h):
    """Sheriff star + handcuffs on a dark panel."""
    draw.rectangle([x0, y0, x0 + w, y0 + h], fill=(32, 32, 40))
    cx, cy = x0 + w // 2, y0 + 52
    draw.polygon(star_points(cx, cy, 34, 14, points=5), fill=GOLD,
                 outline=(140, 110, 20))
    draw.ellipse([cx - 12, cy - 12, cx + 12, cy + 12], fill=(32, 32, 40))
    draw.text((cx - 5, cy - 9), "$", font=F_MAP, fill=GOLD)
    # handcuffs: two rings + chain
    ry = y0 + h - 34
    for rx in (x0 + w // 2 - 30, x0 + w // 2 + 30):
        draw.ellipse([rx - 15, ry - 15, rx + 15, ry + 15],
                     outline=(200, 200, 210), width=5)
    for i in range(3):
        lx = x0 + w // 2 - 12 + i * 12
        draw.ellipse([lx - 4, ry - 4, lx + 4, ry + 4],
                     outline=(200, 200, 210), width=2)
    draw.text((x0 + 10, y0 + h - 16), "SINALOA, MEXICO",
              font=F_MAP_S, fill=(170, 170, 180))


def draw_globe(draw, x0, y0, w, h):
    """A globe under a rising sun for the climate talks."""
    draw.rectangle([x0, y0, x0 + w, y0 + h], fill=(214, 236, 244))
    # sun
    sx, sy = x0 + w - 26, y0 + 26
    for i in range(8):
        ang = math.radians(i * 45)
        draw.line([(sx + 16 * math.cos(ang), sy + 16 * math.sin(ang)),
                   (sx + 26 * math.cos(ang), sy + 26 * math.sin(ang))],
                  fill=FLAME, width=3)
    draw.ellipse([sx - 14, sy - 14, sx + 14, sy + 14], fill=FLAME)
    # globe
    cx, cy, r = x0 + w // 2 - 6, y0 + h // 2 + 8, 52
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(64, 130, 180),
                 outline=NAVY, width=2)
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=NAVY, width=2)
    draw.arc([cx - r, cy - r, cx + r, cy + r], start=90, end=270,
             fill=NAVY, width=2)
    draw.arc([cx - r // 2, cy - r, cx + r // 2, cy + r], start=90, end=270,
             fill=NAVY, width=2)
    draw.line([cx - r, cy, cx + r, cy], fill=NAVY, width=2)
    # land blobs
    draw.ellipse([cx - 34, cy - 30, cx - 6, cy - 8], fill=(96, 160, 90))
    draw.ellipse([cx + 2, cy + 6, cx + 34, cy + 30], fill=(96, 160, 90))
    draw.ellipse([cx - 12, cy + 14, cx + 10, cy + 34], fill=(96, 160, 90))
    draw.text((x0 + 10, y0 + h - 16), "ANTALYA, TURKEY",
              font=F_MAP_S, fill=(60, 90, 110))


def draw_flags(draw, x0, y0, w, h):
    """Three flag panels: US, China, Russia."""
    fw = w // 3
    # USA
    ux = x0
    for i in range(7):
        draw.rectangle([ux, y0 + i * h // 7, ux + fw, y0 + (i + 1) * h // 7],
                       fill=RED if i % 2 == 0 else WHITE)
    draw.rectangle([ux, y0, ux + fw * 0.45, y0 + h * 4 // 7], fill=NAVY)
    for r in range(3):
        for c in range(3):
            px = ux + 6 + c * 9
            py = y0 + 6 + r * 9
            draw.ellipse([px, py, px + 3, py + 3], fill=WHITE)
    # China
    cx = x0 + fw
    draw.rectangle([cx, y0, cx + fw, y0 + h], fill=(222, 41, 16))
    draw.polygon(star_points(cx + 16, y0 + 18, 11, 4.5), fill=(255, 222, 0))
    for sx, sy in [(cx + 34, y0 + 10), (cx + 40, y0 + 20), (cx + 34, y0 + 30)]:
        draw.polygon(star_points(sx, sy, 5, 2), fill=(255, 222, 0))
    # Russia
    rx = x0 + 2 * fw
    draw.rectangle([rx, y0, rx + fw, y0 + h // 3], fill=WHITE)
    draw.rectangle([rx, y0 + h // 3, rx + fw, y0 + 2 * h // 3],
                   fill=(0, 82, 164))
    draw.rectangle([rx, y0 + 2 * h // 3, rx + fw, y0 + h], fill=(213, 0, 50))
    draw.rectangle([x0, y0, x0 + w, y0 + h], outline=INK, width=1)


def draw_chart(draw, x0, y0, w, h):
    """A falling stock chart in red."""
    draw.rectangle([x0, y0, x0 + w, y0 + h], fill=WHITE)
    draw.rectangle([x0, y0, x0 + w, y0 + h], outline=INK, width=1)
    # gridlines
    for i in range(1, 4):
        gy = y0 + i * h // 4
        draw.line([(x0 + 6, gy), (x0 + w - 6, gy)], fill=(225, 225, 225),
                  width=1)
    pts = [(x0 + 10, y0 + 14), (x0 + w * 0.30, y0 + 26),
           (x0 + w * 0.48, y0 + 22), (x0 + w * 0.66, y0 + 44),
           (x0 + w * 0.84, y0 + 50), (x0 + w - 12, y0 + h - 8)]
    draw.line(pts, fill=RED, width=4, joint="curve")
    draw.polygon([(pts[-1][0], pts[-1][1]), (pts[-1][0] - 12, pts[-1][1] - 2),
                  (pts[-1][0] - 2, pts[-1][1] - 12)], fill=RED)
    draw.text((x0 + 10, y0 + h - 24), "S&P 500  -3.7%", font=F_MAP, fill=RED)


def draw_skyline(draw, x0, y0, w, h):
    """A city skyline at night, a missile streak and an explosion."""
    draw.rectangle([x0, y0, x0 + w, y0 + h], fill=SKY)
    # stars
    for sx, sy in [(x0 + 18, y0 + 12), (x0 + 60, y0 + 22), (x0 + 110, y0 + 10),
                   (x0 + 150, y0 + 26), (x0 + 200, y0 + 14),
                   (x0 + 240, y0 + 24)]:
        draw.ellipse([sx, sy, sx + 3, sy + 3], fill=(220, 225, 240))
    # buildings
    heights = [52, 78, 44, 92, 60, 84, 48, 70]
    bw = w // len(heights)
    for i, bh in enumerate(heights):
        bx = x0 + i * bw
        draw.rectangle([bx + 2, y0 + h - bh, bx + bw - 2, y0 + h],
                       fill=(20, 26, 38))
        for wy in range(y0 + h - bh + 8, y0 + h - 8, 14):
            for wx in range(bx + 6, bx + bw - 8, 10):
                draw.rectangle([wx, wy, wx + 4, wy + 5],
                               fill=(255, 210, 110))
    # missile streak
    draw.line([(x0 + w - 30, y0 + 12), (x0 + w - 90, y0 + 58)],
              fill=(255, 240, 200), width=3)
    draw.line([(x0 + w - 90, y0 + 58), (x0 + w - 130, y0 + 78)],
              fill=FLAME, width=5)
    # explosion starburst over a rooftop
    ex, ey = x0 + w - 128, y0 + h - 96
    draw.polygon(star_points(ex, ey, 22, 8, points=8), fill=FLAME)
    draw.polygon(star_points(ex, ey, 12, 5, points=8), fill=(255, 214, 90))


def draw_football(draw, cx, cy, r):
    """A simple football: white ball with black patches."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=WHITE,
                 outline=INK, width=2)
    draw.polygon(star_points(cx, cy, r * 0.42, r * 0.42, points=5),
                 fill=INK)
    for ang in (200, 250, 290, 340, 20, 70, 110, 160):
        a = math.radians(ang)
        px, py = cx + r * 0.78 * math.cos(a), cy + r * 0.78 * math.sin(a)
        draw.polygon(star_points(px, py, r * 0.22, r * 0.22, points=5),
                     fill=INK)


# ---- page ----------------------------------------------------------------

def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 24                      # side margin
    cw = W - 2 * mx              # content width

    # ===== masthead =====
    d.rectangle([0, 0, W, 104], fill=NAVY)
    tag = spaced("THE WORLD'S NEWS IN ONE PAGE")
    tw = d.textlength(tag, font=F_MAST_SMALL)
    d.text(((W - tw) / 2, 10), tag, font=F_MAST_SMALL, fill=GOLD)
    title = "The Sunday Globe"
    tw = d.textlength(title, font=F_MAST)
    d.text(((W - tw) / 2, 30), title, font=F_MAST, fill=WHITE)
    d.line([(mx, 104), (W - mx, 104)], fill=GOLD, width=3)

    # ===== date band =====
    d.rectangle([0, 107, W, 152], fill=RED)
    date = "SUNDAY, 22 NOVEMBER 2026"
    tw = d.textlength(date, font=F_DATE)
    d.text(((W - tw) / 2, 114), date, font=F_DATE, fill=WHITE)
    d.text((mx + 4, 122), "ONE DAY", font=F_DATE_SIDE, fill=(255, 220, 215))
    side = "THE WHOLE WORLD"
    tw = d.textlength(side, font=F_DATE_SIDE)
    d.text((W - mx - 4 - tw, 122), side, font=F_DATE_SIDE,
           fill=(255, 220, 215))

    # ===== lead story: the Gulf =====
    ly = 168
    lh = 292
    lw = 576
    draw_gulf(d, mx, ly, lw, lh)
    d.rectangle([mx, ly, mx + lw, ly + lh], outline=INK, width=2)
    tx = mx + lw + 20
    twd = W - mx - tx
    d.text((tx, ly + 2), "MIDDLE EAST  •  CONFLICT", font=F_KICK, fill=RED)
    d.text((tx, ly + 26), "GULF IN", font=F_LEAD, fill=INK)
    d.text((tx, ly + 76), "FLAMES", font=F_LEAD, fill=INK)
    deck = ("Iran strikes a Bahrain industrial site; two oil tankers "
            "hit near the Strait of Hormuz.")
    y = ly + 132
    for line in wrap(d, deck, F_LEAD_DECK, twd):
        d.text((tx, y), line, font=F_LEAD_DECK, fill=INK)
        y += 26
    y += 8
    facts = [
        "Houthi missiles fired at Riyadh intercepted",
        "Saudi jets strike Yemen's port of Hodeidah",
        "Tehran: reopening Hormuz \"not difficult\"",
    ]
    for fact in facts:
        d.ellipse([tx, y + 5, tx + 7, y + 12], fill=RED)
        for line in wrap(d, fact, F_FACT, twd - 16):
            d.text((tx + 14, y), line, font=F_FACT, fill=(40, 40, 40))
            y += 19
        y += 4

    # ===== row 2: Mexico + COP31 =====
    ry = 476
    rh = 196
    rw = (cw - 16) // 2
    # --- Mexico ---
    x = mx
    d.rounded_rectangle([x, ry, x + rw, ry + rh], radius=6, fill=PANEL,
                        outline=RULE, width=1)
    draw_badge(d, x + 12, ry + 34, 118, rh - 46)
    tx2 = x + 142
    d.text((tx2, ry + 12), "MEXICO  •  JUSTICE", font=F_KICK, fill=RED)
    y = ry + 34
    for line in wrap(d, "“El Chapo Isidro” captured", F_H2, rw - 154):
        d.text((tx2, y), line, font=F_H2, fill=INK)
        y += 32
    y += 2
    for line in wrap(d, "FBI most-wanted cartel boss seized in a Sinaloa "
                      "raid; 11 killed in the firefight.",
                     F_DECK2, rw - 154):
        d.text((tx2, y), line, font=F_DECK2, fill=(40, 40, 40))
        y += 21
    # --- COP31 ---
    x = mx + rw + 16
    d.rounded_rectangle([x, ry, x + rw, ry + rh], radius=6, fill=PANEL,
                        outline=RULE, width=1)
    draw_globe(d, x + 12, ry + 34, 118, rh - 46)
    tx2 = x + 142
    d.text((tx2, ry + 12), "CLIMATE  •  ANTALYA", font=F_KICK, fill=RED)
    y = ry + 34
    for line in wrap(d, "COP31 talks run into overtime", F_H2, rw - 154):
        d.text((tx2, y), line, font=F_H2, fill=INK)
        y += 32
    y += 2
    for line in wrap(d, "Draft deal omits fossil fuels; summit enters a "
                      "second day of overtime.", F_DECK2, rw - 154):
        d.text((tx2, y), line, font=F_DECK2, fill=(40, 40, 40))
        y += 21

    # ===== row 3: summit / markets / Ukraine =====
    ry = 688
    rh = 196
    rw = (cw - 32) // 3
    cols = [
        ("DIPLOMACY", "Trump, Xi, Putin meet in Shenzhen",
         "Leaders agree to open nuclear risk-reduction talks.",
         draw_flags),
        ("MARKETS", "AI sell-off sinks stocks",
         "S&P 500 −3.7%, Nikkei −5.1% as chip shares plunge.",
         draw_chart),
        ("WAR IN UKRAINE", "Missile hits Zelensky's hometown",
         "2 killed, dozens hurt in Kryvyi Rih; Russian missiles land in Poland.",
         draw_skyline),
    ]
    for i, (kick, head, deck, art) in enumerate(cols):
        x = mx + i * (rw + 16)
        d.rounded_rectangle([x, ry, x + rw, ry + rh], radius=6, fill=PANEL,
                            outline=RULE, width=1)
        art(d, x + 10, ry + 10, rw - 20, 62)
        d.text((x + 12, ry + 80), kick, font=F_KICK, fill=RED)
        y = ry + 100
        for line in wrap(d, head, F_H3, rw - 24):
            d.text((x + 12, y), line, font=F_H3, fill=INK)
            y += 25
        y += 2
        for line in wrap(d, deck, F_DECK3, rw - 24):
            d.text((x + 12, y), line, font=F_DECK3, fill=(40, 40, 40))
            y += 18

    # ===== sport strip =====
    sy = 896
    d.rounded_rectangle([mx, sy, W - mx, sy + 44], radius=6, fill=GREEN)
    draw_football(d, mx + 30, sy + 22, 15)
    sport = ("SPORT  •  Leeds stun Chelsea 4–1 at Stamford Bridge — "
             "first win there since 1999")
    d.text((mx + 56, sy + 11), sport, font=F_SPORT, fill=WHITE)

    # ===== ticker =====
    ty = 950
    d.text((mx, ty), "ALSO TODAY —", font=F_TICK_B, fill=RED)
    tick = ("Nigeria boat disaster kills 24  •  6.8 quake shakes Peru  •  "
            "FBI crime database hacked  •  India 720/9 v New Zealand  •  "
            "EU–Indonesia sign trade deal")
    tw = d.textlength("ALSO TODAY — ", font=F_TICK_B)
    y = ty
    for line in wrap(d, tick, F_TICK, cw - tw):
        d.text((mx + tw, y), line, font=F_TICK, fill=INK)
        y += 19

    # ===== footer =====
    foot = ("Drawn in code from the day's reporting  •  Reuters  •  BBC  •  "
            "AP  •  The Guardian")
    tw = d.textlength(foot, font=F_FOOT)
    d.text(((W - tw) / 2, H - 22), foot, font=F_FOOT, fill=MUTED)

    out = HERE / "entry.png"
    img.save(out, optimize=True)
    print("wrote", out, img.size, out.stat().st_size, "bytes")


if __name__ == "__main__":
    main()

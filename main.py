"""THE WORLD TODAY - Thursday 19 November 2026.

One front page, one skyline: the day's news as a single dusk panorama
("ONE DAY, ONE SKYLINE") above a numbered 36-story index in two columns
and a "DAY IN NUMBERS" strip. Drawn with Pillow when it is available;
when it is not, the bundled entry.png is copied byte-for-byte.

Standard library only, apart from the optional Pillow import, which is
guarded by try/except. Deterministic: two runs write identical bytes.
No network, no clock, no randomness.
"""

import math
import os
import shutil
import sys

S = 2  # supersample factor: draw at 2048, downsample to 1024
W, H = 1024, 1024

# ---------------------------------------------------------------- palette
PAPER = (246, 241, 227)
PAPER_DIM = (238, 231, 211)
INK = (20, 36, 62)          # deep navy
INK_SOFT = (52, 66, 96)
CREAM = (246, 241, 227)
AMBER = (232, 160, 76)
AMBER_DEEP = (180, 85, 45)
TEAL = (95, 168, 160)
ROSE = (224, 86, 122)
SKY_TOP = (22, 35, 63)
SKY_MID = (64, 62, 88)
SKY_LOW = (180, 85, 45)
SKY_HORIZON = (232, 160, 76)
LABEL_BAR = (16, 28, 52)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SERIF = os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf")
SERIF_REG = os.path.join(FONT_DIR, "DejaVuSerif.ttf")
SANS = os.path.join(FONT_DIR, "DejaVuSans.ttf")
SANS_BOLD = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")

# ---------------------------------------------------------------- data
# 36 stories, verified against reporting dated 19 November 2026.
# (number, headline) grouped by region; two columns of 18.
REGIONS = [
    ("ASIA", (163, 77, 31), [
        (1, "Trump, Xi and Putin hold first trilateral summit in Shenzhen"),
        (2, "ICJ: Myanmar committed genocide against the Rohingya"),
        (3, "Iran drones hit US bases in Kuwait and Bahrain"),
        (4, "Houthi missile damages Riyadh's PIF Tower"),
        (5, "Israel launches ground operation in central Gaza"),
        (6, "Cyclone Akvan nears India's east coast, landfall Friday"),
        (7, "Bangladesh unrest: four killed, Yunus home torched"),
        (8, "North Korea expanding uranium enrichment, IAEA warns"),
        (9, "South Korea court orders retrial for ex-PM Han"),
    ]),
    ("EUROPE", (47, 93, 138), [
        (10, "Ukraine allies meet in Berlin to back Kyiv"),
        (11, "Russian strikes kill five in Ukraine; Kyiv hits Kerch Bridge"),
        (12, "Russian drones damage Dutch, Austrian embassies in Kyiv"),
        (13, "Denmark approves US-Greenland Arctic security deal"),
        (14, "AI cyberattack disrupts European Commission systems"),
        (15, "UK Covid inquiry: late border controls left UK exposed"),
        (16, "COP31 deadlocked on fossil fuels and finance"),
    ]),
    ("AFRICA", (124, 106, 29), [
        (17, "Migrant boat sinks off Senegal; dozens missing"),
        (18, "Somalia expels UAE ambassador over sovereignty row"),
        (19, "Nigeria's APGA endorses Tinubu for 2027"),
        (20, "Ghana minister gives CPR to woman at COP31"),
        (21, "Dakar Youth Games put Africa on Olympic map"),
    ]),
    ("NORTH AMERICA", (74, 107, 79), [
        (22, "Anthropic IPO raises record $107.3bn on Nasdaq debut"),
        (23, "GTA VI launches: 99 Metascore, $1.84bn day one"),
        (24, "Jeffries nominated Speaker 251-11, a first"),
        (25, "Musk: \"I'm not MAGA\", regrets $500m spending"),
        (26, "Trump asks top court to block Venezuelan TPS shield"),
        (27, "Begich keeps Alaska seat; last 2026 race called"),
        (28, "Voyager 1 confirmed one light-day from Earth"),
    ]),
    ("SOUTH AMERICA", (138, 59, 92), [
        (29, "Hegseth visits Colombia, delivers C-130 Hercules"),
        (30, "Hegseth signs military deal in Venezuela"),
        (31, "Colombia arrests 26 Clan del Golfo members"),
        (32, "Flamengo loses Betano shirt deal in betting ban"),
    ]),
    ("OCEANIA", (47, 122, 114), [
        (33, "Australia jobless rate hits 4.9%, five-year high"),
        (34, "Bancroft: whole team knew of ball-tampering plot"),
        (35, "Nicholls ton lifts New Zealand to 243/5 vs India"),
        (36, "Cyclone Xavier threatens Northern Cook Islands"),
    ]),
]

# Eight panorama scenes, left to right across the skyline.
SEGMENTS = [
    ("SHENZHEN SUMMIT", "Trump · Xi · Putin meet", "shenzhen"),
    ("THE HAGUE", "Myanmar guilty", "hague"),
    ("THE GULF", "Iran drones hit US bases", "gulf"),
    ("RIYADH", "Missile hits PIF Tower", "riyadh"),
    ("LEONIDA", "GTA VI launches today", "leonida"),
    ("NASDAQ", "$107bn record IPO", "nasdaq"),
    ("DEEP SPACE", "16 billion miles out", "voyager"),
    ("BAY OF BENGAL", "Storm nears India", "cyclone"),
]

NUMBERS = [
    ("$107.3BN", "Anthropic IPO", "largest ever"),
    ("$1.84BN", "GTA VI day-one", "sales (SensorTower)"),
    ("16BN MILES", "Voyager 1", "one light-day out"),
    ("10,000", "Rohingya killed", "per ICJ estimate"),
    ("90 MIN", "Shenzhen trilateral", "talks, three leaders"),
]

SOURCES = ("SOURCES: USA TODAY · BBC · LE MONDE · REUTERS · NPR · BLOOMBERG · "
           "NASA · ICJ · AP — ALL STORIES FIRST REPORTED 19 NOV 2026")


# ---------------------------------------------------------------- helpers
def _font(path, size):
    from PIL import ImageFont
    try:
        return ImageFont.truetype(path, size * S)
    except Exception:
        return ImageFont.load_default()


def _text_w(draw, text, font):
    return draw.textlength(text, font=font)


def _center(draw, cx, y, text, font, fill):
    w = _text_w(draw, text, font)
    draw.text((cx - w / 2, y), text, font=font, fill=fill)


def _tracked(draw, cx, y, text, font, fill, tracking):
    """Draw text centered with extra letter spacing."""
    widths = [draw.textlength(ch, font=font) for ch in text]
    total = sum(widths) + tracking * max(len(text) - 1, 0)
    x = cx - total / 2
    for ch, w in zip(text, widths):
        draw.text((x, y), ch, font=font, fill=fill)
        x += w + tracking


def _lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def _star(draw, cx, cy, r, fill):
    draw.polygon([(cx, cy - r), (cx + r * 0.28, cy - r * 0.28),
                  (cx + r, cy), (cx + r * 0.28, cy + r * 0.28),
                  (cx, cy + r), (cx - r * 0.28, cy + r * 0.28),
                  (cx - r, cy), (cx - r * 0.28, cy - r * 0.28)], fill=fill)


# ---------------------------------------------------------------- icons
def _icon_shenzhen(d, x0, y0, x1, y1):
    # Three towers with three small flags.
    base = y1
    for tx, tw, th in ((x0 + 8, 16, 58), (x0 + 30, 20, 84), (x0 + 56, 16, 66)):
        d.rectangle([tx * S, (base - th) * S, (tx + tw) * S, base * S],
                    fill=INK)
        d.rectangle([tx * S, (base - th) * S, (tx + tw) * S,
                     (base - th + 4) * S], fill=AMBER)
    for fx, cols in ((x0 + 78, ((200, 40, 40), (246, 241, 227), (200, 40, 40))),
                     (x0 + 92, ((200, 40, 40), (200, 40, 40), (200, 40, 40))),
                     (x0 + 106, ((246, 241, 227), (40, 80, 160), (200, 40, 40)))):
        d.line([(fx * S, (base - 40) * S), (fx * S, (base - 74) * S)],
               fill=CREAM, width=2 * S)
        for i, c in enumerate(cols):
            d.rectangle([(fx + 1) * S, (base - 74 + i * 4) * S,
                         (fx + 13) * S, (base - 70 + i * 4) * S], fill=c)


def _icon_hague(d, x0, y0, x1, y1):
    base = y1
    cx = (x0 + x1) // 2
    d.polygon([(cx - 52) * S, (base - 52) * S, cx * S, (base - 78) * S,
               (cx + 52) * S, (base - 52) * S], fill=INK)
    d.rectangle([(cx - 52) * S, (base - 52) * S, (cx + 52) * S, base * S],
                fill=INK)
    for i in range(4):
        colx = cx - 42 + i * 28
        d.rectangle([colx * S, (base - 48) * S, (colx + 7) * S, base * S],
                    fill=CREAM)
    # scales of justice above the roofline
    sy = base - 96
    d.line([(cx * S, sy * S), (cx * S, (sy + 16) * S)], fill=AMBER, width=2 * S)
    d.line([((cx - 16) * S, (sy + 4) * S), ((cx + 16) * S, (sy + 4) * S)],
           fill=AMBER, width=2 * S)
    d.pieslice([(cx - 24) * S, (sy + 4) * S, (cx - 8) * S, (sy + 18) * S],
               0, 180, fill=AMBER)
    d.pieslice([(cx + 8) * S, (sy + 4) * S, (cx + 24) * S, (sy + 18) * S],
               0, 180, fill=AMBER)


def _icon_gulf(d, x0, y0, x1, y1):
    base = y1
    # sea waves
    for k, wy in enumerate((base - 22, base - 12, base - 3)):
        pts = []
        for i in range(25):
            px = x0 + 4 + i * 4
            py = wy + 3 * math.sin(i * 0.9 + k)
            pts.append((px * S, py * S))
        d.line(pts, fill=TEAL, width=2 * S)
    # tanker
    d.rectangle([(x0 + 10) * S, (base - 44) * S, (x0 + 78) * S,
                 (base - 26) * S], fill=INK)
    d.rectangle([(x0 + 62) * S, (base - 56) * S, (x0 + 72) * S,
                 (base - 44) * S], fill=INK)
    d.rectangle([(x0 + 14) * S, (base - 42) * S, (x0 + 74) * S,
                 (base - 40) * S], fill=AMBER)
    # drone above
    dx, dy = x0 + 92, base - 66
    d.line([((dx - 12) * S, (dy - 8) * S), ((dx + 12) * S, (dy + 8) * S)],
           fill=CREAM, width=2 * S)
    d.line([((dx - 12) * S, (dy + 8) * S), ((dx + 12) * S, (dy - 8) * S)],
           fill=CREAM, width=2 * S)
    for rx, ry in ((dx - 12, dy - 8), (dx + 12, dy + 8),
                   (dx - 12, dy + 8), (dx + 12, dy - 8)):
        d.ellipse([(rx - 3) * S, (ry - 3) * S, (rx + 3) * S, (ry + 3) * S],
                  fill=AMBER)
    d.ellipse([(dx - 4) * S, (dy - 4) * S, (dx + 4) * S, (dy + 4) * S],
              fill=CREAM)


def _icon_riyadh(d, x0, y0, x1, y1):
    base = y1
    cx = (x0 + x1) // 2
    d.polygon([(cx - 16) * S, base * S, (cx - 9) * S, (base - 96) * S,
               (cx + 9) * S, (base - 96) * S, (cx + 16) * S, base * S],
              fill=INK)
    d.rectangle([(cx - 2) * S, (base - 110) * S, (cx + 2) * S,
                 (base - 96) * S], fill=INK)
    for k in range(6):
        wy = base - 88 + k * 13
        d.line([((cx - 8) * S, wy * S), ((cx + 8) * S, wy * S)],
               fill=AMBER, width=1 * S)
    # crack + flash
    d.line([((cx + 4) * S, (base - 60) * S), ((cx - 2) * S, (base - 48) * S),
            ((cx + 5) * S, (base - 36) * S), ((cx - 1) * S, (base - 24) * S)],
           fill=ROSE, width=2 * S)
    _star(d, (cx + 22) * S, (base - 58) * S, 9 * S, AMBER)


def _icon_leonida(d, x0, y0, x1, y1):
    base = y1
    cx = (x0 + x1) // 2
    # solid setting sun
    d.ellipse([(cx - 26) * S, (base - 78) * S, (cx + 26) * S,
               (base - 26) * S], fill=AMBER)
    d.line([((cx - 26) * S, (base - 52) * S), ((cx + 26) * S, (base - 52) * S)],
           fill=AMBER_DEEP, width=2 * S)
    d.line([((cx - 26) * S, (base - 44) * S), ((cx + 26) * S, (base - 44) * S)],
           fill=AMBER_DEEP, width=2 * S)
    # palm silhouette, pale fronds so it reads against the dusk sky
    px = x0 + 14
    pts = [(px + 8 * math.sin(i * 0.3), base - i * 5) for i in range(13)]
    d.line([(x * S, y * S) for x, y in pts], fill=INK, width=4 * S)
    top = pts[-1]
    for ang in (-160, -120, -80, -40, 0):
        ex = top[0] + 26 * math.cos(math.radians(ang))
        ey = top[1] + 16 * math.sin(math.radians(ang)) - 8
        d.line([(top[0] * S, top[1] * S), (ex * S, ey * S)], fill=CREAM,
               width=3 * S)
    # neon bar
    d.rectangle([(cx + 6) * S, (base - 30) * S, (x1 - 8) * S,
                 (base - 22) * S], fill=ROSE)
    d.rectangle([(cx + 6) * S, (base - 20) * S, (x1 - 8) * S,
                 (base - 16) * S], fill=TEAL)


def _icon_nasdaq(d, x0, y0, x1, y1):
    base = y1
    bars = (26, 40, 54, 72)
    for i, bh in enumerate(bars):
        bx = x0 + 10 + i * 26
        d.rectangle([bx * S, (base - bh) * S, (bx + 16) * S, base * S],
                    fill=TEAL if i % 2 == 0 else AMBER)
    d.line([((x0 + 8) * S, (base - 22) * S), ((x0 + 42) * S, (base - 44) * S),
            ((x0 + 66) * S, (base - 58) * S), ((x0 + 104) * S, (base - 88) * S)],
           fill=CREAM, width=3 * S)
    ax, ay = x0 + 104, base - 88
    d.polygon([(ax * S, (ay - 12) * S), ((ax + 14) * S, (ay + 2) * S),
               ((ax - 2) * S, (ay + 2) * S)], fill=CREAM)


def _icon_voyager(d, x0, y0, x1, y1):
    base = y1
    cx = (x0 + x1) // 2
    # tilted dish bowl with a feed arm, so it reads as a dish, not a dome
    d.pieslice([(cx - 34) * S, (base - 88) * S, (cx + 34) * S,
                (base - 20) * S], 195, 345, fill=CREAM)
    d.line([((cx + 16) * S, (base - 66) * S), ((cx + 26) * S, (base - 84) * S)],
           fill=CREAM, width=2 * S)
    d.ellipse([(cx + 22) * S, (base - 88) * S, (cx + 30) * S,
               (base - 80) * S], fill=AMBER)
    d.line([(cx * S, (base - 50) * S), (cx * S, base * S)], fill=CREAM,
           width=3 * S)
    d.line([((cx - 18) * S, base * S), ((cx + 18) * S, base * S)], fill=CREAM,
           width=3 * S)
    _star(d, (x0 + 16) * S, (base - 92) * S, 5 * S, AMBER)
    _star(d, (x1 - 14) * S, (base - 78) * S, 4 * S, CREAM)
    _star(d, (x0 + 30) * S, (base - 40) * S, 3 * S, CREAM)
    d.line([((x1 - 30) * S, (base - 96) * S), ((x1 - 8) * S, (base - 108) * S)],
           fill=AMBER, width=2 * S)
    d.rectangle([((x1 - 36) * S), (base - 100) * S, (x1 - 28) * S,
                 (base - 92) * S], fill=AMBER)


def _icon_cyclone(d, x0, y0, x1, y1):
    base = y1
    cx, cy = (x0 + x1) // 2, base - 52
    for r, a0, a1 in ((34, 0, 300), (25, 40, 340), (16, 80, 330), (8, 120, 320)):
        d.arc([(cx - r) * S, (cy - r) * S, (cx + r) * S, (cy + r) * S],
              a0, a1, fill=CREAM, width=3 * S)
    d.ellipse([(cx - 4) * S, (cy - 4) * S, (cx + 4) * S, (cy + 4) * S],
              fill=AMBER)
    for rx in (x0 + 12, x0 + 34, x1 - 30):
        d.line([(rx * S, (base - 22) * S), ((rx - 6) * S, (base - 6) * S)],
               fill=TEAL, width=2 * S)
    pts = []
    for i in range(25):
        px = x0 + 4 + i * 4
        py = base - 2 + 2 * math.sin(i * 0.9)
        pts.append((px * S, py * S))
    d.line(pts, fill=TEAL, width=2 * S)


ICONS = {
    "shenzhen": _icon_shenzhen,
    "hague": _icon_hague,
    "gulf": _icon_gulf,
    "riyadh": _icon_riyadh,
    "leonida": _icon_leonida,
    "nasdaq": _icon_nasdaq,
    "voyager": _icon_voyager,
    "cyclone": _icon_cyclone,
}


# ---------------------------------------------------------------- drawing
def _draw_masthead(d):
    f_title = _font(SERIF, 52)
    f_chip = _font(SANS_BOLD, 17)
    f_strap = _font(SANS_BOLD, 12)
    _center(d, W * S // 2, 12 * S, "THE WORLD TODAY", f_title, INK)
    d.line([(24 * S, 72 * S), (1000 * S, 72 * S)], fill=INK, width=2 * S)
    chip = "THURSDAY 19 NOVEMBER 2026"
    cw = int(_text_w(d, chip, f_chip)) + 44 * S
    cx0 = (W * S - cw) // 2
    d.rounded_rectangle([cx0, 78 * S, cx0 + cw, 102 * S], radius=12 * S,
                        fill=INK)
    _center(d, W * S // 2, 83 * S, chip, f_chip, CREAM)
    _tracked(d, W * S // 2, 108 * S,
             "36 STORIES  •  6 CONTINENTS  •  ONE FRONT PAGE",
             f_strap, INK_SOFT, 2 * S)


def _draw_panorama(d):
    x0, y0, x1, y1 = 16, 146, 1008, 436
    f_head = _font(SANS_BOLD, 13)
    f_head_r = _font(SANS, 10)
    d.text((24 * S, 126 * S), "ONE DAY, ONE SKYLINE", font=f_head, fill=INK)
    rt = "EIGHT SCENES FROM THURSDAY"
    d.text(((1000 - _text_w(d, rt, f_head_r)) * S, 128 * S), rt,
           font=f_head_r, fill=INK_SOFT)
    # dusk sky in discrete bands (compresses well as PNG)
    bands = 26
    stops = [(SKY_TOP, 0.0), (SKY_MID, 0.45), (SKY_LOW, 0.78),
             (SKY_HORIZON, 1.0)]
    for i in range(bands):
        t0 = i / bands
        t1 = (i + 1) / bands
        for j in range(len(stops) - 1):
            if stops[j][1] <= t0 <= stops[j + 1][1]:
                f = (t0 - stops[j][1]) / (stops[j + 1][1] - stops[j][1])
                col = _lerp(stops[j][0], stops[j + 1][0], f)
                break
        else:
            col = stops[-1][0]
        yy0 = y0 + int((y1 - y0 - 44) * t0)
        yy1 = y0 + int((y1 - y0 - 44) * t1)
        d.rectangle([x0 * S, yy0 * S, x1 * S, yy1 * S], fill=col)
    # stars in the upper sky
    for sx, sy in ((60, 170), (150, 162), (300, 176), (430, 164), (560, 172),
                   (700, 160), (830, 168), (950, 176), (240, 196), (620, 192),
                   (880, 200), (90, 210)):
        _star(d, sx * S, sy * S, 3 * S, CREAM)
    # continuous skyline silhouette just above the label bar
    sil_top = y1 - 44
    heights = [26, 40, 18, 34, 48, 22, 38, 16, 30, 44, 20, 36, 14, 42, 28,
               18, 34, 46, 24, 32, 16, 38, 26, 20, 44, 30, 18, 36, 22, 40]
    bx = x0
    for hgt in heights:
        bw = 33
        d.rectangle([bx * S, (sil_top - hgt) * S, (bx + bw) * S,
                     sil_top * S], fill=INK)
        bx += bw
        if bx >= x1:
            break
    # eight scenes
    seg_w = (x1 - x0) / 8
    for i, (title, sub, key) in enumerate(SEGMENTS):
        sx0 = x0 + i * seg_w
        sx1 = sx0 + seg_w
        ICONS[key](d, int(sx0) + 2, y0 + 14, int(sx1) - 2, sil_top - 6)
        if i:
            d.line([(sx0 * S, y0 * S), (sx0 * S, y1 * S)],
                   fill=(120, 130, 160), width=1 * S)
    # label bar
    d.rectangle([x0 * S, (y1 - 44) * S, x1 * S, y1 * S], fill=LABEL_BAR)
    f_t = _font(SANS_BOLD, 11)
    f_s = _font(SANS, 9)
    for i, (title, sub, _k) in enumerate(SEGMENTS):
        cx = x0 + (i + 0.5) * seg_w
        _center(d, cx * S, (y1 - 40) * S, title, f_t, CREAM)
        _center(d, cx * S, (y1 - 24) * S, sub, f_s, AMBER)
    d.rectangle([x0 * S, y0 * S, x1 * S, y1 * S], outline=INK, width=2 * S)


def _draw_index(d):
    f_head = _font(SERIF, 15)
    f_region = _font(SANS_BOLD, 11)
    f_num = _font(SANS_BOLD, 12)
    f_item = _font(SANS, 12)
    d.text((24 * S, 448 * S), "THE DAY IN 36 STORIES", font=f_head, fill=INK)
    d.line([(24 * S, 470 * S), (1000 * S, 470 * S)], fill=INK, width=2 * S)
    # split regions into two columns of 18 items
    col1 = REGIONS[0:2] + [("AFRICA", REGIONS[2][1], REGIONS[2][2][:2])]
    col2 = [("AFRICA", REGIONS[2][1], REGIONS[2][2][2:])] + REGIONS[3:]
    columns = [(24, col1), (526, col2)]
    for x_left, groups in columns:
        y = 478
        for name, color, items in groups:
            d.text((x_left * S, y * S), name, font=f_region, fill=color)
            d.line([((x_left + 78) * S, (y + 7) * S),
                    ((x_left + 472) * S, (y + 7) * S)],
                   fill=color, width=1 * S)
            y += 16
            for num, headline in items:
                d.text((x_left * S, y * S), "%d." % num, font=f_num,
                       fill=INK)
                d.text(((x_left + 34) * S, y * S), headline, font=f_item,
                       fill=INK)
                y += 15
            y += 2


def _draw_numbers(d):
    f_head = _font(SERIF, 14)
    f_big = _font(SERIF, 20)
    f_lab = _font(SANS, 10)
    d.text((24 * S, 826 * S), "DAY IN NUMBERS", font=f_head, fill=INK)
    d.line([(24 * S, 846 * S), (1000 * S, 846 * S)], fill=INK, width=2 * S)
    bw, gap = 190, 8
    for i, (big, lab1, lab2) in enumerate(NUMBERS):
        bx0 = 21 + i * (bw + gap)
        d.rectangle([bx0 * S, 854 * S, (bx0 + bw) * S, 956 * S],
                    fill=PAPER_DIM, outline=INK, width=1 * S)
        _center(d, (bx0 + bw // 2) * S, 868 * S, big, f_big, INK)
        _center(d, (bx0 + bw // 2) * S, 908 * S, lab1, f_lab, INK_SOFT)
        _center(d, (bx0 + bw // 2) * S, 924 * S, lab2, f_lab, INK_SOFT)
    f_src = _font(SANS, 9)
    _center(d, W * S // 2, 968 * S, SOURCES, f_src, INK_SOFT)


def _render(out_path):
    from PIL import Image, ImageDraw
    img = Image.new("RGB", (W * S, H * S), PAPER)
    d = ImageDraw.Draw(img)
    # frame
    d.rectangle([8 * S, 8 * S, (W - 8) * S, (H - 8) * S], outline=INK,
                width=3 * S)
    d.rectangle([16 * S, 16 * S, (W - 16) * S, (H - 16) * S], outline=INK,
                width=1 * S)
    _draw_masthead(d)
    _draw_panorama(d)
    _draw_index(d)
    _draw_numbers(d)
    img = img.resize((W, H), Image.LANCZOS)
    # 256-colour palette, no dither: keeps the file small (tie-break)
    # while the flat newspaper palette survives intact.
    img = img.quantize(colors=256, method=Image.Quantize.MEDIANCUT,
                       dither=Image.Dither.NONE)
    img.save(out_path, "PNG", optimize=True)


def _fallback(out_path):
    here = os.path.dirname(os.path.abspath(__file__))
    bundled = os.path.join(here, "entry.png")
    shutil.copyfile(bundled, out_path)


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    try:
        os.makedirs(out_dir, exist_ok=True)
    except OSError:
        out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               "output")
        os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.png")
    try:
        import PIL  # noqa: F401
    except ImportError:
        _fallback(out_path)
        return 0
    _render(out_path)
    return 0


if __name__ == "__main__":
    sys.exit(main())

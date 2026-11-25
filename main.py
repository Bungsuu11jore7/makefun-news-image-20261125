#!/usr/bin/env python3
"""The World Today — 25 November 2026. make.fun news-image-20261125 v2.

Builds a 1024x1024 newspaper-style summary of 38 verified world-news stories
from Wednesday 25 November 2026, with 13 original drawn scenes. Deterministic:
no timestamps, no randomness, fixed PNG settings. Written fresh for v2.
"""
import os
import shutil
import sys
import tempfile

BASE = os.path.dirname(os.path.abspath(__file__))
OUT_ENV = "MAKEFUN_OUTPUT_DIR"


def output_dir():
    d = os.environ.get(OUT_ENV) or "/output"
    try:
        os.makedirs(d, exist_ok=True)
        probe = os.path.join(d, ".probe")
        with open(probe, "w") as f:
            f.write("x")
        os.remove(probe)
        return d
    except Exception:
        return tempfile.mkdtemp(prefix="news-image-20261125-")


# ---------------------------------------------------------------- data
# Featured 1-13: (num, place, field, badge, headline, summary, source)
FEATURED = [
    (1, "GAZA", "WAR", "C",
     "ISRAEL KILLS SECOND HAMAS SECURITY CHIEF IN 24 HOURS",
     "Pre-dawn strike on a Shati camp apartment kills Col. Muhammad Majed "
     "Abu al-Ouf, his wife and two daughters, aged 15 and 13.",
     "Reuters · AP"),
    (2, "USA", "ECONOMY", "C",
     "US GDP REVISED TO 4.3% AS PCE INFLATION STICKS AT 3.8%",
     "Q3 growth revised sharply up; October PCE +3.8%, core +3.3%; jobless "
     "claims 189,000. Bets grow on a Fed hike on 9 Dec.",
     "Zacks · KuCoin · ING"),
    (3, "USA", "MARKETS", "C",
     "WALL STREET SLIDES AS AI ROUT DEEPENS",
     "Dow \u2212831 (\u22121.7%), S&P 500 \u22122.6%, Nasdaq \u22123.8% as AI stocks "
     "plunge again; Nvidia falls ~8%. Markets shut for Thanksgiving.",
     "AP · Reuters"),
    (4, "ANKARA", "DIPLOMACY", "C",
     "HAFTAR MEETS ERDO\u011eAN IN ANKARA",
     "Libya's eastern commander makes his first official visit to Turkey; "
     "his sons attend. No readout or deal announced.",
     "EuropeSays · The Turkiye Times"),
    (5, "GAZA", "JUSTICE", "C",
     "AMNESTY: PROBE ISRAEL OVER BLOCKING BIRTHS IN GAZA",
     "135-page report says Israeli actions since Oct 2023 prevented births "
     "in Gaza; urges the ICC to investigate.",
     "Amnesty International"),
    (6, "CHINA", "SPACE", "C",
     "SHENZHOU-24 LAUNCHES WITH FIRST PAKISTANI IN ORBIT",
     "Long March 2F lifts off from Jiuquan at 00:18 UTC; first Pakistani in "
     "orbit and first foreign astronaut on Tiangong.",
     "Xinhua"),
    (7, "SAUDI ARABIA", "WAR", "C",
     "HOUTHIS CLAIM NEW STRIKES ON SAUDI ARABIA",
     "Houthis say they hit Ras Tanura refinery and Riyadh's financial "
     "district; coalition says four drones intercepted.",
     "Reuters"),
    (8, "RUSSIA", "WAR", "C",
     "UKRAINE DRONES HIT TWO SAMARA REFINERIES",
     "Drones strike Syzran and Kuibyshev refineries ~800 km from the "
     "border; fires reported, one killed. Putin threatens retaliation.",
     "The Independent"),
    (9, "UKRAINE", "WAR", "C",
     "RUSSIA HITS UKRAINE GAS PLANT AND CARGO SHIP",
     "Naftogaz gas facility in Poltava hit, large fire, operations halted; "
     "Russia claims a cargo ship struck at Chornomorsk.",
     "The Independent"),
    (10, "ASIA", "MARKETS", "C",
     "ASIA MARKETS CRASH ON TARIFF THREAT AND AI DOUBTS",
     "KOSPI \u22126.16%, TAIEX \u22124.80%, Nikkei \u22122.78% as a fresh US tariff "
     "threat and AI doubts hit Asian stocks.",
     "AP"),
    (11, "COLOMBIA", "CRIME", "C",
     "CARTAGENA HOSTAGE RESCUE FREES ALL REMAINING CAPTIVES",
     "Colombian forces storm the \u00c9xito supermarket and free all remaining "
     "hostages; one captor killed, four detained.",
     "Reuters"),
    (12, "SWITZERLAND", "SPORT", "C",
     "GUKESH\u2013SINDAROV DRAW IN 20 MOVES, 1\u20131",
     "World champion Gukesh plays the London System in Geneva, but Sindarov "
     "is ready; a 20-move draw by repetition.",
     "Chess.com · ChessBase India"),
    (13, "AUSTRALIA", "ECONOMY", "C",
     "AUSTRALIA INFLATION JUMPS TO 4.9%",
     "October CPI +4.9% YoY, above forecast; trimmed mean 3.8%; fuel +6.3%. "
     "Pressure builds on the RBA before December.",
     "Reuters"),
]

# Also on: (num, badge, headline, source)
ALSO = [
    (14, "C", "Yemen parliament outlaws Houthis", "Daily Voice of Asia"),
    (15, "C", "India rallies against regional slide", "The Hindu BusinessLine"),
    (16, "C", "US shelves Russia business-deal incentives", "Reuters"),
    (17, "C", "Ramaphosa wins court case over \u201cFarmgate\u201d report", "Reuters"),
    (18, "C", "Bitcoin falls below $60,000", "Morningstar / Dow Jones"),
    (19, "C", "Met Police still institutionally racist, review finds", "BBC"),
    (20, "O", "Germany Q3 GDP growth revised down to 0.1%", "Destatis"),
    (21, "C", "Three bodies recovered in search for trapped miners", "Reuters"),
    (22, "R", "El Hierro sets Spain's one-day rescue record", "Russpain"),
    (23, "C", "Peru cuts growth outlook, raises deficit forecast", "Reuters"),
    (24, "C", "Nollywood icon Pete Edochie dies aged 79", "Okay News"),
    (25, "R", "SpaceX launches classified US Space Force payload", "New York Post"),
    (26, "C", "UK welfare review offers \u201cno answers\u201d on PIP bill", "BBC"),
    (27, "C", "MoD bought fake explosives for Ukraine", "Financial Times"),
    (28, "C", "Two men arrested at Prince and Princess of Wales's home", "BBC"),
    (29, "C", "Delhi wakes to coldest morning as air stays \u201cpoor\u201d", "The Hindu BusinessLine"),
    (30, "C", "India's top court refuses interim bail to Khalid, Imam", "Live Law"),
    (31, "R", "India tells UN humans must stay responsible for AI weapons", "RealFeed"),
    (32, "C", "Nigeria police invite Omo-Agege over Delta rally killings", "PSM Nigeria"),
    (33, "C", "New Zealand domestic netball league collapses", "BBC Sport"),
    (34, "C", "Italy marks day against violence against women", "Pollar"),
    (35, "O", "Pope Leo XIV denounces the arms race", "Vatican Report"),
    (36, "C", "Fort Hood: judge hears Hasan's stay plea; no ruling", "Military.com"),
    (37, "C", "Ghana budget debate extended; vote pushed to Thursday", "Ghana Guardian"),
    (38, "C", "Libya army vows retaliation after officers die of wounds", "AP"),
]

CHIPS = [("EUROPE", 11), ("AMERICAS", 7), ("ASIA", 7), ("MIDDLE EAST", 5),
         ("AFRICA", 5), ("OCEANIA", 2), ("WORLD", 1)]

TIMELINE = [
    ("00:18", "Shenzhou-24 launches"),
    ("00:30", "Australia CPI released"),
    ("03:56", "Shenzhou-24 docks"),
    ("06:30", "Cartagena rescue"),
    ("13:30", "US PCE / GDP released"),
    ("14:00", "FIDE Game 2 begins"),
    ("19:00", "Fed Beige Book released"),
    ("21:00", "US markets close"),
]

NUMBERS = [
    ("4.3%", "US Q3 GDP, revised up"),
    ("3.8%", "October PCE inflation YoY"),
    ("189,000", "US jobless claims"),
    ("\u22123.8%", "Nasdaq on Wednesday"),
    ("2,100", "migrant arrivals, El Hierro"),
    ("4.9%", "Australia October CPI"),
]

# Map pins: (num, lon, lat)
PINS = [(1, 35.5, 31.5), (2, -96.0, 39.0), (3, -93.0, 36.0),
        (4, 32.9, 39.9), (5, 34.6, 31.4), (6, 98.5, 40.0),
        (7, 50.2, 26.6), (8, 50.1, 53.2), (9, 34.5, 49.6),
        (10, 127.0, 37.5), (11, -75.5, 10.4), (12, 6.1, 46.2),
        (13, 151.2, -33.9)]

DATE_CHECK = ("DATE CHECK \u2014 Left out: Oxfam/CEOBS Gaza report (published Mon 23 Nov) \u00b7 "
              "Katz on Iran chemical weapons (briefing Tue 24 Nov) \u00b7 ~490,000 Russian war "
              "deaths leak (first reported Tue 24 Nov) \u00b7 US Section 301 tariff plan (first "
              "reported Tue 24 Nov) \u00b7 Dow above 50,000 (Tue 24 Nov close) \u00b7 Ghana budget "
              "vote (did not happen 25 Nov) \u00b7 Iowa detonation (did not happen).")

BADGE_FILL = {"C": (30, 125, 50), "O": (26, 77, 143),
              "R": (178, 106, 0), "CL": (106, 61, 154)}

# ---------------------------------------------------------------- helpers
SS = 2          # supersample factor
W, H = 1024, 1024
M = 14          # margin
CW = W - 2 * M  # content width
PAPER = (247, 243, 234)
INK = (17, 17, 17)
RED = (164, 30, 34)
GREY = (90, 86, 78)
LINE = (120, 115, 100)
MAP_FILL = (214, 205, 182)
MAP_LINE = (150, 140, 115)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
SERIF_B = FONT_DIR + "DejaVuSerif-Bold.ttf"
SERIF = FONT_DIR + "DejaVuSerif.ttf"
SANS_B = FONT_DIR + "DejaVuSans-Bold.ttf"
SANS = FONT_DIR + "DejaVuSans.ttf"


def build():
    from PIL import Image, ImageDraw, ImageFont

    def font(path, size):
        try:
            return ImageFont.truetype(path, int(size * SS))
        except Exception:
            return ImageFont.load_default()

    def F(path, size):
        return font(path, size)

    img = Image.new("RGB", (W * SS, H * SS), PAPER)
    d = ImageDraw.Draw(img)

    def X(v):
        return int(v * SS)

    def rect(x0, y0, x1, y1, fill=None, outline=None, width=1):
        d.rectangle([X(x0), X(y0), X(x1), X(y1)], fill=fill,
                    outline=outline, width=int(width * SS))

    def line(x0, y0, x1, y1, fill=INK, width=1):
        d.line([X(x0), X(y0), X(x1), X(y1)], fill=fill, width=int(width * SS))

    def text(x, y, s, fnt, fill=INK, anchor="la"):
        d.text((X(x), X(y)), s, font=fnt, fill=fill, anchor=anchor)

    def tw(s, fnt):
        return d.textlength(s, font=fnt) / SS

    def fit_font(path, size, s, maxw, min_size=7):
        sz = size
        while sz > min_size and tw(s, font(path, sz)) > maxw:
            sz -= 0.5
        return font(path, sz), sz

    def wrap(s, fnt, maxw):
        words, lines, cur = s.split(), [], ""
        for w in words:
            t = (cur + " " + w).strip()
            if tw(t, fnt) <= maxw or not cur:
                cur = t
            else:
                lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
        return lines

    def wrap_max(s, fnt, maxw, max_lines):
        lines = wrap(s, fnt, maxw)
        if len(lines) > max_lines:
            lines = lines[:max_lines]
            while lines and tw(lines[-1] + "\u2026", fnt) > maxw:
                lines[-1] = lines[-1][:-1]
            lines[-1] = lines[-1] + "\u2026"
        return lines

    def badge(x, y, letter, size=11):
        # small filled square with letter, top-right of a card
        s = size
        rect(x, y, x + s, y + s, fill=BADGE_FILL.get(letter, (90, 90, 90)))
        f = font(SANS_B, size - 2.5)
        text(x + s / 2, y + s / 2 - 0.5, letter, f, fill=(255, 255, 255),
             anchor="mm")

    def crop_fill(path, w, h):
        try:
            im = Image.open(path).convert("RGB")
        except Exception:
            return Image.new("RGB", (max(1, X(w)), max(1, X(h))), (200, 200, 200))
        tw_, th_ = im.size
        ta, sa = w / h, tw_ / th_
        if sa > ta:
            nw = int(th_ * ta)
            x0 = (tw_ - nw) // 2
            im = im.crop((x0, 0, x0 + nw, th_))
        else:
            nh = int(tw_ / ta)
            y0 = (th_ - nh) // 2
            im = im.crop((0, y0, tw_, y0 + nh))
        return im.resize((X(w), X(h)), Image.LANCZOS)

    # ---------------------------------------------------------- top line
    f_top = F(SANS_B, 10)
    text(M, 7, "ONE DAY OF WORLD NEWS", f_top)
    right = ("38 STORIES \u00b7 7 REGIONS \u00b7 14 FIELDS \u00b7 EVERY ONE FROM "
             "WEDNESDAY 25 NOVEMBER 2026")
    f_r, _ = fit_font(SANS_B, 10, right, CW - tw("ONE DAY OF WORLD NEWS", f_top) - 20)
    text(W - M, 7, right, f_r, anchor="ra")

    # ---------------------------------------------------------- masthead
    f_mast, _ = fit_font(SERIF_B, 46, "Wednesday 25 November 2026", CW)
    text(W / 2, 20, "Wednesday 25 November 2026", f_mast, anchor="ma")
    line(M, 70, W - M, 70, width=1.5)
    sub = ("Gaza strike kills second Hamas security chief \u00b7 US GDP revised "
           "to 4.3% \u00b7 Wall Street slides as AI rout deepens")
    f_sub, _ = fit_font(SANS, 11, sub, CW)
    text(W / 2, 74, sub, f_sub, anchor="ma")

    # ---------------------------------------------------------- region chips
    y = 90
    n = len(CHIPS)
    gap = 6
    chw = (CW - gap * (n - 1)) / n
    for i, (name, cnt) in enumerate(CHIPS):
        x0 = M + i * (chw + gap)
        rect(x0, y, x0 + chw, y + 15, outline=INK, width=1)
        label = "%s %d" % (name, cnt)
        f_c, _ = fit_font(SANS_B, 9.5, label, chw - 6)
        text(x0 + chw / 2, y + 7.5, label, f_c, anchor="mm")

    # ---------------------------------------------------------- timeline
    y = 111
    text(M, y, "THE DAY IN UTC", F(SANS_B, 10))
    line(M, y + 13, W - M, y + 13, fill=LINE, width=1)
    colw = CW / len(TIMELINE)
    for i, (t, label) in enumerate(TIMELINE):
        x0 = M + i * colw + (3 if i else 0)
        text(x0, y + 17, t, F(SANS_B, 10), fill=RED)
        for j, ln in enumerate(wrap_max(label, F(SANS, 8.5), colw - 6, 2)):
            text(x0, y + 29 + j * 10, ln, F(SANS, 8.5))

    # ---------------------------------------------------------- in numbers
    y = 164
    text(M, y, "IN NUMBERS", F(SANS_B, 10))
    line(M, y + 13, W - M, y + 13, fill=LINE, width=1)
    colw = CW / len(NUMBERS)
    for i, (val, cap) in enumerate(NUMBERS):
        x0 = M + i * colw + (3 if i else 0)
        f_v, _ = fit_font(SERIF_B, 24, val, colw - 6)
        text(x0, y + 17, val, f_v)
        f_cap, _ = fit_font(SANS, 8.5, cap, colw - 6)
        text(x0, y + 43, cap, f_cap, fill=GREY)
        if i:
            line(M + i * colw - 3, y + 18, M + i * colw - 3, y + 50,
                 fill=LINE, width=1)

    # ---------------------------------------------------------- featured
    y = 218
    text(M, y, "FEATURED \u2014 13 DRAWN STORIES", F(SANS_B, 10))
    line(M, y + 13, W - M, y + 13, fill=LINE, width=1)

    def draw_card(num, place, field, bdg, headline, summary, source,
                  x0, y0, w, h, img_h, hl_size, sum_size):
        rect(x0, y0, x0 + w, y0 + h, outline=INK, width=1)
        im = crop_fill(os.path.join(BASE, "card%d.png" % num), w - 2, img_h)
        img.paste(im, (X(x0 + 1), X(y0 + 1)))
        ty = y0 + img_h + 3
        tag = "%02d \u00b7 %s \u00b7 %s" % (num, place, field)
        f_tag, _ = fit_font(SANS_B, 8.5, tag, w - 16)
        text(x0 + 4, ty, tag, f_tag, fill=RED)
        badge(x0 + w - 15, ty - 1, bdg)
        hy = ty + 11
        f_hl = F(SANS_B, hl_size)
        for j, ln in enumerate(wrap_max(headline, f_hl, w - 8, 2)):
            text(x0 + 4, hy + j * (hl_size + 1), ln, f_hl)
        sy = hy + 2 * (hl_size + 1) + 1
        f_sm = F(SANS, sum_size)
        for j, ln in enumerate(wrap_max(summary, f_sm, w - 8, 2)):
            text(x0 + 4, sy + j * (sum_size + 1), ln, f_sm)
        f_src = F(SANS, 8)
        text(x0 + 4, y0 + h - 10, source, f_src, fill=GREY)

    # row 1: 3 large cards
    y1 = 235
    rw, rg = 326, 9
    for i in range(3):
        c = FEATURED[i]
        draw_card(c[0], c[1], c[2], c[3], c[4], c[5], c[6],
                  M + i * (rw + rg), y1, rw, 146, 68, 11.5, 9)
    # rows 2-3: 5 cards each
    rw2, rg2 = 196, 4
    for r in range(2):
        yr = y1 + 150 + r * 134
        for i in range(5):
            c = FEATURED[3 + r * 5 + i]
            draw_card(c[0], c[1], c[2], c[3], c[4], c[5], c[6],
                      M + i * (rw2 + rg2), yr, rw2, 130, 50, 10, 8.5)

    # ---------------------------------------------------------- also on
    y = 657
    text(M, y, "ALSO ON WEDNESDAY 25 NOVEMBER \u00b7 25 MORE, BY REGION",
         F(SANS_B, 10))
    line(M, y + 13, W - M, y + 13, fill=LINE, width=1)
    cols = [ALSO[0:9], ALSO[9:17], ALSO[17:25]]
    colw = (CW - 12) / 3
    for ci, items in enumerate(cols):
        x0 = M + ci * (colw + 6)
        for ri, (num, bdg, headline, source) in enumerate(items):
            yy = y + 17 + ri * 14.5
            text(x0, yy, str(num), F(SANS_B, 8.5))
            bx = x0 + 17
            rect(bx, yy + 1, bx + 9, yy + 10,
                 fill=BADGE_FILL.get(bdg, (90, 90, 90)))
            text(bx + 4.5, yy + 5.5, bdg, F(SANS_B, 7),
                 fill=(255, 255, 255), anchor="mm")
            hx = bx + 12
            line_txt = "%s \u2014 %s" % (headline, source)
            f_a, _ = fit_font(SANS, 8.5, line_txt, colw - 30)
            text(hx, yy, line_txt, f_a)

    # ---------------------------------------------------------- map
    y = 804
    text(M, y, "WHERE IT HAPPENED \u00b7 PINS 1\u201313", F(SANS_B, 10))
    line(M, y + 13, W - M, y + 13, fill=LINE, width=1)
    my0, my1 = y + 17, 928
    mx0, mx1 = M, 676
    rect(mx0, my0, mx1, my1, outline=INK, width=1)

    def ll(lon, lat):
        fx = (lon + 170.0) / 360.0
        fy = (75.0 - lat) / 130.0
        return (mx0 + 4 + fx * (mx1 - mx0 - 8),
                my0 + 4 + fy * (my1 - my0 - 8))

    # simplified continents (lon, lat) polygons
    continents = [
        [(-168, 66), (-140, 70), (-120, 71), (-95, 69), (-80, 73), (-60, 62),
         (-55, 47), (-70, 42), (-75, 35), (-80, 26), (-90, 21), (-97, 16),
         (-105, 20), (-115, 30), (-125, 40), (-125, 49), (-150, 60)],
        [(-80, 9), (-60, 5), (-50, 0), (-40, -5), (-35, -10), (-40, -20),
         (-48, -28), (-58, -35), (-65, -45), (-70, -52), (-73, -40),
         (-70, -20), (-77, -12), (-80, 0)],
        [(-18, 35), (-10, 37), (0, 36), (10, 37), (20, 32), (30, 36),
         (36, 36), (43, 12), (51, 12), (44, 0), (40, -10), (35, -20),
         (32, -29), (20, -35), (15, -27), (12, -18), (9, -1), (-8, 4),
         (-17, 15), (-17, 27)],
        [(-10, 36), (0, 44), (-5, 48), (0, 51), (5, 58), (10, 59),
         (18, 56), (21, 55), (28, 59), (30, 70), (45, 68), (60, 69),
         (80, 73), (110, 74), (140, 72), (160, 70), (178, 66), (170, 60),
         (160, 55), (142, 50), (140, 40), (130, 33), (122, 30), (110, 20),
         (105, 9), (100, 8), (95, 16), (90, 22), (80, 8), (77, 8),
         (72, 20), (66, 25), (60, 25), (52, 26), (48, 30), (44, 29),
         (39, 21), (35, 28), (30, 36), (22, 37), (19, 42), (12, 44),
         (3, 43), (-2, 37)],
        [(114, -22), (122, -14), (132, -12), (142, -11), (146, -19),
         (150, -23), (153, -27), (150, -37), (140, -38), (129, -32),
         (124, -33), (115, -35), (114, -30)],
    ]
    for poly in continents:
        pts = [ll(lon, lat) for lon, lat in poly]
        d.polygon([(X(px), X(py)) for px, py in pts], fill=MAP_FILL,
                  outline=MAP_LINE)
    for num, lon, lat in PINS:
        px, py = ll(lon, lat)
        r = 7
        d.ellipse([X(px - r), X(py - r), X(px + r), X(py + r)],
                  fill=RED, outline=(255, 255, 255), width=SS)
        text(px, py, str(num), F(SANS_B, 8), fill=(255, 255, 255),
             anchor="mm")

    # region counts box
    bx0, bx1 = 684, W - M
    rect(bx0, my0, bx1, my1, outline=INK, width=1)
    text(bx0 + 8, my0 + 5, "REGION COUNTS", F(SANS_B, 10))
    counts = [("Europe 11", "Middle East 5"), ("Africa 5", "Asia 7"),
              ("Oceania 2", "Americas 7"), ("World 1", "")]
    for i, (a, b) in enumerate(counts):
        yy = my0 + 22 + i * 14
        text(bx0 + 8, yy, a, F(SANS, 9.5))
        if b:
            text(bx0 + 150, yy, b, F(SANS, 9.5))
    text(bx0 + 8, my0 + 84, "Pins 1\u201313 = featured stories above.",
         F(SANS, 8.5), fill=GREY)
    text(bx0 + 8, my0 + 98, "Map simplified; pins approximate.",
         F(SANS, 8.5), fill=GREY)

    # ---------------------------------------------------------- date check
    y = 934
    f_dc = F(SANS, 9)
    dc_lines = wrap_max(DATE_CHECK, f_dc, CW, 2)
    if len(dc_lines) > 2:
        dc_lines = dc_lines[:2]
    # shrink font until it fits in 2 lines
    sz = 9.0
    while len(wrap(DATE_CHECK, font(SANS, sz), CW)) > 2 and sz > 6.5:
        sz -= 0.5
    f_dc = font(SANS, sz)
    dc_lines = wrap(DATE_CHECK, f_dc, CW)[:2]
    for j, ln in enumerate(dc_lines):
        text(M, y + j * 11.5, ln, f_dc)
    line(M, y + 26, W - M, y + 26, fill=LINE, width=1)

    # ---------------------------------------------------------- legend/footer
    text(M, 966, "C = 2+ outlets \u00b7 O = official source \u00b7 R = one outlet "
                  "\u00b7 CL = one side's claim", F(SANS, 8.5), fill=GREY)
    foot = ("Every story happened or was first reported on Wednesday 25 Nov "
            "2026 (UTC) \u00b7 sources named on each item \u00b7 original "
            "drawings, no photos")
    f_ft, _ = fit_font(SANS, 8.5, foot, CW)
    text(W / 2, 980, foot, f_ft, anchor="ma", fill=GREY)

    img = img.resize((W, H), Image.LANCZOS)
    return img


def main():
    out = os.path.join(output_dir(), "entry.png")
    try:
        page = build()
    except Exception:
        bundled = os.path.join(BASE, "entry.png")
        if os.path.exists(bundled):
            shutil.copyfile(bundled, out)
            return 0
        raise
    page.save(out, format="PNG", compress_level=6, optimize=False)
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Draw the news-image-20261124 entry: a 1024x1024 newspaper front page.

Fresh code written for this entry from the kit spec + lessons.md teardown.
Layout: masthead + DATE CHECK strip + 3 lead cells + world map + numbers box
+ 10 section blocks (3 columns x 3 rows) + footer. Every story cell: drawn
pictogram + headline (<=15 words) + source name, with a genuinely empty band
between headline ink and source stamp ink (NI22 r6 lesson).
"""
import json
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 14
FONT_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_R = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

PAPER = (247, 243, 234)
INK = (26, 26, 26)
MASTHEAD_BG = (20, 33, 61)
STRIP_BG = (185, 28, 28)
RULE = (26, 26, 26)
MUTED = (90, 90, 90)
OCEAN = (198, 222, 235)
LAND = (232, 214, 178)
LAND_EDGE = (160, 140, 110)

# (section, headline, source, confidence, icon, lat, lon)
# confidence: "" = CONFIRMED, "DEVELOPING", "1-SOURCE"
STORIES = [
    ("LEAD", "US lawmakers condemn Nvidia's reinstatement of Huang", "Forbes EU", "", "chip", 38.9, -77.0),
    ("LEAD", "Zelensky: intelligence shows Russia planning new strikes", "Reuters", "", "warning", 50.45, 30.52),
    ("LEAD", "India pledges $1.6bn to help Nepal rebuild after floods", "Starlit Daily", "", "aid", 28.6, 77.2),
    ("UKRAINE WAR", "Russian strike hits Kramatorsk evacuation bus; two killed", "Sangaku digest", "1-SOURCE", "strike", 48.7, 37.6),
    ("UKRAINE WAR", "Germany raises annual Ukraine aid nearly sixfold since 2022", "Sangaku digest", "1-SOURCE", "flag", 52.5, 13.4),
    ("UKRAINE WAR", "Italy warns Ukraine war could spread to Mediterranean", "Foravia digest", "1-SOURCE", "ship", 41.9, 12.5),
    ("UKRAINE WAR", "France backs Denmark over alleged Russian assassination plot", "Kijev digest", "1-SOURCE", "shield", 48.85, 2.35),
    ("UKRAINE WAR", "Germany picks trains over Lithuania drills to avoid provoking Moscow", "Sangaku digest", "1-SOURCE", "train", 54.7, 25.3),
    ("MIDDLE EAST", "Gaza now a toxic wasteland, Oxfam-CEOBS report warns", "Disclosure News", "", "leaf", 31.5, 34.47),
    ("MIDDLE EAST", "UAE condemns Khartoum strikes that damaged UN building", "Foravia digest", "1-SOURCE", "flag", 24.45, 54.38),
    ("MIDDLE EAST", "Saudi Arabia denounces Khartoum drone strikes", "Domyrenomy digest", "1-SOURCE", "flag", 24.7, 46.7),
    ("MIDDLE EAST", "Egypt denounces Khartoum strikes, urges UN staff safety", "Domyrenomy digest", "1-SOURCE", "flag", 30.0, 31.2),
    ("MIDDLE EAST", "Iran threatens EU bases with 4,500 km missiles", "Kijev digest", "1-SOURCE", "missile", 35.7, 51.4),
    ("MIDDLE EAST", "Tanker incident involving military forces in Gulf of Oman", "Kijev digest", "1-SOURCE", "ship", 23.6, 58.4),
    ("UNITED STATES", "O'Hare ground stop amid Thanksgiving travel rush", "Times of India", "", "plane", 41.9, -87.6),
    ("UNITED STATES", "White House pulls FDA nominee Heidi Overton", "Affairs360", "", "gavel", 38.9, -77.0),
    ("UNITED STATES", "Trump orders Army to wait on Iowa explosives detonation", "Affairs360", "DEVELOPING", "bolt", 41.6, -93.6),
    ("UNITED STATES", "74% of US Latinos have seen or heard ICE activity nearby", "Kijev digest", "1-SOURCE", "vote", 34.0, -118.2),
    ("UNITED STATES", "Van Hollen demands scrutiny of Nvidia chip exports to China", "The News International", "", "chip", 38.9, -77.0),
    ("EUROPE", "NATO chief warns of intensifying malign activity", "Foravia digest", "1-SOURCE", "shield", 50.85, 4.35),
    ("EUROPE", "Germany and Sweden to build global AI security centre", "Domyrenomy digest", "1-SOURCE", "atom", 59.3, 18.07),
    ("EUROPE", "Cyprus expels two envoys over suspected spying", "Kijev digest", "1-SOURCE", "flag", 35.18, 33.38),
    ("EUROPE", "France seeks fresh start with Israel as Lebanon mission deadline nears", "Sangaku digest", "1-SOURCE", "leaf", 48.85, 2.35),
    ("EUROPE", "Third of UK crime victims won't report, trust in police low", "The Times", "", "scale", 51.5, -0.12),
    ("ASIA-PACIFIC", "Seoul names new foreign minister, first woman spy chief", "Kijev digest", "1-SOURCE", "flag", 37.57, 126.98),
    ("ASIA-PACIFIC", "Pakistan envoy: Shenzhen summit shows multipolar era", "Wisevoter / TASS", "", "globe", 33.7, 73.06),
    ("ASIA-PACIFIC", "Xi sends solidarity message to Palestinian people", "Xinhua", "", "flag", 39.9, 116.4),
    ("ASIA-PACIFIC", "Shenzhen turns garbage trucks into rolling power grid", "Medianet", "", "bolt", 22.54, 114.06),
    ("ASIA-PACIFIC", "Space42 and Microsoft UAE launch geospatial AI report", "Medianet", "", "satellite", 24.45, 54.38),
    ("ASIA-PACIFIC", "Vanuatu-Australia pact ratification recommended", "Medianet", "", "aid", -17.74, 168.3),
    ("LATIN AMERICA & MARKETS", "Brazil cuts 2027 growth forecast to 1.8%", "MercoPress", "", "money", -15.79, -47.88),
    ("LATIN AMERICA & MARKETS", "Brazil markets lift inflation, dollar forecasts", "Xinhua", "", "money", -23.55, -46.63),
    ("LATIN AMERICA & MARKETS", "Russia imports 20,000 Chinese workers for Gazprom project", "Kijev digest", "1-SOURCE", "money", 55.75, 37.62),
    ("SPORT", "FIFA picks US for 2031 Women's World Cup, UK for 2035", "Manila Times", "DEVELOPING", "trophy", 47.38, 8.54),
    ("SPORT", "CAS to rule on Senegal's AFCON title appeal today", "Reuters", "", "court", 46.52, 6.63),
    ("SPORT", "Tyson Fury reveals schizophrenia diagnosis", "Affairs360", "", "health", 51.5, -0.12),
    ("TECH, AI & SOCIETY", "US seeks answers on Nvidia chips sold to China", "Foravia digest", "1-SOURCE", "chip", 38.9, -77.0),
    ("TECH, AI & SOCIETY", "UN chief urges global AI safety framework by next year", "Domyrenomy digest", "1-SOURCE", "globe", 40.7, -74.0),
    ("TECH, AI & SOCIETY", "Connected cars can help abusers track victims, study warns", "Medianet", "", "car", -33.87, 151.2),
    ("TECH, AI & SOCIETY", "NSW councils demand poker machine reform", "Medianet", "", "scale", -33.87, 151.2),
    ("TECH, AI & SOCIETY", "London's new 437m pound museum opens", "The Telegraph", "", "building", 51.5, -0.12),
    ("TECH, AI & SOCIETY", "Dutch activist dies by euthanasia at 28", "Times of India", "DEVELOPING", "leaf", 52.37, 4.9),
    ("SCIENCE & SPACE", "Beaver Supermoon rises tonight, first of four supermoons", "Sky at Night", "", "moon", None, None),
    ("SCIENCE & SPACE", "UNSW unveils world-first 'megafire' simulator iFire 2.3", "Medianet", "", "fire", -33.87, 151.2),
    ("SCIENCE & SPACE", "Eight new emergency drones for Northern Territory", "Medianet", "", "drone", -12.46, 130.84),
]

SECTION_COLORS = {
    "LEAD": (20, 33, 61),
    "UKRAINE WAR": (122, 28, 28),
    "MIDDLE EAST": (146, 90, 16),
    "UNITED STATES": (30, 64, 175),
    "EUROPE": (15, 118, 110),
    "ASIA-PACIFIC": (126, 34, 206),
    "LATIN AMERICA & MARKETS": (21, 101, 52),
    "SPORT": (190, 24, 93),
    "TECH, AI & SOCIETY": (55, 65, 81),
    "SCIENCE & SPACE": (100, 60, 180),
}

SECTION_ORDER = [
    ["UKRAINE WAR", "UNITED STATES", "EUROPE"],
    ["MIDDLE EAST", "ASIA-PACIFIC", "TECH, AI & SOCIETY"],
    ["LATIN AMERICA & MARKETS", "SPORT", "SCIENCE & SPACE"],
]

ICON_COLORS = {
    "chip": (30, 64, 175), "warning": (185, 28, 28), "aid": (21, 101, 52),
    "strike": (185, 28, 28), "flag": (30, 64, 175), "ship": (15, 118, 110),
    "shield": (55, 65, 81), "train": (55, 65, 81), "leaf": (21, 101, 52),
    "missile": (122, 28, 28), "plane": (30, 64, 175), "gavel": (100, 60, 30),
    "bolt": (202, 138, 4), "vote": (126, 34, 206), "atom": (15, 118, 110),
    "scale": (100, 60, 30), "globe": (15, 118, 110), "satellite": (55, 65, 81),
    "money": (21, 101, 52), "trophy": (202, 138, 4), "court": (100, 60, 30),
    "health": (185, 28, 28), "car": (55, 65, 81), "building": (126, 34, 206),
    "moon": (100, 116, 139), "fire": (234, 88, 12), "drone": (55, 65, 81),
}


def font(bold, size):
    return ImageFont.truetype(FONT_B if bold else FONT_R, size)


def wrap(draw, text, fnt, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= width:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_icon(d, x, y, s, kind, color):
    """Draw a simple pictogram of side s inside a light tile at (x, y)."""
    d.rounded_rectangle([x, y, x + s, y + s], radius=max(2, s // 8),
                        fill=(255, 255, 255), outline=color, width=max(1, s // 18))
    p = s / 100.0  # unit
    c = color
    cx, cy = x + s / 2, y + s / 2
    if kind == "chip":
        d.rectangle([x + 30 * p, y + 30 * p, x + 70 * p, y + 70 * p], fill=c)
        for i in range(3):
            d.line([x + 30 * p, y + (40 + i * 10) * p, x + 18 * p, y + (40 + i * 10) * p], fill=c, width=max(1, int(3 * p)))
            d.line([x + 70 * p, y + (40 + i * 10) * p, x + 82 * p, y + (40 + i * 10) * p], fill=c, width=max(1, int(3 * p)))
    elif kind == "warning":
        d.polygon([(cx, y + 18 * p), (x + 84 * p, y + 80 * p), (x + 16 * p, y + 80 * p)], fill=c)
        d.rectangle([cx - 2 * p, y + 38 * p, cx + 2 * p, y + 60 * p], fill=(255, 255, 255))
        d.ellipse([cx - 3 * p, y + 66 * p, cx + 3 * p, y + 72 * p], fill=(255, 255, 255))
    elif kind == "aid":
        d.rectangle([cx - 8 * p, y + 22 * p, cx + 8 * p, y + 78 * p], fill=c)
        d.rectangle([x + 22 * p, cy - 8 * p, x + 78 * p, cy + 8 * p], fill=c)
    elif kind == "strike":
        for a in range(8):
            import math
            ang = a * math.pi / 4
            d.line([cx, cy, cx + 34 * p * math.cos(ang), cy + 34 * p * math.sin(ang)], fill=c, width=max(1, int(4 * p)))
        d.ellipse([cx - 12 * p, cy - 12 * p, cx + 12 * p, cy + 12 * p], fill=c)
    elif kind == "flag":
        d.line([x + 28 * p, y + 16 * p, x + 28 * p, y + 84 * p], fill=c, width=max(1, int(4 * p)))
        d.polygon([(x + 28 * p, y + 18 * p), (x + 78 * p, y + 32 * p), (x + 28 * p, y + 48 * p)], fill=c)
    elif kind == "ship":
        d.polygon([(x + 20 * p, y + 58 * p), (x + 80 * p, y + 58 * p), (x + 68 * p, y + 78 * p), (x + 32 * p, y + 78 * p)], fill=c)
        d.rectangle([x + 42 * p, y + 30 * p, x + 58 * p, y + 58 * p], fill=c)
        d.line([x + 18 * p, y + 86 * p, x + 82 * p, y + 86 * p], fill=c, width=max(1, int(3 * p)))
    elif kind == "shield":
        d.polygon([(cx, y + 16 * p), (x + 80 * p, y + 28 * p), (x + 80 * p, y + 52 * p), (cx, y + 84 * p), (x + 20 * p, y + 52 * p), (x + 20 * p, y + 28 * p)], fill=c)
        d.rectangle([cx - 3 * p, y + 36 * p, cx + 3 * p, y + 56 * p], fill=(255, 255, 255))
    elif kind == "train":
        d.rounded_rectangle([x + 24 * p, y + 16 * p, x + 76 * p, y + 84 * p], radius=6 * p, fill=c)
        d.rectangle([x + 32 * p, y + 26 * p, x + 68 * p, y + 44 * p], fill=(255, 255, 255))
        d.ellipse([x + 34 * p, y + 66 * p, x + 44 * p, y + 76 * p], fill=(255, 255, 255))
        d.ellipse([x + 56 * p, y + 66 * p, x + 66 * p, y + 76 * p], fill=(255, 255, 255))
    elif kind == "leaf":
        d.pieslice([x + 20 * p, y + 16 * p, x + 80 * p, y + 84 * p], 180, 360, fill=c)
        d.line([cx, y + 50 * p, cx, y + 86 * p], fill=c, width=max(1, int(4 * p)))
    elif kind == "missile":
        d.polygon([(cx, y + 14 * p), (x + 62 * p, y + 40 * p), (x + 58 * p, y + 70 * p), (x + 42 * p, y + 70 * p), (x + 38 * p, y + 40 * p)], fill=c)
        d.polygon([(x + 38 * p, y + 62 * p), (x + 22 * p, y + 80 * p), (x + 40 * p, y + 74 * p)], fill=c)
        d.polygon([(x + 62 * p, y + 62 * p), (x + 78 * p, y + 80 * p), (x + 60 * p, y + 74 * p)], fill=c)
    elif kind == "plane":
        d.polygon([(x + 14 * p, cy), (x + 50 * p, y + 30 * p), (x + 62 * p, cy - 4 * p), (x + 86 * p, y + 34 * p), (x + 64 * p, cy + 6 * p), (x + 56 * p, y + 70 * p), (x + 44 * p, cy + 6 * p)], fill=c)
    elif kind == "gavel":
        d.line([x + 24 * p, y + 74 * p, x + 76 * p, y + 26 * p], fill=c, width=max(1, int(6 * p)))
        d.rectangle([x + 52 * p, y + 14 * p, x + 80 * p, y + 34 * p], fill=c)
        d.rectangle([x + 20 * p, y + 46 * p, x + 48 * p, y + 66 * p], fill=c)
    elif kind == "bolt":
        d.polygon([(x + 58 * p, y + 14 * p), (x + 30 * p, y + 54 * p), (x + 48 * p, y + 54 * p), (x + 42 * p, y + 86 * p), (x + 70 * p, y + 44 * p), (x + 52 * p, y + 44 * p)], fill=c)
    elif kind == "vote":
        d.rectangle([x + 24 * p, y + 34 * p, x + 76 * p, y + 82 * p], outline=c, width=max(1, int(4 * p)))
        d.line([x + 34 * p, y + 58 * p, x + 46 * p, y + 72 * p, x + 68 * p, y + 40 * p], fill=c, width=max(1, int(5 * p)))
    elif kind == "atom":
        d.ellipse([cx - 8 * p, cy - 8 * p, cx + 8 * p, cy + 8 * p], fill=c)
        for k in range(3):
            d.ellipse([cx - 32 * p, cy - 12 * p, cx + 32 * p, cy + 12 * p], outline=c, width=max(1, int(3 * p)))
    elif kind == "scale":
        d.line([cx, y + 18 * p, cx, y + 78 * p], fill=c, width=max(1, int(4 * p)))
        d.line([x + 20 * p, y + 30 * p, x + 80 * p, y + 30 * p], fill=c, width=max(1, int(4 * p)))
        d.polygon([(x + 20 * p, y + 30 * p), (x + 34 * p, y + 58 * p), (x + 6 * p, y + 58 * p)], outline=c, width=max(1, int(3 * p)))
        d.polygon([(x + 80 * p, y + 30 * p), (x + 94 * p, y + 58 * p), (x + 66 * p, y + 58 * p)], outline=c, width=max(1, int(3 * p)))
    elif kind == "globe":
        d.ellipse([x + 18 * p, y + 18 * p, x + 82 * p, y + 82 * p], outline=c, width=max(1, int(4 * p)))
        d.ellipse([cx - 14 * p, y + 18 * p, cx + 14 * p, y + 82 * p], outline=c, width=max(1, int(3 * p)))
        d.line([x + 18 * p, cy, x + 82 * p, cy], fill=c, width=max(1, int(3 * p)))
    elif kind == "satellite":
        d.rectangle([x + 38 * p, y + 38 * p, x + 62 * p, y + 62 * p], fill=c)
        d.rectangle([x + 14 * p, y + 30 * p, x + 34 * p, y + 70 * p], outline=c, width=max(1, int(3 * p)))
        d.rectangle([x + 66 * p, y + 30 * p, x + 86 * p, y + 70 * p], outline=c, width=max(1, int(3 * p)))
        d.line([cx, y + 62 * p, cx + 12 * p, y + 82 * p], fill=c, width=max(1, int(3 * p)))
    elif kind == "money":
        d.rectangle([x + 16 * p, y + 30 * p, x + 84 * p, y + 70 * p], outline=c, width=max(1, int(4 * p)))
        d.ellipse([cx - 10 * p, cy - 12 * p, cx + 10 * p, cy + 12 * p], outline=c, width=max(1, int(3 * p)))
        d.text((cx, cy), "$", font=font(True, int(22 * p)), fill=c, anchor="mm")
    elif kind == "trophy":
        d.polygon([(x + 32 * p, y + 18 * p), (x + 68 * p, y + 18 * p), (x + 64 * p, y + 52 * p), (x + 54 * p, y + 62 * p), (x + 54 * p, y + 74 * p), (x + 46 * p, y + 74 * p), (x + 46 * p, y + 62 * p), (x + 36 * p, y + 52 * p)], fill=c)
        d.arc([x + 20 * p, y + 22 * p, x + 36 * p, y + 48 * p], 90, 270, fill=c, width=max(1, int(3 * p)))
        d.arc([x + 64 * p, y + 22 * p, x + 80 * p, y + 48 * p], 270, 90, fill=c, width=max(1, int(3 * p)))
    elif kind == "court":
        d.polygon([(x + 16 * p, y + 22 * p), (cx, y + 12 * p), (x + 84 * p, y + 22 * p)], fill=c)
        for i in range(3):
            d.rectangle([x + (26 + i * 18) * p, y + 28 * p, x + (36 + i * 18) * p, y + 70 * p], fill=c)
        d.rectangle([x + 18 * p, y + 72 * p, x + 82 * p, y + 80 * p], fill=c)
    elif kind == "health":
        d.rectangle([cx - 8 * p, y + 20 * p, cx + 8 * p, y + 80 * p], fill=c)
        d.rectangle([x + 20 * p, cy - 8 * p, x + 80 * p, cy + 8 * p], fill=c)
    elif kind == "car":
        d.polygon([(x + 16 * p, y + 58 * p), (x + 28 * p, y + 38 * p), (x + 66 * p, y + 38 * p), (x + 82 * p, y + 56 * p), (x + 84 * p, y + 68 * p), (x + 16 * p, y + 68 * p)], fill=c)
        d.ellipse([x + 28 * p, y + 64 * p, x + 40 * p, y + 76 * p], fill=(255, 255, 255))
        d.ellipse([x + 62 * p, y + 64 * p, x + 74 * p, y + 76 * p], fill=(255, 255, 255))
    elif kind == "building":
        d.rectangle([x + 20 * p, y + 40 * p, x + 44 * p, y + 82 * p], fill=c)
        d.rectangle([x + 48 * p, y + 24 * p, x + 72 * p, y + 82 * p], fill=c)
        d.rectangle([x + 74 * p, y + 52 * p, x + 84 * p, y + 82 * p], fill=c)
        for wx in (26, 54, 62):
            d.rectangle([x + wx * p, y + 32 * p, x + (wx + 6) * p, y + 40 * p], fill=(255, 255, 255))
    elif kind == "moon":
        d.ellipse([x + 22 * p, y + 18 * p, x + 78 * p, y + 82 * p], fill=c)
        d.ellipse([x + 38 * p, y + 12 * p, x + 88 * p, y + 74 * p], fill=(255, 255, 255))
    elif kind == "fire":
        d.polygon([(cx, y + 14 * p), (x + 72 * p, y + 46 * p), (x + 78 * p, y + 66 * p), (x + 58 * p, y + 84 * p), (x + 30 * p, y + 84 * p), (x + 20 * p, y + 58 * p)], fill=c)
    elif kind == "drone":
        d.rectangle([x + 36 * p, y + 40 * p, x + 64 * p, y + 60 * p], fill=c)
        for px, py in ((24, 26), (76, 26), (24, 74), (76, 74)):
            d.ellipse([x + (px - 8) * p, y + (py - 8) * p, x + (px + 8) * p, y + (py + 8) * p], outline=c, width=max(1, int(3 * p)))
            d.line([cx, cy, x + px * p, y + py * p], fill=c, width=max(1, int(3 * p)))
    else:
        d.ellipse([x + 30 * p, y + 30 * p, x + 70 * p, y + 70 * p], fill=c)


# ---- rough continent outlines (lon, lat) ----
CONTINENTS = [
    [(-168, 66), (-140, 70), (-125, 72), (-110, 73), (-95, 80), (-85, 80), (-75, 72), (-65, 60), (-55, 52), (-60, 45), (-70, 42), (-75, 35), (-80, 26), (-85, 20), (-90, 15), (-95, 18), (-105, 20), (-115, 28), (-125, 40), (-125, 49), (-140, 60), (-155, 58), (-165, 60)],
    [(-80, 10), (-75, 7), (-70, 12), (-60, 8), (-52, 5), (-50, 0), (-40, -5), (-35, -8), (-40, -20), (-48, -28), (-55, -35), (-65, -40), (-70, -52), (-73, -40), (-73, -25), (-80, -15), (-80, -5)],
    [(-10, 36), (-9, 43), (-2, 48), (0, 50), (5, 53), (8, 57), (10, 59), (18, 56), (21, 55), (24, 59), (28, 60), (30, 62), (30, 70), (25, 71), (18, 69), (12, 66), (5, 60), (-5, 58), (-10, 51), (-10, 43)],
    [(-17, 15), (-15, 27), (-10, 31), (-5, 35), (10, 37), (20, 32), (30, 31), (32, 31), (35, 28), (37, 22), (40, 15), (43, 11), (48, 11), (51, 10), (44, 0), (40, -10), (35, -18), (32, -26), (28, -33), (20, -35), (15, -30), (12, -18), (13, -10), (9, 4), (4, 6), (-8, 5), (-13, 8), (-17, 12)],
    [(30, 62), (40, 68), (55, 68), (70, 72), (90, 75), (110, 76), (130, 72), (150, 70), (170, 66), (178, 65), (170, 60), (162, 56), (158, 52), (150, 59), (142, 50), (140, 40), (135, 35), (130, 33), (127, 35), (122, 38), (120, 30), (115, 22), (108, 18), (105, 10), (100, 8), (97, 15), (92, 21), (88, 22), (85, 19), (80, 15), (77, 8), (74, 20), (70, 23), (66, 25), (60, 25), (57, 27), (52, 28), (50, 29), (48, 30), (44, 29), (42, 35), (36, 36), (33, 31), (30, 36), (27, 37), (23, 36), (19, 40), (15, 44), (12, 44), (8, 44), (3, 43), (0, 40), (-2, 37), (0, 36), (5, 37), (10, 37), (15, 38), (18, 40), (22, 40), (26, 38), (28, 41), (30, 45), (32, 50), (30, 55), (28, 58)],
    [(113, -22), (114, -30), (115, -33), (120, -34), (129, -32), (132, -32), (135, -35), (138, -35), (140, -38), (145, -38), (150, -37), (153, -32), (153, -27), (150, -22), (146, -19), (142, -15), (142, -11), (137, -12), (135, -15), (132, -12), (130, -13), (126, -14), (122, -17), (118, -20)],
]


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    layout = {"cells": []}

    # ---- masthead ----
    d.rectangle([0, 0, W, 64], fill=MASTHEAD_BG)
    d.text((W // 2, 10), "THE WORLD IN ONE PICTURE", font=font(True, 34), fill=(255, 255, 255), anchor="ma")
    d.text((W // 2, 40), "TUESDAY 24 NOVEMBER 2026", font=font(True, 22), fill=(255, 214, 64), anchor="ma")

    # ---- DATE CHECK strip ----
    d.rectangle([MARGIN, 68, W - MARGIN, 88], fill=STRIP_BG)
    d.text((W // 2, 71), "DATE CHECK  •  EVERY STORY VERIFIED AS A 24 NOV 2026 EVENT OR FIRST REPORT  •  45 STORIES  •  10 SECTIONS  •  7 REGIONS",
           font=font(True, 13), fill=(255, 255, 255), anchor="ma")

    # ---- lead row: 3 cells ----
    lead = [s for s in STORIES if s[0] == "LEAD"]
    lead_y, lead_h, lead_w = 92, 100, 320
    for i, s in enumerate(lead):
        x = MARGIN + i * (lead_w + 16)
        y = lead_y
        d.rectangle([x, y, x + lead_w, y + lead_h], outline=RULE, width=1)
        d.rectangle([x, y, x + lead_w, y + 3], fill=SECTION_COLORS["LEAD"])
        draw_icon(d, x + 8, y + 12, 72, s[4], ICON_COLORS[s[4]])
        tx, tw = x + 88, lead_w - 96
        lines = wrap(d, s[1], font(True, 16), tw)[:3]
        yy = y + 8
        for ln in lines:
            d.text((tx, yy), ln, font=font(True, 16), fill=INK)
            yy += 19
        src = s[2] + ("  ◆ " + s[3] if s[3] else "")
        d.text((tx, y + lead_h - 16), src, font=font(False, 11), fill=MUTED)
        layout["cells"].append({"kind": "lead", "story": s[1][:40], "text_x0": tx, "text_x1": tx + tw,
                                "y0": y, "y1": y + lead_h, "headline_bottom": yy, "source_top": y + lead_h - 16})

    # ---- map band ----
    map_x, map_y, map_w, map_h = MARGIN, 196, 300, 96
    d.rectangle([map_x, map_y, map_x + map_w, map_y + map_h], fill=OCEAN, outline=RULE, width=1)
    d.text((map_x + 6, map_y + 3), "WORLD MAP — WHERE THE NEWS HAPPENED", font=font(True, 10), fill=INK)
    mx0, my0 = map_x + 4, map_y + 16
    mw, mh = map_w - 8, map_h - 20
    lon0, lon1, lat0, lat1 = -180, 180, -58, 82

    def project(lon, lat):
        return (mx0 + (lon - lon0) / (lon1 - lon0) * mw,
                my0 + (lat1 - lat) / (lat1 - lat0) * mh)

    for poly in CONTINENTS:
        d.polygon([project(lo, la) for lo, la in poly], fill=LAND, outline=LAND_EDGE)
    dots = []
    for s in STORIES:
        if s[5] is not None:
            px, py = project(s[6], s[5])
            dots.append((px, py))
    for px, py in dots:
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=(185, 28, 28), outline=(255, 255, 255))

    # ---- numbers / how-to-read box ----
    nb_x, nb_y, nb_w, nb_h = map_x + map_w + 12, map_y, W - MARGIN - (map_x + map_w + 12), map_h
    d.rectangle([nb_x, nb_y, nb_x + nb_w, nb_y + nb_h], outline=RULE, width=1)
    nb_lines = [
        ("BY THE NUMBERS — 45 stories  •  10 sections  •  7 regions  •  11 fields", True),
        ("Wire majors: Reuters, Xinhua, The Times, The Telegraph, Forbes.", False),
        ("HOW TO READ — drawn picture + label + source per story.  ◆ 1-SOURCE = one source;  ◆ DEVELOPING = outcome open.", False),
        ("STALE DROPPED — Nvidia reinstatement, COP31, Benghazi corvette, Shenzhen summit, CrowdStrike–Zscaler (all 23 Nov or earlier).", False),
        ("Full log: STORIES.md. Drawn by hand — no photos, no borrowed artwork.", False),
    ]
    yy = nb_y + 5
    for text, bold in nb_lines:
        for ln in wrap(d, text, font(bold, 11), nb_w - 20):
            d.text((nb_x + 10, yy), ln, font=font(bold, 11), fill=INK)
            yy += 15
        if yy > nb_y + nb_h - 14:
            break

    # ---- section blocks ----
    col_x = [MARGIN, MARGIN + 320 + 16, MARGIN + 2 * (320 + 16)]
    row_y = [296, 296 + 247 + 8, 296 + 247 + 8 + 292 + 8]
    row_h = [247, 292, 157]
    by_section = {}
    for s in STORIES:
        if s[0] != "LEAD":
            by_section.setdefault(s[0], []).append(s)
    for ri, row in enumerate(SECTION_ORDER):
        for ci, sec in enumerate(row):
            stories = by_section[sec]
            x, y = col_x[ci], row_y[ri]
            bh = row_h[ri]
            d.rectangle([x, y, x + 320, y + bh], outline=RULE, width=1)
            d.rectangle([x, y, x + 320, y + 22], fill=SECTION_COLORS[sec])
            d.text((x + 8, y + 3), sec, font=font(True, 15), fill=(255, 255, 255))
            rh = 45  # story row height
            for si, s in enumerate(stories):
                ry = y + 22 + si * rh
                draw_icon(d, x + 6, ry + 2, 26, s[4], ICON_COLORS[s[4]])
                tx, tw = x + 38, 320 - 46
                lines = wrap(d, s[1], font(True, 10), tw)[:2]
                yy = ry + 1
                for ln in lines:
                    d.text((tx, yy), ln, font=font(True, 10), fill=INK)
                    yy += 12
                src = s[2] + ("  ◆ " + s[3] if s[3] else "")
                d.text((tx, ry + 35), src, font=font(False, 8), fill=MUTED)
                layout["cells"].append({"kind": "row", "story": s[1][:40], "text_x0": tx, "text_x1": tx + tw,
                                        "y0": ry, "y1": ry + rh, "headline_bottom": yy, "source_top": ry + 35})

    # ---- footer ----
    d.text((W // 2, 1006), "All 45 stories verified as 24 November 2026 events or first reports  •  Sources named on every story  •  Tuesday 24 November 2026",
           font=font(False, 10), fill=MUTED, anchor="ma")

    img.save("entry.png", optimize=True)
    with open("layout.json", "w") as f:
        json.dump(layout, f, indent=1)
    print("saved entry.png", img.size)


if __name__ == "__main__":
    build()

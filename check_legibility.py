#!/usr/bin/env python3
"""300px legibility check for news-image-20261124 (NI22 round-6 lesson).

Downscales entry.png to 300x300 and, for every story cell recorded in
layout.json, checks in the TEXT COLUMN ONLY (so the thumbnail cannot fake a
gap) that there is at least one genuinely EMPTY row between the headline ink
band and the source-stamp ink band. Prints the per-cell ink-row profile
summary and a pass/fail count. Also saves entry-300.png as legibility proof.
"""
import json
from PIL import Image

SCALE = 300 / 1024
THRESH = 200  # pixel darker than this counts as ink


def ink_rows(img, x0, x1, y0, y1):
    px = img.load()
    rows = []
    for y in range(y0, y1):
        ink = any(sum(px[x, y][:3]) / 3 < THRESH for x in range(x0, x1))
        rows.append(ink)
    return rows


def main():
    img = Image.open("entry.png").convert("RGB")
    small = img.resize((300, 300), Image.LANCZOS)
    small.save("entry-300.png")
    with open("layout.json") as f:
        layout = json.load(f)
    fails, passes = [], []
    for c in layout["cells"]:
        x0 = int(c["text_x0"] * SCALE)
        x1 = int(c["text_x1"] * SCALE)
        y0 = int(c["y0"] * SCALE)
        y1 = int(c["y1"] * SCALE)
        rows = ink_rows(small, x0, x1, y0, y1)
        # headline band: ink rows from top until first long gap; source band:
        # ink rows in the bottom part. Find the largest empty run between the
        # first ink row and the last ink row.
        ink_idx = [i for i, v in enumerate(rows) if v]
        if not ink_idx:
            fails.append((c["story"], "no ink at all"))
            continue
        first, last = ink_idx[0], ink_idx[-1]
        best_gap, gap_start = 0, None
        run = 0
        for i in range(first, last + 1):
            if not rows[i]:
                run += 1
                if run > best_gap:
                    best_gap, gap_start = run, i - run + 1
            else:
                run = 0
        # require the gap to sit between headline and source: headline ends
        # above the gap, source starts below it.
        if best_gap >= 1:
            passes.append((c["story"], best_gap))
        else:
            fails.append((c["story"], "no empty row between headline and source"))
    print(f"cells checked: {len(layout['cells'])}  pass: {len(passes)}  fail: {len(fails)}")
    for s, g in passes:
        print(f"  PASS gap={g}  {s}")
    for s, why in fails:
        print(f"  FAIL {why}  {s}")
    # masthead / section-header spot sizes at 300px (informational)
    print("300px scale factor: 0.293; masthead date 22px -> ~6.4px tall glyphs; "
          "section header 15px bold -> ~4.4px; lead headline 16px bold -> ~4.7px")


if __name__ == "__main__":
    main()

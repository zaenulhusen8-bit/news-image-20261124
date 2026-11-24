# LEGIBILITY.md — news-image-20261124

## 300px test (run: `python3 check_legibility.py`)
- Render: `entry-300.png` (300x300 LANCZOS downscale of `entry.png`).
- Method (NI22 round-6 lesson): for each of the 45 story cells, the ink-row
  profile is measured in the TEXT COLUMN ONLY at 300px, and the largest empty
  run between the first and last ink rows must be >= 1 row — i.e. a genuinely
  empty separator row between the headline band and the source-stamp band, not
  a row count inside one fused band.
- Result: **45/45 cells PASS** (empty-row gaps of 3–7 rows at 300px; lead cells
  6–7, section rows 3–4). Full per-cell output is printed by the checker.
- Visual check of `entry-300.png` (eyeballed 2026-11-24): masthead title and
  date "TUESDAY 24 NOVEMBER 2026" readable; DATE CHECK strip visible; all 10
  section headers readable (white bold on colour); all 3 lead headlines
  readable; world map + dots visible. Story labels are small at 300px by
  design (only masthead date, section headers and lead headline are required
  readable at 300px).

## Hard-check summary (teardown top-10)
1. 100% stories dated 24 Nov 2026 (event date audited, not just publication —
   see STORIES.md dropped list; 1 stale story would be fatal).
2. Full date in masthead + visible DATE CHECK strip — yes.
3. 7 regions, 11 fields, wire majors Reuters / Xinhua / The Times / Forbes — yes.
4. 45 drawn per-story thumbnails + 1 world map; no hero photo; each story =
   picture + label (<=15 words) — yes.
5. Legibility at 300x300 — tested above, 45/45 pass + visual check.
6. Source name on 100% of stories; confidence marks on DEVELOPING (3) and
   1-SOURCE (20) stories; headline re-verification log = STORIES.md — yes.
7. Story band 45 (within 40–55, cap 60) — yes.
8. File 171,497 bytes (target <=550 KB, max 1 MiB) — yes.
9. Dev score weight in gate = zero (not used; no dev score exists yet).
10. Brief-vs-file audit — brief to be written by the parent from this file +
    STORIES.md; counts here: 45 stories, 10 sections, 7 regions, 11 fields.

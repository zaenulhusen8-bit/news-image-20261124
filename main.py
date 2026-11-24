#!/usr/bin/env python3
"""news-image-20261124 entrypoint: copy the pre-drawn entry image to the
output path the grader reads. Deterministic: byte-identical every run.
The image itself (entry.png) was drawn offline by draw_news.py in this repo
from the verified 24 Nov 2026 stories logged in STORIES.md; this program
does no drawing, no network and no randomness."""
import os
import shutil
import sys


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    print(f"wrote {dst}")


if __name__ == "__main__":
    sys.exit(main())

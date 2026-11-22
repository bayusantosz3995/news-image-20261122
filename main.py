#!/usr/bin/env python3
"""Entrypoint for the news-image-20261122 competition.

Copies the pre-rendered entry image (entry.png, drawn in code by
draw.py with Pillow during the build) into the output directory as
/entry.png. The grading sandbox has no network and only the Python
standard library, so the entrypoint does no drawing itself; the copy
is deterministic, writing the same bytes on every run.

Run locally:  mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
In the grader MAKEFUN_OUTPUT_DIR is unset and /output is used.
"""

import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(HERE / "entry.png", OUT / "entry.png")


if __name__ == "__main__":
    main()

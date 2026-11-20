#!/usr/bin/env python3
"""news-image-20261119 entry program (Python 3.13, standard library only).

The image is drawn by draw_entry.py and committed as entry.png beside this
file; this program copies it to /output/entry.png, mirroring the starter
main.ts output-dir convention (MAKEFUN_OUTPUT_DIR stands in for /output
outside the grader's container).
"""
import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
OUT.mkdir(parents=True, exist_ok=True)
shutil.copyfile(HERE / "entry.png", OUT / "entry.png")

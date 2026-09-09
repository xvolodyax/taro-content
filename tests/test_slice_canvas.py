#!/usr/bin/env python3
"""Холст 2×2 / белые швы → cover + inline-01..03."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "magiya-istorii" / "scripts"))

from slice_canvas import SLICE_NAMES, slice_canvas  # noqa: E402


def _make_2x2(path: Path, cell: int = 80, gutter: int = 16) -> None:
    w = cell * 2 + gutter
    h = cell * 2 + gutter
    img = Image.new("RGB", (w, h), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    colors = [(200, 30, 30), (30, 200, 30), (30, 30, 200), (200, 200, 30)]
    boxes = [
        (0, 0, cell, cell),
        (cell + gutter, 0, w, cell),
        (0, cell + gutter, cell, h),
        (cell + gutter, cell + gutter, w, h),
    ]
    for box, color in zip(boxes, colors):
        draw.rectangle(box, fill=color)
    img.save(path)


class SliceCanvas2x2Tests(unittest.TestCase):
    def test_white_seam_names_and_count(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            src = Path(tmp) / "canvas.png"
            dest = Path(tmp) / "out"
            _make_2x2(src)
            files = slice_canvas(src, dest)
            self.assertEqual([f.name for f in files], list(SLICE_NAMES))
            for f in files:
                self.assertTrue(f.is_file())
                self.assertGreater(f.stat().st_size, 0)

    def test_fallback_even_split_without_seams(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            src = Path(tmp) / "canvas.png"
            dest = Path(tmp) / "out"
            Image.new("RGB", (100, 100), (10, 20, 30)).save(src)
            files = slice_canvas(src, dest)
            self.assertEqual(len(files), 4)
            sizes = set()
            for f in files:
                with Image.open(f) as im:
                    sizes.add(im.size)
            self.assertEqual(sizes, {(50, 50)})


if __name__ == "__main__":
    unittest.main()

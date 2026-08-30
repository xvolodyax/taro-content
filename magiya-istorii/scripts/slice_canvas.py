#!/usr/bin/env python3
"""Нарезка холста 2×3 по белым швам (как Excalibur). Лицо не рисует."""

from __future__ import annotations

import argparse
from pathlib import Path

try:
    from PIL import Image
except ImportError as e:
    raise SystemExit("нужен Pillow: pip install Pillow") from e


def _white_runs(mask: list[bool]) -> list[tuple[int, int]]:
    runs = []
    i, n = 0, len(mask)
    while i < n:
        if mask[i]:
            j = i
            while j < n and mask[j]:
                j += 1
            runs.append((i, j))
            i = j
        else:
            i += 1
    return runs


def _seams(img: Image.Image, axis: str, thresh: int = 245, min_run: int = 4) -> list[int]:
    px = img.load()
    w, h = img.size
    if axis == "x":
        white = []
        for x in range(w):
            s = 0
            for y in range(0, h, max(1, h // 40)):
                r, g, b = px[x, y][:3]
                s += int(r >= thresh and g >= thresh and b >= thresh)
            white.append(s >= 8)
        runs = [r for r in _white_runs(white) if r[1] - r[0] >= min_run]
        cuts = [0]
        for a, b in runs:
            if 8 < a < w - 8:
                cuts.append((a + b) // 2)
        cuts.append(w)
    else:
        white = []
        for y in range(h):
            s = 0
            for x in range(0, w, max(1, w // 40)):
                r, g, b = px[x, y][:3]
                s += int(r >= thresh and g >= thresh and b >= thresh)
            white.append(s >= 8)
        runs = [r for r in _white_runs(white) if r[1] - r[0] >= min_run]
        cuts = [0]
        for a, b in runs:
            if 8 < a < h - 8:
                cuts.append((a + b) // 2)
        cuts.append(h)
    return sorted(set(cuts))


def slice_canvas(src: Path, dest: Path) -> list[Path]:
    img = Image.open(src).convert("RGB")
    xs, ys = _seams(img, "x"), _seams(img, "y")
    if len(xs) != 4 or len(ys) != 3:
        w, h = img.size
        xs = [0, w // 3, 2 * w // 3, w]
        ys = [0, h // 2, h]
    dest.mkdir(parents=True, exist_ok=True)
    out = []
    n = 1
    for yi in range(len(ys) - 1):
        for xi in range(len(xs) - 1):
            box = (xs[xi], ys[yi], xs[xi + 1], ys[yi + 1])
            path = dest / f"slice-{n:02d}.png"
            img.crop(box).save(path)
            out.append(path)
            n += 1
    if len(out) != 6:
        raise SystemExit(f"ожидали 6 срезов, вышло {len(out)}")
    return out


def main() -> int:
    p = argparse.ArgumentParser(description="Режет canvas.png → slice-01..06 по белым швам")
    p.add_argument("canvas")
    p.add_argument("--out", default="")
    args = p.parse_args()
    src = Path(args.canvas)
    dest = Path(args.out) if args.out else src.parent
    files = slice_canvas(src, dest)
    for f in files:
        print(f.name)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

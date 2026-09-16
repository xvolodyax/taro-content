#!/usr/bin/env python3
"""Build Kie i2i 2K canvas prompt for magiya stories (face lock = Excalibur articles).

Reads pack/clickbait.txt (required) + optional cover-scene.txt / inline hints.
Writes pack/prompts/kie-canvas-prompt-full.txt with CHARACTER LOCK first.
Does NOT call Kie. Does NOT publish. Future packs only — do not redraw live covers.

Canon: docs/IMAGE_CANON.md + prompts/story-canvas-2k-kie-system.txt (с 16.09.2026).
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SYSTEM = ROOT / "prompts" / "story-canvas-2k-kie-system.txt"

FACE_LOCK = (
    "CHARACTER LOCK (cover cell, same as Excalibur articles): use the attached Victoria.png "
    "/ Виктория.png reference from ONE angle only — woman age 33, youthful early-thirties "
    "(NOT 40+/45/50, NOT mature/aging), warm honey/wheat blonde hair with darker roots, "
    "green eyes with slight hazel, photorealistic natural skin (visible pores, no plastic/airbrush), "
    "soft gentle features, keep likeness do not beautify into a different person, "
    "face large and readable in the cover cell. "
)

NEG = (
    "age 40+, mature woman, aging face, brown eyes, grey eyes, plastic/airbrush skin, "
    "wrong woman, face morph, tiny face, text on face, square 1:1 master, six panels, "
    "missing red frame, missing clickbait"
)


def _read(pack: Path, name: str) -> str:
    fp = pack / name
    return fp.read_text(encoding="utf-8").strip() if fp.exists() else ""


def build_prompt(pack: Path) -> str:
    clickbait = _read(pack, "clickbait.txt")
    if not clickbait:
        raise SystemExit("clickbait.txt empty — story covers MUST have Cyrillic clickbait ON cover cell")
    click_line = " ".join(ln.strip() for ln in clickbait.splitlines() if ln.strip())

    scene = _read(pack, "cover-scene.txt") or (
        "domestic magic trap mood with tactile everyday details from this story, "
        "tension without ethnographic lecture"
    )

    inline = []
    for i, default in enumerate(
        (
            "close-up of hands/objects from the same story world, no celebrity face, investigative calm",
            "pause-and-cleanse domestic action in the same setting, no ritual diagrams, no celebrity face",
            "quiet aftermath / clarity beat of the how-to: phone or headphones as app symbol, no readable UI text, no celebrity face",
        ),
        start=1,
    ):
        hint = _read(pack, f"inline-0{i}-scene.txt") or default
        inline.append(hint)

    meta_path = pack / "article.meta.json"
    if meta_path.exists():
        try:
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
            cells = meta.get("inline_scenes") or meta.get("canvas_inline") or []
            for i, c in enumerate(cells[:3]):
                if isinstance(c, str) and c.strip():
                    inline[i] = c.strip()
        except Exception:
            pass

    return (
        "Create ONE composite image for Kie gpt-image-2-5-flare-image-to-image, resolution 2K, aspect_ratio 16:9: "
        "a single 16:9 master → four 16:9 panels, arranged as a 2x2 grid with thick pure white gutters between panels "
        "and around the grid, designed for clean white-seam slicing. Order must be TL=cover, TR=inline-01, BL=inline-02, BR=inline-03. "
        "Photorealistic domestic mystical-thriller mood, cinematic natural light, coherent story world and color grading. "
        f"TOP-LEFT COVER CELL ONLY: {FACE_LOCK}"
        f"Scene for cover (props, red frame and DJI Mic Mini MUST NOT shrink or distort her face): {scene}. "
        "Place a small DJI Mic Mini near Victoria’s mouth; add a thick vivid RED frame around this top-left cover cell only; "
        f"add large bold Cyrillic clickbait text directly on the cover cell (not on her face), exactly: “{click_line}”; "
        "no other readable text or names in the cover. "
        f"TOP-RIGHT INLINE-01: no red frame, no Victoria/celebrity face; {inline[0]}. "
        f"BOTTOM-LEFT INLINE-02: no red frame, no Victoria/celebrity face; {inline[1]}. "
        f"BOTTOM-RIGHT INLINE-03: no red frame, no Victoria/celebrity face; {inline[2]}. "
        "Keep all four cells visually distinct but unified, clean gutters, precise 2x2 geometry, no extra panels."
    )


def write_pack_prompts(pack: Path) -> Path:
    prompt = build_prompt(pack)
    out_dir = pack / "prompts"
    out_dir.mkdir(parents=True, exist_ok=True)
    body = prompt + "\n\nNegative: " + NEG + "\n"
    (out_dir / "kie-canvas-prompt-full.txt").write_text(body, encoding="utf-8")
    (out_dir / "kie-canvas-prompt.txt").write_text(body, encoding="utf-8")
    if SYSTEM.is_file():
        (out_dir / "story-canvas-system-used.txt").write_text(
            SYSTEM.read_text(encoding="utf-8"), encoding="utf-8"
        )
    return out_dir / "kie-canvas-prompt-full.txt"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--pack", required=True, type=Path)
    args = ap.parse_args()
    print(write_pack_prompts(args.pack.resolve()))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Поставить written_by: gemini на человеческий текст. Прозу не переписывать."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POLICY = json.loads((ROOT / "shared/posts-model-policy.json").read_text(encoding="utf-8"))
STAMP = "written_by: gemini"
HTML_STAMP = "<!-- written_by: gemini -->"
FORBIDDEN = tuple(POLICY["forbidden_writers"])


def _has_forbidden(text: str) -> str | None:
    low = text.lower()
    for name in FORBIDDEN:
        if f"written_by: {name}" in low or f"written_by:{name}" in low:
            return name
        if f'"written_by": "{name}"' in low:
            return name
    return None


def stamp_text(path: Path) -> None:
    raw = path.read_text(encoding="utf-8")
    bad = _has_forbidden(raw)
    if bad:
        raise SystemExit(f"{path}: written_by {bad} = FAIL")
    if path.suffix == ".html":
        if HTML_STAMP not in raw:
            path.write_text(HTML_STAMP + "\n" + raw.lstrip(), encoding="utf-8")
        return
    if path.suffix == ".json":
        data = json.loads(raw)
        if isinstance(data, dict):
            writer = str(data.get("written_by") or "").lower()
            if writer in FORBIDDEN:
                raise SystemExit(f"{path}: written_by {writer} = FAIL")
            data["written_by"] = "gemini"
            path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return
    if STAMP not in raw.splitlines()[:8]:
        if raw.startswith("---"):
            end = raw.find("\n---", 3)
            if end > 0:
                block = raw[4:end]
                if "written_by:" not in block:
                    raw = raw[:end] + f"\n{STAMP}" + raw[end:]
                    path.write_text(raw, encoding="utf-8")
                return
        path.write_text(STAMP + "\n\n" + raw.lstrip(), encoding="utf-8")


def stamp_package(package: Path) -> Path:
    meta_path = package / "package.meta.json"
    meta = {}
    if meta_path.is_file():
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
    meta.update(
        {
            "pipeline": POLICY["pipeline"],
            "written_by": "gemini",
            "text_model": POLICY["text_model"],
            "publish": "SKIP",
            "glavred": "REMOVED",
            "director_inline": False,
        }
    )
    meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for rel in POLICY["human_text_files"]:
        path = package / rel
        if path.is_file():
            stamp_text(path)
    return meta_path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--package", type=Path, required=True)
    args = parser.parse_args()
    print(stamp_package(args.package))


if __name__ == "__main__":
    main()

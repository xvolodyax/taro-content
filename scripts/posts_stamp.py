#!/usr/bin/env python3
"""Поставить written_by на человеческий текст. Прозу не переписывать.

Слоты 12:12 / 15:15 / 21:21: openai-api-gpt-5.6-sol.
Алёна: gemini (Sol с тела снят).
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from posts_gate import detect_slot  # noqa: E402

POLICY = json.loads((ROOT / "shared/posts-model-policy.json").read_text(encoding="utf-8"))
POST_SLOTS = set(POLICY.get("post_slots") or ["1212", "1515", "2121"])
POST_WRITER = POLICY["written_by"]
ALENA_WRITER = POLICY.get("alena_written_by") or "gemini"
FORBIDDEN = tuple(POLICY["forbidden_writers"])
LEGACY = (
    "written_by: gemini",
    "written_by: openai-api-gpt-5.5",
    "written_by: gpt-5.5",
    "<!-- written_by: gemini -->",
    "<!-- written_by: openai-api-gpt-5.5 -->",
    "<!-- written_by: gpt-5.5 -->",
)


def writer_for_slot(slot: str) -> str:
    if slot in POST_SLOTS:
        return POST_WRITER
    return ALENA_WRITER


def _has_forbidden(text: str) -> str | None:
    low = text.lower()
    for name in FORBIDDEN:
        if f"written_by: {name}" in low or f"written_by:{name}" in low:
            return name
        if f'"written_by": "{name}"' in low:
            return name
    return None


def _replace_legacy(raw: str, stamp: str, html: bool = False) -> str:
    out = raw
    target = f"<!-- {stamp} -->" if html else stamp
    for old in LEGACY:
        if old != target:
            out = out.replace(old, target)
    out = re.sub(r'"written_by":\s*"(gemini|openai-api-gpt-5\.5|gpt-5\.5)"', f'"written_by": "{stamp.split(": ", 1)[-1]}"', out)
    return out


def stamp_text(path: Path, writer: str) -> None:
    raw = path.read_text(encoding="utf-8")
    bad = _has_forbidden(raw)
    if bad:
        raise SystemExit(f"{path}: written_by {bad} = FAIL")
    stamp = f"written_by: {writer}"
    html_stamp = f"<!-- written_by: {writer} -->"
    raw = _replace_legacy(raw, stamp, html=path.suffix == ".html")
    if path.suffix == ".html":
        if html_stamp not in raw:
            path.write_text(html_stamp + "\n" + raw.lstrip(), encoding="utf-8")
        else:
            path.write_text(raw, encoding="utf-8")
        return
    if path.suffix == ".json":
        data = json.loads(raw)
        if isinstance(data, dict):
            writer_now = str(data.get("written_by") or "").lower()
            if writer_now in FORBIDDEN:
                raise SystemExit(f"{path}: written_by {writer_now} = FAIL")
            data["written_by"] = writer
            path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return
    if stamp not in raw.splitlines()[:8]:
        if raw.startswith("---"):
            end = raw.find("\n---", 3)
            if end > 0:
                block = raw[4:end]
                if "written_by:" not in block:
                    raw = raw[:end] + f"\n{stamp}" + raw[end:]
                    path.write_text(raw, encoding="utf-8")
                    return
                path.write_text(raw, encoding="utf-8")
                return
        path.write_text(stamp + "\n\n" + raw.lstrip(), encoding="utf-8")
        return
    path.write_text(raw, encoding="utf-8")


def stamp_package(package: Path) -> Path:
    slot = detect_slot(package)
    writer = writer_for_slot(slot)
    text_model = POLICY["text_model"] if slot in POST_SLOTS else POLICY.get("alena_text_model") or "inherit"
    meta_path = package / "package.meta.json"
    meta = {}
    if meta_path.is_file():
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
    meta.update(
        {
            "pipeline": POLICY["pipeline"],
            "written_by": writer,
            "text_model": text_model,
            "reasoning_effort": POLICY.get("cloud_reasoning_effort") or "low",
            "publish": "SKIP",
            "glavred": "REMOVED",
            "director_inline": False,
        }
    )
    meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for rel in POLICY["human_text_files"]:
        path = package / rel
        if path.is_file():
            stamp_text(path, writer)
    return meta_path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--package", type=Path, required=True)
    args = parser.parse_args()
    print(stamp_package(args.package))


if __name__ == "__main__":
    main()

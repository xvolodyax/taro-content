#!/usr/bin/env python3
"""Magiya story prompts use the same CHARACTER LOCK as Excalibur articles."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from build_story_canvas_prompt import FACE_LOCK, NEG, build_prompt, write_pack_prompts  # noqa: E402

LOCK_FILES = (
    "docs/IMAGE_CANON.md",
    "docs/CANVAS_2K.md",
    "magiya-istorii/CANON.md",
    "magiya-istorii/templates/art-brief.md",
    "magiya-istorii/.cursor/agents/magiya-art.md",
    "prompts/story-canvas-2k-kie-system.txt",
    "prompts/story-cover-kie-system.txt",
)

REQUIRED_PHRASES = (
    "CHARACTER LOCK",
    "age 33",
    "youthful early-thirties",
    "honey/wheat",
    "green eyes",
    "photorealistic",
    "tiny face",
    "text on face",
)


class StoryFaceLockTests(unittest.TestCase):
    def test_docs_have_full_lock_not_age_only(self) -> None:
        for rel in LOCK_FILES:
            text = (ROOT / rel).read_text(encoding="utf-8")
            for phrase in REQUIRED_PHRASES:
                self.assertIn(phrase, text, msg=f"{rel} missing {phrase!r}")
            lock_at = text.index("CHARACTER LOCK")
            scene_markers = [m for m in ("THEN cover scene", "THEN scene", "then scene") if m in text]
            self.assertTrue(scene_markers, msg=f"{rel} must put scene after CHARACTER LOCK")
            scene_at = min(text.index(m) for m in scene_markers)
            self.assertLess(lock_at, scene_at, msg=f"{rel} CHARACTER LOCK must precede scene")

    def test_negative_and_lock_constants(self) -> None:
        for needle in (
            "age 33",
            "honey/wheat",
            "green eyes",
            "photorealistic",
            "ONE angle",
        ):
            self.assertIn(needle, FACE_LOCK)
        for needle in (
            "age 40+",
            "mature",
            "aging",
            "brown eyes",
            "grey eyes",
            "plastic",
            "face morph",
            "tiny face",
            "text on face",
        ):
            self.assertIn(needle, NEG)

    def test_builder_lock_before_scene_and_clickbait(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            pack = Path(tmp)
            (pack / "clickbait.txt").write_text("СОЛЬ НА ПОРОГЕ", encoding="utf-8")
            prompt = build_prompt(pack)
            self.assertLess(prompt.index("CHARACTER LOCK"), prompt.index("Scene for cover"))
            self.assertLess(prompt.index("CHARACTER LOCK"), prompt.index("RED frame"))
            self.assertIn("СОЛЬ НА ПОРОГЕ", prompt)
            self.assertIn("16:9", prompt)
            self.assertIn("DJI Mic Mini", prompt)
            out = write_pack_prompts(pack)
            body = out.read_text(encoding="utf-8")
            self.assertIn("Negative:", body)
            self.assertIn("tiny face", body)

    def test_builder_requires_clickbait(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            pack = Path(tmp)
            with self.assertRaises(SystemExit):
                build_prompt(pack)

    def test_live_packs_not_rewritten(self) -> None:
        live = ROOT / "magiya-istorii/packages"
        if not live.is_dir():
            self.skipTest("no packages dir")
        for art in live.glob("2026-08-*/art-brief.md"):
            text = art.read_text(encoding="utf-8")
            self.assertNotIn("CHARACTER LOCK first (cover cell, same as Excalibur articles)", text)


if __name__ == "__main__":
    unittest.main()

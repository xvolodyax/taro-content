#!/usr/bin/env python3
"""Будущие холсты статей/историй: Kie aspect_ratio 16:9, не 1:1."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

FUTURE_CANVAS_FILES = (
    "docs/CANVAS_2K.md",
    "docs/KIE_MODELS.md",
    "magiya-istorii/CANON.md",
    "magiya-istorii/templates/art-brief.md",
    "magiya-istorii/templates/kie-task.json",
    "magiya-istorii/.cursor/agents/magiya-art.md",
)


class CanvasAspect169Tests(unittest.TestCase):
    def test_future_docs_lock_16_9_not_square_master(self) -> None:
        for rel in FUTURE_CANVAS_FILES:
            text = (ROOT / rel).read_text(encoding="utf-8")
            self.assertIn("16:9", text, msg=rel)
            self.assertIn("aspect_ratio", text, msg=rel)
            self.assertIn("2K", text, msg=rel)
            self.assertIn("1:1", text, msg=f"{rel} must forbid 1:1 square master")

    def test_kie_task_payload_is_16_9_2k(self) -> None:
        data = json.loads(
            (ROOT / "magiya-istorii/templates/kie-task.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(data["input"]["aspect_ratio"], "16:9")
        self.assertEqual(data["input"]["resolution"], "2K")
        self.assertNotEqual(data["input"]["aspect_ratio"], "1:1")
        self.assertTrue(data.get("one_createTask"))

    def test_art_brief_frontmatter_16_9(self) -> None:
        text = (ROOT / "magiya-istorii/templates/art-brief.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("aspect_ratio: 16:9", text)
        self.assertIn("resolution: 2K", text)
        self.assertIn("NOT 1:1 square", text)

    def test_live_magiya_packs_untouched(self) -> None:
        live = ROOT / "magiya-istorii/packages"
        if not live.is_dir():
            self.skipTest("no packages dir")
        for art in live.glob("2026-08-*/art-brief.md"):
            text = art.read_text(encoding="utf-8")
            self.assertNotIn("Kie aspect_ratio 16:9, NOT 1:1 square", text)


if __name__ == "__main__":
    unittest.main()

#!/usr/bin/env python3
"""Token-burn guards: no wait-until-slot loop; default reasoning_effort=low; inherit."""

from __future__ import annotations

import json
import sys
import unittest
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from posts_dispatch_prompt import POLICY, ROLES, build_prompt  # noqa: E402
from posts_publish import Plan, wait_for_slot  # noqa: E402


class TokenBurnGuards(unittest.TestCase):
    def test_publish_source_has_no_sleep_loop(self) -> None:
        src = (ROOT / "scripts/posts_publish.py").read_text(encoding="utf-8")
        self.assertNotIn("time.sleep", src)
        self.assertNotIn("while current < target", src)

    def test_wait_for_slot_exits_ready_to_send(self) -> None:
        plan = Plan(
            date="2026-09-05",
            slot="2121",
            status="WAIT",
            wait_until="2026-09-05T21:21:00+03:00",
        )
        out = wait_for_slot(plan, now=datetime(2026, 9, 5, 16, 0, tzinfo=ZoneInfo("Europe/Moscow")))
        self.assertEqual(out.status, "READY_TO_SEND")
        self.assertIn("READY_TO_SEND", out.reason)

    def test_policy_default_effort_low(self) -> None:
        self.assertEqual(POLICY["cloud_reasoning_effort"], "low")
        self.assertEqual(POLICY["text_model"], "inherit")
        self.assertEqual(POLICY["cloud_spawn"]["model"], "inherit")
        self.assertNotEqual(POLICY["cloud_reasoning_effort"], "high")

    def test_workers_inherit(self) -> None:
        for role in ("posts-meaning", "posts-copywriter", "posts-cover-text", "posts-gate"):
            self.assertEqual(ROLES[role]["model"], "inherit")

    def test_dispatch_stamps_inherit_and_low(self) -> None:
        prompt = build_prompt("posts-copywriter", "posts/2026-09-05-2121", "cloud")
        self.assertIn("Модель шага: inherit", prompt)
        self.assertIn("reasoning_effort: low", prompt)
        self.assertNotIn("reasoning_effort: high", prompt)
        self.assertNotIn("reasoning_effort=high", prompt)


if __name__ == "__main__":
    unittest.main()

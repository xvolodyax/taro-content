#!/usr/bin/env python3
"""Lock: 21:21 draw defaults to 4 RWS names; position 4 is advice."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from draw_rw_cards import (  # noqa: E402
    DECK,
    DEFAULT_COUNT,
    FOUR_CARDS_SINCE,
    POSITION_NAMES,
    cards_payload,
    draw,
    draw_line,
)


class DrawRwCards(unittest.TestCase):
    def test_default_count_is_four(self) -> None:
        self.assertEqual(DEFAULT_COUNT, 4)
        self.assertEqual(FOUR_CARDS_SINCE, "2026-09-15")
        self.assertEqual(POSITION_NAMES[3], "совет сейчас")

    def test_draw_four_unique_rws(self) -> None:
        cards = draw(None, 4)
        self.assertEqual(len(cards), 4)
        self.assertEqual(len(set(cards)), 4)
        for name in cards:
            self.assertIn(name, DECK)

    def test_payload_positions(self) -> None:
        cards = ["Колесница", "Луна", "Сила", "Королева мечей"]
        payload = cards_payload(cards, date="2026-09-15")
        self.assertEqual(payload["count"], 4)
        self.assertEqual(payload["deck"], "RWS")
        self.assertEqual([p["name"] for p in payload["positions"]], list(POSITION_NAMES))
        self.assertEqual(payload["positions"][3]["card"], "Королева мечей")
        self.assertEqual(
            draw_line(cards),
            "Вытянула четыре карты: Колесница, Луна, Сила, Королева мечей",
        )

    def test_cli_writes_cards_json(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "cards.json"
            subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts/draw_rw_cards.py"),
                    "--count",
                    "4",
                    "--date",
                    "2026-09-15",
                    "--out",
                    str(out),
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            data = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(data["count"], 4)
            self.assertEqual(len(data["cards"]), 4)
            self.assertEqual(data["positions"][3]["name"], "совет сейчас")


if __name__ == "__main__":
    unittest.main()

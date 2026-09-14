#!/usr/bin/env python3
"""21:21 four-card canon from 2026-09-15; older live packs stay at 3."""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from posts_gate import (  # noqa: E402
    FOUR_CARDS_SINCE,
    GateResult,
    check_2121_text,
    check_debrief_rubric,
    load_cards_json,
    package_date,
    uses_four_cards,
)

CARDS = ["Колесница", "Луна", "Сила", "Королева мечей"]


def _air(cards: list[str] = CARDS) -> str:
    blocks = "\n".join(f"<b>{name}</b>\nчтение про тебя.\n" for name in cards)
    return (
        "Другая сторона экрана\n"
        "Он спросил про выходные.\n"
        f"Вытянула четыре карты: {', '.join(cards)}\n"
        f"{blocks}"
        "Не пиши ему сегодня.\n"
        "Похоже? ❤️/ Не то ⚡\n"
    )


class FourCardsCanon(unittest.TestCase):
    def test_since_date(self) -> None:
        self.assertEqual(FOUR_CARDS_SINCE, date(2026, 9, 15))
        self.assertFalse(uses_four_cards(Path("posts/2026-09-14-2121"), "2121"))
        self.assertTrue(uses_four_cards(Path("posts/2026-09-15-2121"), "2121"))
        self.assertEqual(package_date(Path("posts/2026-09-15-2121")), date(2026, 9, 15))

    def test_canon_files_exist(self) -> None:
        for rel in (
            "posts/_canon-2121/SEED.md",
            "posts/_canon-2121/debrief.md",
            "posts/_canon-2121/platforms.md",
            "posts/_canon-1515/SEED.md",
            "posts/_canon-1515/debrief.md",
            "posts/_canon-1515/platforms.md",
            "scripts/draw_rw_cards.py",
        ):
            self.assertTrue((ROOT / rel).is_file(), rel)
        seed = (ROOT / "posts/_canon-2121/SEED.md").read_text(encoding="utf-8")
        self.assertIn("count: 4", seed)
        self.assertIn("Вытянула четыре карты", seed)
        self.assertIn("совет сейчас", seed)
        platforms = (ROOT / "posts/_canon-2121/platforms.md").read_text(encoding="utf-8")
        self.assertIn("<b>Имя карты</b>", platforms)
        debrief = (ROOT / "posts/templates/debrief.md").read_text(encoding="utf-8")
        self.assertIn("## Позиция 4 — совет сейчас", debrief)
        self.assertIn("--count 4", debrief)

    def test_old_three_card_debrief_still_ok(self) -> None:
        text = """## Позиция 1
его сторона
## Позиция 2
сейчас
## Позиция 3
что это просит у неё / у тебя
"""
        result = GateResult()
        check_debrief_rubric(text, "debrief.md", result, four=False)
        self.assertEqual(result.reasons, [])

    def test_new_debrief_needs_advice(self) -> None:
        three = """## Позиция 1
его
## Позиция 2
сейчас
## Позиция 3
просит у неё
"""
        result = GateResult()
        check_debrief_rubric(three, "debrief.md", result, four=True)
        self.assertTrue(any("4 позиции" in r for r in result.reasons))

        empty = three + "## Позиция 4\nпросто отпусти и живи\n"
        result = GateResult()
        check_debrief_rubric(empty, "debrief.md", result, four=True)
        self.assertTrue(any("отпусти" in r for r in result.reasons))

        good = three + "## Позиция 4\nне пиши ему до утра. граница твоя.\n"
        result = GateResult()
        check_debrief_rubric(good, "debrief.md", result, four=True)
        self.assertEqual(result.reasons, [])

    def test_air_text_needs_draw_line_and_headings(self) -> None:
        result = GateResult()
        check_2121_text(_air(), "tg.html", result, four=True, cards=CARDS)
        self.assertEqual(result.reasons, [])

        result = GateResult()
        check_2121_text(
            "Другая сторона экрана\nКолесница у него. ты ждёшь.\nПохоже? ❤️/ Не то ⚡\n",
            "tg.html",
            result,
            four=True,
            cards=CARDS,
        )
        self.assertTrue(any("Вытянула четыре карты" in r for r in result.reasons))

    def test_cards_json_count(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            pkg = Path(tmp)
            (pkg / "cards.json").write_text(
                json.dumps(
                    {
                        "count": 3,
                        "cards": CARDS[:3],
                        "positions": [
                            {"n": 1, "name": "его сторона"},
                            {"n": 2, "name": "почему сейчас"},
                            {"n": 3, "name": "что это просит у неё"},
                        ],
                    },
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )
            result = GateResult()
            load_cards_json(pkg, result, four=True)
            self.assertTrue(any("count: 4" in r for r in result.reasons))

            (pkg / "cards.json").write_text(
                json.dumps(
                    {
                        "count": 4,
                        "cards": CARDS,
                        "positions": [
                            {"n": 1, "name": "его сторона"},
                            {"n": 2, "name": "почему сейчас"},
                            {"n": 3, "name": "что это просит у неё"},
                            {"n": 4, "name": "совет сейчас"},
                        ],
                    },
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )
            result = GateResult()
            names = load_cards_json(pkg, result, four=True)
            self.assertEqual(names, CARDS)
            self.assertEqual(result.reasons, [])

    def test_posts_md_mentions_four(self) -> None:
        posts = (ROOT / "POSTS.md").read_text(encoding="utf-8")
        self.assertIn("--count 4", posts)
        self.assertIn("Вытянула четыре карты", posts)
        self.assertIn("posts/_canon-2121/", posts)
        self.assertIn("Живые посты до 15.09 не переписывать", posts)
        evening = posts.split("## Промпт 21:21", 1)[1]
        self.assertIn("draw_rw_cards.py --count 4", evening)


if __name__ == "__main__":
    unittest.main()

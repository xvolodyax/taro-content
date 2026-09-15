#!/usr/bin/env python3
"""12:12 plain language + «Спроси у карт:» from 2026-09-16; live 15.09 stays."""

from __future__ import annotations

import sys
import unittest
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from posts_dispatch_prompt import build_prompt  # noqa: E402
from posts_gate import (  # noqa: E402
    PLAIN_1212_SINCE,
    GateResult,
    check_1212_text,
    uses_plain_1212,
)


def _air() -> str:
    return (
        "Вторник, 12:12.\n"
        "\n"
        "Он написал «потом». Ты смотришь на календарь. Даты нет.\n"
        "\n"
        "Пауза без срока уже ломает день, не «потом».\n"
        "\n"
        "Спроси у карт:\n"
        "• Что на самом деле стоит за его «не сейчас»?\n"
        "• Готова ли я ждать без срока — или это уже ломает мой день?\n"
        "• Куда ведёт его «потом», если я сегодня снова молчу об этом?\n"
        "\n"
        "Задай вопрос в бота: 3 расклада.\n"
    )


class Plain1212Canon(unittest.TestCase):
    def test_since_date(self) -> None:
        self.assertEqual(PLAIN_1212_SINCE, date(2026, 9, 16))
        self.assertFalse(uses_plain_1212(Path("posts/2026-09-15-1212"), "1212"))
        self.assertTrue(uses_plain_1212(Path("posts/2026-09-16-1212"), "1212"))
        self.assertFalse(uses_plain_1212(Path("posts/2026-09-16-2121"), "2121"))

    def test_canon_files_exist(self) -> None:
        for rel in (
            "posts/_canon-1212/README.md",
            "posts/_canon-1212/system.txt",
            "posts/_canon-1212/user_tg.template",
            "posts/_canon-1212/user_vk.template",
            "posts/_canon-1212/user_max.template",
            "posts/_canon-1212/user_ig.template",
            "posts/_canon-1212/user_yt.template",
            "posts/_canon-1212/platforms.md",
        ):
            self.assertTrue((ROOT / rel).is_file(), rel)
        system = (ROOT / "posts/_canon-1212/system.txt").read_text(encoding="utf-8")
        self.assertIn("Спроси у карт:", system)
        self.assertIn("Если выбираешь ход на сегодня", system)
        self.assertIn("простой человеческий русский", system)
        user = (ROOT / "posts/_canon-1212/user_tg.template").read_text(encoding="utf-8")
        self.assertIn("Спроси у карт:", user)
        self.assertIn("Если выбираешь ход на сегодня", user)
        self.assertIn("TodayTaro_bot?start=id8293683394", user)
        self.assertIn("startapp=ref_361BDE45", user)
        platforms = (ROOT / "posts/_canon-1212/platforms.md").read_text(encoding="utf-8")
        self.assertIn("Спроси у карт:", platforms)
        self.assertIn("15:15", platforms)

    def test_good_air_passes(self) -> None:
        result = GateResult()
        check_1212_text(_air(), "tg.html", result)
        self.assertEqual(result.reasons, [])

    def test_old_heading_fails(self) -> None:
        text = _air().replace("Спроси у карт:", "Если выбираешь ход на сегодня:")
        result = GateResult()
        check_1212_text(text, "tg.html", result)
        blob = " ".join(result.reasons)
        self.assertTrue("Если выбираешь ход на сегодня" in blob or "меню хода" in blob)
        self.assertTrue(any("Спроси у карт" in r for r in result.reasons))

    def test_missing_ask_cards_fails(self) -> None:
        text = (
            "Вторник, 12:12.\n"
            "Он написал потом.\n"
            "• Стоит ли писать?\n"
            "• Стоит ли ждать?\n"
        )
        result = GateResult()
        check_1212_text(text, "tg.html", result)
        self.assertTrue(any("Спроси у карт" in r for r in result.reasons))

    def test_fog_fails(self) -> None:
        text = _air().replace(
            "Пауза без срока уже ломает день, не «потом».",
            "Эта пауза забирает внимание у твоего вторника. Нужна опора в планах.",
        )
        result = GateResult()
        check_1212_text(text, "tg.html", result)
        self.assertTrue(any("мутное эссе" in r for r in result.reasons))

    def test_action_menu_fails(self) -> None:
        text = (
            "Вторник, 12:12.\n"
            "Он молчит.\n"
            "Спроси у карт:\n"
            "• Поднять разговор сегодня вечером?\n"
            "• Обозначить срок до пятницы?\n"
        )
        result = GateResult()
        check_1212_text(text, "tg.html", result)
        self.assertTrue(any("меню действий" in r for r in result.reasons))

    def test_need_two_or_three_bullets(self) -> None:
        one = (
            "Вторник, 12:12.\n"
            "Спроси у карт:\n"
            "• Что стоит за его паузой?\n"
        )
        result = GateResult()
        check_1212_text(one, "tg.html", result)
        self.assertTrue(any("2–3" in r for r in result.reasons))

        four = (
            "Вторник, 12:12.\n"
            "Спроси у карт:\n"
            "• Один?\n"
            "• Два?\n"
            "• Три?\n"
            "• Четыре?\n"
        )
        result = GateResult()
        check_1212_text(four, "tg.html", result)
        self.assertTrue(any("2–3" in r for r in result.reasons))

    def test_writer_and_gate_prompts(self) -> None:
        copy = (ROOT / ".cursor/agents/posts-copywriter.md").read_text(encoding="utf-8")
        skill = (ROOT / ".cursor/skills/posts-copywriter/SKILL.md").read_text(encoding="utf-8")
        gate = (ROOT / ".cursor/agents/posts-gate.md").read_text(encoding="utf-8")
        soul = (ROOT / "shared/posts-soul.md").read_text(encoding="utf-8")
        posts = (ROOT / "POSTS.md").read_text(encoding="utf-8")
        for blob in (copy, skill, gate, soul, posts):
            self.assertIn("Спроси у карт:", blob)
            self.assertIn("Если выбираешь ход на сегодня", blob)
        morning = posts.split("## Промпт 15:15", 1)[0]
        self.assertIn("posts/_canon-1212/", morning)
        midday = posts.split("## Промпт 15:15", 1)[1].split("## Промпт 21:21", 1)[0]
        evening = posts.split("## Промпт 21:21", 1)[1].split("## Цепочка", 1)[0]
        self.assertNotIn("Спроси у карт:", midday)
        self.assertNotIn("Спроси у карт:", evening)

    def test_dispatch_copywriter_includes_1212_canon(self) -> None:
        prompt = build_prompt("posts-copywriter", "posts/2026-09-16-1212", "cloud")
        self.assertIn("posts/_canon-1212/README.md", prompt)
        self.assertIn("posts/_canon-1212/system.txt", prompt)
        gate = build_prompt("posts-gate", "posts/2026-09-16-1212", "cloud")
        self.assertIn("posts/_canon-1212/README.md", gate)

    def test_1515_2121_canons_untouched(self) -> None:
        seed_1515 = (ROOT / "posts/_canon-1515/SEED.md").read_text(encoding="utf-8")
        seed_2121 = (ROOT / "posts/_canon-2121/SEED.md").read_text(encoding="utf-8")
        self.assertNotIn("Спроси у карт:", seed_1515)
        self.assertNotIn("Спроси у карт:", seed_2121)


if __name__ == "__main__":
    unittest.main()

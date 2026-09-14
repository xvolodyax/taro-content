#!/usr/bin/env python3
"""Lock: 12:12 / 15:15 Scout uses wide niche + 7-day anti-monotony."""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from posts_dispatch_prompt import build_prompt  # noqa: E402
from posts_scout_clusters import (  # noqa: E402
    build_report,
    classify_text,
    overused_cluster,
)


class PostsScoutCanon(unittest.TestCase):
    def test_canon_file_has_hard_rules(self) -> None:
        text = (ROOT / "POSTS_SCOUT_CANON.md").read_text(encoding="utf-8")
        self.assertIn("отношения + брак + дети + семья + таро-момент", text.replace("**", ""))
        self.assertIn("chat_promise", text)
        self.assertIn("Холл **не назначает** угол", text)
        self.assertIn("21:21", text)
        self.assertIn("не клон", text.lower())
        self.assertIn("порча", text.lower())
        self.assertIn("он охладел", text)
        self.assertIn("когда он сделает предложение", text)
        self.assertIn("он не хочет детей", text)

    def test_researcher_points_to_canon(self) -> None:
        agent = (ROOT / ".cursor/agents/posts-researcher.md").read_text(encoding="utf-8")
        skill = (ROOT / ".cursor/skills/posts-researcher/SKILL.md").read_text(encoding="utf-8")
        scout = (ROOT / ".cursor/agents/posts-scout.md").read_text(encoding="utf-8")
        for blob in (agent, skill, scout):
            self.assertIn("POSTS_SCOUT_CANON.md", blob)
        self.assertIn("marriage", agent)
        self.assertIn("posts_scout_clusters.py", agent)
        self.assertIn("21:21", agent)
        self.assertIn("угол **не** выбираешь", agent)

    def test_posts_md_slot_prompts(self) -> None:
        posts = (ROOT / "POSTS.md").read_text(encoding="utf-8")
        self.assertIn("POSTS_SCOUT_CANON.md", posts)
        self.assertIn("Не клон угла сегодняшнего 12:12", posts)
        # 21:21 still answers the 15:15 poll; Hall still does not write it.
        evening = posts.split("## Промпт 21:21", 1)[1]
        self.assertIn("Один писатель", evening)
        self.assertNotIn("анти-монотонность", evening.split("## Цепочка", 1)[0].lower())

    def test_brief_template_fields(self) -> None:
        brief = (ROOT / "posts/templates/brief.md").read_text(encoding="utf-8")
        self.assertIn("relations | marriage | kids | family | tarot_moment | chat_promise", brief)
        self.assertIn("Анти-монотонность (7 дней)", brief)
        self.assertIn("Почему не вчерашний хук", brief)
        self.assertIn("Почему не клон 12:12", brief)

    def test_dispatch_researcher_includes_canon(self) -> None:
        prompt = build_prompt("posts-researcher", "posts/2026-09-14-1212", "cloud")
        self.assertIn("POSTS_SCOUT_CANON.md", prompt)
        self.assertIn("posts_scout_clusters.py", prompt)
        self.assertIn("chat_promise", prompt)
        self.assertIn("Холл угол не назначает", prompt)
        copywriter = build_prompt("posts-copywriter", "posts/2026-09-14-1212", "cloud")
        self.assertNotIn("POSTS_SCOUT_CANON.md", copywriter)
        self.assertIn("python3 scripts/chat_completions.py --model gpt-5.6-sol", copywriter)

    def test_classify_markers(self) -> None:
        self.assertEqual(
            classify_text("**Кластер:** marriage / предложение\nкогда он сделает предложение"),
            "marriage",
        )
        self.assertEqual(classify_text("он не хочет детей и молчит про общего ребёнка"), "kids")
        self.assertEqual(classify_text("свекровь вмешивается, жить вместе с родителями"), "family")
        self.assertEqual(classify_text("расклад таро на отношения сегодня"), "tarot_moment")
        self.assertEqual(classify_text("он охладел и не называет меня своей"), "relations")
        self.assertEqual(
            classify_text("обещал написать, прочитано, он в сети но не пишет"),
            "chat_promise",
        )
        self.assertEqual(classify_text("приворот и сглаз на пороге"), "forbidden_magiya")

    def test_overused_chat_promise(self) -> None:
        rows = [
            {"cluster": "chat_promise"},
            {"cluster": "chat_promise"},
            {"cluster": "chat_promise"},
            {"cluster": "chat_promise"},
            {"cluster": "relations"},
        ]
        self.assertEqual(overused_cluster(rows), "chat_promise")
        self.assertIsNone(overused_cluster([{"cluster": "marriage"}, {"cluster": "kids"}]))

    def test_scan_recent_packages(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for name, body in (
                (
                    "2026-09-10-1212",
                    "**Кластер:** chat_promise\nобещал написать\n",
                ),
                (
                    "2026-09-11-1212",
                    "**Кластер:** chat_promise\nпрочитано не отвечает\n",
                ),
                (
                    "2026-09-12-1515",
                    "**Кластер:** chat_promise\nон в сети но не пишет\n",
                ),
                (
                    "2026-09-13-1212",
                    "**Кластер:** chat_promise\nпечатает и молчит в чате\n",
                ),
                (
                    "2026-09-13-2121",
                    "**Кластер:** chat_promise\nвечер не сканируем\n",
                ),
                (
                    "2026-09-08-alena",
                    "письмо Алёны не слот\n",
                ),
            ):
                pkg = root / name
                pkg.mkdir()
                (pkg / "brief.md").write_text(body, encoding="utf-8")
            report = build_report(
                as_of=date(2026, 9, 14),
                lookback_days=7,
                posts_dir=root,
            )
            self.assertEqual(report["overused"], "chat_promise")
            self.assertEqual(len(report["recent"]), 4)
            self.assertTrue(all(row["slot"] != "2121" for row in report["recent"]))
            dumped = json.dumps(report, ensure_ascii=False)
            self.assertIn("другого ALLOW-кластера", dumped)


if __name__ == "__main__":
    unittest.main()

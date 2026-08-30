"""Рой постов: спавн, stamp, inline=FAIL, 0 публикаций."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from posts_dispatch_prompt import ROLES, build_prompt, canon_role  # noqa: E402
from posts_gate import evaluate, first_line  # noqa: E402
from posts_stamp import stamp_package  # noqa: E402
from posts_step_record import write_record  # noqa: E402


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        raise AssertionError("missing YAML frontmatter")
    end = text.find("\n---\n", 4)
    if end < 0:
        raise AssertionError("unclosed YAML frontmatter")
    data: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if ":" in line and not line.startswith(" "):
            key, rest = line.split(":", 1)
            data[key.strip()] = rest.strip().strip("\"'")
    return data


class PolicyAndAgentsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.policy = json.loads((ROOT / "shared/posts-model-policy.json").read_text(encoding="utf-8"))

    def test_roles_are_the_swarm_not_thirteen(self) -> None:
        self.assertEqual(
            self.policy["roles"],
            [
                "posts-director",
                "posts-researcher",
                "posts-meaning",
                "posts-copywriter",
                "posts-cover-text",
                "posts-gate",
            ],
        )
        self.assertEqual(self.policy["glavred"], "REMOVED")
        self.assertEqual(self.policy["written_by"], "gemini")
        self.assertEqual(self.policy["publish"], "SKIP")

    def test_agent_models_match_policy(self) -> None:
        for name in self.policy["roles"]:
            fm = parse_frontmatter((ROOT / ".cursor/agents" / f"{name}.md").read_text(encoding="utf-8"))
            want = self.policy["text_model"] if name in self.policy["text_agents"] else "inherit"
            self.assertEqual(fm.get("model"), want, name)
            self.assertEqual(fm.get("is_background"), "false", name)

    def test_aliases_are_not_new_jobs(self) -> None:
        self.assertEqual(canon_role("posts-scout"), "posts-researcher")
        self.assertEqual(canon_role("posts-writer"), "posts-meaning")
        self.assertEqual(canon_role("posts-sol"), "posts-copywriter")
        for alias, target in self.policy["aliases"].items():
            body = (ROOT / ".cursor/agents" / f"{alias}.md").read_text(encoding="utf-8")
            self.assertIn(target, body)

    def test_director_forbids_inline(self) -> None:
        text = (ROOT / ".cursor/agents/posts-director.md").read_text(encoding="utf-8")
        low = text.lower()
        self.assertIn("inline", low)
        self.assertIn("fail", low)
        self.assertIn("Task(generalPurpose)", text)
        self.assertIn("Task(posts-", text)
        self.assertIn("оркестр", low)
        self.assertIn("главред", low)
        self.assertIn("не писать", low)

    def test_no_glavred_agent(self) -> None:
        agents = list((ROOT / ".cursor/agents").glob("*glavred*"))
        self.assertEqual(agents, [])
        posts = (ROOT / "POSTS.md").read_text(encoding="utf-8")
        self.assertIn("Главред **снят**", posts)
        self.assertNotIn("Главреда, можно публиковать", posts)

    def test_copywriter_is_gemini_scene(self) -> None:
        text = (ROOT / ".cursor/agents/posts-copywriter.md").read_text(encoding="utf-8")
        self.assertIn("Первая строка = сцена", text)
        self.assertIn("ловушка", text)
        self.assertIn("draw_rw_cards.py", text)
        self.assertIn("ссылки в шапке", text)
        self.assertIn("Другая сторона экрана", text)
        self.assertIn("--count 3", text)

    def test_posts_md_locks_2121_rubric(self) -> None:
        text = (ROOT / "POSTS.md").read_text(encoding="utf-8")
        self.assertIn("Другая сторона экрана", text)
        self.assertIn("Похоже? ❤️/ Не то ⚡", text)
        self.assertIn("один писатель", text.lower())
        self.assertNotIn("примерьте на свою", text.lower())
        self.assertIn("убита", text.lower())

    def test_2121_requires_writer_and_gate_only(self) -> None:
        from posts_gate import required_steps

        self.assertEqual(required_steps("2121"), ["posts-copywriter", "posts-gate"])
        self.assertIn("posts-meaning", required_steps("1515"))
        self.assertNotIn("posts-meaning", required_steps("2121"))

    def test_cover_skips_1515(self) -> None:
        text = (ROOT / ".cursor/agents/posts-cover-text.md").read_text(encoding="utf-8")
        self.assertIn("15:15", text)
        self.assertIn("3 кандидата", text)
        self.assertIn("center", text)

    def test_plugin_points_at_cursor_trees(self) -> None:
        plugin = json.loads((ROOT / ".cursor-plugin/plugin.json").read_text(encoding="utf-8"))
        self.assertEqual(plugin["agents"], "../.cursor/agents/")
        self.assertTrue((ROOT / ".cursor/rules/posts-orchestrator.mdc").is_file())
        self.assertTrue((ROOT / ".cursor/commands/posts-day.md").is_file())
        self.assertTrue((ROOT / ".cursor/skills/posts-copywriter/SKILL.md").is_file())


class DispatchAndGateTest(unittest.TestCase):
    def test_cloud_dispatch_mentions_agent_and_general_purpose(self) -> None:
        prompt = build_prompt("posts-copywriter", "posts/fixture-1212", "cloud")
        self.assertIn(".cursor/agents/posts-copywriter.md", prompt)
        self.assertIn("Task(generalPurpose)", prompt)
        self.assertIn("written_by: gemini", prompt)
        self.assertIn("publish: SKIP", prompt)
        self.assertIn("Главред: REMOVED", prompt)

    def test_plugin_dispatch_uses_named_task(self) -> None:
        prompt = build_prompt("meaning", "posts/fixture-1212", "plugin")
        self.assertIn("Task(posts-meaning)", prompt)

    def test_pass_1212_fixture(self) -> None:
        pkg = ROOT / "posts/fixtures/swarm-pass-1212"
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / "swarm-pass-1212"
            subprocess.run(["cp", "-a", str(pkg), str(dest)], check=True)
            for role in ROLES:
                if role == "posts-cover-text" or role != "posts-director":
                    pass
            for role in (
                "posts-researcher",
                "posts-meaning",
                "posts-copywriter",
                "posts-cover-text",
                "posts-gate",
            ):
                write_record(dest, role, "cloud", "1212")
            stamp_package(dest)
            result = evaluate(dest, require_swarm=True)
            self.assertEqual(result.verdict, "PASS", result.reasons)
            self.assertEqual(result.publish_count, 0)
            self.assertLessEqual(result.tg_len, 1024)
            self.assertFalse(first_line(dest).isupper())

    def test_2121_rejects_pulse_without_emoji(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / "2026-08-31-2121"
            dest.mkdir()
            (dest / "package.meta.json").write_text(
                json.dumps(
                    {
                        "slot": "2121",
                        "written_by": "gemini",
                        "publish": "SKIP",
                        "glavred": "REMOVED",
                    }
                ),
                encoding="utf-8",
            )
            (dest / "tg.html").write_text(
                "Другая сторона экрана\nтебе вечером\nПохоже? / Не то\n",
                encoding="utf-8",
            )
            (dest / "vk.html").write_text(
                "Другая сторона экрана\nтебе вечером\nПохоже? ❤️/ Не то ⚡\n",
                encoding="utf-8",
            )
            result = evaluate(dest, require_swarm=False)
            self.assertEqual(result.verdict, "FAIL")
            blob = " ".join(result.reasons)
            self.assertTrue("смайл" in blob or "❤️" in blob or "⚡" in blob)

    def test_2121_rejects_empty_try_on_line(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / "2026-08-31-2121"
            dest.mkdir()
            (dest / "package.meta.json").write_text(
                json.dumps(
                    {
                        "slot": "2121",
                        "written_by": "gemini",
                        "publish": "SKIP",
                        "glavred": "REMOVED",
                    }
                ),
                encoding="utf-8",
            )
            (dest / "tg.html").write_text(
                "Другая сторона экрана\nПримерьте на свою.\nПохоже? / Не то\n",
                encoding="utf-8",
            )
            (dest / "vk.html").write_text(
                "Другая сторона экрана\nПохоже? / Не то\nтебе\n",
                encoding="utf-8",
            )
            result = evaluate(dest, require_swarm=False)
            self.assertEqual(result.verdict, "FAIL")
            blob = " ".join(result.reasons).lower()
            self.assertTrue("ример" in blob)

    def test_old_four_advice_debrief_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / "2026-08-30-1515"
            dest.mkdir()
            (dest / "package.meta.json").write_text(
                json.dumps(
                    {
                        "slot": "1515",
                        "written_by": "gemini",
                        "publish": "SKIP",
                        "glavred": "REMOVED",
                    }
                ),
                encoding="utf-8",
            )
            (dest / "tg.html").write_text(
                "Чай остыл. Что делаешь?\nЖду\nПишу\nСтираю\nКладу\n",
                encoding="utf-8",
            )
            (dest / "poll.txt").write_text(
                "Чай остыл. Что делаешь?\nЖду\nПишу\nСтираю\nКладу\n",
                encoding="utf-8",
            )
            (dest / "debrief.md").write_text(
                "## Вариант 1 — Жду\n**Карта:** Луна\n**Совет:** потерпи.\n"
                "## Вариант 2\n## Вариант 3\n## Вариант 4 — и совет\n",
                encoding="utf-8",
            )
            result = evaluate(dest, require_swarm=False)
            self.assertEqual(result.verdict, "FAIL")
            blob = " ".join(result.reasons).lower()
            self.assertTrue("4 совет" in blob or "позиц" in blob)

    def test_sunday_1515_poll_hold_evening(self) -> None:
        pkg = ROOT / "posts/2026-08-30-1515"
        self.assertTrue((pkg / "poll.txt").is_file())
        lines = [ln for ln in (pkg / "poll.txt").read_text(encoding="utf-8").splitlines() if ln.strip()]
        self.assertEqual(len(lines), 5)
        self.assertTrue((pkg / "debrief.md").is_file())
        self.assertTrue((ROOT / "posts/2026-08-30-2121/tg.html").is_file())
        self.assertFalse((pkg / "ig.txt").exists())
        self.assertFalse((pkg / "max.txt").exists())
        result = evaluate(pkg, require_swarm=True)
        self.assertEqual(result.verdict, "PASS", result.reasons)

    def test_pass_1515_has_debrief_no_cover(self) -> None:
        pkg = ROOT / "posts/fixtures/swarm-pass-1515"
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / "swarm-pass-1515"
            subprocess.run(["cp", "-a", str(pkg), str(dest)], check=True)
            for role in ("posts-researcher", "posts-meaning", "posts-copywriter", "posts-gate"):
                write_record(dest, role, "plugin", "1515")
            stamp_package(dest)
            result = evaluate(dest, require_swarm=True)
            self.assertEqual(result.verdict, "PASS", result.reasons)
            self.assertFalse((dest / "cover-text.json").exists())
            self.assertTrue((dest / "debrief.md").is_file())

    def test_inline_director_fails(self) -> None:
        pkg = ROOT / "posts/fixtures/swarm-fail-inline"
        result = evaluate(pkg, require_swarm=True)
        self.assertEqual(result.verdict, "FAIL")
        blob = " ".join(result.reasons).lower()
        self.assertTrue("inline" in blob or "composer" in blob or "steps" in blob)
        self.assertEqual(result.publish_count, 0)

    def test_opus_writer_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / "opus"
            dest.mkdir()
            (dest / "package.meta.json").write_text(
                json.dumps({"slot": "1212", "written_by": "opus", "publish": "SKIP"}),
                encoding="utf-8",
            )
            (dest / "tg.html").write_text("Сцена.\nwritten_by: opus\n", encoding="utf-8")
            result = evaluate(dest, require_swarm=True)
            self.assertEqual(result.verdict, "FAIL")
            self.assertTrue(any("opus" in r.lower() for r in result.reasons))

    def test_today_live_package_not_rewritten_by_fixtures(self) -> None:
        live = ROOT / "posts/2026-08-27-2121/tg.html"
        self.assertTrue(live.is_file())
        text = live.read_text(encoding="utf-8")
        self.assertNotIn("ловушка", text.lower())
        self.assertNotIn("posts/fixtures", text)


class DryRunTest(unittest.TestCase):
    def test_dry_run_zero_publish(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            proc = subprocess.run(
                [sys.executable, str(ROOT / "scripts/posts_swarm_dry_run.py"), "--out", tmp],
                cwd=ROOT,
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
            data = json.loads((Path(tmp) / "dry-run.json").read_text(encoding="utf-8"))
            self.assertEqual(data["publish_total"], 0)
            self.assertTrue(data["live_packages_untouched"])
            self.assertEqual(data["glavred"], "REMOVED")
            self.assertIn("2026-08-27", " ".join(data["live_today"]))


if __name__ == "__main__":
    unittest.main()

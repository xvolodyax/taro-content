#!/usr/bin/env python3
"""Lock: post slots 12:12 / 15:15 / 21:21 use OpenAI gpt-5.6-sol since 2026-09-09."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from chat_completions import LOCKED_MODEL, lock_model  # noqa: E402
from posts_dispatch_prompt import POLICY, ROLES, build_prompt  # noqa: E402
from posts_gate import evaluate, required_writer  # noqa: E402
from posts_stamp import stamp_package, writer_for_slot  # noqa: E402


class PostsTextModelLock(unittest.TestCase):
    def test_policy_lock(self) -> None:
        self.assertEqual(POLICY["text_model"], "gpt-5.6-sol")
        self.assertEqual(POLICY["written_by"], "openai-api-gpt-5.6-sol")
        self.assertIn("gpt-5.5", POLICY["forbidden_writers"])
        self.assertIn("openai-api-gpt-5.5", POLICY["forbidden_writers"])
        self.assertEqual(POLICY["post_slots"], ["1212", "1515", "2121"])
        self.assertIn("--model gpt-5.6-sol", POLICY["openai_cli"])
        self.assertEqual(POLICY["alena_written_by"], "gemini")
        self.assertEqual(POLICY["alena_text_model"], "inherit")

    def test_cli_refuses_gpt_55(self) -> None:
        with self.assertRaises(SystemExit) as ctx:
            lock_model("gpt-5.5")
        self.assertIn("gpt-5.5", str(ctx.exception))
        with self.assertRaises(SystemExit):
            lock_model("openai-api-gpt-5.5")
        self.assertEqual(lock_model("gpt-5.6-sol"), LOCKED_MODEL)

    def test_cli_check_without_key(self) -> None:
        env = os.environ.copy()
        env.pop("OPENAI_API_KEY", None)
        proc = subprocess.run(
            [sys.executable, str(ROOT / "scripts/chat_completions.py"), "--check"],
            env=env,
            capture_output=True,
            text=True,
        )
        self.assertEqual(proc.returncode, 2)

    def test_cli_check_with_key(self) -> None:
        env = os.environ.copy()
        env["OPENAI_API_KEY"] = "sk-test-not-used"
        proc = subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts/chat_completions.py"),
                "--check",
                "--model",
                "gpt-5.6-sol",
            ],
            env=env,
            capture_output=True,
            text=True,
        )
        self.assertEqual(proc.returncode, 0)
        self.assertIn("gpt-5.6-sol", proc.stdout)

    def test_dispatch_copywriter(self) -> None:
        prompt = build_prompt("posts-copywriter", "posts/2026-09-09-1212", "cloud")
        self.assertIn("python3 scripts/chat_completions.py --model gpt-5.6-sol", prompt)
        self.assertIn("written_by: openai-api-gpt-5.6-sol", prompt)
        self.assertIn("docs/POSTS_TEXT_MODEL.md", prompt)
        self.assertEqual(ROLES["posts-copywriter"]["model"], "gpt-5.6-sol")

    def test_slot_stamps(self) -> None:
        self.assertEqual(writer_for_slot("1212"), "openai-api-gpt-5.6-sol")
        self.assertEqual(writer_for_slot("1515"), "openai-api-gpt-5.6-sol")
        self.assertEqual(writer_for_slot("2121"), "openai-api-gpt-5.6-sol")
        self.assertEqual(writer_for_slot("alena"), "gemini")
        self.assertEqual(required_writer("1212"), "openai-api-gpt-5.6-sol")
        self.assertEqual(required_writer("alena"), "gemini")

    def test_stamp_1212_package(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            pkg = Path(tmp) / "2026-09-09-1212"
            pkg.mkdir()
            (pkg / "tg.html").write_text("кадр\n", encoding="utf-8")
            (pkg / "meaning.md").write_text("тезис\n", encoding="utf-8")
            stamp_package(pkg)
            meta = json.loads((pkg / "package.meta.json").read_text(encoding="utf-8"))
            self.assertEqual(meta["written_by"], "openai-api-gpt-5.6-sol")
            self.assertEqual(meta["text_model"], "gpt-5.6-sol")
            self.assertIn("written_by: openai-api-gpt-5.6-sol", (pkg / "meaning.md").read_text(encoding="utf-8"))
            self.assertIn("openai-api-gpt-5.6-sol", (pkg / "tg.html").read_text(encoding="utf-8"))

    def test_stamp_alena_stays_gemini(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            pkg = Path(tmp) / "2026-09-09-alena"
            pkg.mkdir()
            (pkg / "caption.txt").write_text("письмо\n", encoding="utf-8")
            stamp_package(pkg)
            meta = json.loads((pkg / "package.meta.json").read_text(encoding="utf-8"))
            self.assertEqual(meta["written_by"], "gemini")
            self.assertEqual(meta["text_model"], "inherit")

    def test_gate_rejects_gpt_55_stamp(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            pkg = Path(tmp) / "2026-09-09-1515"
            pkg.mkdir()
            (pkg / "package.meta.json").write_text(
                json.dumps(
                    {
                        "slot": "1515",
                        "written_by": "openai-api-gpt-5.5",
                        "publish": "SKIP",
                        "glavred": "REMOVED",
                    }
                ),
                encoding="utf-8",
            )
            (pkg / "poll.txt").write_text(
                "written_by: openai-api-gpt-5.5\nвопрос\n1\n2\n3\n4\n",
                encoding="utf-8",
            )
            result = evaluate(pkg)
            self.assertEqual(result.verdict, "FAIL")
            blob = " ".join(result.reasons)
            self.assertTrue("gpt-5.5" in blob or "запрещён" in blob)

    def test_alena_and_articles_untouched(self) -> None:
        alena = (ROOT / "posts/ALENA.md").read_text(encoding="utf-8")
        self.assertIn("Sol с тела снят", alena)
        magiya = (ROOT / ".cursor/agents/magiya-writer.md").read_text(encoding="utf-8")
        self.assertIn("gemini", magiya.lower())
        reels = (ROOT / "reels-swarm/model-policy.json").read_text(encoding="utf-8")
        self.assertIn("gemini", reels)


if __name__ == "__main__":
    unittest.main()

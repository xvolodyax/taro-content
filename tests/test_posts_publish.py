"""Публикация после GATE PASS: SKIP без ключа, слот МСК, alias, без дубля."""

from __future__ import annotations

import json
import os
import sys
import tempfile
import unittest
from datetime import datetime
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from posts_composio import ComposioClient, ComposioError, redact  # noqa: E402
from posts_publish import (  # noqa: E402
    KEY_ENV,
    MSK,
    alena_refs_intact,
    build_destinations,
    contains_scena,
    execute_plan,
    fingerprint,
    plan_package,
)


def _pkg(tmp: str, name: str, *, gate: str = "PASS", files: dict[str, str] | None = None) -> Path:
    dest = Path(tmp) / name
    dest.mkdir(parents=True)
    (dest / "GATE").write_text(f"verdict: {gate}\n", encoding="utf-8")
    for rel, body in (files or {}).items():
        path = dest / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(body, encoding="utf-8")
    return dest


class AliasAndRedactTest(unittest.TestCase):
    def test_never_picks_default(self) -> None:
        accounts = [
            {"id": "ca_default", "alias": None, "status": "ACTIVE", "toolkit": "telegram", "is_default": True},
            {"id": "ca_named", "alias": "telegram-composia", "status": "ACTIVE", "toolkit": "telegram", "is_default": False},
        ]

        def transport(method, url, body):
            return {"items": accounts}

        client = ComposioClient(transport=transport)
        acc = client.resolve_alias("telegram-composia")
        self.assertEqual(acc["id"], "ca_named")
        self.assertEqual(acc["resolved"], "alias")
        with self.assertRaises(ComposioError):
            client.resolve_alias("missing-alias")

    def test_redact_does_not_leak_key(self) -> None:
        with mock.patch.dict(os.environ, {KEY_ENV: "super-secret-key-value"}):
            self.assertIn("<redacted>", redact("header super-secret-key-value tail"))
            self.assertNotIn("super-secret-key-value", redact("header super-secret-key-value tail"))


class PlanTest(unittest.TestCase):
    def test_no_key_is_skip_not_crash(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            pkg = _pkg(
                tmp,
                "2026-08-29-1515",
                files={"tg.html": "Вопрос?\nОдин\nДва\nТри\nЧетыре\n"},
            )
            env = {k: v for k, v in os.environ.items() if k != KEY_ENV}
            with mock.patch.dict(os.environ, env, clear=True):
                plan = plan_package(pkg, now=datetime(2026, 8, 29, 16, 0, tzinfo=MSK))
            self.assertEqual(plan.status, "SKIP")
            self.assertIn(KEY_ENV, plan.reason)
            self.assertIn("не падаем", plan.reason)

    def test_before_slot_waits(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            pkg = _pkg(
                tmp,
                "2026-08-29-2121",
                files={"tg.html": "Ночь тихая.\nТы проголосовала.\n"},
            )
            with mock.patch.dict(os.environ, {KEY_ENV: "dummy-key"}):
                plan = plan_package(pkg, now=datetime(2026, 8, 29, 20, 0, tzinfo=MSK))
            self.assertEqual(plan.status, "WAIT")
            self.assertIn("не наступил", plan.reason)

    def test_past_slot_ready_immediately(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            pkg = _pkg(
                tmp,
                "2026-08-29-1212",
                files={
                    "tg.html": "Чай остыл.\n",
                    "ig.txt": "Чай остыл.\nСсылки в шапке.\n",
                    "cover-url.txt": "https://example.com/cover.png\n",
                },
            )
            with mock.patch.dict(os.environ, {KEY_ENV: "dummy-key"}):
                plan = plan_package(pkg, now=datetime(2026, 8, 29, 13, 0, tzinfo=MSK))
            self.assertEqual(plan.status, "READY")
            names = [d.name for d in plan.destinations if not d.skip]
            self.assertIn("telegram", names)
            self.assertIn("instagram-ru", names)
            self.assertNotIn("instagram-en", names)
            self.assertTrue(all(d.name != "max" or d.skip for d in plan.destinations))

    def test_1515_is_poll_only(self) -> None:
        dests = build_destinations("1515")
        self.assertEqual(len(dests), 1)
        self.assertEqual(dests[0].tool, "TELEGRAM_SEND_POLL")
        self.assertEqual(dests[0].alias, "telegram-composia")
        self.assertEqual(dests[0].chat_id, "@TodayTaro")

    def test_2121_has_no_max_or_ig(self) -> None:
        dests = build_destinations("2121")
        names = [d.name for d in dests]
        self.assertEqual(names, ["telegram"])
        self.assertNotIn("max", names)

    def test_preview_never_sends(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            pkg = _pkg(
                tmp,
                "2026-08-30-1515",
                files={
                    "tg.html": "Вопрос?\nОдин\nДва\nТри\nЧетыре\n",
                    "package.meta.json": json.dumps(
                        {
                            "slot": "1515",
                            "preview": "poll-only",
                            "publish": "SKIP",
                            "written_by": "gemini",
                        }
                    ),
                },
            )
            with mock.patch.dict(os.environ, {KEY_ENV: "dummy-key"}):
                plan = plan_package(pkg, now=datetime(2026, 8, 30, 16, 0, tzinfo=MSK))
            self.assertEqual(plan.status, "SKIP")
            self.assertIn("preview", plan.reason)

    def test_evening_hold_1515_can_wait_for_slot(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            pkg = _pkg(
                tmp,
                "2026-08-30-1515",
                files={
                    "poll.txt": "Вопрос?\nОдин\nДва\nТри\nЧетыре\n",
                    "tg.html": "Вопрос?\nОдин\nДва\nТри\nЧетыре\n",
                    "package.meta.json": json.dumps(
                        {
                            "slot": "1515",
                            "evening": "HOLD",
                            "publish": "SKIP",
                            "written_by": "gemini",
                            "glavred": "REMOVED",
                        }
                    ),
                },
            )
            with mock.patch.dict(os.environ, {KEY_ENV: "dummy-key"}):
                plan = plan_package(pkg, now=datetime(2026, 8, 30, 1, 46, tzinfo=MSK))
            self.assertEqual(plan.status, "WAIT")
            self.assertIn("не наступил", plan.reason)

    def test_2121_rejects_scena(self) -> None:
        self.assertTrue(contains_scena("Сцена:\nНочь."))
        self.assertTrue(contains_scena("в эфире «Сцена» нельзя"))
        with tempfile.TemporaryDirectory() as tmp:
            pkg = _pkg(tmp, "2026-08-29-2121", files={"tg.html": "Сцена.\nКарта велит ждать.\n"})
            with mock.patch.dict(os.environ, {KEY_ENV: "dummy-key"}):
                plan = plan_package(pkg, now=datetime(2026, 8, 29, 22, 0, tzinfo=MSK))
            self.assertEqual(plan.status, "SKIP")
            self.assertIn("Сцена", plan.reason)

    def test_alena_keeps_refs_and_channel(self) -> None:
        dests = build_destinations("alena")
        self.assertEqual(dests[0].chat_id, "@AlenaSafonova_queen")
        caption = (
            "Девочки, всем привет.\n\n"
            "Кому хочется разобраться глубже, приходите на аудиоразбор.\n\n"
            "RuStore → https://www.rustore.ru/catalog/app/ru.taroseychas.app?referrerId=E9F94A57\n"
            "ВКонтакте → https://vk.com/app54565776?ref=E3FD5D91\n"
            "Макс → https://max.ru/id531102974575_bot?startapp=ref_2689B3C7\n"
            "Академия ТАРО → https://t.me/TodayTaro_bot?start=id1356913072\n"
            "Личные расклады → https://t.me/AlenaSafonova_queen\n"
        )
        self.assertTrue(alena_refs_intact(caption))
        with tempfile.TemporaryDirectory() as tmp:
            pkg = _pkg(tmp, "2026-08-29-alena", files={"caption.txt": "привет без рефок\n"})
            with mock.patch.dict(os.environ, {KEY_ENV: "dummy-key"}):
                plan = plan_package(pkg, now=datetime(2026, 8, 29, 8, 0, tzinfo=MSK))
            self.assertEqual(plan.status, "SKIP")
            self.assertIn("рефки", plan.reason)

    def test_gate_fail_skips(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            pkg = _pkg(tmp, "2026-08-29-1212", gate="FAIL", files={"tg.html": "Чай.\n"})
            with mock.patch.dict(os.environ, {KEY_ENV: "dummy-key"}):
                plan = plan_package(pkg, now=datetime(2026, 8, 29, 13, 0, tzinfo=MSK))
            self.assertEqual(plan.status, "SKIP")
            self.assertIn("GATE", plan.reason)

    def test_duplicate_ledger_skips(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            pkg = _pkg(
                tmp,
                "2026-08-29-1515",
                files={"tg.html": "Вопрос?\nОдин\nДва\nТри\nЧетыре\n"},
            )
            (pkg / "publish.json").write_text(
                json.dumps({"sent": [{"dest": "telegram-poll"}]}),
                encoding="utf-8",
            )
            with mock.patch.dict(os.environ, {KEY_ENV: "dummy-key"}):
                plan = plan_package(pkg, now=datetime(2026, 8, 29, 16, 0, tzinfo=MSK))
            self.assertEqual(plan.status, "SKIP")
            self.assertTrue(plan.destinations[0].skip)

    def test_max_only_with_token(self) -> None:
        dests = build_destinations("1212")
        self.assertTrue(any(d.name == "max" and d.skip for d in dests))
        with tempfile.TemporaryDirectory() as tmp:
            pkg = _pkg(
                tmp,
                "2026-08-29-1212",
                files={
                    "tg.html": "Чай.\n",
                    "ig.txt": "Чай.\nСсылки в шапке.\n",
                    "cover-url.txt": "https://example.com/x.png\n",
                },
            )
            env = {KEY_ENV: "dummy-key", "MAX_BOT_TOKEN": "tok", "MAX_CHAT_ID": "99"}
            with mock.patch.dict(os.environ, env, clear=False):
                plan = plan_package(pkg, now=datetime(2026, 8, 29, 13, 0, tzinfo=MSK))
            max_dest = next(d for d in plan.destinations if d.name == "max")
            self.assertFalse(max_dest.skip)

    def test_dry_run_does_not_call_transport(self) -> None:
        calls: list[str] = []

        def transport(method, url, body):
            calls.append(url)
            raise AssertionError("dry-run must not execute")

        with tempfile.TemporaryDirectory() as tmp:
            pkg = _pkg(
                tmp,
                "2026-08-29-1515",
                files={"tg.html": "Вопрос?\nОдин\nДва\nТри\nЧетыре\n"},
            )
            with mock.patch.dict(os.environ, {KEY_ENV: "dummy-key"}):
                plan = plan_package(pkg, now=datetime(2026, 8, 29, 16, 0, tzinfo=MSK))
                report = execute_plan(
                    pkg,
                    plan,
                    dry_run=True,
                    client=ComposioClient(transport=transport),
                    check_live=False,
                )
        self.assertEqual(report["status"], "DRY-RUN")
        self.assertEqual(report["vk"], "UNTOUCHED")
        self.assertEqual(report["youtube"], "UNTOUCHED")
        self.assertFalse(report["hall_publishes"])
        self.assertEqual(calls, [])

    def test_fingerprint_stable(self) -> None:
        self.assertEqual(fingerprint("А  б\n"), fingerprint("а б"))


class CanonMentionsPublishTest(unittest.TestCase):
    def test_director_calls_publish_script(self) -> None:
        text = (ROOT / ".cursor/agents/posts-director.md").read_text(encoding="utf-8")
        self.assertIn("posts_publish.py", text)
        self.assertIn("COMPOSIO_API_KEY", text)
        self.assertIn("telegram-composia", text)
        self.assertIn("Холл не публикует", text)

    def test_posts_md_has_env_and_slots(self) -> None:
        text = (ROOT / "POSTS.md").read_text(encoding="utf-8")
        self.assertIn("COMPOSIO_API_KEY", text)
        self.assertIn("TELEGRAM_SEND_POLL", text)
        self.assertIn("instagram-ru", text)
        self.assertIn("alena-0700", text)
        self.assertIn("Холл не публикует", text)


if __name__ == "__main__":
    unittest.main()

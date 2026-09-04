#!/usr/bin/env python3
"""После GATE PASS рой сам кладёт слот через Composio. Холл не публикует."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import urllib.request
from dataclasses import dataclass, field
from datetime import datetime
from html.parser import HTMLParser
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from posts_composio import (  # noqa: E402
    KEY_ENV,
    ComposioClient,
    ComposioError,
    key_present,
    redact,
)

CFG = json.loads((ROOT / "shared/posts-publish.json").read_text(encoding="utf-8"))
MSK = ZoneInfo(CFG["timezone"])
LEDGER_NAME = "_publish-ledger.json"
ALENA_REFS = (
    "Кому хочется разобраться глубже, приходите на аудиоразбор.",
    "https://www.rustore.ru/catalog/app/ru.taroseychas.app?referrerId=E9F94A57",
    "https://vk.com/app54565776?ref=E3FD5D91",
    "https://max.ru/id531102974575_bot?startapp=ref_2689B3C7",
    "https://t.me/TodayTaro_bot?start=id1356913072",
    "https://t.me/AlenaSafonova_queen",
)
SCENA_RE = re.compile(r"(?i)(?:^|\n)\s*«?сцена»?\s*(?:[:.\-—–]|$)|«сцена»")
SLOT_RE = re.compile(r"(?P<date>\d{4}-\d{2}-\d{2})-(?P<slot>1212|1515|2121|alena)$")
POLL_DIR_RE = re.compile(r"polls/(?P<date>\d{4}-\d{2}-\d{2})-(?P<slot>1515)")


class _Visible(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []

    def handle_data(self, data: str) -> None:
        self.parts.append(data)


def visible_text(html: str) -> str:
    parser = _Visible()
    parser.feed(re.sub(r"<!--.*?-->", "", html, flags=re.S))
    return "".join(parser.parts)


def strip_stamps(text: str) -> str:
    lines = []
    for line in text.splitlines():
        low = line.strip().lower()
        if low.startswith("written_by") or low.startswith("<!-- written_by"):
            continue
        lines.append(line)
    return "\n".join(lines).strip() + ("\n" if text.endswith("\n") else "")


def detect_slot(package: Path) -> tuple[str, str]:
    match = SLOT_RE.search(package.name)
    if match:
        return match.group("date"), match.group("slot")
    poll = POLL_DIR_RE.search(str(package).replace("\\", "/"))
    if poll:
        return poll.group("date"), "1515"
    meta = package / "package.meta.json"
    if meta.is_file():
        data = json.loads(meta.read_text(encoding="utf-8"))
        slot = str(data.get("slot") or "").replace(":", "").lower()
        date = str(data.get("date") or "")
        if slot in {"0700", "alena", "alena-0700", "alena0700"}:
            slot = "alena"
        if slot in {"1212", "1515", "2121", "alena"} and re.match(r"\d{4}-\d{2}-\d{2}$", date):
            return date, slot
    raise SystemExit(f"cannot detect slot/date: {package}")


def slot_clock(slot: str) -> tuple[int, int]:
    hhmm = CFG["slots"][slot]["clock"]
    hour, minute = hhmm.split(":")
    return int(hour), int(minute)


def slot_dt(date: str, slot: str) -> datetime:
    hour, minute = slot_clock(slot)
    y, m, d = (int(x) for x in date.split("-"))
    return datetime(y, m, d, hour, minute, tzinfo=MSK)


def now_msk(now: datetime | None = None) -> datetime:
    if now is None:
        return datetime.now(MSK)
    if now.tzinfo is None:
        return now.replace(tzinfo=MSK)
    return now.astimezone(MSK)


def gate_verdict(package: Path) -> str:
    path = package / "GATE"
    if not path.is_file():
        return "MISSING"
    text = path.read_text(encoding="utf-8")
    match = re.search(r"(?im)^verdict:\s*(\w+)", text)
    if match:
        return match.group(1).upper()
    if re.search(r"(?im)^GATE:\s*PASS", text):
        return "PASS"
    return "UNKNOWN"


def html_caption(package: Path) -> str:
    for name in ("tg.html", "caption.html"):
        path = package / name
        if path.is_file():
            raw = strip_stamps(path.read_text(encoding="utf-8"))
            return raw.strip()
    return ""


def plain_caption(package: Path) -> str:
    for name in ("caption.txt", "max.txt", "ig.txt"):
        path = package / name
        if path.is_file():
            return strip_stamps(path.read_text(encoding="utf-8")).strip()
    html = html_caption(package)
    return visible_text(html).strip() if html else ""


def ig_caption(package: Path) -> str:
    path = package / "ig.txt"
    if path.is_file():
        return strip_stamps(path.read_text(encoding="utf-8")).strip()
    return plain_caption(package)


def parse_poll(package: Path) -> tuple[str, list[str]]:
    candidates = [
        package / "poll.txt",
        package.parent / "polls" / f"{package.name[:10]}-1515" / "poll.txt",
        ROOT / "posts" / "polls" / f"{package.name[:10]}-1515" / "poll.txt",
    ]
    for path in candidates:
        if path.is_file():
            lines = [ln.rstrip() for ln in path.read_text(encoding="utf-8").splitlines() if ln.strip()]
            if len(lines) >= 3:
                return lines[0], lines[1:]
    tg = package / "tg.html"
    if tg.is_file():
        text = visible_text(strip_stamps(tg.read_text(encoding="utf-8")))
        lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
        if len(lines) >= 3:
            return lines[0], lines[1:5]
    raise ValueError("нет опроса: poll.txt или tg.html с вопросом и вариантами")


def image_url(package: Path, slot: str) -> str:
    for name in ("cover-url.txt", "image-url.txt"):
        path = package / name
        if path.is_file():
            url = path.read_text(encoding="utf-8").strip()
            if url.startswith("http"):
                return url
    meta = package / "package.meta.json"
    if meta.is_file():
        data = json.loads(meta.read_text(encoding="utf-8"))
        url = str(data.get("image_url") or data.get("cover_url") or "").strip()
        if url.startswith("http"):
            return url
    env_name = "ALENA_COVER_URL" if slot == "alena" else "POST_IMAGE_URL"
    url = (os.environ.get(env_name) or os.environ.get("POST_IMAGE_URL") or "").strip()
    if url.startswith("http"):
        return url
    return ""


def has_local_cover(package: Path, slot: str) -> bool:
    for name in ("cover.png", "cover.jpg", "image.png", "image.jpg"):
        if (package / name).is_file():
            return True
    if slot == "alena" and Path("/workspace/alena-covers/prognoz-na-den.png").is_file():
        return True
    return False


def fingerprint(text: str) -> str:
    compact = re.sub(r"\s+", " ", text).strip().lower()
    return compact[:80]


def contains_scena(text: str) -> bool:
    return bool(SCENA_RE.search(text)) or "«сцена»" in text.lower()


def alena_refs_intact(caption: str) -> bool:
    return all(part in caption for part in ALENA_REFS)


def load_json(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, data: dict[str, Any]) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def ledger_path() -> Path:
    return ROOT / "posts" / LEDGER_NAME


def ledger_has(date: str, slot: str, dest: str) -> bool:
    data = load_json(ledger_path())
    rows = data.get("sent") or []
    for row in rows:
        if row.get("date") == date and row.get("slot") == slot and row.get("dest") == dest:
            return True
    return False


def ledger_add(date: str, slot: str, dest: str, extra: dict[str, Any] | None = None) -> None:
    path = ledger_path()
    data = load_json(path)
    rows = list(data.get("sent") or [])
    row = {"date": date, "slot": slot, "dest": dest}
    if extra:
        row.update(extra)
    rows.append(row)
    data["sent"] = rows
    path.parent.mkdir(parents=True, exist_ok=True)
    save_json(path, data)


@dataclass
class Dest:
    name: str
    toolkit: str
    alias: str
    tool: str
    chat_id: str = ""
    reason: str = ""
    skip: bool = False


@dataclass
class Plan:
    date: str
    slot: str
    status: str
    reason: str = ""
    destinations: list[Dest] = field(default_factory=list)
    wait_until: str = ""

    def as_dict(self) -> dict[str, Any]:
        return {
            "date": self.date,
            "slot": self.slot,
            "status": self.status,
            "reason": self.reason,
            "wait_until": self.wait_until,
            "destinations": [
                {
                    "name": d.name,
                    "toolkit": d.toolkit,
                    "alias": d.alias,
                    "tool": d.tool,
                    "chat_id": d.chat_id,
                    "skip": d.skip,
                    "reason": d.reason,
                }
                for d in self.destinations
            ],
        }


def build_destinations(slot: str) -> list[Dest]:
    aliases = CFG["aliases"]
    tg_alias = aliases["telegram"]
    today = CFG["channels"]["todaytaro"]
    alena = CFG["channels"]["alena"]
    tools = CFG["tools"]
    if slot == "1212":
        dests = [
            Dest("telegram", "telegram", tg_alias, tools["telegram_photo"], today),
            Dest("instagram-ru", "instagram", aliases["instagram_ru"], tools["ig_create"]),
        ]
        dests.append(Dest("max", "max", "", "MAX_SEND", skip=True, reason="нет MAX_BOT_TOKEN"))
        return dests
    if slot == "1515":
        return [Dest("telegram-poll", "telegram", tg_alias, tools["telegram_poll"], today)]
    if slot == "2121":
        return [Dest("telegram", "telegram", tg_alias, tools["telegram_photo"], today)]
    if slot == "alena":
        return [Dest("telegram-alena", "telegram", tg_alias, tools["telegram_photo"], alena)]
    raise ValueError(f"unknown slot {slot}")


def apply_optional_max(dests: list[Dest]) -> None:
    token = (os.environ.get("MAX_BOT_TOKEN") or "").strip()
    chat = (os.environ.get("MAX_CHAT_ID") or "AaBmlTdadaI").strip()
    for dest in dests:
        if dest.name != "max":
            continue
        if not token:
            dest.skip = True
            dest.reason = "нет MAX_BOT_TOKEN"
            continue
        dest.skip = False
        dest.reason = ""
        dest.chat_id = chat


def plan_package(package: Path, now: datetime | None = None) -> Plan:
    date, slot = detect_slot(package)
    plan = Plan(date=date, slot=slot, status="READY")
    if slot not in CFG["slots"]:
        plan.status = "SKIP"
        plan.reason = f"слот {slot} не публикуем"
        return plan
    meta_path = package / "package.meta.json"
    if meta_path.is_file():
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        preview = str(meta.get("preview") or "").lower()
        if preview in {"poll-only", "poll", "preview"}:
            plan.status = "SKIP"
            plan.reason = "preview — не публиковать"
            return plan
    verdict = gate_verdict(package)
    if verdict != "PASS":
        plan.status = "SKIP"
        plan.reason = f"GATE {verdict}, эфир только после PASS"
        return plan
    if not key_present():
        plan.status = "SKIP"
        plan.reason = f"{KEY_ENV} нет — SKIP, не падаем"
        return plan

    when = slot_dt(date, slot)
    current = now_msk(now)
    if current < when:
        plan.status = "WAIT"
        plan.reason = "слот МСК ещё не наступил, без отложки"
        plan.wait_until = when.isoformat()
        plan.destinations = build_destinations(slot)
        apply_optional_max(plan.destinations)
        return plan

    dests = build_destinations(slot)
    apply_optional_max(dests)

    if slot == "2121":
        text = html_caption(package) or plain_caption(package)
        if contains_scena(text):
            plan.status = "SKIP"
            plan.reason = "21:21: слово «Сцена» запрещено"
            return plan

    if slot == "alena":
        caption = plain_caption(package) or html_caption(package)
        if not alena_refs_intact(caption):
            plan.status = "SKIP"
            plan.reason = "alena-0700: рефки не совпали, не менять и не слать"
            return plan

    need_image = slot in {"1212", "2121", "alena"}
    url = image_url(package, slot) if need_image else ""
    if need_image and not url:
        local = has_local_cover(package, slot)
        reason = "нет публичного URL картинки (cover-url.txt / POST_IMAGE_URL)"
        if local:
            reason += "; локальный файл Composio не принимает"
        for dest in dests:
            if dest.tool in {CFG["tools"]["telegram_photo"], CFG["tools"]["ig_create"]}:
                dest.skip = True
                dest.reason = reason

    if slot == "1515":
        try:
            parse_poll(package)
        except ValueError as exc:
            plan.status = "SKIP"
            plan.reason = str(exc)
            return plan

    published = load_json(package / "publish.json")
    sent = {row.get("dest") for row in (published.get("sent") or [])}
    for dest in dests:
        if dest.skip:
            continue
        if dest.name in sent or ledger_has(date, slot, dest.name):
            dest.skip = True
            dest.reason = "уже в ledger сегодня — не дублировать"

    plan.destinations = dests
    if all(d.skip for d in dests):
        plan.status = "SKIP"
        plan.reason = plan.reason or "все площадки SKIP"
    else:
        plan.status = "READY"
        plan.reason = "слот наступил или прошёл — слать сразу"
    return plan


def live_fingerprints(client: ComposioClient, dest: Dest) -> list[str]:
    if dest.toolkit != "telegram" or not dest.chat_id:
        return []
    data = client.execute(
        CFG["tools"]["telegram_history"],
        {"chat_id": dest.chat_id, "limit": 20},
        dest.alias,
    )
    blob = json.dumps(data, ensure_ascii=False)
    return [fingerprint(blob)]


def looks_duplicate(live: list[str], text: str) -> bool:
    needle = fingerprint(text)
    if not needle:
        return False
    return any(needle[:40] in item for item in live)


def send_telegram_photo(client: ComposioClient, dest: Dest, caption: str, photo: str) -> dict:
    args = {
        "chat_id": dest.chat_id,
        "photo": photo,
        "caption": caption[:1024],
        "parse_mode": "HTML" if "<" in caption else None,
    }
    if not args["parse_mode"]:
        args.pop("parse_mode")
    return client.execute(dest.tool, args, dest.alias)


def send_telegram_poll(client: ComposioClient, dest: Dest, question: str, options: list[str]) -> dict:
    args = {
        "chat_id": dest.chat_id,
        "question": question[:300],
        "options": [opt[:100] for opt in options[:10]],
        "is_anonymous": True,
        "type": "regular",
    }
    return client.execute(dest.tool, args, dest.alias)


def send_instagram(client: ComposioClient, dest: Dest, caption: str, photo: str) -> dict:
    user = client.execute(CFG["tools"]["ig_user"], {"ig_user_id": "me"}, dest.alias)
    payload = user.get("data") or user
    if isinstance(payload, dict) and "data" in payload and isinstance(payload["data"], dict):
        payload = payload["data"]
    ig_user_id = str(
        payload.get("id")
        or payload.get("ig_id")
        or payload.get("user_id")
        or "me"
    )
    created = client.execute(
        CFG["tools"]["ig_create"],
        {"ig_user_id": ig_user_id, "image_url": photo, "caption": caption},
        dest.alias,
    )
    created_data = created.get("data") or created
    if isinstance(created_data, dict) and "data" in created_data:
        created_data = created_data["data"]
    creation_id = str(
        (created_data or {}).get("id")
        or (created_data or {}).get("creation_id")
        or ""
    )
    if not creation_id:
        raise ComposioError("instagram: нет creation_id")
    return client.execute(
        CFG["tools"]["ig_publish"],
        {"ig_user_id": ig_user_id, "creation_id": creation_id},
        dest.alias,
    )


def send_max(caption: str, photo: str, chat_id: str) -> dict:
    token = (os.environ.get("MAX_BOT_TOKEN") or "").strip()
    if not token:
        raise RuntimeError("MAX_BOT_TOKEN missing")
    body: dict[str, Any] = {"text": visible_text(caption) if "<" in caption else caption}
    if photo:
        body["attachments"] = [{"type": "image", "payload": {"url": photo}}]
    payload = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(
        f"https://platform-api2.max.ru/messages?chat_id={chat_id}",
        data=payload,
        method="POST",
        headers={"Authorization": token, "Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            raw = resp.read().decode("utf-8")
    except Exception as exc:  # noqa: BLE001
        raise RuntimeError(redact(str(exc), [token])) from None
    return json.loads(raw) if raw else {}


def execute_plan(
    package: Path,
    plan: Plan,
    *,
    dry_run: bool,
    client: ComposioClient | None,
    check_live: bool,
) -> dict[str, Any]:
    results: list[dict[str, Any]] = []
    photo = image_url(package, plan.slot)
    caption_html = html_caption(package)
    caption_plain = plain_caption(package)
    for dest in plan.destinations:
        row = {"dest": dest.name, "alias": dest.alias, "tool": dest.tool, "status": "SKIP", "reason": dest.reason}
        if dest.skip:
            results.append(row)
            continue
        text = caption_html if dest.toolkit == "telegram" and dest.tool != CFG["tools"]["telegram_poll"] else caption_plain
        if dest.name == "instagram-ru":
            text = ig_caption(package)
        try:
            if check_live and client and dest.toolkit == "telegram":
                live = live_fingerprints(client, dest)
                probe = text
                if dest.tool == CFG["tools"]["telegram_poll"]:
                    probe, _ = parse_poll(package)
                if looks_duplicate(live, probe):
                    row["status"] = "SKIP"
                    row["reason"] = "живой сегодняшний пост уже есть — не дублировать"
                    dest.skip = True
                    dest.reason = row["reason"]
                    results.append(row)
                    continue
        except ComposioError as exc:
            row["live_check"] = redact(str(exc))

        if dry_run:
            row["status"] = "DRY-RUN"
            row["reason"] = "dry-run, в эфир не ушло"
            results.append(row)
            continue
        if dest.name == "max":
            try:
                send_max(caption_plain or caption_html, photo, dest.chat_id)
                row["status"] = "SENT"
                row["reason"] = ""
                ledger_add(plan.date, plan.slot, dest.name, {"tool": dest.tool, "alias": dest.alias})
            except Exception as exc:
                row["status"] = "SKIP"
                row["reason"] = redact(str(exc))
            results.append(row)
            continue
        if client is None:
            row["status"] = "SKIP"
            row["reason"] = "нет клиента Composio"
            results.append(row)
            continue
        try:
            resp: dict[str, Any] = {}
            if dest.tool == CFG["tools"]["telegram_poll"]:
                question, options = parse_poll(package)
                resp = send_telegram_poll(client, dest, question, options)
            elif dest.toolkit == "instagram":
                resp = send_instagram(client, dest, text, photo)
            else:
                resp = send_telegram_photo(client, dest, text, photo)
            row["status"] = "SENT"
            row["reason"] = ""
            resp_data = resp.get("data") if isinstance(resp, dict) else {}
            if isinstance(resp_data, dict):
                inner_res = resp_data.get("result") if isinstance(resp_data.get("result"), dict) else resp_data
                msg_id = inner_res.get("message_id")
                if msg_id:
                    row["message_id"] = msg_id
                    if dest.chat_id and dest.chat_id.startswith("@"):
                        row["link"] = f"https://t.me/{dest.chat_id.lstrip('@')}/{msg_id}"
            ledger_add(plan.date, plan.slot, dest.name, {"tool": dest.tool, "alias": dest.alias})
        except (ComposioError, RuntimeError, ValueError) as exc:
            row["status"] = "SKIP"
            row["reason"] = redact(str(exc))
        results.append(row)

    sent = [r for r in results if r["status"] == "SENT"]
    skipped = [r for r in results if r["status"] == "SKIP"]
    if sent and skipped:
        status = "PARTIAL"
    elif sent:
        status = "SENT"
    elif any(r["status"] == "DRY-RUN" for r in results):
        status = "DRY-RUN"
    else:
        status = "SKIP"
    report = {
        "package": str(package),
        "date": plan.date,
        "slot": plan.slot,
        "status": status if plan.status == "READY" else plan.status,
        "reason": plan.reason,
        "results": results,
        "hall_publishes": False,
        "vk": "UNTOUCHED",
        "youtube": "UNTOUCHED",
        "key_env": KEY_ENV,
        "key_present": key_present(),
    }
    for r in results:
        if r.get("link"):
            report["link"] = r["link"]
        if r.get("message_id"):
            report["message_id"] = r["message_id"]
    save_json(package / "publish.json", report)
    return report


def wait_for_slot(plan: Plan, now: datetime | None = None) -> Plan:
    if plan.status != "WAIT" or not plan.wait_until:
        return plan
    target = datetime.fromisoformat(plan.wait_until)
    current = now_msk(now)
    while current < target:
        delay = min(30, max(1, int((target - current).total_seconds())))
        time.sleep(delay)
        current = now_msk()
    plan.status = "READY"
    plan.reason = "слот наступил — слать сразу"
    return plan


def main() -> int:
    parser = argparse.ArgumentParser(description="Публикация слота после GATE PASS через Composio")
    parser.add_argument("--package", type=Path, required=True)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--wait", action="store_true", help="ждать слот МСК (без отложки Telegram)")
    parser.add_argument("--no-live-check", action="store_true")
    parser.add_argument("--now")
    args = parser.parse_args()
    package = args.package
    if not package.is_absolute():
        package = (Path.cwd() / package).resolve()
    now = None
    if args.now:
        now = datetime.fromisoformat(args.now)
        if now.tzinfo is None:
            now = now.replace(tzinfo=MSK)
    plan = plan_package(package, now=now)
    if plan.status == "WAIT" and args.wait:
        plan = wait_for_slot(plan, now=now)
        plan = plan_package(package, now=now_msk())
    client = None
    if key_present() and plan.status == "READY" and not args.dry_run:
        client = ComposioClient(CFG["composio_base_url"])
    if plan.status in {"SKIP", "WAIT"}:
        report = {
            "package": str(package),
            "date": plan.date,
            "slot": plan.slot,
            "status": plan.status,
            "reason": plan.reason,
            "wait_until": plan.wait_until,
            "destinations": plan.as_dict()["destinations"],
            "hall_publishes": False,
            "vk": "UNTOUCHED",
            "youtube": "UNTOUCHED",
            "key_env": KEY_ENV,
            "key_present": key_present(),
        }
        save_json(package / "publish.json", report)
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0
    report = execute_plan(
        package,
        plan,
        dry_run=args.dry_run,
        client=client,
        check_live=not args.no_live_check,
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())

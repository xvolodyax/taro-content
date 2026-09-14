#!/usr/bin/env python3
"""Кластеры углов 12:12 / 15:15: анти-монотонность за ~7 дней.

Scout читает отчёт до brief.md. Холл угол не назначает.
21:21 не сканируем: вечер отвечает опросу 15:15.
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
POSTS = ROOT / "posts"

SLOT_RE = re.compile(r"^(?P<date>\d{4}-\d{2}-\d{2})-(?P<slot>1212|1515|2121)(?:/|$)")
CLUSTER_FIELD_RE = re.compile(
    r"^\*\*Кластер:\*\*\s*(?P<value>.+?)\s*$",
    re.MULTILINE,
)

CLUSTER_IDS = (
    "relations",
    "marriage",
    "kids",
    "family",
    "tarot_moment",
    "chat_promise",
)

FORBIDDEN_ID = "forbidden_magiya"

# Более узкие кластеры раньше широкого chat_promise.
_MARKERS: dict[str, tuple[str, ...]] = {
    FORBIDDEN_ID: (
        "порч",
        "приворот",
        "сглаз",
        "обряд",
        "проклят",
        "чёрная магия",
        "черная магия",
        "вызов духа",
        "навести",
        "снять порчу",
    ),
    "marriage": (
        "женить",
        "жениться",
        "замуж",
        "свадьб",
        "предложен",
        "кольцо",
        "гражданский брак",
        "роспис",
        "расписаться",
        "помолв",
    ),
    "kids": (
        "хочет ли он детей",
        "не хочет детей",
        "хочет детей",
        "общий ребенок",
        "общий ребёнок",
        "береме",
        "сказать ему про ребен",
        "сказать ему про ребён",
        "разговор про детей",
    ),
    "family": (
        "свекров",
        "родители не принимают",
        "его родители",
        "её родители",
        "съехаться",
        "жить вместе",
        "жить с родителями",
        "тёща",
        "теща",
        "семья не принимает",
        "быт семьи",
    ),
    "tarot_moment": (
        "таро-момент",
        "расклад таро",
        "что говорят карты",
        "вытянула карту",
        "стоит ли гадать",
        "карты перед разговором",
        "гадать на него",
    ),
    "relations": (
        "охладел",
        "не готов к отношен",
        "не называет",
        "ревн",
        "измен",
        "расста",
        "общее будущее",
        "совместное будущее",
        "статус пары",
        "не своей",
    ),
    "chat_promise": (
        "не пишет",
        "обещал",
        "обещала",
        "печатает",
        "прочитано",
        "онлайн",
        "в сети",
        "удалил сообщение",
        "сообщение удалено",
        "галочк",
        "не отвечает",
        "написать первой",
        "писать первой",
        "напишу в",
        "молчит в чате",
        "тишина в чате",
        "спишемся",
    ),
}

_ID_ALIASES = {
    "отношения": "relations",
    "отношен": "relations",
    "relations": "relations",
    "брак": "marriage",
    "marriage": "marriage",
    "дети": "kids",
    "kids": "kids",
    "семья": "family",
    "семьи": "family",
    "family": "family",
    "таро-момент": "tarot_moment",
    "таро момент": "tarot_moment",
    "tarot_moment": "tarot_moment",
    "чат": "chat_promise",
    "чат/микросигнал": "chat_promise",
    "chat_promise": "chat_promise",
    "обещания": "chat_promise",
    "пауза": "chat_promise",
    "молчание-пауза": "chat_promise",
}


def _norm(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "").lower()).strip()


def cluster_from_field(value: str) -> str | None:
    raw = _norm(value)
    if not raw:
        return None
    # Берём первый токен / id до слэша или скобок.
    head = re.split(r"[/,;(]", raw, maxsplit=1)[0].strip()
    if head in _ID_ALIASES:
        return _ID_ALIASES[head]
    for alias, cid in _ID_ALIASES.items():
        if alias in raw:
            return cid
    return None


def classify_text(text: str) -> str:
    """Один кластер по явном полю или маркерам. Уже — уже."""
    field = CLUSTER_FIELD_RE.search(text or "")
    if field:
        mapped = cluster_from_field(field.group("value"))
        if mapped:
            return mapped
    blob = _norm(text)
    for cid in (
        FORBIDDEN_ID,
        "marriage",
        "kids",
        "family",
        "tarot_moment",
        "relations",
        "chat_promise",
    ):
        if any(marker in blob for marker in _MARKERS[cid]):
            return cid
    return "unknown"


def package_date_slot(name: str) -> tuple[date, str] | None:
    match = SLOT_RE.match(name)
    if not match:
        return None
    return date.fromisoformat(match.group("date")), match.group("slot")


def iter_recent_briefs(
    posts_dir: Path,
    *,
    as_of: date,
    lookback_days: int,
    slots: Iterable[str] = ("1212", "1515"),
) -> list[dict[str, str]]:
    wanted = {s.strip() for s in slots}
    start = as_of - timedelta(days=lookback_days - 1)
    rows: list[dict[str, str]] = []
    if not posts_dir.is_dir():
        return rows
    for path in sorted(posts_dir.iterdir()):
        if not path.is_dir():
            continue
        parsed = package_date_slot(path.name)
        if not parsed:
            continue
        pkg_date, slot = parsed
        if slot not in wanted:
            continue
        if pkg_date < start or pkg_date > as_of:
            continue
        brief = path / "brief.md"
        text = brief.read_text(encoding="utf-8") if brief.is_file() else ""
        rows.append(
            {
                "package": path.name,
                "date": pkg_date.isoformat(),
                "slot": slot,
                "cluster": classify_text(text),
                "has_brief": str(brief.is_file()).lower(),
            }
        )
    return rows


def overused_cluster(rows: list[dict[str, str]]) -> str | None:
    """Доминация: ≥3 слота и один кластер ≥50%, либо chat_promise ≥4."""
    classified = [r["cluster"] for r in rows if r["cluster"] not in {"unknown", FORBIDDEN_ID}]
    if not classified:
        return None
    counts = Counter(classified)
    top, top_n = counts.most_common(1)[0]
    if counts.get("chat_promise", 0) >= 4:
        return "chat_promise"
    if len(classified) >= 3 and top_n * 2 >= len(classified):
        return top
    return None


def build_report(
    *,
    as_of: date,
    lookback_days: int,
    posts_dir: Path = POSTS,
    slots: Iterable[str] = ("1212", "1515"),
) -> dict:
    rows = iter_recent_briefs(
        posts_dir, as_of=as_of, lookback_days=lookback_days, slots=slots
    )
    counts = Counter(r["cluster"] for r in rows)
    overused = overused_cluster(rows)
    return {
        "as_of": as_of.isoformat(),
        "lookback_days": lookback_days,
        "slots": list(slots),
        "recent": rows,
        "counts": dict(counts),
        "overused": overused or "none",
        "rule": (
            "Если overused != none — взять жирный Wordstat из другого ALLOW-кластера. "
            "Сиды: relations + marriage + kids + family + tarot_moment. "
            "chat_promise нельзя жевать неделю. Magiya/порча — не для постов. "
            "Холл угол не назначает. 21:21 не трогаем."
        ),
    }


def parse_as_of(raw: str | None) -> date:
    if not raw:
        return datetime.now().date()
    return date.fromisoformat(raw)


def main() -> int:
    parser = argparse.ArgumentParser(description="Анти-монотонность кластеров 12:12/15:15")
    parser.add_argument("--lookback-days", type=int, default=7)
    parser.add_argument("--date", dest="as_of", default="", help="YYYY-MM-DD, по умолчанию сегодня")
    parser.add_argument("--posts-dir", type=Path, default=POSTS)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    report = build_report(
        as_of=parse_as_of(args.as_of or None),
        lookback_days=args.lookback_days,
        posts_dir=args.posts_dir,
    )
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0
    print(f"as_of: {report['as_of']}")
    print(f"lookback_days: {report['lookback_days']}")
    print(f"overused: {report['overused']}")
    if report["counts"]:
        print("counts:")
        for key, value in sorted(report["counts"].items(), key=lambda kv: (-kv[1], kv[0])):
            print(f"  {key}: {value}")
    else:
        print("recent: 0")
    for row in report["recent"]:
        print(f"- {row['date']} {row['slot']} {row['cluster']} {row['package']}")
    print(report["rule"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

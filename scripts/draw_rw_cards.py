#!/usr/bin/env python3
"""Жеребьёвка карт Райдер-Уэйт.

С 2026-09-15 слот 21:21 — 4 случайных имени RWS, не 3.
Позиция 4 = совет сейчас (что делать NOW), не 4 совета на варианты опроса.
Пакеты до 15.09 не перетягивать этим скриптом.
"""

from __future__ import annotations

import argparse
import json
import random
import re
import sys
from pathlib import Path

MAJOR = [
    "Шут",
    "Маг",
    "Верховная Жрица",
    "Императрица",
    "Император",
    "Иерофант",
    "Влюблённые",
    "Колесница",
    "Сила",
    "Отшельник",
    "Колесо Фортуны",
    "Справедливость",
    "Повешенный",
    "Смерть",
    "Умеренность",
    "Дьявол",
    "Башня",
    "Звезда",
    "Луна",
    "Солнце",
    "Суд",
    "Мир",
]

RANKS = [
    "Туз",
    "Двойка",
    "Тройка",
    "Четвёрка",
    "Пятёрка",
    "Шестёрка",
    "Семёрка",
    "Восьмёрка",
    "Девятка",
    "Десятка",
    "Паж",
    "Рыцарь",
    "Королева",
    "Король",
]
SUITS = ["жезлов", "кубков", "мечей", "пентаклей"]
MINOR = [f"{rank} {suit}" for suit in SUITS for rank in RANKS]
DECK = MAJOR + MINOR

# 21:21 с 15.09.2026. Не путать со старой формой «4 совета на варианты».
DEFAULT_COUNT = 4
FOUR_CARDS_SINCE = "2026-09-15"
POSITION_NAMES = (
    "его сторона",
    "почему сейчас",
    "что это просит у неё",
    "совет сейчас",
)


def yesterday_sets(ledger: Path, count: int) -> list[set[str]]:
    if not ledger.is_file():
        return []
    text = ledger.read_text(encoding="utf-8")
    sets: list[set[str]] = []
    for line in text.splitlines():
        if "карты:" in line.lower() or "cards:" in line.lower():
            names = re.split(r"\s*[|/,-]\s*", line.split(":", 1)[1])
            names = [n.strip() for n in names if n.strip()]
            if len(names) >= count:
                sets.append(set(names[:count]))
    return sets


def draw(ledger: Path | None, count: int = DEFAULT_COUNT) -> list[str]:
    if count < 1 or count > len(DECK):
        raise SystemExit(f"count {count} вне колоды")
    banned = yesterday_sets(ledger, count) if ledger else []
    rng = random.SystemRandom()
    for _ in range(40):
        pick = rng.sample(DECK, count)
        if set(pick) not in banned:
            return pick
    raise SystemExit("не удалось вытянуть набор, отличный от ledger")


def position_name(n: int) -> str:
    if 1 <= n <= len(POSITION_NAMES):
        return POSITION_NAMES[n - 1]
    return f"позиция {n}"


def cards_payload(
    cards: list[str],
    *,
    date: str | None = None,
    slot: str = "2121",
    ledger: Path | None = None,
) -> dict:
    count = len(cards)
    source = f"python3 scripts/draw_rw_cards.py --count {count}"
    if ledger:
        source += f" --ledger {ledger}"
    positions = [
        {"n": i, "name": position_name(i), "card": card}
        for i, card in enumerate(cards, start=1)
    ]
    payload: dict = {
        "slot": slot,
        "source": source,
        "draw": "random",
        "deck": "RWS",
        "count": count,
        "cards": list(cards),
        "positions": positions,
    }
    if date:
        payload["date"] = date
    return payload


def draw_line(cards: list[str]) -> str:
    if len(cards) == 4:
        return "Вытянула четыре карты: " + ", ".join(cards)
    if len(cards) == 3:
        return "Вытянула три карты: " + ", ".join(cards)
    return "Вытянула карты: " + ", ".join(cards)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ledger", type=Path, default=None)
    parser.add_argument(
        "--count",
        type=int,
        default=DEFAULT_COUNT,
        help="21:21 с 2026-09-15: 4. До 15.09 живые пакеты не перетягивать.",
    )
    parser.add_argument("--date", default=None, help="YYYY-MM-DD в cards.json")
    parser.add_argument("--json", action="store_true", help="печатать cards.json")
    parser.add_argument(
        "--out",
        type=Path,
        default=None,
        help="записать cards.json (seed)",
    )
    args = parser.parse_args()
    cards = draw(args.ledger, args.count)
    payload = cards_payload(cards, date=args.date, ledger=args.ledger)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    if args.json or args.out:
        if args.json or not args.out:
            sys.stdout.write(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
        else:
            sys.stdout.write(draw_line(cards) + "\n")
        return
    sys.stdout.write(" | ".join(cards) + "\n")


if __name__ == "__main__":
    main()

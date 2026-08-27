#!/usr/bin/env python3
"""Жеребьёвка 4 карт Райдер-Уэйт. Сначала случайный набор, потом расклад."""

from __future__ import annotations

import argparse
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


def yesterday_sets(ledger: Path) -> list[set[str]]:
    if not ledger.is_file():
        return []
    text = ledger.read_text(encoding="utf-8")
    sets: list[set[str]] = []
    for line in text.splitlines():
        if "карты:" in line.lower() or "cards:" in line.lower():
            names = re.split(r"\s*[|/,-]\s*", line.split(":", 1)[1])
            names = [n.strip() for n in names if n.strip()]
            if len(names) >= 4:
                sets.append(set(names[:4]))
    return sets


def draw(ledger: Path | None) -> list[str]:
    banned = yesterday_sets(ledger) if ledger else []
    rng = random.SystemRandom()
    for _ in range(40):
        pick = rng.sample(DECK, 4)
        if set(pick) not in banned:
            return pick
    raise SystemExit("не удалось вытянуть набор, отличный от ledger")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ledger", type=Path, default=None)
    args = parser.parse_args()
    cards = draw(args.ledger)
    sys.stdout.write(" | ".join(cards) + "\n")


if __name__ == "__main__":
    main()

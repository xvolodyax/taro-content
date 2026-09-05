#!/usr/bin/env python3
"""Проверка пакета alena-0700: длина, рефки, запретные заголовки."""
from __future__ import annotations

import re
import sys
from pathlib import Path

REFS = """Кому хочется разобраться глубже, приходите на аудиоразбор.

RuStore → https://www.rustore.ru/catalog/app/ru.taroseychas.app?referrerId=E9F94A57
ВКонтакте → https://vk.com/app54565776?ref=E3FD5D91
Макс → https://max.ru/id531102974575_bot?startapp=ref_2689B3C7
Академия ТАРО → https://t.me/TodayTaro_bot?start=id1356913072
Личные расклады → https://t.me/AlenaSafonova_queen"""

HEADINGS = re.compile(
    r"(?m)^(?:#+\s*)?(Развилка(?: дня)?|Действие(?: дня)?|Не стоит|Чего делать не стоит)\s*$"
)


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: python3 scripts/alena_check.py posts/YYYY-MM-DD-alena", file=sys.stderr)
        return 2
    root = Path(sys.argv[1])
    cap = (root / "caption.txt").read_text(encoding="utf-8")
    html = (root / "caption.html").read_text(encoding="utf-8")
    errors: list[str] = []

    if not cap.endswith("\n"):
        cap_cmp = cap
    else:
        cap_cmp = cap[: -1] if cap.endswith("\n") and not cap.endswith("\n\n") else cap.rstrip("\n")

    n = len(cap_cmp)
    if n > 1700:
        errors.append(f"caption.txt {n} > 1700")
    if REFS not in cap_cmp:
        errors.append("рефки в caption.txt не совпали с каноном")
    if HEADINGS.search(cap_cmp):
        errors.append("одинокий заголовок Развилка/Действие/Не стоит")
    if "ловушка" in cap_cmp.lower():
        errors.append("слово ловушка")
    if "—" in cap_cmp:
        errors.append("длинное тире")
    for url in (
        "referrerId=E9F94A57",
        "ref=E3FD5D91",
        "ref_2689B3C7",
        "start=id1356913072",
        "AlenaSafonova_queen",
    ):
        if url not in html:
            errors.append(f"в caption.html нет {url}")
    if "<a href=" not in html:
        errors.append("caption.html без ссылок")

    print(f"caption_len: {n}")
    if errors:
        print("FAIL")
        for e in errors:
            print(f"- {e}")
        return 1
    print("ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

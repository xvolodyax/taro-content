#!/usr/bin/env python3
"""Небо на дату слота alena-0700. Москва. Цифры не выдумывать.

Лунный день из календарей (восход Луны) Scout сверяет сам.
Этот скрипт даёт знак, фазу, восход/заход МСК и аспекты.
"""
from __future__ import annotations

import argparse
import sys
from datetime import datetime, timedelta, timezone

MSK = timezone(timedelta(hours=3))
SIGNS = (
    "Овен",
    "Телец",
    "Близнецы",
    "Рак",
    "Лев",
    "Дева",
    "Весы",
    "Скорпион",
    "Стрелец",
    "Козерог",
    "Водолей",
    "Рыбы",
)
PLANETS = ("Sun", "Mercury", "Venus", "Mars", "Jupiter", "Saturn")


def _need_ephem():
    try:
        import ephem  # noqa: F401
    except ImportError:
        print("Нет ephem. Поставь: pip3 install --user ephem", file=sys.stderr)
        sys.exit(2)


def msk_from_ephem(edate):
    import ephem

    dt = edate.datetime().replace(tzinfo=timezone.utc).astimezone(MSK)
    return dt


def ecl_lon(body, utc_str: str) -> float:
    import ephem

    body.compute(utc_str)
    return float(ephem.Ecliptic(body).lon) * 180.0 / ephem.pi


def sign_of(lon: float) -> str:
    return SIGNS[int(lon % 360 // 30)]


def sep(a: float, b: float) -> float:
    return abs((a - b + 180) % 360 - 180)


def aspect_name(d: float) -> str | None:
    checks = (
        (0, 6, "соединение"),
        (60, 4, "секстиль"),
        (90, 5, "квадрат"),
        (120, 5, "тригон"),
        (180, 6, "оппозиция"),
    )
    for angle, orb, name in checks:
        if abs(d - angle) <= orb:
            return name
    return None


def utc_stamp(dt_msk: datetime) -> str:
    return dt_msk.astimezone(timezone.utc).strftime("%Y/%m/%d %H:%M:%S")


def main() -> int:
    _need_ephem()
    import ephem

    p = argparse.ArgumentParser()
    p.add_argument("--date", required=True, help="YYYY-MM-DD, Москва")
    args = p.parse_args()
    day = datetime.strptime(args.date, "%Y-%m-%d").date()

    noon = datetime(day.year, day.month, day.day, 12, 0, tzinfo=MSK)
    moon = ephem.Moon(utc_stamp(noon))
    ml = ecl_lon(moon, utc_stamp(noon))
    moon.compute(utc_stamp(noon))

    obs = ephem.Observer()
    obs.lat, obs.lon, obs.elevation = "55.7522", "37.6156", 156
    obs.date = utc_stamp(datetime(day.year, day.month, day.day, 0, 0, tzinfo=MSK))
    rise = msk_from_ephem(obs.next_rising(ephem.Moon()))
    sett = msk_from_ephem(obs.next_setting(ephem.Moon()))

    prev_new = msk_from_ephem(ephem.previous_new_moon(utc_stamp(noon)))
    next_new = msk_from_ephem(ephem.next_new_moon(utc_stamp(noon)))
    prev_full = msk_from_ephem(ephem.previous_full_moon(utc_stamp(noon)))
    next_full = msk_from_ephem(ephem.next_full_moon(utc_stamp(noon)))
    # if full/new is today morning before noon, previous_* may be today
    full_today = prev_full.date() == day or next_full.date() == day
    new_today = prev_new.date() == day or next_new.date() == day

    phase = "растущая"
    if moon.phase >= 99.2 or full_today:
        phase = "полнолуние"
    elif moon.phase <= 1.5 or new_today:
        phase = "новолуние"
    elif prev_full < noon < next_new:
        phase = "убывающая"

    print(f"date: {day.isoformat()}")
    print("tz: Europe/Moscow")
    print(f"moon_sign: {sign_of(ml)} {ml % 30:.1f}°")
    print(f"illumination: {moon.phase:.1f}%")
    print(f"phase_guess: {phase}")
    print(f"moonrise_msk: {rise.strftime('%Y-%m-%d %H:%M')}")
    print(f"moonset_msk: {sett.strftime('%Y-%m-%d %H:%M')}")
    print(f"prev_new_msk: {prev_new.strftime('%Y-%m-%d %H:%M')}")
    print(f"next_new_msk: {next_new.strftime('%Y-%m-%d %H:%M')}")
    print(f"prev_full_msk: {prev_full.strftime('%Y-%m-%d %H:%M')}")
    print(f"next_full_msk: {next_full.strftime('%Y-%m-%d %H:%M')}")
    print("haircut_hard_no: да" if phase in {"полнолуние", "новолуние"} else "haircut_hard_no: нет")
    print("lunar_day: сверить с календарем; смена ≈ восход Луны")
    print("aspects (07:00, 12:00, 19:00 МСК):")

    for hour in (7, 12, 19):
        tm = datetime(day.year, day.month, day.day, hour, 0, tzinfo=MSK)
        stamp = utc_stamp(tm)
        moon_b = ephem.Moon(stamp)
        mlon = ecl_lon(moon_b, stamp)
        found = []
        ru = {
            "Sun": "Солнце",
            "Mercury": "Меркурий",
            "Venus": "Венера",
            "Mars": "Марс",
            "Jupiter": "Юпитер",
            "Saturn": "Сатурн",
        }
        for name in PLANETS:
            pl = getattr(ephem, name)(stamp)
            d = sep(mlon, ecl_lon(pl, stamp))
            kind = aspect_name(d)
            if kind:
                found.append(f"{kind} с {ru[name]} ({d:.1f}°)")
        print(f"  {hour:02d}:00 {', '.join(found) if found else '—'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

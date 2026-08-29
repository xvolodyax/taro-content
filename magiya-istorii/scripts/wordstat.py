#!/usr/bin/env python3
"""Живой Wordstat (Yandex Cloud Search API v2). Ключ в stdout/stderr не писать."""

from __future__ import annotations

import argparse
import json
import os
import ssl
import sys
import time
import urllib.error
import urllib.request

API_BASE = "https://searchapi.api.cloud.yandex.net/v2/wordstat"
KEY_ENV = "YANDEX_CLOUD_SEARCH_API_KEY"
FOLDER_ENV = "YANDEX_FOLDER_ID"


def _redact(text: str, key: str) -> str:
    if not text:
        return text
    out = text
    if key:
        out = out.replace(key, "[REDACTED]")
    for token in ("Api-Key ", "api-key ", "AQVN"):
        if token.lower() in out.lower() and key:
            out = out.replace(key, "[REDACTED]")
    return out


def _env() -> tuple[str | None, str | None]:
    key = os.environ.get(KEY_ENV)
    folder = os.environ.get(FOLDER_ENV)
    return (key.strip() if key else None, folder.strip() if folder else None)


def _call(path: str, body: dict, key: str, folder: str) -> dict:
    payload = dict(body)
    payload.setdefault("folderId", folder)
    req = urllib.request.Request(
        f"{API_BASE}/{path}",
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={
            "Authorization": f"Api-Key {key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    ctx = ssl.create_default_context()
    try:
        with urllib.request.urlopen(req, timeout=30, context=ctx) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", errors="replace")
        return {
            "_http_error": e.code,
            "_body": _redact(raw, key)[:800],
        }
    except Exception as e:
        return {"_error": _redact(str(e), key)}


def _count(value) -> int | None:
    if value is None:
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def top_requests(phrase: str, key: str, folder: str, num: int = 20) -> dict:
    raw = _call("topRequests", {"phrase": phrase, "numPhrases": num}, key, folder)
    if raw.get("_http_error") or raw.get("_error"):
        return {
            "phrase": phrase,
            "ok": False,
            "error": raw.get("_body") or raw.get("_error") or f"HTTP {raw.get('_http_error')}",
        }
    results = [
        {"phrase": r.get("phrase", ""), "count": _count(r.get("count"))}
        for r in raw.get("results") or []
    ]
    associations = [
        {"phrase": r.get("phrase", ""), "count": _count(r.get("count"))}
        for r in raw.get("associations") or []
    ]
    return {
        "phrase": phrase,
        "ok": True,
        "total_count": _count(raw.get("totalCount")),
        "results": results,
        "associations": associations,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Wordstat topRequests. Ключ не логируется.")
    parser.add_argument("phrases", nargs="+", help="Фразы для живого спроса")
    parser.add_argument("--num", type=int, default=15, help="Сколько похожих фраз")
    parser.add_argument("--sleep", type=float, default=0.25)
    args = parser.parse_args()

    key, folder = _env()
    report: dict = {
        "status": "OK",
        "queries": [],
        "note": "",
    }

    if not key or not folder:
        missing = [n for n, v in ((KEY_ENV, key), (FOLDER_ENV, folder)) if not v]
        report["status"] = "PARTIAL"
        report["note"] = "нет env: " + ", ".join(missing) + ". Цифры не выдумывать."
        json.dump(report, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
        return 0

    for i, phrase in enumerate(args.phrases):
        if i:
            time.sleep(args.sleep)
        row = top_requests(phrase, key, folder, num=args.num)
        report["queries"].append(row)
        if not row.get("ok"):
            report["status"] = "PARTIAL"

    if report["status"] == "PARTIAL":
        report["note"] = report.get("note") or "часть запросов не ответила. PARTIAL не стоп."

    json.dump(report, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

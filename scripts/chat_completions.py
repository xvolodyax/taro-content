#!/usr/bin/env python3
"""OpenAI Chat Completions для слотов 12:12 / 15:15 / 21:21.

Канон с 2026-09-09: только ``--model gpt-5.6-sol``.
gpt-5.5 запрещён. Статьи / magiya / Алёна этим скриптом не писать.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from typing import Any

LOCKED_MODEL = "gpt-5.6-sol"
ENDPOINT = "https://api.openai.com/v1/chat/completions"
BLOCKED = frozenset(
    {
        "gpt-5.5",
        "openai-api-gpt-5.5",
        "gpt-5.5-chat-latest",
    }
)
WRITTEN_BY = "openai-api-gpt-5.6-sol"


def lock_model(name: str) -> str:
    raw = (name or "").strip()
    lowered = raw.lower()
    if lowered in BLOCKED or "gpt-5.5" in lowered:
        raise SystemExit(
            "posts lock 2026-09-09: gpt-5.5 запрещён, нужен --model gpt-5.6-sol"
        )
    if raw != LOCKED_MODEL:
        raise SystemExit(
            f"posts lock 2026-09-09: модель {raw!r}, нужен {LOCKED_MODEL}"
        )
    return raw


def build_payload(model: str, prompt: str, system: str) -> dict[str, Any]:
    messages: list[dict[str, str]] = []
    if system.strip():
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    return {"model": model, "messages": messages}


def request_chat(payload: dict[str, Any], api_key: str, timeout: float) -> dict[str, Any]:
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        ENDPOINT,
        data=body,
        method="POST",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        err_body = exc.read().decode("utf-8", errors="replace")
        raise SystemExit(f"openai chat completions HTTP {exc.code}: {err_body}") from exc
    except urllib.error.URLError as exc:
        raise SystemExit(f"openai chat completions network: {exc}") from exc


def extract_text(data: dict[str, Any]) -> str:
    choices = data.get("choices") or []
    if not choices:
        raise SystemExit("openai chat completions: пустой choices")
    message = choices[0].get("message") or {}
    content = message.get("content")
    if isinstance(content, list):
        parts = []
        for item in content:
            if isinstance(item, dict) and item.get("type") == "text":
                parts.append(str(item.get("text") or ""))
            elif isinstance(item, str):
                parts.append(item)
        content = "".join(parts)
    if not isinstance(content, str) or not content.strip():
        raise SystemExit("openai chat completions: пустой content")
    return content


def read_arg_text(literal: str, path: str) -> str:
    if path:
        with open(path, encoding="utf-8") as fh:
            return fh.read()
    return literal


def main() -> int:
    parser = argparse.ArgumentParser(
        description="OpenAI chat completions; posts lock = gpt-5.6-sol"
    )
    parser.add_argument("--model", default=LOCKED_MODEL)
    parser.add_argument("--prompt", default="")
    parser.add_argument("--prompt-file", default="")
    parser.add_argument("--system", default="")
    parser.add_argument("--system-file", default="")
    parser.add_argument("--out", default="")
    parser.add_argument(
        "--check",
        action="store_true",
        help="проверить модель и OPENAI_API_KEY, без запроса",
    )
    parser.add_argument("--timeout", type=float, default=120.0)
    args = parser.parse_args()

    model = lock_model(args.model)
    key = (os.environ.get("OPENAI_API_KEY") or "").strip()
    if args.check:
        if not key:
            print("check=FAIL reason=no_openai_api_key model=" + model, file=sys.stderr)
            return 2
        print(f"check=OK model={model} written_by={WRITTEN_BY} key=present")
        return 0

    prompt = read_arg_text(args.prompt, args.prompt_file).strip()
    if not prompt:
        raise SystemExit("нужен --prompt или --prompt-file")
    system = read_arg_text(args.system, args.system_file)
    if not key:
        raise SystemExit("нет OPENAI_API_KEY — FAIL, текст не подменять")

    data = request_chat(build_payload(model, prompt, system), key, args.timeout)
    text = extract_text(data)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(text)
            if not text.endswith("\n"):
                fh.write("\n")
    else:
        sys.stdout.write(text)
        if not text.endswith("\n"):
            sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())

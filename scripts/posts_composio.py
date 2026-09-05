#!/usr/bin/env python3
"""Composio HTTP: ключ только из env, аккаунт только по alias, не default."""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from typing import Any
DEFAULT_BASE = "https://backend.composio.dev/api/v3"
KEY_ENV = "COMPOSIO_API_KEY"
REDACT = "<redacted>"


class ComposioError(RuntimeError):
    pass


def redact(text: str, extras: list[str] | None = None) -> str:
    out = str(text)
    secrets = [os.environ.get(KEY_ENV) or ""]
    secrets.extend(extras or [])
    for secret in secrets:
        if secret and secret in out:
            out = out.replace(secret, REDACT)
    return out


def api_key() -> str:
    return (os.environ.get(KEY_ENV) or "").strip()


def key_present() -> bool:
    return bool(api_key())


class ComposioClient:
    def __init__(self, base_url: str = DEFAULT_BASE, transport=None) -> None:
        self.base_url = base_url.rstrip("/")
        self.transport = transport
        self._accounts: list[dict[str, Any]] | None = None

    def _headers(self) -> dict[str, str]:
        key = api_key()
        if not key:
            raise ComposioError(f"{KEY_ENV} missing")
        return {
            "x-api-key": key,
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

    def request(self, method: str, path: str, body: dict | None = None) -> dict[str, Any]:
        url = path if path.startswith("http") else f"{self.base_url}{path}"
        payload = json.dumps(body).encode("utf-8") if body is not None else None
        if self.transport is not None:
            return self.transport(method, url, body)
        req = urllib.request.Request(url, data=payload, method=method, headers=self._headers())
        try:
            with urllib.request.urlopen(req, timeout=45) as resp:
                raw = resp.read().decode("utf-8")
        except urllib.error.HTTPError as exc:
            err = exc.read().decode("utf-8", errors="replace")
            raise ComposioError(redact(f"HTTP {exc.code} {err[:400]}")) from None
        except urllib.error.URLError as exc:
            raise ComposioError(redact(f"URL {exc.reason}")) from None
        if not raw:
            return {}
        try:
            data = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise ComposioError("bad JSON from Composio") from exc
        if not isinstance(data, dict):
            return {"data": data}
        return data

    def list_accounts(self) -> list[dict[str, Any]]:
        if self._accounts is not None:
            return self._accounts
        data = self.request("GET", "/connected_accounts?limit=50")
        items = data.get("items") or data.get("data") or []
        if not isinstance(items, list):
            items = []
        safe: list[dict[str, Any]] = []
        for acc in items:
            if not isinstance(acc, dict):
                continue
            toolkit = acc.get("toolkit") or {}
            slug = toolkit.get("slug") if isinstance(toolkit, dict) else toolkit
            safe.append(
                {
                    "id": acc.get("id") or acc.get("nanoid"),
                    "alias": acc.get("alias"),
                    "status": acc.get("status"),
                    "toolkit": slug,
                    "is_default": bool(acc.get("is_default") or acc.get("isDefault")),
                }
            )
        self._accounts = safe
        return safe

    def resolve_alias(self, alias: str) -> dict[str, Any]:
        alias = (alias or "").strip()
        if not alias:
            raise ComposioError("empty alias")
        try:
            accounts = self.list_accounts()
        except ComposioError:
            return {"id": alias, "alias": alias, "status": "UNKNOWN", "resolved": "alias_passthrough"}
        matches = [a for a in accounts if str(a.get("alias") or "") == alias]
        if len(matches) == 1:
            acc = dict(matches[0])
            acc["resolved"] = "alias"
            return acc
        if len(matches) > 1:
            raise ComposioError(f"alias {alias}: несколько аккаунтов")
        # Поиск по toolkit если alias не прописан в REST, но аккаунт нужного типа один
        if alias == "telegram-composia":
            tg_accs = [a for a in accounts if a.get("toolkit") == "telegram" and a.get("status") in {"ACTIVE", "active"}]
            if len(tg_accs) == 1:
                acc = dict(tg_accs[0])
                acc["resolved"] = "toolkit_telegram"
                return acc
        elif alias == "instagram-ru":
            ig_accs = [a for a in accounts if a.get("toolkit") == "instagram" and a.get("status") in {"ACTIVE", "active"} and not a.get("is_default")]
            if len(ig_accs) == 1:
                acc = dict(ig_accs[0])
                acc["resolved"] = "toolkit_instagram_ru"
                return acc
        elif alias == "instagram-en":
            ig_accs = [a for a in accounts if a.get("toolkit") == "instagram" and a.get("status") in {"ACTIVE", "active"} and a.get("is_default")]
            if len(ig_accs) == 1:
                acc = dict(ig_accs[0])
                acc["resolved"] = "toolkit_instagram_en"
                return acc
        # Никогда не брать default / первый попавшийся.
        defaults = [a for a in accounts if a.get("is_default")]
        if defaults:
            raise ComposioError(f"alias {alias} не найден; default запрещён")
        return {"id": alias, "alias": alias, "status": "UNKNOWN", "resolved": "alias_passthrough"}

    def execute(self, tool: str, arguments: dict[str, Any], alias: str) -> dict[str, Any]:
        acc = self.resolve_alias(alias)
        body = {
            "arguments": arguments,
            "connected_account_id": acc.get("id") or alias,
            "version": "latest",
        }
        # Alias ещё раз — чтобы бэкенд не свалился в default.
        if acc.get("alias"):
            body["account"] = acc["alias"]
        data = self.request("POST", f"/tools/execute/{tool}", body)
        if data.get("successful") is False or data.get("success") is False:
            raise ComposioError(redact(str(data.get("error") or data.get("message") or "execute failed")))
        return data

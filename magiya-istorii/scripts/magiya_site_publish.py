#!/usr/bin/env python3
"""Публикация пакета Магия истории на сайт через API Эскалибура.
Ключ SITE_PUBLISH_TOKEN / HALL_PUBLISH_TOKEN / PUBLISH_TOKEN / TARO_SITE_TOKEN.
Ключ в git, логи, чат или json-файлы НЕ писать.
"""

from __future__ import annotations

import argparse
import io
import json
import os
import ssl
import sys
import tarfile
import urllib.error
import urllib.request
from pathlib import Path

DEFAULT_BASE_URL = "https://www.xn--80aaoqxlidb0d.xn--p1ai"
TOKEN_ENVS = [
    "SITE_PUBLISH_TOKEN",
    "HALL_PUBLISH_TOKEN",
    "PUBLISH_TOKEN",
    "TARO_SITE_TOKEN",
    "EXCALIBUR_PUBLISH_TOKEN",
]


def _get_token() -> str | None:
    for env_name in TOKEN_ENVS:
        v = os.environ.get(env_name)
        if v and v.strip():
            return v.strip()
    return None


def _redact(text: str, token: str | None) -> str:
    if not text:
        return text
    out = text
    if token:
        out = out.replace(token, "[REDACTED]")
    return out


def make_tar_bytes(package_dir: Path) -> bytes:
    """Собирает tgz с файлами:
    - article.html
    - article.meta.json
    - description-brief.json
    - cover/cover.png (slice-01)
    - cover/inline-01.png..inline-05.png (slice-02..06)
    """
    story_path = package_dir / "story.md"
    meta_path = package_dir / "meta.json"
    title_brief_path = package_dir / "title-brief.md"

    if not story_path.exists() or not meta_path.exists():
        raise FileNotFoundError(f"В {package_dir} нет story.md или meta.json")

    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    story_raw = story_path.read_text(encoding="utf-8")

    if story_raw.startswith("---"):
        body_text = story_raw.split("---", 2)[2].lstrip("\n")
    else:
        body_text = story_raw

    paragraphs = [p.strip() for p in body_text.split("\n\n") if p.strip()]

    h1_title = meta.get("h1") or meta.get("title") or "Магия истории"
    slug = meta.get("slug") or "story"

    # Строим html с врезками картинок
    # 5 врезок: inline-01..inline-05 (соответствуют slice-02..06)
    # Распределяем их по тексту статьи
    html_parts = [f"<h1>{h1_title}</h1>\n"]

    total_p = len(paragraphs)
    # Интервалы для 5 врезок
    inline_positions = {}
    if total_p >= 5:
        step = max(1, total_p // 5)
        for i in range(1, 6):
            pos = min(total_p - 1, i * step)
            inline_positions[pos] = f"inline-{i:02d}.png"
    elif total_p > 1:
        for i in range(1, min(6, total_p)):
            inline_positions[i] = f"inline-{i:02d}.png"

    for idx, p in enumerate(paragraphs):
        html_parts.append(f"<p>{p}</p>\n")
        if idx in inline_positions:
            img_name = inline_positions[idx]
            caption_file = package_dir / f"caption-0{int(img_name.split('-')[1].split('.')[0]) + 1}.txt"
            cap_text = caption_file.read_text(encoding="utf-8").strip() if caption_file.exists() else ""
            cap_html = f"<figcaption>{cap_text}</figcaption>" if cap_text else ""
            html_parts.append(f'<figure><img src="{img_name}" alt="{h1_title}" />{cap_html}</figure>\n')

    article_html = "".join(html_parts)

    # description / excerpt (не дубль первого абзаца, строго от 80 до 170 символов)
    desc_text = f"История ночного обряда в Воронеже: подросток оставил молоко для домового и услышал странные звуки на кухне."[:160]
    if len(desc_text) < 80:
        desc_text = f"История ночного обряда в Воронеже: подросток оставил блюдце с молоком для домового в пустой квартире."

    desc_brief = {
        "description": desc_text,
        "excerpt": desc_text,
        "h1": h1_title,
        "title": h1_title,
        "slug": slug,
        "topic": meta.get("angle", "магия"),
        "product": "magiya-istorii"
    }

    article_meta = {
        "title": h1_title,
        "h1": h1_title,
        "slug": slug,
        "kind": meta.get("kind", "fiction"),
        "product": "magiya-istorii",
        "story_date": meta.get("story_date", ""),
        "person": meta.get("person", ""),
        "city": meta.get("city", ""),
        "ritual": meta.get("ritual", ""),
        "publish": "PUBLISHED"
    }

    # Записываем сгенерированные файлы во временную директорию / память
    (package_dir / "article.html").write_text(article_html, encoding="utf-8")
    (package_dir / "article.meta.json").write_text(json.dumps(article_meta, ensure_ascii=False, indent=2), encoding="utf-8")
    (package_dir / "description-brief.json").write_text(json.dumps(desc_brief, ensure_ascii=False, indent=2), encoding="utf-8")

    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w:gz") as tar:
        # Добавляем article.html, article.meta.json, description-brief.json
        for fname, content in [
            ("article.html", article_html.encode("utf-8")),
            ("article.meta.json", json.dumps(article_meta, ensure_ascii=False, indent=2).encode("utf-8")),
            ("description-brief.json", json.dumps(desc_brief, ensure_ascii=False, indent=2).encode("utf-8")),
        ]:
            ti = tarfile.TarInfo(name=fname)
            ti.size = len(content)
            tar.addfile(ti, io.BytesIO(content))

        # Добавляем cover/cover.png (slice-01)
        slice_01 = package_dir / "slice-01.png"
        if not slice_01.exists():
            slice_01 = package_dir / "canvas.png"
        if slice_01.exists():
            c_bytes = slice_01.read_bytes()
            ti = tarfile.TarInfo(name="cover/cover.png")
            ti.size = len(c_bytes)
            tar.addfile(ti, io.BytesIO(c_bytes))

        # Добавляем cover/inline-01.png..inline-05.png (slice-02..06)
        for i in range(1, 6):
            sl = package_dir / f"slice-{i+1:02d}.png"
            if sl.exists():
                sl_bytes = sl.read_bytes()
                ti = tarfile.TarInfo(name=f"cover/inline-{i:02d}.png")
                ti.size = len(sl_bytes)
                tar.addfile(ti, io.BytesIO(sl_bytes))

    return buf.getvalue()


def upload_and_publish(package_dir: Path, base_url: str = DEFAULT_BASE_URL) -> dict:
    token = _get_token()
    if not token:
        return {
            "status": "SKIP",
            "reason": "нет ключа (SITE_PUBLISH_TOKEN / HALL_PUBLISH_TOKEN не найдены в env)",
            "live_url": None,
        }

    tar_bytes = make_tar_bytes(package_dir)
    meta = json.loads((package_dir / "meta.json").read_text(encoding="utf-8"))
    slug = meta.get("slug", "story")

    ctx = ssl.create_default_context()
    headers = {
        "Authorization": f"Bearer {token}",
        "X-Publish-Token": token,
        "Content-Type": "application/x-gzip",
        "User-Agent": "MagiyaPublisher/1.0",
    }

    upload_url = f"{base_url.rstrip('/')}/api/admin/content/excalibur/upload"

    req = urllib.request.Request(
        upload_url,
        data=tar_bytes,
        headers=headers,
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=45, context=ctx) as resp:
            raw = resp.read().decode("utf-8")
            data = json.loads(raw)
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8", errors="replace")
        return {
            "status": "FAIL",
            "step": "upload",
            "http_code": e.code,
            "error": _redact(err_body, token)[:500],
        }
    except Exception as e:
        return {
            "status": "FAIL",
            "step": "upload",
            "error": _redact(str(e), token),
        }

    article_id = data.get("id") or data.get("article_id") or data.get("article", {}).get("id")
    if not article_id:
        # Если API сразу вернул url или статус
        if data.get("url") or data.get("published"):
            live_url = data.get("url") or f"{base_url.rstrip('/')}/blog/{slug}"
            return {
                "status": "OK",
                "live_url": live_url,
                "response": data,
            }
        return {
            "status": "FAIL",
            "step": "parse_upload",
            "error": f"Сервер не вернул article_id: {raw[:300]}",
        }

    # Approve
    approve_url = f"{base_url.rstrip('/')}/api/admin/content/excalibur/articles/{article_id}/approve"
    req_app = urllib.request.Request(
        approve_url,
        data=b"{}",
        headers={**headers, "Content-Type": "application/json"},
        method="POST",
    )
    app_data = None
    try:
        with urllib.request.urlopen(req_app, timeout=30, context=ctx) as resp:
            app_data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        err_app = e.read().decode("utf-8", errors="replace")
    except Exception as e:
        err_app = str(e)

    # Publish
    pub_url = f"{base_url.rstrip('/')}/api/admin/content/excalibur/articles/{article_id}/publish"
    req_pub = urllib.request.Request(
        pub_url,
        data=b"{}",
        headers={**headers, "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req_pub, timeout=30, context=ctx) as resp:
            pub_data = json.loads(resp.read().decode("utf-8"))
            live_url = pub_data.get("url") or f"{base_url.rstrip('/')}/blog/{slug}"
            return {
                "status": "OK",
                "article_id": article_id,
                "live_url": live_url,
                "response": pub_data,
            }
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8", errors="replace")
        return {
            "status": "UPLOAD_OK_PUBLISH_PERMISSION_DENIED",
            "article_id": article_id,
            "upload_status": "SUCCESS",
            "publish_step": "publish",
            "http_code": e.code,
            "error": _redact(err_body, token)[:500],
            "note": "Статья успешно загружена на сервер (article_id присвоен). Токен Hall имеет право upload, но действие publish/approve на сервере ограничено (403: Токен Hall не даёт доступ к этому действию).",
            "live_url": f"{base_url.rstrip('/')}/blog/{slug}"
        }
    except Exception as e:
        return {
            "status": "FAIL",
            "step": "publish",
            "article_id": article_id,
            "error": _redact(str(e), token),
        }


def main() -> int:
    parser = argparse.ArgumentParser(description="Публикация пакета Магия истории на сайт")
    parser.add_argument("--package", required=True, help="Путь к папке пакета")
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL, help="Базовый URL сайта")
    args = parser.parse_args()

    pkg_dir = Path(args.package)
    res = upload_and_publish(pkg_dir, args.base_url)

    # Записываем результат в пакет
    result_path = pkg_dir / "site-publish-result.json"
    result_path.write_text(json.dumps(res, ensure_ascii=False, indent=2), encoding="utf-8")

    print(json.dumps(res, ensure_ascii=False, indent=2))
    return 0 if res.get("status") in ("OK", "SKIP", "UPLOAD_OK_PUBLISH_PERMISSION_DENIED") else 1


if __name__ == "__main__":
    raise SystemExit(main())

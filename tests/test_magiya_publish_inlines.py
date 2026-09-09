#!/usr/bin/env python3
"""Публикация: cover-only для живых пакетов; врезки 01..03 если уже нарезаны."""

from __future__ import annotations

import io
import json
import sys
import tarfile
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "magiya-istorii" / "scripts"))

from magiya_site_publish import _article_html, make_tar_bytes  # noqa: E402


def _pkg(tmp: Path, *, inlines: bool) -> Path:
    pkg = tmp / "pkg"
    pkg.mkdir()
    (pkg / "story.md").write_text(
        "---\ntitle: T\nh1: T\n---\n\n"
        "Первый абзац про обряд в городе.\n\n"
        "Второй абзац про жест руками.\n\n"
        "Третий абзац про тишину в комнате.\n\n"
        "Четвёртый абзац про развилку.\n\n"
        "Что делать дальше, если порог уже закрыт?\n",
        encoding="utf-8",
    )
    (pkg / "meta.json").write_text(
        json.dumps({"h1": "T", "title": "T", "slug": "t"}, ensure_ascii=False),
        encoding="utf-8",
    )
    (pkg / "cover.png").write_bytes(b"\x89PNG\r\n\x1a\ncover")
    if inlines:
        for i in range(1, 4):
            (pkg / f"inline-{i:02d}.png").write_bytes(b"\x89PNG\r\n\x1a\n" + bytes([i]))
    return pkg


class PublishInlineTests(unittest.TestCase):
    def test_cover_only_html_when_no_inlines(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            pkg = _pkg(Path(tmp), inlines=False)
            html = _article_html(
                pkg,
                [
                    "Первый абзац про обряд в городе.",
                    "Второй абзац про жест руками.",
                    "Что делать дальше, если порог уже закрыт?",
                ],
                "T",
            )
            self.assertIn("<h1>T</h1>", html)
            self.assertNotIn("inline-", html)
            self.assertNotIn("cover.png", html)

    def test_three_inlines_in_body_not_cover(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            pkg = _pkg(Path(tmp), inlines=True)
            paragraphs = [
                "Первый абзац про обряд в городе.",
                "Второй абзац про жест руками.",
                "Третий абзац про тишину в комнате.",
                "Четвёртый абзац про развилку.",
                "Что делать дальше, если порог уже закрыт?",
            ]
            html = _article_html(pkg, paragraphs, "T")
            self.assertIn('src="inline-01.png"', html)
            self.assertIn('src="inline-02.png"', html)
            self.assertIn('src="inline-03.png"', html)
            self.assertNotIn("cover.png", html)

    def test_tar_has_cover_and_inlines(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            pkg = _pkg(Path(tmp), inlines=True)
            raw = make_tar_bytes(pkg)
            with tarfile.open(fileobj=io.BytesIO(raw), mode="r:gz") as tar:
                names = set(tar.getnames())
            self.assertIn("cover/cover.png", names)
            self.assertIn("cover/inline-01.png", names)
            self.assertIn("cover/inline-02.png", names)
            self.assertIn("cover/inline-03.png", names)
            self.assertIn("article.html", names)


if __name__ == "__main__":
    unittest.main()

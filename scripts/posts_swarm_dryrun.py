#!/usr/bin/env python3
"""Dry-run of posts swarm step records. No Kie pixels required."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECK = ROOT / "scripts" / "posts_gate_check.py"

REQUIRED_AGENTS = [
    "posts-director.md",
    "posts-researcher.md",
    "posts-meaning.md",
    "posts-copywriter.md",
    "posts-cover-text.md",
    "posts-gate.md",
]
FORBIDDEN_AGENTS = [
    "posts-glavred.md",
    "posts-scout.md",
    "posts-writer.md",
    "posts-sol.md",
]


def run_check(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(CHECK), *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )


def write_fragment(path: Path, role: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        f"=== POSTS-{role.upper()} ===\n"
        f"Статус: OK\n"
        f"written_by: gemini\n"
        f"Кратко: dry-run, pixels skipped\n"
        f"Артефакты:\n- (no kie png)\n"
        f"incident_report: none\n",
        encoding="utf-8",
    )


def assert_true(cond: bool, msg: str, errors: list[str]) -> None:
    if not cond:
        errors.append(msg)


def main() -> int:
    errors: list[str] = []
    agents = ROOT / ".cursor" / "agents"
    for name in REQUIRED_AGENTS:
        assert_true((agents / name).is_file(), f"missing agent {name}", errors)
    for name in FORBIDDEN_AGENTS:
        assert_true(not (agents / name).exists(), f"forbidden agent still present: {name}", errors)

    policy = json.loads((ROOT / "shared" / "posts-model-policy.json").read_text(encoding="utf-8"))
    assert_true("glavred" in policy.get("forbidden_roles", []), "policy must forbid glavred", errors)
    assert_true(policy.get("pixels_required_for_pass") is False, "pixels must not block PASS", errors)
    assert_true(
        policy.get("cloud_fallback", {}).get("use") == "Task(generalPurpose)",
        "cloud fallback must be Task(generalPurpose)",
        errors,
    )

    posts = (ROOT / "POSTS.md").read_text(encoding="utf-8")
    assert_true("researcher" in posts and "meaning" in posts and "copywriter" in posts, "POSTS.md missing swarm roles", errors)
    assert_true("Главреда нет" in posts or "Главред" in posts and "нет" in posts, "POSTS.md must drop Glavred", errors)

    canon = run_check(["--canon-only", "--root", str(ROOT)])
    assert_true(canon.returncode == 0, f"canon check failed: {canon.stderr}", errors)

    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        good = tmp_path / "2026-08-27-2121"
        (good / "swarm").mkdir(parents=True)
        (good / "brief.md").write_text("---\nwritten_by: gemini\n---\nсцена\n", encoding="utf-8")
        (good / "meaning.md").write_text("---\nwritten_by: gemini\n---\nтезис\n", encoding="utf-8")
        (good / "debrief.md").write_text("---\nwritten_by: gemini\n---\nкарты\n", encoding="utf-8")
        (good / "tg.html").write_text("<!-- written_by: gemini -->\nкадр\n", encoding="utf-8")
        (good / "vk.html").write_text("<!-- written_by: gemini -->\nкадр\n", encoding="utf-8")
        (good / "yt.txt").write_text(
            "written_by: gemini\nchannel: @todaytaro_club\nссылки в шапке канала\n",
            encoding="utf-8",
        )
        (good / "cover-text.json").write_text(
            json.dumps(
                {
                    "written_by": "gemini",
                    "chosen": "Заходит и молчит",
                    "candidates": ["a", "b", "c"],
                    "placement": "center",
                },
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
        (good / "image-prompt.txt").write_text("hook centered at optical center\n", encoding="utf-8")
        for role in ("researcher", "meaning", "copywriter", "cover-text", "gate"):
            write_fragment(good / "swarm" / f"{role}.md", role)
        (good / "GATE").write_text(
            "=== POSTS GATE ===\nverdict: PASS\ndirector_wrote: no\nglavred_required: no\nincident_report: none\n",
            encoding="utf-8",
        )
        ok = run_check(["--pack", str(good), "--root", str(ROOT)])
        assert_true(ok.returncode == 0, f"good pack should PASS: {ok.stderr}", errors)

        max_pack = tmp_path / "badmax-2121"
        shutil.copytree(good, max_pack)
        (max_pack / "max.txt").write_text("written_by: gemini\nразбор на Макс\n", encoding="utf-8")
        bad_max = run_check(["--pack", str(max_pack), "--root", str(ROOT)])
        assert_true(bad_max.returncode != 0, "21:21 max.txt must FAIL", errors)
        assert_true("max.txt" in bad_max.stderr, f"max.txt fail reason missing: {bad_max.stderr}", errors)

        ig_pack = tmp_path / "badig-2121"
        shutil.copytree(good, ig_pack)
        (ig_pack / "ig-story.txt").write_text("written_by: gemini\nstory\n", encoding="utf-8")
        bad_ig = run_check(["--pack", str(ig_pack), "--root", str(ROOT)])
        assert_true(bad_ig.returncode != 0, "21:21 ig-story.txt must FAIL", errors)
        assert_true("ig-story" in bad_ig.stderr, f"ig-story fail reason missing: {bad_ig.stderr}", errors)

        director_pack = tmp_path / "director-inline"
        shutil.copytree(good, director_pack)
        (director_pack / "tg.html").write_text("я теперь копирайтер\nwritten_by: director\n", encoding="utf-8")
        (director_pack / "swarm" / "copywriter.md").unlink()
        bad_dir = run_check(["--pack", str(director_pack), "--root", str(ROOT)])
        assert_true(bad_dir.returncode != 0, "inline Director writing must FAIL", errors)
        assert_true(
            "Director" in bad_dir.stderr or "written_by" in bad_dir.stderr or "copywriter" in bad_dir.stderr,
            f"director fail reason missing: {bad_dir.stderr}",
            errors,
        )

        glavred_pack = tmp_path / "glavred-step"
        shutil.copytree(good, glavred_pack)
        (glavred_pack / "swarm" / "glavred.md").write_text("required step\n", encoding="utf-8")
        bad_g = run_check(["--pack", str(glavred_pack), "--root", str(ROOT)])
        assert_true(bad_g.returncode != 0, "Glavred as required step must FAIL", errors)
        assert_true("glavred" in bad_g.stderr.lower() or "Главред" in bad_g.stderr, f"glavred reason missing: {bad_g.stderr}", errors)

        dry = ROOT / "posts" / "_dryrun" / "swarm"
        if dry.exists():
            shutil.rmtree(dry)
        for role in ("researcher", "meaning", "copywriter", "cover-text", "gate"):
            write_fragment(dry / f"{role}.md", role)
        assert_true(not list(dry.glob("*.png")), "dry-run must not require pixels", errors)

    if errors:
        sys.stderr.write("SWARM DRY-RUN FAIL\n")
        for item in errors:
            sys.stderr.write(f"- {item}\n")
        return 1
    sys.stdout.write("SWARM DRY-RUN PASS\n")
    sys.stdout.write("step records: posts/_dryrun/swarm/ (no Kie pixels)\n")
    sys.stdout.write("rejected: inline Director writing\n")
    sys.stdout.write("rejected: Glavred as required step\n")
    sys.stdout.write("rejected: 21:21 max.txt\n")
    sys.stdout.write("rejected: 15:15/21:21 Instagram\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

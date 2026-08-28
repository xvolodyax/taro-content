#!/usr/bin/env python3
"""Сухой прогон step records. 0 живых публикаций. Сегодняшние эфиры не трогает."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from posts_gate import evaluate  # noqa: E402
from posts_stamp import stamp_package  # noqa: E402
from posts_step_record import write_record  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
LIVE_TODAY = "2026-08-27"
FIXTURES = ROOT / "posts/fixtures"


def live_packages(root: Path) -> list[Path]:
    posts = root / "posts"
    if not posts.is_dir():
        return []
    return sorted(
        p
        for p in posts.iterdir()
        if p.is_dir() and p.name.startswith(LIVE_TODAY) and p.name[-4:] in {"1212", "1515", "2121"}
    )


def rebuild_steps(package: Path, slot: str, runtime: str) -> None:
    steps = package / "steps"
    if steps.exists():
        shutil.rmtree(steps)
    roles = ["posts-researcher", "posts-meaning", "posts-copywriter"]
    if slot != "1515":
        roles.append("posts-cover-text")
    roles.append("posts-gate")
    for role in roles:
        write_record(package, role, runtime, slot)


def run_fixture(src: Path, dest_root: Path, runtime: str) -> dict:
    slot = src.name.split("-")[-1]
    if slot not in {"1212", "1515", "2121"}:
        slot = "1212"
        if "1515" in src.name:
            slot = "1515"
    dest = dest_root / src.name
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(src, dest)
    rebuild_steps(dest, slot, runtime)
    stamp_package(dest)
    result = evaluate(dest, require_swarm=True)
    return {
        "fixture": src.name,
        "dest": str(dest.relative_to(ROOT)) if dest.is_relative_to(ROOT) else str(dest),
        "verdict": result.verdict,
        "publish_count": result.publish_count,
        "reasons": result.reasons,
        "steps": sorted(p.name for p in (dest / "steps").glob("*.json")),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=ROOT / "posts/_dry-run")
    parser.add_argument("--runtime", choices=("cloud", "plugin"), default="cloud")
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    touched_live = [str(p) for p in live_packages(ROOT)]
    reports = []
    for name in ("swarm-pass-1212", "swarm-pass-1515"):
        src = FIXTURES / name
        if src.is_dir():
            reports.append(run_fixture(src, args.out, args.runtime))
    fail_src = FIXTURES / "swarm-fail-inline"
    if fail_src.is_dir():
        dest = args.out / fail_src.name
        if dest.exists():
            shutil.rmtree(dest)
        shutil.copytree(fail_src, dest)
        result = evaluate(dest, require_swarm=True)
        reports.append(
            {
                "fixture": fail_src.name,
                "dest": str(dest.relative_to(ROOT)) if dest.is_relative_to(ROOT) else str(dest),
                "verdict": result.verdict,
                "publish_count": result.publish_count,
                "reasons": result.reasons,
                "expect": "FAIL",
            }
        )
    publish_total = sum(int(r.get("publish_count") or 0) for r in reports)
    live_after = [str(p) for p in live_packages(ROOT)]
    summary = {
        "publish_total": publish_total,
        "live_packages_untouched": touched_live == live_after,
        "live_today": touched_live,
        "reports": reports,
        "glavred": "REMOVED",
        "hall_publishes": True,
    }
    out_json = args.out / "dry-run.json"
    out_json.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    pass_ok = all(r["verdict"] == "PASS" for r in reports if r.get("fixture", "").startswith("swarm-pass"))
    fail_ok = all(r["verdict"] == "FAIL" for r in reports if r.get("fixture") == "swarm-fail-inline")
    if publish_total != 0 or not pass_ok or not fail_ok or touched_live != live_after:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

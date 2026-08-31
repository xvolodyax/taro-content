#!/usr/bin/env python3
"""Записать step record роя. Директор вызывает после каждого Task."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from posts_dispatch_prompt import POLICY, ROLES, canon_role  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]


def step_index(role: str, slot: str) -> int:
    slot = str(slot).replace(":", "")
    if slot == "2121":
        order = ["posts-researcher", "posts-copywriter", "posts-cover-text", "posts-gate"]
    else:
        order = ["posts-researcher", "posts-meaning", "posts-copywriter"]
        if slot not in {"1515", "alena", "0700"}:
            order.append("posts-cover-text")
        order.append("posts-gate")
    role = canon_role(role)
    return order.index(role) + 1


def short_name(role: str) -> str:
    return canon_role(role).removeprefix("posts-")


def write_record(
    package: Path,
    role: str,
    runtime: str,
    slot: str,
    artifacts: list[str] | None = None,
) -> Path:
    role = canon_role(role)
    spec = ROLES[role]
    runtime = runtime.strip().lower()
    idx = step_index(role, slot)
    name = f"{idx:02d}-{short_name(role)}"
    steps = package / "steps"
    steps.mkdir(parents=True, exist_ok=True)
    prompt_rel = f"steps/{name}.prompt.md"
    if runtime == "cloud":
        from posts_dispatch_prompt import build_prompt

        prompt = build_prompt(role, str(package), "cloud")
        (package / prompt_rel).write_text(prompt, encoding="utf-8")
    record = {
        "role": role,
        "spawn": "Task",
        "subagent_type": (
            POLICY["cloud_spawn"]["subagent_type"]
            if runtime == "cloud"
            else role
        ),
        "model": spec["model"],
        "inline": False,
        "written_by": spec["written_by"],
        "dispatch_prompt": prompt_rel if runtime == "cloud" else None,
        "artifacts": artifacts or spec["artifacts"],
        "publish": "SKIP",
        "runtime": runtime,
    }
    path = steps / f"{name}.json"
    path.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--package", type=Path, required=True)
    parser.add_argument("--role", required=True)
    parser.add_argument("--runtime", choices=("cloud", "plugin"), default="cloud")
    parser.add_argument("--slot", required=True)
    parser.add_argument("--artifacts", default="")
    args = parser.parse_args()
    arts = [a for a in args.artifacts.split(",") if a.strip()] or None
    path = write_record(args.package, args.role, args.runtime, args.slot, arts)
    print(path)


if __name__ == "__main__":
    main()

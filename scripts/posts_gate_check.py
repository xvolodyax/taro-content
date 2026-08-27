#!/usr/bin/env python3
"""Gate HARD rejects: inline Director writing, Glavred as a required step."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

FORBIDDEN_ROLES = {
    "glavred",
    "posts-glavred",
    "dzen-glavred",
    "posts-scout",
    "posts-writer",
    "posts-sol",
}

GLAVRED_AS_STEP = re.compile(
    r"(?:главред|glavred).{0,40}(?:шаг|step|обязател|required|нужен|зови|Task)",
    re.I | re.S,
)
WAIT_PUBLISH = re.compile(r"можно публиковать", re.I)
DIRECTOR_INLINE = re.compile(
    r"(я теперь копирайтер|i am the copywriter now|напишу сам(?:а)? эфир|director writes? (?:tg|debrief|copy))",
    re.I,
)
LOVUSHKA = re.compile(r"ловушк", re.I)

HUMAN_FILES = (
    "brief.md",
    "meaning.md",
    "debrief.md",
    "tg.html",
    "max.txt",
    "vk.html",
    "yt.txt",
    "ig-story.txt",
    "ig.txt",
    "cover-text.json",
)
RAW_URL = re.compile(r"https?://", re.I)


def _read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return ""


def check_canon(root: Path) -> list[str]:
    fails: list[str] = []
    policy_path = root / "shared" / "posts-model-policy.json"
    policy = json.loads(_read(policy_path) or "{}")
    for role in policy.get("forbidden_roles", []):
        if role in ("glavred", "posts-glavred") and role not in policy.get("text_agents", []):
            continue
    if "glavred" in policy.get("text_agents", []) or "posts-glavred" in policy.get(
        "required_steps", []
    ):
        fails.append("policy: Glavred listed as required/text agent")
    if "posts-glavred.md" in [p.name for p in (root / ".cursor" / "agents").glob("*.md")]:
        fails.append("agents: posts-glavred.md exists")
    if (root / ".cursor" / "agents" / "dzen-glavred.md").exists():
        # dzen file in this repo would be a leak into posts machine
        fails.append("agents: dzen-glavred.md leaked into posts repo")

    for rel in (
        "POSTS.md",
        ".cursor/agents/FOR-AGENTS.md",
        "shared/posts-swarm.md",
        "shared/posts-chain.md",
    ):
        text = _read(root / rel)
        if not text:
            fails.append(f"missing canon file: {rel}")
            continue
        if GLAVRED_AS_STEP.search(text) and "нет" not in text.lower() and "запрещ" not in text.lower():
            # allowed if the file forbids Glavred; fail only if it requires it
            pass
        if re.search(
            r"(?:обязательн(?:ый|ым)\s+шаг\s+главред|зови\s+главред|return:\s*glavred|required_steps[^\]]*glavred)",
            text,
            re.I,
        ):
            fails.append(f"{rel}: Glavred appears as required chain step")
        if re.search(r"(?:нужно подождать|жди(?:те)?)\s+«?можно публиковать", text, re.I):
            fails.append(f"{rel}: waits for «можно публиковать»")
    return fails


def check_pack(pack: Path, root: Path | None = None) -> list[str]:
    fails: list[str] = []
    if not pack.is_dir():
        return [f"pack not found: {pack}"]

    swarm = pack / "swarm"
    if (swarm / "glavred.md").exists() or (swarm / "posts-glavred.md").exists():
        fails.append("swarm/glavred.md present: Glavred must not be a step")

    gate = _read(pack / "GATE")
    if WAIT_PUBLISH.search(gate) and "не " not in gate.lower():
        fails.append("GATE requires «можно публиковать»")
    if re.search(r"return:.*glavred", gate, re.I):
        fails.append("GATE returns to Glavred")
    if LOVUSHKA.search(gate):
        fails.append("GATE contains «ловушка»")

    handoff = _read((root or ROOT) / ".cursor" / "posts-handoff.md")
    pack_text = "\n".join(_read(p) for p in pack.glob("*") if p.is_file())
    if DIRECTOR_INLINE.search(handoff) or DIRECTOR_INLINE.search(pack_text):
        fails.append("inline Director writing («я теперь копирайтер»)")

    air = [name for name in ("tg.html", "max.txt", "debrief.md") if (pack / name).exists()]
    if air and not (swarm / "copywriter.md").is_file():
        fails.append("air files without swarm/copywriter.md (Director wrote?)")

    for name in HUMAN_FILES:
        path = pack / name
        if not path.is_file():
            continue
        text = _read(path)
        if LOVUSHKA.search(text):
            fails.append(f"{name}: слово «ловушка»")
        if name.endswith(".json"):
            try:
                data = json.loads(text)
            except json.JSONDecodeError:
                fails.append(f"{name}: invalid json")
                continue
            written = str(data.get("written_by", "")).lower()
        else:
            m = re.search(r"written_by:\s*(\w+)", text)
            written = (m.group(1).lower() if m else "")
        if written in {"director", "glavred", "sol", "scout"}:
            fails.append(f"{name}: written_by={written}")
        if not written:
            fails.append(f"{name}: missing written_by: gemini")
        elif written != "gemini":
            fails.append(f"{name}: written_by must be gemini, got {written}")

    slot = pack.name[-4:] if len(pack.name) >= 4 else ""
    if slot in {"1212", "2121"} and (pack / "tg.html").exists():
        if not (pack / "cover-text.json").exists():
            fails.append("12:12/21:21 missing cover-text.json")
        if (swarm / "cover-text.md").is_file() is False and (pack / "cover-text.json").exists():
            fails.append("cover-text.json without swarm/cover-text.md")

    if slot in {"1515", "2121"}:
        if not (pack / "yt.txt").is_file():
            fails.append(f"{slot}: missing yt.txt")
        if not (pack / "vk.html").is_file():
            fails.append(f"{slot}: missing vk.html")
        if (pack / "ig-story.txt").is_file():
            fails.append(f"{slot}: Instagram dropped; ig-story.txt forbidden")
        if (pack / "ig.txt").is_file():
            fails.append(f"{slot}: Instagram dropped; ig.txt forbidden")
        if (pack / "max.txt").is_file():
            fails.append(f"{slot}: Max dropped; max.txt forbidden")
        yt = _read(pack / "yt.txt")
        if yt and RAW_URL.search(yt):
            fails.append("yt.txt: raw URL forbidden on YT")

    if slot == "1515":
        yt = _read(pack / "yt.txt")
        if yt and not re.search(r"poll_options:\s*4\b", yt):
            fails.append("15:15 yt.txt must set poll_options: 4")

    return fails


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pack", type=Path, default=None)
    parser.add_argument("--canon-only", action="store_true")
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    fails = check_canon(args.root)
    if args.pack and not args.canon_only:
        fails.extend(check_pack(args.pack, args.root))
    if fails:
        sys.stderr.write("GATE CHECK FAIL\n")
        for item in fails:
            sys.stderr.write(f"- {item}\n")
        return 1
    sys.stdout.write("GATE CHECK PASS\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

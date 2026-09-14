#!/usr/bin/env python3
"""Собрать dispatch-prompt для одного шага роя постов."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POLICY = json.loads((ROOT / "shared/posts-model-policy.json").read_text(encoding="utf-8"))

SOL = POLICY["text_model"]
SOL_STAMP = POLICY["written_by"]
SOL_CLI = POLICY.get("openai_cli") or "python3 scripts/chat_completions.py --model gpt-5.6-sol"

ROLES = {
    "posts-researcher": {
        "agent": ".cursor/agents/posts-researcher.md",
        "skill": ".cursor/skills/posts-researcher/SKILL.md",
        "artifacts": ["brief.md"],
        "model": "inherit",
        "written_by": "inherit",
        "extra_canon": [
            "POSTS_SCOUT_CANON.md",
            "posts/_canon-1515/SEED.md",
            "posts/_canon-2121/SEED.md",
        ],
    },
    "posts-meaning": {
        "agent": ".cursor/agents/posts-meaning.md",
        "skill": ".cursor/skills/posts-meaning/SKILL.md",
        "artifacts": ["meaning.md"],
        "model": SOL,
        "written_by": SOL_STAMP,
    },
    "posts-copywriter": {
        "agent": ".cursor/agents/posts-copywriter.md",
        "skill": ".cursor/skills/posts-copywriter/SKILL.md",
        "artifacts": ["tg.html", "vk.html", "debrief.md", "poll.txt"],
        "model": SOL,
        "written_by": SOL_STAMP,
        "extra_canon": [
            "posts/_canon-2121/SEED.md",
            "posts/_canon-2121/debrief.md",
            "posts/_canon-2121/platforms.md",
        ],
    },
    "posts-cover-text": {
        "agent": ".cursor/agents/posts-cover-text.md",
        "skill": ".cursor/skills/posts-cover-text/SKILL.md",
        "artifacts": ["cover-text.json", "image-prompt.txt"],
        "model": SOL,
        "written_by": SOL_STAMP,
    },
    "posts-gate": {
        "agent": ".cursor/agents/posts-gate.md",
        "skill": ".cursor/skills/posts-gate/SKILL.md",
        "artifacts": ["GATE"],
        "model": "inherit",
        "written_by": SOL_STAMP,
        "extra_canon": ["posts/_canon-2121/platforms.md", "posts/_canon-2121/debrief.md"],
    },
}

ALIASES = POLICY["aliases"]


def canon_role(name: str) -> str:
    raw = name if name.startswith("posts-") else f"posts-{name}"
    return ALIASES.get(raw, raw)


def build_prompt(role: str, package: str, runtime: str, ready: str = "") -> str:
    role = canon_role(role)
    if role not in ROLES:
        raise SystemExit(f"unknown role: {role}")
    if role == "posts-director":
        raise SystemExit("Director is not a Task")
    spec = ROLES[role]
    runtime = runtime.strip().lower()
    spawn = (
        "Task(generalPurpose) — этот промпт целиком"
        if runtime == "cloud"
        else f"Task({role})"
    )
    ready_line = ready.strip() or "смотри файлы пакета"
    effort = POLICY.get("cloud_reasoning_effort") or "low"
    extra = spec.get("extra_canon") or []
    extra_block = "".join(f"- {path}\n" for path in extra)
    text_line = (
        f"Текст слота: {SOL_CLI}. Task inherit (не пинить Cursor-slug). gpt-5.5 запрещён."
        if role in POLICY["text_agents"]
        else "Модель шага: inherit (модель окна; не пинить slug). Текст слота не писать."
    )
    scout_line = ""
    if role == "posts-researcher":
        scout_line = (
            "\nScout 12:12 / 15:15: ниша relations+marriage+kids+family+tarot_moment. "
            "Анти-монотонность против зажёванного chat_promise. Холл угол не назначает. "
            "21:21 угол не выбирает.\n"
            "Скрипт: python3 scripts/posts_scout_clusters.py --lookback-days 7\n"
        )
    return f"""Ты один шаг роя постов ТАРО СЕЙЧАС. Не Директор.

Роль: {role}
Пакет: {package}
Runtime: {runtime}
Спавн: {spawn}
{text_line}
reasoning_effort: {effort}
# high — только явный оверрайд Владимира
written_by: {spec["written_by"]}
канон модели: docs/POSTS_TEXT_MODEL.md
publish: SKIP
Главред: REMOVED. Не писать «можно публиковать».
Дефолтный Cloud Agent / Director текст не пишет. Нет OpenAI API / модели — FAIL, без своего черновика.

Прочитай целиком и следуй:
- {spec["agent"]}
- {spec["skill"]}
- POSTS.md
{extra_block}- shared/posts-soul.md
- shared/posts-funnel.md
- shared/posts-step-contract.md
- shared/posts-model-policy.json
{scout_line}
Уже готово: {ready_line}
Артефакты этого шага: {", ".join(spec["artifacts"])}

Запрещено:
- писать соседние роли (тема + тезис + пост + хук в одних руках)
- Task(posts-*), /in-cloud, /babysit, environment: cloud
- публиковать, ходить в Telegram/Composio/browser
- генерировать картинку / звать Kie
- Главред, слово «ловушка»
- Opus / Sonnet / Composer / gpt-5.5 как писатель слота

Верни Директору маркер роли и список файлов. Не публикуй.
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--role", required=True)
    parser.add_argument("--package", required=True)
    parser.add_argument("--runtime", choices=("cloud", "plugin"), default="cloud")
    parser.add_argument("--ready", default="")
    args = parser.parse_args()
    print(build_prompt(args.role, args.package, args.runtime, args.ready), end="")


if __name__ == "__main__":
    main()

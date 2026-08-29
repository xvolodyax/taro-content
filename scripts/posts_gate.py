#!/usr/bin/env python3
"""Механический Gate роя постов. Inline Директора и чужой писатель = FAIL."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POLICY = json.loads((ROOT / "shared/posts-model-policy.json").read_text(encoding="utf-8"))
ALIASES = POLICY["aliases"]
FORBIDDEN_WRITERS = tuple(name.lower() for name in POLICY["forbidden_writers"])
BOT_TG = "https://t.me/TodayTaro_bot?start=id8293683394"
APP_TG = "https://t.me/TodayTaro_bot?startapp=ref_361BDE45"

THEME_TITLES = (
    "писать первой",
    "любит или нет",
    "скучает ли он",
    "что у него ко мне",
    "что он думает",
    "что он чувствует",
)

STOP_PHRASES = (
    "ловушка",
    "можно публиковать",
    "главред",
    "загадай ситуацию",
    "давай честно",
    "знакомо?",
    "без розовых очков",
)

SLOT_RE = re.compile(r"(?P<date>\d{4}-\d{2}-\d{2})-(?P<slot>1212|1515|2121|alena)$")
SCENA_RE = re.compile(r"(?i)(?:^|\n)\s*«?сцена»?\s*(?:[:.\-—–]|$)|«сцена»")


class _Visible(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []

    def handle_data(self, data: str) -> None:
        self.parts.append(data)


def visible_text(html: str) -> str:
    parser = _Visible()
    parser.feed(re.sub(r"<!--.*?-->", "", html, flags=re.S))
    return "".join(parser.parts)


def canon_role(name: str) -> str:
    raw = name if name.startswith("posts-") else f"posts-{name}"
    return ALIASES.get(raw, raw)


def detect_slot(package: Path) -> str:
    match = SLOT_RE.search(package.name)
    if match:
        return match.group("slot")
    meta = package / "package.meta.json"
    if meta.is_file():
        slot = str(json.loads(meta.read_text(encoding="utf-8")).get("slot") or "")
        slot = slot.replace(":", "")
        if slot in {"0700", "alena", "alena-0700", "alena0700"}:
            return "alena"
        if slot in {"1212", "1515", "2121", "alena"}:
            return slot
    brief = package / "brief.md"
    if brief.is_file():
        text = brief.read_text(encoding="utf-8")
        if "15:15" in text or "slot: 1515" in text:
            return "1515"
        if "21:21" in text or "slot: 2121" in text:
            return "2121"
        if "12:12" in text or "slot: 1212" in text:
            return "1212"
        if "alena" in text.lower() or "07:00" in text:
            return "alena"
    raise SystemExit(f"cannot detect slot: {package}")


def required_steps(slot: str) -> list[str]:
    if slot == "2121":
        return ["posts-copywriter", "posts-gate"]
    roles = ["posts-researcher", "posts-meaning", "posts-copywriter"]
    if slot not in {"1515", "alena"}:
        roles.append("posts-cover-text")
    roles.append("posts-gate")
    return roles


def _meta(package: Path) -> dict:
    path = package / "package.meta.json"
    if not path.is_file():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def preview_poll_only(package: Path) -> bool:
    preview = str(_meta(package).get("preview") or "").lower()
    return preview in {"poll-only", "poll", "preview"}


def evening_hold(package: Path) -> bool:
    return str(_meta(package).get("evening") or "").upper() == "HOLD"


def poll_locked(package: Path) -> bool:
    meta = _meta(package)
    if meta.get("poll_locked") is True:
        return True
    return str(meta.get("evening") or "").upper() in {"ATTACHED", "WRITTEN"}


def first_line(package: Path) -> str:
    for name in ("tg.html", "max.txt", "vk.html"):
        path = package / name
        if path.is_file():
            text = path.read_text(encoding="utf-8")
            if name.endswith(".html"):
                text = visible_text(text)
            for line in text.splitlines():
                line = line.strip()
                if line and not line.startswith("written_by") and not line.startswith("<!--"):
                    return line
    return ""


@dataclass
class GateResult:
    verdict: str = "PASS"
    reasons: list[str] = field(default_factory=list)
    publish_count: int = 0
    tg_len: int = 0
    slot: str = ""

    def fail(self, reason: str) -> None:
        self.verdict = "FAIL"
        self.reasons.append(reason)


def load_steps(package: Path) -> dict[str, dict]:
    out: dict[str, dict] = {}
    steps = package / "steps"
    if not steps.is_dir():
        return out
    for path in sorted(steps.glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        role = canon_role(str(data.get("role") or path.stem.split("-", 1)[-1]))
        data["_path"] = str(path.relative_to(package))
        out[role] = data
    return out


def check_writer_stamp(text: str, label: str, result: GateResult) -> None:
    low = text.lower()
    for name in FORBIDDEN_WRITERS:
        if f"written_by: {name}" in low or f'"written_by": "{name}"' in low:
            result.fail(f"{label}: written_by {name} = FAIL")
    if "главред" in low and "removed" not in low:
        result.fail(f"{label}: Главред не удалён")
    if "можно публиковать" in low and label != "GATE":
        result.fail(f"{label}: «можно публиковать» от Главреда запрещено")


def check_funnel(text: str, slot: str, filename: str, result: GateResult) -> None:
    if "ловушка" in text.lower():
        result.fail(f"{filename}: слово «ловушка»")
    if slot == "1515":
        return
    if filename == "ig.txt":
        if re.search(r"https?://", text):
            result.fail("ig.txt: сырой URL")
        if "шапк" not in text.lower() and "шапке" not in text.lower():
            result.fail("ig.txt: нет «ссылки в шапке»")
        return
    if filename == "yt.txt":
        if "шапк" not in text.lower():
            result.fail("yt.txt: нет «ссылки в шапке»")
        return
    if filename == "tg.html":
        low = text.lower()
        if "start=id8293683394" in text and "startapp=ref_361BDE45" in text:
            bot_pos = text.find("start=id8293683394")
            app_pos = text.find("startapp=ref_361BDE45")
            audio_pos = low.find("аудио")
            triplet_pos = low.find("3 расклад")
            if audio_pos >= 0 and abs(audio_pos - bot_pos) < 70 and abs(audio_pos - app_pos) > 70:
                result.fail("tg.html: аудио повешено на бота, не на приложение")
            if triplet_pos >= 0 and abs(triplet_pos - app_pos) < 70 and abs(triplet_pos - bot_pos) > 70:
                result.fail("tg.html: три расклада повешены на приложение")
        elif "аудио" in low and "start=id8293683394" in text and "startapp=" not in text:
            result.fail("tg.html: аудио без ссылки приложения")


def check_swarm(package: Path, slot: str, result: GateResult, require_swarm: bool) -> None:
    if slot == "1515" and (
        evening_hold(package) or preview_poll_only(package) or poll_locked(package)
    ):
        return
    steps = load_steps(package)
    has_copy = any((package / name).is_file() for name in ("tg.html", "vk.html", "max.txt"))
    if require_swarm or steps or (package / "package.meta.json").is_file():
        if not steps and has_copy:
            result.fail("Director wrote copy inline: нет steps/, есть тексты")
            return
        for role in required_steps(slot):
            rec = steps.get(role)
            if rec is None:
                result.fail(f"нет step record: {role}")
                continue
            if rec.get("inline") is True:
                result.fail(f"{role}: inline=true (Директор писал сам)")
            if rec.get("spawn") != "Task":
                result.fail(f"{role}: spawn должен быть Task")
            if rec.get("publish") not in {None, "SKIP"}:
                result.fail(f"{role}: publish не SKIP")
                result.publish_count += 1
            sub = str(rec.get("subagent_type") or "")
            runtime = str(rec.get("runtime") or "")
            if sub == "posts-director":
                result.fail("нельзя Task(posts-director)")
            if sub == "generalPurpose" or runtime == "cloud":
                prompt = rec.get("dispatch_prompt")
                if not prompt:
                    result.fail(f"{role}: cloud шаг без dispatch-prompt")
                else:
                    path = package / str(prompt)
                    if not path.is_file():
                        result.fail(f"{role}: нет файла {prompt}")
                    else:
                        body = path.read_text(encoding="utf-8")
                        agent = f".cursor/agents/{role}.md"
                        if agent not in body:
                            result.fail(f"{role}: dispatch-prompt без {agent}")
                        if "Task(generalPurpose)" not in body and "generalPurpose" not in body:
                            result.fail(f"{role}: cloud dispatch без generalPurpose")
            elif sub not in {role, *{k for k, v in ALIASES.items() if v == role}}:
                result.fail(f"{role}: плохой subagent_type {sub}")
            if role in POLICY["text_agents"]:
                model = str(rec.get("model") or "")
                if model != POLICY["text_model"]:
                    result.fail(f"{role}: модель {model}, нужен {POLICY['text_model']}")
                writer = str(rec.get("written_by") or "").lower()
                if writer in FORBIDDEN_WRITERS:
                    result.fail(f"{role}: written_by {writer} = FAIL")
                if writer and writer != "gemini":
                    result.fail(f"{role}: written_by {writer}, нужен gemini")
        if any(canon_role(k).endswith("glavred") or "glavred" in k for k in steps):
            result.fail("шаг Главреда запрещён")


OLD_2121 = (
    "ты проголосовала. вот расклад по твоему варианту",
    "действие руками сегодня вечером",
)
WHEN_WRITES = ("когда напишет", "когда он напишет", "когда напишет?")
FROZEN_TEMPLATE = (
    "о чём он думает когда молчит",
    "о чем он думает когда молчит",
)
FAIRY = ("он думает о тебе, потерпи", "он думает о тебе потерпи")
EMPTY_TRY_ON = ("примерьте на свою", "примерь на свою", "примерить на свою")
SUIT_METAPHOR = (
    "живая вода",
    "щуп",
    "дозрел до",
)
HER_TOKENS = ("неё", "нее", "тебе", "тебя", "ты ", "ты.", "ей", "читатель", "собой", "себе")


def check_debrief_rubric(text: str, label: str, result: GateResult) -> None:
    low = text.lower()
    if "вариант 4" in low and "совет" in low:
        result.fail(f"{label}: старая форма 4 советов на варианты")
    pos = len(re.findall(r"(?im)^##\s*позиция\s*[123]", text))
    if pos < 3:
        result.fail(f"{label}: нужны 3 позиции рубрики, не 4 совета")
    if "когда напишет" in low:
        result.fail(f"{label}: нельзя тянуть «когда напишет»")
    for phrase in FROZEN_TEMPLATE:
        if phrase in low:
            result.fail(f"{label}: запечён шаблон тишины")
    third = re.search(
        r"(?is)##\s*позиция\s*3.*?(?=##\s*позиция|\Z)",
        text,
    )
    if third:
        blob = third.group(0).lower()
        if not any(tok in blob for tok in HER_TOKENS):
            result.fail(f"{label}: позиция 3 должна быть про неё")
    for phrase in EMPTY_TRY_ON:
        if phrase in low:
            result.fail(f"{label}: пустая вода про «примерить»")


def check_2121_text(vis: str, label: str, result: GateResult) -> None:
    low = vis.lower()
    if SCENA_RE.search(vis) or "«сцена»" in low:
        result.fail(f"{label}: слово «Сцена» запрещено")
    for phrase in EMPTY_TRY_ON:
        if phrase in low:
            result.fail(f"{label}: пустая вода про «примерить»")
    if "похоже" not in low or "не то" not in low:
        result.fail(f"{label}: нет пульса «Похоже? / Не то»")
    pulse = re.search(r"(?i)похоже", vis)
    body = vis[: pulse.start()] if pulse else vis
    if not any(tok in body.lower() for tok in HER_TOKENS):
        result.fail(f"{label}: позиция 3 должна быть про неё")
    if "когда напишет" in low:
        result.fail(f"{label}: нельзя тянуть «когда напишет»")
    for phrase in OLD_2121:
        if phrase in low:
            result.fail(f"{label}: убитая форма 4 советов на варианты")
    for phrase in FAIRY:
        if phrase in low:
            result.fail(f"{label}: дневная сказка")
    for phrase in SUIT_METAPHOR:
        if phrase in low:
            result.fail(f"{label}: метафора мастей / «дозрел до»")


def check_editorial(package: Path, slot: str, result: GateResult) -> None:
    line = first_line(package)
    if line:
        compact = re.sub(r"[?!.…]+$", "", line).strip()
        if compact.isupper() and len(compact.split()) <= 6:
            result.fail("первая строка — заголовок темы капсом, не сцена")
        if compact.lower() in THEME_TITLES:
            result.fail("первая строка — ярлык темы, не сцена")
        if compact.endswith("?") and compact.isupper():
            result.fail("первая строка — тема-вопрос, не кадр")
    for rel in POLICY["human_text_files"] + ["brief.md", "GATE", "package.meta.json"]:
        path = package / rel
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        check_writer_stamp(text, rel, result)
        for phrase in STOP_PHRASES:
            if phrase in text.lower() and rel != "GATE":
                if phrase == "главред" and "removed" in text.lower():
                    continue
                if phrase == "ловушка" and rel in {"GATE", "brief.md"}:
                    # mention in checklist is ok only as ban
                    if "нет слова" in text.lower() or "не использовать" in text.lower():
                        continue
                result.fail(f"{rel}: стоп «{phrase}»")
        if path.suffix in {".html", ".txt", ".md"} and rel != "brief.md":
            check_funnel(text, slot, rel, result)
    tg = package / "tg.html"
    if tg.is_file():
        vis = visible_text(tg.read_text(encoding="utf-8"))
        result.tg_len = len(vis)
        if slot in {"1212", "2121"} and result.tg_len > 1024:
            result.fail(f"tg.html visible {result.tg_len} > 1024")
    if slot == "1515":
        if (package / "cover-text.json").is_file() or (package / "image-prompt.txt").is_file():
            result.fail("15:15 не должен иметь cover/image")
        if (package / "ig.txt").is_file() or (package / "max.txt").is_file():
            result.fail("15:15: нет Макс / IG")
        poll = package / "poll.txt"
        if poll.is_file():
            lines = [ln for ln in poll.read_text(encoding="utf-8").splitlines() if ln.strip()]
            if len(lines) != 5:
                result.fail(f"15:15: poll.txt должен быть 5 строк, сейчас {len(lines)}")
        debrief = package / "debrief.md"
        if evening_hold(package) or preview_poll_only(package):
            if debrief.is_file():
                result.fail("15:15 evening HOLD: debrief.md не писать")
        elif debrief.is_file():
            check_debrief_rubric(debrief.read_text(encoding="utf-8"), "debrief.md", result)
    if slot in {"1212", "2121"}:
        cover = package / "cover-text.json"
        if cover.is_file():
            data = json.loads(cover.read_text(encoding="utf-8"))
            if data.get("placement") != "center":
                result.fail("cover placement не center")
            cands = data.get("candidates") or []
            if len(cands) != 3:
                result.fail("cover: нужны ровно 3 хука")
            if not data.get("chosen"):
                result.fail("cover: не выбран хук")
        if slot == "1212":
            for name in ("ig.txt", "yt.txt", "max.txt", "vk.html"):
                if not (package / name).is_file():
                    result.fail(f"12:12: нет {name}")
        if slot == "2121":
            if (package / "ig.txt").is_file() or (package / "max.txt").is_file():
                result.fail("21:21: не писать IG/Макс")
            if not (package / "vk.html").is_file():
                result.fail("21:21: нет vk.html (пульс Похоже / Не то)")
            if tg.is_file():
                vis = visible_text(tg.read_text(encoding="utf-8"))
                check_2121_text(vis, "tg.html", result)
            vk = package / "vk.html"
            if vk.is_file():
                check_2121_text(visible_text(vk.read_text(encoding="utf-8")), "vk.html", result)
            debrief = package / "debrief.md"
            if debrief.is_file():
                check_debrief_rubric(debrief.read_text(encoding="utf-8"), "debrief.md", result)
    meta = package / "package.meta.json"
    if meta.is_file():
        data = json.loads(meta.read_text(encoding="utf-8"))
        if str(data.get("publish") or "SKIP").upper() != "SKIP":
            result.fail("package.meta.json: publish не SKIP")
            result.publish_count += 1
        if str(data.get("written_by") or "").lower() in FORBIDDEN_WRITERS:
            result.fail("package.meta.json: запрещённый писатель")
        if str(data.get("glavred") or "").upper() not in {"", "REMOVED", "NONE", "SKIP"}:
            result.fail("Главред не REMOVED")
        if data.get("director_inline") is True:
            result.fail("director_inline=true")


def evaluate(package: Path, require_swarm: bool = False) -> GateResult:
    result = GateResult()
    result.slot = detect_slot(package)
    check_swarm(package, result.slot, result, require_swarm)
    check_editorial(package, result.slot, result)
    return result


def write_gate_file(package: Path, result: GateResult) -> None:
    reasons = "\n".join(f"- {r}" for r in result.reasons) or "резать нечего"
    text = f"""=== POSTS GATE ===
slot: {package.name}
verdict: {result.verdict}
return: {"copywriter" if result.verdict == "FAIL" else "none"}
publish: SKIP
glavred: REMOVED
director_inline: {"FAIL" if any("inline" in r.lower() or "steps/" in r for r in result.reasons) else "ok"}
tg_len: {result.tg_len or "n/a"}
incident_report: none

# Причины
{reasons}

# Чеклист
- [ ] 12:12/15:15: researcher → meaning → copywriter → cover-text? → gate
- [ ] 21:21: один writer → gate (meaning нет)
- [ ] Директор / Холл не писал inline
- [ ] written_by: gemini
- [ ] Главред снят, фразы Главреда нет
- [ ] нет слова «ловушка»
- [ ] бот ≠ приложение
- [ ] 21:21: длина, нет «Сцена», нет пустой воды про «примерить», пульс, позиция 3 = она
- [ ] Gate предложения не переписывает
- [ ] publish SKIP у писателей; эфир — posts_publish.py
"""
    (package / "GATE").write_text(text, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--package", type=Path, required=True)
    parser.add_argument("--require-swarm", action="store_true")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    result = evaluate(args.package, require_swarm=args.require_swarm)
    if args.write:
        write_gate_file(args.package, result)
    print(f"verdict={result.verdict}")
    print(f"publish_count={result.publish_count}")
    print(f"tg_len={result.tg_len}")
    for reason in result.reasons:
        print(f"FAIL: {reason}")
    return 0 if result.verdict == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Механический Gate роя постов. Inline Директора и чужой писатель = FAIL."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from datetime import date
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POLICY = json.loads((ROOT / "shared/posts-model-policy.json").read_text(encoding="utf-8"))
ALIASES = POLICY["aliases"]
FORBIDDEN_WRITERS = tuple(name.lower() for name in POLICY["forbidden_writers"])
POST_SLOTS = set(POLICY.get("post_slots") or ["1212", "1515", "2121"])
POST_WRITER = str(POLICY.get("written_by") or "openai-api-gpt-5.6-sol").lower()
ALENA_WRITER = str(POLICY.get("alena_written_by") or "gemini").lower()
POST_TEXT_MODEL = str(POLICY.get("text_model") or "gpt-5.6-sol")


def required_writer(slot: str) -> str:
    return POST_WRITER if slot in POST_SLOTS else ALENA_WRITER


def required_text_model(slot: str) -> str:
    if slot in POST_SLOTS:
        return POST_TEXT_MODEL
    return str(POLICY.get("alena_text_model") or "inherit")
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
FOUR_CARDS_SINCE = date(2026, 9, 15)
PLAIN_1212_SINCE = date(2026, 9, 16)
FOG_1212 = (
    "забирает внимание у",
    "опора в собственных планах",
    "опора в планах",
    "вернуть себе ясность",
    "вернуть ясность",
    "обозначить для себя",
    "динамика неопределённости",
    "пространство для",
)
ACTION_MENU_1212 = (
    "поднять разговор",
    "обозначить срок",
)
HEADING_1212_RE = re.compile(
    r"(?im)^(?:если\s+выбираешь(?:\s+ход(?:\s+на\s+сегодня)?)?|ход\s+на\s+сегодня|что\s+сделать\s+сегодня)\s*:?\s*$"
)
ADVICE_TOKENS = (
    "напиш",
    "не пиш",
    "не пиши",
    "границ",
    "подожд",
    "жди ",
    "ждать",
    "спроси",
    "до утра",
    "до вечера",
    "не отвеч",
    "поставь",
    "закрыт",
)


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


def package_date(package: Path) -> date | None:
    match = SLOT_RE.search(package.name)
    if match:
        try:
            return date.fromisoformat(match.group("date"))
        except ValueError:
            return None
    meta = package / "package.meta.json"
    if meta.is_file():
        raw = str(json.loads(meta.read_text(encoding="utf-8")).get("date") or "")
        if raw:
            try:
                return date.fromisoformat(raw[:10])
            except ValueError:
                return None
    return None


def uses_four_cards(package: Path, slot: str) -> bool:
    if slot != "2121":
        return False
    day = package_date(package)
    if day is None:
        return True
    return day >= FOUR_CARDS_SINCE


def uses_plain_1212(package: Path, slot: str) -> bool:
    if slot != "1212":
        return False
    day = package_date(package)
    if day is None:
        return True
    return day >= PLAIN_1212_SINCE


def check_1212_text(vis: str, label: str, result: GateResult) -> None:
    low = vis.lower()
    if "если выбираешь ход на сегодня" in low:
        result.fail(f"{label}: запрещён заголовок «Если выбираешь ход на сегодня»")
    if HEADING_1212_RE.search(vis):
        result.fail(f"{label}: запрещён заголовок-меню хода")
    for phrase in FOG_1212:
        if phrase in low:
            result.fail(f"{label}: мутное эссе «{phrase}»")
    if "спроси у карт:" not in low:
        result.fail(f"{label}: нет заголовка «Спроси у карт:»")
        return
    match = re.search(r"(?is)спроси у карт\s*:\s*(.*)", vis)
    if not match:
        result.fail(f"{label}: нет заголовка «Спроси у карт:»")
        return
    rest = match.group(1)
    bullets = re.findall(r"(?m)^\s*[•·]\s+\S.*", rest)
    if not (2 <= len(bullets) <= 3):
        result.fail(f"{label}: нужны 2–3 вопроса «•» после «Спроси у карт:»")
    block = rest.lower()
    for phrase in ACTION_MENU_1212:
        if phrase in block:
            result.fail(f"{label}: вопросы-меню действий, не вопросы к картам")
    qmarks = sum(1 for line in bullets if "?" in line)
    if bullets and qmarks < min(2, len(bullets)):
        result.fail(f"{label}: вопросы к картам должны быть вопросами")


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
    cover_md5: str = ""
    cover_hook: str = ""

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


def check_writer_stamp(text: str, label: str, result: GateResult, slot: str = "") -> None:
    low = text.lower()
    for name in FORBIDDEN_WRITERS:
        if f"written_by: {name}" in low or f'"written_by": "{name}"' in low:
            result.fail(f"{label}: written_by {name} = FAIL")
    if slot in POST_SLOTS and label in POLICY["human_text_files"]:
        expect = required_writer(slot)
        if f"written_by: {expect}" not in low and f'"written_by": "{expect}"' not in low:
            result.fail(f"{label}: нет written_by {expect}")
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
                expect_model = required_text_model(slot)
                if model != expect_model:
                    result.fail(f"{role}: модель {model}, нужен {expect_model}")
                writer = str(rec.get("written_by") or "").lower()
                if writer in FORBIDDEN_WRITERS:
                    result.fail(f"{role}: written_by {writer} = FAIL")
                expect_writer = required_writer(slot)
                if writer and writer != expect_writer:
                    result.fail(f"{role}: written_by {writer}, нужен {expect_writer}")
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


def check_debrief_rubric(text: str, label: str, result: GateResult, four: bool = False) -> None:
    low = text.lower()
    if "вариант 4" in low and "совет" in low:
        result.fail(f"{label}: старая форма 4 советов на варианты")
    needed = 4 if four else 3
    pos = len(re.findall(r"(?im)^##\s*позиция\s*[1234]", text))
    if pos < needed:
        if four:
            result.fail(f"{label}: с 15.09 нужны 4 позиции, позиция 4 = совет")
        else:
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
    if four:
        fourth = re.search(
            r"(?is)##\s*позиция\s*4.*?(?=##\s*позиция|\Z)",
            text,
        )
        if fourth:
            blob = fourth.group(0).lower()
            if "отпусти" in blob:
                result.fail(f"{label}: позиция 4 пустое «отпусти»")
            if not any(tok in blob for tok in ADVICE_TOKENS):
                result.fail(f"{label}: позиция 4 должна быть ходом сейчас")
    for phrase in EMPTY_TRY_ON:
        if phrase in low:
            result.fail(f"{label}: пустая вода про «примерить»")


def card_has_heading(vis: str, card: str) -> bool:
    escaped = re.escape(card)
    return bool(
        re.search(rf"(?is)<b>\s*{escaped}\s*</b>", vis)
        or re.search(rf"(?im)^\*\*{escaped}\*\*", vis)
        or re.search(rf"(?im)^##\s*{escaped}\b", vis)
        or re.search(rf"(?im)^{escaped}\s*$", vis)
    )


def check_2121_text(
    vis: str,
    label: str,
    result: GateResult,
    *,
    four: bool = False,
    cards: list[str] | None = None,
) -> None:
    low = vis.lower()
    if SCENA_RE.search(vis) or "«сцена»" in low:
        result.fail(f"{label}: слово «Сцена» запрещено")
    for phrase in EMPTY_TRY_ON:
        if phrase in low:
            result.fail(f"{label}: пустая вода про «примерить»")
    if not any(tok in low for tok in HER_TOKENS):
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
    if four:
        if "вытянула четыре карты" not in low:
            result.fail(f"{label}: нет строки «Вытянула четыре карты»")
        for card in cards or []:
            if card and card.lower() not in low:
                result.fail(f"{label}: не названа карта {card}")
            elif card and not card_has_heading(vis, card):
                result.fail(f"{label}: нет заголовка карты {card}")
        if "отпусти" in low:
            result.fail(f"{label}: пустое «отпусти» вместо хода")


def load_cards_json(package: Path, result: GateResult, four: bool) -> list[str]:
    path = package / "cards.json"
    if not path.is_file():
        return []
    data = json.loads(path.read_text(encoding="utf-8"))
    cards = [str(name) for name in (data.get("cards") or []) if str(name).strip()]
    if four:
        count = int(data.get("count") or 0)
        if count != 4 or len(cards) != 4:
            result.fail("cards.json: с 15.09 count: 4 и четыре имени")
        positions = data.get("positions") or []
        if positions and len(positions) < 4:
            result.fail("cards.json: нужны 4 позиции")
        if len(positions) >= 4:
            name = str(positions[3].get("name") or "").lower()
            if "совет" not in name and "ход" not in name and "делать" not in name:
                result.fail("cards.json: позиция 4 = совет сейчас")
    return cards


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
        check_writer_stamp(text, rel, result, slot)
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
            result.cover_hook = str(data.get("chosen") or "")
            if data.get("placement") != "center":
                result.fail("cover placement не center")
            cands = data.get("candidates") or []
            if len(cands) != 3:
                result.fail("cover: нужны ровно 3 хука")
            if not data.get("chosen"):
                result.fail("cover: не выбран хук")
        cover_img = package / "cover.png"
        if cover_img.is_file():
            import hashlib
            cur_md5 = hashlib.md5(cover_img.read_bytes()).hexdigest()
            result.cover_md5 = cur_md5
            # Anti-stale: compare with other covers in posts/*/cover.png
            root_posts = ROOT / "posts"
            if root_posts.is_dir():
                for other in root_posts.glob("*/cover.png"):
                    if other.resolve() != cover_img.resolve():
                        other_md5 = hashlib.md5(other.read_bytes()).hexdigest()
                        if other_md5 == cur_md5:
                            result.fail(f"cover.png дублирует {other.parent.name} (md5 {cur_md5})")
                            break
        if slot == "1212":
            for name in ("ig.txt", "yt.txt", "max.txt", "vk.html"):
                if not (package / name).is_file():
                    result.fail(f"12:12: нет {name}")
            if uses_plain_1212(package, slot):
                for name in ("tg.html", "vk.html", "max.txt", "ig.txt", "yt.txt"):
                    path = package / name
                    if not path.is_file():
                        continue
                    raw = path.read_text(encoding="utf-8")
                    vis = visible_text(raw) if name.endswith(".html") else raw
                    check_1212_text(vis, name, result)
        if slot == "2121":
            four = uses_four_cards(package, slot)
            cards = load_cards_json(package, result, four)
            if (package / "ig.txt").is_file() or (package / "max.txt").is_file():
                result.fail("21:21: не писать IG/Макс")
            if not (package / "vk.html").is_file():
                result.fail("21:21: нет vk.html")
            if tg.is_file():
                raw = tg.read_text(encoding="utf-8")
                check_2121_text(raw, "tg.html", result, four=four, cards=cards)
            vk = package / "vk.html"
            if vk.is_file():
                check_2121_text(
                    vk.read_text(encoding="utf-8"),
                    "vk.html",
                    result,
                    four=four,
                    cards=cards,
                )
            debrief = package / "debrief.md"
            if debrief.is_file():
                check_debrief_rubric(
                    debrief.read_text(encoding="utf-8"),
                    "debrief.md",
                    result,
                    four=four,
                )
    meta = package / "package.meta.json"
    if meta.is_file():
        data = json.loads(meta.read_text(encoding="utf-8"))
        if str(data.get("publish") or "SKIP").upper() != "SKIP":
            result.fail("package.meta.json: publish не SKIP")
            result.publish_count += 1
        meta_writer = str(data.get("written_by") or "").lower()
        if meta_writer in FORBIDDEN_WRITERS:
            result.fail("package.meta.json: запрещённый писатель")
        expect_writer = required_writer(slot)
        if meta_writer and meta_writer != expect_writer:
            result.fail(f"package.meta.json: written_by {meta_writer}, нужен {expect_writer}")
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
cover_md5: {result.cover_md5 or "n/a"}
cover_hook: {result.cover_hook or "n/a"}
incident_report: none

# Причины
{reasons}

# Чеклист
- [ ] 12:12/15:15: researcher → meaning → copywriter → cover-text? → gate
- [ ] 12:12 с 16.09: «Спроси у карт:» + 2–3 •; нет «Если выбираешь ход на сегодня»; нет мутного эссе
- [ ] 21:21: один writer → gate (meaning нет)
- [ ] Директор / Холл не писал inline
- [ ] written_by: {required_writer(result.slot) or "openai-api-gpt-5.6-sol"}
- [ ] Главред снят, фразы Главреда нет
- [ ] нет слова «ловушка»
- [ ] бот ≠ приложение
- [ ] 21:21: длина, нет «Сцена», нет пустой воды про «примерить», 4 карты с 15.09, позиция 3 = она, позиция 4 = совет
- [ ] cover anti-stale: новый кадр, уникальный md5, хук совпадает
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
    print(f"cover_md5={result.cover_md5}")
    print(f"cover_hook={result.cover_hook}")
    for reason in result.reasons:
        print(f"FAIL: {reason}")
    return 0 if result.verdict == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())

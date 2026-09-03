# Canon

## Модели (HARD)

Все роли, что пишут прозу, caption, сценарий, `montage.md` / `montage-ai.json` как текст, `questions.md` — **только Gemini 3.8 Flash High**:
- **Cloud Agent / launch:** model id `gemini-3.8-flash`, param `reasoning_effort: high`.
- **Локальный IDE Task:** alias `gemini-3.8-flash-high`.
- **Жёсткое правило (HARD 03.09):** Дефолтный Cloud Agent / Director НИКОГДА не подменяет текст, который по канону пишет Gemini (ни сценарии, ни caption, ни монтаж, ни вопросы). Если Gemini недоступна / Task не спавнится / slug неверный — только FAIL + явный отчёт «модель недоступна», без своего черновика. Лазейки «напишу сам» нет.

Директор передаёт `model` в Task явно. YAML роли без Task-модели перебивается окном Холла.

| Пишет текст | Модель |
| --- | --- |
| Gemini (`script-draft.md`) | `gemini-3.8-flash` + `reasoning_effort: high` (alias Task: `gemini-3.8-flash-high`) |
| Смыслы (`script.md`, `smysly.md`) | `gemini-3.8-flash` + `reasoning_effort: high` (alias Task: `gemini-3.8-flash-high`) |
| Funnel (`caption.md`) | `gemini-3.8-flash` + `reasoning_effort: high` (alias Task: `gemini-3.8-flash-high`) |
| Storyboard (`storyboard.md`) | `gemini-3.8-flash` + `reasoning_effort: high` (alias Task: `gemini-3.8-flash-high`) |
| Монтаж (`montage.md`, `montage-ai.json`) | `gemini-3.8-flash` + `reasoning_effort: high` (alias Task: `gemini-3.8-flash-high`) |
| Вопросы (`questions.md`) | `gemini-3.8-flash` + `reasoning_effort: high` (alias Task: `gemini-3.8-flash-high`) |

Не Gemini: Director / Extractor / Analyst / Filter / Gate (`inherit`); Kie / пиксели; Composio / публикация; Wordstat API.
Пиксели не генерировать. В Telegram не слать. Живые пакеты эфира не переписывать ради модели.

Политика: [`model-policy.json`](model-policy.json). Роли: [`agents/FOR-AGENTS.md`](agents/FOR-AGENTS.md).

## Funnel
- **Product:** In-app audio breakdown «Суть – Тень – Вектор» on the reel topic.
- **Closer:** Code word in comments → Direct → audio breakdown in the APP.
- **App vs Bot:** Do NOT mix bot and app. Do NOT sell the Telegram/Max bot's 3 free spreads.
- **Instagram URL Rule:** No raw URLs in Instagram captions. Links live in the profile header.
- **Core Value Proposition:** They buy access to the head of a person they cannot ask, not tarot.

## Red Zones
- Minors/under 21 sexual-romantic
- Abuse, rape, incest
- SVO/war
- Medical
- Suicide
- 13–17 targeting

## Montage (two artifacts)
- Role **Монтаж** writes two files per reel: `montage.md` (human) and `montage-ai.json` (Remotion). Schema: `MONTAGE-AI.md`.
- Every future reel pack MUST contain valid `montage-ai.json`. Gate FAIL if missing, invalid, or a beat lacks exact `card.text` / `startSec` / `endSec` / `line`.
- Hall does not write montage. Director does not write montage. Script, caption, questions stay with their owners.

## CTA wording (spoken + on-screen)
- «автоматически пришлю» → «СРАЗУ пришлю»
- «в нашем приложении» / «нашем приложении» → «в моём приложении»
- Sell the app audio «Суть – Тень – Вектор». Never «3 free bot readings».

## Tone & Style
- **No «Сцена»:** Never use the word «Сцена» in scripts, cards, or montage.
- **Voice:** Gemini's living spoken voice. No corporate speak.
- **Promises:** Do not promise to read minds.
- **Fear:** Do not scare with loneliness.
- **Hype:** Do not hype war or medicine.
- **Anonymity:** Anonymize real client names from the source in public-facing scripts.
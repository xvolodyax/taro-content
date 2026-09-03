# Рилсы — роли роя

Канон: [`../canon.md`](../canon.md).
Монтаж JSON: [`../MONTAGE-AI.md`](../MONTAGE-AI.md).
Модели: [`../model-policy.json`](../model-policy.json).

Не посты 12:12 / 15:15 / 21:21. Не Алёна. Не «Магия истории». Не Composio.

Одно окно: Директор только очередь. Один агент не пишет сценарий + caption + монтаж + вопросы.

| # | Роль | Файл | Модель | Пишет |
| --- | --- | --- | --- | --- |
| 0 | Директор | `1-director.md` | inherit | **нет** |
| 1 | Extractor | `2-extractor.md` | inherit | `knowledge/*` |
| 2 | Analyst | `3-analyst.md` | inherit | `knowledge/*` |
| 3 | Filter | `4-filter.md` | inherit | red zones |
| 4 | Gemini | `5-gemini.md` | `gemini-3.8-flash-high` | `script-draft.md` |
| 5 | Смыслы | `smysly.md` | `gemini-3.8-flash-high` | `script.md`, `smysly.md` |
| 6 | Funnel | `6-funnel.md` | `gemini-3.8-flash-high` | `caption.md`, `code-word.txt` |
| 7 | Storyboard | `7-storyboard.md` | `gemini-3.8-flash-high` | `storyboard.md` |
| 8 | Монтаж | `9-montage.md` | `gemini-3.8-flash-high` | `montage.md`, `montage-ai.json` |
| 9 | Вопросы | `10-questions.md` | `gemini-3.8-flash-high` | `questions.md` |
| 10 | Gate | `8-gate.md` | inherit | PASS/FAIL |

Текстовые Task: явно `model: gemini-3.8-flash-high`.
`written_by: gemini`. Opus / Sonnet / Composer / Grok = FAIL.
Не Gemini: Kie / пиксели, Composio / публикация, Wordstat API.
Живые пакеты эфира не переписывать ради модели.

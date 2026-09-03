# Магия истории — роли

Источник правды: [`magiya-istorii/.cursor/agents/FOR-AGENTS.md`](../magiya-istorii/.cursor/agents/FOR-AGENTS.md).
Канон: [`magiya-istorii/CANON.md`](../magiya-istorii/CANON.md).
Контракт: [`magiya-istorii/CONTRACT.md`](../magiya-istorii/CONTRACT.md).

Не посты «ТАРО СЕЙЧАС». Не 21:21. Не Excalibur-плагин. Не Каруселька.

| Текст | Хозяин | Модель (Cloud / Local Task alias) |
| --- | --- | --- |
| Тело `story.md` | Writer, один проход | `gemini-3.8-flash` + `reasoning_effort: high` (alias Task: `gemini-3.8-flash-high`) |
| H1 == title | Title | `gemini-3.8-flash` + `reasoning_effort: high` (alias Task: `gemini-3.8-flash-high`) |
| Overlay обложки | Clickbait | `gemini-3.8-flash` + `reasoning_effort: high` (alias Task: `gemini-3.8-flash-high`) |
| Один кадр 16:9 | Art (реф Виктория.png, микрофон в руке, жирная красная рамка + кликбейт; не шесть картинок) | `gemini-3.8-flash` + `reasoning_effort: high` (alias Task: `gemini-3.8-flash-high`) |

Plot — необязательные заметки, в статью не пишет.
Gate — только проверка, предложения не переписывает.
Фиксера / копирайтера / enrichment по телу нет.
Директор будит роли и сам не пишет.
Если Task с текстовой ролью недоступен — Директор текст сам НЕ пишет (fallback на `gemini-3.8-flash`+high либо FAIL).

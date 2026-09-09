# Магия истории — роли

Источник правды: [`magiya-istorii/.cursor/agents/FOR-AGENTS.md`](../magiya-istorii/.cursor/agents/FOR-AGENTS.md).
Канон: [`magiya-istorii/CANON.md`](../magiya-istorii/CANON.md).
Контракт: [`magiya-istorii/CONTRACT.md`](../magiya-istorii/CONTRACT.md).

Не посты «ТАРО СЕЙЧАС». Не 21:21. Не Excalibur-плагин. Не Каруселька.

| Текст | Хозяин | Модель (Cloud / Local Task alias) | Правило дефолта |
| --- | --- | --- | --- |
| Тело `story.md` | Writer, один проход | `gemini-3.8-flash` + `reasoning_effort: high` (alias Task: `gemini-3.8-flash-high`) | Дефолт не пишет: FAIL if unavailable |
| H1 == title | Title | `gemini-3.8-flash` + `reasoning_effort: high` (alias Task: `gemini-3.8-flash-high`) | Дефолт не пишет: FAIL if unavailable |
| Overlay обложки | Clickbait | `gemini-3.8-flash` + `reasoning_effort: high` (alias Task: `gemini-3.8-flash-high`) | Дефолт не пишет: FAIL if unavailable |
| Холст 2K 2×2 | Art (cover: Вика + mic + красная рамка + кликбейт; inline-01…03 без лица; не четыре 1K) | `gemini-3.8-flash` + `reasoning_effort: high` (alias Task: `gemini-3.8-flash-high`) | Текст оверлея только из clickbait.txt |

Plot — необязательные заметки, в статью не пишет.
Gate — только проверка, предложения не переписывает.
Фиксера / копирайтера / enrichment по телу нет.
Директор будит роли и сам не пишет.
Дефолтный Cloud Agent / Director НИКОГДА не подменяет текст Gemini (ни статьи, ни посты, ни опрос, ни Алёна, ни рилсы). Если модель недоступна — только FAIL («модель недоступна»), без своего черновика.

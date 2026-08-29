# Магия истории — роли

Канон: [`../../CANON.md`](../../CANON.md).
Контракт: [`../../CONTRACT.md`](../../CONTRACT.md).

Не посты «ТАРО СЕЙЧАС». Не Алёна. Не 12:12 / 15:15 / 21:21.
Не Дзен-боль. Не продажа раскладов. Не Composio.

Одно окно: Директор ведёт цепочку. Специалист — один шаг.
Директор сам scout / plot / title / story / clickbait / GATE / art **не пишет**.

| # | Роль | Файл | Модель | Task? |
| --- | --- | --- | --- | --- |
| 0 | Директор | `magiya-director.md` | `inherit` | **нет** |
| 1 | Scout / Wordstat | `magiya-scout.md` | `inherit` | да |
| 2 | Plot | `magiya-plot.md` | `inherit` | да |
| 3 | Title (H1==title, Эскалибур) | `magiya-title.md` | `gemini-3.7-flash-high` | да |
| 4 | Writer | `magiya-writer.md` | `gemini-3.7-flash-high` | да |
| 5 | Gate (текст) | `magiya-gate.md` | `inherit` | да |
| 6 | Clickbait (только кадр 1) | `clickbait.md` | `gemini-3.7-flash-high` | да, после Plot |
| 7 | Art (только текст art-brief) | `magiya-art.md` | `gemini-3.7-flash-high` | да, после Clickbait |

Все текстовые роли (Title, Writer, Clickbait, Art-brief) — строго `gemini-3.7-flash-high`.
Title ≠ Clickbait. Clickbait не меняет `title`/`h1`.
Art: холст 2×3, Вика держит DJI Mic Mini в руке у рта, на кадр 1 жирная красная рамка + `clickbait.txt` (display), кадры 2–6 — тезисы действия сюжета.
Свет и место — по сюжету (в базовый промпт «ночь» не зашивать).
Холст не валит текст. Лицо Холл не рисует. Публикации нет.

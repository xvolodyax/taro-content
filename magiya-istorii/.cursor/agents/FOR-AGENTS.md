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
Директор передаёт эту модель в Task явно (шаблоны `templates/steps/03-title.json`, `04-writer.json`, `06-clickbait.json`, `07-art.json`).
Title ≠ Clickbait. Clickbait не меняет `title`/`h1`.
Art: одно полотно, одна генерация; на кадр 1 только `clickbait.txt`. Пиксели не запускать.
Холст не валит текст. Director не говорит «ещё раз нарисуй».
Срезы 2–6 — врезки в статью. Лицо Холл не рисует. Публикации нет.

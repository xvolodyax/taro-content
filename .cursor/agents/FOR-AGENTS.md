# Посты каналов — роли

Канон: [`POSTS.md`](../../POSTS.md).
Не Excalibur-плагин. Не статьи Дзена. Не рилсы.

Одно окно: Директор ведёт цепочку. Специалист — один шаг, не зовёт соседние роли.

| # | Роль | Файл | Модель | Task? |
| --- | --- | --- | --- | --- |
| 0 | Директор | `posts-director.md` | inherit | **нет** |
| 1 | Scout / Wordstat или луна | `posts-scout.md` | inherit | да, foreground |
| 2 | Writer (смысл) | `posts-writer.md` | `gemini-3.7-flash-high` | да |
| 3 | Sol (слог / письмо Алёны) | `posts-sol.md` | `gemini-3.7-flash-high` | да |
| 4 | Gate | `posts-gate.md` | `gemini-3.7-flash-high` | да |
| 5 | Cover (хук + prompt) | `posts-cover-text.md` | `gemini-3.7-flash-high` | да, только 12:12 и 21:21 |

Cover читает весь `writer.md` и финальный текст слота. Хук 2–6 слов **по центру** 1:1, чтобы читался как превью сетки Instagram (~200px). Пиксели и Kie — Холл. Ролей `posts-cover-hook` / `posts-cover-render` нет.
Слот **`alena-0700`**: те же 0–4, Cover нет. `posts-cover-text` не звать и не править. Нового Директора нет.

Нет ролей: Publish, Research-статья, Title, Schema, Indexer, Setup, Главред снаружи, отдельный Cover-директор, `posts-director-alena`.

Статьи Дзена, `video/`, `images/prompts/` старого плейбука, однофайловые посты на других ветках — **чужая машина**. Не открывать, не «дотягивать».

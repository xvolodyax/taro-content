# Посты каналов — роли роя

Канон: [`POSTS.md`](../../POSTS.md).
Не Excalibur-плагин. Не статьи Дзена. Не рилсы. Не Каруселька-контент.

Одно окно: Директор только оркестрирует. Один агент не делает тему + тезис + пост + хук.

| # | Роль | Файл | Модель | Спавн |
| --- | --- | --- | --- | --- |
| 0 | Директор | `posts-director.md` | inherit | **нет** (чат Холла) |
| 1 | researcher | `posts-researcher.md` | inherit | Plugin `Task(posts-researcher)`; Cloud `Task(generalPurpose)` + dispatch |
| 2 | meaning | `posts-meaning.md` | `gemini-3.7-flash-high` | Plugin `Task(posts-meaning)`; Cloud `generalPurpose` |
| 3 | copywriter | `posts-copywriter.md` | `gemini-3.7-flash-high` | Plugin `Task(posts-copywriter)`; Cloud `generalPurpose` |
| 4 | cover-text | `posts-cover-text.md` | `gemini-3.7-flash-high` | 12:12 и 21:21; 15:15 нет |
| 5 | gate | `posts-gate.md` | `gemini-3.7-flash-high` | после текстов; inline Директора = FAIL |

Алиасы (не новые роли): `posts-scout` → researcher, `posts-writer` → meaning, `posts-sol` → copywriter.

Cover читает `meaning.md` + финальный текст. 3 хука, один выбран, центр 1:1, превью сетки (~200px). Пиксели и Kie — Холл.

**Снято:** Главред, «можно публиковать» от Главреда.
**21:21:** рубрика «Другая сторона экрана». Meaning изобретает 3 вопроса из заявки 15:15.
Не 4 совета на варианты. Холл текст не пишет.

**Publish:** у писателей SKIP. После PASS Директор вызывает `scripts/posts_publish.py`.
Холл не публикует. Ключ только `COMPOSIO_API_KEY`. Нет ключа — SKIP.
`preview: poll-only` — публикацию не звать. `evening: HOLD` — без 21:21; опрос 15:15 в слот можно.

Нет ролей: Publish-агент, 13-й «флафф», `posts-cover-hook`, Setup, Schema, Indexer.

Статьи Дзена, `video/`, чужие пакеты — не открывать.

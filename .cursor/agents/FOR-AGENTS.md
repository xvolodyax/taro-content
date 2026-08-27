# Посты каналов — роли роя

Канон: [`POSTS.md`](../../POSTS.md). Контракт роя: [`shared/posts-swarm.md`](../../shared/posts-swarm.md).
Не Excalibur-плагин. Не статьи Дзена. Не рилсы. Не Каруселька целиком.

Одно окно: Директор ведёт цепочку. Сотрудник — один шаг, не зовёт соседние роли.
Cloud: нет `Task(posts-*)`. Директор зовёт `Task(generalPurpose)` с промптом файла роли.

| # | Роль | Файл | Модель | Task? |
| --- | --- | --- | --- | --- |
| 0 | Директор | `posts-director.md` | inherit | **нет** |
| 1 | researcher | `posts-researcher.md` | `gemini-3.7-flash-high` | да, foreground / generalPurpose |
| 2 | meaning | `posts-meaning.md` | `gemini-3.7-flash-high` | да |
| 3 | copywriter | `posts-copywriter.md` | `gemini-3.7-flash-high` | да |
| 4 | cover-text | `posts-cover-text.md` | `gemini-3.7-flash-high` | да, только 12:12 и 21:21 |
| 5 | gate | `posts-gate.md` | `gemini-3.7-flash-high` | да |

Cover читает смысл и пишет **только хуки** + `image-prompt.txt`. Хук 2–6 слов **по центру** 1:1. Пиксели и Kie — Холл.

## Запрещённые роли

Главред, `posts-glavred`, Scout, Writer, Sol, Publish, `posts-cover-hook`, `posts-cover-render`.
Штамп «можно публиковать» не требуется. Качество внутри researcher + meaning + Gemini + gate.

Статьи Дзена, `video/`, однофайловые посты на других ветках — чужая машина.

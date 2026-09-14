# Dispatch-prompt — Cloud Task(generalPurpose)

Директор в Cloud **не** пишет роль сам. На каждый шаг:

1. Собрать промпт: `python3 scripts/posts_dispatch_prompt.py --role ROLE --package DIR --runtime cloud`
2. Сохранить в `steps/NN-ROLE.prompt.md`
3. Вызвать **один** `Task(generalPurpose)` с этим промптом
4. Записать `steps/NN-ROLE.json` (`inline: false`, `spawn: Task`)

В Plugin этот файл не нужен: зови `Task(posts-ROLE)`.

## Что обязательно внутри промпта

- путь агента: `.cursor/agents/posts-<role>.md`
- путь skill: `.cursor/skills/posts-<role>/SKILL.md`
- канон: `POSTS.md`, `shared/posts-soul.md`, `shared/posts-funnel.md`
- researcher ещё: `POSTS_SCOUT_CANON.md` (широкая ниша + анти-монотонность 7 дней; Холл угол не назначает)
- путь пакета и слот
- что уже готово
- что **не** делать (соседние роли, публикация, картинка, Главред)
- `written_by: openai-api-gpt-5.6-sol` на человеческий текст слота
- текст: `python3 scripts/chat_completions.py --model gpt-5.6-sol` (`docs/POSTS_TEXT_MODEL.md`)
- `gpt-5.5` запрещён
- `publish: SKIP`
- Task inherit; `reasoning_effort=low` (high — только оверрайд Владимира)
- дефолтный агент / Director текст не пишет

Директор не дописывает в промпт готовый пост «для правки». Это снова inline.

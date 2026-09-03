# Step records — доказательство роя

Директор **не** пишет тему, тезис, пост и хук. Каждый шаг — отдельный `Task`.
Inline Директора = `GATE` FAIL.

## Где лежат

```text
posts/<slot>/steps/01-researcher.json
posts/<slot>/steps/01-researcher.prompt.md   # cloud: полный dispatch-prompt
posts/<slot>/steps/02-meaning.json            # нет на 21:21
posts/<slot>/steps/03-copywriter.json
posts/<slot>/steps/04-cover-text.json         # нет на 15:15; на 21:21 после поста
posts/<slot>/steps/05-gate.json
posts/<slot>/package.meta.json
```

Номер = порядок в слоте, не глобальный id. Имя файла = канон роли
(`researcher` / `meaning` / `copywriter` / `cover-text` / `gate`).

## JSON шага

```json
{
  "role": "posts-researcher",
  "spawn": "Task",
  "subagent_type": "posts-researcher",
  "model": "inherit",
  "inline": false,
  "written_by": "inherit",
  "dispatch_prompt": "steps/01-researcher.prompt.md",
  "artifacts": ["brief.md"],
  "publish": "SKIP"
}
```

| Поле | Правило |
| --- | --- |
| `spawn` | только `Task` |
| `inline` | только `false`. `true` или отсутствие шага при живом артефакте = FAIL |
| `subagent_type` | Plugin: `posts-<role>`. Cloud: `generalPurpose` |
| `dispatch_prompt` | Cloud обязателен: файл с полным промптом из `scripts/posts_dispatch_prompt.py` |
| `model` | meaning / copywriter / cover-text / gate → `gemini-3.8-flash-high` |
| `written_by` | человеческий текст → `gemini`. Opus / Sonnet / Composer = FAIL |
| `publish` | у писателей всегда `SKIP`. Эфир после PASS — `scripts/posts_publish.py` у Директора |

## Cloud vs plugin

**Cloud (окно Холла):** один `Task(generalPurpose)` на шаг. В prompt — вывод
`python3 scripts/posts_dispatch_prompt.py --role <role> --package <dir> --runtime cloud`.
Кастомный `Task(posts-*)` в Cloud часто недоступен. Не писать шаг в чате Директора.

**Plugin:** `Task(posts-researcher)` / `Task(posts-meaning)` / `Task(posts-copywriter)` /
`Task(posts-cover-text)` / `Task(posts-gate)`. Промпт короткий: путь пакета, слот, что не делать.

## Когда Gate режет

- нет `steps/` у нового пакета, а тексты уже есть
- шаг с `inline: true` или `spawn` ≠ `Task`
- Cloud-шаг без файла dispatch-prompt
- dispatch-prompt не содержит путь агента роли
- `written_by` из стоп-листа моделей
- есть шаг / файл Главреда, или фраза «можно публиковать» от Главреда
- `publish` у шага писателя не `SKIP`

Алиасы старых имён в step record принимаются: `posts-scout` → researcher,
`posts-writer` → meaning, `posts-sol` → copywriter.

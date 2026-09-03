---
name: posts-director
description: Оркестратор роя постов. Не пишет тему, тезис, пост, хук. После PASS публикует скриптом.
---

# Director

12:12 / 15:15: researcher → meaning → copywriter → cover-text? → gate → publish.
21:21: researcher? → draw_rw_cards.py → ОДИН writer (Gemini 3.8 Flash High) → gate.

Cloud: один `Task(generalPurpose)` на шаг, промпт из
`scripts/posts_dispatch_prompt.py`. Текстовые шаги: Cloud id `gemini-3.8-flash` + `reasoning_effort=high` (alias IDE Task: `gemini-3.8-flash-high`).
Если Gemini недоступна / Task не спавнится / slug неверный — только FAIL («модель недоступна»), без своего черновика! Director текст сам НЕ подменяет.
Plugin: `Task(posts-*)`.

После шага: `scripts/posts_step_record.py`. Потом stamp + gate.
После `GATE` = PASS: `python3 scripts/posts_publish.py --package DIR`.
Ключ только `COMPOSIO_API_KEY`. Нет ключа — SKIP, не падать.
Холл не публикует и не пишет посты. Сегодняшние эфиры не переписывать.

---
name: posts-director
description: Оркестратор роя постов. Не пишет тему, тезис, пост, хук. После PASS публикует скриптом.
---

# Director

12:12 / 15:15: researcher → meaning → copywriter → cover-text? → gate → publish.
21:21: researcher? (тема дня) → draw_rw_cards.py → ОДИН writer (вопрос + расклад, Gemini 3.8 Flash High) → gate. Пульс снят.

Cloud: один `Task(generalPurpose)` на шаг, промпт из
`scripts/posts_dispatch_prompt.py`. Текстовые шаги: `gemini-3.8-flash-high`.
Plugin: `Task(posts-*)`.

После шага: `scripts/posts_step_record.py`. Потом stamp + gate.
После `GATE` = PASS: `python3 scripts/posts_publish.py --package DIR`.
Ключ только `COMPOSIO_API_KEY`. Нет ключа — SKIP, не падать.
Холл не публикует и не пишет посты. Сегодняшние эфиры не переписывать.

# Старт дня постов

Не писать сегодняшний уже вышедший слот. Холл не публикует.

1. Одно окно в `taro-content`. Главный агент = `posts-director`.
2. Env: `COMPOSIO_API_KEY` (значение в чат не писать). Нет ключа — слот SKIP, не падать.
3. Вставить промпт слота из `POSTS.md`.
4. Cloud: Директор на каждый шаг делает `Task(generalPurpose)` + dispatch-prompt.
   Plugin: `Task(posts-*)`.
5. Дождаться `GATE` = PASS. Директор сам:
   `python3 scripts/posts_publish.py --package DIR`
6. Кадр: публичный HTTPS в `POST_IMAGE_URL` / `cover-url.txt`. Без URL фото-площадки SKIP.

Алиасы: `telegram-composia`, `instagram-ru`.
12:12: ВК и YouTube не трогать. 21:21: TG рой; ВК/YouTube — Холл/браузер, если нет ключа.
21:21 = один вопрос + один расклад. Пульс снят. Холл не пишет.
`preview: poll-only` — не публиковать.
Главред не звать. PASS + скрипт публикации.

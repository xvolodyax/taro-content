# Слот alena-0700

Узкий слот в **той же** машине постов. Директор тот же: `posts-director`.
Нового роя и второго Директора нет.

Канал: https://t.me/AlenaSafonova_queen  
Не `@TodayTaro`. Не ТАРО СЕЙЧАС.

Эфир **07:00 МСК**. После `GATE` = PASS Директор кладёт сам:

```text
python3 scripts/posts_publish.py --package posts/YYYY-MM-DD-alena
```

Алиас `telegram-composia`, chat `@AlenaSafonova_queen`. Без отложки.
Раньше 07:00 не слать. Слот прошёл — сразу. Холл не публикует.

Рефки святые, слова и URL не менять: [`shared/alena-funnel.md`](../shared/alena-funnel.md).
Нет ключа `COMPOSIO_API_KEY` — SKIP, не падать.
Картинка: публичный URL в `ALENA_COVER_URL` / `cover-url.txt`. Готовый файл у Холла
`/workspace/alena-covers/prognoz-na-den.png` сам в Telegram не уедет.

Пакет: `posts/YYYY-MM-DD-alena/` (`caption.txt` / `caption.html`, `GATE`).
Cover и `posts-cover-text` не звать. ВК и YouTube не трогать.

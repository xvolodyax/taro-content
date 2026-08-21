---
name: dzen-publish
description: "Чеклист публикации статьи Дзена для Холла. Не WordPress. Не публиковать без «можно публиковать»."
model: inherit
readonly: false
is_background: false
---

**Язык:** русский. Канон: `articles/ARTICLE.md` §8–9. Ошибки: `articles/pipeline-errors.md`.

## Жёстко

Ты не публикуешь сам, если ты не Холл в браузере. Агент готовит чеклист и пакет файлов.

Без отмашки «можно публиковать» — стоп.

## Пакет Холлу

- канал: `todaytaro_bot`
- формат: **Статья**, не пост
- `article.md` (status `approved`)
- `dzen-description.md` (карточка)
- `cover-brief.md` + **файл** обложки с диска
- воронка Макс и/или ВК уже в тексте гиперссылками
- без хештегов, без Telegram

Не использовать: WordPress, SFTP, RSS, `localhost` / `127.0.0.1`, URL `/new-publication`.

После реальной выкладки — строка в `articles/published-titles.md`, status `published`.

```text
=== DZEN PUBLISH CHECKLIST ===
approved: yes | no
cover_file: path | MISSING
localhost: no
incident_report: none | articles/pipeline-errors.md#INC-…
```

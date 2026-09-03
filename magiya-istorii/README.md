# Магия истории

Отдельный продукт в `taro-content`. Захватывающие истории про магию, чёрную магию, обряды, духов, колоды, проклятия.

Это **не** посты «ТАРО СЕЙЧАС», не Алёна, не слоты 12:12 / 15:15 / 21:21, не `PUBLISH.md`, не Composio.
Не канал боли и не продажа раскладов.

Канон: [`CANON.md`](CANON.md).  
Контракт: [`CONTRACT.md`](CONTRACT.md).  
Роли: [`.cursor/agents/FOR-AGENTS.md`](.cursor/agents/FOR-AGENTS.md).

## Как запустить Director

1. Одно окно Cloud Agent в `taro-content`.
2. Главный агент — **`magiya-director`**. Не `Task(magiya-director)`. Не `/in-cloud`.
3. Промпт:

```text
Собери пакет «Магия истории» на YYYY-MM-DD.
Канон: magiya-istorii/CANON.md. Контракт: magiya-istorii/CONTRACT.md.
Director сам тексты не пишет.
Текстовые роли (H1, тело, overlay, art): Cloud model gemini-3.8-flash + reasoning_effort=high (alias IDE Task: gemini-3.8-flash-high).
Дефолт не пишет в эфир ничего: ни H1, ни кликбейт, ни тело. Если Task недоступен — только FAIL.
Тело — только Writer (один проход). H1 — только Title. Overlay — только Clickbait.
Plot — необязательные заметки, биты в Writer не вшивать.
Scout → Plot → Title(только H1) → Writer(только тело) → Gate(только проверка).
Clickbait (только overlay кадра 1) после Plot, не в title/h1/тело.
Art: один кадр 16:9. Реф Виктория.png, микрофон DJI в руке у рта, жирная красная рамка + clickbait.txt на этой же картинке.
Не шесть кадров, не холст, не нарезка. В тело ту же картинку не ставить.
Свет и локацию Art берет из сюжета, в базовое ядро промпта «ночь» не зашивать.
Одна генерация обложки. Картинка не валит текст. Лицо Холл не рисует. Живые истории не перерисовывать.
Посты ТАРО СЕЙЧАС, Алёну, 12:12/15:15/21:21, PUBLISH.md, Composio не трогать.
После PASS: путь, GATE, h1, overlay, art.
```

## Цепочка

```text
Scout → Plot(заметки) → Title(H1) → Writer(тело) → Gate(проверка)
Clickbait ∥ после Plot (не в тело, не в H1)
Art после Clickbait (обложка 16:9 1K, готовая строка)
Publisher: только если Холл сказал публиковать
```

| Шаг | Агент / Скрипт | Выход |
| --- | --- | --- |
| 1 | `magiya-scout` | `scout.md` |
| 2 | `magiya-plot` | `plot.md` (необязательные заметки) |
| 3 | `magiya-title` | только H1; тело не трогает |
| 4 | `magiya-writer` | только тело `story.md` |
| 5 | `magiya-gate` | `GATE` (проверка, не рерайт) |
| 6 | `clickbait` | `clickbait.txt`, `meta.overlay_clickbait` |
| 7 | `magiya-art` | `art-brief.md`, `cover.png` (16:9 1K) |
| 8 | `magiya_site_publish.py` | upload, approve, publish на сайт |

Title ≠ Clickbait. Кликбейт не в H1, не в URL.
Публикация: при наличии `SITE_PUBLISH_TOKEN` рой сам заливает историю на сайт. Холл не публикует.

## Wordstat

```text
python3 magiya-istorii/scripts/wordstat.py "чёрная магия" "обряд на пороге" "проклятие"
```

Env: `YANDEX_CLOUD_SEARCH_API_KEY` + `YANDEX_FOLDER_ID`. Ключ не в лог. PARTIAL не стоп.

Нарезка холста **не используется**. Один кадр `cover.png` 16:9. `slice_canvas.py` — хвост старого канона шести кадров.

## Демо

`packages/2026-08-29-pack/` — `story.md` + `meta.json` (`title`/`h1` отдельно от `overlay_clickbait`) + `caption-01`…`06`. В эфир не выкладывать.

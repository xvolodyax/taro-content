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
Director сам тексты не пишет:
Scout → Plot → Title(H1==title, Эскалибур) → Writer → Gate(текст).
Clickbait (только overlay кадра 1) после Plot, не в title/h1.
Art: холст 6 клеток (2×3), глянец 2020-х. Вика держит DJI Mic Mini в руке у рта.
Кадр 1 — жирная красная рамка + clickbait.txt (display-шрифт). Кадры 2–6 — тезисы действия сюжета.
Свет и локацию Art берет из сюжета, в базовое ядро промпта «ночь» не зашивать.
Одна генерация холста. Холст не валит текст. Лицо Холл не рисует. Не публиковать.
Посты ТАРО СЕЙЧАС, Алёну, 12:12/15:15/21:21, PUBLISH.md, Composio не трогать.
После PASS: путь, GATE, h1, overlay, art.
```

## Цепочка

```text
Scout → Plot → Title → Writer → Gate
Clickbait ∥ после Plot
Art после Clickbait (холст 2×3)
Publisher: magiya_site_publish.py -> сайт (при наличии ключа)
```

| Шаг | Агент / Скрипт | Выход |
| --- | --- | --- |
| 1 | `magiya-scout` | `scout.md` |
| 2 | `magiya-plot` | `plot.md` |
| 3 | `magiya-title` | `title-brief.md`, `meta.title`=`meta.h1` |
| 4 | `magiya-writer` | `story.md` |
| 5 | `magiya-gate` | `GATE` |
| 6 | `clickbait` | `clickbait.txt`, `meta.overlay_clickbait` |
| 7 | `magiya-art` | `art-brief.md`, `canvas.png`, `slice-01..06.png` |
| 8 | `magiya_site_publish.py` | upload, approve, publish на сайт |

Title ≠ Clickbait. Кликбейт не в H1, не в URL.
Публикация: при наличии `SITE_PUBLISH_TOKEN` рой сам заливает историю на сайт. Холл не публикует.

## Wordstat

```text
python3 magiya-istorii/scripts/wordstat.py "чёрная магия" "обряд на пороге" "проклятие"
```

Env: `YANDEX_CLOUD_SEARCH_API_KEY` + `YANDEX_FOLDER_ID`. Ключ не в лог. PARTIAL не стоп.

Нарезка холста (когда появится `canvas.png`):

```text
python3 magiya-istorii/scripts/slice_canvas.py canvas.png --out .
```

## Демо

`packages/2026-08-29-pack/` — `story.md` + `meta.json` (`title`/`h1` отдельно от `overlay_clickbait`) + `caption-01`…`06`. В эфир не выкладывать.

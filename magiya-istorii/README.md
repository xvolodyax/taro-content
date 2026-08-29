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
Art: одно полотно, одна сцена (одежда/место/свет не менять). Холст 6, глянец 2020-х.
Кадр 1 — только clickbait.txt + журнальная красная рамка (обложка). Кадры 2–6 — врезки в статью, не карусель.
Одна генерация холста. Не «ещё раз нарисуй». Холст не валит текст.
Лицо Холл не рисует. Не публиковать.
Посты ТАРО СЕЙЧАС, Алёну, 12:12/15:15/21:21, PUBLISH.md, Composio не трогать.
После PASS: путь, GATE, h1, overlay, art.
```

## Цепочка

```text
Scout → Plot → Title → Writer → Gate
Clickbait ∥ после Plot
Art после Clickbait (холст 2×3)
```

| Шаг | Агент | Выход |
| --- | --- | --- |
| 1 | `magiya-scout` | `scout.md` |
| 2 | `magiya-plot` | `plot.md` |
| 3 | `magiya-title` | `title-brief.md`, `meta.title`=`meta.h1` |
| 4 | `magiya-writer` | `story.md` |
| 5 | `magiya-gate` | `GATE` |
| 6 | `clickbait` | `clickbait.txt`, `meta.overlay_clickbait` |
| 7 | `magiya-art` | `art-brief.md` |

Title ≠ Clickbait. Кликбейт не в H1, не в URL. Пиксели не обязательны.

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

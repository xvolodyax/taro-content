# Контракт пакета «Магия истории»

Пакет = одна история. Папка:

```text
magiya-istorii/packages/YYYY-MM-DD-slug/
```

`slug` — из **title/H1** (Эскалибур), не из кликбейта, не жирнейшая фраза Вордстата.

## Файлы (обязательные)

| Файл | Кто | Зачем |
| --- | --- | --- |
| `scout.md` | Scout | Живой спрос, угол ≠ топ H1 |
| `plot.md` | Plot | Кто / где / когда / ставка / цена |
| `title-brief.md` | Title | H1 == title, Эскалибур |
| `story.md` | Writer | Повесть 8–14 тыс. |
| `clickbait.txt` | Clickbait | Overlay кадра 1, одна строка |
| `meta.json` | Title + Writer + Clickbait (свои поля) | `title`/`h1` ≠ `overlay_clickbait` |
| `GATE` | Gate | PASS или FAIL |
| `art-brief.md` | Art | Холст 2×3, кадр 1 только текст Clickbait |
| `package.meta.json` | Director | publish=SKIP, pixels=skip |
| `steps/0N-ROLE.json` | Director | шаг не inline |

После пикселей (не обязательны, лицо Холл не рисует): `canvas.png`, `slice-01.png`…`slice-06.png`.
Одно полотно, одна сцена. Срезы **в статью**: `01` обложка, `02–06` врезки. Не карусель. В теле не дублировать обложку.

Шаблоны: [`templates/`](templates/).

## `meta.json`

```json
{
  "product": "magiya-istorii",
  "kind": "fiction",
  "title": "",
  "h1": "",
  "overlay_clickbait": "",
  "clickbait_red_frame": true,
  "slug": "",
  "person": "",
  "city": "",
  "story_date": "",
  "ritual": "",
  "stake": "",
  "price": "",
  "wordstat_status": "OK | PARTIAL",
  "angle": "",
  "fattest_query_not_in_h1": true,
  "h1_equals_title": true,
  "overlay_not_in_title": true,
  "chars": 0,
  "living_people": "none",
  "publish": "SKIP"
}
```

Правила полей:

- `title` == `h1` (Эскалибур). Clickbait эти поля не пишет.
- `overlay_clickbait` — только кадр 1. Не копировать в `title` / `h1` / slug.
- `kind: document` — только если есть открытый источник и живых не оговариваем.

## Swarm

Директор **не** пишет scout / plot / title / story / clickbait / GATE / art-brief.
Каждый шаг — отдельный `Task`. Cloud: `Task(generalPurpose)` + файл роли.
Inline Директора = FAIL.

```text
Scout → Plot → Title → Writer → Gate(текст)
Clickbait: после Plot (можно параллельно с Writer / Gate)
Art: после Clickbait; на кадр 1 кладёт ТОЛЬКО clickbait.txt
```

FAIL Gate → только проза. Холст текст не валит. Вернуть дырявый текстовый шаг, не чинить самому.
**Одна генерация холста.** Director не говорит «ещё раз нарисуй». Art не fail'ит Writer.
Пиксели не обязательны. Лицо Холл не рисует. Публикации нет. `publish` всегда `SKIP`.

## Чужое

Не открывать и не писать: `posts/`, слоты 12:12 / 15:15 / 21:21, Алёна, `PUBLISH.md`, Composio, Дзен-боль.

## Выход Директора Холлу

```text
=== MAGIYA DIRECTOR ===
package: magiya-istorii/packages/YYYY-MM-DD-slug
gate: PASS | FAIL
chars: <n>
kind: fiction | document
h1: <Эскалибур>
overlay: <кадр 1>
art: art-brief.md (canvas 2x3)
publish: SKIP
next: Hall | return <role>
incident_report: none
```

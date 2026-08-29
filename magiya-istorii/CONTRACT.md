# Контракт пакета «Магия истории»

Пакет = одна история. Папка:

```text
magiya-istorii/packages/YYYY-MM-DD-slug/
```

`slug` — короткий угол, не жирнейшая фраза Вордстата. Латиница, дефисы.

## Файлы (обязательные)

| Файл | Кто | Зачем |
| --- | --- | --- |
| `scout.md` | Scout | Живой спрос, угол ≠ топ H1 |
| `plot.md` | Plot | Кто / где / когда / ставка / цена |
| `story.md` | Writer | Повесть 8–14 тыс. знаков |
| `meta.json` | Writer кладёт черновик, Gate сверяет | Выдумка vs документ, факты пакета |
| `GATE` | Gate | PASS или FAIL |
| `art-brief.md` | Art | Один кадр, без пикселей |
| `package.meta.json` | Director | Кто писал, publish=SKIP |
| `steps/0N-ROLE.json` | Director | Доказательство, что шаг не inline |

Шаблоны: [`templates/`](templates/).

## `meta.json`

```json
{
  "product": "magiya-istorii",
  "kind": "fiction | document",
  "title": "",
  "slug": "",
  "person": "",
  "city": "",
  "story_date": "YYYY-MM-DD или год+ночь словами",
  "ritual": "",
  "stake": "",
  "price": "",
  "wordstat_status": "OK | PARTIAL",
  "angle": "",
  "fattest_query_not_in_h1": true,
  "chars": 0,
  "living_people": "none",
  "publish": "SKIP"
}
```

`kind: document` — только если есть опора на открытый источник и живых не оговариваем.
Иначе `fiction`. В тексте истории ярлык не произносить.

## Swarm

Директор **не** пишет scout / plot / story / GATE / art-brief в своём чате.
Каждый шаг — отдельный `Task`. Cloud: `Task(generalPurpose)` + файл агента роли.
Inline Директора = FAIL.

```text
Scout → Plot → Writer → Gate → Art
```

Параллели нет. FAIL Gate → вернуть дырявый шаг, не чинить самому.
Пиксели не обязательны. Публикации нет. `publish` всегда `SKIP`.

## Чужое

Не открывать и не писать:

- `posts/`, слоты 12:12 / 15:15 / 21:21, Алёна
- `posts/PUBLISH.md`, Composio, `scripts/posts_*.py`
- статьи Дзена, рилсы, воронку бота

## Выход Директора Холлу

```text
=== MAGIYA DIRECTOR ===
package: magiya-istorii/packages/YYYY-MM-DD-slug
gate: PASS | FAIL
chars: <n>
kind: fiction | document
angle: <угол, не жирная фраза>
art: art-brief.md
publish: SKIP
next: Hall | return <role>
incident_report: none
```

# Контракт пакета «Магия истории»

Пакет = одна история. Папка:

```text
magiya-istorii/packages/YYYY-MM-DD-slug/
```

`slug` — из **title/H1** (Эскалибур), не из кликбейта, не жирнейшая фраза Вордстата.

## Публикация на сайт (Эскалибур-пайплайн)

После того как `GATE` = PASS и сформированы `slice-01.png`…`slice-06.png`, Director запускает скрипт публикации `scripts/magiya_site_publish.py`. `publish` больше не всегда SKIP.
Холл руками ничего не upload, не approve и не publish — всё делает рой.

- Секрет: `SITE_PUBLISH_TOKEN` (также проверяются `HALL_PUBLISH_TOKEN`, `PUBLISH_TOKEN`, `TARO_SITE_TOKEN`).
- Токены **никогда не писать** в git, логи, чат или json-файлы.
- Если токена в окружении нет — скрипт выставляет `GATE` = PASS и `publish: SKIP` с причиной `нет ключа`, пайплайн не падает.
- Дзен Студию не открывать — сайт сам отдаёт RSS из `/blog/rss.xml`.
- Никаких воронок ТАРО: нет бота, нет приложения, нет «3 бесплатных расклада», нет кодовых слов.

## Файлы пакета

| Файл | Кто | Зачем |
| --- | --- | --- |
| `scout.md` | Scout | Живой спрос, угол ≠ топ H1 |
| `plot.md` | Plot | Кто / где / когда / ставка / цена |
| `title-brief.md` | Title | H1 == title, Эскалибур |
| `story.md` | Writer | Быстрая история с триггерным вопросом в конце |
| `article.html` | Director / Publisher | Чистый HTML из `story.md` + H1 + врезки `slice-02`…`06` |
| `article.meta.json` | Director / Publisher | Метаданные для загрузки на сайт |
| `description-brief.json` | Director / Publisher | Описание/excerpt (не дубль первого абзаца) |
| `caption-01.txt` … `caption-06.txt` | Writer | Тезисы/подписи к кадрам |
| `clickbait.txt` | Clickbait | Overlay кадра 1, одна строка |
| `meta.json` | Package Metadata | `title`/`h1` ≠ `overlay_clickbait` |
| `GATE` | Gate | PASS или FAIL |
| `art-brief.md` | Art | Холст 2×3, кадр 1 только текст Clickbait |
| `canvas.png`, `slice-01.png`…`slice-06.png` | Art | Холст и 6 срезов |
| `package.meta.json` | Director | Статус публикации и пайплайна |
| `steps/0N-ROLE.json` | Director | Шаги выполнения ролей |

## Структура архива tgz для публикации

```text
package-upload.tgz
├── article.html              # H1 + тело без дубля cover-hero, врезки slice-02..06
├── article.meta.json          # title, slug, kind, product
├── description-brief.json     # excerpt (не дубль лида)
└── cover/
    ├── cover.png              # slice-01.png (обложка с красной рамкой и overlay)
    ├── inline-01.png          # slice-02.png
    ├── inline-02.png          # slice-03.png
    ├── inline-03.png          # slice-04.png
    ├── inline-04.png          # slice-05.png
    └── inline-05.png          # slice-06.png
```

Правила верстки `article.html`:
- H1 в начале статьи.
- Лид идёт один раз в тексте, без дублирования `dek` / `excerpt` сразу под H1.
- Обложка (`cover.png` = `slice-01.png`) отображается сайтом как hero один раз. Внутри `article.html` картинка `slice-01` **НЕ дублируется**.
- В теле статьи размещаются только врезки `inline-01.png` … `inline-05.png` (`slice-02` … `slice-06`).
- Нет слов «Сцена», «Возьмём:» и карточек Plot.

## Swarm

Директор **не** пишет scout / plot / title / story / clickbait / GATE / art-brief.
Каждый шаг — отдельный `Task`. Cloud: `Task(generalPurpose)` + файл роли.
Inline Директора = FAIL.

```text
Scout → Plot → Title → Writer → Gate(текст)
Clickbait: после Plot (можно параллельно с Writer / Gate)
Art: после Clickbait; на кадр 1 кладёт ТОЛЬКО clickbait.txt
Publisher: после GATE PASS и готовых картинок -> заливка на сайт
```

FAIL Gate → только проза. Холст текст не валит. Вернуть дырявый текстовый шаг, не чинить самому.
**Одна генерация холста.** Director не говорит «ещё раз нарисуй». Art не fail'ит Writer.
Лицо Холл не рисует.

## Чужое

Не открывать и не трогать: слоты 12:12 / 15:15 / 21:21, Алёну, `posts/`, `PUBLISH.md`, Composio, Дзен-боль.

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
site_publish: OK (URL) | SKIP (reason) | FAIL (error)
next: Hall
incident_report: none
```

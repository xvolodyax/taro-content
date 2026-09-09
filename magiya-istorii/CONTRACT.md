# Контракт пакета «Магия истории»

Пакет = одна история. Папка:

```text
magiya-istorii/packages/YYYY-MM-DD-slug/
```

`slug` — из **title/H1** (Эскалибур), не из кликбейта, не жирнейшая фраза Вордстата.

## Публикация на сайт (Эскалибур-пайплайн)

После того как `GATE` = PASS и готов холст 2K (срез `cover.png` + `inline-01`…`03`), Director запускает скрипт публикации `scripts/magiya_site_publish.py`. `publish` больше не всегда SKIP.
Холл руками ничего не upload, не approve и не publish — всё делает рой.

- Секрет: `SITE_PUBLISH_TOKEN` (также проверяются `HALL_PUBLISH_TOKEN`, `PUBLISH_TOKEN`, `TARO_SITE_TOKEN`).
- Токены **никогда не писать** в git, логи, чат или json-файлы.
- Если токена в окружении нет — скрипт выставляет `GATE` = PASS и `publish: SKIP` с причиной `нет ключа`, пайплайн не падает.
- Дзен Студию не открывать — сайт сам отдаёт RSS из `/blog/rss.xml`.
- Никаких воронок ТАРО: нет бота, нет приложения, нет «3 бесплатных расклада», нет кодовых слов.

## Файлы пакета

| Файл | Кто | Зачем |
| --- | --- | --- |
| `scout.md` | Scout | Живой спрос, угол ≠ топ H1. Историю не пишет |
| `plot.md` | Plot | Необязательные заметки. В статью не пишет. Биты не предписывает |
| `title-brief.md` | Title | Только H1 == title. Тело не правит |
| `story.md` | Writer | Только тело: проза + триггерный вопрос. Один проход |
| `article.html` | Director / Publisher | HTML из `story.md` + H1 + врезки `inline-01`…`03`. Без дубля cover |
| `article.meta.json` | Director / Publisher | Метаданные для загрузки на сайт |
| `description-brief.json` | Director / Publisher | Описание/excerpt (не дубль первого абзаца) |
| `clickbait.txt` | Clickbait | Overlay на клетке cover холста 2×2, одна строка |
| `meta.json` | Package Metadata | `title`/`h1` ≠ `overlay_clickbait` |
| `GATE` | Gate | Только проверка. Предложения не переписывает |
| `art-brief.md` | Art | Промпт холста 2K 2×2 |
| `canvas.png` | Art / Hall | Один Kie 2K; живые пакеты не регенерировать |
| `cover.png` | срез | Клетка 1 |
| `inline-01.png`…`03` | срез | Клетки 2–4, в тело |
| `package.meta.json` | Director | Статус публикации и пайплайна |
| `steps/0N-ROLE.json` | Director | Шаги выполнения ролей |

## Структура архива tgz для публикации

```text
package-upload.tgz
├── article.html              # H1 + тело без дубля cover-hero
├── article.meta.json          # title, slug, kind, product
├── description-brief.json     # excerpt (не дубль лида)
└── cover/
    ├── cover.png              # клетка 1: Вика, mic, красная рамка + кликбейт; в тело не дублировать
    ├── inline-01.png
    ├── inline-02.png
    └── inline-03.png          # без лица Вики
```

Правила верстки `article.html`:
- H1 в начале статьи.
- Лид идёт один раз в тексте, без дублирования `dek` / `excerpt` сразу под H1.
- Обложка (`cover.png`) отображается сайтом как hero один раз. Внутри `article.html` картинка `cover.png` не дублируется.
- Врезки только `inline-01`…`03`. Старые `inline-04`…`06` / шесть срезов в новые пакеты не класть.
- Нет слов «Сцена», «Возьмём:», «Примерьте на свою» и карточек Plot.

## Swarm

Директор **не** пишет scout / plot / title / story / clickbait / GATE / art-brief.
Каждый шаг — отдельный `Task`. Cloud: `Task(generalPurpose)` + файл роли.
Текстовые роли: строго Gemini 3.8 Flash High (в Cloud: model `gemini-3.8-flash`, param `reasoning_effort: high`; alias IDE Task: `gemini-3.8-flash-high`).
Дефолт не пишет в эфир ничего: ни H1, ни кликбейт, ни тело статьи.
Если Gemini недоступна / Task не спавнится / slug неверный — Director НЕ пишет текст сам! Только FAIL («модель недоступна»), без своего черновика. Лазейки «напишу сам» нет.
Inline Директора = FAIL.
Фиксера / копирайтера / второго прохода по телу **нет**.

```text
Scout → Plot(заметки) → Title(только H1) → Writer(только тело) → Gate(только проверка)
Clickbait: после Plot (можно параллельно с Writer — разный текст)
Art: после Clickbait; один холст 2K 2×2 → cover + inline-01…03; прозу не пишет; cover в тело не дублировать
Publisher: агент сам upload → approve → publish (`SITE_PUBLISH_TOKEN`)
```

FAIL тела → Writer. FAIL H1 → Title. FAIL overlay → Clickbait.
Plot на тело не возвращать. Картинка текст не валит. Не чинить самому.
**Одна генерация холста 2K.** Не четыре 1K. Не одна 16:9 без врезок (новые пакеты). Director не говорит «ещё раз нарисуй». Art не fail'ит Writer. Живые пакеты не перерисовывать.
Лицо Холл не рисует.

## Чужое

Не открывать и не трогать: слоты 12:12 / 15:15 / 21:21, Алёну, `posts/`, `PUBLISH.md`, Composio, Дзен-боль, Excalibur-плагин, Карусельку.
Живые пакеты (домовой, соль) не переписывать без нового задания Холла.

## Выход Директора Холлу

```text
=== MAGIYA DIRECTOR ===
package: magiya-istorii/packages/YYYY-MM-DD-slug
gate: PASS | FAIL
chars: <n>
kind: fiction | document
h1: <Эскалибур>
overlay: <кадр 1>
art: canvas 2K → cover + inline-01..03
site_publish: OK (URL) | SKIP (reason) | FAIL (error)
hall_chat: live URL / «на сайте» (полный story.md не класть)
next: Hall
incident_report: none
```

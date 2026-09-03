# Контракт пакета «Магия истории»

Пакет = одна история. Папка:

```text
magiya-istorii/packages/YYYY-MM-DD-slug/
```

`slug` — из **title/H1** (Эскалибур), не из кликбейта, не жирнейшая фраза Вордстата.

## Публикация на сайт (Эскалибур-пайплайн)

После того как `GATE` = PASS и готова одна обложка `cover.png` (16:9), Director запускает скрипт публикации `scripts/magiya_site_publish.py`. `publish` больше не всегда SKIP.
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
| `article.html` | Director / Publisher | Чистый HTML из `story.md` + H1. Без `inline-02`…`06`, без дубля обложки |
| `article.meta.json` | Director / Publisher | Метаданные для загрузки на сайт |
| `description-brief.json` | Director / Publisher | Описание/excerpt (не дубль первого абзаца) |
| `clickbait.txt` | Clickbait | Overlay на единственной обложке 16:9, одна строка |
| `meta.json` | Package Metadata | `title`/`h1` ≠ `overlay_clickbait` |
| `GATE` | Gate | Только проверка. Предложения не переписывает |
| `art-brief.md` | Art | Текст промпта обложки 16:9 (1K) |
| `cover.png` | Art | Готовая обложка 16:9 |
| `package.meta.json` | Director | Статус публикации и пайплайна |
| `steps/0N-ROLE.json` | Director | Шаги выполнения ролей |

## Структура архива tgz для публикации

```text
package-upload.tgz
├── article.html              # H1 + тело без дубля cover-hero
├── article.meta.json          # title, slug, kind, product
├── description-brief.json     # excerpt (не дубль лида)
└── cover/
    └── cover.png              # один кадр 16:9: реф Виктории, микрофон у рта, жирная красная рамка + кликбейт; в тело не дублировать
```

Правила верстки `article.html`:
- H1 в начале статьи.
- Лид идёт один раз в тексте, без дублирования `dek` / `excerpt` сразу под H1.
- Обложка (`cover.png`) отображается сайтом как hero один раз. Внутри `article.html` картинка `cover.png` не дублируется.
- `inline-02`…`inline-06` / `slice-01`…`slice-06` не делать и в статью не класть.
- Нет слов «Сцена», «Возьмём:», «Примерьте на свою» и карточек Plot.

## Swarm

Директор **не** пишет scout / plot / title / story / clickbait / GATE / art-brief.
Каждый шаг — отдельный `Task`. Cloud: `Task(generalPurpose)` + файл роли.
Текстовые роли: строго Gemini 3.8 Flash High (в Cloud: model `gemini-3.8-flash`, param `reasoning_effort: high`; alias IDE Task: `gemini-3.8-flash-high`).
Если Task недоступен — Director НЕ пишет текст сам (fallback на `gemini-3.8-flash`+high либо FAIL).
Inline Директора = FAIL.
Фиксера / копирайтера / второго прохода по телу **нет**.

```text
Scout → Plot(заметки) → Title(только H1) → Writer(только тело) → Gate(только проверка)
Clickbait: после Plot (можно параллельно с Writer — разный текст)
Art: после Clickbait; один кадр 16:9 (`cover.png`) = реф Виктория.png + микрофон в руке + жирная красная рамка + кликбейт; прозу не пишет; в тело ту же картинку не ставить
Publisher: агент сам upload → approve → publish (`SITE_PUBLISH_TOKEN`)
```

FAIL тела → Writer. FAIL H1 → Title. FAIL overlay → Clickbait.
Plot на тело не возвращать. Картинка текст не валит. Не чинить самому.
**Одна генерация обложки 16:9.** Не холст, не шесть кадров, не нарезка. Director не говорит «ещё раз нарисуй». Art не fail'ит Writer.
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
art: cover.png (один кадр 16:9)
site_publish: OK (URL) | SKIP (reason) | FAIL (error)
hall_chat: live URL / «на сайте» (полный story.md не класть)
next: Hall
incident_report: none
```

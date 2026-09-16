# IMAGE CANON — taro-content

Kie model: [`KIE_MODELS.md`](KIE_MODELS.md) — `gpt-image-2-5-flare-text-to-image` / `gpt-image-2-5-flare-image-to-image` (Flare).

Живые пакеты и уже вышедшие обложки **не перерисовывать** без команды Владимира. Правило на **будущие** пакеты.

Пиксели — только Kie. Реф лица Вики в этом репо: `magiya-istorii/refs/Виктория.png` (лист 12 ракурсов, ~2 191 823 байт). Один ракурс, без усреднения лиц.

---

## Возраст и CHARACTER LOCK (с 08.09; усиление историй 16.09)

Везде, где в кадре лицо Вики по рефу `Виктория.png` / Victoria.png: **тот же lock**, что у статей Эскалибура.

В промпт **сначала** CHARACTER LOCK, **потом** сцена / красная рамка / DJI / кликбейт (English: THEN scene).

**Lock (English, for Kie):**

- Victoria.png / `Виктория.png` from **ONE angle only**
- age **33**, youthful early-thirties (**NOT** 40+/45/50, **NOT** mature/aging)
- warm honey/wheat blonde with darker roots
- green eyes with slight hazel
- photorealistic natural skin (pores, no plastic/airbrush)
- face large and readable; props / red frame / DJI **must not** shrink or distort the face

**Negative must include:** age 40+, mature, aging, brown/grey eyes, plastic skin, face morph, tiny face, text on face

Слабый lock («Victoria age 33» без волос/глаз/кожи) — косяк 16.09: в историях likeness хуже статей. Запрещён.

---

## История / magiya (холст 2K, с 09.09 + face lock 16.09)

Источник правды геометрии: [`CANVAS_2K.md`](CANVAS_2K.md) (после PR #78: мастер **16:9**, не 1:1).

1. Одна Kie-генерация `resolution: 2K`, `aspect_ratio: 16:9`, сетка 2×2, белые швы. Не квадрат `1:1`.
2. Slice → `cover.png` + `inline-01`…`03` (все 16:9).
3. Не 4×1K отдельных задач. Живые `magiya-istorii/packages/2026-08-*` не трогать.

| Клетка | Содержание |
| --- | --- |
| **cover** | CHARACTER LOCK как у статей; **толстая красная рамка** этой клетки; кликбейт из `clickbait.txt` ON image (не на лицо); DJI Mic Mini у рта |
| **inline-01..03** | Сцены той же истории; без red frame; без лица Вики |

Промпт-шаблон: [`../prompts/story-canvas-2k-kie-system.txt`](../prompts/story-canvas-2k-kie-system.txt).  
Одиночная обложка (legacy, не холст): [`../prompts/story-cover-kie-system.txt`](../prompts/story-cover-kie-system.txt).  
Сборка промпта пакета (lock вшит): `python3 scripts/build_story_canvas_prompt.py --pack magiya-istorii/packages/YYYY-MM-DD-slug` → `prompts/kie-canvas-prompt-full.txt`. Скрипт **не** зовёт Kie и **не** рисует live.

---

## Статья / Excalibur (тот же face lock)

Cover статьи: тот же CHARACTER LOCK, B14 cover-text, **без** красной рамки magiya. Геометрия холста та же: 2K 16:9 2×2. Ядро: [`CANVAS_2K.md`](CANVAS_2K.md).

---

## Чеклист перед PASS (картинки)

- [ ] История: один 2K холст **16:9** → slice на 4×**16:9**; cover red frame + clickbait + DJI; **face lock = как у статей**; 3 inline без лица
- [ ] CHARACTER LOCK в промпте **перед** сценой
- [ ] Negative: age 40+, mature, aging, brown/grey eyes, plastic, face morph, tiny face, text on face
- [ ] Нет 4× отдельных 1K createTask
- [ ] Live обложки не перерисованы

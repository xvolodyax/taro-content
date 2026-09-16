# Canvas 2K + нарезка по белым швам

HARD 09.09.2026 (Холл, ночь). Дешёвый пайплайн картинок для **статей Эскалибура** и **историй «Магия истории»**.

Не регенерировать уже опубликованные живые ассеты (в т.ч. live id80 на квадратном 2K).

## Одна генерация, не четыре

| Было (дорого) | Стало |
| --- | --- |
| Четыре отдельных Kie `createTask` по **1K** (обложка + три врезки) | **Один** `createTask` на холст **2K** |
| Старое правило историй: только одна обложка 16:9 1K, без врезок | Тот же холст 2×2, что у статей; клетка обложки своя |
| Квадратный мастер `aspect_ratio: 1:1` (дефолт Kie, id80) | Мастер **`aspect_ratio: 16:9`**. После среза все четыре клетки — **16:9** горизонталь |

Четыре отдельные 1K-генерации **запрещены**. Квадратный мастер **запрещён** для новых холстов.

## Холст

- Сетка **2×2**: четыре равные клетки.
- Между клетками — **толстые белые швы** (white gutters), чтобы резалось без угадывания.
- Kie `resolution` — строка **`2K`**.
- Kie `aspect_ratio` — строка **`16:9`**. Не `1:1`. Не square. Не `auto` (auto + 2K у Kie ломается / даёт квадрат).
- Мастер 16:9 + равная сетка 2×2 ⇒ каждая клетка после среза тоже **16:9 landscape**.
- Модель: `gpt-image-2-5-flare-image-to-image`; если рефа нет — `gpt-image-2-5-flare-text-to-image`. Канон id: [`KIE_MODELS.md`](KIE_MODELS.md).
- Не Sunburst, не `gpt-image-2*`.

```text
cover        inline-01
inline-02    inline-03
```

Нарезка: `magiya-istorii/scripts/slice_canvas.py` (белые швы → `cover.png` + `inline-01.png`…`inline-03.png`). Лицо скрипт не рисует.

```text
python3 magiya-istorii/scripts/slice_canvas.py canvas.png --out DIR
```

## createTask (один, не четыре)

i2i (есть реф Вики / Victoria 33):

```json
{
  "model": "gpt-image-2-5-flare-image-to-image",
  "input": {
    "prompt": "<ядро холста из брифа>",
    "input_urls": ["<Victoria / Victoria 33>"],
    "aspect_ratio": "16:9",
    "resolution": "2K"
  }
}
```

t2i (рефа нет — пиксели не стартовать, если канон требует лицо):

```json
{
  "model": "gpt-image-2-5-flare-text-to-image",
  "input": {
    "prompt": "<ядро холста из брифа>",
    "aspect_ratio": "16:9",
    "resolution": "2K"
  }
}
```

`aspect_ratio: 1:1` / square / omitted → **FAIL для новых холстов**. Живые кадры не перерисовывать.

## Клетка обложки vs врезки

| | Статьи Эскалибура | Истории «Магия истории» |
| --- | --- | --- |
| Пайплайн | тот же холст 2K 16:9 2×2 + шов + срез | тот же |
| Cover (верх-лево) | **тот же CHARACTER LOCK** (Victoria.png, 33 youthful, honey/wheat + darker roots, green/hazel, photoreal skin) + **B14** кириллический cover-text **на пикселях** + brand line. **Без** красной рамки | **тот же CHARACTER LOCK, что у статей** (не «Victoria age 33» без волос/глаз/кожи) + DJI Mic Mini у рта + кликбейт из `clickbait.txt` **на пикселях** + **жирная красная рамка** этой клетки. Сцена/рамка/mic **не** сжимают лицо |
| inline-01…03 | без лица Вики | без лица Вики; без красной рамки; биты сюжета |

Обложку в тело второй раз не ставить. Врезки — в статью, не в карусель TG/IG.

Лицо: [`IMAGE_CANON.md`](IMAGE_CANON.md). С 16.09.2026 в промпте истории **сначала lock**, потом сцена.

## Ядро промпта: статьи Эскалибура

```text
A cinematic 2x2 photographic contact sheet on ONE 16:9 landscape master canvas (Kie aspect_ratio 16:9, NOT 1:1 square), resolution 2K, one canvas not four images. Four equal 16:9 landscape panels separated by THICK WHITE gutter seams so each panel stays 16:9 after slice. CHARACTER LOCK first (cover cell): use Victoria.png from ONE angle only; woman age 33, youthful early-thirties (NOT 40+/45/50, NOT mature/aging); warm honey/wheat blonde with darker roots; green eyes with slight hazel; photorealistic natural skin (pores, no plastic/airbrush); face large and readable. THEN scene: B14 Cyrillic cover-text baked ON the pixels (not a sticker bar) plus a brand line; NO red frame. Panels 2 to 4: NO Victoria face; distinct editorial stills of place, object and atmosphere for the article. Thick white gutters must stay sliceable. Negative: age 40+, mature, aging, brown eyes, grey eyes, plastic skin, face morph, tiny face, text on face.
```

## Ядро промпта: истории «Магия истории» (тот же lock)

```text
A cinematic 2x2 photographic contact sheet on ONE 16:9 landscape master canvas (Kie aspect_ratio 16:9, NOT 1:1 square), resolution 2K, one canvas not four images. Four equal 16:9 landscape panels separated by THICK WHITE gutter seams so each panel stays 16:9 after slice. CHARACTER LOCK first (cover cell, same as Excalibur articles): use Victoria.png / Виктория.png from ONE angle only; woman age 33, youthful early-thirties (NOT 40+/45/50, NOT mature/aging); warm honey/wheat blonde with darker roots; green eyes with slight hazel; photorealistic natural skin (pores, no plastic/airbrush); soft gentle features; keep likeness — do not beautify into a different person; face large and readable. THEN cover scene (props, red frame and DJI Mic Mini MUST NOT shrink or distort the face): stylish 2020s investigative reporter holding a compact black DJI Mic Mini Transmitter in her hand right near her mouth; BOLD THICK RED magazine cover border around THIS PANEL ONLY; high-impact DISPLAY Cyrillic overlay with the clickbait title baked on the pixels, text NOT on face. Panels 2 to 4: NO Victoria face, NO red frame, NO clickbait; distinct story-beat editorial photographs of place, object and atmosphere from the same setting and light. Thick white gutters must stay sliceable. Negative: age 40+, mature woman, aging face, brown eyes, grey eyes, plastic/airbrush skin, wrong woman, face morph, tiny face, text on face.
```

Сборка пакета: `python3 scripts/build_story_canvas_prompt.py --pack …` (Kie не вызывает). Шаблон: `prompts/story-canvas-2k-kie-system.txt`.

## Что не этот пайплайн

- Посты 12:12 / 21:21 — по-прежнему **один** кадр **1K 1:1**, не холст.
- Каруселька / carousel storyboard — по-прежнему **4K**.
- Живые пакеты (`magiya-istorii/packages/2026-08-*`, уже вышедшие статьи, **id80**) — не перерисовывать ради смены формата.

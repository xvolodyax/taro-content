# Canvas 2K + нарезка по белым швам

HARD 09.09.2026 (Холл, вечер). Дешёвый пайплайн картинок для **статей Эскалибура** и **историй «Магия истории»**.

Не регенерировать уже опубликованные живые ассеты.

## Одна генерация, не четыре

| Было (дорого) | Стало |
| --- | --- |
| Четыре отдельных Kie `createTask` по **1K** (обложка + три врезки) | **Один** `createTask` на холст **2K** |
| Старое правило историй: только одна обложка 16:9 1K, без врезок | Тот же холст 2×2, что у статей; клетка обложки своя |

Четыре отдельные 1K-генерации **запрещены**.

## Холст

- Сетка **2×2**: четыре равные клетки.
- Между клетками — **толстые белые швы** (white gutters), чтобы резалось без угадывания.
- Kie `resolution` — строка **`2K`**.
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

## Клетка обложки vs врезки

| | Статьи Эскалибура | Истории «Магия истории» |
| --- | --- | --- |
| Пайплайн | тот же холст 2K 2×2 + шов + срез | тот же |
| Cover (верх-лево) | **Victoria 33** + **B14** кириллический cover-text **на пикселях** + brand line. **Без** красной рамки | Вика с рефа + DJI Mic Mini у рта + кликбейт из `clickbait.txt` **на пикселях** + **жирная красная рамка** этой клетки |
| inline-01…03 | без лица Вики | без лица Вики; без красной рамки; биты сюжета |

Обложку в тело второй раз не ставить. Врезки — в статью, не в карусель TG/IG.

## Ядро промпта: статьи Эскалибура

```text
A cinematic 2x2 photographic contact sheet of 4 equal panels separated by THICK WHITE gutter seams, resolution 2K, one canvas not four images. Panel 1 (top-left, cover): Victoria 33 face lock from the reference sheet, one angle, no morphing; B14 Cyrillic cover-text baked ON the pixels (not a sticker bar) plus a brand line; NO red frame. Panels 2 to 4: NO Victoria face; distinct editorial stills of place, object and atmosphere for the article. Thick white gutters must stay sliceable.
```

## Что не этот пайплайн

- Посты 12:12 / 21:21 — по-прежнему **один** кадр **1K**, не холст.
- Каруселька / carousel storyboard — по-прежнему **4K**.
- Живые пакеты (`magiya-istorii/packages/2026-08-*` и уже вышедшие статьи) — не перерисовывать ради смены формата.

---
name: dzen-cover
description: "Обложка Дзена по приёму Хорошева: лицо i2i + cover_hook 2–6 слов на кадре. 1K. Не design code Excalibur, не localhost."
model: inherit
readonly: false
is_background: false
---

**Язык:** русский. Канон: `articles/ARTICLE.md` §7. Шаблон: `articles/templates/cover-brief.md`.

Плагин Excalibur не ставить. Берём приём (лицо + короткий хук на кадре), не белое худи / стикеры / quad 2×2.

Если влит `images/PROMPTS.md` — для статей Дзена §7 главнее: хук на обложке **нужен**.

## Задача

1. Заполнить `face` / `cover_hook` / `scene_hint` / `forbidden_style`.
2. `face: victoria` по умолчанию. `alena` — только если статья про неё или её слот. Нет рефа в `images/refs/` — `face: none`, человека нет. Двойника не выдумывать.
3. `cover_hook` — 2–6 слов **на кадре**, ≠ H1, ≠ description. Пустая атмосфера — FAIL.
4. Реф есть → Kie.ai `gpt-image-2-image-to-image`. Рефа нет → `gpt-image-2-text-to-image`. **1K, не 2K**.
5. Светлый современный кадр. Запрет: тёмный стол, свечи, готика, «магический подвал».
6. Файл на диск. В Дзен потом **файлом**, не localhost.

Не публиковать.

## Выход

`articles/dzen/<slug>/cover-brief.md` + `cover.png`

```text
=== DZEN COVER ===
face: victoria | alena | none
cover_hook:
resolution: 1K
file_on_disk: cover.png | pending
incident_report: none | articles/pipeline-errors.md#INC-…
```

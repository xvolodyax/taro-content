---
name: dzen-description
description: "Тизер карточки Дзена: 80–180 знаков, ≠ title, ≠ обрезка лида."
model: inherit
readonly: false
is_background: false
---

**Язык:** русский. Канон: `articles/ARTICLE.md` §6. Шаблон: `articles/templates/dzen-description.md`.

## Когда

После Главреда, по финальному `article.md`. Прозу не трогать.

## Жёстко

- description ≠ title / h1
- description ≠ первые N символов opening
- 80–180 символов, одно предложение
- без HTML, эмодзи, URL, хештегов, кликбейта

Инцидент-антипаттерн: `articles/pipeline-errors.md#INC-excalibur-description-dup`.

## Выход

`articles/dzen/<slug>/dzen-description.md`

```text
=== DZEN DESCRIPTION ===
topic_id:
description:
char_count:
verdict: PASS | FAIL
incident_report: none | articles/pipeline-errors.md#INC-…
```

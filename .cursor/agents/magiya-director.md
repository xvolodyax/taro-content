---
name: magiya-director
description: |
  [Д] Директор «Магия истории». Будит роли, сам не пишет.
  Тело — Writer. H1 — Title. Overlay — Clickbait.
  Если Task недоступен — сам текст не пишет: fallback на gemini-3.8-flash+high или FAIL.
  Посты / 21:21 / Excalibur / Карусельку не трогать.
model: inherit
is_background: false
---

Исполняй `magiya-istorii/.cursor/agents/magiya-director.md`.
Канон: `magiya-istorii/CANON.md`.
В промпт Writer биты Plot не вшивать.
Текстовые роли: Cloud model `gemini-3.8-flash` + `reasoning_effort: high` (alias IDE Task: `gemini-3.8-flash-high`). Если недоступен — не писать текст самому, FAIL.

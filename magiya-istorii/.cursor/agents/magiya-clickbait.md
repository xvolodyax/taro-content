---
name: magiya-clickbait
description: "Clickbait «Магия истории»: только overlay кадра 1. Gemini 3.8 Flash High."
model: gemini-3.8-flash
reasoning_effort: high
readonly: false
is_background: false
---

Исполняй `magiya-istorii/.cursor/agents/clickbait.md`.
Только overlay кадра 1. Тело и H1 не трогать.
Модель: Cloud model `gemini-3.8-flash` + `reasoning_effort: high` (alias локального IDE Task: `gemini-3.8-flash-high`).
Дефолтный агент overlay не пишет: если модель недоступна — FAIL («модель недоступна»), без своего черновика.

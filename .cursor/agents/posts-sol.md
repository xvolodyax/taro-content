---
name: posts-sol
description: "Alias posts-copywriter. Не отдельная роль. Director MUST Task(posts-copywriter). gpt-5.6-sol / OpenAI API."
model: inherit
reasoning_effort: low
readonly: false
is_background: false
---

Ты **posts-copywriter**. Открой `.cursor/agents/posts-copywriter.md` и skill
`.cursor/skills/posts-copywriter/SKILL.md`. Живая сцена, вопросы, CTA.

В step record пиши `role: posts-copywriter`. `written_by: openai-api-gpt-5.6-sol`. Текст: `--model gpt-5.6-sol`.

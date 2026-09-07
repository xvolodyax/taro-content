Ты один шаг роя постов ТАРО СЕЙЧАС. Не Директор.

Роль: posts-gate
Пакет: posts/2026-08-29-1212
Runtime: cloud
Спавн: Task(generalPurpose) — этот промпт целиком
Модель шага: gemini-3.7-flash-high
written_by: gemini
publish: SKIP
Главред: REMOVED. Не писать «можно публиковать».

Прочитай целиком и следуй:
- .cursor/agents/posts-gate.md
- .cursor/skills/posts-gate/SKILL.md
- POSTS.md
- shared/posts-soul.md
- shared/posts-funnel.md
- shared/posts-step-contract.md
- shared/posts-model-policy.json

Уже готово: слот 12:12 2026-08-29. Пакет собран: brief, meaning, площадки, cover. Прогон: python3 scripts/posts_gate.py --package posts/2026-08-29-1212 --require-swarm --write. Не переписывать тексты. Главред снят. «можно публиковать» не писать. Слово Сцена не писать (в чеклисте: кадр). publish SKIP. written_by: gemini.
Артефакты этого шага: GATE

Запрещено:
- писать соседние роли (тема + тезис + пост + хук в одних руках)
- Task(posts-*), /in-cloud, /babysit, environment: cloud
- публиковать, ходить в Telegram/Composio/browser
- генерировать картинку / звать Kie
- Главред, слово «ловушка»
- Opus / Sonnet / Composer как писатель

Верни Директору маркер роли и список файлов. Не публикуй.

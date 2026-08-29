Ты один шаг роя постов ТАРО СЕЙЧАС. Не Директор.

Роль: posts-gate
Пакет: posts/2026-08-29-1515
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

Уже готово: слот 15:15 2026-08-29. researcher, meaning, copywriter готовы. Cover нет (шаг 04 = gate). Сначала python3 scripts/posts_gate.py --package posts/2026-08-29-1515 --require-swarm --write. Если скрипт FAIL — вердикт FAIL, площадки не переписывать. Дополнительно проверь лимиты опроса (ВК ≤80, TG header+вопрос ≤300, варианты ≤100), 4 случайные карты не набор 28.08, нет картинки/ПРИНИМАЮ/бота/кодового слова, poll.txt 5 строк, чужие пакеты не тронуты. Главред снят. «можно публиковать» не писать. publish SKIP.
Артефакты этого шага: GATE

Запрещено:
- писать соседние роли (тема + тезис + пост + хук в одних руках)
- Task(posts-*), /in-cloud, /babysit, environment: cloud
- публиковать, ходить в Telegram/Composio/browser
- генерировать картинку / звать Kie
- Главред, слово «ловушка»
- Opus / Sonnet / Composer как писатель

Верни Директору маркер роли и список файлов. Не публикуй.

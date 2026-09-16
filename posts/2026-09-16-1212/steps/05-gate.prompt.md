Ты один шаг роя постов ТАРО СЕЙЧАС. Не Директор.

Роль: posts-gate
Пакет: posts/2026-09-16-1212
Runtime: cloud
Спавн: Task(generalPurpose) — этот промпт целиком
Модель шага: inherit (модель окна; не пинить slug). Текст слота не писать.
reasoning_effort: low
# high — только явный оверрайд Владимира
written_by: openai-api-gpt-5.6-sol
канон модели: docs/POSTS_TEXT_MODEL.md
publish: SKIP
Главред: REMOVED. Не писать «можно публиковать».
Дефолтный Cloud Agent / Director текст не пишет. Нет OpenAI API / модели — FAIL, без своего черновика.

Прочитай целиком и следуй:
- .cursor/agents/posts-gate.md
- .cursor/skills/posts-gate/SKILL.md
- POSTS.md
- posts/_canon-1212/README.md
- posts/_canon-1212/platforms.md
- posts/_canon-2121/platforms.md
- posts/_canon-2121/debrief.md
- shared/posts-soul.md
- shared/posts-funnel.md
- shared/posts-step-contract.md
- shared/posts-model-policy.json

Уже готово: слот 12:12 2026-09-16; brief.md есть (Scout, marriage); meaning FAIL: OpenAI API 401 ip_not_authorized с IP 3.149.191.121; copywriter/cover НЕ звать; Director текст не писал; cover нет; cover_md5: none; cover_hook: none; verdict должен быть FAIL openai_api, return: meaning
Артефакты этого шага: GATE

Запрещено:
- писать соседние роли (тема + тезис + пост + хук в одних руках)
- Task(posts-*), /in-cloud, /babysit, environment: cloud
- публиковать, ходить в Telegram/Composio/browser
- генерировать картинку / звать Kie
- Главред, слово «ловушка»
- Opus / Sonnet / Composer / gpt-5.5 как писатель слота

Верни Директору маркер роли и список файлов. Не публикуй.

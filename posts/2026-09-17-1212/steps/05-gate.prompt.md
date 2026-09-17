Ты один шаг роя постов ТАРО СЕЙЧАС. Не Директор.

Роль: posts-gate
Пакет: posts/2026-09-17-1212
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

Уже готово: brief.md family OK; meaning Task был, OpenAI 401 ip_not_authorized, meaning.md пустой шаблон; copywriter/cover-text/Kie не звать; площадок нет; cover нет.
Артефакты этого шага: GATE

Запрещено:
- писать соседние роли (тема + тезис + пост + хук в одних руках)
- Task(posts-*), /in-cloud, /babysit, environment: cloud
- публиковать, ходить в Telegram/Composio/browser
- генерировать картинку / звать Kie
- Главред, слово «ловушка»
- Opus / Sonnet / Composer / gpt-5.5 как писатель слота

Верни Директору маркер роли и список файлов. Не публикуй.

## Этот шаг

Пакет: `posts/2026-09-17-1212`. Слот 12:12 2026-09-17.

1. Прочитай skill и запусти:
   `python3 scripts/posts_gate.py --package posts/2026-09-17-1212 --require-swarm --write`
2. Предложения не переписывать. Пост/тезис/хук не писать.
3. Copywriter и cover-text не звать.
4. В `GATE` обязательно строки:
   - `cover_md5: none`
   - `cover_hook: none`
   - `openai_api: FAIL (модель недоступна)`
   - причина 401 `ip_not_authorized`, IP Cloud Agent: `52.15.104.219`
5. `return: meaning`. `publish: SKIP`. `READY_TO_SEND` нет.
6. Не публиковать.

Маркер:
=== POSTS GATE ===
verdict: FAIL
return: meaning
cover_md5: none
cover_hook: none
publish: SKIP

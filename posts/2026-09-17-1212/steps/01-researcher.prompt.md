Ты один шаг роя постов ТАРО СЕЙЧАС. Не Директор.

Роль: posts-researcher
Пакет: posts/2026-09-17-1212
Runtime: cloud
Спавн: Task(generalPurpose) — этот промпт целиком
Модель шага: inherit (модель окна; не пинить slug). Текст слота не писать.
reasoning_effort: low
# high — только явный оверрайд Владимира
written_by: inherit
канон модели: docs/POSTS_TEXT_MODEL.md
publish: SKIP
Главред: REMOVED. Не писать «можно публиковать».
Дефолтный Cloud Agent / Director текст не пишет. Нет OpenAI API / модели — FAIL, без своего черновика.

Прочитай целиком и следуй:
- .cursor/agents/posts-researcher.md
- .cursor/skills/posts-researcher/SKILL.md
- POSTS.md
- POSTS_SCOUT_CANON.md
- posts/_canon-1515/SEED.md
- posts/_canon-2121/SEED.md
- shared/posts-soul.md
- shared/posts-funnel.md
- shared/posts-step-contract.md
- shared/posts-model-policy.json

Scout 12:12 / 15:15: ниша relations+marriage+kids+family+tarot_moment. Анти-монотонность против зажёванного chat_promise. Холл угол не назначает. 21:21 угол не выбирает.
Скрипт: python3 scripts/posts_scout_clusters.py --lookback-days 7

Уже готово: слот 12:12 четверг 2026-09-17 MSK; папка posts/2026-09-17-1212 пустая; живого 12:12 сегодня нет; в чекауте нет dated-пакетов за 7 дней (scout_clusters → overused:none) — учесть факты недели из промпта, угол сам
Артефакты этого шага: brief.md

Запрещено:
- писать соседние роли (тема + тезис + пост + хук в одних руках)
- Task(posts-*), /in-cloud, /babysit, environment: cloud
- публиковать, ходить в Telegram/Composio/browser
- генерировать картинку / звать Kie
- Главред, слово «ловушка»
- Opus / Sonnet / Composer / gpt-5.5 как писатель слота

Верни Директору маркер роли и список файлов. Не публикуй.

# Посты «ТАРО СЕЙЧАС» — канон роя

Одно окно. Один слот. Директор **только** оркестрирует.
Тема, тезис, пост и хук — разные агенты. Inline Директора = `GATE` FAIL.
В эфир — только `GATE` = PASS. После PASS **рой сам** кладёт слот через Composio.
Холл **не** публикует. Как вызывать и env: [`posts/PUBLISH.md`](posts/PUBLISH.md).

Это не статьи Excalibur, не Дзен, не рилсы, не Каруселька-контент.
Репу `taro-excalibur` не клонировать.

Слово **«ловушка»** не использовать. Главред **снят**: шага нет, фразы
«можно публиковать» нет. Холлу достаточно PASS.

Пакет пишется, только если Холл назвал слот и дату.
Сегодняшний уже вышедший слот не переписывать.

## Петля дня

```text
alena-0700  письмо Алёны в t.me/AlenaSafonova_queen (не @TodayTaro)
12:12       сцена + вопросы в бота → TG + IG RU
15:15       опрос на ту же сцену → только TELEGRAM_SEND_POLL
21:21       разбор опроса: карта = совет, без «Сцена» → TG
```

Статьи 9:00 / 16:00 / 20:00 живут в Дзене и на сайте. **21:21 от статьи не зависит.**
Instagram и YouTube в 21:21 не писать.

## Как запускать день

Одно Cloud / plugin окно в `taro-content`. Главный агент — `posts-director`.
Не `Task(posts-director)`. Не `/in-cloud`. Не `/babysit`. Главред не звать.
Холл не публикует.

Env в среду агента (значение ключа в чат и git не писать):

| Env | Зачем |
| --- | --- |
| `COMPOSIO_API_KEY` | TG и IG. Нет — SKIP, не падать |
| `POST_IMAGE_URL` / `ALENA_COVER_URL` | публичный HTTPS кадра |
| `MAX_BOT_TOKEN` + `MAX_CHAT_ID` | Макс; иначе Макс не трогаем |

Алиасы Composio, не default: `telegram-composia` (`@TodayTaro` / канал Алёны),
`instagram-ru`, `instagram-en` (EN этими слотами не шлём).

1. **alena-0700** — промпт слота. PASS → `posts_publish.py` в `t.me/AlenaSafonova_queen` в 07:00 МСК. Рефки не менять.
2. **12:12** — промпт. PASS → TG+IG RU, картинка+текст. ВК и YouTube community не трогать.
3. **15:15** — опрос + 4 расклада вместе. PASS → только `TELEGRAM_SEND_POLL`.
4. **21:21** — из `debrief.md`. PASS → TG картинка+текст. Карта = совет, без «Сцена».

Telegram без отложки: раньше слота МСК не слать. Слот прошёл — сразу.
Живые сегодняшние не дублировать.

После PASS Директор:

```text
python3 scripts/posts_publish.py --package posts/YYYY-MM-DD-HHMM
```

Писатели шагов: `publish: SKIP`.

### Cloud vs plugin

| Где окно | Как Директор зовёт шаг |
| --- | --- |
| Cloud | один `Task(generalPurpose)` + `scripts/posts_dispatch_prompt.py` |
| Plugin | `Task(posts-researcher)` / `meaning` / `copywriter` / `cover-text` / `gate` |

После каждого Task — `scripts/posts_step_record.py`. Потом stamp + `scripts/posts_gate.py --require-swarm`.

## Промпт 12:12

```text
Слот 12:12 на YYYY-MM-DD.
Канон: POSTS.md. Рой в этом окне, Директор не пишет тексты:
researcher → meaning → copywriter → cover-text → gate.
Cloud: один Task(generalPurpose) на шаг + dispatch-prompt.
Plugin: Task(posts-*).
written_by: gemini. Opus/Sonnet/Composer = FAIL.
Пакет: posts/YYYY-MM-DD-1212/
После PASS: python3 scripts/posts_publish.py --package posts/YYYY-MM-DD-1212
TG+IG RU, картинка+текст. ВК и YouTube не трогать. Холл не публикует.
Не генерировать картинку. Не писать 15:15 и 21:21.
Главред не звать. Существующие и уже вышедшие посты не трогать.
```

## Промпт 15:15

Опрос и вечерний разбор пишутся **вместе**, в 13:15. Голоса не ждать.

```text
Слот 15:15 на YYYY-MM-DD. Та же сцена, что 12:12.
Канон: POSTS.md. Рой: researcher → meaning → copywriter → gate. Cover нет.
Copywriter: опрос + 4 расклада вместе. Карты: draw_rw_cards.py, не «в тему».
Cloud: Task(generalPurpose)+dispatch. Plugin: Task(posts-*).
written_by: gemini. Главред не звать.
Пакет: posts/YYYY-MM-DD-1515/
После PASS: python3 scripts/posts_publish.py --package posts/YYYY-MM-DD-1515
Только TELEGRAM_SEND_POLL. Холл не публикует. Существующие посты не трогать.
```

## Промпт 21:21

Если `posts/YYYY-MM-DD-1515/debrief.md` есть — researcher/meaning не запускать.

```text
Слот 21:21 на YYYY-MM-DD.
Канон: POSTS.md. Разбор опроса, не тизер статьи.
Рой: copywriter (из debrief) → cover-text → gate.
Cloud: Task(generalPurpose)+dispatch. Plugin: Task(posts-*).
written_by: gemini. Без IG/YT. Карта = совет, без «Сцена». Главред не звать.
Пакет: posts/YYYY-MM-DD-2121/
После PASS: python3 scripts/posts_publish.py --package posts/YYYY-MM-DD-2121
TG картинка+текст. Холл не публикует. Существующие посты не трогать.
```

## Цепочка

```text
researcher(одна тема) → meaning(один тезис)
→ copywriter(сцена, вопросы / опрос+debrief, CTA)
→ cover-text(3 хука, один в центре) → gate → publish
```

| Шаг | Агент | Модель | Выход |
| --- | --- | --- | --- |
| 0 | `posts-director` | inherit | папка, Task, step records, после PASS `posts_publish.py` |
| 1 | `posts-researcher` | inherit | `brief.md` |
| 2 | `posts-meaning` | `gemini-3.7-flash-high` | `meaning.md` |
| 3 | `posts-copywriter` | `gemini-3.7-flash-high` | площадки; на 15:15 ещё `debrief.md` |
| 4 | `posts-cover-text` | `gemini-3.7-flash-high` | `cover-text.json` + `image-prompt.txt` (нет на 15:15 и alena) |
| 5 | `posts-gate` | `gemini-3.7-flash-high` + `scripts/posts_gate.py` | `GATE` |

Алиасы: Scout → researcher, Writer → meaning, Sol → copywriter. Новых ролей сверх таблицы нет.

FAIL → вернуть дырявый шаг Task-ом. Директор не «доглаживает».
В эфир без PASS нельзя.

## Слоты

| Слот | Что | В эфир (рой) | Не трогать |
| --- | --- | --- | --- |
| **alena-0700** | письмо, рефки как есть | TG `@AlenaSafonova_queen` 07:00 | `@TodayTaro`, IG, ВК, YT |
| **12:12** | фото + текст. Сцена и 2–3 вопроса в бота | TG `@TodayTaro` + IG RU | ВК, YouTube community |
| **15:15** | опрос + сразу 4 вечерних расклада | только `TELEGRAM_SEND_POLL` | картинка, IG, Макс, ВК, YT |
| **21:21** | разбор: карта = совет, без «Сцена» | TG фото+текст | IG, YT, ВК |

**12:12.** Первая строка = сцена, не заголовок темы. Подпись TG ≤ 1024.
TG / ВК / Макс **без** кодового слова. IG — слово в комментарий + «ссылки в шапке». YT — шапка канала.

**15:15.** Без картинки, без Макс, без IG/YT. Вопрос ВК ≤ 80.
Четыре варианта = четыре состояния рук. Карты случайные Райдер-Уэйт, не подобраны к ответам.

**21:21.** Не тизер статьи. Instagram и YouTube не делать. В эфире нет слова «Сцена».
Карта советует ход, не ставит диагноз.

На каждый из 4 вариантов:

1. Своя **случайная** карта Райдер-Уэйт (русские имена). Сначала жеребьёвка, потом текст. Вчерашний набор не повторять (`posts/LEDGER.md`).
2. Карта + этот ответ → совет на вечер, не диагноз.
3. Одно действие руками сегодня вечером.

Каркас 21:21 (TG = Макс, ≤ 1024):

- 1–2 строки дневной сцены
- «Ты проголосовала. Вот расклад по твоему варианту.»
- 4 блока: вариант / карта / 2 предложения
- мягко: вопрос в бота (3 расклада) или аудио в приложении

Слот **18:18** этой машины нет. Рилсы — `video/`.

## Канон смысла

Клиентки **20–50**. ~78% отношения. Расклад нужен, чтобы сегодня решить ход.

- **researcher:** один угол из Wordstat / боли. Не 13–17, не война, не медицина.
- **meaning:** один тезис / почему этот хук. Не подпись.
- **copywriter = Gemini:** живая сцена, 2–3 вопроса, CTA площадок.
- **cover-text:** 3 хука, один в центре 1:1.
- **gate:** вода, воронка, рой, штамп. Голос не гладит.

Полный слог: [`shared/posts-soul.md`](shared/posts-soul.md).

## Воронка (не путать бот и приложение)

| Что | Зачем | Куда |
| --- | --- | --- |
| Бот TG | 3 бесплатных расклада | https://t.me/TodayTaro_bot?start=id8293683394 |
| Приложение TG | аудио «Суть – Тень – Вектор» | https://t.me/TodayTaro_bot?startapp=ref_361BDE45 |
| Бот Макс | 3 бесплатных расклада | https://max.ru/id531102974575_bot |
| Приложение Макс | аудио «Суть – Тень – Вектор» | https://max.ru/id531102974575_bot?startapp=ref_9BAD4149 |
| Приложение ВК | аудио «Суть – Тень – Вектор» | https://vk.com/app54565776 |

Канон: [`shared/posts-funnel.md`](shared/posts-funnel.md).
IG / YT: сырых URL нет, «ссылки в шапке», IG — слово в коммент.

## Кадр (12:12 и 21:21)

3 кандидата, один выбран. Хук 2–6 слов **строго по центру** 1:1, читается как превью сетки (~200px).
Не капс-H1, не Вордстат, не первая строка TG. Пиксели рисует Холл через Kie.
15:15 картинки нет.

## Пакет

```text
posts/YYYY-MM-DD-HHMM/
  brief.md
  meaning.md
  debrief.md          # 15:15 обязательно
  tg.html
  vk.html
  max.txt             # нет на 15:15
  ig.txt              # только 12:12
  yt.txt              # только 12:12
  cover-text.json     # 12:12 и 21:21
  image-prompt.txt    # 12:12 и 21:21
  package.meta.json
  steps/*.json
  GATE
  publish.json        # после posts_publish.py
  cover-url.txt       # публичный HTTPS кадра, если есть
```

Шаблоны: [`posts/templates/`](posts/templates/). Старые пакеты не переписывать.
Сухой прогон роя: `python3 scripts/posts_swarm_dry_run.py` (0 живых публикаций).
Публикация: `python3 scripts/posts_publish.py --package DIR`. Холл не публикует.

## Запреты

- Один агент пишет тему + тезис + пост + хук
- Директор пишет inline (без Task / без dispatch-prompt)
- Главред, «можно публиковать» от Главреда
- Opus / Sonnet / Composer как писатель
- Публикация писателем шага или Холлом; default-аккаунт Composio
- Ключ `COMPOSIO_API_KEY` в git / лог / чат
- ВК и YouTube community
- Отложка Telegram; слать раньше слота МСК
- Дубль живого сегодняшнего
- `Task(posts-director)`, `/in-cloud`, `/babysit`, background Task
- Специалист зовёт `Task(posts-*)`
- Писать соседний слот «заодно» или уже вышедший сегодняшний
- Путать бот и приложение; сырой URL в IG
- «Загадай ситуацию», слово «ловушка»
- Подбирать карту «под вариант»; ждать голоса 15:15
- Тизер статьи в 21:21; слово «Сцена» в 21:21
- Плодить 13-го агента / `posts-cover-hook` / второго Директора
- Менять рефки Алёны; слать alena-0700 в `@TodayTaro`

## Промпт alena-0700

```text
Слот alena-0700 на YYYY-MM-DD.
Канал: https://t.me/AlenaSafonova_queen (не @TodayTaro).
Канон: POSTS.md + posts/ALENA.md. Рефки не менять.
После PASS: python3 scripts/posts_publish.py --package posts/YYYY-MM-DD-alena
Холл не публикует. Cover нет.
```

## Файлы

Публикация: [`posts/PUBLISH.md`](posts/PUBLISH.md).
Алёна: [`posts/ALENA.md`](posts/ALENA.md).
Цепочка: [`shared/posts-chain.md`](shared/posts-chain.md).
Шаги: [`shared/posts-step-contract.md`](shared/posts-step-contract.md).
Модели: [`shared/posts-model-policy.json`](shared/posts-model-policy.json).
Роли: [`.cursor/agents/FOR-AGENTS.md`](.cursor/agents/FOR-AGENTS.md).

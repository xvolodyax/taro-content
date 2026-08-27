# Рой постов — контракт (как Karuselka)

Одно окно. Директор **не пишет** эфир. Один шаг = один Task. Публикует Холл.

Это не статьи Дзена и не карусель. Репу `Karuselka` / `taro-excalibur` не клонировать.
От Карусельки берём только закон: оркестратор не сотрудник, Cloud без `Task(posts-*)` → `Task(generalPurpose)` с промптом сотрудника.

## Сотрудники (закрытый список)

| # | Роль | Файл | Модель | Пишет |
| --- | --- | --- | --- | --- |
| 0 | Директор | `posts-director.md` | inherit | только handoff / папка из шаблонов. **Не** эфир |
| 1 | researcher | `posts-researcher.md` | `gemini-3.7-flash-high` | `brief.md` (боль Wordstat / тема) |
| 2 | meaning | `posts-meaning.md` | `gemini-3.7-flash-high` | `meaning.md` (один тезис) |
| 3 | copywriter | `posts-copywriter.md` | `gemini-3.7-flash-high` | сцена, вопросы, опрос, debrief 21:21, площадки |
| 4 | cover-text | `posts-cover-text.md` | `gemini-3.7-flash-high` | хуки 12:12 и 21:21; 15:15 шага нет |
| 5 | gate | `posts-gate.md` | `gemini-3.7-flash-high` | `GATE` |

**Нет ролей:** Главред, Sol, Scout, Writer, Publish, Cover-render, второй Директор.
Качество живёт внутри researcher + meaning + Gemini-copywriter + gate.
Не ждать штампа «можно публиковать». `GATE` = PASS значит пакет готов Холлу. Холл публикует руками.

## Cloud (HARD)

В Cloud **нет** `Task(posts-*)`. Директор на каждый шаг:

```text
Task(generalPurpose)
  model: gemini-3.7-flash-high   # весь человеческий текст
  run_in_background: false
  prompt: полный текст .cursor/agents/posts-<role>.md
          + путь пакета + слот + что уже есть + что не делать
```

`Inline «я теперь копирайтер»` = FAIL. Директор не дописывает `tg.html` / `debrief.md` / хук.

## Цепочка

```text
researcher → meaning → copywriter(Gemini) → cover-text → gate
```

- **12:12:** все пять шагов. Cover пишет хук + `image-prompt.txt`. Пиксели — Холл / Kie.
- **15:15:** researcher → meaning → copywriter → gate. Cover нет. Картинки нет.
- **21:21:** все пять. Это разбор опроса, не тизер статьи. Cover = хук + промпт. Пиксели не обязательны для PASS.

Параллелей нет. FAIL Gate → вернуть тот шаг, где дыра. Директор дыру не штопает текстом.

## Step records

Каждый сотрудник пишет fragment:

`posts/YYYY-MM-DD-HHMM/swarm/<role>.md`

и строку в `.cursor/posts-handoff.md`.

Без `incident_report:` fragment невалиден. Директор не идёт дальше.

Пиксели Kie **не** нужны, чтобы запись шага считалась сделанной. Dry-run: `python3 scripts/posts_swarm_dryrun.py`.

## written_by

Весь человеческий текст слота штампуется:

```text
written_by: gemini
```

Нет штампа, штамп `director`, штамп `glavred` → Gate FAIL.

## Gate режет (HARD)

1. **Inline Director writing.** Эфирные файлы без fragment copywriter / cover-text, или `written_by` не `gemini`.
2. **Главред как обязательный шаг.** Упоминание Glavred / «можно публиковать» как требуемого этапа в каноне, FOR-AGENTS, policy, `swarm/`, `GATE`.
3. Вода, воронка, лимиты, слово «ловушка» — как в `POSTS.md`.

Скрипт тех же запретов: `python3 scripts/posts_gate_check.py --pack posts/YYYY-MM-DD-HHMM`.

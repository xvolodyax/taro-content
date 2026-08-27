# Посты — рой в одном окне

Ориентир закона — Karuselka (оркестратор → один Task на шаг → fragment).
Это **посты**, не карусель и не блог. Плагин, Kie-пиксели, Instagram publish не переносить.

## Одно окно

Холл поднимает **один** Cloud Agent: `posts-director`.
Сотрудники — foreground Task в том же прогоне, тот же checkout, та же ветка.

Человек видит один run. Не пять окон researcher / meaning / copywriter.

## Cloud fallback (HARD)

В Cloud **нет** `Task(posts-researcher)` и прочих `Task(posts-*)`.

```text
Каждый шаг:
  subagent_type: generalPurpose
  model: gemini-3.7-flash-high
  run_in_background: false
  (environment не передавать)
  prompt: полный текст .cursor/agents/posts-<role>.md
          + путь пакета + слот + вход + запреты
```

Если Task совсем нет:

`❌ БЛОКЕР: среда не поддерживает subagents.`

Директор тогда **не** пишет эфир сам.

## Запрещено

| Действие | Почему |
| --- | --- |
| Директор пишет `tg.html` / debrief / хук | inline writing = FAIL |
| «Я теперь копирайтер» | ломает рой |
| Главред как шаг | качества нет снаружи |
| Ждать «можно публиковать» | Холл публикует после PASS |
| `Task(..., environment="cloud")` | новое окно |
| `/in-cloud`, `/babysit` | субагент вне цепочки |
| `run_in_background: true` | шаг не блокирует родителя |
| Isolated worktree / `best-of-n-runner` | чужой checkout |
| `Task(posts-director)` | оркестратор не субагент |
| Сотрудник вызывает `Task(posts-*)` | вложенный пайплайн |

Параллелей нет. Cover после copywriter, только 12:12 и 21:21.
Пиксели Kie не блокируют запись шага и не блокируют PASS.

## Fragment

`posts/YYYY-MM-DD-HHMM/swarm/<role>.md` + блок в `.cursor/posts-handoff.md`.
Обязательна строка `incident_report:`. Без неё шаг не сдан.

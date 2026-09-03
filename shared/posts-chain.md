# Посты — рой в одном окне

Ориентир спавна — Каруселька (Директор не пишет шаги). Логика слотов — этот канон.
Это **посты**, не блог и не карусель. WordPress / schema / indexer не переносить.

## Одно окно

Холл поднимает **один** Cloud Agent: `posts-director`.
Специалисты — foreground Task в том же прогоне.
Человек видит один run. Не пять окон researcher / meaning / copywriter.

Один агент не делает тему + тезис + пост + хук.

## Спавн

| Среда | Как звать шаг |
| --- | --- |
| Plugin | `Task(posts-researcher)` … `Task(posts-gate)` |
| Cloud | один `Task(generalPurpose)` на шаг + dispatch-prompt |

Cloud-промпт:

```text
python3 scripts/posts_dispatch_prompt.py --role posts-copywriter --package posts/YYYY-MM-DD-1212 --runtime cloud
```

Потом step record: `scripts/posts_step_record.py`.
Контракт: `shared/posts-step-contract.md`.

## Запрещено

| Действие | Почему |
| --- | --- |
| Писать brief / meaning / tg.html / хук в чате Директора | inline = FAIL |
| `Task(..., environment="cloud")` | новое окно (`/in-cloud`) |
| `/in-cloud`, `/babysit`, background Task | цепочка рассыпается |
| `Task(posts-director)` | оркестратор не субагент |
| Специалист вызывает `Task(posts-*)` | вложенный пайплайн |
| Главред / «можно публиковать» | шаг снят |
| Opus / Sonnet / Composer как писатель | `written_by` не gemini |
| Публикация писателем шага | `publish: SKIP`; после PASS — `posts_publish.py`, Холл не публикует |

Параллелей нет. Cover после copywriter, только 12:12 и 21:21 (после заморозки поста).
На 21:21 Meaning нет. Один писатель.

## Модели

- meaning / copywriter / cover-text / gate: `gemini-3.8-flash-high`
- researcher / director: `inherit`
- Если Task опускает `model`, runtime может взять модель окна. Текстовые шаги передавать явно.

# Посты — цепочка в одном окне

Ориентир логики — Excalibur-2 (оркестратор → foreground Task → следующий шаг).
Это **посты**, не блог. Плагин, Setup, WordPress, schema, indexer не переносить.

## Одно окно

Холл поднимает **один** Cloud Agent: `posts-director`.
Специалисты — foreground Task в том же прогоне, тот же checkout, та же ветка.
Результат возвращается Директору. Директор зовёт следующий шаг.

Человек видит один run. Не шесть окон Scout / Writer / Sol.

## Запрещено

| Действие | Почему |
| --- | --- |
| `Task(..., environment="cloud")` | Новое окно и ветка (`/in-cloud`) |
| `/in-cloud`, `/babysit` | Субагент вне цепочки |
| `is_background: true` / `run_in_background: true` | Шаг не блокирует родителя |
| Isolated worktree / `best-of-n-runner` | Чужой checkout |
| `Task(posts-director)` | Оркестратор не субагент |
| Специалист вызывает `Task(posts-*)` | Вложенный пайплайн |
| Один проход «напиши tg/vk/max/ig/yt + промпт» | Ломает смысл → слог → Gate |
| Автозапуск Writer мимо Директора | Нет брифа |

Параллелей нет. Cover после PASS, только 12:12 и 21:21, не рядом с Sol.
Cover = `posts-cover-text`. Не плодить `posts-cover-hook` / `posts-cover-render`.
Слот `alena-0700` в том же окне: Scout(луна) → Writer → Sol → Gate. Cover не звать. Второго Директора нет.

## Как Директор вызывает Task

```text
Scout:
  subagent_type: posts-scout
  model: inherit
  run_in_background: false

Текст (writer / sol / gate / cover-text):
  subagent_type: posts-{writer|sol|gate|cover-text}
  model: gemini-3.7-flash-high
  run_in_background: false
  (environment не передавать)
```

В prompt субагенту: путь пакета, слот, что уже готово, что **не** делать.
Субагент не видит историю родителя.

Если Task опускает `model`, runtime может взять модель окна и перебить YAML.
Текстовые шаги Директор передаёт явно: `gemini-3.7-flash-high`.

На `alena-0700` Cover-шага нет. Scout всё ещё `inherit`: луну считает Cursor, не Холл.

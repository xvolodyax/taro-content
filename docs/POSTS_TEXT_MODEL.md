# Модель текста постов (12:12 / 15:15 / 21:21)

С **2026-09-09** (вечер, Владимир / Холл) слоты **12:12**, **15:15**, **21:21**
и подписи площадок этих постов пишутся только через OpenAI API:

```text
python3 scripts/chat_completions.py --model gpt-5.6-sol
```

Штамп на человеческом тексте:

```text
written_by: openai-api-gpt-5.6-sol
```

`gpt-5.5` / `openai-api-gpt-5.5` на эти слоты **не звать**.
Нет ключа / 401 / модель недоступна — `FAIL`, текст не подменять
(ни Gemini, ни inherit окна, ни Grok, ни Composer, ни gpt-5.5).

## Не этот канон

| Что | Модель |
| --- | --- |
| Статьи / «Магия истории» / Дзен | как было (`gpt-5.5` / Gemini по их канону). Этим скриптом не писать |
| Алёна `alena-0700` | inherit окна. Sol с тела снят (`posts/ALENA.md`) |
| Каруселька | уже Sol — не трогать |
| Рилсы | свой `reels-swarm/model-policy.json` |

Исторические пакеты `posts/YYYY-MM-DD-*` не перештамповывать ради смены id.

Канон роя: [`POSTS.md`](../POSTS.md). Политика: [`shared/posts-model-policy.json`](../shared/posts-model-policy.json).

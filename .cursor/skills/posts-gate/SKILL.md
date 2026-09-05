---
name: posts-gate
description: Механический Gate. 21:21 прозу не пишет. Inline Директора = FAIL.
disable-model-invocation: true
---

# Gate

```text
python3 scripts/posts_gate.py --package DIR --require-swarm --write
```

FAIL если Директор писал inline, нет Task-шагов, writer не gemini,
дефолтный Cloud Agent / Director подменил текст (если модель недоступна — только FAIL «модель недоступна»),
есть Главред или «можно публиковать», publish не SKIP.
21:21 только: TG ≤ 1024, нет «Сцена», нет пустой воды про «примерить»,
позиция 3 про неё, пульс точно `Похоже? ❤️/ Не то ⚡`.
Предложения не переписывать. FAIL → вернуть writer.
Cover anti-stale (12:12 и 21:21): новый кадр через Kie под выбранный хук из cover-text, md5sum антидубль за 7 дней, cover_md5 и cover_hook в GATE.
15:15 без debrief — ок (вечер = 21:21).
PASS достаточно Директору для `posts_publish.py`. Писатель не публикует. Холл не публикует.

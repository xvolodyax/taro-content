---
name: posts-gate
description: Механический и смысловой Gate. Рубрика 21:21. Inline Директора = FAIL.
disable-model-invocation: true
---

# Gate

```text
python3 scripts/posts_gate.py --package DIR --require-swarm --write
```

FAIL если Директор писал inline, нет Task-шагов, writer не gemini,
есть Главред или «можно публиковать», publish не SKIP,
21:21 старой формы (4 совета на варианты), есть «Сцена» / «когда напишет».
15:15 poll-only без debrief — ок, в эфир всё равно не слать.
PASS достаточно Директору для `posts_publish.py`. Писатель не публикует. Холл не публикует.

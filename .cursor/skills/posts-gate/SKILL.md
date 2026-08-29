---
name: posts-gate
description: Механический и смысловой Gate. Inline Директора = FAIL. Главред снят.
disable-model-invocation: true
---

# Gate

```text
python3 scripts/posts_gate.py --package DIR --require-swarm --write
```

FAIL если Директор писал inline, нет Task-шагов, writer не gemini,
есть Главред или «можно публиковать», publish не SKIP.
PASS достаточно Директору для `posts_publish.py`. Писатель не публикует. Холл не публикует.

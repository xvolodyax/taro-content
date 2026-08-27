# Шаблон fragment шага роя

Путь: `posts/YYYY-MM-DD-HHMM/swarm/<role>.md`
Плюс блок в `.cursor/posts-handoff.md`.

```text
=== POSTS-<ROLE> ===
Статус: OK | WARN | FAIL
written_by: gemini
Кратко: ...

Артефакты:
- path/to/file

incident_report: none
```

Без строки `incident_report` fragment невалиден. Директор не идёт дальше.

Пиксели Kie в артефактах не обязательны.

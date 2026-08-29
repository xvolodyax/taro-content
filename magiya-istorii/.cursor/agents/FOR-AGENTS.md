# Магия истории — роли

Канон: [`../../CANON.md`](../../CANON.md).
Контракт: [`../../CONTRACT.md`](../../CONTRACT.md).

Не посты «ТАРО СЕЙЧАС». Не Алёна. Не 12:12 / 15:15 / 21:21.
Не Дзен-боль. Не продажа раскладов. Не Composio.

Одно окно: Директор ведёт цепочку. Специалист — один шаг, не зовёт соседние роли.
Директор сам scout / plot / story / GATE / art **не пишет**.

| # | Роль | Файл | Модель | Task? |
| --- | --- | --- | --- | --- |
| 0 | Директор | `magiya-director.md` | inherit | **нет** |
| 1 | Scout / Wordstat | `magiya-scout.md` | inherit | да, foreground |
| 2 | Plot | `magiya-plot.md` | inherit | да |
| 3 | Writer | `magiya-writer.md` | inherit | да |
| 4 | Gate | `magiya-gate.md` | inherit | да |
| 5 | Art brief | `magiya-art.md` | inherit | да |

Cloud: кастомный `Task(magiya-*)` часто нет. На шаг — `Task(generalPurpose)` и полный текст роли из этого файла.
Plugin: `Task(magiya-scout)` и т.д., если Cursor видит агентов в `magiya-istorii/.cursor/agents/`.

Нет ролей: Publish, Sol площадок, Cover-лого, Главред, Setup.
Пиксели не обязательны. В эфир из этого продукта нельзя.

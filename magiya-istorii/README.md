# Магия истории

Отдельный продукт в `taro-content`. Захватывающие истории про магию, чёрную магию, обряды, духов, колоды, проклятия.

Это **не** посты «ТАРО СЕЙЧАС», не Алёна, не слоты 12:12 / 15:15 / 21:21, не `PUBLISH.md`, не Composio.
Не канал боли и не продажа раскладов. Бот и приложение «ТАРО СЕЙЧАС» сюда не тащить.

Канон: [`CANON.md`](CANON.md).  
Контракт пакета: [`CONTRACT.md`](CONTRACT.md).  
Роли: [`.cursor/agents/FOR-AGENTS.md`](.cursor/agents/FOR-AGENTS.md).  
Ledger: [`LEDGER.md`](LEDGER.md).

## Как запустить Director

1. Открыть **одно** окно Cloud Agent / чат в репо `taro-content`.
2. Главный агент — **`magiya-director`**. Не `Task(magiya-director)`. Не `/in-cloud`. Не `/babysit`.
3. В промпт вставить блок. Дату подставить. Тему за Scout не придумывать.

```text
Собери пакет «Магия истории» на YYYY-MM-DD.
Канон: magiya-istorii/CANON.md. Контракт: magiya-istorii/CONTRACT.md.
Цепочка в этом окне, Director сам тексты не пишет:
Scout/Wordstat → Plot → Writer → Gate → Art brief.
Пакет: magiya-istorii/packages/YYYY-MM-DD-slug/
Env Scout: YANDEX_CLOUD_SEARCH_API_KEY + YANDEX_FOLDER_ID.
Ключ не в лог. PARTIAL не стоп. Угол не самая жирная фраза в H1.
Не публиковать. Пиксели не обязательны.
Посты ТАРО СЕЙЧАС, Алёну, 12:12/15:15/21:21, PUBLISH.md, Composio не трогать.
После PASS верни Холлу: путь пакета, GATE, знаки, kind, угол.
```

4. Дождаться `GATE` = PASS, `story.md` + `meta.json`, `art-brief.md`.
5. Публикацию в соцсети **не** делать. Картинку Холл рисует сам, если нужно.

## Цепочка

```text
Scout (живой Wordstat) → Plot (кто/где/когда/ставка/цена)
→ Writer (8–14 тыс.) → Gate → Art brief (один кадр)
```

| Шаг | Агент | Выход |
| --- | --- | --- |
| 0 | `magiya-director` | папка пакета, вызовы Task |
| 1 | `magiya-scout` | `scout.md` |
| 2 | `magiya-plot` | `plot.md` |
| 3 | `magiya-writer` | `story.md`, `meta.json` |
| 4 | `magiya-gate` | `GATE` |
| 5 | `magiya-art` | `art-brief.md` |

Cloud: на шаг — `Task(generalPurpose)` и текст роли из `.cursor/agents/magiya-*.md`.
Директор inline = FAIL.

## Wordstat

```text
python3 magiya-istorii/scripts/wordstat.py "чёрная магия" "обряд на пороге" "проклятие"
```

Нужны `YANDEX_CLOUD_SEARCH_API_KEY` и `YANDEX_FOLDER_ID`.  
Скрипт не печатает ключ. Нет доступа или часть фраз упала → `PARTIAL`, цепочка идёт дальше.

## Демо

Пакет после первого прогона: см. `packages/` и строку в `LEDGER.md`.
Минимум готового пакета: `story.md` + `meta.json`. В эфир не выкладывать.

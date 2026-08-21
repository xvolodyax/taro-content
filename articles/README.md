# Статьи Дзена

Это **не** посты каналов. Посты живут в `posts/` и идут в слоты 12:12 / 15:15 / 18:18 / 21:21.

Канон пайплайна: [`ARTICLE.md`](ARTICLE.md).  
Бренд: [`brand-brief.md`](brand-brief.md).  
Уже вышедшие заголовки: [`published-titles.md`](published-titles.md).  
Журнал ошибок: [`pipeline-errors.md`](pipeline-errors.md).

## Как хранить одну статью

Одна тема — одна папка:

```text
articles/dzen/YYYY-MM-DD-slug/
  research-brief.md
  title-brief.md
  writer.md
  article.md
  dzen-description.md
  cover-brief.md
  cover.png          # файл 1K на диске, в Дзен грузить файлом
```

Шаблоны копировать из [`templates/`](templates/). Имя папки = дата слота + кириллический запрос латиницей.

Старый одиночный файл `articles/dzen/2026-08-17-chto-delat-esli-on-ne-pishet.md` (PR #1) уже в ledger. Новую тему «он не пишет» / «дата рождения» не брать.

## Слоты (будни)

| Время | Угол | Воронка |
| --- | --- | --- |
| 9:00 | острый запрос | Макс |
| 16:00 | нумерология / персональный | ВК |
| 20:00 | вечерний вопрос | Макс |

Слоты 12:12 / 15:15 — другая машина.

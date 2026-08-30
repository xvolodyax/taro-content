# Магия истории — роли

Канон: [`../../CANON.md`](../../CANON.md).
Контракт: [`../../CONTRACT.md`](../../CONTRACT.md).

Не посты «ТАРО СЕЙЧАС». Не Алёна. Не 12:12 / 15:15 / 21:21.
Не Дзен-боль. Не продажа раскладов. Не Composio.
Не Excalibur-плагин. Не Каруселька.

Одно окно: Директор будит роли. Специалист — один шаг.
Директор сам scout / plot / title / story / clickbait / GATE / art **не пишет**.

## Чей текст (HARD)

Разные роли владеют **разным** текстом. Это нормально.

| Текст | Кто пишет | Кто не трогает |
| --- | --- | --- |
| Тело статьи (`story.md`: проза + триггерный вопрос) | **Writer**, один проход, Gemini 3.7 | Plot, Title, Clickbait, Gate, Art, Director, любой фиксер / копирайтер / «обогатитель» |
| H1 == title | **Title** | Writer, Clickbait, Gate, Plot, Art, Director |
| Overlay кадра 1 | **Clickbait** | Title, Writer, Gate, Plot, Art (Art только рисует готовую строку) |

**Болезнь (убить):** Plot / Gate / Title / Clickbait / фиксер / копирайтер наваливаются на **тело**. Второй проход по прозе запрещён.

Ролей fixer / copywriter / enrichment / Главред по `story.md` **нет**. Не звать. Не выдумывать.

## Цепочка

| # | Роль | Файл | Модель | Task? | Что сдаёт |
| --- | --- | --- | --- | --- | --- |
| 0 | Директор | `magiya-director.md` | `inherit` | **нет** | будит роли, не пишет |
| 1 | Scout / Wordstat | `magiya-scout.md` | `inherit` | да | тема (Wordstat / Дзен / сайт). Историю не пишет |
| 2 | Plot | `magiya-plot.md` | `inherit` | да | необязательные заметки. В статью не пишет. Биты не предписывает |
| 3 | Title | `magiya-title.md` | `gemini-3.7-flash-high` | да | только H1. Тело не правит |
| 4 | Writer | `magiya-writer.md` | `gemini-3.7-flash-high` | да | только тело. Один проход |
| 5 | Gate | `magiya-gate.md` | `inherit` | да | только проверка. Предложения не переписывает |
| 6 | Clickbait | `clickbait.md` | `gemini-3.7-flash-high` | да, после Plot | только overlay кадра 1 |
| 7 | Art | `magiya-art.md` | `gemini-3.7-flash-high` | да, после Clickbait | пиксели / art-brief. Прозу не пишет |
| 8 | Site Publish | `scripts/magiya_site_publish.py` | Python stdlib | скрипт Director | не в этом прогоне, если Холл сказал не публиковать |

Все читаемые текстовые роли (Title, Writer, Clickbait, Art-brief) — строго `gemini-3.7-flash-high`.

Title ≠ Clickbait ≠ Writer.
Clickbait не меняет `title` / `h1` / `story.md`.
Title не меняет `story.md` (тело).
Writer не выдумывает H1 и не пишет overlay.
Art на кадр 1 кладёт **готовую** строку из `clickbait.txt`. Свою не придумывает.
Обложка 16:9 (1K), `Виктория.png`, глаза зелёные с лёгким карим оттенком, микрофон в руке у рта, жирная красная рамка по периметру.
Картинка не валит текст. Лицо Холл не рисует.

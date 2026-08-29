# Публикация слота — рой, не Холл

После `GATE` = PASS Директор сам кладёт эфир через Composio.
Холл **не** публикует и отложку не ставит.

Писатели роя (`researcher` / `meaning` / `copywriter` / `cover-text` / `gate`)
по-прежнему `publish: SKIP` и в Telegram не ходят.

## Как вызвать

```text
python3 scripts/posts_publish.py --package posts/YYYY-MM-DD-1212
python3 scripts/posts_publish.py --package posts/YYYY-MM-DD-1515
python3 scripts/posts_publish.py --package posts/YYYY-MM-DD-2121
python3 scripts/posts_publish.py --package posts/YYYY-MM-DD-alena
```

Опции:

| Флаг | Зачем |
| --- | --- |
| `--dry-run` | план без эфира |
| `--wait` | ждать слот МСК в процессе, потом слать сразу (не отложка Telegram) |
| `--no-live-check` | не смотреть живой канал (ledger всё равно) |
| `--now 2026-08-29T16:00:00+03:00` | тесты / подставить «сейчас» |

Код выхода всегда `0` на SKIP / WAIT / SENT, кроме кривого запуска (нет пакета).

## Env

Ключ в git, логи и чат **не** писать.

| Переменная | Нужна | Если нет |
| --- | --- | --- |
| `COMPOSIO_API_KEY` | да, для TG и IG | SKIP, процесс не падает |
| `POST_IMAGE_URL` | 12:12 / 21:21, публичный HTTPS | SKIP фото-площадок |
| `ALENA_COVER_URL` | alena-0700, публичный HTTPS | SKIP фото Алёны |
| `MAX_BOT_TOKEN` | Макс | Макс не трогаем |
| `MAX_CHAT_ID` | Макс, вместе с токеном | Макс SKIP |

Локальный `cover.png` Composio как файл не принимает: нужен HTTPS URL
в `cover-url.txt`, `package.meta.json image_url` или env.

## Алиасы Composio (не default)

| Alias | Куда |
| --- | --- |
| `telegram-composia` | `@TodayTaro`; на alena-0700 — `@AlenaSafonova_queen` |
| `instagram-ru` | 12:12, картинка+текст |
| `instagram-en` | зарезервирован, этими слотами не шлём |

Default-аккаунт брать **запрещено**, даже если alias пустой в REST.

## Слоты МСК

Без отложки Telegram. Раньше слота не слать. Слот прошёл — сразу.

| Слот | Что уходит | Что не трогать |
| --- | --- | --- |
| **12:12** | TG фото+текст, IG RU фото+текст | ВК, YouTube community |
| **15:15** | только `TELEGRAM_SEND_POLL` | картинка, IG, Макс, ВК, YT |
| **21:21** | TG фото+текст; карта = совет, без «Сцена» | IG, YT, ВК |
| **alena-0700** | 07:00, канал Алёны, рефки как есть | `@TodayTaro`, IG |

Макс (12:12 / 21:21) — только если в env есть `MAX_BOT_TOKEN`.

Живой сегодняшний пост с тем же отпечатком не дублировать.
Статус пишется в `posts/<пакет>/publish.json` и `posts/_publish-ledger.json` (не в git).

Конфиг: [`shared/posts-publish.json`](../shared/posts-publish.json).

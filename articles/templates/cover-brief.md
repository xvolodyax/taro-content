# Cover-brief

Скопировать в `articles/dzen/YYYY-MM-DD-slug/cover-brief.md`.

Приём Хорошева, не его стиль: **лицо бренда + короткий текст смысла на кадре**.  
`cover_hook` ≠ title статьи ≠ карточка Дзена.

```text
topic_id: DZEN-YYYYMMDD-слот
face: victoria | alena | none
cover_hook:            # 2–6 простых русских слов, точная надпись на кадре
scene_hint:            # бытовая сцена кадра одной строкой
forbidden_style: dark table; candles; gothic; magic basement; white hoodie; meme stickers; tape collage; «лох»; quad 2×2; 2K
aspect: 16:9
mode: i2i | t2i
model: gpt-image-2-image-to-image | gpt-image-2-text-to-image
resolution: 1K
ref:                   # обязателен при face ≠ none: images/refs/victoria-1.jpg | victoria-2.jpg | alena-1.jpg | alena-2.jpg
why-her:               # пусто при victoria по умолчанию; для alena — почему её слот / статья про неё
why-2k:                # не заполнять: по умолчанию 1K
file_on_disk: cover.png
prompt:                # английский кадр + точная русская строка cover_hook в кавычках
why:                   # одна русская строка: кто в кадре, какая сцена, какой хук
```

## Как заполнять

- `face: victoria` — по умолчанию. `alena` — только если статья про Алёну или явно её слот. Нет файла в `images/refs/` — `face: none`, человека нет.
- `cover_hook` — 2–6 слов смысла, которые **видны на обложке**. Не пустая атмосфера. Не H1. Не description.
- `scene_hint` — что происходит в кадре (телефон на льне, окно, дневной свет), не «мистика».
- `forbidden_style` — копировать строку выше целиком, не вычёркивать пункты.

## Модель

| Реф | mode | model |
| --- | --- | --- |
| есть, `face` victoria/alena | i2i | Kie.ai `gpt-image-2-image-to-image` |
| нет рефа | t2i | `gpt-image-2-text-to-image`, человека нет |

Разрешение **1K, не 2K**. Плагин Excalibur не ставить.

## Кадр

- светлый современный: окно, лён, стекло, дневной свет
- лицо по рефу, не двойник «по памяти»
- хук на кадре читается за секунду
- не тёмный стол, не свечи, не готика, не «магический подвал»
- не белое худи, не мемные стикеры, не скотч-коллаж, не «лох», не quad 2×2

## После генерации

- файл лежит в папке статьи
- в Дзен Холл грузит **файлом**, никогда `localhost` / `127.0.0.1`

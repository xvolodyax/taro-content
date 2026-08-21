# Cover-brief

Скопировать в `articles/dzen/YYYY-MM-DD-slug/cover-brief.md`.  
Хук обложки отдельно от title и от карточки Дзена.

```text
topic_id: DZEN-YYYYMMDD-слот
hook:                  # 2–8 простых русских слов, ≠ H1
highlight:             # одно слово из hook, если нужно выделить
aspect: 16:9
mode: t2i | i2i
model: gpt-image-2-text-to-image | gpt-image-2-image-to-image
resolution: 1K
ref:                   # только если i2i: images/refs/victoria-1.jpg | alena-1.jpg
who:                   # Виктория | Алёна | никто
why-her:               # зачем лицо; пусто, если кадра без человека
why-2k:                # заполнять только если resolution: 2K
file_on_disk: cover.png
prompt:                # английский, 40–80 слов, один абзац
why:                   # одна русская строка: что в кадре и зачем этой статье
```

## Кадр

- светлый современный: окно, лён, стекло, дневной свет
- одна сцена, одна эмоция, один объект
- карты — мелкая деталь, не весь кадр
- не тёмный стол, не свечи, не готика
- не худи / стикеры «лох» / quad 2×2 (это чужой мем Excalibur)
- в промпте: `no text, no letters, no watermark, no logo`
- лица только с рефом из `images/refs/`; файла нет — `mode: t2i`, человека нет

## После генерации

- файл лежит в папке статьи, не на localhost
- в Дзен Холл грузит **файлом**
- буквы на картинку модель не рисует: хук уходит текстом в Студию, если нужен

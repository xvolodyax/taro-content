---
grid: 2x2
resolution: 2K
pixels: skip
face: pending-ref
overlay_source: clickbait.txt
model: gpt-image-2-5-flare-image-to-image
---

# Art brief (холст 2×2, 2K)

**Пайплайн:** один Kie `createTask`, `resolution: 2K`, сетка 2×2, толстые белые швы. Потом `slice_canvas.py` → `cover.png` + `inline-01`…`03`. Не четыре отдельных 1K.
**Канон:** `docs/CANVAS_2K.md`. Модель: GPT Image 2.5 Flare i2i (`gpt-image-2-5-flare-image-to-image`). Нет рефа — t2i. Не Sunburst, не `gpt-image-2*`.
**Язык:** современный журнал / editorial / reportage, глянец 2020-х.
**Лицо:** только клетка обложки. i2i `magiya-istorii/refs/Виктория.png`. Холл лицо не рисует. Врезки — без лица Вики.
**Микрофон:** DJI Mic Mini Transmitter в руке у рта — только клетка 1.
**Наряд (клетка 1):**
**Сцена и свет:** из `story.md`. В базовый промпт «ночь» не зашивать.
**Куда срезы:** `cover` — hero; `inline-01`…`03` — врезки в тело. Cover в теле не дублировать.

## Клетка 1 / cover (лента)

- Вика + Mic Mini. Картинка, не видео.
- Overlay дословно из `clickbait.txt` (кириллица на пикселях, display). Не title/h1.
- **ЖИРНАЯ красная журнальная рамка только этой клетки.**

## Клетки 2–4 / inline-01…03

Без лица Вики. Без красной рамки. Без кликбейта. Три разных бита сюжета, тот же свет/место.

| Срез | Бит | Кадр (без лица) | Подпись |
| --- | --- | --- | --- |
| cover | обложка | Вика + mic + рамка + overlay | `clickbait.txt` |
| inline-01 |  |  | `caption-01.txt` |
| inline-02 |  |  | `caption-02.txt` |
| inline-03 |  |  | `caption-03.txt` |

Одна генерация холста. Второй холст в прогоне запрещён. Art не валит Writer. Живые пакеты не перерисовывать.

## Промпт (ядро 2×2, 2K)

```text
A cinematic 2x2 photographic contact sheet of 4 equal panels separated by THICK WHITE gutter seams, resolution 2K, one canvas not four images. Panel 1 (top-left, cover): a single woman referenced from one angle of the Victoria sheet (no face morphing): distinct hazel-green eyes, warm blonde hair with darker roots, soft features; stylish 2020s investigative reporter holding a compact black DJI Mic Mini Transmitter in her hand right near her mouth; BOLD THICK RED magazine cover border around THIS PANEL ONLY; high-impact DISPLAY Cyrillic overlay with the clickbait title baked on the pixels. Panels 2 to 4: NO Victoria face, NO red frame, NO clickbait; distinct story-beat editorial photographs of place, object and atmosphere from the same setting and light, optional subtle editorial captions. Thick white gutters must stay sliceable.
```

## Стоп

Не четыре 1K createTask. Не сетка 2×3 / шесть кадров. Не одна 16:9 без врезок (это снято для новых пакетов). Не Алёна. Не лого «ТАРО СЕЙЧАС». Не лицо «по памяти». Не реген живых пакетов.

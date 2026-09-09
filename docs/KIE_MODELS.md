# Kie image models

С **2026-09-09** дефолт для новых генераций — **GPT Image 2.5 Flare**.
Не Sunburst. Старые id `gpt-image-2*` на новые кадры не звать.

| Режим | Kie model id |
| --- | --- |
| Text→Image | `gpt-image-2-5-flare-text-to-image` |
| Image→Image | `gpt-image-2-5-flare-image-to-image` |

Сняты (не для будущих прогонов): `gpt-image-2`, `gpt-image-2-text-to-image`, `gpt-image-2-image-to-image`. Bare `gpt-image-2` как имя движка не писать — только явный t2i или i2i id из таблицы.

## Куда какой id

- Посты 12:12 / 21:21: i2i (реф медальона в `image-prompt.txt`) → `gpt-image-2-5-flare-image-to-image`.
- Статьи Эскалибура и «Магия истории»: i2i (реф Вики / Victoria 33) → `gpt-image-2-5-flare-image-to-image`.
- Text→Image — только если рефа нет; тогда `gpt-image-2-5-flare-text-to-image`.

## Разрешение (HARD 09.09)

| Продукт | Kie `resolution` | Сколько createTask |
| --- | --- | --- |
| Посты 12:12 / 21:21 | **1K**, один кадр | один still |
| Статьи Эскалибура + истории «Магия истории» | **2K**, холст 2×2 | **один** холст, потом срез. Не четыре 1K |
| Каруселька / carousel storyboard | **4K** | как в каноне карусели |

Холст и нарезка: [`CANVAS_2K.md`](CANVAS_2K.md).

Исторические пакеты (`magiya-istorii/packages/2026-08-*` и прошлые `posts/YYYY-MM-DD-*`) не переписывать и не перерисовывать ради смены id или формата.

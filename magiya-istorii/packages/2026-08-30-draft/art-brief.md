---
format: 16:9
resolution: 1K
pixels: skip
face: Виктория.png
overlay_source: clickbait.txt
---

# Art brief (Обложка 16:9, 1K)

**Формат:** одна горизонтальная обложка 16:9, 1K (~1920×1080). Не сетка 2×3, не 6 кадров, не нарезка. Файл `cover.png`.
**Язык:** современный журнал / editorial / reportage cover, глянец 2020-х. Не шаблон нейросети, не открытка, не коллаж.
**Персонаж:** Вика (i2i `magiya-istorii/refs/Виктория.png`, 2 191 823 байт).
**Глаза:** строго зелёные с лёгким карим оттенком (distinct hazel-green: green with a subtle warm brown tint).
**Волосы и лицо:** тёплый блонд с более тёмными корнями, мягкие нежные черты лица (строго по одному якорному ракурсу анфас/3/4 реф-листа, без морфинга и усреднения 12 лиц).
**Микрофон:** компактный чёрный передатчик **DJI Mic Mini Transmitter ВСЕГДА В РУКЕ У РТА** (в руке ведущей прямо перед ртом, говорит как репортёр-расследователь). Не на одежде.
**Наряд:** стильный тёмный тренч / пальто 2020-х (tailored dark structured trench coat), современный чистый журнальный крой (образ ведущей-расследователя, не жертвы).
**Сюжетная сцена пакета и свет:** прихожая типовой квартиры в Кирове у входной двери, рассохшийся сосновый дверной косяк над верхним замком с торчащей тёмной швейной иглой, направленный луч фонарика в полутьме коридора, сдержанный кинематографичный свет прихожей. В базовый промпт слово «ночь» не зашито.
**Окантовка:** ЖИРНАЯ красная журнальная рамка по всему внешнему периметру 16:9. Не снимать.
**Текст на обложке:** только ударный overlay из `clickbait.txt` (акцидентный броский display-шрифт): «Оля нащупала иглу в дверном косяке в Кирове — гость ушёл, а подклад остался». Не снимать. Свой заголовок не выдумывать.
**Размещение в статье:** обложка `cover.png` используется только как титульная обложка материала. В тело статьи ту же картинку повторно не ставить.

## Базовое ядро промпта (Base Prompt Kernel)

```text
A cinematic 16:9 horizontal photographic editorial magazine cover. ONE FRAME ONLY — not a 2x3 grid, not six panels, not a contact sheet. A single woman on scene: distinct hazel-green eyes (green with a subtle warm brown tint), warm blonde hair with darker roots, soft gentle facial features referenced strictly from one angle of the Victoria reference sheet (no face morphing, not a 12-face average). She is a stylish 2020s investigative reporter holding a compact black DJI Mic Mini Transmitter in her hand right near her mouth as she speaks on scene. The frame has a BOLD THICK RED magazine cover border around the entire perimeter and high-impact DISPLAY typography overlay with the clickbait title. 16:9, cinematic lighting, editorial magazine aesthetic.
```

## Полный промпт генерации (Full English Generation Prompt)

```text
A cinematic 16:9 horizontal photographic editorial magazine cover. ONE FRAME ONLY — not a 2x3 grid, not six panels, not a contact sheet. A single woman on scene: distinct hazel-green eyes (green with a subtle warm brown tint), warm blonde hair with darker roots, soft gentle facial features referenced strictly from one angle of the Victoria reference sheet (no face morphing, not a 12-face average). She is a stylish 2020s investigative reporter holding a compact black DJI Mic Mini Transmitter in her hand right near her mouth as she speaks on scene. Wearing a tailored dark structured trench coat with modern minimalist editorial styling. Setting is an apartment entryway hallway in Kirov right next to a weathered pine doorframe above the lock where a dark sewing needle is embedded in the wood, directional smartphone flashlight beam illuminating the door jamb in the dim atmospheric hallway. The frame has a BOLD THICK RED magazine cover border around the entire perimeter and high-impact DISPLAY typography overlay: 'Оля нащупала иглу в дверном косяке в Кирове — гость ушёл, а подклад остался'. 16:9, 1K resolution, cinematic lighting, editorial magazine aesthetic.
```

## Стоп

Не 2×3, не 6 кадров, не нарезка. Жирную красную рамку и кликбейт с этого кадра не снимать. В тело статьи ту же картинку не ставить. Не Алёна. Не лого «ТАРО СЕЙЧАС». Не бот. Не лицо «по памяти». Живые пакеты (домовой, соль) не перерисовывать и не открывать. Пиксели: skip (запустит Директор отдельно один раз). Публикации нет (publish: SKIP).

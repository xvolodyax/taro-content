---
grid: 2x3
pixels: generated
face: Виктория.png
overlay_source: clickbait.txt
overlay_first_line: Настя сыплет соль за шкаф в Омске — крик срезался, а ярость заперта в спальне
mic_position: in_hand_near_mouth
generations: 1
regen: no
writer_fail: no
---

# Art brief

**Холст:** одно полотно 2×3, 6 клеток, белые швы. Не 9, не 12. Не карусель.
**Персонаж:** Вика (i2i по `magiya-istorii/refs/Виктория.png`, 2 191 823 байт). Глаза зелёные с лёгким карим оттенком, тёплый блонд с более тёмными корнями, мягкие нежные черты лица (строго по одному якорному ракурсу анфас/3/4 реф-листа, без морфинга и усреднения 12 лиц).
**Микрофон:** компактный чёрный передатчик **DJI Mic Mini Transmitter ВСЕГДА В РУКЕ У РТА** (в руке ведущей прямо перед ртом, говорит как репортёр-расследователь).
**Наряд:** стильное шерстяное пальто кремового оттенка 2020-х (tailored cream wool coat), современный чистый журнальный крой (один и тот же наряд на всех 6 кадрах, не тёмный жакет домового).
**Сюжетная сцена пакета:** спальня в двухкомнатной панельной квартире на Левом берегу Омска сразу после ссоры, тяжёлый шкаф, осыпающаяся штукатурка, рассыпанная белая соль «Экстра» в пыли у плинтуса, гнетущая атмосфера запертой ярости, приглушённый свет.
**Куда срезы:** `slice-01` — обложка в ленте; `slice-02`…`slice-06` — врезки в тело статьи. В тексте не дублировать 01.

## Кадр 1 (Обложка в ленте)
- **Жирная красная журнальная рамка** по внешнему краю кадра.
- **Display-шрифт (акцидентный броский заголовок, overlay из clickbait.txt):** «Настя сыплет соль за шкаф в Омске — крик срезался, а ярость заперта в спальне».
- **Вика в кадре:** держит DJI Mic Mini в руке у рта, обращаясь к зрителю.

## Кадры 2–6 (Тезисы сюжета на пикселях, журнальный editorial-шрифт, без красной рамки)
- **slice-02:** Текст на кадре: «Аварийный клапан: попытка механически оборвать вибрацию скандала». Вика стоит у входа в спальню, микрофон в руке у рта, на заднем плане комната после ссоры.
- **slice-03:** Текст на кадре: «Мгновенный срез: неестественная тишина вместо долгого остывания гнева». Вика держит микрофон у рта, вслушиваясь в оборвавшийся за стеной шум.
- **slice-04:** Текст на кадре: «Солевой конденсатор: кристаллы запирают ярость, но не гасят ее». Вика указывает в сторону щели за шкафом, где осели крупицы соли, микрофон в руке у рта.
- **slice-05:** Текст на кадре: «Пыль на пальцах: невозможность стереть следы обряда или выйти из комнаты». Вика у шкафа, микрофон в руке у рта, акцент на побелевших подушечках пальцев и осадке обряда.
- **slice-06:** Текст на кадре: «Герметичная ловушка: спальня с запертым осадком чужой обиды». Вика у кровати в полумраке запертой комнаты, микрофон в руке у рта, атмосфера плотного тяжелого холода.

## Базовое ядро промпта (Base Prompt Kernel)
```text
A cinematic 2x3 photographic contact sheet grid of 6 equal panels with white gutter seams. The exact same woman throughout: hazel-green eyes, warm blonde hair with dark roots, soft gentle facial features referenced strictly from single identity anchor of reference sheet (no face morphing). She is a stylish 2020s investigative reporter holding a compact black DJI Mic Mini Transmitter in her hand right near her mouth as she speaks on scene. Same tailored editorial outfit across all panels. Panel 1 has a BOLD THICK RED magazine cover border frame and high-impact DISPLAY typography overlay text. Panels 2 to 6 have NO red borders, featuring distinct story beats with subtle clean editorial text captions embedded in layout. 8k resolution, editorial magazine aesthetic.
```

## Полный промпт генерации (Full English Generation Prompt)
```text
A cinematic 2x3 photographic contact sheet grid of 6 equal panels separated by crisp white gutters. The exact same woman throughout: hazel-green eyes, warm blonde hair with darker roots, soft gentle facial features referenced strictly from single front-facing anchor of Viktoriya reference sheet (no face morphing). She is a stylish 2020s investigative reporter holding a compact black DJI Mic Mini Transmitter in her hand directly in front of her mouth as she speaks on camera. Wearing the same tailored cream wool coat with modern minimalist editorial styling across all 6 panels. Setting is an Omsk apartment bedroom immediately after an intense domestic fight, heavy wardrobe cabinet with a narrow gap against the wall, white Extra salt crystals scattered in dust near baseboard, tense heavy atmosphere with muted ambient room lighting. Panel 1 has a THICK BOLD RED outer magazine cover frame and bold high-impact DISPLAY typography overlay: 'Настя сыплет соль за шкаф в Омске — крик срезался, а ярость заперта в спальне'. Panels 2 to 6 have NO red borders, showing dynamic investigative reporting moments with embedded editorial headline captions: Panel 2 'Аварийный клапан: попытка механически оборвать вибрацию скандала', Panel 3 'Мгновенный срез: неестественная тишина вместо долгого остывания гнева', Panel 4 'Солевой конденсатор: кристаллы запирают ярость, но не гасят ее', Panel 5 'Пыль на пальцах: невозможность стереть следы обряда или выйти из комнаты', Panel 6 'Герметичная ловушка: спальня с запертым осадком чужой обиды'. High-end editorial magazine layout, 8k resolution.
```

## Стоп
Не Алёна. Не лого «ТАРО СЕЙЧАС». Не бот. Не лицо «по памяти». Пиксели: одна генерация Kie gpt-image-2-image-to-image. Публикации нет.

**canvas_note:** кадр 1 — рамка красная, но тоньше «жирной журнальной»; overlay читается. кадры 4 и 6 — сверху затекла чужая строка с соседних клеток. Микрофон в руке у рта на всех 6. Наряд кремовый, один. Реген нет.
**canvas_regen:** no

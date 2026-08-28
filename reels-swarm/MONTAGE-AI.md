# montage-ai.json — схема для Remotion

Машинный монтаж. Один объект на рил. UTF-8, валидный JSON, без markdown-ограждения.

Hall копирует содержимое файла в одну ячейку Google Sheet. Пишет файлы только роль **Монтаж**. Скрипт, caption, вопросы не трогает. Публикации нет.

## Два артефакта на рил

| Файл | Кто читает |
|---|---|
| `montage.md` | человек (раскадровка) |
| `montage-ai.json` | Remotion + ячейка Hall |

Gate **FAIL**, если `montage-ai.json` нет, JSON невалиден, или у бита нет точных `card.text` / `startSec` / `endSec` / `line`.

## Объект

```
version: 1
code: кодовое слово (ПАУЗА … ТАЙНА)
fps: 30
width: 1080
height: 1920
durationSec: 25–35, равно last beat endSec
safe: { bottomPct: 20, cardNotOnFace: true }
music: { name: "Dark Ambient Pad", duckOnSfx: true }
beats: []  // по фразам, не 4 общих блока
```

## Бит

- `id` — порядок с 1
- `line` — дословная реплика из `script.md` этого рила, не пересказ
- `startSec` / `endSec` — смежные, без дыр и наложений; первый `startSec` = 0
- `card.text` — точная строка на экране, коротко, по-русски
- `card.position`: `center-above-face` \| `top-third` (нижние 20% пустые)
- `card.in`: `fade-up` \| `punch` \| `word-sync`
- `card.onWord` — слово из `line`, на котором карточка садится
- `camera.shot`: `close-face` \| `mid-chest` \| `mid-confident`
- `camera.zoomFrom` / `zoomTo`
- `camera.cut`: `punch-in` \| `jump-cut` \| `hold` \| `slow-zoom`
- `sfx.name` только из студийного пака:
  Cinematic Impact, Sub Drop, Air Whoosh Transition, Tension Riser,
  Reverse Cymbal, Downlifter, UI Soft Click, Dark Ambient Pad
- Запрещённый сленг: Low Boom, Boom, whoosh, swoosh, Pop, «хит»

## CTA и язык

- На CTA-бите кодовое слово крупно в `card.text`
- `sfx.name` = `UI Soft Click` на кодовом слове (`onWord`)
- В любой экранной или произносимой строке монтажа: «автоматически пришлю» → «СРАЗУ пришлю»; «в нашем приложении» / «нашем приложении» → «в моём приложении»
- Продаём аудио «Суть – Тень – Вектор» в приложении. Не «3 free bot readings». Слова «Сцена» нет никогда

## Hall

Компактная копия того же JSON (pretty-print) лежит в `reels-swarm/hall-paste/<NN-КОД>.json`. Одна ячейка = один файл целиком.

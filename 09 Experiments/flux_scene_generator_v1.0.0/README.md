# ONYX Flux Scene Generator 0.4

Первая тестовая версия генератора сцен с фиксированными и случайными параметрами.

## Что уже работает

- каждый блок в `scene_config.json` имеет режим `fixed` или `random`;
- поза, руки, локация и композиция объединены в `scene_blueprint`, чтобы не создавать конфликтные сочетания;
- для каждого кадра сохраняются seed, выбранные параметры, итоговый prompt и настройки Flux;
- API-workflow автоматически получает `20 steps`, `896 × 1152`, prompt и seed;
- изображения загружаются из ComfyUI в локальную папку `output`.

## Подготовка

Положите рядом три файла:

1. `scene_generator.py`
2. `scene_config.json`
3. `ONYX_Flux_Scene_Generator_0.3_API.json`

ComfyUI должен быть запущен на `http://127.0.0.1:8188`.

## Первый безопасный тест

Из PowerShell в папке генератора:

```powershell
python scene_generator.py --dry-run --count 3
```

Команда не обращается к ComfyUI и создаёт только три JSON-файла с собранными prompt и seed в папке `output`.

## Первая генерация

```powershell
python scene_generator.py --count 3
```

Результат: три PNG и три одноимённых JSON-файла в папке `output`.

## Фиксированный кадр

В `scene_config.json` установите для нужных блоков `"mode": "fixed"`, а для seed:

```json
"seed_mode": "fixed",
"fixed_seed": 240805001
```

Для случайной серии верните `"seed_mode": "random"` и `"mode": "random"` у нужных параметров.

## Важное замечание об API-файле 0.3

В экспортированном workflow сохранено `28 steps`. Генератор намеренно заменяет это значение на `20`, указанное в `scene_config.json`, поэтому при запуске через скрипт используется подтверждённая рабочая настройка.

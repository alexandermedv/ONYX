# ONYX Flux Scene Generator

Версия: v1.0.0
Статус: стабильная standalone-версия

## Назначение

Flux Scene Generator — модуль ONYX Method для автоматической
генерации исходных фотосцен на базе FLUX.

## Место в пайплайне

Client Profile
↓
Flux Scene Generator
↓
FaceFusion
↓
Postprocessing
↓
Quality Control
↓
Финальное изображение

## Возможности v1.0

- режим Client
- режим Portfolio
- поддержка Client Profile v2
- управление параметрами fixed/random
- 12 Executive-пресетов
- рандомизация одежды
- рандомизация выражения лица
- diversity-контроль без повторов
- уникальный seed для каждого изображения
- сохранение metadata
- интеграция с ComfyUI API
- контроль возраста через prompt

## Известные ограничения

### Растительность на лице

FLUX может генерировать короткую бороду даже при значении
`clean-shaven` в Client Profile.

Профиль и prompt передаются корректно. Ограничение будет
дополнительно проверено после восстановления личности через FaceFusion.
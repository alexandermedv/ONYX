# ONYX Generation Route Policy v1

**Status:** production default policy.

## Default

Для новых production-заказов и generation dry run по умолчанию используется ChatGPT Imagegen через встроенный навык `imagegen`. Референсы, ограничения идентичности, scene plan и QA gate передаются в явном виде для каждой задачи.

## Never-default routes

`PuLID` и `FLUX` никогда не выбираются автоматически как generation route по умолчанию. Их можно использовать только при явном выборе для конкретного эксперимента или заказа и после проверки совместимости и качества.

Наличие workflow, LoRA, старого benchmark или локального runtime не является основанием для автоматического выбора этого маршрута.

## Route selection

1. Проверить текущий order metadata и Reference QA.
2. Использовать ChatGPT Imagegen, если заказ не содержит явного route override.
3. Для identity-sensitive работы передать только approved reference set текущего заказа.
4. До массовой генерации выполнить один технический qualifier и проверить likeness, identity consistency, anatomy, realism и требования сцены.
5. При failure использовать targeted retry в ChatGPT Imagegen. Переход на PuLID или FLUX требует отдельного явного решения и записи причины.

## Scope

Эта политика определяет default generation route. Она не запускает генерацию, не загружает файлы во внешние сервисы и не изменяет Product System, pricing или Collection Book standards.

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

## Selection-first production strategy

Production does not use `2 candidates × every scene` as its default. The default is to generate slightly more than the delivery target, run QA, rank the complete set, and select the strongest coherent collection.

### Signature

- Target delivery: `10 final photos`.
- Default generation budget: `12 production images`.
- Run QA and rank by likeness, realism, anatomy, composition, variety, collection coherence, and intended-use suitability; select the best 10.
- The two lower-ranked images are internal-only or dropped. Regeneration is allowed only when the quality floor prevents assembling 10 strong images.

### Premium

- Target delivery: `20 final photos`.
- Default generation budget: `25 production images`.
- After QA, select the best 20 using the same collection-level criteria; the five lower-ranked images are excluded from delivery.
- Regeneration is allowed only when the quality floor is not met.

The historical `ORD-2026-0001` dry run used 20 candidates for 10 finals (two candidates per scene). That run is preserved as an experimental baseline and is not the production default going forward.

## Wearable accessory guidance

For men's business, lifestyle, and professional scenes, the preferred smartwatch or sport-luxury reference when a watch is appropriate is the **Garmin Forerunner 965**. It must be realistic, correctly scaled and fitted, and visually subordinate to the portrait; use it episodically rather than in every scene.

For women’s Business and Executive series, target a neat, refined business-appropriate manicure in at least about half of final images where hands are clearly visible. When it naturally fits the character and styling, preferably include an **Apple Watch** in one or two final images. Keep it correctly scaled and worn, and visually subordinate. These are styling preferences, not reasons to compromise identity, realism, anatomy, or business coherence; never force a watch or a hand pose into a scene.

## Male business / executive tie anchor

For men's `Business` and `Executive` collections, at least one final image must be a formal business anchor shot with a realistic, neatly tied, conservative tie unless the collection explicitly overrides this rule. The tie should support the premium styling without becoming flashy; the rule applies to one or more anchor frames, not the whole series.

## Final image aspect ratio

Every ONYX collection must define a canonical final aspect ratio. For the current Signature Business product the canonical format is portrait `3:4` (or the closest native Imagegen portrait format). Horizontal images, images requiring letterboxing, and images that materially break the collection format are not eligible for the approved delivery set. Do not use black or neutral bands to force a ratio; content quality alone is insufficient for PASS when the final format is wrong.

## Scope

Эта политика определяет default generation route. Она не запускает генерацию, не загружает файлы во внешние сервисы и не изменяет Product System, pricing или Collection Book standards.

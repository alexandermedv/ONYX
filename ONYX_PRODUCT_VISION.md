# ONYX — Product Vision

## 1. Vision

ONYX — не отдельная AI-модель и не простой генератор изображений. Это цифровая AI-фотостудия и production system: клиент передаёт обычные фотографии, а ONYX производит готовую профессиональную фотосессию.

> Клиент отправляет 3–5 обычных фотографий и получает серию профессиональных изображений без студии, фотографа и сложной работы с генераторами.

ONYX продаёт готовый результат, а не доступ к модели, prompt или workflow.

## 2. Initial product: ONYX Business

Первый MVP-продукт — **ONYX Business**.

- Input: 3–5 reference photos одного взрослого человека.
- Output: 10 готовых профессиональных фотографий с разными ракурсами, business outfits и environments; минимум один full-body кадр; высокая сохранность identity; версии WEB и FULL.

Клиент не выбирает GPT, FLUX, Kandinsky, FaceFusion или LoRA. Это внутренние production backends ONYX.

## 3. Target customer

Первичный B2C-сегмент: специалисты, менеджеры, руководители, предприниматели и люди из IT, consulting, finance и corporate-профессий, которым нужны фотографии для CV, LinkedIn, Telegram, сайта, выступлений и personal brand.

Дальнейшие сегменты: Executive, Personal Brand, Recruiting, Corporate portraits, B2B team photography и recurring content subscription.

## 4. Positioning

Предпочтительное позиционирование — «цифровая фотостудия» и «профессиональная фотосессия из ваших обычных фотографий». Термин «нейрофото» не должен быть главным обещанием commodity-продукта. AI — технология производства, а не продуктовый promise.

## 5. Production architecture

Архитектура должна оставаться model-agnostic:

```text
Reference Intake
→ Reference QA
→ Client / Identity Profile
→ SceneSpec
→ Prompt Compiler
→ Generation Router
→ Candidate Pool
→ Automated QA
→ Ranking
→ Human Review
→ Repair / Regenerate
→ Upscale
→ Final QA
→ Delivery
```

Generation Router в будущем может выбирать large cloud models, local FLUX, Kontext/Klein/Fill, FaceFusion/identity repair, LoRA и региональные или внешние модели. Ни одна конкретная модель не является обязательной частью ONYX.

## 6. Key production principles

### Model agnostic

Модели взаимозаменяемы через adapters.

### SceneSpec first

Сцена описывается структурированно; она не существует только как единый буквальный prompt.

### Model-specific prompt compilation

Одна SceneSpec может компилироваться в разные prompts для GPT, FLUX, Kandinsky и других backends.

### Candidate-based generation

ONYX генерирует несколько candidates и выбирает лучшие, а не считает первый удачный output delivery.

### QA and repair

QA проходит до delivery. Если сильный кадр имеет локальный исправимый дефект, предпочтителен repair, а не полная регенерация.

### Preserve rejected data

Статусы PASS, REPAIR, REGENERATE и REJECT вместе с причинами сохраняются как production/R&D dataset.

### Human in the loop

MVP допускает финальный shortlist и review человеком; полная автоматизация не является предварительным условием запуска.

## 7. Identity policy

Identity fidelity — главная quality dimension. ONYX должен сохранять facial proportions, форму лица, глаза, нос, губы, jawline, лоб, hairline, естественную асимметрию, apparent age, текстуру кожи и характеристики тела.

Отдельно отслеживаются identity, appearance fidelity и beautification drift. Нежелательны заметное омоложение, generic model face, изменение массы тела или facial structure, чрезмерное beautification и потеря характерных особенностей.

## 8. Quality system

QA постепенно включает identity similarity, technical quality, face integrity, hands, naturalness, scene compliance, diversity, blur и duplicate/near-duplicate detection.

Решения: **PASS**, **REPAIR**, **REGENERATE**, **REJECT**. InsightFace — полезный сигнал, но не единственный абсолютный judge; позднее возможен vision-LLM reviewer.

## 9. Unit economics

Production telemetry должна измерять generated candidates, First Pass Yield, Delivery Yield, Cost per Delivery Image, cloud cost, local GPU time, repair/regeneration rate, operator generation/review/retouch time, total operator minutes и gross margin заказа.

> Human operator time может быть дороже GPU cost и должен измеряться обязательно.

Ориентир standard order: target для MVP — не более 30 минут human operator time; позднее — 10–15 минут. Это targets, а не подтверждённые факты.

## 10. Business model

Initial: B2C Business portraits. Future: Executive, Personal Brand, Corporate, Teams, Recruiting, subscriptions и visual content factory.

LoRA не обязательна для mass-production single order. Она остаётся VIP/Premium option, R&D и потенциальной технологией recurring/high-LTV клиентов. Photo-to-video и short motion clips рассматриваются как upsell и не блокируют MVP.

## 11. Competitive moat

Moat ONYX — не отдельная модель, а накопленная production system:

- Scene library и structured SceneSpecs;
- Prompt Compiler и Generation Router;
- identity pipeline, QA/ranker и repair loop;
- production telemetry и PASS/REJECT dataset;
- production UX и repeatable delivery workflow.

## 12. R&D policy

R&D не блокирует launch. Новая модель или технология попадает в production только если benchmark показывает улучшение хотя бы одного существенного параметра: quality, identity, delivery yield, cost, speed, operator time или reproducibility.

Примеры R&D: mini-LoRA 3/5/10, PuLID, FLUX Kontext/Klein, Kandinsky, cloud models, Chinese/Russian alternatives и video generation.

## 13. Roadmap

### P0 — blocks launch

- Product Spec, Reference Intake и Business Scene Pack;
- P01 benchmark и full dry-run;
- cost/time/yield measurement;
- initial portfolio и Avito/test launch.

### P1 — improves production

- candidate manifest, automated QA и LLM reviewer;
- adaptive generation, repair routing и delivery builder.

### P2 — R&D

- mini-LoRA, cloud benchmark, Kandinsky, Kontext/Klein variations, video и regional models.

### P3 — scale

- website, payments, customer portal, order DB, automated intake, B2B и subscription.

## 14. Out of scope for MVP

MVP не требует full automation, идеального сайта, mobile app, CRM, payment automation, Kubernetes, сложной database, собственной video-модели, завершения всех LoRA/external-model исследований или нулевого human review.

See also: [MVP v0.1 Definition of Done](ONYX_MVP_V0_1.md).

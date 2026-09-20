# ONYX Client Intake Pack v1

Этот пакет помогает собрать только ту информацию, которая влияет на результат съёмки. Его можно отправить клиенту как набор документов или перенести поля в форму.

## Состав

```text
Intake/
├── README.md
├── ONYX_REFERENCE_GUIDE_v1.md
├── ONYX_SIGNATURE_INTAKE_v1.md
├── ONYX_BOUDOIR_SIGNATURE_INTAKE_v1.md
├── ONYX_PREMIUM_CREATIVE_PROFILE_v1.md
├── ONYX_CONSENT_AND_PRIVACY_v1.md
├── ONYX_DATA_RETENTION_AND_DELETION_v1.md
├── ONYX_REFERENCE_QA_STANDARD_v1.md
└── schemas/
    ├── intake_v1.schema.yaml
    ├── example_portrait.yaml
    ├── example_signature.yaml
    └── example_premium.yaml
```

## Как использовать

1. Отправьте каждому клиенту [руководство по фотографиям](ONYX_REFERENCE_GUIDE_v1.md) и [согласия](ONYX_CONSENT_AND_PRIVACY_v1.md).
2. Для **Portrait** соберите только короткий набор полей из схемы: имя для отображения, номер заказа или контакт, выбранную коллекцию, назначение, стиль, референсы, пожелания и согласия.
3. Для **Signature** заполните [короткую анкету](ONYX_SIGNATURE_INTAKE_v1.md). Для **Boudoir** дополнительно заполните [Boudoir Signature intake](ONYX_BOUDOIR_SIGNATURE_INTAKE_v1.md); все Boudoir-specific поля и согласия обязательны.
   Для коллекции **Boudoir** дополнительно обязательны поля из [Boudoir Signature intake](ONYX_BOUDOIR_SIGNATURE_INTAKE_v1.md), включая границы образа, возраст и отдельные согласия.
4. Для **Premium** заполните [Creative Profile](ONYX_PREMIUM_CREATIVE_PROFILE_v1.md), затем перенесите согласованный профиль в Concept Card. До массового производства концепция должна быть одобрена.
5. Внутренний специалист проверяет референсы по [стандарту QA](ONYX_REFERENCE_QA_STANDARD_v1.md) и фиксирует результат в поле `reference_qa_status`.

## Signature и Premium

| Уровень | Что заполняет клиент | Зачем |
|---|---|---|
| Signature | Короткая анкета: цель, стиль, важные особенности внешности, одежда и то, чего следует избегать. | Получить точный и естественный результат без длинного брифа. |
| Premium | Creative Profile: образ, приоритеты, среда, гардероб, настроение и индивидуальные пожелания. | Согласовать творческое направление до подготовки Concept Card. |

Вопросы должны касаться только результата. Не просите клиента описывать себя сверх того, что поможет создать его образ.

## Язык и границы

Клиентские документы написаны простым, спокойным языком: без технических терминов, медицинских оценок и обещаний, которых нет в сервисе. Примеры в `schemas/` демонстрационные и не содержат реальных данных.

## Машиночитаемый формат

[Схема intake_v1.3](schemas/intake_v1.schema.yaml) описывает канонические поля, подписи, типы, обязательность и контролируемые значения. Boudoir-specific поля обязательны для `collection: BOUDOIR`; они являются источником для формы, ручного заполнения и передачи данных в производство. Примеры показывают минимально достаточное заполнение для каждого продукта.


## Commercial freeze, 2026-09-20

[Product System](../../Product_Standards/ONYX_PRODUCT_SYSTEM.md) governs prices/scope. Portrait is one finished professional portrait; Signature/Premium use one main Collection with usually 2–3/4–6 Concepts. Confirm references, feasible scope and capacity before 100% prepayment. A paid order never implies publication consent.

For all tiers 4–8 useful references is guidance only; the quality-based Reference Guide controls sufficiency. `PORTRAIT` is current; `PREVIEW` and `example_preview.yaml` are legacy-only, SUPERSEDED and not for new intake. Existing Boudoir fields/consent requirements remain intact. Image retention and manual deletion follow [ONYX_DATA_RETENTION_AND_DELETION_v1](ONYX_DATA_RETENTION_AND_DELETION_v1.md); the schema needs no extra intake fields.

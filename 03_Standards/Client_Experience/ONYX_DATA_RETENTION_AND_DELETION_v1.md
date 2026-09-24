# ONYX Client Data Retention & Deletion v1

**Status:** CURRENT / soft-launch operational policy  
**Effective:** 2026-09-21  
**Commercial source:** [ONYX Commercial Product System v1](../Product/ONYX_PRODUCT_SYSTEM.md)

This operational policy applies to orders accepted from its effective date. For an existing open order, explain the rule at the next client contact and apply it going forward without shortening a specifically promised period; do not revive closed orders or retroactively change an agreed term without the client's agreement. It supplements, and does not weaken, the client's existing consent or any stricter applicable privacy requirement. It does not promise deletion from systems outside ONYX's control.

## Production image materials

Reference images; candidate generations; working images; repair intermediates; production working files; and retained copies of final images are stored in the active ONYX production workspace only as needed to perform the order and its agreed follow-up.

Retention ends **30 calendar days after order closure (`CLOSED`)**. Record the closure timestamp with timezone as `order_closed_at`; calculate `retention_until` by adding 30 calendar days in that order timezone. The deletion task is due at or before `retention_until`. For an order closed on 2026-09-21 at 14:00 +03:00, deletion is due by 2026-10-21 at 14:00 +03:00. Closure is recorded only after delivery or an agreed cancellation/refund resolution; a failed order is not reported as successfully delivered.

This period supports included corrections, delivery issue resolution, limited re-delivery and production incident review. ONYX deletes covered image materials from active production storage through the available manual process after this period. Where an open correction, complaint, dispute or incident still requires particular files, document the specific hold, reason, owner and next review date; retain only the necessary items and delete them once the hold ends. A hold does not silently restart or extend the default retention clock for every asset.

Backups, caches, third-party generation/payment services and other systems outside the verified ONYX deletion process may have separate handling. Do not claim immediate or universal erasure from those systems. Before sending material to any external processor, communicate the applicable processing limits and use only an authorized route. No new external service or retention promise is created here.

## Early deletion request

Log the request date and order ID. If the order is closed and no correction, delivery issue, complaint, dispute or incident requires the assets, run the deletion checklist promptly. If there is a specific necessary hold, explain which category must remain and why, restrict access, set a review date and delete the rest. Do not retain images merely to support possible future upgrades or analytics.

Separate client image assets from minimal order, transaction and consent evidence. Delete client image assets when eligible. Preserve only minimal business records that are operationally necessary or must be retained under a confirmed applicable requirement. This policy sets **no fixed retention term** for accounting/payment records; do not invent one. Keep access restricted and avoid copying client images into records.

## Marketing permission

Buying an ONYX product does not grant permission to publish references, generated finals, before/after examples, a Collection Book, a client's name, testimonial or other order material in a portfolio, Avito listing, website, social media or advertising. Obtain the separately applicable explicit permission recorded by the existing Consent & Privacy policy before publication. Keep publication within the permission actually given and the approved asset scope. `DENIED`, `NOT_ASKED`, missing or unclear consent means do not publish.

Refusing marketing permission does not change price, quality or access to the service. Synthetic portfolio characters remain governed by their own documented provenance and approval.

## Minimal order record

After image deletion, retain only what is needed to establish order handling, subject to stricter existing requirements:

- Order ID and product;
- order dates and current/resolution status;
- amount charged and whether payment/refund occurred;
- consent status and when it was recorded;
- minimal operational QA and correction outcome;
- anonymized production metrics where useful.

Do not keep a client's name, contact details, references, image links, prompts or source files in an analytics record without a specific operational need. Keep any required order/accounting evidence separate from deleted image assets and restrict access.

## Manual deletion checklist

The operator completes this checklist; no automatic deletion is implemented.

1. Find orders whose `retention_until` is due or earlier eligible early-deletion requests.
2. Confirm the order is closed and check open corrections, delivery issues, complaints, disputes and incidents. Record any specific asset hold, reason, owner and review date.
3. Keep only allowed minimal order/transaction/consent records; remove unnecessary personal information from analytics copies.
4. Delete eligible references, candidates, working images, repair intermediates, production files and retained final copies from active production storage. Record any unavailable external/backup copy separately without claiming it was erased.
5. Check that no client JPEG/PNG or other image asset was added to Git. Remove a confirmed accidental image from the worktree/index using the approved incident procedure; never silently erase unrelated user work.
6. Record `deletion_status` (`PENDING`, `PARTIAL_EXTERNAL_LIMITATION`, `HOLD`, `COMPLETE`), `deleted_at` when complete, operator and exception notes in restricted order metadata.
7. Leave separately authorized marketing assets in their approved marketing location only while that permission remains applicable; these are not order-working copies. If permission is withdrawn or unclear, pause publication and follow the consent record's withdrawal procedure.

Review this policy when the storage/deletion tools or external processors change. Any stricter established privacy requirement takes precedence.

## Short client-facing wording

> Сначала мы бесплатно посмотрим ваши фотографии и подтвердим, что заказ можно выполнить. После согласования состава и стоимости нужна полная предоплата. Срочную дату подтвердим заранее. Технические ошибки ONYX исправим бесплатно. В Signature включён один раунд пожеланий к готовым фото, в Premium — два. Если после разумных попыток мы не сможем подготовить подходящий результат, вернём оплату за невыполненный заказ. Рабочие материалы и копии готовых фотографий хранятся до 30 календарных дней после закрытия заказа; после завершения необходимых исправлений можно попросить удалить их раньше. Внешние сервисы и резервные копии могут удаляться по отдельным правилам. Мы не публикуем ваши фотографии, имя, фотокнигу или отзыв без отдельного разрешения. Отказ от публикации не меняет цену, качество или возможность заказать услугу.

Use this summary in Avito/messages with the product-specific correction count; explain any agreed exception before taking payment. Do not describe the 30-day period as an accounting-record retention period or guarantee erasure from external services.

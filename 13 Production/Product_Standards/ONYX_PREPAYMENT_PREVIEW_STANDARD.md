# ONYX Prepayment Preview Standard v1

До оплаты клиент получает фирменный preview, а не технический черновик.

- Canvas: 1080 × 1350 px, full width photo, без боковых полей.
- Нижний footer: 230 px, каменная onyx-текстура и утверждённый lockup `BUSINESS COLLECTION / CLIENT PREVIEW`.
- Фото сохраняет голову и лицо; нижняя часть может уходить под footer.
- Поверх фото размещается небольшой полупрозрачный watermark `ONYX / PRIVATE PREVIEW / ORDER <ID>` без чёрной плашки и без перекрытия лица.
- В footer или рядом с watermark указывается ID заказа.
- Preview экспортируется в уменьшенном размере; paid delivery содержит clean JPEG и master без watermark.
- Нельзя отправлять preview без watermark и нельзя использовать watermark, который можно легко обрезать.
- Подпись `PORTFOLIO PREVIEW` используется только для портфолио и запрещена в клиентской выдаче.
- Папка `00_PREPAYMENT_PREVIEW` располагается рядом с тремя оплаченными наборами, но не включается в оплачиваемые ZIP-архивы.

### Approved watermark treatment v1.1

- Use five repeated transparent lockups per image.
- Each lockup contains the monogram incision, ONYX, and PRIVATE PREVIEW with the order ID handled by the delivery manifest.
- One lockup may lightly cross the face so the mark cannot be removed by a simple crop.
- No opaque panel, black badge, or high-contrast central banner is allowed.


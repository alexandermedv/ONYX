# ONYX Price Book v1

**Status:** launch pricing framework. Client-facing prices are active launch prices; internal cost fields are intentionally unfilled until real orders are measured.

## Client-facing launch prices

| Product | Total product price, RUB | Customer wording |
| --- | ---: | --- |
| ONYX Preview | 900 | Personal test frame ONYX |
| ONYX Signature | 3,000 | Personal photoshoot in a chosen collection |
| ONYX Premium | 5,000 | Personalized visual story |

## Preview upgrade pricing

Preview payment is credited in full toward one subsequent Signature or Premium purchase.

| Upgrade | Total product price, RUB | Preview credit, RUB | Remaining amount after Preview upgrade, RUB |
| --- | ---: | ---: | ---: |
| Preview → Signature | 3,000 | 900 | 2,100 |
| Preview → Premium | 5,000 | 900 | 4,100 |

Always show both the total product price and the remaining amount after Preview upgrade. Do not call the remaining amount the price of Signature or Premium.

## Internal pricing fields — TBD after production tests

| Field | Definition | Status |
| --- | --- | --- |
| `inference_cost` | Direct generation cost per order | TBD |
| `manual_minutes` | Measured human production time | TBD |
| `repair_cost` | Cost of repair/regeneration work | TBD |
| `motion_cost` | Direct Motion cost for Premium | TBD |
| `delivery_cost` | Packaging, storage and delivery cost | TBD |
| `total_variable_cost` | Sum of variable costs | TBD |
| `effective_hourly_margin` | Margin after measured manual time | TBD |
| `gross_margin` | Revenue less variable cost | TBD |

## Payment policy — OWNER DECISION REQUIRED

The following are framework fields only and are not customer terms until approved by the owner:

- payment model and timing of prepayment;
- cancellation treatment;
- refund conditions;
- outcome when production cannot pass quality requirements;
- expiry or transferability of a Preview credit.

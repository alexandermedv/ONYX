# ONYX Launch KPI Framework v1

CURRENT — 2026-09-20. [Commercial authority](ONYX_PRODUCT_SYSTEM.md). Schema/manual measurement only; no collection automation has been implemented.

Use [launch_kpi_v1.yaml](launch_kpi_v1.yaml) per order and reporting period. Unknown values are null, never invented zero. Store order IDs without client names/source photos/private URLs. Owner/operator updates events and measured costs; review weekly and at 10 unique paid orders.

| Area | Required measures |
|---|---|
| Funnel | ad impressions, ad views, inquiries, qualified leads, intake started/completed, references accepted, paid orders, inquiry → payment conversion |
| Product mix | Portrait, Signature, Premium, Repair orders; Priority and Express attachment/order counts |
| Upsell | Additional Final Images, Concepts, Correction Rounds; Portrait → Signature and Signature → Premium upgrade rates; add-on attachment rate |
| Revenue | total revenue, average order value, revenue per product, add-ons and upgrades separately |
| Production | candidate generations, regeneration rate, technical reject rate, correction requests, operator minutes, production time, elapsed delivery time, agreed delivery SLA and cost per order when measurable |
| Quality | delivered orders, satisfaction, refund requests/rate, repeat purchase, Additional Collection interest, complaint reasons |

Inquiry → payment = unique converted inquiries / unique inquiries in the defined cohort. AOV = recognized order revenue / unique paid orders; include add-ons/upgrades once and report refunds separately as net revenue adjustments. Product revenue uses line items; upgrade revenue is incremental cash, not a second full tier charge. Attribution and reporting period must be explicit.

Upgrade rate = eligible source-tier orders upgraded / eligible source-tier orders whose 7-day window has closed. Track unavailable-context exclusions separately. Add-on attachment = paid orders with at least one add-on / paid orders. Regeneration rate = regeneration attempts / all candidate attempts; technical reject rate = technically rejected evaluated candidates / evaluated candidates. Refund rate = orders with completed refund / paid orders in the same cohort. Zero denominators produce null.

SLA adherence compares actual delivery timestamp with the explicitly agreed deadline. Production duration and elapsed delivery time are different: the latter includes waiting. Correction requests track QA defects separately from subjective rounds. Operator minutes are measured active work, not agent elapsed wall time.

Portrait economics: collect operator minutes, generation attempts, actual generation/API costs when applicable, correction frequency and upgrade conversion. Evaluate standalone contribution and acquisition value after real orders; keep the 1000-RUB frozen price until the authorized review/exception process.

At **10 PAID ORDERS**, run **ONYX Product & Pricing Review v1.1** across economics, deliverability, quality, customer confusion and scope. Do not count upgrade/add-on transactions as new orders or assume sample orders were paid.

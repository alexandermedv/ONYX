# ONYX Boudoir Signature Intake

Please answer each field before production. Boudoir is an adult-only, tasteful, non-explicit editorial collection.

- `sensuality_level`: NATURAL, SUBTLE, ELEVATED or MAX_NON_EXPLICIT.
- `clothing_level`: FULL_COVERAGE, MODERATE or MINIMAL.
- `preferred_wardrobe_types`: choose or describe garments (for example lingerie, silk robe, slip dress, oversized shirt).
- `preferred_coverage`: FULL_COVERAGE, IMPLIED_TASTEFUL or OTHER. ONYX does not create explicit nudity.
- Explicit wardrobe permissions: `lingerie_allowed`, `bodysuit_allowed`, `silk_robe_allowed`, `sheer_layers_allowed`, `implied_nudity_allowed`, and `strategic_coverage_required`.
- Hard boundaries: `explicit_nudity: false`; `sexual_activity: false`.
- `mood`: words describing the intended impression.
- `lighting_preference`: preferred light and atmosphere.
- `intended_use`: intended use of the collection.
- `must_avoid`: poses, garments, edits or other content to avoid.
- `service_processing_consent`: GRANTED or DENIED for this order. Required GRANTED before processing.
- `reference_reuse_consent`: GRANTED or DENIED if references from another order will be reused.
- `adult_confirmation`: CONFIRMED_18_PLUS is required before a Boudoir order can start.
- `portfolio_use_consent`: GRANTED, NOT_GRANTED or NOT_ASKED. Separate from processing consent; default is NOT_GRANTED.

## Production boundary

Sensual, intimate editorial photography with owner-approved coverage and wardrobe preferences. Minimal clothing, lingerie, bodysuits, sheer layers, and implied coverage may be approved while remaining non-explicit and strategically covered. No explicit nudity or sexual activity.

An Imagegen route refusal must not silently lower the approved sensuality or coverage. Permit at most one compliant rewrite that preserves the same creative intent and approximate coverage. Do not substitute fully clothed fashion/lifestyle styling unless it is an approved scene. If still blocked, record `ROUTE_BLOCKED` and stop for owner direction.

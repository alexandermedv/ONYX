# Asset Rights Matrix

Checked 2026-09-21 against the explicit owner authorization, P02 persona record, source inventory and production export manifest.

| Persona / group | Collection | Synthetic / real | Approval scope | Safe for this Avito pack |
|---|---|---|---|---|
| P02 / Anna | Business A01–A10 only | Synthetic persona | `AVITO_LAUNCH_V1` | YES |
| P02 / Anna | Exact canonical reference `P02_REF03.png` only | Synthetic persona / identity v1 | `AVITO_LAUNCH_V1_BEFORE_AFTER` | YES — Before card only |
| P01 | Any | Not established here | Not approved | NO |
| P03 | Any | Not established here | Not approved | NO |
| P02 | Lifestyle / Boudoir | Outside this decision | Not approved | NO |
| Client / Orders assets | Any | Sensitive client material | Not approved | NO |
| Client Collection Books / delivery | Any | Sensitive client material | Not approved | NO |

## Approved file-level inventory

All paths resolve below `13 Production/Portfolio/P02/Business_V1/final_source_resolution/`.

| ID | File | Role | SHA-256 | Safe for Avito |
|---|---|---|---|---|
| A01 | `ONYX_P02_BUSINESS_01_HERO.jpg` | HERO | `ffcd2a6e021d4edc4e1fd31159ae314ecde6097ea8610267ea86b7fe24c05162` | YES |
| A02 | `ONYX_P02_BUSINESS_02_CLOSE.jpg` | CLOSE | `a8c54ee3f73541d513f19e89c84beb05e319f33e0c40edbc636e11c335387582` | YES |
| A03 | `ONYX_P02_BUSINESS_03_WAIST.jpg` | WAIST | `0e984d2851d5e3d99f4ff97906dbcfe748d27482eec4aa1280bf251738e23479` | YES |
| A04 | `ONYX_P02_BUSINESS_04_SEATED.jpg` | SEATED | `c51335f9dd689e77d0169be643b7d721fd443c23487b51c8d8bbb06ff1c0ddc3` | YES |
| A05 | `ONYX_P02_BUSINESS_05_ENVIRONMENT.jpg` | ENVIRONMENT | `e5fc685dd0d6859f7afeaa31f85dab2659535dd7ac58f7aea6c368ecb68157c0` | YES |
| A06 | `ONYX_P02_BUSINESS_06_ACTION.jpg` | ACTION | `f6c071d10147c4187192b2cf6274f5366f53b15fc07cbf6b3953b8d748f3a1c8` | YES |
| A07 | `ONYX_P02_BUSINESS_07_3Q_BODY.jpg` | 3Q BODY | `ced65a4bab43cdeadd2406321eb2c1fd8a63971081f58288c39663d35c6ace58` | YES |
| A08 | `ONYX_P02_BUSINESS_08_FULL_BODY.jpg` | FULL BODY | `6cc8ec0317a48b54fd5c48d9d7a515f29f1b8fcfc0ee5cd53ba005f87732a425` | YES |
| A09 | `ONYX_P02_BUSINESS_09_MOOD.jpg` | MOOD / WORKSPACE | `aa84f1f2f61e125cd6b91fbbb8095a529a1408ead5b4dd830298be8a91c746fd` | YES |
| A10 | `ONYX_P02_BUSINESS_10_EDITORIAL.jpg` | EDITORIAL | `d918c5e894d5a6f8a0b191e1d78db72f03d3a30e4be98db4797e60c99261f6f5` | YES |

## Revision v2 Before → After reference

| ID | Exact source | Role | SHA-256 | Safe for Avito |
|---|---|---|---|---|
| B01 | `09 Experiments/identity_benchmark_v1/P02_F30_Lifestyle/01_references/P02_REF03.png` | BEFORE / ordinary synthetic reference | `23fb0883218085354fe2de85d92d2641916501ac41e754735892babb10a004c2` | YES — revision v2 comparison only |

`identity_manifest.yaml` and `references_metadata.yaml` identify B01 as a canonical asset of `P02_F30_Lifestyle`, identity version 1, with `synthetic_identity: true`. The owner permission is exact-file only; REF01, REF02, REF04 and REF05 are not approved by implication.

## Scope enforcement

The P02 source inventory records the five requested approval fields, the exact ten-path Business allowlist, a separate exact REF03 approval object, `unlisted_assets_approved: false` and `unlisted_references_approved: false`. Working copies reproduce the same source hashes. No permission is inferred for neighboring files, folders or channels.

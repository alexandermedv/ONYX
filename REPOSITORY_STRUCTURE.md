# ONYX Repository Structure

**Status:** ACTIVE
**Version:** 1.0
**Date:** 2026-09-24

## Canonical structure

```text
ONYX/
├─ 01_Characters/          synthetic identities and character sessions
├─ 02_Marketing/           shared ONYX campaigns and channel exports
├─ 03_Standards/           stable brand, product and service rules
├─ 04_Templates/           reusable generic templates
├─ 09 Experiments/         immutable R&D evidence and benchmarks
├─ engine/                 runtime, providers and production automation
├─ comfyui-workflows/      versioned workflow definitions
├─ config/                 non-secret repository configuration
├─ docs/
│  ├─ Decisions/           architecture decision records
│  └─ Knowledge_Base/      historical and supporting project notes
├─ tests/                  automated verification
└─ Archive/                explicitly retired or historical material

D:\AI\ONYX_Clients/       real client data and orders, outside Git
```

`13 Production/` is a temporary legacy migration root. It is not authoritative. It remains only because active modified and untracked work must be preserved until each package is closed and migrated.

## Authority rules

| Entity | Authoritative location | Rule |
| --- | --- | --- |
| Brand rules and approved visual identity | `03_Standards/Brand/` | Logo, watermark, typography policy and brand guidelines use one canonical set here. |
| Synthetic character | `01_Characters/<ID>/` | Master, references, identity manifest and character-specific sessions stay together. |
| Portfolio result | `01_Characters/<ID>/02_Sessions/<Collection>/02_Final/` | A portfolio result is the approved final view of a character session; no second top-level copy is created. |
| Shared marketing | `02_Marketing/` | Campaign compositions and channel exports may reference character finals. |
| Product and service rules | `03_Standards/Product/` and related standard domains | Pricing, QA, service and client-experience rules are stable standards. |
| Reusable template | `04_Templates/` | Templates contain no personal client data. |
| Production execution | `engine/production/`, `engine/runtime/`, `comfyui-workflows/` | Execution code and workflows do not own Brand, Character, Marketing or Client content. |
| Experiment | `09 Experiments/` | R&D evidence remains historical and is promoted through explicit manifests. |
| Real client | `D:\AI\ONYX_Clients/<CL-ID>/` | Client media, intake, order state, QA and delivery never belong in Git. |
| Historical documentation | `docs/Knowledge_Base/` | Supporting notes are not a second production authority. |
| Architectural decisions | `docs/Decisions/` | ADRs record accepted structural decisions. |

## What must not be duplicated

- Character masters and reference sets outside `01_Characters/<ID>/01_Identity/`.
- Portfolio source photographs inside a marketing package.
- Live client data, client orders or private media anywhere in the repository.
- Approved logos or watermark masters in `assets/`, Marketing or execution folders.
- Stable product rules in scripts, samples or campaign folders.
- Experiment outputs represented as production-approved without a promotion record.

## Character, Portfolio and Marketing

`Characters` owns the identity and the complete synthetic session. `Portfolio` is a role of approved session finals, represented inside that character package. `Marketing` owns the way ONYX presents and sells those results: layouts, campaign copy and channel-specific exports. A marketing asset may depend on a character final but does not become its source of truth.

The derivative chain is:

```text
01_Characters/<ID>/.../02_Final/source
  -> character-specific branded derivative when required
  -> 02_Marketing/<Channel>/<Campaign>/export
```

Every derivative records its source path or source identifier in a manifest. Marketing packages do not keep undocumented `source_copy` folders.

## Adding content

### New synthetic character

Create `01_Characters/<ID>/01_Identity/` and an identity manifest. Add sessions below `02_Sessions/`. Do not copy the identity into Production, Portfolio or Marketing.

### New client

Create the client only below `D:\AI\ONYX_Clients`. Use repository schemas from `04_Templates/`; never copy completed intake or client photographs back into Git.

### New marketing campaign

Create it below `02_Marketing/<Channel>/`. Record provenance to canonical character finals and separate editable master assets from final channel exports.

### New product or policy

Add the stable rule to the appropriate domain under `03_Standards/`. Add a reusable input or output scaffold to `04_Templates/`. Runtime implementation belongs in `engine/`.

### New experiment

Create a self-contained, versioned folder under `09 Experiments/`. Preserve configuration, seeds, manifests and evaluation results. Promotion requires QA and an explicit production decision; experiment evidence is not rewritten during promotion.

## Naming

- Character IDs use `P01`, `P02`, `P03`, and so on.
- Client IDs use `CL-XXXX` only outside the repository.
- Order IDs use `ORD-YYYY-NNNN` only outside the repository or in generic examples with placeholder data.
- Collections use a semantic name plus version, for example `Business_v1`.
- Numbering inside a package may express lifecycle order such as `01_Source`, `02_Final`, `03_Branded`.
- Top-level numbering is reserved for the four canonical content domains and the preserved `09 Experiments` R&D root.

## Migration safety

Modified or untracked legacy content is `DEFERRED_WIP`. It stays in place until its owner closes the work and its destination, references and SHA256 integrity can be verified. A legacy copy is never treated as authoritative merely because it still exists.

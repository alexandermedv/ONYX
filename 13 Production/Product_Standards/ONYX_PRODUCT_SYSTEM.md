# ONYX Product System v1

**Status:** production launch standard.
**Scope:** product architecture and customer value; implementation, prices and service operations are defined by the linked standards.

## Positioning

ONYX is not a service for generating isolated AI images. Its core product is a **personal virtual photoshoot**, designed, selected, refined and delivered as a finished visual collection.

Technology is not the customer value proposition. The value is identity consistency, creative direction, diversity of the series, selection, quality control, regeneration and repair, retouch and enhancement, upscale, curator-style selection, Collection Book and a convenient delivery package.

## Launch product matrix

| Product | Customer outcome | Price, RUB | Final photographs | Creative model | Collection Book | Motion | Revisions |
| --- | --- | ---: | ---: | --- | --- | --- | --- |
| ONYX Preview | Personal test frame: proof of identity and collection quality before a full photoshoot | 900 | 1 | One chosen collection and primary look | No | No | Technical correction only |
| ONYX Signature | Personal photoshoot in a chosen collection | 3,000 | 10 | Standardized ONYX collection, adapted to the person | Standard | No | One launch-policy round, limited scope |
| ONYX Premium | Personalized visual story designed around the person’s goals and desired image | 5,000 | 20 | Personal Creative Profile, creative direction and scene plan | Extended | ONYX Motion | Two launch-policy rounds, broader scope |

**Preview proves. Signature standardizes. Premium personalizes.** Premium is not simply a 20-image Signature package.

Client-facing launch prices and Preview upgrade arithmetic are authoritative in [ONYX Price Book v1](ONYX_PRICE_BOOK_v1.md). The structured source for future automation is [products_v1.yaml](products_v1.yaml).

## ONYX Preview

### Purpose

Preview is a low-risk first purchase. It lets a client check identity preservation, see the style of a selected collection, understand ONYX quality and decide whether to purchase a full photoshoot.

Use customer language such as **«персональный тестовый кадр ONYX»**. Do not describe it as a sale of one AI image.

### Included

- one final high-resolution photograph;
- one chosen production-approved collection and one primary look;
- production QA;
- repair or regeneration when required for technical quality;
- final processing and high-resolution delivery.

Preview has no Concept Card, personal creative profile or client-directed creative cycle. A full Preview payment is credited when the client upgrades to Signature or Premium; it is a product price credit, not a discount on the listed total price.

## ONYX Signature

### Purpose

**Персональная фотосессия в выбранной коллекции.** Signature is the standard mass-market ONYX product.

Signature is standardized by creative framework. The client chooses a ready ONYX Collection, such as Business, Executive, Lifestyle or another production-approved collection. ONYX adapts the collection to the individual; it does not design a wholly new visual concept from zero.

### Included

- 10 final photographs;
- usually 2–3 looks and 4–6 visually distinct scenes, adjusted when quality requires it;
- one coherent collection visual language;
- identity consistency and diversity control;
- production QA, repair or regeneration, retouch or enhancement and upscale;
- ONYX Selection;
- standard ONYX Collection Book;
- high-resolution originals and delivery package.

The P02 Business Collection Book is the approved Signature reference implementation. See [Collection Book Standard](ONYX_COLLECTION_BOOK_STANDARD.md) and [production guide](../Templates/Collection_Book/COLLECTION_BOOK_PRODUCTION_GUIDE.md).

## ONYX Premium

### Purpose

Premium is a **photoshoot developed around the client’s personality, goals and desired image**. It is a personalized visual story with more creative variety, not a larger standard collection.

### Included

- 20 final photographs;
- Personal Creative Profile and Premium Creative Brief;
- individual creative direction and scene plan;
- usually 4–5 looks, 8–12 scenes and several visual chapters or moods, adjusted when quality requires it;
- increased variety and identity consistency;
- production QA, repair or regeneration, retouch or enhancement and upscale;
- extended ONYX Collection Book;
- ONYX Selection and, where useful, additional curator selections;
- Personal Style Recommendation and Recommended Use guidance;
- ONYX Motion;
- social-ready export formats in addition to high-resolution originals;
- expanded client revision scope.

The 5,000 RUB launch price is a hypothesis. Reassess it after the first real orders using measured unit economics; it is not a promise of a permanent price.

### Personal Creative Profile

Premium production begins only after collecting: purpose of the photoshoot; profession or field; intended uses; desired impression; preferred style; Natural / Polished / Glamour level; clothing; preferred environments; elements to avoid; permitted facial and body correction; and other wishes.

These inputs become the internal **Premium Creative Brief**. They guide production but do not authorize unsupported changes to identity or appearance.

### Concept Card and approval

Premium includes a brief operational concept approval before batch production. It is a bounded direction check, not an open-ended bespoke design engagement.

```text
ONYX PREMIUM CONCEPT

Client:
Collection / concept:
Visual direction:
Mood:
Primary use:
Looks:
Scenes:
Key priorities:
Avoid:
```

The client approves or corrects this card once before mass generation. The service standard defines the state transition.

### Visual chapters

Premium should be organized as logical visual chapters so it reads as a complete story rather than 20 variations of one scene. For a Business or Executive direction, chapters may be Portrait, At Work, Personal Brand and Editorial. This is an example, not a mandatory universal list; chapters come from the Creative Profile.

### ONYX Motion

ONYX Motion is a Premium deliverable: a short cinematic motion portrait based on a key collection frame. Target: about four seconds, natural motion and expression, minimal artefacts, a premium look and vertical/social-friendly format. The underlying model is not part of the product definition and may change.

### Premium Collection Book and use guidance

Premium Book requirements extend the Signature standard with Personal Creative Direction, visual chapters, ONYX Selection, optional additional curator selections, Personal Style Recommendation, Recommended Use, personal closing note and next collections. No Premium Book PDF is defined by this document.

Recommended Use is personalized after final selection and may cover a professional profile, avatar, corporate site, speaker bio, CV, social media or editorial/personal-brand use when relevant. It does not promise particular platforms.

Social-ready exports are optional optimized copies such as avatar/profile, portrait post or story/reel cover. High-resolution originals remain the main deliverable; no social assets are generated by this standard.

## What is outside the launch line

The following are future scope, not launch products: ONYX Private; fully bespoke products above Premium; subscriptions; corporate packages; website self-service; automated SaaS; unlimited generation; and Model Arena as a customer feature.

## Related standards

- [Price Book](ONYX_PRICE_BOOK_v1.md): prices, Preview credit and unit-economics placeholders.
- [Service Standard](ONYX_SERVICE_STANDARD_v1.md): journey, corrections, privacy, retention and delivery rules.
- [Portfolio Standard](ONYX_PORTFOLIO_STANDARD.md): asset roles and portfolio QA.
- [Marketing Standard](ONYX_MARKETING_STANDARD.md): marketing collateral only.
- [Collection Book Standard](ONYX_COLLECTION_BOOK_STANDARD.md): Signature and Premium Book requirements.

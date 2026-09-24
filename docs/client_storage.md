# Private client storage

Real client data is stored outside this repository under the `ONYX_CLIENT_ROOT` location.

Default Windows location:

`D:\\AI\\ONYX_Clients`

The repository may contain generic schemas, templates, automation code, and anonymized examples. Do not add client photos, references, intake answers, order prompts, QA, Collection Books, delivery packages, or client-specific metadata to Git.

Use a placeholder such as `CL-XXXX_ClientName` when documenting a new storage folder. Keep each order self-contained below the client folder.

## Client and order identifiers

- Use a stable client identifier in the form `CL-{number}`. A display-name slug may change without changing the client identifier.
- Reuse the existing client identifier for later orders. A matching display name alone is not enough to merge client records.
- Use `ORD-{year}-{number}` as the canonical order identifier and keep its machine-readable order record inside the external client folder.
- Record scope and quote confirmation before payment, then payment status and receipt evidence before production.
- When an order closes, record its resolution and retention deadline. Keep only the minimum payment, consent and anonymized reporting evidence after the applicable client assets are deleted.

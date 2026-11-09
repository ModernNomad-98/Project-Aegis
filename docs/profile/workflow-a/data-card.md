# Data card — synthetic policy corpus

**Status:** design record. The corpus is specified but **not created** by this
item; the 13 documents are described here so a future build can create them
without inventing a data policy.

## Dataset identity

| Field | Value |
| --- | --- |
| Name | Synthetic support policy corpus A |
| Version | `corpus-a/0.1.0` (design version; no content digest yet) |
| Documents | 13 short policy documents, 150–400 words each |
| Origin | **Synthetic.** Written for this exercise; invented organization, people and amounts. |
| Language | English (a locale field exists; only `en` is specified) |
| Personal data | **None.** No real name, email, phone, address, account, tenant or credential. |
| Source | Hand-authored from a written outline; no scrape, no customer export, no model generation. |
| Retention | Retained with the repository design record until superseded; fixtures retained with the item. |
| Document ids | `refunds`, `shipping`, `returns`, `warranty`, `promotions`, `billing`, `cancellations`, `account`, `privacy`, `security`, `support-hours`, `holidays`, `accessibility` |

## Why synthetic

The workflow exists to test grounding and refusal, not to answer real policy
questions. Synthetic documents let the corpus contain deliberate traps (an
embedded instruction, a contradictory clause, a stale clause) without exposing
anyone's data or creating a real compliance obligation.

## Allowed use

- Offline design, schema checks and fixture replay.
- Hand-written or mock-transport exercise of the retrieval and citation rules.
- Negative-case testing of the seven NC rows.

## Prohibited use

- Any live, paid or provider-backed run without a separate owner decision.
- Any claim that the corpus is real policy, legal advice or production content.
- Mixing real data into the corpus or fixtures, even as an example.
- Publication of the corpus as a product dataset.

## Leakage checks (to run when the corpus is created)

1. Search every document and fixture for email addresses, phone numbers, account
   ids and credential-shaped strings; expect zero.
2. Confirm every organization and person name is invented and marked synthetic.
3. Confirm no document is copied from a real policy page.
4. Confirm the corpus digest is recorded in the workflow output object.
5. Confirm the negative fixtures do not quote real incidents.

## Known limitations

- Thirteen documents are too few to support any retrieval-quality claim.
- The corpus cannot represent the ambiguity of real policy text.
- No PII process is exercised because no PII exists; this card is not a
  privacy-compliance artifact.

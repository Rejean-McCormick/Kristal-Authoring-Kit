# UNESCO Educational policy — scoped integration candidate

Repository: `Kristal-Authoring-Kit`  
Windows path: `C:\mycode\Kristal\Kristal-Authoring-Kit`  
Role: `canonical_authoring`

This file is a **non-normative pilot integration record**, not a claim of interoperability or a public release. The 41 UNESCO concepts are **seed membership**, not 41 canonical KQ or 41 published articles. The 36 Wikidata P3916 candidates remain unreviewed. The Wikipedia EN SQL index and compressed XML remain local on D:; this repo must not redistribute them.

**Consumes:** `reviewed_identity_decisions`, `reviewed_source_assertions`, `candidate_lexical_catalog`.  
**Produces:** `versioned_canonical_branch_graph`.

**Next correction:** Create reviewed branch KQ/KP/KA/KS only through authorized and journaled v11 transactions.

## Mandatory invariants

- **One branch Kristal** `unesco-mt1-10`; 41 starting concepts; individual multilingual encyclopedia articles are **projections**, not distinct Kristals or copies/translations of Wikipedia.
- KQ/KP/KA/KS require their own native provenance and appropriate canonical review. QID and UNESCO identifiers remain external. An AI suggestion or Wikipedia reference does not create canonical KA or KS.
- The 14 requested locales are an **objective**, not proof of GF/SemantiK/Spek qualification or 574 completed articles.
- Never enable GitHub synchronization, Pages, wiki upload or public mode based solely on this pilot manifest. C1/C2/C3/C4 authorizations remain external and blocked.
- All source readings and candidate handoffs are local or explicitly chosen; never rewrite D: source dumps, framework pins, existing Kristal commitments, or private databases.

An additive contract smoke test is at `tests/test_unesco_mt1_10_handoff.py`; run it without touching existing repository semantics.

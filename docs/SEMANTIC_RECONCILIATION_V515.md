# Semantic reconciliation V5.15 — read-only consumer boundary

**Status:** candidate implementation, not owner review or Framework approval.

Kristal-Manager may build a **private reconciliation index** from an exact
V5.14 local semantic observatory database. This is a consumer-side observation:
it does not register, select, change, or migrate Kit-owned canonical v11
artifacts, and it never reads hosted `kristal-public` as the correction source.

Review cases include scoped identity-role drift, lexeme competition,
polysemous terms, multiple active (`candidate`/`accepted`) external targets,
status divergence, missing evidence, and multiple complete but **unselected**
revisions. Previously rejected crosswalk alternatives do not count as active
target ambiguity. Dictionary-only revisions do not require their own identity
registries; false orphans must not be inferred from that absence.

Review SQLite and JSON are bound to the source-index SHA-256. Every case is
`NOT_DECIDED`. An accepted status in a crosswalk is not independent acceptance
by this tool, and a shared label cannot promote two KQ/KP identities into one.

The Authoring Kit remains the *only* canonical registrar. Any future approved
correction must be a new isolated local revision using the Kit's adopted v11
contracts and recoverable transaction journal. Qualification C1/C2, GitHub
publication C3, and runtime activation remain separate external gates.

Owner reference: `Kristal-Manager/kristal_manager/semantic_reconciliation_v515.py`.

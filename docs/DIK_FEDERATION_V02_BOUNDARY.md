# Authoring Kit / diK — explicit canonical production boundary

**Candidate coordination note, 24 November 2026.** The Kit remains the
sole producer/registrar of a Kristal's canonical v11 graph and catalog
state. diK is the owner of lexical dictionaries, source evidence and
derived-view selection proposals. The Kit must never convert a diK SQLite
view, source `accepted` flag or Wikidata label into canonical authority.

The Framework v11 `11.0.0-draft.4` semantic schemas are byte-identical to
diK's vendor copies in the supplied 24 November SmartDump; this is an
integrity observation, not a TCK qualification. Every local reference remains
`(namespace_id, KQ/KP)`; external Q/P requires independently reviewed
`exactMatch` evidence. No existing canonical artifacts are altered.

diK now requires `dik.canonical-selection-decisions/0.2`, including SHA-256
of the **inspected graph**. These decisions authorize only a derived lookup,
not the Kit commands `import-dik-catalog`, `select-v11-catalog` or
`recover-v11`. Existing journaling, recovery and authoritative registration
gates remain mandatory. Historical selection files `/0.1` are not silently
upgraded or treated as approvals. This page is not a new Kit import API.

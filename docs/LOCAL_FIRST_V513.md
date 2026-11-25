# V5.13 — Local-first derived candidates

Status: **candidate integration guidance**, not independent qualification.

Each Kristal under `C:\mycode\Kristal\locals` owns its canonical semantic content. The Authoring Kit validates, builds and materializes **derived read surfaces on private copies**; it does not directly edit `kristal-public` or grant C1/C2 approval. Manager coordinates explicit selection with `stage-public-candidate --slug <slug> --kit <path> --output <private-dir> --build-on-copy --write-private`.

First use Manager's `audit-local-public` integrity diagnostic. Byte-for-byte integrity neither validates Wikidata QIDs nor selects a semantic revision. The reviewer must verify graph-pinned selection, registry/graph/crosswalk/catalog consistency, input provenance and all owner-specific gates. Preserve labels, definitions, evidence, historic revisions and deliberate sync-manifest exclusions. Do not add excluded canonical artifacts to the public read surface.

Only after independent review may an explicit candidate proceed to C3 checks and an exact local commit. Publication still requires independent C1/C2 receipts and the hosting policy. Nothing in this overlay writes to a Kristal's canon, public checkout, publication workflow or RuntimeSet.

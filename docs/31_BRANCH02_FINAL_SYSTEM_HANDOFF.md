# Branch 02 — final-system semantic authoring and reviewed input handoff

**State:** locally tested against supplied Framework 11.0.0-draft.4; no publication/activation permitted by these tests.

## Authoritative state and receiving interface

The Authoring Kit 4.0.0-draft.4 is the owner of local canonical graph registration and semantic workspace transactions. Framework dictates KQ/KP/KA/KS meaning; diK contributes versioned dictionary and crosswalk **candidates**; Kristalizer proposes reviewed corrections; Arketype defines reusable, non-normative structures. A proposal cannot authorize a Kit graph/crosswalk/catalog write by itself.

Exact source pins live at `contracts/v11-framework-pin.json`: the supported Framework profile is `11.0.0-draft.4`, with thirteen source file hashes. A local `qualify-v11` report is a read-only conformance observation, not a release grant.

## Reproducible, read-only local campaign

```bash
python scripts/check_branch02_interop.py --framework ../Framework --dik ../diK
python tools/kristal.py qualify-v11 examples/demo-semantic-v11 --framework ../Framework --locales fr,fr-CA
```

`check_branch02_interop.py` rejects a missing/tampered Framework source, unexpected Kit version, modified diK v11 vendored schema, or incomplete semantic input. It compares Framework reference coverage against a real Kit workspace and checks that the four semantic inputs remain byte-identical. The diK probe only establishes that its eleven vendored v11 schemas are byte-identical to those provided with Framework draft.4. It does **not** execute a diK import operation or certify schema-equivalent behavior of every diK command.

## Functional requirements for adoption

1. All external mappings enter **review-only staging**, never the authoritative KQ/KP graph directly. Approved identity and evidence refs must be checked against exact source revisions.
2. `import-dik-catalog` creates a new isolated candidate; `--register`, `select-v11-catalog`, `check-v11` and build are separate stages with independent authorization.
3. Existing transaction journals, Logical Artifacts, source history and v9 state commitments are retained. On pending v11 journal, stop writes and explicitly recover; do not delete the journal.
4. `build-v9` and `qualify-v11` do not publish, deploy, synchronize remote Git or activate anything.
5. If a new Arketype workspace is created using an external Kit, it must remain empty/unqualified until explicit namespace allocation, graph/crosswalk/catalog review and registration.

## Owner follow-ups

- Agree a signed/reviewed candidate import manifest and authorization policy with diK and Kristalizer owners; this campaign has not adopted a new wire-schema ID.
- Run actual diK **producer output → Kit `import-dik-catalog`** fixtures with rejected unapproved records and a reversible registration transaction before asserting bilateral importer qualification.
- Provide the exact compatible read-view source and tests to Branch 03 release and Branch 04 Integration Pack/consumer work.

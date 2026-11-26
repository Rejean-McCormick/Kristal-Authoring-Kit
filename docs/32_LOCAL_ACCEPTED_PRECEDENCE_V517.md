# V5.17 — Recoverable accepted-precedence crosswalk evolution

V5.17 performs an **actual local canonical** evolution under strict limits:
when one local v11 KQ/KP has a source-recorded, KS-evidenced `accepted`
Wikidata `exactMatch`, competing different-QID `candidate` exact matches of
that same identity are marked `superseded` in a NEW canonical crosswalk.

The original crosswalk, graph, registry, dictionary catalog, and all prior
state commitments remain byte-for-byte intact. The new crosswalk is registered
through `kristal_v11_core.register_artifact_recoverably` and the active v11
authoring profile is validated and updated with a hash-addressed history copy.
`canon/state.index.json` is only modified through the Kit's journal protocol.

The rule uses the local owner's **existing recorded acceptance**, not
external Wikidata verification. It creates no `accepted` mappings or new
semantic identities. Multiple candidate QIDs without an accepted one stay
ambiguous. Every changed candidate receives a reproducible audited-rule
decision ID with registered KS evidence from the existing accepted record.

## One-shot PS7 deployment

The V5.17 overlay installer updates its four owner repositories, runs the
focused tests and invokes the helper, then refreshes the V5.16 local derived
semantic views. No separate operator review cycle is needed for this narrowly
defined precedence operation.

Direct invocation after installation:

```powershell
python 'C:\mycode\Kristal\Kristal-Authoring-Kit\tools\v517_accepted_precedence.py' `
  --locals 'C:\mycode\Kristal\locals' `
  --private-dir (Join-Path $env:LOCALAPPDATA 'Kristal') --apply
```

The helper preflights **all** affected workspaces before changing any of
them. V5.17.1 recognizes only real `Kristal-*` directories as workspaces;
regular neighboring files such as `Kristal-*.zip` snapshots are ignored and
kept unchanged. Symlinks and junctions that claim to be workspaces still fail
closed. Each registration is crash-recoverable and each profile has a SHA-pinned
history backup. If a batch is interrupted after a registered artifact, do
not delete it or manually rewrite the state index. Inspect the private
`SEMANTIC_V517_*.json` progress report, use `recover-v11 --mode status` and
the Kit's documented `finish`/`rollback` only when appropriate, then rerun.

Canonical multi-workspace changes are **not** one filesystem-atomic
transaction. An interrupted batch may be partially completed; the next run
is idempotent. The operation deliberately does not build v9 commitments,
qualify C1/C2, publish, change `kristal-public`, push Git or activate a runtime.

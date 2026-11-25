# V5.14 federated semantic observatory boundary

**Status:** proposed interoperability adapter, not Framework qualification.

Manager may read **locally registered** `canon/state.index.json` entries to
build a private, rebuildable cross-Kristal semantic index. The authoring Kit
remains the sole canonical graph/identity registrar for its adopted v11
contract. No Kit or local Kristal files are changed by this adapter.

The observatory records `(namespace_id, semantic_id)`, the exact owner slug,
revision directory, source path and observed SHA-256. It keeps labels in
versioned JSON/JSONL dictionary layers and Wikidata Q/P IDs in separate
crosswalk observations. It recognizes historical typed aliases (`registry.json`,
`graph.json`, `crosswalk.json`) without rewriting them.

All revisions are **unselected**. An imported source claim of `accepted` is
not equivalent to reviewed equivalence, independent C1/C2 approval, or
permission to publish. Before any future owner-authorized local correction,
require exact registered source commitments, explicit revision and evidence,
Kit's recoverable v11 journaling, and independent qualification. Hosted public
Kristals must only ever be derived from qualified local sources.

Manager implementation and tests: `kristal_manager/semantic_federation_inventory.py`
and `tests/test_semantic_federation_inventory_v514.py` in Kristal-Manager.

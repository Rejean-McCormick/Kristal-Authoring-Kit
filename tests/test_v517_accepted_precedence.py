"""V5.17 canonical crosswalk precedence and recoverable history tests."""
from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import sys
import tempfile
import unittest


TOOLS = Path(__file__).resolve().parents[1] / "tools"
sys.path.insert(0, str(TOOLS))
import kristal_v11_core as v11  # noqa: E402
from v517_accepted_precedence import plan_workspace, apply_workspace, evolve_all  # noqa: E402


class AcceptedPrecedenceTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.base = Path(temp.name)
        self.locals = self.base / "locals"
        self.private = self.base / "private"
        self.locals.mkdir()
        self.private.mkdir()
        self.root = self.locals / "Kristal-Test"
        self.root.mkdir()
        self.write("kristal.workspace.json", {"slug": "test", "state_ref": "urn:kristal:test:state"})

    def write(self, rel, obj):
        path = self.root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        data = obj if isinstance(obj, bytes) else (json.dumps(obj, ensure_ascii=False) + "\n").encode("utf8")
        path.write_bytes(data)
        return path

    def fixture(self, *, accepted=True, multiple_candidates=2):
        base = "canon/domain/v11/base"
        ns = "test:scope"
        registry = base + "/registry.json"
        graph = base + "/graph.json"
        crosswalk = base + "/crosswalk.json"
        catalog = base + "/dictionaries/catalog.json"
        self.write(registry, {"artifact_type": "kristal_identity_registry", "schema_version": "11.0",
                              "registry_id": "test-registry", "namespace_id": ns, "identities": [
                                  {"id": "KQ1001", "kind": "entity", "status": "stable"},
                                  {"id": "KS4001", "kind": "source", "status": "stable"}]})
        self.write(graph, {"artifact_type": "kristal_semantic_graph", "schema_version": "11.0",
                           "namespace_id": ns, "graph_id": "test-graph", "entities": ["KQ1001"],
                           "properties": [], "sources": ["KS4001"], "assertions": []})
        mappings = []
        def mapping(mid, qid, status):
            row = {"mapping_id": mid, "local_ref": {"namespace_id": ns, "id": "KQ1001"},
                   "external_ref": {"system": "wikidata", "id": qid},
                   "relation": "exactMatch", "status": status}
            if status == "accepted":
                row["review"] = {"method": "human", "decision_id": "reviewed", "evidence_refs": ["KS4001"]}
            return row
        if accepted:
            mappings.append(mapping("m1", "Q42", "accepted"))
        for n in range(multiple_candidates):
            mappings.append(mapping(f"candidate{n}", f"Q{43+n}", "candidate"))
        self.write(crosswalk, {"schema_version": "11.0", "artifact_type": "kristal_external_crosswalk",
                               "crosswalk_id": "cw-original", "mappings": mappings})
        self.write(catalog, {"schema_version": "11.0", "artifact_type": "kristal_dictionary_catalog",
                             "namespace_id": ns, "catalog_id": "test-catalog",
                             "languages": [{"tag": "fr", "fallbacks": [], "layers": []}]})
        roles = {"registry": registry, "graph": graph, "crosswalk": crosswalk, "catalog": catalog}
        self.write("canon/state.index.json", {"canonical_artifacts": [
            {"artifact_id": "urn:test:" + k, "path": p,
             "logical_contract": {"id": "test." + k, "version": "11.0"},
             "commitment": {"mode": "compute-json-jcs", "profile": "kristal.logical/jcs-sha256-v1"}}
            for k, p in roles.items()]})
        self.write(".kristal/v11/authoring.json", {
            "format": "kristal.authoring-v11-profile/1.0",
            "semantic_profile": "kristal.semantic-identity/11.0", **roles})
        v11.validate(self.root)
        return roles

    def test_registers_new_crosswalk_selects_and_preserves_original(self):
        roles = self.fixture()
        old_crosswalk = (self.root / roles["crosswalk"]).read_bytes()
        old_profile = (self.root / ".kristal/v11/authoring.json").read_bytes()
        change = plan_workspace(self.root)
        self.assertEqual((change.affected_id_count, change.superseded_mapping_count), (1, 2))
        result = apply_workspace(change)
        self.assertEqual(result["superseded_candidate_mappings"], 2)
        self.assertEqual((self.root / roles["crosswalk"]).read_bytes(), old_crosswalk)
        active = v11.load_profile(self.root)
        self.assertEqual(active["crosswalk"], result["artifact"])
        newer = v11.read(self.root / result["artifact"])
        self.assertEqual([row["status"] for row in newer["mappings"]],
                         ["accepted", "superseded", "superseded"])
        self.assertEqual(newer["mappings"][0], json.loads(old_crosswalk)["mappings"][0])
        self.assertEqual(v11.validate(self.root)["namespace_id"], "test:scope")
        self.assertEqual((self.root / result["profile_backup"]).read_bytes(), old_profile)
        self.assertEqual(plan_workspace(self.root), None)  # idempotent

    def test_never_invents_acceptance_from_candidates(self):
        self.fixture(accepted=False)
        before = (self.root / "canon/state.index.json").read_bytes()
        summary = evolve_all(self.locals, self.private, apply=True)
        self.assertEqual(summary["change_owners"], 0)
        self.assertEqual(summary["wikidata_acceptance_added"], 0)
        self.assertEqual((self.root / "canon/state.index.json").read_bytes(), before)

    def test_plan_pins_source_profile_and_state_before_writes(self):
        self.fixture()
        change = plan_workspace(self.root)
        profile_path = self.root / ".kristal/v11/authoring.json"
        profile_path.write_bytes(profile_path.read_bytes() + b" ")
        with self.assertRaisesRegex(v11.V11Error, "authoring profile drifted"):
            apply_workspace(change)
        self.assertFalse((self.root / change.target_path).exists())

    def test_missing_accepted_evidence_fails_closed(self):
        roles = self.fixture()
        path = self.root / roles["crosswalk"]
        old = json.loads(path.read_text())
        old["mappings"][0]["review"]["evidence_refs"] = []
        self.write(roles["crosswalk"], old)
        with self.assertRaises(v11.V11Error):
            plan_workspace(self.root)
        self.assertFalse((self.root / "canon/domain/v11/updates").exists())

    def test_complete_one_operation_and_retry(self):
        self.fixture()
        result = evolve_all(self.locals, self.private, apply=True)
        self.assertEqual(result["status"], "LOCAL_CANONICAL_REVISION_SELECTED")
        self.assertEqual((result["change_owners"], result["candidate_mappings_to_supersede"]), (1, 2))
        self.assertEqual(len(result["selected"]), 1)
        self.assertEqual(evolve_all(self.locals, self.private, apply=True)["change_owners"], 0)
        assert sha256((self.root / result["selected"][0]["artifact"]).read_bytes()).hexdigest() == result["selected"][0]["artifact_sha256"]

    def test_sibling_kristal_zip_snapshot_is_not_a_workspace(self):
        self.fixture()
        archive = self.locals / "Kristal-Test_backup_20261125.zip"
        archive.write_bytes(b"not a working directory")
        stray_file = self.locals / "Kristal-Old-Notes.txt"
        stray_file.write_text("archived notes", encoding="utf8")
        summary = evolve_all(self.locals, self.private, apply=True)
        self.assertEqual(summary["local_workspaces"], 1)
        self.assertEqual(summary["change_owners"], 1)
        self.assertTrue(archive.is_file())
        self.assertEqual(archive.read_bytes(), b"not a working directory")

    def test_symlink_workspace_is_still_a_hard_block(self):
        self.fixture()
        link = self.locals / "Kristal-Untrusted-Link"
        try:
            link.symlink_to(self.root, target_is_directory=True)
        except OSError:
            self.skipTest("Creating test symlinks is not permitted on this host")
        with self.assertRaisesRegex(v11.V11Error, "not a real local workspace"):
            evolve_all(self.locals, self.private, apply=True)


if __name__ == "__main__":
    unittest.main()

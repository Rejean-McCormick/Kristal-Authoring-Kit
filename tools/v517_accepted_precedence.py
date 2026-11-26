"""V5.17 opt-in local canonical crosswalk evolution, with no new Wikidata approval.

Only a *source-recorded accepted* exactMatch with registered KS evidence may
supersede competing still-candidate QIDs for the same scoped identity. The
old canonical crosswalk stays byte-for-byte intact. The Authoring Kit's
recoverable registration journal is the only writer of canon/state.index.
"""
from __future__ import annotations

import argparse
from copy import deepcopy
from dataclasses import dataclass
from hashlib import sha256
import json
import os
from pathlib import Path
import re
import sys

import kristal_v11_core as v11


PROFILE = "koa.local-wikidata-accepted-precedence/0.1"
REVISION = "accepted-precedence-v517"
SLUG_RE = re.compile(r"^[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$")


def _digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def _is_link_or_junction(path: Path) -> bool:
    """Fail closed for symlinks on all OSes and junctions on Windows 3.12+."""
    check_junction = getattr(path, "is_junction", None)
    return path.is_symlink() or (callable(check_junction) and check_junction())


def _encoded(obj: dict) -> bytes:
    return (json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf8")


def _assert_real_parents(root: Path, relative: str):
    if not isinstance(relative, str) or not relative or relative.startswith("/") or "\\" in relative:
        raise v11.V11Error("unsafe canonical/profile path")
    if any(x in ("", ".", "..") for x in relative.split("/")):
        raise v11.V11Error("unsafe canonical/profile path components")
    path = root
    for part in relative.split("/"):
        path = path / part
        if _is_link_or_junction(path):
            raise v11.V11Error(f"refusing symlink path: {path}")


@dataclass(frozen=True)
class Change:
    root: Path
    slug: str
    source_path: str
    source_sha: str
    profile_sha: str
    state_sha: str
    target_path: str
    artifact_id: str
    payload: bytes
    affected_id_count: int
    superseded_mapping_count: int
    evidence_refs: tuple[str, ...]


def _read_workspace(root: Path) -> tuple[str, dict] | None:
    if _is_link_or_junction(root) or not root.is_dir():
        raise v11.V11Error(f"not a real local workspace: {root}")
    _assert_real_parents(root, "kristal.workspace.json")
    ws = v11.read(root / "kristal.workspace.json")
    slug = ws.get("slug")
    if not isinstance(slug, str) or not SLUG_RE.fullmatch(slug):
        raise v11.V11Error(f"unsafe workspace slug: {root}")
    if not (root / v11.CONFIG).is_file():
        return slug, {}
    _assert_real_parents(root, v11.CONFIG)
    return slug, v11.load_profile(root)


def _proposal(old: dict, namespace: str, registry_ids: dict) -> tuple[dict, int, int, set[str]]:
    """Keep accepted mappings verbatim. Change competing candidates only."""
    mappings = old.get("mappings")
    if not isinstance(mappings, list):
        raise v11.V11Error("bad crosswalk mappings")
    accepted = {}
    for m in mappings:
        if m.get("relation") != "exactMatch" or m.get("status") != "accepted":
            continue
        local = m.get("local_ref", {})
        if local.get("namespace_id") != namespace:
            raise v11.V11Error("accepted mapping namespace mismatch")
        sid = local.get("id")
        evidence = m.get("review", {}).get("evidence_refs", [])
        if not evidence or any(registry_ids.get(x) != "source" for x in evidence):
            raise v11.V11Error("accepted alignment needs registered KS evidence")
        if sid in accepted:
            raise v11.V11Error("multiple accepted QIDs for one scoped ID")
        accepted[sid] = m
    changed = deepcopy(old)
    affected = set()
    evidence_used = set()
    total = 0
    for m in changed["mappings"]:
        if m.get("relation") != "exactMatch" or m.get("status") != "candidate":
            continue
        local = m.get("local_ref", {})
        sid = local.get("id")
        selected = accepted.get(sid)
        if selected is None or local.get("namespace_id") != namespace:
            continue
        if m.get("external_ref", {}).get("id") == selected["external_ref"]["id"]:
            continue
        evidence = selected["review"]["evidence_refs"]
        seed = [namespace, sid, selected["mapping_id"], m["mapping_id"]]
        ticket = sha256(json.dumps(seed, separators=(",", ":")).encode()).hexdigest()[:20]
        m["status"] = "superseded"
        m["review"] = {"method": "audited_rule", "decision_id": f"v517-accepted-precedence-{ticket}",
                       "evidence_refs": sorted(set(evidence))}
        total += 1
        affected.add(sid)
        evidence_used.update(evidence)
    return changed, len(affected), total, evidence_used


def plan_workspace(root: Path) -> Change | None:
    incoming = Path(root)
    if _is_link_or_junction(incoming):
        raise v11.V11Error(f"not a real local workspace: {incoming}")
    root = incoming.resolve(strict=True)
    if (root / v11.CONFIG).exists() is False:
        return None
    ws = _read_workspace(root)
    if ws is None or not ws[1]:
        return None
    slug, profile = ws
    v11._assert_no_pending(root)
    profile_sha = _digest(root / v11.CONFIG)
    state_path = root / "canon/state.index.json"
    state_sha = _digest(state_path)
    source_path = profile["crosswalk"]
    _assert_real_parents(root, source_path)
    source = v11.safe(root, source_path)
    old = v11.read(source)
    registry_path = profile["registry"]
    _assert_real_parents(root, registry_path)
    namespace, ids = v11.registry_check(v11.read(v11.safe(root, registry_path)))
    # This is a canonical-changing operation: require complete Kit validation.
    v11.validate(root)
    new, groups, alternatives, evidence = _proposal(old, namespace, ids)
    if alternatives == 0:
        return None
    origin_sha = _digest(source)
    suffix = origin_sha[:16]
    new["crosswalk_id"] = old["crosswalk_id"] + ":" + REVISION + ":" + suffix
    payload = _encoded(new)
    v11.crosswalk_check(new, namespace, ids)
    # Layer compatibility with accepted mappings is preserved. No new accepted.
    subdir = f"canon/domain/v11/updates/{REVISION}-{suffix}"
    target = subdir + "/external-crosswalk.json"
    artifact_id = f"urn:kristal:{slug}:v11:crosswalk:{REVISION}:{suffix}"
    _assert_real_parents(root, target)
    registered = v11.read(state_path).get("canonical_artifacts", [])
    target_entry = [x for x in registered if x.get("path") == target]
    if target_entry:
        if len(target_entry) != 1 or target_entry[0].get("artifact_id") != artifact_id:
            raise v11.V11Error("target already registered with different identity")
        if not (root / target).is_file() or (root / target).read_bytes() != payload:
            raise v11.V11Error("previous V5.17 target differs; manual recovery required")
    elif (root / target).exists():
        raise v11.V11Error("unregistered canonical target already exists")
    return Change(root, slug, source_path, origin_sha, profile_sha, state_sha, target,
                  artifact_id, payload, groups, alternatives, tuple(sorted(evidence)))


def _verify_frozen(change: Change):
    root = change.root
    if _digest(root / v11.CONFIG) != change.profile_sha:
        raise v11.V11Error(f"{change.slug}: authoring profile drifted")
    if _digest(root / "canon/state.index.json") != change.state_sha:
        raise v11.V11Error(f"{change.slug}: canonical index drifted")
    if _digest(v11.safe(root, change.source_path)) != change.source_sha:
        raise v11.V11Error(f"{change.slug}: source crosswalk drifted")
    v11._assert_no_pending(root)


def apply_workspace(change: Change) -> dict:
    root = change.root
    _verify_frozen(change)
    state = v11.read(root / "canon/state.index.json")
    existing = [x for x in state.get("canonical_artifacts", []) if x.get("path") == change.target_path]
    if not existing:
        v11.register_artifact_recoverably(root, rel=change.target_path, payload=change.payload,
            artifact_id=change.artifact_id, contract_id="kristal.v11.external-crosswalk")
    else:
        if len(existing) != 1 or existing[0].get("artifact_id") != change.artifact_id or \
                (root / change.target_path).read_bytes() != change.payload:
            raise v11.V11Error("existing registered v517 artifact disagrees with proposed output")
    original_profile = v11.load_profile(root)
    candidate = dict(original_profile, crosswalk=change.target_path)
    v11.validate(root, candidate, require_registered=True)
    previous = (root / v11.CONFIG).read_bytes()
    history = root / ".kristal/v11/history"
    history.mkdir(parents=True, exist_ok=True)
    backup = history / (sha256(previous).hexdigest() + ".json")
    if backup.exists():
        if backup.read_bytes() != previous:
            raise v11.V11Error("historical authoring profile SHA collision or corruption")
    else:
        v11._write_exclusive_synced(backup, previous)
    v11._replace_synced(root / v11.CONFIG, v11._json_bytes(candidate))
    return {"slug": change.slug, "source_sha256": change.source_sha,
            "artifact": change.target_path, "artifact_sha256": sha256(change.payload).hexdigest(),
            "profile_backup": backup.relative_to(root).as_posix(),
            "affected_semantic_ids": change.affected_id_count,
            "superseded_candidate_mappings": change.superseded_mapping_count,
            "registered_KS_evidence_refs": list(change.evidence_refs)}


def evolve_all(locals_root: Path, private_dir: Path, *, apply=False) -> dict:
    locals_root = Path(locals_root).resolve(strict=True)
    private_dir = Path(private_dir).resolve(strict=True)
    if not locals_root.is_dir() or not private_dir.is_dir() or private_dir.is_symlink():
        raise v11.V11Error("expected real local/private directories")
    if private_dir == locals_root or private_dir in locals_root.parents or locals_root in private_dir.parents:
        raise v11.V11Error("private report directory must be outside local trees")
    # Local archives often sit beside live workspaces (e.g. Kristal-Name.zip).
    # They are snapshots, not writable canonical owners. Include symlinks in
    # the preflight intentionally so _read_workspace rejects them, rather than
    # silently following or disregarding a suspect would-be workspace.
    workspaces = sorted(
        p for p in locals_root.iterdir()
        if p.name.startswith("Kristal-") and (p.is_dir() or _is_link_or_junction(p))
    )
    seen = set()
    plan = []
    for root in workspaces:
        ws = _read_workspace(root)
        if ws is None:
            continue
        slug, _ = ws
        if slug in seen:
            raise v11.V11Error(f"duplicate local slug: {slug}")
        seen.add(slug)
        change = plan_workspace(root)
        if change:
            plan.append(change)
    summary = {"profile": PROFILE, "status": "DRY_RUN", "applied": False,
               "local_workspaces": len(seen), "change_owners": len(plan),
               "affected_semantic_ids": sum(p.affected_id_count for p in plan),
               "candidate_mappings_to_supersede": sum(p.superseded_mapping_count for p in plan),
               "wikidata_acceptance_added": 0, "canonical_history_overwritten": False,
               "public_modified": False, "selected": []}
    if apply:
        # New private report is created before canonical writes. It becomes
        # a progress journal after every committed local change.
        report = private_dir / ("SEMANTIC_V517_" + os.urandom(6).hex() + ".json")
        summary["report"] = str(report)
        def report_progress():
            pending = report.with_suffix(".json.new")
            try:
                with pending.open("x", encoding="utf8") as stream:
                    json.dump(summary, stream, ensure_ascii=False, indent=2)
                    stream.write("\n")
                    stream.flush()
                    os.fsync(stream.fileno())
                os.replace(pending, report)
            finally:
                pending.unlink(missing_ok=True)
        report_progress()
        try:
            for change in plan:
                result = apply_workspace(change)
                summary["selected"].append(result)
                report_progress()
        except Exception as exc:
            summary["status"] = "BLOCKED_PARTIAL" if summary["selected"] else "BLOCKED_BEFORE_CHANGE"
            summary["error"] = str(exc)
            report_progress()
            raise
        summary["applied"] = True
        summary["status"] = "LOCAL_CANONICAL_REVISION_SELECTED"
        report_progress()
    return summary


def main(argv=None):
    parser = argparse.ArgumentParser(description="V5.17 local-only audited accepted precedence")
    parser.add_argument("--locals", required=True, type=Path)
    parser.add_argument("--private-dir", required=True, type=Path)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args(argv)
    try:
        summary = evolve_all(args.locals, args.private_dir, apply=args.apply)
    except (v11.V11Error, OSError, ValueError, KeyError, TypeError) as exc:
        parser.exit(2, f"BLOCKED: {exc}\n")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

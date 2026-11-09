#!/usr/bin/env python3
"""Kit v11 read-only verification of an *explicit* existing workspace.

No init, register-artifact, enable-v11, build-v9, push, or canonical file write.
Do not infer workspace identities from UNESCO or Wikidata candidates.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

PROFILE = 'koa.unesco-mt1-10-kit-v11-readonly-gate/1.0'
KIT_TOOL = Path(__file__).resolve().parent / 'kristal.py'
ID_RE = re.compile(r'^K(Q|P|A|S)[1-9][0-9]*$')
KIND = {'KQ':'entity','KP':'property','KA':'assertion','KS':'source'}

class KitGateError(ValueError): pass

def _safe_relative(root: Path, rel: str) -> Path:
    if not isinstance(rel, str) or not rel or '\\' in rel or ':' in rel:
        raise KitGateError('Chemin v11 unsafe')
    p = Path(rel)
    if p.is_absolute() or any(x in ('..', '.') for x in p.parts):
        raise KitGateError('Chemin v11 unsafe')
    target = root / p
    if target.resolve() != root.resolve() and not target.resolve().is_relative_to(root.resolve()):
        raise KitGateError('Chemin v11 hors workspace')
    if target.is_symlink() or not target.is_file() or target.stat().st_size > 8_000_000:
        raise KitGateError('Artefact v11 absent / non regulier')
    return target

def inspect(workspace: str | Path | None = None, *, kit_tool: Path = KIT_TOOL):
    result = {
        'format':PROFILE, 'branch':'unesco-mt1-10',
        'workspace_supplied':workspace is not None,
        'workspace_branch_binding':'NOT_ESTABLISHED',
        'workspace_v11_status':'NOT_CHECKED_NO_EXPLICIT_WORKSPACE',
        'kit_check_v11_executed':False, 'registry':{},
        'canonical_writes':0, 'enable_v11_called':False,
        'build_v9_called':False, 'publication_authorized':False,
    }
    if workspace is None:
        return result
    root = Path(workspace).expanduser().resolve()
    if not root.is_dir() or Path(workspace).is_symlink():
        raise KitGateError('Workspace explicite absent ou lien symbolique')
    if not kit_tool.is_file():
        raise KitGateError('CLI Kit v11 introuvable')
    config = root/'.kristal/v11/authoring.json'
    if config.is_symlink() or not config.is_file():
        result['workspace_v11_status'] = 'V11_PROFILE_ABSENT'
        return result
    if config.stat().st_size > 500_000:
        raise KitGateError('Profil v11 anormalement volumineux')
    data = json.loads(config.read_text('utf-8-sig'))
    if (data.get('format') != 'kristal.authoring-v11-profile/1.0'
            or data.get('semantic_profile') != 'kristal.semantic-identity/11.0'):
        raise KitGateError('Profil Kit v11 inattendu')
    registry_path = _safe_relative(root, data.get('registry'))
    crosswalk_path = _safe_relative(root, data.get('crosswalk'))
    registry_bytes = registry_path.read_bytes()
    registry_data = json.loads(registry_bytes.decode('utf-8-sig'))
    if (registry_data.get('schema_version') != '11.0'
            or registry_data.get('artifact_type') != 'kristal_identity_registry'):
        raise KitGateError('Registre v11 incompatible')
    completed = subprocess.run([sys.executable, str(kit_tool), 'check-v11', str(root)],
                               capture_output=True, text=True, timeout=60)
    result['kit_check_v11_executed'] = True
    if completed.returncode:
        result['workspace_v11_status'] = 'KIT_CHECK_V11_FAILED'
        result['check_detail'] = (completed.stderr or completed.stdout)[-1000:]
        return result
    ids = {}
    for entry in registry_data.get('identities', []):
        ident = entry.get('id')
        kind = entry.get('kind')
        if (not isinstance(ident,str) or not ID_RE.fullmatch(ident)
                or KIND[ident[:2]] != kind or ident in ids):
            raise KitGateError('Identite incoherente dans registre')
        ids[ident] = {'kind':kind, 'status':entry.get('status')}
    workspace_meta_path=root/'kristal.workspace.json'
    if workspace_meta_path.is_symlink() or not workspace_meta_path.is_file():
        raise KitGateError('Metadonnees workspace manquantes')
    workspace_meta=json.loads(workspace_meta_path.read_text('utf-8-sig'))
    result['workspace_slug']=workspace_meta.get('slug')
    result['workspace_branch_binding']=('EXPLICIT_SLUG_MATCH' if workspace_meta.get('slug')=='unesco-mt1-10'
                                        else 'NOT_ESTABLISHED')
    result['workspace_v11_status']='EXISTING_WORKSPACE_KIT_CHECK_V11_PASSED'
    crosswalk=json.loads(crosswalk_path.read_text('utf-8-sig'))
    accepted=[]
    for mapping in crosswalk.get('mappings',[]):
        if mapping.get('status')=='accepted' and mapping.get('relation')=='exactMatch':
            local=mapping.get('local_ref') or {}
            external=mapping.get('external_ref') or {}
            review=mapping.get('review') or {}
            accepted.append({'KQ_or_KP':local.get('id'), 'external_id':external.get('id'),
                             'decision_id':review.get('decision_id'),
                             'evidence_refs':review.get('evidence_refs',[])})
    result['accepted_exact_matches_in_existing_workspace']=accepted
    result['registry']={'namespace_id':registry_data.get('namespace_id'),
                        'sha256':hashlib.sha256(registry_bytes).hexdigest(),
                        'identities':ids, 'identity_count':len(ids)}
    result['workspace_read_only_path']=str(root)
    return result

def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--workspace',type=Path)
    args = p.parse_args(argv)
    print(json.dumps(inspect(args.workspace),ensure_ascii=False,indent=2,sort_keys=True))
    return 0

if __name__ == '__main__':
    try:sys.exit(main())
    except (KitGateError,ValueError,OSError,KeyError,TypeError,subprocess.TimeoutExpired,json.JSONDecodeError) as exc:
        print('KIT V11 READONLY BLOQUE: '+str(exc),file=sys.stderr);sys.exit(2)

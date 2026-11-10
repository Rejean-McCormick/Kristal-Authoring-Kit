#!/usr/bin/env python3
"""Read-only Branch 02 checks: Framework draft.4 <-> Kit <-> diK schema bytes.

No migration, dictionary registration, activation, external network call or
producer-owned file write. This is an explicit *local* compatibility campaign,
not a complete cross-repository TCK, real-world Wikidata qualification or
semantic/publication approval.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.qualify_framework_v11 import qualify, verify_pin, QualificationError


def digest(file: Path):
    return hashlib.sha256(file.read_bytes()).hexdigest()


def verify_dik_source(framework: Path, dik: Path) -> dict:
    dik = dik.resolve()
    external = dik/'src/dik/_framework/schemas/v11'
    canonical = framework/'schemas/v11'
    if not external.is_dir() or not (dik/'pyproject.toml').is_file():
        raise QualificationError('diK source is missing or incomplete')
    # Avoid interpreting an old/new project as the currently selected alpha.7.
    pyproject = (dik/'pyproject.toml').read_text(encoding='utf-8')
    if not any(s in pyproject for s in ('version = "1.0.0a7"', "version = '1.0.0a7'")):
        raise QualificationError('diK version is not the approved alpha.7 comparison subject')
    ours = {p.name: p for p in canonical.glob('*.schema.json')}
    theirs = {p.name: p for p in external.glob('*.schema.json')}
    if len(ours) != 11 or ours.keys() != theirs.keys():
        raise QualificationError('diK vendored Framework schema inventory drift')
    for name, src in ours.items():
        if digest(src) != digest(theirs[name]):
            raise QualificationError('diK vendored Framework schema drift: ' + name)
    return {'dik_source':'explicit-local-alpha.7','v11_schema_count':len(ours),
            'schema_byte_parity':True,
            'draft3_to_draft4_semantic_compatibility':'not_inferred_beyond_unchanged_schema_bytes'}


def check(framework: Path, dik: Path | None = None, workspace: Path | None = None) -> dict:
    framework = Path(framework).resolve()
    workspace = Path(workspace).resolve() if workspace is not None else ROOT/'examples/demo-semantic-v11'
    pin = verify_pin(framework)
    if (ROOT/'VERSION').read_text(encoding='utf-8').strip() != '4.0.0-draft.4':
        raise QualificationError('Authoring Kit version drift')
    parts = [workspace/'canon/domain/v11'/p for p in ('graph.json','registry.json','crosswalk.json','dictionaries/catalog.json')]
    if not all(f.is_file() for f in parts):
        raise QualificationError('Selected semantic workspace source is incomplete')
    before = [digest(f) for f in parts]
    result = qualify(workspace, framework, locales=['fr','fr-CA'])
    if [digest(f) for f in parts] != before:
        raise QualificationError('Qualification unexpectedly modified canonical source')
    dik_report = verify_dik_source(framework,Path(dik)) if dik is not None else None
    return {
        'format':'kristal.branch02-local-interop-check/1.0',
        'classification':'LOCAL_SOURCE_COMPATIBILITY_NOT_FULL_TCK',
        'kit_version':'4.0.0-draft.4', 'framework_version':pin['version'],
        'framework_pin_profile':pin['profile'],
        'framework_pinned_file_count':len(pin['files']),
        'workspace_graph_sha256':result['graph_sha256'],
        'workspace_catalog_sha256':result['catalog_sha256'],
        'framework_reference_coverage_match':result['reference_coverage_match'],
        'diK':dik_report, 'canonical_workspace_modified':False,
        'approved_to_publish':False,'approved_to_activate':False,
    }


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--framework',type=Path,required=True)
    p.add_argument('--dik',type=Path,help='Optional explicit diK alpha.7 checkout for exact schema parity')
    p.add_argument('--workspace',type=Path,help='Read-only existing v11 workspace (default shipped demo)')
    args=p.parse_args(argv)
    try:
        result=check(args.framework,args.dik,args.workspace)
    except (QualificationError,ValueError,KeyError,TypeError,OSError,ImportError) as exc:
        p.exit(1,'Branch02 interop refused: '+str(exc)+'\n')
    print(json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2))

if __name__=='__main__': main()

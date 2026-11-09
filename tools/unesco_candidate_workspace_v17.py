#!/usr/bin/env python3
"""Prepare isolated private *copy* of an existing Kit-validated UNESCO v11 candidate.

The source Workbench and canonical registries are strictly read-only. Additional
editorial information is placed only below derived/; no v11 identity mutation.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys

class CandidateKitError(ValueError): pass

def sha(raw):return hashlib.sha256(raw).hexdigest()
def jb(obj):return (json.dumps(obj,ensure_ascii=False,indent=2,sort_keys=True)+'\n').encode('utf-8')

def _check(workspace:Path,kit:Path):
    if not kit.is_file() or kit.is_symlink():raise CandidateKitError('Kit officiel absent')
    for cmd in ('check','check-v11'):
        p=subprocess.run([sys.executable,str(kit),cmd,str(workspace)],capture_output=True,text=True,timeout=90)
        if p.returncode:raise CandidateKitError('Kit '+cmd+' refuse le workspace: '+(p.stderr or p.stdout)[-700:])
    return True

def prepare(source:Path,destination:Path,kit:Path,editorial:dict,alignment:dict):
    source=Path(source); destination=Path(destination)
    if source.is_symlink() or not source.is_dir():raise CandidateKitError('Source Workbench invalide')
    if destination.exists():raise CandidateKitError('Destination deja presente')
    if not _check(source,kit):raise CandidateKitError('Workbench non valide')
    # Clone only bounded, ordinary files. Prevent symlink traversal and accidental
    # copying of large dump/database/cache data into private output.
    original_files=[];bytes_total=0
    for entry in sorted(source.rglob('*')):
        rel=entry.relative_to(source)
        if any(s in ('.git','node_modules','__pycache__','.venv') for s in rel.parts):continue
        if entry.is_symlink():raise CandidateKitError('Lien symbolique interdit dans le Workbench')
        if not entry.is_file():continue
        if entry.stat().st_size>15_000_000:raise CandidateKitError('Un artefact source est trop volumineux')
        bytes_total+=entry.stat().st_size
        if len(original_files)>=300 or bytes_total>32_000_000:raise CandidateKitError('Workspace hors limite de copie')
        original_files.append(entry)
    if len(original_files)<10:raise CandidateKitError('Source v11 incomplete')
    destination.mkdir(parents=True)
    src_shas={}
    for p in original_files:
        rel=p.relative_to(source);target=destination/rel;target.parent.mkdir(parents=True,exist_ok=True)
        original=p.read_bytes();target.write_bytes(original)
        src_shas[rel.as_posix()]=sha(original)
    dest_derived=destination/'derived/unesco-mt1-10'
    dest_derived.mkdir(parents=True,exist_ok=True)
    (dest_derived/'editorial-candidate-v17.json').write_bytes(jb(editorial))
    (dest_derived/'identity-alignment-v17.json').write_bytes(jb(alignment))
    (dest_derived/'PROVENANCE_V17.json').write_bytes(jb({'format':'koa.unesco-v17-derived-workspace/1.0',
      'original_workspace_files_sha256':src_shas,'editorial_not_canonical':True,
      'no_KA_or_KS_approved':True,'publication_authorized':False}))
    _check(destination,kit)
    for rel,expected in src_shas.items():
        if sha((destination/rel).read_bytes())!=expected:
            raise CandidateKitError('Le Kit a modifie une piece de registre pendant le controle: '+rel)
    return {'kit_check':'PASSED','kit_check_v11':'PASSED','workspace_status':'PRIVATE_WORKBENCH_CLONE_PROVISIONAL',
      'copied_files':len(src_shas),'source_files_sha256':src_shas,
      'derived_editorial_files':3,'canonical_registry_changed':False,
      'build_v9_called':False,'enable_v11_called':False,'github_push':False}

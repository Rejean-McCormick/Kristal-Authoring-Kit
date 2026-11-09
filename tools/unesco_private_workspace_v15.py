#!/usr/bin/env python3
"""Initialize an *actual Kit* private UNESCO workspace, with no v11 canonical activation.

This is deliberately a blank v9/v10 Local workspace envelope from the real Kit
CLI. UNESCO candidates are copied only as derived research, never in canon.
The caller must supply a new empty target within its private staging directory.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import subprocess
import sys

KIT=Path(__file__).resolve().parent/'kristal.py'
BRANCH='unesco-mt1-10'
class WorkspaceError(ValueError):pass

def jbytes(obj):
    return (json.dumps(obj,ensure_ascii=False,sort_keys=True,indent=2)+'\n').encode('utf-8')
def digest(raw):return hashlib.sha256(raw).hexdigest()

def command(*args,kit=KIT):
    if not kit.is_file() or kit.is_symlink():raise WorkspaceError('CLI officiel du Kit absent')
    p=subprocess.run([sys.executable,str(kit),*map(str,args)],capture_output=True,text=True,timeout=90)
    if p.returncode:raise WorkspaceError('Kit '+str(args[0])+' refuse: '+(p.stderr or p.stdout)[-1500:])
    return p.stdout

def make(target:Path,graph:dict,graph_sha:str,*,kit=KIT):
    target=Path(target)
    if target.exists() or target.is_symlink():raise WorkspaceError('Workspace deja present: refuser toute reinitialisation')
    if (graph.get('branch')!=BRANCH or len(graph.get('nodes',[]))!=41 or
        len(graph.get('candidate_statements',[]))!=85 or len(graph.get('skos_internal_observations',[]))!=61 or
        graph.get('canonical_graph_built') is not False or graph.get('approved_KS')!=0):
        raise WorkspaceError('Graphe editorial v14 non conforme')
    target.parent.mkdir(parents=True,exist_ok=True)
    command('init',target,'--slug',BRANCH,'--title','UNESCO Educational Policy', '--profile','open',kit=kit)
    meta=json.loads((target/'kristal.workspace.json').read_text('utf-8'))
    if meta.get('slug')!=BRANCH or meta.get('portable_ai',{}).get('enabled') or (target/'.kristal/v11/authoring.json').exists():
        raise WorkspaceError('Profil workspace incorrect ou v11 active')
    # All imported material is noncanonical *derived research*, never under canon/.
    research=target/'derived/unesco-mt1-10'
    research.mkdir(parents=True,exist_ok=True)
    research_file=research/'candidat_editorial_sans_KQ.json'
    research_file.write_bytes(jbytes(graph))
    (target/'docs/UNESCO_NON_CANONIQUE.md').write_text(
        '# UNESCO Educational Policy — recherche privee\n\n'
        'Ce workspace a ete initialise par le Kit officiel avec le slug '+BRANCH+'.\n\n'
        'Son graphe UNESCO candidat est **derive**, dans derived/unesco-mt1-10/.\n'
        'Le dossier canon/ ne contient aucun registre KQ/KP/KA/KS cree par ce programme.\n'
        'Aucune activation v11, aucun enregistrement canonique, aucune construction ou publication.\n'
        'Le profil v11 ne doit etre active qu apres decisions humaines et preuves KS attestees.\n', encoding='utf-8',newline='\n')
    command('check',target,kit=kit)
    if (target/'.kristal').exists() or list((target/'canon/domain').glob('v11/*')):
        raise WorkspaceError('Activation v11 inattendue')
    return {'format':'koa.unesco-mt1-10-kit-workspace-scaffold/1.0',
        'branch':BRANCH,'workspace_type':'KIT_LOCAL_WORKSPACE_INITIALIZED_NONCANONICAL',
        'workspace_slug':meta['slug'],'kit_check':'PASSED',
        'source_editorial_graph_sha256':graph_sha,
        'derived_research_sha256':digest(research_file.read_bytes()),
        'v11_profile_created':False,'canonical_IDs_created':0,
        'enable_v11_called':False,'build_v9_called':False,'publication_authorized':False}

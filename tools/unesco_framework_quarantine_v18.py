#!/usr/bin/env python3
"""UNESCO V18: isolate an unsigned Workbench dictionary without inventing approvals.

Input: the *already generated* V17 private product on D:.
Output: a NEW V18 private copy, preserving the source Workbench and V17 output.

Only the active dictionary catalog of the new copy is changed. The original
external UNESCO lexical layer is kept byte-for-byte, and its previous catalog
is saved in derived/ with an explicit quarantine receipt. Real Kit check,
Kit check-v11, pinned Framework and Integration Pack verification run on the
new copy. Those are STRUCTURAL checks, never canonical-source approval.

No enable/build/publish/GitHub commands. Fail closed on differences and never
replace user data or previous output.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
import tempfile

BRANCH = 'unesco-mt1-10'
DEFAULT_WORK = Path(r'D:\EncyKlopedia\30_working\unesco_mt1_10\autopilot_concept10_puis_41')
DEFAULT_V17 = 'semantic_stage_v17_integrated_product'
DEFAULT_V18 = 'semantic_stage_v18_framework_quarantine'
CLONE = 'workbench_v11_candidat_prive'
CATALOG = 'canon/domain/v11/dictionaries/catalog.json'
LEXICON = 'canon/domain/v11/dictionaries/unesco-skos-en.jsonl'
DEST_CLONE = 'workbench_v11_quarantaine_privee'
QUARANTINE_DIR = 'derived/unesco-mt1-10/quarantine-v18'
MAX_FILE_BYTES = 18_000_000
MAX_FILES = 480
MAX_TOTAL_BYTES = 48_000_000

class V18Error(ValueError):
    pass


def checksum(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def json_bytes(data: dict) -> bytes:
    return (json.dumps(data, ensure_ascii=False, sort_keys=True, indent=2) + '\n').encode('utf-8')


def safe_rel(rel: str) -> PurePosixPath:
    if not isinstance(rel, str) or not rel or '\\' in rel or ':' in rel:
        raise V18Error('Chemin relatif non fiable: ' + str(rel))
    path = PurePosixPath(rel)
    if path.is_absolute() or any(p in ('', '.', '..') for p in path.parts):
        raise V18Error('Chemin non fiable: ' + rel)
    return path


def safe_bytes(path: Path) -> bytes:
    if path.is_symlink() or not path.is_file():
        raise V18Error('Fichier manquant ou symbolique: ' + str(path))
    if path.stat().st_size > MAX_FILE_BYTES:
        raise V18Error('Fichier hors limite: ' + str(path))
    return path.read_bytes()


def read_json(path: Path) -> dict:
    try:
        return json.loads(safe_bytes(path).decode('utf-8-sig'))
    except (ValueError, UnicodeError) as e:
        raise V18Error('JSON invalide: ' + str(path)) from e


def bounded_files(directory: Path) -> dict[str, bytes]:
    if directory.is_symlink() or not directory.is_dir():
        raise V18Error('Dossier manquant ou lien symbolique: ' + str(directory))
    files, total = {}, 0
    for item in sorted(directory.rglob('*')):
        if item.is_symlink():
            raise V18Error('Lien symbolique interdit: ' + str(item))
        if item.is_dir():
            continue
        if not item.is_file():
            raise V18Error('Objet non régulier: ' + str(item))
        rel = item.relative_to(directory).as_posix()
        safe_rel(rel)
        if len(files) >= MAX_FILES:
            raise V18Error('Trop de fichiers dans le dossier privé')
        blob = safe_bytes(item)
        total += len(blob)
        if total > MAX_TOTAL_BYTES:
            raise V18Error('Dossier privé hors limite')
        files[rel] = blob
    return files


def verify_v17(stage17: Path) -> tuple[dict, dict[str, bytes]]:
    if stage17.is_symlink() or not stage17.is_dir():
        raise V18Error('Etape v17 absente ou symbolique: ' + str(stage17))
    report = read_json(stage17/'RAPPORT_PRODUIT_V17.json')
    if not (report.get('branch') == BRANCH
            and report.get('status') == 'PRIVATE_INTEGRATED_PRODUCT_READY_FINAL_RELEASE_BLOCKED'
            and report.get('editorial_concepts') == 41
            and report.get('editorial_statements') == 85
            and report.get('private_english_reading_pages') == 41
            and report.get('human_admissions_pending') == 191
            and report.get('canonical_assertions_created') == 0
            and report.get('C1_C4_qualified') is False
            and report.get('github_push') is False):
        raise V18Error('Le rapport v17 ne correspond pas au produit privé attendu')
    manifest = read_json(stage17/'MANIFESTE_V17.json')
    indexed = manifest.get('files_sha256')
    if not (manifest.get('branch') == BRANCH
            and manifest.get('canonical_approval_not_performed') is True
            and manifest.get('public_release_authorized') is False
            and isinstance(indexed, dict) and len(indexed) >= 20):
        raise V18Error('Manifeste v17 incomplet ou non privé')
    files = bounded_files(stage17)
    if set(files) != set(indexed) | {'MANIFESTE_V17.json'}:
        raise V18Error('Fichiers v17 absents ou non indexés')
    for rel, expected in indexed.items():
        safe_rel(rel)
        if not isinstance(expected,str) or not re.fullmatch('[0-9a-f]{64}', expected) or checksum(files[rel]) != expected:
            raise V18Error('Empreinte v17 divergente: ' + str(rel))
    # The source manifests must cover the original dictionary and its catalog.
    for rel in (f'{CLONE}/{CATALOG}', f'{CLONE}/{LEXICON}',
                f'{CLONE}/.kristal/v11/authoring.json'):
        if rel not in indexed:
            raise V18Error('Workspace v11 absent du manifeste v17: ' + rel)
    return report, files


def analyze_lexicon(copyfiles: dict[str,bytes]) -> tuple[dict, dict, bytes, bytes]:
    orig_catalog = copyfiles.get(CATALOG)
    orig_layer = copyfiles.get(LEXICON)
    if orig_catalog is None or orig_layer is None:
        raise V18Error('Dictionnaire source UNESCO absent')
    try:
        catalog = json.loads(orig_catalog.decode('utf-8-sig'))
        rows = [json.loads(line) for line in orig_layer.decode('utf-8-sig').splitlines() if line.strip()]
    except (ValueError,UnicodeError) as exc:
        raise V18Error('Dictionnaire UNESCO illisible') from exc
    langs = catalog.get('languages')
    if not (catalog.get('schema_version') == '11.0'
            and catalog.get('artifact_type') == 'kristal_dictionary_catalog'
            and isinstance(langs,list) and len(langs) == 1
            and langs[0].get('tag') == 'en'
            and langs[0].get('fallbacks') == []
            and len(langs[0].get('layers',[])) == 1):
        raise V18Error('Topologie du catalogue modifiée : revue manuelle nécessaire')
    layer = langs[0]['layers'][0]
    if not (layer.get('kind') == 'external' and layer.get('source_system') == 'unesco_skos'
            and layer.get('path') == 'unesco-skos-en.jsonl'
            and layer.get('sha256') == checksum(orig_layer)):
        raise V18Error('La couche UNESCO ne correspond pas au SHA du catalogue')
    if (len(rows) != 44 or len({r.get('semantic_id') for r in rows}) != 44
        or sum(bool(re.fullmatch(r'KQ[1-9][0-9]*',str(r.get('semantic_id','')))) for r in rows) != 41
        or {r.get('semantic_id') for r in rows if str(r.get('semantic_id','')).startswith('KP')} != {'KP1001','KP1002','KP1003'}):
        raise V18Error('41 KQ et 3 KP UNESCO/SKOS uniques requis')
    for row in rows:
        alignment = row.get('alignment')
        kid = str(row.get('semantic_id',''))
        uri = str(row.get('source_record_id',''))
        valid_uri = (bool(re.fullmatch(r'https?://vocabularies\.unesco\.org/thesaurus/concept[0-9]+',uri))
                     if kid.startswith('KQ') else uri == {
                       'KP1001':'https://www.w3.org/2004/02/skos/core#broader',
                       'KP1002':'https://www.w3.org/2004/02/skos/core#narrower',
                       'KP1003':'https://www.w3.org/2004/02/skos/core#related'}.get(kid))
        if not (bool(re.fullmatch(r'K[QP][1-9][0-9]*', kid)) and valid_uri
                and row.get('namespace_id') == catalog['namespace_id']
                and row.get('source_snapshot') == layer.get('source_snapshot')
                and row.get('source_system') == layer.get('source_system')
                and row.get('language') == 'en'
                and row.get('license') == layer.get('license')
                and isinstance(alignment,dict)
                and 'decision_id' not in alignment and 'reviewer' not in alignment
                and 'review' not in row):
            raise V18Error('Une fiche source a changé ou comporte une décision à respecter')
    # Explicitly keep original 41 rows unchanged. No alias conversion or synthetic review.
    revised = json.loads(orig_catalog.decode('utf-8-sig'))
    revised['catalog_id'] = catalog['catalog_id'] + '-quarantine-unapproved-v18'
    revised['languages'][0]['layers'] = []
    return catalog, revised, orig_catalog, orig_layer


def run_check(command: list[str], name: str, *, json_result: bool=True):
    try:
        proc = subprocess.run(command,capture_output=True,text=True,timeout=180)
    except subprocess.TimeoutExpired as exc:
        raise V18Error(name + ': délai de validation dépassé') from exc
    if proc.returncode:
        raise V18Error(name + ': ' + (proc.stderr or proc.stdout)[-1300:])
    if not json_result:
        return proc.stdout[-2000:]
    try:
        result = json.loads(proc.stdout)
    except ValueError as exc:
        raise V18Error(name + ': réponse JSON invalide') from exc
    return result


def official_checks(repo: Path, workspace: Path) -> dict:
    kit = repo/'Kristal/Kristal-Authoring-Kit/tools/kristal.py'
    qualifier = repo/'Kristal/Kristal-Authoring-Kit/scripts/qualify_framework_v11.py'
    framework = repo/'Kristal/Kristal-Framework'
    integration = repo/'Kristal/Kristal-Integration-Pack'
    for p in (kit,qualifier,framework/'VERSION',integration/'contracts/v11-framework-pin.json'):
        if not p.is_file() or p.is_symlink():
            raise V18Error('Outil officiel manquant: ' + str(p))
    # Read-only Kit checks; no build/enable/publish actions.
    kit_standard = run_check([sys.executable,str(kit),'check',str(workspace)], 'Kit check', json_result=False)
    kit_v11 = run_check([sys.executable,str(kit),'check-v11',str(workspace)], 'Kit check-v11')
    independent = run_check([sys.executable,str(qualifier),'--project',str(workspace),
        '--framework',str(framework),'--integration-pack',str(integration)], 'Framework + Integration Pack')
    if not (independent.get('valid') is True
            and independent.get('reference_coverage_match') is True
            and independent.get('integration_pack') == 'coverage-and-check-matched'):
        raise V18Error('Qualification indépendante et Integration Pack non concordants')
    coverage = run_check([sys.executable,str(kit),'coverage-v11',str(workspace), '--locales','en'], 'Kit coverage-v11')
    loc = next((x for x in coverage.get('locales',[]) if x.get('tag') == 'en'),None)
    if not (loc and loc['KQ']['direct'] == 0 and loc['KP']['direct'] == 0
            and loc['KQ']['missing'] == 41 and loc['KP']['missing'] == 3):
        raise V18Error('Couverture lexicale anormalement qualifiée après retrait')
    return {'kit_check_passed':True,'kit_v11_check_passed':True,
        'independent_framework_technical_valid':True,
        'integration_pack_checked':True,
        'kit_standard_check':kit_standard,'kit_v11_check':kit_v11,
        'framework_qualification':independent,'lexical_coverage_en':coverage}


def workspace_files(stage17_files: dict[str,bytes]) -> dict[str,bytes]:
    prefix = CLONE + '/'
    result = {k[len(prefix):]:raw for k,raw in stage17_files.items() if k.startswith(prefix)}
    if len(result) < 10:
        raise V18Error('Copie Workbench v17 incomplète')
    return result


def write_workspace(root: Path, files: dict[str,bytes]) -> None:
    root.mkdir(parents=True)
    for rel, raw in files.items():
        dest = root / Path(*safe_rel(rel).parts)
        dest.parent.mkdir(parents=True,exist_ok=True)
        dest.write_bytes(raw)


def verify_existing(out: Path, stage17: Path, repo: Path, *, recheck: bool) -> dict:
    if out.is_symlink() or not out.is_dir():
        raise V18Error('Dossier v18 absent ou symbolique')
    files = bounded_files(out)
    if 'MANIFESTE_V18.json' not in files:
        raise V18Error('Manifeste v18 absent')
    manifest = read_json(out/'MANIFESTE_V18.json')
    pinned = manifest.get('files_sha256')
    if (manifest.get('branch') != BRANCH or not isinstance(pinned,dict)
        or set(files) != set(pinned)|{'MANIFESTE_V18.json'}):
        raise V18Error('Dossier v18 altéré ou fichiers additionnels')
    for rel,expected in pinned.items():
        safe_rel(rel)
        if checksum(files[rel]) != expected:
            raise V18Error('Fichier v18 modifié, ne pas écraser: '+rel)
    current_v17 = checksum(safe_bytes(stage17/'MANIFESTE_V17.json'))
    if manifest.get('source_v17_manifest_sha256') != current_v17:
        raise V18Error('Source v17 modifiée; utiliser un nouveau dossier de sortie')
    report = read_json(out/'RAPPORT_V18.json')
    if not (report.get('status') == 'PRIVATE_FRAMEWORK_TECHNICAL_CHECK_PASSED_LEXICON_QUARANTINED'
            and report.get('approved_KQ_KP_KA_KS') == 0
            and report.get('public_release_authorized') is False):
        raise V18Error('Rapport v18 incohérent')
    if recheck:
        new_result = official_checks(repo,out/DEST_CLONE)
        if new_result['framework_qualification'] != read_json(out/'QUALIFICATION_FRAMEWORK_V18.json')['framework_qualification']:
            raise V18Error('Nouvelle qualification diverge du rapport initial')
    return {**report,'operation':'DEJA_PRESENT_INTACT','output':str(out)}


def execute(stage17: Path, repo: Path, out: Path, *, audit: bool=False) -> dict:
    stage17 = Path(stage17).resolve(strict=True)
    repo = Path(repo).resolve(strict=True)
    out = Path(out)
    if not out.name.startswith('semantic_stage_v18_') or not re.fullmatch(r'semantic_stage_v18_[a-zA-Z0-9_-]{3,80}',out.name):
        raise V18Error('Nom du dossier de sortie v18 invalide')
    if out.is_symlink() or out.resolve() == stage17 or out.resolve().is_relative_to(stage17):
        raise V18Error('Destination dangereuse ou sous la source v17')
    if out.parent.resolve() != stage17.parent.resolve():
        raise V18Error('La sortie v18 doit être un dossier frère de v17 sur D:')
    if out.exists():
        # Verify the existing result rather than overwriting it.
        verify_v17(stage17)
        return verify_existing(out,stage17,repo,recheck=audit)
    if audit:
        raise V18Error('Sortie v18 absente : audit impossible')
    v17_report, full_stage = verify_v17(stage17)
    files = workspace_files(full_stage)
    old, new, raw_catalog, raw_layer = analyze_lexicon(files)
    new_catalog = json_bytes(new)
    with tempfile.TemporaryDirectory(prefix='_unesco-v18-staging-',dir=out.parent) as temp:
        stage = Path(temp)/out.name
        copied = stage/DEST_CLONE
        write_workspace(copied, files)
        active = copied/Path(*safe_rel(CATALOG).parts)
        active.write_bytes(new_catalog)
        quarantine = copied/Path(*safe_rel(QUARANTINE_DIR).parts)
        quarantine.mkdir(parents=True,exist_ok=True)
        (quarantine/'catalog-original.json').write_bytes(raw_catalog)
        (quarantine/'receipt.json').write_bytes(json_bytes({
            'format':'koa.unesco-mt1-10-dictionary-quarantine/1.0',
            'original_catalog_sha256':checksum(raw_catalog),
            'original_layer_sha256':checksum(raw_layer),
            'original_layer_path':LEXICON,
            'quarantined_entries':44,'quarantined_KQ':41,'quarantined_KP':3,
            'reason':'source labels not approved: synonyms format and absent alignment decision_id/reviewer',
            'original_layer_bytes_preserved':True,
            'new_active_catalog_sha256':checksum(new_catalog),
            'no_reviewer_invented':True,'no_KS_approved':True,'publication_authorized':False}))
        official = official_checks(repo,copied)
        summary = {
            'format':'koa.unesco-mt1-10-framework-quarantine/1.0',
            'branch':BRANCH,
            'status':'PRIVATE_FRAMEWORK_TECHNICAL_CHECK_PASSED_LEXICON_QUARANTINED',
            'source_v17_report_sha256':checksum(safe_bytes(stage17/'RAPPORT_PRODUIT_V17.json')),
            'source_v17_workspace_files':len(files),
            'unsigned_unesco_lexicon_rows_preserved':44, 'unsigned_KQ_labels_preserved':41, 'unsigned_KP_labels_preserved':3,
            'active_unapproved_external_layers':0,
            'framework_pinned_technical_check_passed':True,
            'integration_pack_technical_check_passed':True,
            'kit_check_v11_passed':True,
            'direct_english_lexical_coverage_KQ':0,
            'direct_english_lexical_coverage_KP':0,
            'provisional_KQ':41,'provisional_KP':3,'provisional_KS':1,
            'approved_KQ_KP_KA_KS':0,'human_admissions_pending':191,
            'multilingual_realizations':0,'official_articles_generated':0,
            'canonical_kristal_approved':False,'public_release_authorized':False,
            'git_push':False,
            'next':'Review and attest UNESCO lexicon with authorized decisions; qualify KS/KQ/KP/KA and real GF before public release'}
        (stage/'RAPPORT_V18.json').write_bytes(json_bytes(summary))
        (stage/'QUALIFICATION_FRAMEWORK_V18.json').write_bytes(json_bytes(official))
        (stage/'README_V18_PRIVE.md').write_text(
            '# UNESCO — vérification technique v18, privée\n\n'
            'Le Framework + Integration Pack valident une COPIE DU WORKSPACE.\n'
            'Les 44 enregistrements (41 KQ + 3 KP) non approuvés restent intacts mais sont détachés du catalogue actif.\n'
            'La couverture lexicale anglaise du catalogue actif est 0 KQ / 0 KP.\n'
            'Ce résultat NE vaut PAS validation des connaissances, des preuves KS ni autorisation de publication.\n'
            'Ne jamais synchroniser ce workspace vers kristal-public.\n',encoding='utf-8',newline='\n')
        indexed = bounded_files(stage)
        (stage/'MANIFESTE_V18.json').write_bytes(json_bytes({
            'format':'koa.unesco-mt1-10-framework-quarantine-manifest/1.0',
            'branch':BRANCH,'source_v17_manifest_sha256':checksum(safe_bytes(stage17/'MANIFESTE_V17.json')),
            'files_sha256':{rel:checksum(raw) for rel,raw in indexed.items()},
            'canonical_approval_not_performed':True,'public_release_authorized':False}))
        if out.exists():
            raise V18Error('Destination apparue pendant le calcul; refus d’écraser')
        stage.rename(out)
    return {**summary,'operation':'NOUVELLE_COPIE_PRIVEE','output':str(out)}


def main(argv=None):
    default_repo = Path(__file__).resolve().parents[3]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo-root',type=Path,default=default_repo)
    parser.add_argument('--stage17',type=Path,default=DEFAULT_WORK/DEFAULT_V17)
    parser.add_argument('--out',type=Path,default=DEFAULT_WORK/DEFAULT_V18)
    parser.add_argument('--audit',action='store_true',help='Contrôler sans écrire, y compris le Framework officiel')
    args = parser.parse_args(argv)
    print(json.dumps(execute(args.stage17,args.repo_root,args.out,audit=args.audit),ensure_ascii=False,indent=2,sort_keys=True))


if __name__ == '__main__':
    try:
        main()
    except (V18Error,ValueError,KeyError,TypeError,OSError,UnicodeError,json.JSONDecodeError,subprocess.TimeoutExpired) as exc:
        print('UNESCO V18 BLOQUE SANS MODIFIER V17/CANON: '+str(exc),file=sys.stderr)
        sys.exit(2)

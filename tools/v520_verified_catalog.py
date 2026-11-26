"""Add-only V11 catalog evolution from fresh, exact-anchored lexical records.
Caller must capture and validate official-source responses before calling.
No identity, graph or crosswalk edits. Existing labels are immutable.
"""
from __future__ import annotations
import hashlib, json, re, stat, tempfile
from copy import deepcopy
from pathlib import Path, PurePosixPath
import kristal_v11_core as v11


def guard(path):
    path=Path(path).absolute()
    for p in [*reversed(path.parents),path]:
        if p.exists() or p.is_symlink():
            s=p.lstat()
            v11.must(not stat.S_ISLNK(s.st_mode) and not getattr(s,'st_file_attributes',0)&0x400, f'link/reparse refused: {p}')
    return path


def member(root, rel):
    p=PurePosixPath(rel)
    v11.must(not p.is_absolute() and not any(x in ('','.','..') for x in rel.split('/')) and '\\' not in rel and ':' not in rel,'unsafe relative path')
    return guard(root.joinpath(*p.parts))


def sha(b): return hashlib.sha256(b).hexdigest()
def encoded(d): return (json.dumps(d,ensure_ascii=False,sort_keys=True,indent=2)+'\n').encode('utf8')


def same_or_create(p,b):
    guard(p)
    if p.exists(): v11.must(p.is_file() and v11.digest(p)==sha(b),f'immutable target differs: {p}')
    else: v11._write_exclusive_synced(p,b)


def prepare(root, rows, expected, schema_dir):
    """Return immutable in-memory payloads, or None; no workspace writes."""
    from jsonschema import Draft202012Validator
    root=guard(root); profile=member(root,v11.CONFIG); index=member(root,'canon/state.index.json')
    v11.must(v11.digest(profile)==expected[0] and v11.digest(index)==expected[1],'profile or index drift')
    cfg=v11.load_profile(root)
    for role in ('registry','graph','crosswalk','catalog'): member(root,cfg[role])
    old_path=member(root,cfg['catalog']); old=v11.read(old_path)
    for lang in old['languages']:
        for layer in lang['layers']: member(old_path.parent,layer['path'])
    data=v11.validate(root); ns,ids=v11.registry_check(v11.read(data['files']['registry']))
    exact=v11.crosswalk_check(v11.read(data['files']['crosswalk']),ns,ids)
    _,_,all_terms=v11.catalog_check(old_path,ns,ids,exact)
    graph_ids=set(data['KQ'])|set(data['KP'])
    record_validator=Draft202012Validator(v11.read(member(schema_dir,'kristal-wikidata-lexical-record.schema.json')))
    catalog_validator=Draft202012Validator(v11.read(member(schema_dir,'kristal-dictionary-catalog.schema.json')))
    accepted={}; seen=set()
    for r in rows:
        record_validator.validate(r)
        sid,tag=r['semantic_id'],r['language']
        v11.must(r['namespace_id']==ns and exact.get(r['external_id'])==sid,'not an active accepted exact mapping')
        if sid not in graph_ids or sid in all_terms.get(tag,{}): continue
        v11.must((sid,tag) not in seen,'duplicate new lexical cell'); seen.add((sid,tag))
        v11.must(re.fullmatch(r'wbgetentities-sha256-[0-9a-f]{64}',r['source_snapshot']) is not None and type(r.get('source_revision')) is int and r['source_revision']>0,'missing captured source revision')
        accepted.setdefault((tag,r['source_snapshot']),[]).append(r)
    if not accepted:return None
    payloads={}; new=deepcopy(old); langmap={l['tag']:l for l in new['languages']}
    for n,l in enumerate(new['languages']):
        for i,layer in enumerate(l['layers']):
            orig=member(old_path.parent,layer['path']); b=orig.read_bytes()
            v11.must(sha(b)==layer['sha256'],'old layer drift')
            rel=f'layers/old-{n}-{i}'+('.json' if layer['kind']=='curated' else '.jsonl')
            payloads[rel]=b;layer['path']=rel
    for i,((tag,snapshot),recs) in enumerate(sorted(accepted.items())):
        l=langmap.get(tag)
        if l is None:
            l={'tag':tag,'fallbacks':[],'layers':[]};new['languages'].append(l);langmap[tag]=l
        rel=f'layers/v520-{i}.jsonl'; b=b''.join((json.dumps(r,ensure_ascii=False,sort_keys=True,separators=(',',':'))+'\n').encode('utf8') for r in sorted(recs,key=lambda r:r['semantic_id']))
        payloads[rel]=b; layerid='v520-'+sha(b)[:24];v11.must(all(x['layer_id']!=layerid for x in l['layers']),'layer ID conflict')
        l['layers'].append({'layer_id':layerid,'kind':'wikidata','priority':0,'path':rel,'sha256':sha(b),'source_snapshot':snapshot})
    token=sha(encoded([sha(old_path.read_bytes()),sorted((k,sha(v)) for k,v in payloads.items())]))[:24]
    new['catalog_id']=old['catalog_id']+':v520:'+token; catalog_validator.validate(new)
    payloads['catalog.json']=encoded(new)
    with tempfile.TemporaryDirectory() as td:
        stage=Path(td)
        for rel,b in payloads.items():
            p=stage/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
        _,_,after=v11.catalog_check(stage/'catalog.json',ns,ids,exact)
        v11.must(all(after[tag].get(sid)==term for tag,terms in all_terms.items() for sid,term in terms.items()),'existing preferred term changed')
        v11.must(sum(len(x) for x in after.values())-sum(len(x) for x in all_terms.values())==len(seen),'unexpected lexical delta')
    # Pin the old role and shard bytes as well as profile and state.
    pins={cfg[k]:v11.digest(member(root,cfg[k])) for k in ('registry','graph','crosswalk','catalog')}
    for l in old['languages']:
        for layer in l['layers']:
            p=member(old_path.parent,layer['path']);pins[p.relative_to(root).as_posix()]=layer['sha256']
    return {'root':root,'expected':expected,'pins':pins,'config':cfg,'payloads':payloads,'token':token,'count':len(seen),'old_terms':all_terms}


def apply(plan, backup_dir, slug):
    root=plan['root'];profile=member(root,v11.CONFIG);idx=member(root,'canon/state.index.json')
    v11.must((v11.digest(profile),v11.digest(idx))==tuple(plan['expected']),'state/profile drift before apply')
    for rel,h in plan['pins'].items():v11.must(v11.digest(member(root,rel))==h,'role/layer drift before apply')
    v11._assert_no_pending(root)
    v11.must(re.fullmatch(r'[a-z0-9][a-z0-9-]*',slug) is not None,'unsafe slug')
    before=profile.read_bytes();state=idx.read_bytes();backup_dir=guard(backup_dir)
    same_or_create(backup_dir/(slug+'-profile-'+sha(before)+'.json'),before)
    same_or_create(backup_dir/(slug+'-state-'+sha(state)+'.json'),state)
    folder='canon/domain/v11/updates/verified-lexical-v520-'+plan['token']+'/dictionaries'
    for rel,b in plan['payloads'].items():
        p=member(root,folder+'/'+rel);same_or_create(p,b)
    rel=folder+'/catalog.json';artifact='urn:kristal:'+slug+':v11:catalog:v520:'+plan['token']
    candidate=dict(plan['config'],catalog=rel)
    v11.validate(root,candidate,require_registered=False)
    existing=[a for a in v11.read(idx).get('canonical_artifacts',[]) if a.get('path')==rel or a.get('artifact_id')==artifact]
    if existing:
        v11.must(len(existing)==1 and existing[0].get('path')==rel and existing[0].get('artifact_id')==artifact,'conflicting prior registration')
    else:
        v11.register_artifact_recoverably(root,rel=rel,payload=plan['payloads']['catalog.json'],artifact_id=artifact,contract_id='kristal.v11.dictionary-catalog',allow_existing=True)
    v11.validate(root,candidate)
    history=member(root,'.kristal/v11/history/'+sha(before)+'.json');same_or_create(history,before)
    v11.must(profile.read_bytes()==before,'profile changed during registration')
    v11._replace_synced(profile,v11._json_bytes(candidate))
    return {'slug':slug,'catalog':rel,'new_cells':plan['count'],'catalog_sha256':sha(plan['payloads']['catalog.json']),'previous_profile_sha256':sha(before)}

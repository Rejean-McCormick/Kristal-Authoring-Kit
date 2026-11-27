"""Private reader qualification helpers. No canonical authoring or promotion."""
from __future__ import annotations
import importlib.util
from pathlib import Path

def framework_reader(framework):
    p=Path(framework)/'tools/v11/unified_native_v5215.py';s=importlib.util.spec_from_file_location('kristal_unified_reader',p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m

# Explicit native collection contracts; not a heuristic JSON-to-V11 mapper.
COLLECTIONS={
 'k-monetary-system':{
 'canon/epistemic/assumptions.json':[('/items','id','k.monetary.epistemic/assumptions/0.1.0')],
 'canon/epistemic/hypotheses.json':[('/items','id','k.monetary.epistemic/hypotheses/0.1.0')],
 'canon/epistemic/counterarguments.json':[('/items','id','k.monetary.epistemic/counterarguments/0.1.0')],
 'canon/epistemic/multiangle/claims.json':[('/items','id','k.monetary.multiangle/claims/0.1.0')]},
 'pitheory-prime-bridge':{
 'canon/epistemic/claim-ledger.json':[('/claims','id','pitheory-prime-bridge.claim-ledger/2.7.0')],
 'canon/epistemic/research-claims-2026-10-08.json':[('/claims','id','pitheory-prime-bridge.research-claims/0.1.0')]},
 'prime-numbers':{'canon/domain/v9-logical-payload.json':[(f'/registries/{key}/{key}',field,None) for key,field in [('entities','entity_id'),('properties','property_id'),('assertions','assertion_id'),('sources','source_id')]]}}

def native_rows(reader,slug,path,doc):
    f=reader.f;out=[]
    for collection,id_field,fmt in COLLECTIONS.get(slug,{}).get(path,[]):
        if fmt is not None:f.require(doc.get('format')==fmt,'Native format mismatch')
        else:
            reg=reader.pointer(doc,collection.rsplit('/',1)[0]);f.require(reg.get('schema_version')=='7.0' and reg.get('namespace_id')=='kristall-primalite-mecanique','Unexpected prime registry')
        rows=reader.pointer(doc,collection);f.require(isinstance(rows,list),'Native collection must be list');seen=set()
        for i,row in enumerate(rows):
            key=row.get(id_field) if isinstance(row,dict) else None
            f.require(isinstance(key,str) and key.strip() and key not in seen,'Duplicate or missing native ID');seen.add(key)
            out.append((slug,path,collection,key,id_field,collection+'/'+str(i)))
    return out

def candidate_rows(reader,root,result,inventory):
    f=reader.f;read=lambda rel:f.decode(reader.verified(root,rel,inventory[rel]))
    bridge=read('bridge.json');state=read('native-originals/state.json');graph=read('canon/domain/v11/graph.json');cat=read('canon/domain/v11/dictionaries/catalog.json');ns=result['namespace_id'];slug=result['slug']
    f.require(bridge['slug']==slug and bridge['namespace_id']==graph['namespace_id']==cat['namespace_id']==ns,'Candidate scope mismatch');f.require(bridge['source_sha256']==result['source_sha256'],'Source mismatch')
    for k,h in result['source_sha256'].items():reader.verified(root,'native-originals/'+k+'.json',h)
    for p,h in result['candidate_files'].items():f.require(inventory[p]==h,'Candidate role digest mismatch')
    identities=[(ns,x['semantic_id'],slug,x['kind'],x['native_ref'],x['json_pointer'],x['source_sha256']) for x in bridge['entries']];f.require(len(identities)==len({x[1] for x in identities})==result['identities'],'Identity count/uniqueness')
    ga={x['id']:x for x in graph['assertions']};assertions=[];pointers=set()
    for x in bridge['entries']:
        if x['kind']!='assertion':continue
        f.require(x['source']=='state' and x['source_sha256']==result['source_sha256']['state'],'Assertion source mismatch');a=reader.pointer(state,x['json_pointer']);f.require(a['assertion_id']==x['native_ref'] and x['semantic_id'] in ga and x['json_pointer'] not in pointers,'Assertion bridge mismatch');pointers.add(x['json_pointer']);assertions.append((ns,x['semantic_id'],slug,x['json_pointer'],a.get('assertion_status'),a.get('record_role')))
    f.require(len(assertions)==len(state['assertions'])==len(ga)==result['assertion_occurrences'],'Assertion occurrence coverage mismatch')
    labels=[]
    for lang in cat['languages']:
        for layer in lang['layers']:
            rel='canon/domain/v11/dictionaries/'+layer['path'];f.require(inventory[rel]==layer['sha256'],'Layer digest mismatch');doc=read(rel);labels.extend((ns,x['semantic_id'],lang['tag'],x['preferred_term']) for x in doc['entries'])
    f.require(len(labels)==result['labels'],'Label count mismatch');return identities,labels,assertions

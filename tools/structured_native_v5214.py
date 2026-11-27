"""Build immutable private structured packets from exact pinned native sources."""
import importlib.util,json
from pathlib import Path

def load_framework(framework):
    path=Path(framework)/'tools/v11/structured_native_v5214.py'
    spec=importlib.util.spec_from_file_location('kristal_structured_framework_v5214',path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module

def build(root,slug,pin,output,framework):
    f=framework;output=Path(output);root=Path(root)
    for rel,h in pin['files'].items():
        raw=f.safe(root,rel).read_bytes();f.require(f.sha(raw)==h,'Pinned native drift: '+slug+'/'+rel)
        dst=f.safe(output/'originals',rel);dst.parent.mkdir(parents=True,exist_ok=True)
        with dst.open('xb') as stream:stream.write(raw)
    idx=f.decode(f.safe(output/'originals','canon/state.index.json').read_bytes())
    registered=[{'path':x['path'],'artifact_id':x['artifact_id'],'contract_id':x['logical_contract']['id'],'contract_version':x['logical_contract']['version']} for x in idx['canonical_artifacts']]
    src=pin['state'];rr=[]
    if src is not None:_,rr=f.records(slug,src,f.safe(output/'originals',src).read_bytes())
    f.require(len(rr)==pin['assertions'],'Native occurrence count mismatch')
    packet={'format':f.FORMAT,'status':f.STATUS,'slug':slug,'source_path':src,'files':pin['files'],'registered_artifacts':registered,'records':rr}
    with (output/'packet.json').open('xb') as stream:stream.write((json.dumps(packet,ensure_ascii=True,sort_keys=True,separators=(',',':'))+'\n').encode('ascii'))
    f.validate_packet(output,packet);return packet

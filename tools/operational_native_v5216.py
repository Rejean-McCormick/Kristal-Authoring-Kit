"""Read-only activation preflight. Never grants approval, registers, or activates."""
import hashlib,json
from pathlib import Path

def require(ok,msg):
    if not ok: raise ValueError(msg)

def check_pending(root,safe):
    home=safe(root,'.kristal/v11/transactions')
    if not home.exists():return
    require(home.is_dir(),'Invalid transaction directory')
    for path in sorted(home.glob('*.json')):
        entry=json.loads(safe(root,path.relative_to(root).as_posix()).read_bytes())
        require(entry.get('profile')=='kristal.v11-recoverable-registration/1.0' and entry.get('status') in ('complete','rolled_back'),'Pending or unrecognized V11 transaction: '+path.name)

def preflight(root,plan,packet,inventory,*,safe,digest):
    check_pending(root,safe)
    require(plan['format']=='koa.kristal-native-registration-plan/1.0' and plan['status']=='PRIVATE_REHEARSAL_ONLY' and plan['activation_authorized'] is False,'Not a private registration plan')
    require(plan['requires_independent_editorial_approval'] is True and plan['requires_epistemic_reader_contract'] is True,'Missing gate')
    require(plan['slug']==packet['slug'] and plan['candidate_inventory']==inventory,'Candidate/packet mismatch')
    require(not safe(root,'.kristal/v11/authoring.json').exists(),'Profile already exists')
    require(set(plan['source_paths'])==set(plan['source_sha256']),'Source scope mismatch')
    for k,path in plan['source_paths'].items():require(digest(safe(root,path))==plan['source_sha256'][k],'Native source drift: '+path)
    require(digest(safe(root,'canon/state.index.json'))==plan['state_index_sha256'],'State drift')
    # Verify unique role/target mapping and all exact source hashes, without writing.
    roles={a['role']:a for a in plan['artifacts']};require(len(plan['artifacts'])==4 and set(roles)=={'registry','graph','crosswalk','catalog'},'Bad registration roles')
    require(all(plan['profile'][r]==a['target'] for r,a in roles.items()),'Profile target mismatch')
    entries=plan['artifacts']+plan['layers'];targets=[a['target'] for a in entries]
    require(len(targets)==len(set(targets)) and len(targets)==len(set(t.casefold() for t in targets)),'Duplicate target')
    for a in entries:
        require(a['target'].startswith('canon/domain/v11/updates/') and inventory[a['source']]==a['sha256'],'Target or source mismatch')
        require(not safe(root,a['target']).exists(),'Target already exists: '+a['target'])
    state=json.loads(safe(root,'canon/state.index.json').read_bytes());existing=state['canonical_artifacts'];ids={a['artifact_id'] for a in existing};paths={a['path'] for a in existing}
    require(not ids&{a['artifact_id'] for a in plan['artifacts']} and not paths&set(targets),'Existing registration collision')
    # Historical entries are inventoried, not byte-qualified by this preflight.
    return {'status':'PREFLIGHT_PASSED_EDITORIAL_AND_TRANSACTION_PENDING','targets':len(targets),'canonical_roles':4,'existing_entries':len(existing),'production_activation':False,'editorial_approval_verified':False,'reader_policy_verified':False,'transaction_executor_implemented':False,'required_phases':['recheck_source_and_live_index','authenticate_independent_approval','verify_reader_policy_in_production','acquire_workspace_transaction_lock','stage_all_artifacts_and_recovery_journal','register_all_roles_and_verify','publish_profile_last','rebuild_private_index','verify_or_recover_from_journal'],'existing_artifact_bytes_revalidated':False}

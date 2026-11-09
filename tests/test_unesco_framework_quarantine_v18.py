"""UNESCO v18 regression: quarantine, integrity, no false approvals and optional real Kit tests."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import tempfile
import unittest

MODULE=Path(__file__).resolve().parents[1]/'tools/unesco_framework_quarantine_v18.py'
spec=importlib.util.spec_from_file_location('unesco_framework_quarantine_v18',MODULE)
v18=importlib.util.module_from_spec(spec);spec.loader.exec_module(v18)


def fixture():
    ns='urn:kristal:unesco:mt1.10:encyclopedia:en:candidate-v1'
    lines=[]
    for n in range(1,42):
        lines.append(json.dumps({'semantic_id':f'KQ{n}','namespace_id':ns,'language':'en',
            'preferred_term':f'Educational concept {n}', 'source_system':'unesco_skos',
            'source_snapshot':'s'*64,'source_record_id':f'http://vocabularies.unesco.org/thesaurus/concept{n}',
            'license':'local-terms','alignment':{'evidence_refs':['KS9001']},'synonyms':[]},sort_keys=True))
    for ident,token in [('KP1001','broader'),('KP1002','narrower'),('KP1003','related')]:
        lines.append(json.dumps({'semantic_id':ident,'namespace_id':ns,'language':'en',
            'preferred_term':'SKOS '+token,'source_system':'unesco_skos','source_snapshot':'s'*64,
            'source_record_id':'https://www.w3.org/2004/02/skos/core#'+token,
            'license':'local-terms','alignment':{'evidence_refs':['KS9001']}},sort_keys=True))
    raw=('\n'.join(lines)+'\n').encode()
    catalog={'schema_version':'11.0','artifact_type':'kristal_dictionary_catalog',
        'catalog_id':'unesco-mt1-10-unreviewed-english-v1','namespace_id':ns,
        'languages':[{'tag':'en','fallbacks':[], 'layers':[{'layer_id':'unesco-skos-en-source-labels',
            'priority':10,'kind':'external','path':'unesco-skos-en.jsonl','sha256':v18.checksum(raw),
            'source_system':'unesco_skos','source_snapshot':'s'*64,'license':'local-terms'}]}]}
    return {v18.CATALOG:v18.json_bytes(catalog),v18.LEXICON:raw}


class QuarantineUnitTests(unittest.TestCase):
    def test_prepared_layer_has_41_rows_and_zero_active_layers(self):
        old,new,raw,layer=v18.analyze_lexicon(fixture())
        self.assertEqual(len(layer.splitlines()),44)
        self.assertEqual(len(old['languages'][0]['layers']),1)
        self.assertEqual(new['languages'][0]['layers'],[])
        self.assertNotEqual(v18.checksum(v18.json_bytes(new)),v18.checksum(raw))
    def test_all_source_bytes_remain_unchanged(self):
        src=fixture();old,new,cat,layer=v18.analyze_lexicon(src)
        self.assertEqual(cat,src[v18.CATALOG]);self.assertEqual(layer,src[v18.LEXICON])
    def test_reject_unpinned_lexicon_sha(self):
        src=fixture();src[v18.LEXICON]+=b'\n'
        with self.assertRaisesRegex(v18.V18Error,'SHA'):v18.analyze_lexicon(src)
    def test_reject_signed_reviewer_without_quarantine(self):
        src=fixture();rows=[json.loads(r) for r in src[v18.LEXICON].splitlines()]
        rows[0]['alignment']['reviewer']='a real reviewer'
        src[v18.LEXICON]=('\n'.join(json.dumps(r) for r in rows)+'\n').encode()
        cat=json.loads(src[v18.CATALOG]);cat['languages'][0]['layers'][0]['sha256']=v18.checksum(src[v18.LEXICON]);src[v18.CATALOG]=v18.json_bytes(cat)
        with self.assertRaisesRegex(v18.V18Error,'décision'):v18.analyze_lexicon(src)
    def test_reject_extra_catalog_layer(self):
        src=fixture();cat=json.loads(src[v18.CATALOG]);cat['languages'][0]['layers'].append(dict(cat['languages'][0]['layers'][0]))
        src[v18.CATALOG]=v18.json_bytes(cat)
        with self.assertRaisesRegex(v18.V18Error,'Topologie'):v18.analyze_lexicon(src)
    def test_reject_incomplete_rows(self):
        src=fixture();src[v18.LEXICON]=b'\n'.join(src[v18.LEXICON].splitlines()[:-1])+b'\n'
        cat=json.loads(src[v18.CATALOG]);cat['languages'][0]['layers'][0]['sha256']=v18.checksum(src[v18.LEXICON]);src[v18.CATALOG]=v18.json_bytes(cat)
        with self.assertRaisesRegex(v18.V18Error,'41 KQ'):v18.analyze_lexicon(src)
    def test_reject_path_traversal(self):
        for path in ('../source','a/../../b','C:/windows','a\\b','/tmp/x'):
            with self.assertRaises(v18.V18Error):v18.safe_rel(path)
    def test_reject_symbolic_files(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d);(p/'real').write_text('ok')
            try:(p/'link').symlink_to(p/'real')
            except (OSError,NotImplementedError):self.skipTest('symlinks unsupported')
            with self.assertRaises(v18.V18Error):v18.bounded_files(p)
    def test_report_requires_private_state(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)
            (p/'RAPPORT_PRODUIT_V17.json').write_bytes(v18.json_bytes({'branch':'unesco-mt1-10','status':'PUBLIC'}))
            with self.assertRaisesRegex(v18.V18Error,'rapport v17'):v18.verify_v17(p)
    def test_output_path_never_reuses_stage17(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)
            with self.assertRaisesRegex(v18.V18Error,'Nom du dossier'):v18.execute(p,p,p)


# This test uses the *real* Workbench and pinned Kit/Framework if they are
# installed; otherwise it is skipped. No network or publishing is involved.
class RealFrameworkEndToEnd(unittest.TestCase):
    def test_real_source_copy_and_three_independent_checks(self):
        repo=Path(os.environ.get('UNESCO_V18_REPO_ROOT',str(MODULE.parents[3])))
        source=repo/'EncyKlopedia/UNESCO_Workbench/candidates/educational-policy-en-v11/unesco-mt1-10'
        framework=repo/'Kristal/Kristal-Framework'
        integration=repo/'Kristal/Kristal-Integration-Pack'
        if not all(p.exists() for p in (source,framework,integration)):
            self.skipTest('Real Workbench or Framework/Integration Pack unavailable')
        with tempfile.TemporaryDirectory() as directory:
            d=Path(directory)
            stage17=d/'semantic_stage_v17_integrated_product'
            stage17.mkdir()
            shutil.copytree(source,stage17/v18.CLONE)
            report={'branch':v18.BRANCH,'status':'PRIVATE_INTEGRATED_PRODUCT_READY_FINAL_RELEASE_BLOCKED',
                'editorial_concepts':41,'editorial_statements':85,
                'private_english_reading_pages':41,'human_admissions_pending':191,
                'canonical_assertions_created':0,'C1_C4_qualified':False,'github_push':False}
            (stage17/'RAPPORT_PRODUIT_V17.json').write_bytes(v18.json_bytes(report))
            files=v18.bounded_files(stage17)
            (stage17/'MANIFESTE_V17.json').write_bytes(v18.json_bytes({
                'branch':v18.BRANCH,'canonical_approval_not_performed':True,
                'public_release_authorized':False,'files_sha256':{k:v18.checksum(b) for k,b in files.items()}}))
            before=v18.checksum((source/v18.CATALOG).read_bytes())
            out=d/'semantic_stage_v18_framework_quarantine'
            result=v18.execute(stage17,repo,out)
            self.assertEqual(result['status'],'PRIVATE_FRAMEWORK_TECHNICAL_CHECK_PASSED_LEXICON_QUARANTINED')
            self.assertEqual(result['approved_KQ_KP_KA_KS'],0)
            self.assertEqual(result['direct_english_lexical_coverage_KQ'],0)
            self.assertEqual(before,v18.checksum((source/v18.CATALOG).read_bytes()))
            self.assertEqual((out/v18.DEST_CLONE/v18.LEXICON).read_bytes(),(source/v18.LEXICON).read_bytes())
            self.assertTrue((out/v18.DEST_CLONE/v18.QUARANTINE_DIR/'catalog-original.json').exists())
            self.assertEqual(v18.execute(stage17,repo,out)['operation'],'DEJA_PRESENT_INTACT')
            self.assertEqual(v18.execute(stage17,repo,out,audit=True)['operation'],'DEJA_PRESENT_INTACT')
            with self.assertRaisesRegex(v18.V18Error,'modifié'):
                (out/'README_V18_PRIVE.md').write_text('tampered')
                v18.execute(stage17,repo,out)
            self.assertEqual(before,v18.checksum((source/v18.CATALOG).read_bytes()))

if __name__=='__main__':unittest.main()

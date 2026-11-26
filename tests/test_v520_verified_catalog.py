import json, os, shutil, sys, tempfile, unittest
from pathlib import Path
from jsonschema.exceptions import ValidationError
KIT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(KIT/'tools'))
import kristal_v11_core as v11
import v520_verified_catalog as writer
SCHEMAS=Path(os.environ.get('KRISTAL_FRAMEWORK_ROOT',str(KIT.parent/'Kristal-Framework')))/'schemas/v11'
class VerifiedCatalogTests(unittest.TestCase):
    def setUp(self):
        t=tempfile.TemporaryDirectory();self.addCleanup(t.cleanup);self.base=Path(t.name);self.root=self.base/'Kristal-Test';shutil.copytree(KIT/'examples/demo-semantic-v11',self.root);self.private=self.base/'private';self.private.mkdir()
        self.cfg=v11.load_profile(self.root);self.before=(v11.digest(self.root/v11.CONFIG),v11.digest(self.root/'canon/state.index.json'))
    def row(self,tag='en',**kw):
        return dict({'namespace_id':'test:project','semantic_id':'KQ1001','external_id':'Q8018','language':tag,'preferred_term':'Augustine of Hippo','aliases':[],'source_snapshot':'wbgetentities-sha256-'+'a'*64,'source_revision':1},**kw)
    def plan(self,rows):return writer.prepare(self.root,rows,self.before,SCHEMAS)
    def test_add_and_preserve(self):
        files={p:(self.root/p).read_bytes() for p in [self.cfg[k] for k in ('registry','graph','crosswalk','catalog')]};plan=self.plan([self.row(),self.row('fr',preferred_term='not the old label')]);self.assertEqual(plan['count'],1)
        self.assertEqual(v11.digest(self.root/v11.CONFIG),self.before[0]);result=writer.apply(plan,self.private,'test');self.assertEqual(result['new_cells'],1)
        for p,b in files.items():self.assertEqual((self.root/p).read_bytes(),b)
        terms=v11.validate(self.root)['lexical_terms'];self.assertEqual(terms['fr']['KQ1001'][1],"Augustin d'Hippone");self.assertEqual(terms['en']['KQ1001'][1],'Augustine of Hippo')
        self.assertTrue((self.root/'.kristal/v11/history'/ (self.before[0]+'.json')).exists())
        now=(v11.digest(self.root/v11.CONFIG),v11.digest(self.root/'canon/state.index.json'));self.assertIsNone(writer.prepare(self.root,[self.row()],now,SCHEMAS))
    def test_wrong_scope(self):
        with self.assertRaises(v11.V11Error):self.plan([self.row(namespace_id='other')])
    def test_wrong_qid(self):
        with self.assertRaises(v11.V11Error):self.plan([self.row(external_id='Q42')])
    def test_source_revision_required(self):
        with self.assertRaises(v11.V11Error):self.plan([self.row(source_revision=0)])
    def test_source_snapshot_required(self):
        with self.assertRaises(v11.V11Error):self.plan([self.row(source_snapshot='old-cache')])
    def test_schema_rejects_unexpected_fields(self):
        with self.assertRaises(ValidationError):self.plan([self.row(untrusted=True)])
    def test_duplicate_cell(self):
        with self.assertRaises(v11.V11Error):self.plan([self.row(),self.row()])
    def test_drift_refused(self):
        plan=self.plan([self.row()]);p=self.root/self.cfg['crosswalk'];p.write_bytes(p.read_bytes()+b'\n')
        with self.assertRaises(v11.V11Error):writer.apply(plan,self.private,'test')
        self.assertEqual(v11.digest(self.root/v11.CONFIG),self.before[0])
if __name__=='__main__':unittest.main()

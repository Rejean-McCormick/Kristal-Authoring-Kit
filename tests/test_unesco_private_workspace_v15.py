import importlib.util
from pathlib import Path
import tempfile
import unittest

SCRIPT=Path(__file__).resolve().parents[1]/'tools/unesco_private_workspace_v15.py'
spec=importlib.util.spec_from_file_location('unesco_private_workspace_v15',SCRIPT)
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)

def graph():
    return {'branch':'unesco-mt1-10','nodes':[{'unesco_id':'concept'+str(i)} for i in range(1,42)],
            'candidate_statements':[{}]*85,'skos_internal_observations':[{}]*61,
            'canonical_graph_built':False,'approved_KS':0}

class PrivateWorkspaceTests(unittest.TestCase):
    def test_init_is_real_kit_workspace_with_no_v11_opt_in(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'new'
            result=mod.make(p,graph(),'a'*64)
            self.assertEqual(result['kit_check'],'PASSED')
            self.assertFalse(result['enable_v11_called'])
            self.assertFalse((p/'.kristal/v11/authoring.json').exists())
            self.assertEqual(len(list((p/'canon/domain').glob('*.json'))),0)
            self.assertTrue((p/'derived/unesco-mt1-10/candidat_editorial_sans_KQ.json').is_file())
    def test_existing_folder_is_refused(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(mod.WorkspaceError):mod.make(Path(d),graph(),'a'*64)
    def test_reject_incomplete_graph(self):
        with tempfile.TemporaryDirectory() as d:
            g=graph();g['candidate_statements']=[]
            with self.assertRaises(mod.WorkspaceError):mod.make(Path(d)/'new',g,'a'*64)
    def test_reject_false_source_approval(self):
        with tempfile.TemporaryDirectory() as d:
            g=graph();g['approved_KS']=1
            with self.assertRaises(mod.WorkspaceError):mod.make(Path(d)/'new',g,'a'*64)
    def test_reject_false_canon(self):
        with tempfile.TemporaryDirectory() as d:
            g=graph();g['canonical_graph_built']=True
            with self.assertRaises(mod.WorkspaceError):mod.make(Path(d)/'new',g,'a'*64)

if __name__=='__main__':unittest.main()

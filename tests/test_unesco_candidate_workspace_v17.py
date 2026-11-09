import json
from pathlib import Path
import sys
import tempfile
import unittest

REPO=Path(__file__).resolve().parents[1]
ROOT=REPO.parents[1]
sys.path.insert(0,str(REPO/'tools'))
from unesco_candidate_workspace_v17 import prepare,CandidateKitError
WB=ROOT/'EncyKlopedia/UNESCO_Workbench/candidates/educational-policy-en-v11/unesco-mt1-10'

@unittest.skipUnless(WB.is_dir(),'Workbench UNESCO non fourni')
class TestPrivateClone(unittest.TestCase):
 def test_source_untouched_and_official_kit_accepts_copy(self):
    kit=REPO/'tools/kristal.py'
    before=(WB/'canon/domain/v11/registry.json').read_bytes()
    with tempfile.TemporaryDirectory() as td:
        result=prepare(WB,Path(td)/'clone',kit,{'branch':'unesco-mt1-10'}, {'concepts':41})
        self.assertEqual(result['kit_check_v11'],'PASSED')
        self.assertFalse(result['canonical_registry_changed'])
        self.assertEqual((Path(td)/'clone/canon/domain/v11/registry.json').read_bytes(),before)
        with self.assertRaises(CandidateKitError):prepare(WB,Path(td)/'clone',kit,{}, {})
    self.assertEqual((WB/'canon/domain/v11/registry.json').read_bytes(),before)
if __name__=='__main__':unittest.main()

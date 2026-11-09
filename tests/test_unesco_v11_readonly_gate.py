import importlib.util
from pathlib import Path
import tempfile
import unittest

SCRIPT=Path(__file__).resolve().parents[1]/'tools'/'unesco_v11_readonly_gate.py'
spec=importlib.util.spec_from_file_location('unesco_v11_readonly_gate',SCRIPT)
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)

class KitGateTests(unittest.TestCase):
 def test_missing_workspace_is_not_implied(self):
  report=mod.inspect(None)
  self.assertEqual(report['workspace_v11_status'],'NOT_CHECKED_NO_EXPLICIT_WORKSPACE')
  self.assertEqual(report['registry'],{})
  self.assertFalse(report['enable_v11_called'])
 def test_absent_workspace_rejected(self):
  with tempfile.TemporaryDirectory() as t:
   with self.assertRaises(mod.KitGateError):mod.inspect(Path(t)/'not-here')
 def test_existing_v11_demonstration_only_is_not_branch(self):
  demo=SCRIPT.parents[1]/'examples'/'demo-semantic-v11'
  r=mod.inspect(demo)
  self.assertEqual(r['workspace_v11_status'],'EXISTING_WORKSPACE_KIT_CHECK_V11_PASSED')
  self.assertEqual(r['workspace_branch_binding'],'NOT_ESTABLISHED')
  self.assertEqual(r['registry']['identities']['KQ1001']['kind'],'entity')
  self.assertFalse(r['publication_authorized'])
  self.assertEqual(len(r['accepted_exact_matches_in_existing_workspace']),1)
 def test_v11_profile_missing_is_not_created(self):
  with tempfile.TemporaryDirectory() as t:
   r=mod.inspect(t)
   self.assertEqual(r['workspace_v11_status'],'V11_PROFILE_ABSENT')
   self.assertFalse((Path(t)/'.kristal').exists())

if __name__=='__main__':unittest.main()

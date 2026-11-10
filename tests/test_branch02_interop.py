"""Read-only final-system v11 interop campaign: source pins and denials."""
import json
import os
from pathlib import Path
import shutil
import tempfile
import unittest
from scripts.check_branch02_interop import check, verify_dik_source
from scripts.qualify_framework_v11 import QualificationError

ROOT=Path(__file__).resolve().parents[1]
FW=Path(os.environ.get('KRISTAL_FRAMEWORK_ROOT','/missing-fw'))
DIK=Path(os.environ.get('BRANCH02_DIK_ROOT','/missing-dik'))

class Branch02ReadOnlyInteropTests(unittest.TestCase):
    @unittest.skipUnless(FW.is_dir(),'Actual Framework snapshot required')
    def test_local_kit_framework_qualification(self):
        sources=[ROOT/'examples/demo-semantic-v11/canon/domain/v11'/x for x in ('graph.json','registry.json','crosswalk.json','dictionaries/catalog.json')]
        original=[f.read_bytes() for f in sources]
        result=check(FW)
        self.assertTrue(result['framework_reference_coverage_match'])
        self.assertFalse(result['approved_to_publish'])
        self.assertEqual([f.read_bytes() for f in sources],original)

    @unittest.skipUnless(FW.is_dir() and DIK.is_dir(),'Actual Framework and diK snapshots required')
    def test_real_dik_alpha7_schema_parity_is_a_limited_claim(self):
        report=check(FW,DIK)
        self.assertEqual(report['diK']['v11_schema_count'],11)
        self.assertIn('not_inferred',report['diK']['draft3_to_draft4_semantic_compatibility'])

    @unittest.skipUnless(FW.is_dir() and DIK.is_dir(),'Actual Framework and diK snapshots required')
    def test_tampered_dik_vendor_schema_is_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            dst=Path(td)/'dik'
            shutil.copytree(DIK/'src/dik/_framework/schemas/v11',dst/'src/dik/_framework/schemas/v11')
            shutil.copyfile(DIK/'pyproject.toml',dst/'pyproject.toml')
            f=dst/'src/dik/_framework/schemas/v11/kristal-semantic-graph.schema.json'
            f.write_bytes(f.read_bytes()+b' ')
            with self.assertRaisesRegex(QualificationError,'schema drift'):
                verify_dik_source(FW,dst)

    def test_invalid_dik_root_is_denied(self):
        with tempfile.TemporaryDirectory() as td:
            with self.assertRaisesRegex(QualificationError,'missing'):
                verify_dik_source(ROOT,Path(td))

if __name__=='__main__':unittest.main()

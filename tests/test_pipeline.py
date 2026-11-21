import json, sys, tempfile, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from fonsisnet_sdd.core import validate_brief, validate_script, check_claims, register_asset, validate_audio_package, qa_checklist, build_review_package

class PipelineTests(unittest.TestCase):
 def test_example_brief_and_script(self):
  brief=json.loads((ROOT/'examples/brief.json').read_text())
  script=json.loads((ROOT/'examples/script.json').read_text())
  self.assertEqual(validate_brief(brief),[])
  self.assertEqual(validate_script(script),[])
 def test_unconfirmed_contact_blocked(self):
  b=json.loads((ROOT/'examples/brief.json').read_text()); b['contact_details']='600123123'
  self.assertTrue(any('confirmación' in e for e in validate_brief(b)))
 def test_risky_claim_never_auto_approved(self):
  s={'scenes':[{'id':'S1','claims':['Ahorra un 30% garantizado']}]}
  finding=check_claims(s)[0]
  self.assertEqual(finding['status'],'BLOCKED_REVIEW_REQUIRED'); self.assertFalse(finding['human_approved'])
 def test_asset_requires_rights_and_zero_cost(self):
  self.assertTrue(register_asset({'asset_id':'a','kind':'music','source':'x','license':'unknown','permission_status':'unknown','cost_eur':0}))
  self.assertEqual(register_asset({'asset_id':'a','kind':'music','source':'x','license':'CC0','permission_status':'public_domain','cost_eur':0}),[])
 def test_audio_requires_licenses_and_caption_accessibility(self):
  a={'voice':{'license':'unknown','permission_status':'unknown'},'music':{'license':'CC0','permission_status':'public_domain'},'captions':{'language':'es-ES','contrast_checked':True}}
  self.assertTrue(validate_audio_package(a))
 def test_qa_blocks_until_all_human_checks(self):
  q=qa_checklist({}); self.assertFalse(q['passed']); self.assertIn('human_final_approval',q['blocked'])
 def test_review_zip_has_manifest_and_blocks_publish(self):
  with tempfile.TemporaryDirectory() as td:
   root=Path(td); (root/'proof.txt').write_text('evidence')
   out=root/'review.zip'; result=build_review_package(root,out,['proof.txt'])
   self.assertEqual(result['files'],1)
   import zipfile
   with zipfile.ZipFile(out) as z:
    manifest=json.loads(z.read('REVIEW_MANIFEST.json'))
   self.assertEqual(manifest['approval'],'NOT_APPROVED_FOR_PUBLICATION')
 def test_package_rejects_path_traversal(self):
  with tempfile.TemporaryDirectory() as td:
   root=Path(td); (root.parent/'outside-sdd-test.txt').write_text('x')
   with self.assertRaises(ValueError): build_review_package(root,root/'x.zip',['../outside-sdd-test.txt'])
   (root.parent/'outside-sdd-test.txt').unlink()

if __name__=='__main__': unittest.main()

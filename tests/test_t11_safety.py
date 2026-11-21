import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from fonsisnet_sdd.core import (
    validate_brief, validate_script, check_claims, register_asset,
    validate_audio_package, qa_checklist, build_review_package,
)


class T11SafetyTests(unittest.TestCase):
    def setUp(self):
        self.brief = json.loads((ROOT / 'examples/brief.json').read_text(encoding='utf-8'))
        self.script = json.loads((ROOT / 'examples/script.json').read_text(encoding='utf-8'))

    def test_brief_rejects_bad_durations_without_crash(self):
        for value in ('quince', 15.5, True, 999, None):
            with self.subTest(value=value):
                self.brief['duration_seconds'] = value
                self.assertTrue(validate_brief(self.brief))

    def test_script_rejects_invalid_numeric_times(self):
        for value in ('nan', float('nan'), True, -1):
            with self.subTest(value=value):
                self.script['scenes'][0]['start'] = value
                self.assertTrue(validate_script(self.script))

    def test_script_rejects_missing_script_fields(self):
        del self.script['scenes'][0]['voiceover']
        self.assertTrue(validate_script(self.script))

    def test_script_rejects_duplicate_scene_ids(self):
        self.script['scenes'][1]['id'] = self.script['scenes'][0]['id']
        self.assertTrue(validate_script(self.script))

    def test_unlisted_risky_voiceover_is_flagged(self):
        self.script['scenes'][0]['voiceover'] = 'Ahorra 30% garantizado'
        result = check_claims(self.script)
        self.assertTrue(any(r.get('field') == 'voiceover' and r['status'] == 'BLOCKED_REVIEW_REQUIRED' for r in result))
        self.assertTrue(all(r['human_approved'] is False for r in result))

    def test_asset_requires_explicit_zero_cost(self):
        item = {'asset_id': 'a', 'kind': 'image', 'source': 'self', 'license': 'CC0', 'permission_status': 'public_domain'}
        self.assertTrue(register_asset(item))
        item['cost_eur'] = 0
        self.assertEqual(register_asset(item), [])
        item['cost_eur'] = False
        self.assertTrue(register_asset(item))

    def test_audio_requires_nonempty_verified_resources(self):
        audio = {'voice': {}, 'music': {}, 'captions': {}}
        self.assertTrue(validate_audio_package(audio))

    def test_qa_string_true_does_not_authorize_release(self):
        fields = ('duration_ok', 'aspect_ratio_ok', 'brand_checked', 'audio_checked',
                  'captions_checked', 'rights_checked', 'claims_human_approved',
                  'privacy_checked', 'final_human_approval')
        qa = {field: True for field in fields}
        qa['final_human_approval'] = 'true'
        self.assertFalse(qa_checklist(qa)['passed'])

    def test_review_package_rejects_duplicate_and_unsafe_paths(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / 'proof.txt').write_text('safe', encoding='utf-8')
            for paths in (['proof.txt', 'proof.txt'], ['../proof.txt'], ['/etc/passwd'],
                          ['REVIEW_MANIFEST.json'], ['proof.txt/../proof.txt'],
                          ['proof.txt\\evil']):
                with self.subTest(paths=paths):
                    with self.assertRaises(ValueError):
                        build_review_package(root, root / 'review.zip', paths)

    def test_project_policy_prevents_cost_and_production(self):
        policy = json.loads((ROOT / 'config/policy.json').read_text(encoding='utf-8'))
        self.assertEqual(policy['default_budget_eur'], 0)
        self.assertFalse(policy['paid_services_allowed'])
        self.assertFalse(policy['production_deploy_allowed'])
        self.assertTrue(policy['human_approval_required'])

    def test_ci_has_no_deploy_or_write_access(self):
        text = (ROOT / '.github/workflows/t11-ci.yml').read_text(encoding='utf-8')
        self.assertIn('contents: read', text)
        self.assertIn('github.event.repository.private == false', text)
        self.assertNotIn('contents: write', text)
        self.assertNotIn('vercel deploy', text)
        self.assertNotIn('deployments: write', text)


if __name__ == '__main__':
    unittest.main()

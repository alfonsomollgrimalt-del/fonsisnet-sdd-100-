"""Negative security tests for T11 v0.3.1; all offline/stdlib."""
import hashlib
import json
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from fonsisnet_sdd import __version__
from fonsisnet_sdd.core import (
    register_asset, validate_audio_package, build_review_package, validate_script,
)


class SecurityPatchTests(unittest.TestCase):
    def fixture(self, directory: Path, file_name='evidence.txt'):
        (directory / file_name).write_text('Rights record for test asset, offline only', encoding='utf-8')
        digest = hashlib.sha256((directory / file_name).read_bytes()).hexdigest()
        evidence = {
            'file': file_name,
            'sha256': digest,
            'rights_holder': 'Rights owner under test',
            'reviewed_by': 'Test human reviewer',
            'reviewed_at': '2026-11-20T12:00:00+00:00',
            'human_approved': True,
        }
        asset = {'asset_id': 'asset1', 'kind': 'music', 'source': 'internal-test',
                 'license': 'CC0', 'permission_status': 'public_domain',
                 'cost_eur': 0, 'rights_evidence': evidence}
        return asset

    def test_genuine_local_evidence_hash_and_human_review_is_accepted(self):
        with tempfile.TemporaryDirectory() as td:
            asset = self.fixture(Path(td))
            self.assertEqual(register_asset(asset, td), [])

    def test_no_evidence_directory_fails_closed(self):
        with tempfile.TemporaryDirectory() as td:
            asset = self.fixture(Path(td))
            self.assertTrue(register_asset(asset))

    def test_no_local_document_blocks_rights(self):
        with tempfile.TemporaryDirectory() as td:
            asset = self.fixture(Path(td))
            (Path(td) / 'evidence.txt').unlink()
            self.assertTrue(register_asset(asset, td))

    def test_hash_tampering_fails_closed(self):
        with tempfile.TemporaryDirectory() as td:
            asset = self.fixture(Path(td))
            (Path(td) / 'evidence.txt').write_text('tampered', encoding='utf-8')
            self.assertTrue(register_asset(asset, td))

    def test_rights_review_required_even_with_matching_hash(self):
        with tempfile.TemporaryDirectory() as td:
            asset = self.fixture(Path(td))
            asset['rights_evidence']['human_approved'] = 'true'
            self.assertTrue(register_asset(asset, td))

    def test_untrusted_approval_fields_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            asset = self.fixture(Path(td))
            for key in ('rights_holder', 'reviewed_by', 'reviewed_at'):
                with self.subTest(key=key):
                    old = asset['rights_evidence'][key]
                    asset['rights_evidence'][key] = '[PENDIENTE DE COMPROBAR]'
                    self.assertTrue(register_asset(asset, td))
                    asset['rights_evidence'][key] = old

    def test_future_review_and_expired_rights_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            asset = self.fixture(Path(td))
            ev = asset['rights_evidence']
            ev['reviewed_at'] = '2100-01-01T00:00:00Z'
            self.assertTrue(register_asset(asset, td))
            ev['reviewed_at'] = '2026-11-20T12:00:00+00:00'
            ev['valid_until'] = '2001-01-01'
            self.assertTrue(register_asset(asset, td))

    def test_evidence_path_traversal_and_symlink_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            asset = self.fixture(root)
            asset['rights_evidence']['file'] = '../outside.txt'
            self.assertTrue(register_asset(asset, td))
            asset['rights_evidence']['file'] = 'proof-link'
            (root / 'proof-link').symlink_to(root / 'evidence.txt')
            self.assertTrue(register_asset(asset, td))

    def test_unhashable_malformed_permission_rejected_without_crash(self):
        with tempfile.TemporaryDirectory() as td:
            asset = self.fixture(Path(td))
            for malformed in ([], {}, None, True):
                with self.subTest(malformed=malformed):
                    asset['permission_status'] = malformed
                    self.assertTrue(register_asset(asset, td))

    def test_asset_cost_must_be_explicit_real_zero(self):
        with tempfile.TemporaryDirectory() as td:
            asset = self.fixture(Path(td))
            for bad in (None, True, False, -1, 0.01, '0', float('nan'), float('inf')):
                with self.subTest(value=bad):
                    asset['cost_eur'] = bad
                    self.assertTrue(register_asset(asset, td))
            asset['cost_eur'] = 0.0
            self.assertEqual(register_asset(asset, td), [])

    def test_audio_nonzero_and_missing_cost_fails(self):
        with tempfile.TemporaryDirectory() as td:
            asset = self.fixture(Path(td))
            audio = {'voice': dict(asset, asset_id='voice', kind='voice'),
                     'music': dict(asset, asset_id='music', kind='music'),
                     'captions': {'language': 'es-ES', 'contrast_checked': True}}
            self.assertEqual(validate_audio_package(audio, td), [])
            for key in ('voice', 'music'):
                audio[key]['cost_eur'] = 250
                self.assertTrue(validate_audio_package(audio, td))
                audio[key]['cost_eur'] = 0
                del audio[key]['cost_eur']
                self.assertTrue(validate_audio_package(audio, td))
                audio[key]['cost_eur'] = 0

    def test_audio_requires_local_document(self):
        with tempfile.TemporaryDirectory() as td:
            asset = self.fixture(Path(td))
            audio = {'voice': dict(asset), 'music': dict(asset),
                     'captions': {'language': 'es-ES', 'contrast_checked': True}}
            self.assertTrue(validate_audio_package(audio))

    def test_review_zip_does_not_overwrite_existing_file(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / 'proof.txt').write_text('evidence', encoding='utf-8')
            destination = root / 'review.zip'
            destination.write_bytes(b'important existing data')
            with self.assertRaises(FileExistsError):
                build_review_package(root, destination, ['proof.txt'])
            self.assertEqual(destination.read_bytes(), b'important existing data')

    def test_review_zip_cannot_escape_project(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / 'project'
            root.mkdir()
            (root / 'proof.txt').write_text('safe', encoding='utf-8')
            destination = Path(td) / 'outside.zip'
            with self.assertRaises(ValueError):
                build_review_package(root, destination, ['proof.txt'])
            self.assertFalse(destination.exists())

    def test_review_zip_cannot_write_through_symlink(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / 'project';root.mkdir()
            (root / 'proof.txt').write_text('safe', encoding='utf-8')
            outside = Path(td) / 'outside.zip'
            outside.write_bytes(b'important')
            (root / 'linked.zip').symlink_to(outside)
            with self.assertRaises(ValueError):
                build_review_package(root, root / 'linked.zip', ['proof.txt'])
            self.assertEqual(outside.read_bytes(), b'important')

    def test_review_zip_requires_existing_directory(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / 'proof.txt').write_text('safe', encoding='utf-8')
            with self.assertRaises(ValueError):
                build_review_package(root, root / 'not-yet-existing' / 'zip.zip', ['proof.txt'])

    def test_review_zip_valid_manifest_is_reproducible(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / 'proof.txt').write_text('safe', encoding='utf-8')
            result = build_review_package(root, root / 'review.zip', ['proof.txt'])
            self.assertEqual(result['files'], 1)
            import zipfile
            with zipfile.ZipFile(root / 'review.zip') as obj:
                manifest = json.loads(obj.read('REVIEW_MANIFEST.json'))
                self.assertEqual(manifest['files'][0]['sha256'], hashlib.sha256(b'safe').hexdigest())
                self.assertEqual(manifest['approval'], 'NOT_APPROVED_FOR_PUBLICATION')

    def test_script_rejects_uncovered_start_gap_and_end(self):
        base = json.loads((ROOT / 'examples/script.json').read_text(encoding='utf-8'))
        first = json.loads(json.dumps(base))
        first['scenes'][0]['start'] = 1
        self.assertTrue(any('hueco' in e for e in validate_script(first)))
        middle = json.loads(json.dumps(base))
        middle['scenes'][1]['start'] = 5
        self.assertTrue(any('hueco' in e for e in validate_script(middle)))
        end = json.loads(json.dumps(base))
        end['scenes'][-1]['end'] = 14
        self.assertTrue(any('final' in e for e in validate_script(end)))
        self.assertEqual(validate_script(base), [])

    def test_version_metadata_is_consistent(self):
        policy = json.loads((ROOT / 'config/policy.json').read_text(encoding='utf-8'))
        self.assertEqual(__version__, '0.3.1')
        self.assertEqual(policy['version'], __version__)
        self.assertFalse(policy['production_deploy_allowed'])
        self.assertFalse(policy['paid_services_allowed'])
        self.assertTrue(policy['remote_code_uploaded'])

    def test_ci_pins_action_hashes_and_read_only(self):
        workflow = (ROOT / '.github/workflows/t11-ci.yml').read_text(encoding='utf-8')
        self.assertIn('actions/checkout@11d5960a326750d5838078e36cf38b85af677262', workflow)
        self.assertIn('actions/setup-python@a26af69be951a213d495a4c3e4e4022e16d87065', workflow)
        self.assertIn('contents: read', workflow)
        self.assertNotIn('push:', workflow)
        self.assertNotIn('deployments: write', workflow)
        self.assertNotIn('npm install', workflow)

if __name__ == '__main__':
    unittest.main()

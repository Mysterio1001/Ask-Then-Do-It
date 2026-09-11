"""Current release boundaries; this does not claim live Claude verification."""
import copy
import json
import unittest
from pathlib import Path

from tests.release.test_release_transaction import load_builder_module

ROOT = Path(__file__).resolve().parents[2]


class ReleaseAlignmentTests(unittest.TestCase):
    def setUp(self):
        self.builder = load_builder_module()
        self.config = json.loads((ROOT / 'release/release.json').read_text(encoding='utf-8'))

    def test_current_config_loads_three_version_matched_families(self):
        config = self.builder.load_config(ROOT / 'release/release.json')
        self.assertEqual(config['release_version'], '1.4.0')
        self.assertEqual(config['core_version'], '1.4.0')
        self.assertEqual(set(config['managed_outputs']), {'codex', 'generic', 'claude', 'checksums.sha256'})
        for family in ('codex', 'generic', 'claude'):
            self.assertTrue(config[family]['archive'].endswith('-1.4.0.zip'))

    def test_claude_required_checks_cannot_be_omitted(self):
        self.assertIn('claude', self.config)
        for check in ('claude-plugin-validation', 'claude-conformance', 'claude-package-inventory', 'claude-behavior', 'claude-context', 'claude-live-smoke'):
            with self.subTest(check=check):
                config = copy.deepcopy(self.config)
                config['required_validation_checks'].remove(check)
                with self.assertRaises(self.builder.BuildError):
                    self.builder.validate_claude_config(config)

    def test_claude_wrong_version_cannot_be_accepted(self):
        self.assertIn('claude', self.config)
        config = copy.deepcopy(self.config)
        config['core_version'] = '1.3.1'
        with self.assertRaises(self.builder.BuildError):
            self.builder.validate_claude_config(config)

    def test_historical_preview_path_rejects_current_source(self):
        with self.assertRaises(self.builder.claude_package.ClaudePackageError):
            self.builder.claude_preview_config()

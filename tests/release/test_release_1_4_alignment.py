"""Current release boundaries; this does not claim live Claude verification."""
import copy
import json
import re
import unittest
from pathlib import Path

import yaml

from tests.release.test_release_transaction import load_builder_module

ROOT = Path(__file__).resolve().parents[2]


class ReleaseAlignmentTests(unittest.TestCase):
    def setUp(self):
        self.builder = load_builder_module()
        self.config = json.loads((ROOT / 'release/release.json').read_text(encoding='utf-8'))

    def test_current_config_loads_three_version_matched_families(self):
        config = self.builder.load_config(ROOT / 'release/release.json')
        self.assertEqual(config['release_version'], '1.4.2')
        self.assertEqual(config['core_version'], '1.4.2')
        self.assertEqual(set(config['managed_outputs']), {'codex', 'generic', 'claude', 'checksums.sha256'})
        for family in ('codex', 'generic', 'claude'):
            self.assertTrue(config[family]['archive'].endswith('-1.4.2.zip'))

    def test_provider_catalogs_pin_the_same_current_release_tag(self):
        codex_catalog = json.loads(
            (ROOT / '.agents/plugins/marketplace.json').read_text(encoding='utf-8')
        )
        claude_catalog = json.loads(
            (ROOT / '.claude-plugin/marketplace.json').read_text(encoding='utf-8')
        )
        self.assertEqual(codex_catalog['plugins'][0]['source']['ref'], 'v1.4.2')
        self.assertEqual(claude_catalog['plugins'][0]['source']['ref'], 'v1.4.2')
        self.assertEqual(claude_catalog['plugins'][0]['version'], '1.4.2')

    def test_historical_slimming_artifacts_keep_their_original_core_version(self):
        for relative in (
            'docs/specs/codex-skill-runtime-slimming.md',
            'docs/plans/codex-skill-runtime-slimming.md',
        ):
            with self.subTest(path=relative):
                self.assertIn('Core version: `1.4.1`', (ROOT / relative).read_text(encoding='utf-8'))
        for relative in (
            'docs/project/drafts/codex-skill-runtime-slimming/lifecycle-manifest.json',
            'docs/project/drafts/codex-skill-runtime-slimming/migration/source-manifest.json',
        ):
            with self.subTest(path=relative):
                value = json.loads((ROOT / relative).read_text(encoding='utf-8'))
                recorded_version = (
                    value['core_version'] if 'core_version' in value
                    else value['canonical'][0]['core_version']
                )
                self.assertEqual(recorded_version, '1.4.1')

    def test_readme_downloads_and_adapter_manifests_match_release_version(self):
        version = self.config['release_version']
        repository = 'https://github.com/Mysterio1001/Ask-Then-Do-It'
        readme = (ROOT / 'README.md').read_text(encoding='utf-8')
        downloads = re.findall(
            re.escape(repository) + r'/releases/download/v([^/]+)/([^\s)]+\.zip)',
            readme,
        )
        self.assertEqual(
            set(downloads),
            {(version, Path(self.config[family]['archive']).name)
             for family in ('codex', 'generic', 'claude')},
        )
        for family, manifest_directory in (
            ('codex', '.codex-plugin'), ('claude', '.claude-plugin'),
        ):
            with self.subTest(family=family):
                manifest = ROOT / self.config[family]['source'] / manifest_directory / 'plugin.json'
                self.assertEqual(json.loads(manifest.read_text(encoding='utf-8'))['version'], version)
        for adapter, declaration in (
            ('codex', 'conformance.yaml'), ('generic-prompts', 'manifest.yaml'),
            ('claude-code', 'conformance.yaml'),
        ):
            with self.subTest(adapter=adapter):
                manifest = yaml.safe_load(
                    (ROOT / 'adapters' / adapter / declaration).read_text(encoding='utf-8')
                )
                self.assertEqual(manifest['adapter_version'], version)
                self.assertEqual(manifest['core_version'], self.config['core_version'])

    def test_claude_static_checks_cannot_be_omitted(self):
        self.assertIn('claude', self.config)
        static_checks = (
            'claude-plugin-validation',
            'claude-conformance',
            'claude-package-inventory',
        )
        live_checks = ('claude-behavior', 'claude-context', 'claude-live-smoke')
        baseline = copy.deepcopy(self.config)
        baseline['required_validation_checks'] = [
            check
            for check in baseline['required_validation_checks']
            if check not in live_checks
        ]
        self.builder.validate_claude_config(baseline)
        for check in static_checks:
            with self.subTest(check=check):
                config = copy.deepcopy(baseline)
                config['required_validation_checks'].remove(check)
                with self.assertRaises(self.builder.BuildError):
                    self.builder.validate_claude_config(config)

    def test_claude_live_checks_cannot_be_required(self):
        live_checks = ('claude-behavior', 'claude-context', 'claude-live-smoke')
        baseline = copy.deepcopy(self.config)
        baseline['required_validation_checks'] = [
            check
            for check in baseline['required_validation_checks']
            if check not in live_checks
        ]
        for check in live_checks:
            with self.subTest(check=check):
                config = copy.deepcopy(baseline)
                config['required_validation_checks'].append(check)
                with self.assertRaisesRegex(
                    self.builder.BuildError,
                    '[Oo]ptional Claude live qualification checks',
                ):
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

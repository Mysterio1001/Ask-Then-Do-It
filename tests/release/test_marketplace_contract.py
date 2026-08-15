import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CATALOG = ROOT / ".agents" / "plugins" / "marketplace.json"
VALIDATOR = ROOT / "scripts" / "validate_marketplace.py"


def run_validator(catalog: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(VALIDATOR), "--catalog", str(catalog)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )


class MarketplaceContractTests(unittest.TestCase):
    def test_official_marketplace_catalog_is_tag_pinned_and_unique(self) -> None:
        self.assertTrue(CATALOG.is_file(), f"missing marketplace catalog: {CATALOG}")
        catalog = json.loads(CATALOG.read_text(encoding="utf-8"))

        self.assertEqual(catalog["name"], "ask-then-do-it")
        self.assertEqual(catalog["interface"]["displayName"], "Ask Then Do It")
        plugins = catalog["plugins"]
        self.assertEqual(len(plugins), 1)

        plugin = plugins[0]
        self.assertEqual(plugin["name"], "ask-then-do-it")
        self.assertEqual(plugin["policy"], {
            "installation": "AVAILABLE",
            "authentication": "ON_INSTALL",
        })
        self.assertEqual(plugin["category"], "Developer Tools")

        source = plugin["source"]
        self.assertEqual(source["source"], "git-subdir")
        self.assertEqual(
            source["url"],
            "https://github.com/Mysterio1001/Ask-Then-Do-It.git",
        )
        self.assertEqual(source["path"], "adapters/codex/plugin/ask-then-do-it")
        self.assertEqual(source["ref"], "v1.3.0")

    def test_catalog_is_repository_metadata_only(self) -> None:
        self.assertTrue(CATALOG.is_relative_to(ROOT))
        self.assertEqual(CATALOG.relative_to(ROOT).as_posix(), ".agents/plugins/marketplace.json")

    def test_validator_accepts_the_official_catalog(self) -> None:
        result = run_validator(CATALOG)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_validator_rejects_unsafe_marketplace_mutations(self) -> None:
        mutations = {
            "mutable ref": lambda value: value["plugins"][0]["source"].update(ref="main"),
            "alternate URL": lambda value: value["plugins"][0]["source"].update(
                url="https://github.com/other/Ask-Then-Do-It.git"
            ),
            "wrong source type": lambda value: value["plugins"][0]["source"].update(
                source="github"
            ),
            "wrong path": lambda value: value["plugins"][0]["source"].update(
                path="plugins/ask-then-do-it"
            ),
            "wrong policy": lambda value: value["plugins"][0]["policy"].update(
                installation="INSTALLED_BY_DEFAULT"
            ),
            "extra entry": lambda value: value["plugins"].append(value["plugins"][0].copy()),
        }
        baseline = json.loads(CATALOG.read_text(encoding="utf-8"))
        for label, mutate in mutations.items():
            with self.subTest(label=label):
                value = json.loads(json.dumps(baseline))
                mutate(value)
                with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
                    candidate = Path(temporary) / "marketplace.json"
                    candidate.write_text(json.dumps(value), encoding="utf-8")
                    result = run_validator(candidate)
                    self.assertNotEqual(result.returncode, 0, result.stdout)


if __name__ == "__main__":
    unittest.main()

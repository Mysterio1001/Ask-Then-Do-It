import hashlib
import importlib.util
import json
import re
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[2]
CONFIG = ROOT / "release" / "release.json"
BUILDER = ROOT / "scripts" / "build_release.py"
RELEASE_VERSION = "1.3.0"
CORE_VERSION = "1.3.0"
VERSIONED_GUIDE_ROOT = (
    "https://github.com/Mysterio1001/Ask-Then-Do-It/blob/v1.3.0/docs/guides"
)
EXPECTED_SKILLS = {
    "ask-then-do-it",
    "ask-requirements",
    "ask-with-docs",
    "implement-direct",
    "implement-tdd",
    "improve-architecture",
    "plan-tickets",
    "review-code",
    "write-spec",
}
EXPECTED_SKILL_ORDER = [
    "ask-then-do-it",
    "ask-requirements",
    "ask-with-docs",
    "implement-direct",
    "implement-tdd",
    "improve-architecture",
    "plan-tickets",
    "review-code",
    "write-spec",
]
EXPECTED_MODULES = [
    "bootstrap.md",
    "orchestration.md",
    "lite-workflow.md",
    "requirements.md",
    "documented-requirements.md",
    "specification.md",
    "ticket-planning.md",
    "direct-implementation.md",
    "tdd-implementation.md",
    "review.md",
    "architecture-improvement.md",
]

# These are approved 1.2.0 release artifacts. Their bytes are historical input,
# not active release declarations, and must remain untouched by integration.
HISTORICAL_SHA256 = {
    "docs/evidence/ask-then-do-it-1.2.0-release-architecture-diagnosis.md": "19ebc7327edf3b99d8773949d6cae9fc837fad1a050fd14058b84a7a31638da6",
    "docs/evidence/ask-then-do-it-release-1.2.0.json": "d89e907412bfea1c69622c106c1b34d352e2099cc60bfc5dc6ea42986cd3584c",
    "docs/evidence/ask-then-do-it-release-1.2.0.md": "a0b4aa12ad2be3465d10faaf380ac94f84b73fa6d0da1530bf66e0e700525ecc",
    "docs/evidence/command-install-update-1.2.0-ticket-1.md": "3adc21a11409f8978ae39b246affa909a0d2ad34192922765fdf3178edfa8806",
    "docs/evidence/command-install-update-1.2.0-ticket-1-review.md": "3f3bb9bd5fd43105a59c436d162782eac2dc7b914a87f428246f31147f6fd2d8",
    "docs/evidence/command-install-update-1.2.0-ticket-2.md": "6e5dca8605f804d61a34b018bdd7960c31d4e1e06f750154ed2c133ccff7b2ed",
    "docs/evidence/command-install-update-1.2.0-ticket-2-review.md": "fc1ee56ee31d0410f2fef2108b01c333a6946fea47226a1016beba8787c05f73",
    "docs/evidence/command-install-update-1.2.0-ticket-3.md": "09d24939155ab4e21c1a10da8cb47c8b7000c00803996e4117a07aa3212d6848",
    "docs/evidence/command-install-update-1.2.0-ticket-3-review.md": "14e84a179647bc78ab22f4bad9db1a1036ff27e30da1193cf6f95b3e4ddc90f4",
    "docs/evidence/command-install-update-1.2.0-ticket-4.md": "8cc9789036c96b56c4b63065f87f51d2160c24eda96c906ae7efd092ab6257a4",
    "docs/evidence/command-install-update-1.2.0-ticket-4-review.md": "53a1209505a272d4ca461a3f054a45e8b7be59020cfcbb997c01d46f572e39b1",
    "docs/evidence/command-install-update-1.2.0-ticket-5.md": "5ee28e66be1539f2df6d28fdbf8e87794ad864284275776ca85a2d4eee5427d7",
    "docs/evidence/command-install-update-1.2.0-ticket-5-review.md": "64f2da860ffe9bc809c2b5f2cef9d76714cf9693d251862a839d4867e836d7d5",
    "docs/plans/command-install-update-1.2.0.md": "e9724cac8123a62ea997a4939a57bbaa919c32b43c6268549af49aac68f41c64",
    "docs/requirements/command-install-update-1.2.0.md": "8eea63d8c2ee772745fef39cea8c0214f464b274054c55db706430b62acdc0ad",
    "docs/specs/command-install-update-1.2.0.md": "1bb133889d50263ca6d1a5ff86cfa0baa7e0ac536de81fa529f690e19c9bcc9f",
}


def read_json(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def top_level_scalar(path: Path, key: str) -> str:
    pattern = re.compile(rf"^{re.escape(key)}:\s*([^#\s]+)")
    for line in path.read_text(encoding="utf-8").splitlines():
        match = pattern.match(line)
        if match:
            return match.group(1).strip("\"'")
    raise AssertionError(f"missing {key} in {path}")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_builder(output: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            sys.executable,
            str(BUILDER),
            "--allow-test-output-root",
            "--output-root",
            str(output),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )


def load_builder_module():
    spec = importlib.util.spec_from_file_location("release_builder_1_3", BUILDER)
    if spec is None or spec.loader is None:
        raise AssertionError(f"unable to load release builder: {BUILDER}")
    module = importlib.util.module_from_spec(spec)
    scripts_path = str(BUILDER.parent)
    sys.path.insert(0, scripts_path)
    try:
        spec.loader.exec_module(module)
    finally:
        sys.path.remove(scripts_path)
    return module


def files_under(root: Path) -> set[str]:
    return {
        path.relative_to(root).as_posix()
        for path in root.rglob("*")
        if path.is_file()
    }


class ReleaseOneThreeContractTests(unittest.TestCase):
    def test_active_identity_and_current_document_downloads_are_1_3_0(self) -> None:
        config = read_json(CONFIG)
        self.assertEqual(config["release_version"], RELEASE_VERSION)
        self.assertEqual(config["core_version"], CORE_VERSION)

        plugin = read_json(
            ROOT
            / "adapters"
            / "codex"
            / "plugin"
            / "ask-then-do-it"
            / ".codex-plugin"
            / "plugin.json"
        )
        self.assertEqual(plugin["version"], RELEASE_VERSION)
        self.assertEqual(
            read_json(ROOT / ".agents" / "plugins" / "marketplace.json")["plugins"][0]["source"]["ref"],
            "v1.3.0",
        )

        self.assertIn(f"Core version: `{CORE_VERSION}`", (ROOT / "core" / "CORE.md").read_text(encoding="utf-8"))
        for declaration in (
            ROOT / "core" / "rules" / "rules.yaml",
            ROOT / "adapters" / "codex" / "conformance.yaml",
            ROOT / "adapters" / "generic-prompts" / "manifest.yaml",
        ):
            self.assertEqual(top_level_scalar(declaration, "core_version"), CORE_VERSION)

        root_download_docs = [
            ROOT / "README.md",
            *(ROOT / name for name in ("START-HERE.en.md", "START-HERE.zh-TW.md", "START-HERE.ja.md")),
        ]
        for document in root_download_docs:
            body = document.read_text(encoding="utf-8")
            with self.subTest(document=document.relative_to(ROOT)):
                self.assertIn("v1.3.0", body)
                self.assertIn("ask-then-do-it-1.3.0.zip", body)
                self.assertIn("ask-then-do-it-generic-1.3.0.zip", body)

        host_contracts = (
            (
                "codex",
                [ROOT / "docs" / "guides" / f"codex.{locale}.md" for locale in ("en", "zh-TW", "ja")],
                "ask-then-do-it-1.3.0.zip",
                "ask-then-do-it-generic-1.3.0.zip",
            ),
            (
                "generic",
                [ROOT / "docs" / "guides" / f"generic.{locale}.md" for locale in ("en", "zh-TW", "ja")],
                "ask-then-do-it-generic-1.3.0.zip",
                "ask-then-do-it-1.3.0.zip",
            ),
        )
        for host, documents, required_archive, forbidden_archive in host_contracts:
            for document in documents:
                body = document.read_text(encoding="utf-8")
                with self.subTest(host=host, document=document.relative_to(ROOT)):
                    self.assertIn("v1.3.0", body)
                    self.assertIn(required_archive, body)
                    self.assertNotIn(forbidden_archive, body)
                    self.assertNotIn("1.2.0", body)

        package_starts = (
            (
                "codex",
                [ROOT / "adapters" / "codex" / "plugin" / "ask-then-do-it" / f"START-HERE.{locale}.md" for locale in ("en", "zh-TW", "ja")],
                "ask-then-do-it-generic-1.3.0.zip",
            ),
            (
                "generic",
                [ROOT / "release" / "generic" / f"START-HERE.{locale}.md" for locale in ("en", "zh-TW", "ja")],
                "ask-then-do-it-1.3.0.zip",
            ),
        )
        for host, documents, forbidden_archive in package_starts:
            for document in documents:
                body = document.read_text(encoding="utf-8")
                with self.subTest(host=host, document=document.relative_to(ROOT)):
                    self.assertIn("1.3.0", body)
                    self.assertNotIn(forbidden_archive, body)

    def test_release_config_locks_runtime_inventory_and_proxy_gate(self) -> None:
        config = read_json(CONFIG)
        self.assertEqual(config["codex"]["skills"], EXPECTED_SKILL_ORDER)
        self.assertEqual(config["generic"]["modules"], EXPECTED_MODULES)
        self.assertIn("workflow-token-proxy", config["required_validation_checks"])
        self.assertEqual(config["codex"]["archive"], "codex/ask-then-do-it-1.3.0.zip")
        self.assertEqual(config["generic"]["directory"], "generic/ask-then-do-it-generic-1.3.0")
        self.assertEqual(config["generic"]["archive"], "generic/ask-then-do-it-generic-1.3.0.zip")

    def test_source_runtime_versions_and_generic_order_are_current(self) -> None:
        generic = ROOT / "adapters" / "generic-prompts"
        for module in EXPECTED_MODULES:
            body = (generic / module).read_text(encoding="utf-8")
            with self.subTest(module=module):
                self.assertTrue(
                    f"Prompt version: `{RELEASE_VERSION}`" in body,
                    f"{module} must declare prompt version {RELEASE_VERSION}",
                )
                self.assertTrue(
                    f"Core version: `{CORE_VERSION}`" in body,
                    f"{module} must declare Core version {CORE_VERSION}",
                )

        codex_skills = ROOT / "adapters" / "codex" / "plugin" / "ask-then-do-it" / "skills"
        for skill in EXPECTED_SKILLS:
            body = (codex_skills / skill / "SKILL.md").read_text(encoding="utf-8")
            with self.subTest(skill=skill):
                if "core_version" in body:
                    self.assertTrue(
                        "core_version` `1.2.0`" not in body,
                        f"{skill} still emits the previous active Core identity",
                    )

    def test_release_builder_rejects_marketplace_ref_version_drift(self) -> None:
        builder = load_builder_module()
        catalog = read_json(ROOT / ".agents" / "plugins" / "marketplace.json")
        catalog["plugins"][0]["source"]["ref"] = "v1.2.0"

        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            candidate = Path(temporary) / "marketplace.json"
            candidate.write_text(json.dumps(catalog), encoding="utf-8")
            with mock.patch.object(builder, "MARKETPLACE_CATALOG", candidate):
                with self.assertRaisesRegex(builder.BuildError, "marketplace.*v1.3.0"):
                    builder.load_config(CONFIG)

    def test_builder_emits_exact_1_3_runtime_packages_and_reference_inventory(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            output = Path(temporary) / "dist"
            result = run_builder(output)
            if result.returncode != 0:
                self.fail(f"builder did not produce the approved 1.3.0 package: {result.stderr}")

            codex = output / "codex" / "ask-then-do-it"
            generic = output / "generic" / "ask-then-do-it-generic-1.3.0"
            self.assertTrue(codex.is_dir(), codex)
            self.assertTrue(generic.is_dir(), generic)
            self.assertEqual(
                {path.name for path in (codex / "skills").iterdir() if path.is_dir()},
                EXPECTED_SKILLS,
            )
            self.assertTrue(
                (codex / "skills" / "ask-then-do-it" / "references" / "lite-workflow.md").is_file()
            )
            self.assertTrue((codex / "assets" / "icon.png").is_file())
            self.assertTrue((codex / "assets" / "logo.png").is_file())
            self.assertFalse(any(path.name == "marketplace.json" for path in codex.rglob("*")))
            self.assertEqual(
                {path.name for path in (generic / "prompts").iterdir() if path.is_file()},
                set(EXPECTED_MODULES),
            )
            self.assertFalse((generic / "assets").exists())
            self.assertFalse(any(path.name == "marketplace.json" for path in generic.rglob("*")))
            combined = (generic / "generic-workflow.md").read_text(encoding="utf-8")
            self.assertEqual(combined.count("BEGIN SOURCE: lite-workflow.md"), 1)
            self.assertEqual(
                [combined.index(f"BEGIN SOURCE: {name}") for name in EXPECTED_MODULES],
                sorted(combined.index(f"BEGIN SOURCE: {name}") for name in EXPECTED_MODULES),
            )
            manifest = (generic / "manifest.yaml").read_text(encoding="utf-8")
            self.assertIn('release_version: "1.3.0"', manifest)
            self.assertIn('core_version: "1.3.0"', manifest)

            for host, package in (("codex", codex), ("generic", generic)):
                for locale in ("en", "zh-TW", "ja"):
                    body = (package / f"START-HERE.{locale}.md").read_text(
                        encoding="utf-8"
                    )
                    with self.subTest(host=host, locale=locale):
                        self.assertNotIn("](/docs/guides/", body)
                        self.assertIn(
                            f"{VERSIONED_GUIDE_ROOT}/{host}.{locale}.md", body
                        )
                        self.assertIn(
                            f"{VERSIONED_GUIDE_ROOT}/"
                            f"getting-started-simple.{locale}.md",
                            body,
                        )

            for provider, archive in (
                ("codex", "ask-then-do-it-1.3.0.zip"),
                ("generic", "ask-then-do-it-generic-1.3.0.zip"),
            ):
                with zipfile.ZipFile(output / provider / archive) as bundle:
                    self.assertTrue(bundle.namelist())
                    self.assertFalse(any(name.endswith("marketplace.json") for name in bundle.namelist()))

    def test_two_clean_builds_are_byte_reproducible_and_checksums_match(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            root = Path(temporary)
            first = root / "first"
            second = root / "second"
            first_result = run_builder(first)
            second_result = run_builder(second)
            if first_result.returncode != 0:
                self.fail(first_result.stderr)
            if second_result.returncode != 0:
                self.fail(second_result.stderr)
            self.assertEqual(files_under(first), files_under(second))
            for relative in files_under(first):
                with self.subTest(relative=relative):
                    self.assertEqual((first / relative).read_bytes(), (second / relative).read_bytes())

            checksums = {}
            for line in (first / "checksums.sha256").read_text(encoding="ascii").splitlines():
                digest, relative = line.split("  ", 1)
                checksums[relative] = digest
            self.assertEqual(
                set(checksums),
                {"codex/ask-then-do-it-1.3.0.zip", "generic/ask-then-do-it-generic-1.3.0.zip"},
            )
            for relative, digest in checksums.items():
                self.assertEqual(sha256(first / relative), digest)

            for directory, archive, archive_root in (
                ("codex/ask-then-do-it", "codex/ask-then-do-it-1.3.0.zip", "ask-then-do-it"),
                ("generic/ask-then-do-it-generic-1.3.0", "generic/ask-then-do-it-generic-1.3.0.zip", "ask-then-do-it-generic-1.3.0"),
            ):
                with zipfile.ZipFile(first / archive) as bundle:
                    expected = {f"{archive_root}/{name}" for name in files_under(first / directory)}
                    actual = {name for name in bundle.namelist() if not name.endswith("/")}
                    self.assertEqual(actual, expected)
                    for name in expected:
                        self.assertEqual(bundle.read(name), (first / directory / name.removeprefix(f"{archive_root}/")).read_bytes())

    def test_approved_historical_1_2_artifacts_are_byte_identical(self) -> None:
        for relative, expected in HISTORICAL_SHA256.items():
            path = ROOT / relative
            with self.subTest(relative=relative):
                self.assertTrue(path.is_file())
                self.assertEqual(sha256(path), expected)


if __name__ == "__main__":
    unittest.main()

from tests.release.built_fixture import current_distribution

import hashlib
import importlib.util
import json
import re
import shutil
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
RELEASE_VERSION = "1.4.0"
CORE_VERSION = "1.4.0"
VERSIONED_GUIDE_ROOT = (
    "https://github.com/Mysterio1001/Ask-Then-Do-It/blob/v1.4.0/docs/guides"
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

# Immutable historical release ledgers remain in the repository. Original
# Markdown evidence is preserved in the approved external cleanup snapshot.
HISTORICAL_LEDGER_SHA256 = {
    "docs/evidence/ask-then-do-it-release-1.0.0.json": "446499092854a35eb55af31a103056f44865fed80d5bc3f05cc4995ad65aaae7",
    "docs/evidence/ask-then-do-it-release-1.1.0.json": "191ac26cd432a983d5facd97067b83690a88801868ea69b48e809f42dcc9813e",
    "docs/evidence/ask-then-do-it-release-1.2.0.json": "d89e907412bfea1c69622c106c1b34d352e2099cc60bfc5dc6ea42986cd3584c",
    "docs/evidence/ask-then-do-it-release-1.3.0.json": "953c3261aa7a4766911cf72f48fd92aac8800ffa1c60c5254d0eb3f9d7157ec3",
    "docs/evidence/ask-then-do-it-release-1.3.1.json": "a6fd7315b62fa764a24ab5571d875d097f2f8bccc8bdbb51b49d2fc31ec6b7c5",
    "docs/evidence/grill-me-release-1.0.0.json": "e6b36352a28b7089f7e599d5390f75933c3a76bbf218d4629d4e9cccf9bd52b8",
}


TOKEN_PROXY_FIXTURE_SHA256 = {
    "tests/release/fixtures/workflow-token-proxy/benchmark.json": "ca7739178900fe6b7e947bc568fc92a0cd473ef8ed7004ab2b3893514d33f6e0",
    "tests/release/fixtures/workflow-token-proxy/full/completion.md": "e382af89622cfac9d8dae36ae515c7d5d47dde74087fe701390572cb678bbf6f",
    "tests/release/fixtures/workflow-token-proxy/full/handoffs.md": "857da1de087d0c1a9f448b2febfd28ef5848f5a4392e0ba92dd43fd9d979d6fa",
    "tests/release/fixtures/workflow-token-proxy/full/implementation-evidence.md": "c28ec0a9072270e856673fb026381fba19f74b08d4e40f1af29f751c49127f29",
    "tests/release/fixtures/workflow-token-proxy/full/questions.md": "b920ae77a5d38b00cd5277b74553cc5d52f387876ea7c5259e755f2b6149869f",
    "tests/release/fixtures/workflow-token-proxy/full/review.md": "2edbca743de6da64ced7fbe9b6f008623acb3d0f1cc764bfd29c026313315bab",
    "tests/release/fixtures/workflow-token-proxy/full/scope-and-planning.md": "e5c13684f9f50c1f0fa1f31c709e4344943999ea84cb7787f933ea6a7a4b5423",
    "tests/release/fixtures/workflow-token-proxy/lite/change-brief.md": "728e1a54efb5d273097b8dd94720707b2d695964109370efe9b29d813169dfbc",
    "tests/release/fixtures/workflow-token-proxy/lite/completion.md": "39fed1b606982293da4932e89f29c6dc7d5be1cfc62959b801bac388d6b93ac1",
    "tests/release/fixtures/workflow-token-proxy/lite/handoffs.md": "3d6b3769b041d3e36f598d680c65929bac425234a5e6d730c4d7975424e421e7",
    "tests/release/fixtures/workflow-token-proxy/lite/implementation-validation.md": "4382cf59eba6bdbbca6bdfa00897d18338f123cef631a482f98cbfbe8329f14b",
    "tests/release/fixtures/workflow-token-proxy/lite/questions.md": "44888b2365be85f7ef401d45ce94286f0923cab99072cadae183b87ff9979f42",
    "tests/release/fixtures/workflow-token-proxy/lite/review.md": "084e7a4f70687d0df665d410ba0395da62b7dab23697f66eabd397eb98e99124",
}


# Git blobs in the historical tags use LF; Windows checkouts may use CRLF.
# Preserve the original hashes above and accept only these independently
# verified alternate bytes. No content or arbitrary whitespace is normalized.
HISTORICAL_CHECKOUT_ALTERNATE_SHA256 = {
    "docs/evidence/ask-then-do-it-release-1.0.0.json": "25439c4597572462fe1ef58e0e48121cca4a63a3b00af53ace7ff7942c7fa9cf",
    "docs/evidence/ask-then-do-it-release-1.1.0.json": "615968f1ab1f429b8f4dea646228778485d56d4669b01ca24b2684595659c2c6",
    "docs/evidence/ask-then-do-it-release-1.2.0.json": "2fe7d1ede91d9a415d97e72e602d148ec45094fc951ec5bbe66b09b2e4771f14",
    "docs/evidence/ask-then-do-it-release-1.3.0.json": "87d7b14af3a67bdf07389300ec522c52547efc2e54a9413ddc0773e9f3dde060",
    "docs/evidence/ask-then-do-it-release-1.3.1.json": "82c7e456acb0308b122d8b75aa10ca518bdaec3d1537336928717f936dfdb177",
    "docs/evidence/grill-me-release-1.0.0.json": "bd9861b1f5d045217f35b1aed6e8057eba29b1227171426a2c3f3116f3fce917",
    "tests/release/fixtures/workflow-token-proxy/benchmark.json": "4aef5d19720fb4e75c8c0130ae12c53554418eeeb634c99f2c4652c11a762f27",
    "tests/release/fixtures/workflow-token-proxy/full/completion.md": "17bd47126e95753f8e9e734834aefd7a22acf316692bbb76cb33dc48fc5a9a13",
    "tests/release/fixtures/workflow-token-proxy/full/handoffs.md": "74f2b89970352aa5dd379cade0d48a401c107eddd8f69a4f31a0de3a3bdb6c26",
    "tests/release/fixtures/workflow-token-proxy/full/implementation-evidence.md": "1a340bef30f7a0436621ddeffeed81eb0e7f73ed2e72ef8efd5541d8a3ea227e",
    "tests/release/fixtures/workflow-token-proxy/full/questions.md": "c6ee04d3cd67b1a10b48107f627e7a485a3ca4700e5a7d123271a083521064a8",
    "tests/release/fixtures/workflow-token-proxy/full/review.md": "665d4464071bbec1938d1bd81fdfa7e9ebff45f6684cbb6dc70bfc004e8551a7",
    "tests/release/fixtures/workflow-token-proxy/full/scope-and-planning.md": "ee61048f1c72d15d25e713d69fd486dd52a231eca8cab517386431e1228e06f5",
    "tests/release/fixtures/workflow-token-proxy/lite/change-brief.md": "9a4f163e9ccabb9f554ee1cabf169382002b6e39791d18bcbd026d15a318d8c1",
    "tests/release/fixtures/workflow-token-proxy/lite/completion.md": "191a8ba8989e8b6676b27752f7acfe4ab513e80841d5d9a40a54e0467d94e40d",
    "tests/release/fixtures/workflow-token-proxy/lite/handoffs.md": "774b789ef289724974b843435b2e935d15d6e3e00dbd41c5f026a543baeb18a6",
    "tests/release/fixtures/workflow-token-proxy/lite/implementation-validation.md": "d933f4d7387b6a005b834db4e818af5ebee1793734457e11d9342f952752ae09",
    "tests/release/fixtures/workflow-token-proxy/lite/questions.md": "86b1078c1ed07f86783cee585ca24e7dd02458b3c2633f7a628acb707cfbb700",
    "tests/release/fixtures/workflow-token-proxy/lite/review.md": "5555ce9db7a662a6ccf682818a586b61338bc22d099bc79cf77c8604bd0699a0"
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
    def assert_trees_byte_equal(self, left: Path, right: Path) -> None:
        self.assertEqual(files_under(left), files_under(right))
        for relative in files_under(left):
            self.assertEqual(
                (left / relative).read_bytes(),
                (right / relative).read_bytes(),
                relative,
            )

    def test_active_identity_and_current_document_downloads_are_current(self) -> None:
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
            "v1.4.0",
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

        ]
        for document in root_download_docs:
            body = document.read_text(encoding="utf-8")
            with self.subTest(document=document.relative_to(ROOT)):
                self.assertIn("v1.4.0", body)
                self.assertIn("ask-then-do-it-1.4.0.zip", body)
                self.assertIn("ask-then-do-it-generic-1.4.0.zip", body)

        host_contracts = (
            (
                "codex",
                [ROOT / "docs" / "guides" / f"codex.{locale}.md" for locale in ("en", "zh-TW", "ja")],
                "ask-then-do-it-1.4.0.zip",
                "ask-then-do-it-generic-1.4.0.zip",
            ),
            (
                "generic",
                [ROOT / "docs" / "guides" / f"generic.{locale}.md" for locale in ("en", "zh-TW", "ja")],
                "ask-then-do-it-generic-1.4.0.zip",
                "ask-then-do-it-1.4.0.zip",
            ),
        )
        for host, documents, required_archive, forbidden_archive in host_contracts:
            for document in documents:
                body = document.read_text(encoding="utf-8")
                with self.subTest(host=host, document=document.relative_to(ROOT)):
                    self.assertIn("v1.4.0", body)
                    self.assertIn(required_archive, body)
                    self.assertNotIn(forbidden_archive, body)
                    self.assertNotIn("1.2.0", body)

        package_starts = (
            (
                "codex",
                [ROOT / "adapters" / "codex" / "plugin" / "ask-then-do-it" / f"START-HERE.{locale}.md" for locale in ("en", "zh-TW", "ja")],
                "ask-then-do-it-generic-1.4.0.zip",
            ),
            (
                "generic",
                [ROOT / "release" / "generic" / f"START-HERE.{locale}.md" for locale in ("en", "zh-TW", "ja")],
                "ask-then-do-it-1.4.0.zip",
            ),
        )
        for host, documents, forbidden_archive in package_starts:
            for document in documents:
                body = document.read_text(encoding="utf-8")
                with self.subTest(host=host, document=document.relative_to(ROOT)):
                    self.assertIn("1.4.0", body)
                    self.assertNotIn(forbidden_archive, body)

    def test_release_config_locks_runtime_inventory_and_proxy_gate(self) -> None:
        config = read_json(CONFIG)
        self.assertEqual(config["codex"]["skills"], EXPECTED_SKILL_ORDER)
        self.assertEqual(config["generic"]["modules"], EXPECTED_MODULES)
        self.assertIn("workflow-token-proxy", config["required_validation_checks"])
        self.assertEqual(config["codex"]["archive"], "codex/ask-then-do-it-1.4.0.zip")
        self.assertEqual(config["generic"]["directory"], "generic/ask-then-do-it-generic-1.4.0")
        self.assertEqual(config["generic"]["archive"], "generic/ask-then-do-it-generic-1.4.0.zip")

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
                with self.assertRaisesRegex(builder.BuildError, "marketplace.*v1.4.0"):
                    builder.load_config(CONFIG)

    def test_builder_emits_exact_1_3_runtime_packages_and_reference_inventory(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            output = Path(temporary) / "dist"
            result = run_builder(output)
            if result.returncode != 0:
                self.fail(f"builder did not produce the approved 1.4.0 package: {result.stderr}")

            codex = output / "codex" / "ask-then-do-it"
            generic = output / "generic" / "ask-then-do-it-generic-1.4.0"
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
            self.assertIn('release_version: "1.4.0"', manifest)
            self.assertIn('core_version: "1.4.0"', manifest)

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
                ("codex", "ask-then-do-it-1.4.0.zip"),
                ("generic", "ask-then-do-it-generic-1.4.0.zip"),
            ):
                with zipfile.ZipFile(output / provider / archive) as bundle:
                    self.assertTrue(bundle.namelist())
                    self.assertFalse(any(name.endswith("marketplace.json") for name in bundle.namelist()))

    def test_consumer_sources_packages_and_archives_exclude_pillow(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            output = Path(temporary) / "dist"
            result = run_builder(output)
            if result.returncode != 0:
                self.fail(result.stderr)

            codex = output / "codex" / "ask-then-do-it"
            generic = output / "generic" / "ask-then-do-it-generic-1.4.0"
            roots = (
                ROOT / "adapters" / "codex" / "plugin" / "ask-then-do-it",
                ROOT / "adapters" / "generic-prompts",
                codex,
                generic,
            )
            for root in roots:
                for relative in files_under(root):
                    segments = {segment.casefold() for segment in relative.split("/")}
                    with self.subTest(root=root, relative=relative):
                        self.assertNotIn("pillow", segments)
                        self.assertNotIn("pil", segments)

            plugin = read_json(codex / ".codex-plugin" / "plugin.json")
            self.assertNotIn("dependencies", plugin)
            self.assertNotIn("pillow", json.dumps(plugin).casefold())
            manifest = (generic / "manifest.yaml").read_text(encoding="utf-8")
            self.assertNotIn("pillow", manifest.casefold())
            self.assertNotIn("\ndependencies:", f"\n{manifest.casefold()}")

            for archive in (
                output / "codex" / "ask-then-do-it-1.4.0.zip",
                output / "generic" / "ask-then-do-it-generic-1.4.0.zip",
            ):
                with zipfile.ZipFile(archive) as bundle:
                    for name in bundle.namelist():
                        segments = {segment.casefold() for segment in name.split("/")}
                        with self.subTest(archive=archive.name, name=name):
                            self.assertNotIn("pillow", segments)
                            self.assertNotIn("pil", segments)

    def test_clean_builds_and_default_dist_are_byte_reproducible(self) -> None:
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
            self.assert_trees_byte_equal(first, second)
            self.assert_trees_byte_equal(first, current_distribution())

            checksums = {}
            for line in (first / "checksums.sha256").read_text(encoding="ascii").splitlines():
                digest, relative = line.split("  ", 1)
                checksums[relative] = digest
            self.assertEqual(
                set(checksums),
                {"codex/ask-then-do-it-1.4.0.zip", "generic/ask-then-do-it-generic-1.4.0.zip", "claude/ask-then-do-it-claude-1.4.0.zip"},
            )
            for relative, digest in checksums.items():
                self.assertEqual(sha256(first / relative), digest)

            for directory, archive, archive_root in (
                ("claude/ask-then-do-it", "claude/ask-then-do-it-claude-1.4.0.zip", "ask-then-do-it"),
                ("codex/ask-then-do-it", "codex/ask-then-do-it-1.4.0.zip", "ask-then-do-it"),
                ("generic/ask-then-do-it-generic-1.4.0", "generic/ask-then-do-it-generic-1.4.0.zip", "ask-then-do-it-generic-1.4.0"),
            ):
                with zipfile.ZipFile(first / archive) as bundle:
                    expected = {f"{archive_root}/{name}" for name in files_under(first / directory)}
                    actual = {name for name in bundle.namelist() if not name.endswith("/")}
                    self.assertEqual(actual, expected)
                    for name in expected:
                        self.assertEqual(bundle.read(name), (first / directory / name.removeprefix(f"{archive_root}/")).read_bytes())

            drifted = root / "drifted"
            shutil.copytree(first, drifted)
            extra = drifted / "codex" / "ask-then-do-it" / "pillow-stale.txt"
            extra.write_text("not part of the release", encoding="utf-8")
            with self.assertRaises(AssertionError):
                self.assert_trees_byte_equal(first, drifted)

            extra.unlink()
            changed = drifted / "checksums.sha256"
            changed.write_bytes(changed.read_bytes() + b"\n")
            with self.assertRaises(AssertionError):
                self.assert_trees_byte_equal(first, drifted)

    def test_historical_release_ledgers_are_byte_identical(self) -> None:
        for relative, expected in HISTORICAL_LEDGER_SHA256.items():
            path = ROOT / relative
            with self.subTest(relative=relative):
                self.assertTrue(path.is_file())
                self.assertIn(sha256(path), {expected, HISTORICAL_CHECKOUT_ALTERNATE_SHA256[relative]})


    def test_frozen_token_proxy_fixture_bytes_are_identical(self) -> None:
        for relative, expected in TOKEN_PROXY_FIXTURE_SHA256.items():
            path = ROOT / relative
            with self.subTest(relative=relative):
                self.assertTrue(path.is_file())
                self.assertIn(sha256(path), {expected, HISTORICAL_CHECKOUT_ALTERNATE_SHA256[relative]})


if __name__ == "__main__":
    unittest.main()

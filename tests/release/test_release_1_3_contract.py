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
RELEASE_VERSION = "1.3.1"
CORE_VERSION = "1.3.1"
VERSIONED_GUIDE_ROOT = (
    "https://github.com/Mysterio1001/Ask-Then-Do-It/blob/v1.3.1/docs/guides"
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
HISTORICAL_1_2_SHA256 = {
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

# These approved 1.3.0 workflow and release artifacts are immutable historical
# inputs to the 1.3.1 maintenance release.
HISTORICAL_1_3_SHA256 = {
    "docs/evidence/ask-then-do-it-1.3.0-evidence-closure-after-footer.md": "2c825e118b66b5de34031291365d3ae2ecb6c2e09a52f31af8c2879376725953",
    "docs/evidence/ask-then-do-it-1.3.0-evidence-closure-review.md": "77ae04cb53d16b7b4aa0b348cc32cf12565036b747b1f44a4cf0fec845eccc60",
    "docs/evidence/ask-then-do-it-1.3.0-final-independent-review-after-p2.md": "0ad622004ae2761e49aed51497c828576bd1a1ad9c3bf9653fb03db47319b21c",
    "docs/evidence/ask-then-do-it-1.3.0-final-review-after-fixes.md": "88883120fc16635494a5b87d9ff3acf74a38f5e989fa2cf922bb8ee3c4e4a53f",
    "docs/evidence/ask-then-do-it-1.3.0-final-review.md": "62ee6ad803e56553aef97e8bf8b200a685f6dab26f6949b003ec8d259d675f41",
    "docs/evidence/ask-then-do-it-1.3.0-release-architecture-diagnosis-after-fix.md": "124d8f85aecd3a892b53a41fa24d3be51651484f510a5f9ec6e16fc2486d5842",
    "docs/evidence/ask-then-do-it-1.3.0-release-architecture-diagnosis-after-p2-fix.md": "3c19373d8d508b5d6c2f4f29739b96c1b0854bd216ae39f9b95a1e5c4de99558",
    "docs/evidence/ask-then-do-it-1.3.0-release-architecture-diagnosis-after-review-fixes.md": "7133ca782a3482c5899c33039ba1c8d0cc5d7c0bed807fe5e22e6e49683affbf",
    "docs/evidence/ask-then-do-it-1.3.0-release-architecture-diagnosis.md": "c5039f4b46237efa8ccc4fb3761259ad30e194ae4abf0234ad01d6ec67f28f04",
    "docs/evidence/ask-then-do-it-1.3.0-user-document-footer-independent-review.md": "712bb43aa8dcc57d2d4cda0e83caa0cbb0d86f11a180cb345ee05e175177889b",
    "docs/evidence/ask-then-do-it-release-1.3.0.json": "953c3261aa7a4766911cf72f48fd92aac8800ffa1c60c5254d0eb3f9d7157ec3",
    "docs/evidence/ask-then-do-it-release-1.3.0.md": "dda885aaf119e8818bf8ac079230c9e8164acf984a2b4f634d608fe45a07418a",
    "docs/evidence/lite-workflow-mode-1.3.0-direct-entry-correction-review-after-p2.md": "35ea5da8940a3760fd1a918431bd8b462cd93b508f7d89b511568d6e8200c6a9",
    "docs/evidence/lite-workflow-mode-1.3.0-direct-entry-correction-review.md": "9f89fa4f14507d972108797491975c81b2e5e422939aa0ab066f79b5f226321a",
    "docs/evidence/lite-workflow-mode-1.3.0-final-review-corrections-review.md": "7dd24554bc358ae52b519840a155029e6c5845b161fd468db7e90b4a7c906c9e",
    "docs/evidence/lite-workflow-mode-1.3.0-final-review-corrections.md": "52864e806e6cb3a65b4e2d257aeca66d8828c30ac979b8920503eccd2765b638",
    "docs/evidence/lite-workflow-mode-1.3.0-package-link-correction-review.md": "aa25c8eab06082d8ff6bfcc9e90db9819451ce798bee11fed8e092697e7471db",
    "docs/evidence/lite-workflow-mode-1.3.0-package-link-correction.md": "34c4ae7123ebbcd5c01f80d928aed36c35e10f132c9bef329a52d43dce8a79d6",
    "docs/evidence/lite-workflow-mode-1.3.0-ticket-1-review-after-fixes.md": "d3f89882c3f4ae4420f0e982036707ee3534af1488a965a1425390ad6bdaf489",
    "docs/evidence/lite-workflow-mode-1.3.0-ticket-1-review.md": "83a995394ef35336f4ea0cc7cf08ba6ac1aa4d77a2df750d3a27c07f707b4974",
    "docs/evidence/lite-workflow-mode-1.3.0-ticket-1.md": "f0ff972f5cd8d76cc207fbfb2bd5f00c3cb4b891bb9bcc5eab1c08f69e9a0796",
    "docs/evidence/lite-workflow-mode-1.3.0-ticket-2-review.md": "e57e07e62e414cd32dad8a836606037896eae5e3490dac3f51bf89ee269a8739",
    "docs/evidence/lite-workflow-mode-1.3.0-ticket-2.md": "31d8509096a796557a305d9cc30e277b0fb6719459ebc395adae7f8a6c322a52",
    "docs/evidence/lite-workflow-mode-1.3.0-ticket-3-review.md": "a2b488fde3b034ee990124c5d803671a3cc169ee7b50e356b5d77a766689b4ec",
    "docs/evidence/lite-workflow-mode-1.3.0-ticket-3.md": "91a28b9cb31b8bb8ba95e2ed641829f817796fe5f9699891d5c8a3fe062807eb",
    "docs/evidence/lite-workflow-mode-1.3.0-ticket-4-review-after-fixes.md": "35d5370465b00c796b157f7fc11ecaf86410f0a6cbd83666f8d5a109d1baf997",
    "docs/evidence/lite-workflow-mode-1.3.0-ticket-4-review-final.md": "51b5478a460df6841c953dac6f09e83787ae28770595c46a71a0eb503be8b8b4",
    "docs/evidence/lite-workflow-mode-1.3.0-ticket-4-review.md": "cded0a189d9946af4ddd0eca372ec651727dfc566f3f36b443b4ccfb76a94ca1",
    "docs/evidence/lite-workflow-mode-1.3.0-ticket-4.md": "8c8553debf03486edfdfccb46a36f3662b9a054417787f9f2a1443f904fbb604",
    "docs/evidence/lite-workflow-mode-1.3.0-ticket-5-review-closure.md": "f85df1d5aa18ff79b0f5de3a6bf2b851c6b43e071435dba800d2c4cbd75cb6f6",
    "docs/evidence/lite-workflow-mode-1.3.0-ticket-5-review-final.md": "75ee2564b314fd31f70df06800249ac915aa9b6b2400cb5a3e75d1a12b2fcce6",
    "docs/evidence/lite-workflow-mode-1.3.0-ticket-5-review.md": "57b01180a04bc4b32be392a3009140b0eaf2e69dbda7614bdd9b8b55153c28d4",
    "docs/evidence/lite-workflow-mode-1.3.0-ticket-5.md": "59f2b3dc6b263cf20565943c5a7ff4ad8594736505c469102c98fbb0373ab1a5",
    "docs/evidence/lite-workflow-mode-1.3.0-ticket-6-review-closure.md": "3e6749bc49b4b581bfeb2a1fb5ab8c258ec8d4126c2dde582e8646df2086c1a4",
    "docs/evidence/lite-workflow-mode-1.3.0-ticket-6-review-final.md": "8ffd3701e7a79dce4595c3f2bfd1a2320e8b79e03ffe23f8ca6cb1d22313257e",
    "docs/evidence/lite-workflow-mode-1.3.0-ticket-6-review.md": "083ebef3f392bd2c5070ad6106a80c2c070dd8b2fc697184be22f8905c53ab4b",
    "docs/evidence/lite-workflow-mode-1.3.0-ticket-6.md": "4a72a70f9c500d3c57ee4e98eec44d333d7b3175016a1b364969421b677cecd7",
    "docs/evidence/lite-workflow-mode-1.3.0-ticket-7-review.md": "acca0c35cf1afc70c434a2278f4b7295ca848813cdcc5cf1d8c900cc1424d2bc",
    "docs/evidence/lite-workflow-mode-1.3.0-ticket-7.md": "49cb74ec487d1f9be4787d55b745b5ef2b1fcf9a8c6d2a5ebd103171dcb06c39",
    "docs/evidence/lite-workflow-mode-1.3.0-ticket-8.md": "f7addea7d8f67c450c8ff2a2c87e39ac9dbd6f26b6e6f44a9e44cf5566c6be89",
    "docs/plans/lite-workflow-mode-1.3.0.md": "d0884eab5d170ca92427411ef22c948f48c0998d658032a9cc481c40a10a4454",
    "docs/requirements/lite-workflow-mode-1.3.0.md": "79bd50f12c6710c819ea727dbfeff72323eb2d85344c37928d37b7f81657abc0",
    "docs/specs/lite-workflow-mode-1.3.0.md": "a2e0a828c9351506bea269f284120c90ebfbde81768c1ba9d26ab08ad28357ac",
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

    def test_active_identity_and_current_document_downloads_are_1_3_1(self) -> None:
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
            "v1.3.1",
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
                self.assertIn("v1.3.1", body)
                self.assertIn("ask-then-do-it-1.3.1.zip", body)
                self.assertIn("ask-then-do-it-generic-1.3.1.zip", body)

        host_contracts = (
            (
                "codex",
                [ROOT / "docs" / "guides" / f"codex.{locale}.md" for locale in ("en", "zh-TW", "ja")],
                "ask-then-do-it-1.3.1.zip",
                "ask-then-do-it-generic-1.3.1.zip",
            ),
            (
                "generic",
                [ROOT / "docs" / "guides" / f"generic.{locale}.md" for locale in ("en", "zh-TW", "ja")],
                "ask-then-do-it-generic-1.3.1.zip",
                "ask-then-do-it-1.3.1.zip",
            ),
        )
        for host, documents, required_archive, forbidden_archive in host_contracts:
            for document in documents:
                body = document.read_text(encoding="utf-8")
                with self.subTest(host=host, document=document.relative_to(ROOT)):
                    self.assertIn("v1.3.1", body)
                    self.assertIn(required_archive, body)
                    self.assertNotIn(forbidden_archive, body)
                    self.assertNotIn("1.2.0", body)

        package_starts = (
            (
                "codex",
                [ROOT / "adapters" / "codex" / "plugin" / "ask-then-do-it" / f"START-HERE.{locale}.md" for locale in ("en", "zh-TW", "ja")],
                "ask-then-do-it-generic-1.3.1.zip",
            ),
            (
                "generic",
                [ROOT / "release" / "generic" / f"START-HERE.{locale}.md" for locale in ("en", "zh-TW", "ja")],
                "ask-then-do-it-1.3.1.zip",
            ),
        )
        for host, documents, forbidden_archive in package_starts:
            for document in documents:
                body = document.read_text(encoding="utf-8")
                with self.subTest(host=host, document=document.relative_to(ROOT)):
                    self.assertIn("1.3.1", body)
                    self.assertNotIn(forbidden_archive, body)

    def test_release_config_locks_runtime_inventory_and_proxy_gate(self) -> None:
        config = read_json(CONFIG)
        self.assertEqual(config["codex"]["skills"], EXPECTED_SKILL_ORDER)
        self.assertEqual(config["generic"]["modules"], EXPECTED_MODULES)
        self.assertIn("workflow-token-proxy", config["required_validation_checks"])
        self.assertEqual(config["codex"]["archive"], "codex/ask-then-do-it-1.3.1.zip")
        self.assertEqual(config["generic"]["directory"], "generic/ask-then-do-it-generic-1.3.1")
        self.assertEqual(config["generic"]["archive"], "generic/ask-then-do-it-generic-1.3.1.zip")

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
                with self.assertRaisesRegex(builder.BuildError, "marketplace.*v1.3.1"):
                    builder.load_config(CONFIG)

    def test_builder_emits_exact_1_3_runtime_packages_and_reference_inventory(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            output = Path(temporary) / "dist"
            result = run_builder(output)
            if result.returncode != 0:
                self.fail(f"builder did not produce the approved 1.3.1 package: {result.stderr}")

            codex = output / "codex" / "ask-then-do-it"
            generic = output / "generic" / "ask-then-do-it-generic-1.3.1"
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
            self.assertIn('release_version: "1.3.1"', manifest)
            self.assertIn('core_version: "1.3.1"', manifest)

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
                ("codex", "ask-then-do-it-1.3.1.zip"),
                ("generic", "ask-then-do-it-generic-1.3.1.zip"),
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
            generic = output / "generic" / "ask-then-do-it-generic-1.3.1"
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
                output / "codex" / "ask-then-do-it-1.3.1.zip",
                output / "generic" / "ask-then-do-it-generic-1.3.1.zip",
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
            self.assert_trees_byte_equal(first, ROOT / "dist")

            checksums = {}
            for line in (first / "checksums.sha256").read_text(encoding="ascii").splitlines():
                digest, relative = line.split("  ", 1)
                checksums[relative] = digest
            self.assertEqual(
                set(checksums),
                {"codex/ask-then-do-it-1.3.1.zip", "generic/ask-then-do-it-generic-1.3.1.zip"},
            )
            for relative, digest in checksums.items():
                self.assertEqual(sha256(first / relative), digest)

            for directory, archive, archive_root in (
                ("codex/ask-then-do-it", "codex/ask-then-do-it-1.3.1.zip", "ask-then-do-it"),
                ("generic/ask-then-do-it-generic-1.3.1", "generic/ask-then-do-it-generic-1.3.1.zip", "ask-then-do-it-generic-1.3.1"),
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

    def test_approved_historical_1_2_artifacts_are_byte_identical(self) -> None:
        for relative, expected in HISTORICAL_1_2_SHA256.items():
            path = ROOT / relative
            with self.subTest(relative=relative):
                self.assertTrue(path.is_file())
                self.assertEqual(sha256(path), expected)

    def test_approved_historical_1_3_artifacts_are_byte_identical(self) -> None:
        for relative, expected in HISTORICAL_1_3_SHA256.items():
            path = ROOT / relative
            with self.subTest(relative=relative):
                self.assertTrue(path.is_file())
                self.assertEqual(sha256(path), expected)

    def test_frozen_token_proxy_fixture_bytes_are_identical(self) -> None:
        for relative, expected in TOKEN_PROXY_FIXTURE_SHA256.items():
            path = ROOT / relative
            with self.subTest(relative=relative):
                self.assertTrue(path.is_file())
                self.assertEqual(sha256(path), expected)


if __name__ == "__main__":
    unittest.main()

import hashlib
import io
import json
import math
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unicodedata
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "validate_codex_contract.py"
ADAPTER = ROOT / "adapters" / "codex"
SOURCE_PACKAGE = ADAPTER / "plugin" / "ask-then-do-it"
RULE_MAPPING = ADAPTER / "rule-mapping.yaml"
CORE_CATALOG = ROOT / "core" / "rules" / "rules.yaml"
CONFORMANCE = ADAPTER / "conformance.yaml"
BASELINE = ROOT / "docs" / "evidence" / "codex-skill-runtime-slimming-t1-baseline.json"
BASELINE_SHA256 = "f1970671ef31829ea9dde3c64236a8edc1eeaada3132bcfeda0497d88f775dfe"

PUBLIC_SKILLS = (
    "ask-requirements",
    "ask-then-do-it",
    "ask-with-docs",
    "implement-direct",
    "implement-tdd",
    "improve-architecture",
    "plan-tickets",
    "review-code",
    "write-spec",
)


def run_validator(
    *,
    adapter_root: Path = ADAPTER,
    source_package: Path = SOURCE_PACKAGE,
    package_root: Path | None = None,
    rule_mapping: Path = RULE_MAPPING,
    core_catalog: Path | None = None,
    conformance: Path | None = None,
    report: Path | None = None,
) -> subprocess.CompletedProcess[str]:
    if core_catalog is None:
        core_catalog = CORE_CATALOG if adapter_root == ADAPTER else adapter_root / "core-rules.yaml"
        if not core_catalog.exists():
            write_text(
                core_catalog,
                "core_version: 1.4.1\n"
                "rules:\n"
                "  - id: TEST-RULE-001\n"
                "    mandatory: true\n",
            )
    if conformance is None:
        conformance = CONFORMANCE if adapter_root == ADAPTER else adapter_root / "conformance.yaml"
        if not conformance.exists():
            write_text(
                conformance,
                "core_version: 1.4.1\n"
                "implemented_rules:\n"
                "  - TEST-RULE-001\n",
            )
    command = [
        sys.executable,
        "-X",
        "utf8",
        str(SCRIPT),
        "--adapter-root",
        str(adapter_root),
        "--source-package-root",
        str(source_package),
        "--package-root",
        str(package_root or source_package),
        "--rule-mapping",
        str(rule_mapping),
        "--core-catalog",
        str(core_catalog),
        "--conformance",
        str(conformance),
        "--json",
    ]
    if report is not None:
        command.extend(("--report", str(report)))
    if source_package != SOURCE_PACKAGE:
        command.append("--validate-only")
    return subprocess.run(
        command,
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_mapping(path: Path, *, source: str, section: str) -> None:
    write_text(
        path,
        "core_version: 1.4.1\n"
        "rules:\n"
        "  TEST-RULE-001:\n"
        f"    - file: {source}\n"
        f"      section: {section}\n"
        "      implementation: fixture mapping\n",
    )


def create_package(root: Path, *, link: str = "references/contract.md") -> Path:
    package = root / "plugin" / "ask-then-do-it"
    write_text(
        package / "skills" / "consumer" / "SKILL.md",
        "---\nname: consumer\ndescription: fixture\n---\n\n"
        "# Fixture\n\n## Consumer\n\n"
        f"Read the [contract]({link}) before acting.\n",
    )
    write_text(
        package / "skills" / "consumer" / "references" / "contract.md",
        "# Contract\n\n## Required behavior\n\nFixture.\n",
    )
    return package


def normalized_context(paths: list[Path]) -> bytes:
    parts = []
    for path in paths:
        text = unicodedata.normalize("NFC", path.read_text(encoding="utf-8"))
        parts.append(re.sub(r"\s+", " ", text, flags=re.UNICODE).strip())
    return "\n".join(parts).encode("utf-8")


class CodexContractValidatorTests(unittest.TestCase):
    def test_t1_baseline_is_immutable_and_well_formed(self) -> None:
        baseline_bytes = BASELINE.read_bytes()
        self.assertEqual(hashlib.sha256(baseline_bytes).hexdigest(), BASELINE_SHA256)
        baseline = json.loads(baseline_bytes)

        self.assertEqual(baseline["schema_version"], 1)
        algorithm = baseline["algorithm"]
        self.assertEqual(algorithm["id"], "normalized-utf8-quarter-v1")
        self.assertEqual(algorithm["bytes_per_proxy_token"], 4)
        self.assertFalse(algorithm["billing_guarantee"])
        self.assertFalse(algorithm["total_context_guarantee"])
        self.assertIn("source-level", algorithm["limitation"])
        self.assertEqual(tuple(baseline["source_files"]), PUBLIC_SKILLS)

    def test_current_codex_contract_is_reproducible(self) -> None:
        actual_reports = []
        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            for index in range(2):
                report = Path(temporary) / f"report-{index}.json"
                result = run_validator(report=report)

                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertTrue(report.is_file())
                actual = json.loads(result.stdout)
                self.assertEqual(actual, json.loads(report.read_text(encoding="utf-8")))
                actual_reports.append(actual)

        self.assertEqual(actual_reports[0], actual_reports[1])
        actual = actual_reports[0]
        self.assertEqual(actual["schema_version"], 1)
        algorithm = actual["algorithm"]
        self.assertEqual(algorithm["id"], "normalized-utf8-quarter-v1")
        self.assertEqual(algorithm["bytes_per_proxy_token"], 4)
        self.assertFalse(algorithm["billing_guarantee"])
        self.assertFalse(algorithm["total_context_guarantee"])
        self.assertIn("source-level", algorithm["limitation"])

        source_files = actual["source_files"]
        self.assertEqual(tuple(source_files), PUBLIC_SKILLS)
        root_skill = SOURCE_PACKAGE / "skills" / "ask-then-do-it" / "SKILL.md"
        root_measurement = source_files["ask-then-do-it"]
        self.assertEqual(root_measurement["raw_utf8_bytes"], len(root_skill.read_bytes()))
        self.assertEqual(
            root_measurement["whitespace_words"],
            len(root_skill.read_text(encoding="utf-8").split()),
        )
        self.assertEqual(
            root_measurement["sha256"],
            hashlib.sha256(root_skill.read_bytes()).hexdigest(),
        )

    def test_codex_runtime_bytes_are_pinned_to_lf(self) -> None:
        attributes = (ROOT / ".gitattributes").read_text(encoding="utf-8")
        self.assertIn(
            "adapters/codex/plugin/ask-then-do-it/** text eol=lf -filter -working-tree-encoding -ident",
            attributes.splitlines(),
        )
        self.assertIn(
            "adapters/codex/plugin/ask-then-do-it/assets/icon.png -text -eol -filter -working-tree-encoding -ident",
            attributes.splitlines(),
        )
        self.assertIn(
            "adapters/codex/plugin/ask-then-do-it/assets/logo.png -text -eol -filter -working-tree-encoding -ident",
            attributes.splitlines(),
        )

        attribute_result = subprocess.run(
            [
                "git",
                "check-attr",
                "text",
                "--",
                "adapters/codex/plugin/ask-then-do-it/assets/icon.png",
                "adapters/codex/plugin/ask-then-do-it/assets/logo.png",
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(attribute_result.returncode, 0, attribute_result.stderr)
        self.assertEqual(
            attribute_result.stdout.splitlines(),
            [
                "adapters/codex/plugin/ask-then-do-it/assets/icon.png: text: unset",
                "adapters/codex/plugin/ask-then-do-it/assets/logo.png: text: unset",
            ],
        )

        text_suffixes = {".json", ".md", ".yaml", ".yml"}
        runtime_files = sorted(
            path
            for path in SOURCE_PACKAGE.rglob("*")
            if path.is_file() and path.suffix.casefold() in text_suffixes
        )
        self.assertTrue(runtime_files)
        for path in runtime_files:
            with self.subTest(path=path.relative_to(ROOT)):
                self.assertNotIn(b"\r", path.read_bytes())

    def test_measurement_uses_normalized_utf8_and_ordered_load_sets(self) -> None:
        module_root = str(ROOT / "scripts")
        if module_root not in sys.path:
            sys.path.insert(0, module_root)
        import validate_codex_contract as contract

        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            temp_root = Path(temporary)
            package = create_package(temp_root)
            first = package / "skills" / "consumer" / "SKILL.md"
            second = package / "skills" / "consumer" / "references" / "contract.md"
            write_text(first, "A\\n\\n cafe\u0301 \\t B\\n")
            write_text(second, "Second\\n  file\\n")

            measurement = contract.measure_load_set(
                package,
                ("skills/consumer/SKILL.md", "skills/consumer/references/contract.md"),
            )
            normalized = normalized_context([first, second])
        self.assertEqual(measurement["normalized_utf8_bytes"], len(normalized))
        self.assertEqual(
            measurement["loaded_context_proxy"], math.ceil(len(normalized) / 4)
        )
        self.assertEqual(
            measurement["sources"],
            [
                "skills/consumer/SKILL.md",
                "skills/consumer/references/contract.md",
            ],
        )

    def test_source_measurement_read_errors_fail_closed(self) -> None:
        module_root = str(ROOT / "scripts")
        if module_root not in sys.path:
            sys.path.insert(0, module_root)
        import validate_codex_contract as contract

        with mock.patch.object(
            Path,
            "read_bytes",
            autospec=True,
            side_effect=PermissionError("denied"),
        ), self.assertRaises(contract.CodexContractError) as measurement_error:
            contract.measure_source_file(SOURCE_PACKAGE, "ask-then-do-it")

        self.assertEqual(
            [item.code for item in measurement_error.exception.diagnostics],
            ["MEASUREMENT_INPUT_UNREADABLE"],
        )

    def test_source_measurement_read_error_is_a_controlled_cli_failure(self) -> None:
        module_root = str(ROOT / "scripts")
        if module_root not in sys.path:
            sys.path.insert(0, module_root)
        import validate_codex_contract as contract

        summary = mock.Mock()
        summary.reference_graph.public_skills = ("ask-then-do-it",)
        stderr = io.StringIO()
        with mock.patch.object(sys, "argv", [str(SCRIPT)]), mock.patch.object(
            contract,
            "validate_contract",
            return_value=summary,
        ), mock.patch.object(
            Path,
            "read_bytes",
            autospec=True,
            side_effect=PermissionError("denied"),
        ), mock.patch("sys.stderr", stderr):
            exit_code = contract.main()

        self.assertEqual(exit_code, 2, stderr.getvalue())
        self.assertIn("MEASUREMENT_INPUT_UNREADABLE", stderr.getvalue())
        self.assertNotIn("Traceback", stderr.getvalue())

    def test_missing_reference_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            temp_root = Path(temporary)
            package = create_package(temp_root, link="references/missing.md")
            mapping = temp_root / "rule-mapping.yaml"
            write_mapping(
                mapping,
                source="plugin/ask-then-do-it/skills/consumer/SKILL.md",
                section="Consumer",
            )
            result = run_validator(
                adapter_root=temp_root,
                source_package=package,
                rule_mapping=mapping,
            )

        self.assertEqual(result.returncode, 2)
        self.assertIn("missing reference", result.stderr.lower())

    def test_missing_canonical_lens_reference_fails_closed(self) -> None:
        module_root = str(ROOT / "scripts")
        if module_root not in sys.path:
            sys.path.insert(0, module_root)
        import validate_codex_contract as contract

        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            temp_root = Path(temporary)
            package = temp_root / "package"
            shutil.copytree(SOURCE_PACKAGE, package)
            review = package / "skills" / "review-code" / "SKILL.md"
            review.write_text(
                review.read_text(encoding="utf-8").replace(
                    "../ask-then-do-it/references/artifact-contract.md",
                    "../ask-then-do-it/references/architecture-refactoring-lenses.md",
                ),
                encoding="utf-8",
            )
            (
                package
                / "skills"
                / "ask-then-do-it"
                / "references"
                / "architecture-refactoring-lenses.md"
            ).unlink()

            graph, diagnostics = contract.validate_reference_graph(package, package)

        self.assertIsNone(graph)
        self.assertIn(
            "MISSING_REFERENCE_TARGET",
            {item.code for item in diagnostics},
        )

    def test_supported_markdown_link_forms_fail_closed_when_missing(self) -> None:
        link_forms = (
            "Read [contract][shared].\n\n[shared]: references/missing.md\n",
            "Read [contract](<references/missing contract.md>).\n",
            "Read [contract](references/missing(v2).md).\n",
        )
        for link_form in link_forms:
            with self.subTest(link_form=link_form):
                with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
                    temp_root = Path(temporary)
                    package = create_package(temp_root)
                    write_text(
                        package / "skills" / "consumer" / "SKILL.md",
                        "---\nname: consumer\ndescription: fixture\n---\n\n"
                        "# Fixture\n\n## Consumer\n\n"
                        f"{link_form}",
                    )
                    mapping = temp_root / "rule-mapping.yaml"
                    write_mapping(
                        mapping,
                        source="plugin/ask-then-do-it/skills/consumer/SKILL.md",
                        section="Consumer",
                    )
                    result = run_validator(
                        adapter_root=temp_root,
                        source_package=package,
                        rule_mapping=mapping,
                    )

                self.assertEqual(result.returncode, 2)
                self.assertIn("missing reference", result.stderr.lower())

    def test_container_reference_definitions_fail_closed_when_missing(self) -> None:
        markdown_cases = (
            "- [shared]: references/missing.md\n\nUse [shared].\n",
            "> [shared]: references/missing.md\n>\n> Use [shared].\n",
            "- [shared]:\n    references/missing.md\n\nUse [shared].\n",
            "> [shared]:\n>   references/missing.md\n>\n> Use [shared].\n",
            "> - [shared]:\n>     references/missing.md\n>\n> Use [shared].\n",
        )
        for markdown in markdown_cases:
            with self.subTest(markdown=markdown):
                with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
                    temp_root = Path(temporary)
                    package = create_package(temp_root)
                    write_text(
                        package / "skills" / "consumer" / "SKILL.md",
                        "---\nname: consumer\ndescription: fixture\n---\n\n"
                        "# Fixture\n\n## Consumer\n\n"
                        f"{markdown}",
                    )
                    mapping = temp_root / "rule-mapping.yaml"
                    write_mapping(
                        mapping,
                        source="plugin/ask-then-do-it/skills/consumer/SKILL.md",
                        section="Consumer",
                    )
                    result = run_validator(
                        adapter_root=temp_root,
                        source_package=package,
                        rule_mapping=mapping,
                    )

                self.assertEqual(result.returncode, 2, result.stderr)
                self.assertIn("missing reference", result.stderr.lower())

    def test_supported_markdown_link_forms_resolve_existing_targets(self) -> None:
        link_forms = (
            (
                "Read [contract][shared].\n\n[shared]: references/contract.md\n",
                "references/contract.md",
            ),
            (
                "Read [contract](<references/contract copy.md>).\n",
                "references/contract copy.md",
            ),
            (
                "Read [contract](references/contract(v2).md).\n",
                "references/contract(v2).md",
            ),
        )
        for link_form, target in link_forms:
            with self.subTest(link_form=link_form):
                with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
                    temp_root = Path(temporary)
                    package = create_package(temp_root)
                    write_text(
                        package / "skills" / "consumer" / "SKILL.md",
                        "---\nname: consumer\ndescription: fixture\n---\n\n"
                        "# Fixture\n\n## Consumer\n\n"
                        f"{link_form}",
                    )
                    write_text(
                        package / "skills" / "consumer" / Path(target),
                        "# Contract\n",
                    )
                    mapping = temp_root / "rule-mapping.yaml"
                    write_mapping(
                        mapping,
                        source="plugin/ask-then-do-it/skills/consumer/SKILL.md",
                        section="Consumer",
                    )
                    result = run_validator(
                        adapter_root=temp_root,
                        source_package=package,
                        rule_mapping=mapping,
                    )

                self.assertEqual(result.returncode, 0, result.stderr)

    def test_escaped_prefixes_that_still_form_links_are_scanned(self) -> None:
        module_root = str(ROOT / "scripts")
        if module_root not in sys.path:
            sys.path.insert(0, module_root)
        import validate_codex_contract as contract

        cases = (
            (r"\\[contract](references/missing.md)", "references/missing.md"),
            (r"\![contract](references/missing.md)", "references/missing.md"),
        )
        for markdown, expected in cases:
            with self.subTest(markdown=markdown):
                diagnostics: list[contract.Diagnostic] = []
                self.assertEqual(
                    contract.local_markdown_targets(markdown, diagnostics, "fixture.md"),
                    [expected],
                )
                self.assertEqual(diagnostics, [])

    def test_escaped_prefix_links_fail_closed_through_package_validation(self) -> None:
        link_forms = (
            r"Read \\[contract](references/missing.md)." "\n",
            r"Read \![contract](references/missing.md)." "\n",
        )
        for link_form in link_forms:
            with self.subTest(link_form=link_form):
                with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
                    temp_root = Path(temporary)
                    package = create_package(temp_root)
                    write_text(
                        package / "skills" / "consumer" / "SKILL.md",
                        "---\nname: consumer\ndescription: fixture\n---\n\n"
                        "# Fixture\n\n## Consumer\n\n"
                        f"{link_form}",
                    )
                    mapping = temp_root / "rule-mapping.yaml"
                    write_mapping(
                        mapping,
                        source="plugin/ask-then-do-it/skills/consumer/SKILL.md",
                        section="Consumer",
                    )
                    result = run_validator(
                        adapter_root=temp_root,
                        source_package=package,
                        rule_mapping=mapping,
                    )

                self.assertEqual(result.returncode, 2)
                self.assertIn("missing reference", result.stderr.lower())

    def test_entity_destinations_fail_closed_through_package_validation(self) -> None:
        link_forms = (
            "Read [contract](references/missing&#46;md).\n",
            "Read [contract](references/missing&#x2e;md).\n",
        )
        for link_form in link_forms:
            with self.subTest(link_form=link_form):
                with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
                    temp_root = Path(temporary)
                    package = create_package(temp_root)
                    write_text(
                        package / "skills" / "consumer" / "SKILL.md",
                        "---\nname: consumer\ndescription: fixture\n---\n\n"
                        "# Fixture\n\n## Consumer\n\n"
                        f"{link_form}",
                    )
                    mapping = temp_root / "rule-mapping.yaml"
                    write_mapping(
                        mapping,
                        source="plugin/ask-then-do-it/skills/consumer/SKILL.md",
                        section="Consumer",
                    )
                    result = run_validator(
                        adapter_root=temp_root,
                        source_package=package,
                        rule_mapping=mapping,
                    )

                self.assertEqual(result.returncode, 2)
                self.assertIn("missing reference", result.stderr.lower())

    def test_code_span_comment_opener_does_not_hide_package_link(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            temp_root = Path(temporary)
            package = create_package(temp_root)
            write_text(
                package / "skills" / "consumer" / "SKILL.md",
                "---\nname: consumer\ndescription: fixture\n---\n\n"
                "# Fixture\n\n## Consumer\n\n"
                "`<!--` [contract](references/missing.md)\n",
            )
            mapping = temp_root / "rule-mapping.yaml"
            write_mapping(
                mapping,
                source="plugin/ask-then-do-it/skills/consumer/SKILL.md",
                section="Consumer",
            )
            result = run_validator(
                adapter_root=temp_root,
                source_package=package,
                rule_mapping=mapping,
            )

        self.assertEqual(result.returncode, 2)
        self.assertIn("missing reference", result.stderr.lower())

    def test_code_and_html_comment_link_syntax_is_ignored(self) -> None:
        module_root = str(ROOT / "scripts")
        if module_root not in sys.path:
            sys.path.insert(0, module_root)
        import validate_codex_contract as contract

        markdown = (
            "`[inline](references/inline.md)`\n"
            "<!-- [comment](references/comment.md) -->\n"
            "    [indented](references/indented.md)\n"
        )
        diagnostics: list[contract.Diagnostic] = []

        self.assertEqual(
            contract.local_markdown_targets(markdown, diagnostics, "fixture.md"),
            [],
        )
        self.assertEqual(diagnostics, [])

    def test_fenced_code_requires_a_compatible_closing_fence(self) -> None:
        module_root = str(ROOT / "scripts")
        if module_root not in sys.path:
            sys.path.insert(0, module_root)
        import validate_codex_contract as contract

        cases = (
            (
                "````\n```\n[hidden](references/hidden.md)\n````\n"
                "[visible](references/visible.md)\n",
                ["references/visible.md"],
            ),
            (
                "```js\n```not-close\n[hidden](references/hidden.md)\n```\n"
                "[visible](references/visible.md)\n",
                ["references/visible.md"],
            ),
        )
        for markdown, expected in cases:
            with self.subTest(markdown=markdown):
                diagnostics: list[contract.Diagnostic] = []
                self.assertEqual(
                    contract.local_markdown_targets(markdown, diagnostics, "fixture.md"),
                    expected,
                )
                self.assertEqual(diagnostics, [])

    def test_container_fenced_code_does_not_create_runtime_references(self) -> None:
        markdown_cases = (
            "> ~~~md\n> [fake](references/missing.md)\n> ~~~\n",
            "- item\n     ~~~md\n     [fake](references/missing.md)\n     ~~~\n",
        )
        for markdown in markdown_cases:
            with self.subTest(markdown=markdown):
                with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
                    temp_root = Path(temporary)
                    package = create_package(temp_root)
                    write_text(
                        package / "skills" / "consumer" / "SKILL.md",
                        "---\nname: consumer\ndescription: fixture\n---\n\n"
                        "# Fixture\n\n## Consumer\n\n"
                        f"{markdown}",
                    )
                    mapping = temp_root / "rule-mapping.yaml"
                    write_mapping(
                        mapping,
                        source="plugin/ask-then-do-it/skills/consumer/SKILL.md",
                        section="Consumer",
                    )
                    result = run_validator(
                        adapter_root=temp_root,
                        source_package=package,
                        rule_mapping=mapping,
                    )

                self.assertEqual(result.returncode, 0, result.stderr)

    def test_container_indented_code_does_not_create_runtime_references(self) -> None:
        markdown_cases = (
            ">     [fake](references/missing.md)\n",
            "> - item\n>\n>       [fake](references/missing.md)\n",
        )
        for markdown in markdown_cases:
            with self.subTest(markdown=markdown):
                with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
                    temp_root = Path(temporary)
                    package = create_package(temp_root)
                    write_text(
                        package / "skills" / "consumer" / "SKILL.md",
                        "---\nname: consumer\ndescription: fixture\n---\n\n"
                        "# Fixture\n\n## Consumer\n\n"
                        f"{markdown}",
                    )
                    mapping = temp_root / "rule-mapping.yaml"
                    write_mapping(
                        mapping,
                        source="plugin/ask-then-do-it/skills/consumer/SKILL.md",
                        section="Consumer",
                    )
                    result = run_validator(
                        adapter_root=temp_root,
                        source_package=package,
                        rule_mapping=mapping,
                    )

                self.assertEqual(result.returncode, 0, result.stderr)

    def test_markdown_lexical_and_indentation_boundaries(self) -> None:
        cases = (
            (
                r"\` [contract](references/missing.md) \`" "\n",
                2,
            ),
            (
                "text <!-- ` --> [contract](references/missing.md) `\n",
                2,
            ),
            (
                "- item\n    [contract](references/missing.md)\n",
                2,
            ),
            (
                "- owner:\n    - [contract](references/missing.md)\n",
                2,
            ),
            (
                "- owner:\n     - [contract](references/missing.md)\n",
                2,
            ),
            (
                "- owner:\n      - [contract](references/missing.md)\n",
                0,
            ),
            (
                "-     [contract](references/missing.md)\n",
                0,
            ),
            (
                "Paragraph continuation\n"
                "    [contract](references/missing.md)\n",
                2,
            ),
            (
                "Paragraph continuation\n"
                "    - [contract](references/missing.md)\n",
                2,
            ),
            (
                "Paragraph\n## Heading\n"
                "    [contract](references/missing.md)\n",
                0,
            ),
            (
                "Paragraph\n---\n"
                "    [contract](references/missing.md)\n",
                0,
            ),
            (
                "Paragraph\n> quote\n"
                "    [contract](references/missing.md)\n",
                0,
            ),
            (
                "Paragraph\n\n"
                "    [contract](references/missing.md)\n",
                0,
            ),
            (
                r"\<!-- [contract](references/missing.md) -->" "\n",
                2,
            ),
            (
                "    - [contract](references/missing.md)\n",
                0,
            ),
            (
                "\t- [contract](references/missing.md)\n",
                0,
            ),
            (
                "   - [contract](references/missing.md)\n",
                2,
            ),
            (
                "-\t[contract](references/missing.md)\n",
                2,
            ),
            (
                "    [contract](references/missing.md)\n",
                0,
            ),
            (
                " \t[contract](references/missing.md)\n",
                0,
            ),
        )
        for markdown, expected_code in cases:
            with self.subTest(markdown=markdown):
                with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
                    temp_root = Path(temporary)
                    package = create_package(temp_root)
                    write_text(
                        package / "skills" / "consumer" / "SKILL.md",
                        "---\nname: consumer\ndescription: fixture\n---\n\n"
                        "# Fixture\n\n## Consumer\n\n"
                        f"{markdown}",
                    )
                    mapping = temp_root / "rule-mapping.yaml"
                    write_mapping(
                        mapping,
                        source="plugin/ask-then-do-it/skills/consumer/SKILL.md",
                        section="Consumer",
                    )
                    result = run_validator(
                        adapter_root=temp_root,
                        source_package=package,
                        rule_mapping=mapping,
                    )

                self.assertEqual(result.returncode, expected_code, result.stderr)
                if expected_code:
                    self.assertIn("missing reference", result.stderr.lower())

    def test_valid_bare_and_escaped_destinations_are_decoded(self) -> None:
        module_root = str(ROOT / "scripts")
        if module_root not in sys.path:
            sys.path.insert(0, module_root)
        import validate_codex_contract as contract

        markdown = (
            "[apostrophe](references/contract's.md)\n"
            r"[escaped](references/contract\(v2\).md)" "\n"
        )
        diagnostics: list[contract.Diagnostic] = []

        self.assertEqual(
            contract.local_markdown_targets(markdown, diagnostics, "fixture.md"),
            ["references/contract's.md", "references/contract(v2).md"],
        )
        self.assertEqual(diagnostics, [])

    def test_escaped_reference_label_resolves(self) -> None:
        module_root = str(ROOT / "scripts")
        if module_root not in sys.path:
            sys.path.insert(0, module_root)
        import validate_codex_contract as contract

        markdown = (
            r"[a\]b]: references/missing.md" "\n"
            r"Read [contract][a\]b]." "\n"
        )
        diagnostics: list[contract.Diagnostic] = []

        self.assertEqual(
            contract.local_markdown_targets(markdown, diagnostics, "fixture.md"),
            ["references/missing.md"],
        )
        self.assertEqual(diagnostics, [])

    def test_entity_and_escape_reference_labels_resolve_together(self) -> None:
        module_root = str(ROOT / "scripts")
        if module_root not in sys.path:
            sys.path.insert(0, module_root)
        import validate_codex_contract as contract

        markdown = (
            "[a&#93;b]: references/missing.md\n"
            r"Read [contract][a\]b]." "\n"
        )
        diagnostics: list[contract.Diagnostic] = []

        self.assertEqual(
            contract.local_markdown_targets(markdown, diagnostics, "fixture.md"),
            ["references/missing.md"],
        )
        self.assertEqual(diagnostics, [])

    def test_malformed_angle_destination_fails_closed(self) -> None:
        module_root = str(ROOT / "scripts")
        if module_root not in sys.path:
            sys.path.insert(0, module_root)
        import validate_codex_contract as contract

        diagnostics: list[contract.Diagnostic] = []
        targets = contract.local_markdown_targets(
            "[contract](<references/contract.md>garbage)\n",
            diagnostics,
            "fixture.md",
        )

        self.assertEqual(targets, [])
        self.assertEqual(
            [item.code for item in diagnostics],
            ["MARKDOWN_LINK_INVALID"],
        )

    def test_malformed_local_reference_definition_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            temp_root = Path(temporary)
            package = create_package(temp_root)
            write_text(
                package / "skills" / "consumer" / "SKILL.md",
                "---\nname: consumer\ndescription: fixture\n---\n\n"
                "# Fixture\n\n## Consumer\n\n"
                "[broken]: <references/broken.md>garbage\n"
                "Use [broken].\n",
            )
            mapping = temp_root / "rule-mapping.yaml"
            write_mapping(
                mapping,
                source="plugin/ask-then-do-it/skills/consumer/SKILL.md",
                section="Consumer",
            )
            result = run_validator(
                adapter_root=temp_root,
                source_package=package,
                rule_mapping=mapping,
            )

        self.assertEqual(result.returncode, 2)
        self.assertIn("invalid local markdown link", result.stderr.lower())

    def test_multiline_reference_and_encoded_malformed_target_fail_closed(self) -> None:
        cases = (
            (
                "[shared]:\n  references/missing.md\nRead [contract][shared].\n",
                "missing reference",
            ),
            (
                "Read [contract](<references/missing%2Emd>garbage).\n",
                "invalid local markdown link",
            ),
        )
        for markdown, expected_error in cases:
            with self.subTest(markdown=markdown):
                with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
                    temp_root = Path(temporary)
                    package = create_package(temp_root)
                    write_text(
                        package / "skills" / "consumer" / "SKILL.md",
                        "---\nname: consumer\ndescription: fixture\n---\n\n"
                        "# Fixture\n\n## Consumer\n\n"
                        f"{markdown}",
                    )
                    mapping = temp_root / "rule-mapping.yaml"
                    write_mapping(
                        mapping,
                        source="plugin/ask-then-do-it/skills/consumer/SKILL.md",
                        section="Consumer",
                    )
                    result = run_validator(
                        adapter_root=temp_root,
                        source_package=package,
                        rule_mapping=mapping,
                    )

                self.assertEqual(result.returncode, 2, result.stderr)
                self.assertIn(expected_error, result.stderr.lower())

    def test_markdown_file_paths_reject_trailing_and_encoded_separators(self) -> None:
        cases = (
            ("references/contract.md/", "REFERENCE_PATH_ESCAPE"),
            ("references/contract.md%2F", "REFERENCE_PATH_ESCAPE"),
            ("references%2Fcontract.md", "REFERENCE_PATH_ESCAPE"),
            ("references%5Ccontract.md", "REFERENCE_PATH_ESCAPE"),
            ("references//contract.md", "REFERENCE_PATH_ESCAPE"),
        )
        syntaxes = (
            "Read [contract]({destination}).\n",
            "Read [contract][shared].\n\n[shared]: {destination}\n",
        )
        for destination, expected_code in cases:
            for syntax in syntaxes:
                with self.subTest(destination=destination, syntax=syntax):
                    with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
                        temp_root = Path(temporary)
                        package = create_package(temp_root)
                        write_text(
                            package / "skills" / "consumer" / "SKILL.md",
                            "---\nname: consumer\ndescription: fixture\n---\n\n"
                            "# Fixture\n\n## Consumer\n\n"
                            f"{syntax.format(destination=destination)}",
                        )
                        mapping = temp_root / "rule-mapping.yaml"
                        write_mapping(
                            mapping,
                            source="plugin/ask-then-do-it/skills/consumer/SKILL.md",
                            section="Consumer",
                        )
                        result = run_validator(
                            adapter_root=temp_root,
                            source_package=package,
                            rule_mapping=mapping,
                        )

                    self.assertEqual(result.returncode, 2, result.stderr)
                    self.assertIn(expected_code, result.stderr)
                    self.assertNotIn("Traceback", result.stderr)

    def test_encoded_separators_in_query_and_fragment_do_not_change_local_path(self) -> None:
        destinations = (
            "references/contract.md#heading%2Fpart",
            "references/contract.md?redirect=%2F",
            "references/contract.md#heading%5Cpart",
            "references/contract.md?redirect=%5C",
        )
        syntaxes = (
            "Read [contract]({destination}).\n",
            "Read [contract][shared].\n\n[shared]: {destination}\n",
        )
        for destination in destinations:
            for syntax in syntaxes:
                with self.subTest(destination=destination, syntax=syntax):
                    with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
                        temp_root = Path(temporary)
                        package = create_package(temp_root)
                        write_text(
                            package / "skills" / "consumer" / "SKILL.md",
                            "---\nname: consumer\ndescription: fixture\n---\n\n"
                            "# Fixture\n\n## Consumer\n\n"
                            f"{syntax.format(destination=destination)}",
                        )
                        mapping = temp_root / "rule-mapping.yaml"
                        write_mapping(
                            mapping,
                            source="plugin/ask-then-do-it/skills/consumer/SKILL.md",
                            section="Consumer",
                        )
                        result = run_validator(
                            adapter_root=temp_root,
                            source_package=package,
                            rule_mapping=mapping,
                        )

                    self.assertEqual(result.returncode, 0, result.stderr)

    def test_percent_encoded_nul_fails_closed_without_traceback(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            temp_root = Path(temporary)
            package = create_package(temp_root, link="references/%00.md")
            mapping = temp_root / "rule-mapping.yaml"
            write_mapping(
                mapping,
                source="plugin/ask-then-do-it/skills/consumer/SKILL.md",
                section="Consumer",
            )
            result = run_validator(
                adapter_root=temp_root,
                source_package=package,
                rule_mapping=mapping,
            )

        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertIn("REFERENCE_PATH_INVALID", result.stderr)
        self.assertIn("control character", result.stderr.lower())
        self.assertNotIn("Traceback", result.stderr)

    def test_malformed_markdown_authority_fails_closed_without_traceback(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            temp_root = Path(temporary)
            package = create_package(temp_root, link="//[invalid.md")
            mapping = temp_root / "rule-mapping.yaml"
            write_mapping(
                mapping,
                source="plugin/ask-then-do-it/skills/consumer/SKILL.md",
                section="Consumer",
            )
            result = run_validator(
                adapter_root=temp_root,
                source_package=package,
                rule_mapping=mapping,
            )

        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertIn("MARKDOWN_LINK_INVALID", result.stderr)
        self.assertNotIn("Traceback", result.stderr)

    def test_windows_drive_relative_markdown_target_fails_closed(self) -> None:
        for target in ("C:references/contract.md", "C%3Areferences/contract.md"):
            with self.subTest(target=target):
                with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
                    temp_root = Path(temporary)
                    package = create_package(temp_root, link=target)
                    mapping = temp_root / "rule-mapping.yaml"
                    write_mapping(
                        mapping,
                        source="plugin/ask-then-do-it/skills/consumer/SKILL.md",
                        section="Consumer",
                    )
                    result = run_validator(
                        adapter_root=temp_root,
                        source_package=package,
                        rule_mapping=mapping,
                    )

                self.assertEqual(result.returncode, 2, result.stderr)
                self.assertIn("REFERENCE_PATH_ESCAPE", result.stderr)
                self.assertNotIn("Traceback", result.stderr)

    def test_local_file_uri_and_unc_markdown_dependencies_fail_closed(self) -> None:
        destinations = (
            "file:///C:/outside.md",
            "file://server/share/outside.md",
            "//server/share/outside.md",
            "file&#58;&#47;&#47;&#47;C&#58;/outside&#46;md",
            "&#47;&#47;server/share/outside&#46;md",
            "file:%2F%2F%2FC%3A/outside%2Emd",
            "file%3A%2F%2F%2FC%3A/outside%2Emd",
            "%2F%2Fserver/share/outside%2Emd",
        )
        syntaxes = (
            "Read [outside]({destination}).\n",
            "Read [outside][dependency].\n\n[dependency]: {destination}\n",
        )
        for destination in destinations:
            for syntax in syntaxes:
                markdown = syntax.format(destination=destination)
                with self.subTest(destination=destination, syntax=syntax):
                    with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
                        temp_root = Path(temporary)
                        package = create_package(temp_root)
                        write_text(
                            package / "skills" / "consumer" / "SKILL.md",
                            "---\nname: consumer\ndescription: fixture\n---\n\n"
                            "# Fixture\n\n## Consumer\n\n"
                            f"{markdown}",
                        )
                        mapping = temp_root / "rule-mapping.yaml"
                        write_mapping(
                            mapping,
                            source="plugin/ask-then-do-it/skills/consumer/SKILL.md",
                            section="Consumer",
                        )
                        result = run_validator(
                            adapter_root=temp_root,
                            source_package=package,
                            rule_mapping=mapping,
                        )

                    self.assertEqual(result.returncode, 2, result.stderr)
                    self.assertIn("REFERENCE_PATH_ESCAPE", result.stderr)
                    self.assertNotIn("Traceback", result.stderr)

    def test_malformed_file_uri_dependencies_fail_closed(self) -> None:
        markdown_cases = (
            "Read [outside](<file:///C:/outside.md>garbage).\n",
            "Read [outside][dependency].\n\n"
            "[dependency]: <file:///C:/outside.md>garbage\n",
        )
        for markdown in markdown_cases:
            with self.subTest(markdown=markdown):
                with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
                    temp_root = Path(temporary)
                    package = create_package(temp_root)
                    write_text(
                        package / "skills" / "consumer" / "SKILL.md",
                        "---\nname: consumer\ndescription: fixture\n---\n\n"
                        "# Fixture\n\n## Consumer\n\n"
                        f"{markdown}",
                    )
                    mapping = temp_root / "rule-mapping.yaml"
                    write_mapping(
                        mapping,
                        source="plugin/ask-then-do-it/skills/consumer/SKILL.md",
                        section="Consumer",
                    )
                    result = run_validator(
                        adapter_root=temp_root,
                        source_package=package,
                        rule_mapping=mapping,
                    )

                self.assertEqual(result.returncode, 2, result.stderr)
                self.assertIn("MARKDOWN_LINK_INVALID", result.stderr)
                self.assertNotIn("Traceback", result.stderr)

    def test_https_markdown_dependencies_remain_external(self) -> None:
        destinations = (
            "https://example.test/outside.md",
            "https&#58;//example.test/outside&#46;md",
            "https://example.test/outside%2Emd",
        )
        syntaxes = (
            "Read [external]({destination}).\n",
            "Read [external][dependency].\n\n[dependency]: {destination}\n",
        )
        for destination in destinations:
            for syntax in syntaxes:
                markdown = syntax.format(destination=destination)
                with self.subTest(destination=destination, syntax=syntax):
                    with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
                        temp_root = Path(temporary)
                        package = create_package(temp_root)
                        write_text(
                            package / "skills" / "consumer" / "SKILL.md",
                            "---\nname: consumer\ndescription: fixture\n---\n\n"
                            "# Fixture\n\n## Consumer\n\n"
                            f"{markdown}",
                        )
                        mapping = temp_root / "rule-mapping.yaml"
                        write_mapping(
                            mapping,
                            source="plugin/ask-then-do-it/skills/consumer/SKILL.md",
                            section="Consumer",
                        )
                        result = run_validator(
                            adapter_root=temp_root,
                            source_package=package,
                            rule_mapping=mapping,
                        )

                    self.assertEqual(result.returncode, 0, result.stderr)

    def test_multiline_reference_and_malformed_external_boundaries(self) -> None:
        module_root = str(ROOT / "scripts")
        if module_root not in sys.path:
            sys.path.insert(0, module_root)
        import validate_codex_contract as contract

        cases = (
            (
                "[shared]:\n  references/contract.md\nRead [contract][shared].\n",
                ["references/contract.md"],
                [],
            ),
            (
                "[shared]:\n\n  references/missing.md\nRead [contract][shared].\n",
                [],
                [],
            ),
            (
                "[shared]:\n  <references/missing.md>garbage\n"
                "Read [contract][shared].\n",
                [],
                ["MARKDOWN_LINK_INVALID"],
            ),
            (
                "Read [external](<https://example.test/missing%2Emd>garbage).\n",
                [],
                [],
            ),
        )
        for markdown, expected_targets, expected_codes in cases:
            with self.subTest(markdown=markdown):
                diagnostics: list[contract.Diagnostic] = []
                targets = contract.local_markdown_targets(
                    markdown,
                    diagnostics,
                    "fixture.md",
                )
                self.assertEqual(targets, expected_targets)
                self.assertEqual(
                    [item.code for item in diagnostics],
                    expected_codes,
                )

    def test_duplicate_reference_definitions_use_first_destination(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            temp_root = Path(temporary)
            package = create_package(temp_root)
            write_text(
                package / "skills" / "consumer" / "SKILL.md",
                "---\nname: consumer\ndescription: fixture\n---\n\n"
                "# Fixture\n\n## Consumer\n\n"
                "Read [contract][shared].\n\n"
                "[shared]: references/missing.md\n"
                "[shared]: https://example.test/safe.md\n",
            )
            mapping = temp_root / "rule-mapping.yaml"
            write_mapping(
                mapping,
                source="plugin/ask-then-do-it/skills/consumer/SKILL.md",
                section="Consumer",
            )
            result = run_validator(
                adapter_root=temp_root,
                source_package=package,
                rule_mapping=mapping,
            )

        self.assertEqual(result.returncode, 2)
        self.assertIn("missing reference", result.stderr.lower())

    def test_malformed_local_markdown_link_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            temp_root = Path(temporary)
            package = create_package(temp_root)
            write_text(
                package / "skills" / "consumer" / "SKILL.md",
                "---\nname: consumer\ndescription: fixture\n---\n\n"
                "# Fixture\n\n## Consumer\n\n"
                "Read [contract](references/missing.md before acting.\n",
            )
            mapping = temp_root / "rule-mapping.yaml"
            write_mapping(
                mapping,
                source="plugin/ask-then-do-it/skills/consumer/SKILL.md",
                section="Consumer",
            )
            result = run_validator(
                adapter_root=temp_root,
                source_package=package,
                rule_mapping=mapping,
            )

        self.assertEqual(result.returncode, 2)
        self.assertIn("invalid local markdown link", result.stderr.lower())

    def test_external_image_and_fragment_links_are_not_runtime_references(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            temp_root = Path(temporary)
            package = create_package(temp_root)
            write_text(
                package / "skills" / "consumer" / "SKILL.md",
                "---\nname: consumer\ndescription: fixture\n---\n\n"
                "# Fixture\n\n## Consumer\n\n"
                "![image](references/missing.md)\n\n"
                "Read [external](https://example.test/missing.md) or "
                "[section](#consumer).\n",
            )
            mapping = temp_root / "rule-mapping.yaml"
            write_mapping(
                mapping,
                source="plugin/ask-then-do-it/skills/consumer/SKILL.md",
                section="Consumer",
            )
            result = run_validator(
                adapter_root=temp_root,
                source_package=package,
                rule_mapping=mapping,
            )

        self.assertEqual(result.returncode, 0, result.stderr)

    def test_nested_link_syntax_in_image_alt_is_not_a_runtime_reference(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            temp_root = Path(temporary)
            package = create_package(temp_root)
            write_text(
                package / "skills" / "consumer" / "SKILL.md",
                "---\nname: consumer\ndescription: fixture\n---\n\n"
                "# Fixture\n\n## Consumer\n\n"
                "![image [label](references/missing.md)](asset.png)\n",
            )
            mapping = temp_root / "rule-mapping.yaml"
            write_mapping(
                mapping,
                source="plugin/ask-then-do-it/skills/consumer/SKILL.md",
                section="Consumer",
            )
            result = run_validator(
                adapter_root=temp_root,
                source_package=package,
                rule_mapping=mapping,
            )

        self.assertEqual(result.returncode, 0, result.stderr)

    def test_reference_path_escape_fails_closed_but_internal_parent_path_is_allowed(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            temp_root = Path(temporary)
            package = create_package(temp_root, link="../other/references/shared.md")
            write_text(
                package / "skills" / "other" / "references" / "shared.md",
                "# Shared\n",
            )
            mapping = temp_root / "rule-mapping.yaml"
            write_mapping(
                mapping,
                source="plugin/ask-then-do-it/skills/consumer/SKILL.md",
                section="Consumer",
            )
            allowed = run_validator(
                adapter_root=temp_root,
                source_package=package,
                rule_mapping=mapping,
            )
            write_text(
                package / "skills" / "consumer" / "SKILL.md",
                "---\nname: consumer\ndescription: fixture\n---\n\n"
                "# Fixture\n\n## Consumer\n\n"
                "Read [outside](../../../../outside/references/secret.md).\n",
            )
            escaped = run_validator(
                adapter_root=temp_root,
                source_package=package,
                rule_mapping=mapping,
            )

        self.assertEqual(allowed.returncode, 0, allowed.stderr)
        self.assertEqual(escaped.returncode, 2)
        self.assertIn("escapes package", escaped.stderr.lower())

    def test_internal_symlink_component_fails_closed(self) -> None:
        module_root = str(ROOT / "scripts")
        if module_root not in sys.path:
            sys.path.insert(0, module_root)
        import validate_codex_contract as contract

        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            package = create_package(Path(temporary))
            source = package / "skills" / "consumer" / "SKILL.md"
            diagnostics: list[contract.Diagnostic] = []
            with mock.patch.object(contract, "has_link_component", return_value=True):
                resolved = contract.resolve_reference(
                    source,
                    "references/contract.md",
                    package,
                    diagnostics,
                )

        self.assertIsNone(resolved)
        self.assertEqual([item.code for item in diagnostics], ["REFERENCE_SYMLINK_ESCAPE"])

    def test_second_hop_reference_and_cycle_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            temp_root = Path(temporary)
            package = create_package(temp_root)
            reference = package / "skills" / "consumer" / "references" / "contract.md"
            write_text(reference, "# Contract\n\nRead [next](next.md).\n")
            write_text(reference.parent / "next.md", "# Next\n")
            mapping = temp_root / "rule-mapping.yaml"
            write_mapping(
                mapping,
                source="plugin/ask-then-do-it/skills/consumer/SKILL.md",
                section="Consumer",
            )
            second_hop = run_validator(
                adapter_root=temp_root,
                source_package=package,
                rule_mapping=mapping,
            )

            write_text(
                reference.parent / "next.md",
                "# Next\n\nRead [contract](contract.md).\n",
            )
            cycle = run_validator(
                adapter_root=temp_root,
                source_package=package,
                rule_mapping=mapping,
            )

        self.assertEqual(second_hop.returncode, 2)
        self.assertIn("second-hop", second_hop.stderr.lower())
        self.assertEqual(cycle.returncode, 2)
        self.assertIn("reference cycle", cycle.stderr.lower())

    def test_missing_mapping_section_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            temp_root = Path(temporary)
            package = create_package(temp_root)
            mapping = temp_root / "rule-mapping.yaml"
            write_mapping(
                mapping,
                source="plugin/ask-then-do-it/skills/consumer/SKILL.md",
                section="Missing section",
            )
            result = run_validator(
                adapter_root=temp_root,
                source_package=package,
                rule_mapping=mapping,
            )

        self.assertEqual(result.returncode, 2)
        self.assertIn("missing markdown section", result.stderr.lower())

    def test_mapping_headings_follow_comment_and_atx_boundaries(self) -> None:
        cases = (
            (
                "# Fixture\n\n<!--\n## Consumer\n-->\n",
                "Consumer",
                2,
            ),
            (
                "# Fixture\n\n   ## Consumer\n",
                "Consumer",
                0,
            ),
            (
                "# Fixture\n\n## Contract#\n",
                "Contract",
                2,
            ),
        )
        for markdown, section_name, expected_code in cases:
            with self.subTest(markdown=markdown, section=section_name):
                with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
                    temp_root = Path(temporary)
                    package = create_package(temp_root)
                    write_text(
                        package / "skills" / "consumer" / "SKILL.md",
                        "---\nname: consumer\ndescription: fixture\n---\n\n"
                        f"{markdown}",
                    )
                    mapping = temp_root / "rule-mapping.yaml"
                    write_mapping(
                        mapping,
                        source="plugin/ask-then-do-it/skills/consumer/SKILL.md",
                        section=section_name,
                    )
                    result = run_validator(
                        adapter_root=temp_root,
                        source_package=package,
                        rule_mapping=mapping,
                    )

                self.assertEqual(result.returncode, expected_code, result.stderr)
                if expected_code:
                    self.assertIn("missing markdown section", result.stderr.lower())

    def test_unreachable_runtime_mapping_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            temp_root = Path(temporary)
            package = create_package(temp_root)
            write_text(
                package / "skills" / "consumer" / "references" / "orphan.md",
                "# Orphan\n\n## Orphan\n",
            )
            mapping = temp_root / "rule-mapping.yaml"
            write_mapping(
                mapping,
                source="plugin/ask-then-do-it/skills/consumer/references/orphan.md",
                section="Orphan",
            )
            result = run_validator(
                adapter_root=temp_root,
                source_package=package,
                rule_mapping=mapping,
            )

        self.assertEqual(result.returncode, 2)
        self.assertIn("unreachable runtime mapping", result.stderr.lower())

    def test_package_omission_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            temp_root = Path(temporary)
            source = create_package(temp_root)
            package = temp_root / "built-package"
            write_text(
                package / "skills" / "consumer" / "SKILL.md",
                (source / "skills" / "consumer" / "SKILL.md").read_text(
                    encoding="utf-8"
                ),
            )
            mapping = temp_root / "rule-mapping.yaml"
            write_mapping(
                mapping,
                source="plugin/ask-then-do-it/skills/consumer/SKILL.md",
                section="Consumer",
            )
            result = run_validator(
                adapter_root=temp_root,
                source_package=source,
                package_root=package,
                rule_mapping=mapping,
            )

        self.assertEqual(result.returncode, 2)
        self.assertIn("package omission", result.stderr.lower())

    def test_package_only_skill_link_mutation_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            temp_root = Path(temporary)
            source = create_package(temp_root)
            package = temp_root / "built-package"
            shutil.copytree(source, package)
            write_text(
                package / "skills" / "consumer" / "SKILL.md",
                "---\nname: consumer\ndescription: fixture\n---\n\n"
                "# Fixture\n\n## Consumer\n\n"
                "Read [contract](references/missing.md).\n",
            )
            mapping = temp_root / "rule-mapping.yaml"
            write_mapping(
                mapping,
                source="plugin/ask-then-do-it/skills/consumer/SKILL.md",
                section="Consumer",
            )
            result = run_validator(
                adapter_root=temp_root,
                source_package=source,
                package_root=package,
                rule_mapping=mapping,
            )

        self.assertEqual(result.returncode, 2)
        self.assertIn("package runtime content differs", result.stderr.lower())

    def test_package_only_reference_second_hop_mutation_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            temp_root = Path(temporary)
            source = create_package(temp_root)
            package = temp_root / "built-package"
            shutil.copytree(source, package)
            write_text(
                package / "skills" / "consumer" / "references" / "contract.md",
                "# Contract\n\nRead [next](missing.md).\n",
            )
            mapping = temp_root / "rule-mapping.yaml"
            write_mapping(
                mapping,
                source="plugin/ask-then-do-it/skills/consumer/SKILL.md",
                section="Consumer",
            )
            result = run_validator(
                adapter_root=temp_root,
                source_package=source,
                package_root=package,
                rule_mapping=mapping,
            )

        self.assertEqual(result.returncode, 2)
        self.assertIn("package runtime content differs", result.stderr.lower())

    def test_package_intermediate_link_and_linked_root_fail_closed(self) -> None:
        module_root = str(ROOT / "scripts")
        if module_root not in sys.path:
            sys.path.insert(0, module_root)
        import validate_codex_contract as contract

        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            temp_root = Path(temporary)
            source = create_package(temp_root)
            package = temp_root / "built-package"
            shutil.copytree(source, package)
            linked_parent = package / "skills" / "consumer" / "references"

            original_is_link = contract.is_link

            def intermediate_link(path: Path) -> bool:
                return Path(path) == linked_parent or original_is_link(Path(path))

            with mock.patch.object(contract, "is_link", side_effect=intermediate_link):
                _, intermediate_diagnostics = contract.validate_reference_graph(
                    source,
                    package,
                )
            with mock.patch.object(
                contract,
                "is_link",
                side_effect=lambda path: Path(path) == package
                or original_is_link(Path(path)),
            ):
                _, root_diagnostics = contract.validate_reference_graph(source, package)
            with mock.patch.object(
                contract,
                "is_link",
                side_effect=lambda path: Path(path) == source
                or original_is_link(Path(path)),
            ):
                _, source_root_diagnostics = contract.validate_reference_graph(
                    source,
                    package,
                )

        self.assertIn("PACKAGE_PATH_LINK", {item.code for item in intermediate_diagnostics})
        self.assertIn("PACKAGE_ROOT_LINK", {item.code for item in root_diagnostics})
        self.assertIn(
            "SOURCE_ROOT_LINK",
            {item.code for item in source_root_diagnostics},
        )

    def test_real_package_intermediate_symlink_fails_closed_when_supported(self) -> None:
        module_root = str(ROOT / "scripts")
        if module_root not in sys.path:
            sys.path.insert(0, module_root)
        import validate_codex_contract as contract

        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            temp_root = Path(temporary)
            source = create_package(temp_root)
            package = temp_root / "built-package"
            skill_target = package / "skills" / "consumer" / "SKILL.md"
            write_text(
                skill_target,
                (source / "skills" / "consumer" / "SKILL.md").read_text(
                    encoding="utf-8"
                ),
            )
            external = temp_root / "external-references"
            write_text(external / "contract.md", "# External\n")
            link = skill_target.parent / "references"
            try:
                os.symlink(external, link, target_is_directory=True)
            except OSError as exc:
                self.skipTest(f"directory symlink unavailable: {exc}")

            _, diagnostics = contract.validate_reference_graph(source, package)

        self.assertIn("PACKAGE_PATH_LINK", {item.code for item in diagnostics})

    def test_unreadable_package_reference_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            temp_root = Path(temporary)
            source = create_package(temp_root)
            package = temp_root / "built-package"
            skill_target = package / "skills" / "consumer" / "SKILL.md"
            write_text(
                skill_target,
                (source / "skills" / "consumer" / "SKILL.md").read_text(
                    encoding="utf-8"
                ),
            )
            invalid_target = (
                package
                / "skills"
                / "consumer"
                / "references"
                / "contract.md"
            )
            invalid_target.parent.mkdir(parents=True, exist_ok=True)
            invalid_target.write_bytes(b"\xff")
            mapping = temp_root / "rule-mapping.yaml"
            write_mapping(
                mapping,
                source="plugin/ask-then-do-it/skills/consumer/SKILL.md",
                section="Consumer",
            )
            result = run_validator(
                adapter_root=temp_root,
                source_package=source,
                package_root=package,
                rule_mapping=mapping,
            )

        self.assertEqual(result.returncode, 2)
        self.assertIn("package target is not readable utf-8", result.stderr.lower())

    def test_mapping_and_measurement_link_boundaries_fail_closed(self) -> None:
        module_root = str(ROOT / "scripts")
        if module_root not in sys.path:
            sys.path.insert(0, module_root)
        import validate_codex_contract as contract

        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            temp_root = Path(temporary)
            package = create_package(temp_root)
            mapping = temp_root / "rule-mapping.yaml"
            write_mapping(
                mapping,
                source="plugin/ask-then-do-it/skills/consumer/SKILL.md",
                section="Consumer",
            )
            linked_parent = package / "skills" / "consumer"
            built_package = temp_root / "built-package"
            shutil.copytree(package, built_package)
            linked_package_parent = built_package / "skills" / "consumer"
            original_is_link = contract.is_link

            with mock.patch.object(
                contract,
                "is_link",
                side_effect=lambda path: Path(path) == linked_parent
                or original_is_link(Path(path)),
            ):
                _, mapping_diagnostics = contract.validate_rule_mapping(
                    temp_root,
                    package,
                    package,
                    mapping,
                    {"skills/consumer/SKILL.md", "skills/consumer/references/contract.md"},
                )
                with self.assertRaises(contract.CodexContractError) as measurement_error:
                    contract.measure_load_set(
                        package,
                        ("skills/consumer/SKILL.md",),
                    )

            with mock.patch.object(
                contract,
                "is_link",
                side_effect=lambda path: Path(path) == linked_package_parent
                or original_is_link(Path(path)),
            ):
                _, package_mapping_diagnostics = contract.validate_rule_mapping(
                    temp_root,
                    package,
                    built_package,
                    mapping,
                    {"skills/consumer/SKILL.md", "skills/consumer/references/contract.md"},
                )

            with mock.patch.object(
                contract,
                "is_link",
                side_effect=lambda path: Path(path) == package
                or original_is_link(Path(path)),
            ):
                with self.assertRaises(contract.CodexContractError) as root_error:
                    contract.measure_load_set(
                        package,
                        ("skills/consumer/SKILL.md",),
                    )

        self.assertIn("MAPPING_SOURCE_LINK", {item.code for item in mapping_diagnostics})
        self.assertIn(
            "PACKAGE_PATH_LINK",
            {item.code for item in package_mapping_diagnostics},
        )
        self.assertIn(
            "MEASUREMENT_PATH_LINK",
            {item.code for item in measurement_error.exception.diagnostics},
        )
        self.assertIn(
            "MEASUREMENT_ROOT_LINK",
            {item.code for item in root_error.exception.diagnostics},
        )

    def test_link_boundaries_are_rejected_before_directory_enumeration(self) -> None:
        module_root = str(ROOT / "scripts")
        if module_root not in sys.path:
            sys.path.insert(0, module_root)
        import validate_codex_contract as contract

        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            temp_root = Path(temporary)
            package = create_package(temp_root)
            mapping = temp_root / "rule-mapping.yaml"
            write_mapping(
                mapping,
                source="plugin/ask-then-do-it/skills/consumer/SKILL.md",
                section="Consumer",
            )
            built_package = temp_root / "built-package"
            shutil.copytree(package, built_package)

            source = package / "skills" / "consumer" / "SKILL.md"
            reference_target = (
                package / "skills" / "consumer" / "references" / "contract.md"
            )
            package_target = (
                built_package
                / "skills"
                / "consumer"
                / "references"
                / "contract.md"
            )
            mapping_target = package / "skills" / "consumer" / "SKILL.md"
            measurement_target = mapping_target
            original_is_link = contract.is_link
            original_iterdir = Path.iterdir

            def call_with_mocked_link(linked_path: Path, callback):
                iterated: list[Path] = []

                def record_iterdir(path: Path):
                    iterated.append(Path(path))
                    return original_iterdir(path)

                try:
                    with mock.patch.object(
                        contract,
                        "is_link",
                        side_effect=lambda path: Path(path) == linked_path
                        or original_is_link(Path(path)),
                    ), mock.patch.object(Path, "iterdir", new=record_iterdir):
                        return callback()
                finally:
                    self.assertEqual(
                        iterated,
                        [],
                        f"enumerated directory before rejecting linked path: {linked_path}",
                    )

            reference_diagnostics: list[contract.Diagnostic] = []
            resolved_reference = call_with_mocked_link(
                reference_target,
                lambda: contract.resolve_reference(
                    source,
                    "references/contract.md",
                    package,
                    reference_diagnostics,
                ),
            )
            self.assertIsNone(resolved_reference)
            self.assertEqual(
                [item.code for item in reference_diagnostics],
                ["REFERENCE_SYMLINK_ESCAPE"],
            )

            package_diagnostics: list[contract.Diagnostic] = []
            resolved_package = call_with_mocked_link(
                package_target,
                lambda: contract.validate_package_file(
                    built_package,
                    "skills/consumer/references/contract.md",
                    package_diagnostics,
                    missing_code="PACKAGE_TARGET_MISSING",
                    missing_detail="package target is missing",
                ),
            )
            self.assertIsNone(resolved_package)
            self.assertEqual(
                [item.code for item in package_diagnostics],
                ["PACKAGE_PATH_LINK"],
            )

            _, mapping_diagnostics = call_with_mocked_link(
                mapping_target,
                lambda: contract.validate_rule_mapping(
                    temp_root,
                    package,
                    package,
                    mapping,
                    {
                        "skills/consumer/SKILL.md",
                        "skills/consumer/references/contract.md",
                    },
                ),
            )
            self.assertIn(
                "MAPPING_SOURCE_LINK",
                {item.code for item in mapping_diagnostics},
            )

            with self.assertRaises(contract.CodexContractError) as measurement_error:
                call_with_mocked_link(
                    measurement_target,
                    lambda: contract.resolve_measurement_path(
                        package,
                        "skills/consumer/SKILL.md",
                    ),
                )
            self.assertIn(
                "MEASUREMENT_PATH_LINK",
                {item.code for item in measurement_error.exception.diagnostics},
            )

    def test_case_verification_io_errors_fail_closed_for_all_consumers(self) -> None:
        module_root = str(ROOT / "scripts")
        if module_root not in sys.path:
            sys.path.insert(0, module_root)
        import validate_codex_contract as contract

        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            temp_root = Path(temporary)
            package = create_package(temp_root)
            mapping = temp_root / "rule-mapping.yaml"
            write_mapping(
                mapping,
                source="plugin/ask-then-do-it/skills/consumer/SKILL.md",
                section="Consumer",
            )
            built_package = temp_root / "built-package"
            shutil.copytree(package, built_package)
            source = package / "skills" / "consumer" / "SKILL.md"

            reference_diagnostics: list[contract.Diagnostic] = []
            with mock.patch.object(
                Path,
                "iterdir",
                side_effect=PermissionError("denied"),
            ):
                resolved_reference = contract.resolve_reference(
                    source,
                    "references/contract.md",
                    package,
                    reference_diagnostics,
                )
            self.assertIsNone(resolved_reference)
            self.assertEqual(
                [item.code for item in reference_diagnostics],
                ["REFERENCE_CASE_UNVERIFIABLE"],
            )

            package_diagnostics: list[contract.Diagnostic] = []
            with mock.patch.object(
                Path,
                "iterdir",
                side_effect=PermissionError("denied"),
            ):
                resolved_package = contract.validate_package_file(
                    built_package,
                    "skills/consumer/references/contract.md",
                    package_diagnostics,
                    missing_code="PACKAGE_TARGET_MISSING",
                    missing_detail="package target is missing",
                )
            self.assertIsNone(resolved_package)
            self.assertEqual(
                [item.code for item in package_diagnostics],
                ["PACKAGE_PATH_CASE_UNVERIFIABLE"],
            )

            with mock.patch.object(
                Path,
                "iterdir",
                side_effect=PermissionError("denied"),
            ):
                _, mapping_diagnostics = contract.validate_rule_mapping(
                    temp_root,
                    package,
                    package,
                    mapping,
                    {
                        "skills/consumer/SKILL.md",
                        "skills/consumer/references/contract.md",
                    },
                )
            self.assertIn(
                "MAPPING_SOURCE_CASE_UNVERIFIABLE",
                {item.code for item in mapping_diagnostics},
            )

            with mock.patch.object(
                Path,
                "iterdir",
                side_effect=PermissionError("denied"),
            ), self.assertRaises(contract.CodexContractError) as measurement_error:
                contract.resolve_measurement_path(
                    package,
                    "skills/consumer/SKILL.md",
                )
            self.assertIn(
                "MEASUREMENT_INPUT_CASE_UNVERIFIABLE",
                {item.code for item in measurement_error.exception.diagnostics},
            )

    def test_case_verification_io_error_is_a_controlled_cli_failure(self) -> None:
        module_root = str(ROOT / "scripts")
        if module_root not in sys.path:
            sys.path.insert(0, module_root)
        import validate_codex_contract as contract

        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            temp_root = Path(temporary)
            package = create_package(temp_root)
            mapping = temp_root / "rule-mapping.yaml"
            write_mapping(
                mapping,
                source="plugin/ask-then-do-it/skills/consumer/SKILL.md",
                section="Consumer",
            )
            core_catalog = temp_root / "core-rules.yaml"
            write_text(
                core_catalog,
                "core_version: 1.4.1\n"
                "rules:\n"
                "  - id: TEST-RULE-001\n"
                "    mandatory: true\n",
            )
            conformance = temp_root / "conformance.yaml"
            write_text(
                conformance,
                "core_version: 1.4.1\n"
                "implemented_rules:\n"
                "  - TEST-RULE-001\n",
            )
            arguments = [
                str(SCRIPT),
                "--adapter-root",
                str(temp_root),
                "--source-package-root",
                str(package),
                "--package-root",
                str(package),
                "--rule-mapping",
                str(mapping),
                "--core-catalog",
                str(core_catalog),
                "--conformance",
                str(conformance),
                "--validate-only",
            ]
            stderr = io.StringIO()
            with mock.patch.object(sys, "argv", arguments), mock.patch.object(
                contract,
                "first_case_mismatch",
                side_effect=PermissionError("denied"),
            ), mock.patch("sys.stderr", stderr):
                exit_code = contract.main()

        self.assertEqual(exit_code, 2, stderr.getvalue())
        self.assertIn("CASE_UNVERIFIABLE", stderr.getvalue())
        self.assertNotIn("Traceback", stderr.getvalue())

    def test_public_skill_discovery_io_error_fails_closed(self) -> None:
        module_root = str(ROOT / "scripts")
        if module_root not in sys.path:
            sys.path.insert(0, module_root)
        import validate_codex_contract as contract

        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            package = create_package(Path(temporary))
            skills_root = package / "skills"
            original_iterdir = Path.iterdir

            def guarded_iterdir(path: Path):
                if path == skills_root:
                    raise PermissionError("denied")
                return original_iterdir(path)

            diagnostics: list[contract.Diagnostic] = []
            with mock.patch.object(
                Path,
                "iterdir",
                autospec=True,
                side_effect=guarded_iterdir,
            ):
                skill_ids = contract.discover_public_skills(package, diagnostics)

        self.assertEqual(skill_ids, ())
        self.assertEqual(
            [item.code for item in diagnostics],
            ["SKILL_ROOT_UNREADABLE"],
        )

    def test_public_skill_discovery_io_error_is_a_controlled_cli_failure(self) -> None:
        module_root = str(ROOT / "scripts")
        if module_root not in sys.path:
            sys.path.insert(0, module_root)
        import validate_codex_contract as contract

        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            temp_root = Path(temporary)
            package = create_package(temp_root)
            mapping = temp_root / "rule-mapping.yaml"
            write_mapping(
                mapping,
                source="plugin/ask-then-do-it/skills/consumer/SKILL.md",
                section="Consumer",
            )
            core_catalog = temp_root / "core-rules.yaml"
            write_text(
                core_catalog,
                "core_version: 1.4.1\n"
                "rules:\n"
                "  - id: TEST-RULE-001\n"
                "    mandatory: true\n",
            )
            conformance = temp_root / "conformance.yaml"
            write_text(
                conformance,
                "core_version: 1.4.1\n"
                "implemented_rules:\n"
                "  - TEST-RULE-001\n",
            )
            arguments = [
                str(SCRIPT),
                "--adapter-root",
                str(temp_root),
                "--source-package-root",
                str(package),
                "--package-root",
                str(package),
                "--rule-mapping",
                str(mapping),
                "--core-catalog",
                str(core_catalog),
                "--conformance",
                str(conformance),
                "--validate-only",
            ]
            skills_root = package / "skills"
            original_iterdir = Path.iterdir

            def guarded_iterdir(path: Path):
                if path == skills_root:
                    raise PermissionError("denied")
                return original_iterdir(path)

            stderr = io.StringIO()
            with mock.patch.object(
                Path,
                "iterdir",
                autospec=True,
                side_effect=guarded_iterdir,
            ), mock.patch.object(sys, "argv", arguments), mock.patch(
                "sys.stderr", stderr
            ):
                exit_code = contract.main()

        self.assertEqual(exit_code, 2, stderr.getvalue())
        self.assertIn("SKILL_ROOT_UNREADABLE", stderr.getvalue())
        self.assertNotIn("Traceback", stderr.getvalue())

    def test_rule_mapping_source_path_and_section_exist_in_current_adapter(self) -> None:
        result = run_validator()

        self.assertEqual(result.returncode, 0, result.stderr)

    def test_rule_mapping_requires_matching_core_version(self) -> None:
        mapping_cases = (
            (
                "rules:\n"
                "  TEST-RULE-001:\n"
                "    - file: plugin/ask-then-do-it/skills/consumer/SKILL.md\n"
                "      section: Consumer\n"
                "      implementation: fixture mapping\n",
                "core_version is missing",
            ),
            (
                "core_version: wrong\n"
                "rules:\n"
                "  TEST-RULE-001:\n"
                "    - file: plugin/ask-then-do-it/skills/consumer/SKILL.md\n"
                "      section: Consumer\n"
                "      implementation: fixture mapping\n",
                "core_version does not match",
            ),
        )
        for mapping_text, expected_error in mapping_cases:
            with self.subTest(mapping=mapping_text):
                with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
                    temp_root = Path(temporary)
                    package = create_package(temp_root)
                    mapping = temp_root / "rule-mapping.yaml"
                    write_text(mapping, mapping_text)
                    result = run_validator(
                        adapter_root=temp_root,
                        source_package=package,
                        rule_mapping=mapping,
                    )

                self.assertEqual(result.returncode, 2, result.stderr)
                self.assertIn(expected_error, result.stderr.lower())

    def test_conformance_requires_matching_core_version(self) -> None:
        conformance_cases = (
            (
                "implemented_rules:\n  - TEST-RULE-001\n",
                "conformance core_version is missing",
            ),
            (
                "core_version: wrong\nimplemented_rules:\n  - TEST-RULE-001\n",
                "conformance core_version does not match",
            ),
        )
        for conformance_text, expected_error in conformance_cases:
            with self.subTest(conformance=conformance_text):
                with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
                    temp_root = Path(temporary)
                    package = create_package(temp_root)
                    mapping = temp_root / "rule-mapping.yaml"
                    write_mapping(
                        mapping,
                        source="plugin/ask-then-do-it/skills/consumer/SKILL.md",
                        section="Consumer",
                    )
                    conformance = temp_root / "conformance.yaml"
                    write_text(conformance, conformance_text)
                    result = run_validator(
                        adapter_root=temp_root,
                        source_package=package,
                        rule_mapping=mapping,
                        conformance=conformance,
                    )

                self.assertEqual(result.returncode, 2, result.stderr)
                self.assertIn(expected_error, result.stderr.lower())

    def test_rule_inventory_matches_core_and_conformance(self) -> None:
        mutation_cases = (
            (
                "mapping-missing",
                "core_version: 1.4.1\nrules:\n"
                "  OTHER-RULE-001:\n"
                "    - file: plugin/ask-then-do-it/skills/consumer/SKILL.md\n"
                "      section: Consumer\n"
                "      implementation: fixture mapping\n",
                None,
                "missing mandatory rule mapping",
            ),
            (
                "mapping-unknown",
                "core_version: 1.4.1\nrules:\n"
                "  TEST-RULE-001:\n"
                "    - file: plugin/ask-then-do-it/skills/consumer/SKILL.md\n"
                "      section: Consumer\n"
                "      implementation: fixture mapping\n"
                "  UNKNOWN-RULE-001:\n"
                "    - file: plugin/ask-then-do-it/skills/consumer/SKILL.md\n"
                "      section: Consumer\n"
                "      implementation: fixture mapping\n",
                None,
                "unknown rule mapping",
            ),
            (
                "conformance-missing",
                None,
                "core_version: 1.4.1\nimplemented_rules:\n  - OTHER-RULE-001\n",
                "missing mandatory conformance rule",
            ),
            (
                "conformance-unknown",
                None,
                "core_version: 1.4.1\nimplemented_rules:\n"
                "  - TEST-RULE-001\n  - UNKNOWN-RULE-001\n",
                "unknown conformance rule",
            ),
        )
        for name, mapping_text, conformance_text, expected_error in mutation_cases:
            with self.subTest(case=name):
                with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
                    temp_root = Path(temporary)
                    package = create_package(temp_root)
                    mapping = temp_root / "rule-mapping.yaml"
                    write_mapping(
                        mapping,
                        source="plugin/ask-then-do-it/skills/consumer/SKILL.md",
                        section="Consumer",
                    )
                    if mapping_text is not None:
                        write_text(mapping, mapping_text)
                    conformance = temp_root / "conformance.yaml"
                    if conformance_text is not None:
                        write_text(conformance, conformance_text)
                    result = run_validator(
                        adapter_root=temp_root,
                        source_package=package,
                        rule_mapping=mapping,
                        conformance=(
                            conformance if conformance_text is not None else None
                        ),
                    )

                self.assertEqual(result.returncode, 2, result.stderr)
                self.assertIn(expected_error, result.stderr.lower())

    def test_rule_mapping_rejects_trailing_top_level_syntax(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            temp_root = Path(temporary)
            package = create_package(temp_root)
            mapping = temp_root / "rule-mapping.yaml"
            write_mapping(
                mapping,
                source="plugin/ask-then-do-it/skills/consumer/SKILL.md",
                section="Consumer",
            )
            write_text(
                mapping,
                mapping.read_text(encoding="utf-8") + "unsupported: true\n",
            )
            result = run_validator(
                adapter_root=temp_root,
                source_package=package,
                rule_mapping=mapping,
            )

        self.assertEqual(result.returncode, 2)
        self.assertIn("unsupported rule-mapping syntax", result.stderr.lower())

    def test_rule_mapping_rejects_malformed_yaml_scalars(self) -> None:
        mapping_cases = (
            (
                "core_version: [\n"
                "rules:\n"
                "  TEST-RULE-001:\n"
                "    - file: plugin/ask-then-do-it/skills/consumer/SKILL.md\n"
                "      section: Consumer\n"
                "      implementation: fixture mapping\n",
                "core_version",
            ),
            (
                "core_version: 1.4.1\n"
                "rules:\n"
                "  TEST-RULE-001:\n"
                "    - file: plugin/ask-then-do-it/skills/consumer/SKILL.md\n"
                "      section: Consumer\n"
                "      implementation: [\n",
                "implementation",
            ),
        )
        for mapping_text, field in mapping_cases:
            with self.subTest(field=field):
                with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
                    temp_root = Path(temporary)
                    package = create_package(temp_root)
                    mapping = temp_root / "rule-mapping.yaml"
                    write_text(mapping, mapping_text)
                    result = run_validator(
                        adapter_root=temp_root,
                        source_package=package,
                        rule_mapping=mapping,
                    )

                self.assertEqual(result.returncode, 2, result.stderr)
                self.assertIn("invalid yaml scalar", result.stderr.lower())
                self.assertIn(field, result.stderr.lower())

    def test_windows_nonportable_paths_fail_closed(self) -> None:
        module_root = str(ROOT / "scripts")
        if module_root not in sys.path:
            sys.path.insert(0, module_root)
        import validate_codex_contract as contract

        cases = (
            "C:plugin/ask-then-do-it/skills/consumer/SKILL.md",
            "C:/plugin/ask-then-do-it/skills/consumer/SKILL.md",
            "//server/share/plugin/ask-then-do-it/skills/consumer/SKILL.md",
            r"\\server\share\plugin\ask-then-do-it\skills\consumer\SKILL.md",
            r"\\?\C:\plugin\ask-then-do-it\skills\consumer\SKILL.md",
            r"\\.\C:\plugin\ask-then-do-it\skills\consumer\SKILL.md",
        )
        for value in cases:
            with self.subTest(value=value):
                with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
                    temp_root = Path(temporary)
                    package = create_package(temp_root)
                    mapping = temp_root / "rule-mapping.yaml"
                    write_mapping(mapping, source=value, section="Consumer")
                    result = run_validator(
                        adapter_root=temp_root,
                        source_package=package,
                        rule_mapping=mapping,
                    )

                    with self.assertRaises(contract.CodexContractError) as raised:
                        contract.resolve_measurement_path(package, value)

                self.assertEqual(result.returncode, 2, result.stderr)
                self.assertIn(
                    "mapping source escapes adapter root",
                    result.stderr.lower(),
                )
                self.assertIn(
                    "MEASUREMENT_INPUT_INVALID",
                    {item.code for item in raised.exception.diagnostics},
                )

    def test_windows_nonportable_components_are_rejected(self) -> None:
        module_root = str(ROOT / "scripts")
        if module_root not in sys.path:
            sys.path.insert(0, module_root)
        import validate_codex_contract as contract

        invalid_cases = (
            "references/carrier.md:contract.md",
            "references/less<than.md",
            "references/greater>than.md",
            'references/double"quote.md',
            "references/pipe|name.md",
            "references/question?.md",
            "references/star*.md",
            "references/CON",
            "references/prn.md",
            "references/AuX.txt",
            "references/nul.json",
            "references/CON/contract.md",
            "references/COM1.md",
            "references/com9",
            "references/LPT1.txt",
            "references/lpt9.json",
            "references/con.tar.gz",
            "references/CON .md",
            "references./contract.md",
            "references /contract.md",
            "references/contract.md.",
            "references/contract.md ",
            "references/...",
            "references/.. ",
        )
        for value in invalid_cases:
            with self.subTest(value=value):
                self.assertFalse(contract.is_portable_relative_path(value))

        valid_cases = (
            ".",
            "..",
            "./references/contract.md",
            "references/../references/contract.md",
            "references/CONSOLE.md",
            "references/.hidden.md",
            "references/AUXILIARY.md",
            "references/NULL.md",
            "references/COM0.md",
            "references/COM10.md",
            "references/LPT0.md",
            "references/LPT10.md",
            "references/name..part.md",
            "references/file%3Aname.md",
        )
        for value in valid_cases:
            with self.subTest(value=value):
                self.assertTrue(contract.is_portable_relative_path(value))

    def test_ntfs_ads_markdown_targets_fail_closed_for_both_syntaxes(self) -> None:
        markdown_cases = (
            "Read [contract](references/carrier.md:contract.md).\n",
            "Read [contract][dependency].\n\n"
            "[dependency]: references/carrier.md:contract.md\n",
        )
        for markdown in markdown_cases:
            with self.subTest(markdown=markdown):
                with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
                    temp_root = Path(temporary)
                    package = create_package(temp_root)
                    write_text(
                        package / "skills" / "consumer" / "SKILL.md",
                        "---\nname: consumer\ndescription: fixture\n---\n\n"
                        "# Fixture\n\n## Consumer\n\n"
                        f"{markdown}",
                    )
                    carrier = (
                        package
                        / "skills"
                        / "consumer"
                        / "references"
                        / "carrier.md"
                    )
                    write_text(carrier, "# Carrier\n")
                    write_text(
                        carrier.with_name("carrier.md:contract.md"),
                        "# Contract\n\nFixture.\n",
                    )
                    mapping = temp_root / "rule-mapping.yaml"
                    write_mapping(
                        mapping,
                        source="plugin/ask-then-do-it/skills/consumer/SKILL.md",
                        section="Consumer",
                    )
                    result = run_validator(
                        adapter_root=temp_root,
                        source_package=package,
                        rule_mapping=mapping,
                    )

                self.assertEqual(result.returncode, 2, result.stderr)
                self.assertIn("REFERENCE_PATH_ESCAPE", result.stderr)
                self.assertNotIn("Traceback", result.stderr)

    def test_win32_alias_markdown_targets_fail_closed(self) -> None:
        destinations = (
            "references./contract.md",
            "references%2E/contract.md",
            "references%20/contract.md",
        )
        syntaxes = (
            "Read [contract]({destination}).\n",
            "Read [contract][dependency].\n\n"
            "[dependency]: {destination}\n",
        )
        for destination in destinations:
            for syntax in syntaxes:
                with self.subTest(destination=destination, syntax=syntax):
                    with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
                        temp_root = Path(temporary)
                        package = create_package(temp_root)
                        mapping = temp_root / "rule-mapping.yaml"
                        write_mapping(
                            mapping,
                            source="plugin/ask-then-do-it/skills/consumer/SKILL.md",
                            section="Consumer",
                        )
                        write_text(
                            package / "skills" / "consumer" / "SKILL.md",
                            "---\nname: consumer\ndescription: fixture\n---\n\n"
                            "# Fixture\n\n## Consumer\n\n"
                            + syntax.format(destination=destination),
                        )
                        result = run_validator(
                            adapter_root=temp_root,
                            source_package=package,
                            rule_mapping=mapping,
                        )

                    self.assertEqual(result.returncode, 2, result.stderr)
                    self.assertIn("REFERENCE_PATH_ESCAPE", result.stderr)
                    self.assertNotIn("Traceback", result.stderr)

    def test_ntfs_ads_paths_fail_closed_for_non_markdown_consumers(self) -> None:
        module_root = str(ROOT / "scripts")
        if module_root not in sys.path:
            sys.path.insert(0, module_root)
        import validate_codex_contract as contract

        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            temp_root = Path(temporary)
            package = create_package(temp_root)
            carrier = (
                package
                / "skills"
                / "consumer"
                / "references"
                / "carrier.md"
            )
            write_text(carrier, "# Carrier\n")
            write_text(
                carrier.with_name("carrier.md:contract.md"),
                "# Contract\n\nFixture.\n",
            )
            relative = "skills/consumer/references/carrier.md:contract.md"

            package_diagnostics: list[contract.Diagnostic] = []
            package_result = contract.validate_package_file(
                package,
                relative,
                package_diagnostics,
                missing_code="PACKAGE_TARGET_MISSING",
                missing_detail="package target is missing",
            )

            mapping_source = (
                "plugin/ask-then-do-it/skills/consumer/SKILL.md:contract.md"
            )
            write_text(
                package / "skills" / "consumer" / "SKILL.md:contract.md",
                "# Fixture\n\n## Consumer\n\nFixture.\n",
            )
            mapping = temp_root / "rule-mapping.yaml"
            write_mapping(mapping, source=mapping_source, section="Consumer")
            mapping_result = run_validator(
                adapter_root=temp_root,
                source_package=package,
                rule_mapping=mapping,
            )

            with self.assertRaises(contract.CodexContractError) as raised:
                contract.resolve_measurement_path(package, relative)

        self.assertIsNone(package_result)
        self.assertEqual(
            [item.code for item in package_diagnostics],
            ["PACKAGE_PATH_ESCAPE"],
        )
        self.assertEqual(mapping_result.returncode, 2, mapping_result.stderr)
        self.assertIn("MAPPING_SOURCE_ESCAPE", mapping_result.stderr)
        self.assertIn(
            "MEASUREMENT_INPUT_INVALID",
            {item.code for item in raised.exception.diagnostics},
        )

    def test_unlisted_path_aliases_fail_closed_for_all_consumers(self) -> None:
        module_root = str(ROOT / "scripts")
        if module_root not in sys.path:
            sys.path.insert(0, module_root)
        import validate_codex_contract as contract

        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            temp_root = Path(temporary)
            package = create_package(temp_root)
            source = package / "skills" / "consumer" / "SKILL.md"
            reference = (
                package
                / "skills"
                / "consumer"
                / "references"
                / "contract.md"
            )
            mapping = temp_root / "rule-mapping.yaml"
            write_mapping(
                mapping,
                source="plugin/ask-then-do-it/skills/consumer/SKILL.md",
                section="Consumer",
            )
            original_iterdir = Path.iterdir

            def without_entry(directory: Path, hidden_name: str):
                def filtered_iterdir(path: Path):
                    entries = original_iterdir(path)
                    if path == directory:
                        return (
                            entry for entry in entries if entry.name != hidden_name
                        )
                    return entries

                return mock.patch.object(Path, "iterdir", new=filtered_iterdir)

            reference_diagnostics: list[contract.Diagnostic] = []
            with without_entry(reference.parent, reference.name):
                reference_result = contract.resolve_reference(
                    source,
                    "references/contract.md",
                    package,
                    reference_diagnostics,
                )

            package_diagnostics: list[contract.Diagnostic] = []
            with without_entry(reference.parent, reference.name):
                package_result = contract.validate_package_file(
                    package,
                    "skills/consumer/references/contract.md",
                    package_diagnostics,
                    missing_code="PACKAGE_TARGET_MISSING",
                    missing_detail="package target is missing",
                )

            with without_entry(source.parent, source.name):
                _, mapping_diagnostics = contract.validate_rule_mapping(
                    temp_root,
                    package,
                    package,
                    mapping,
                    {
                        "skills/consumer/SKILL.md",
                        "skills/consumer/references/contract.md",
                    },
                )

            with without_entry(source.parent, source.name), self.assertRaises(
                contract.CodexContractError
            ) as measurement_error:
                contract.resolve_measurement_path(
                    package,
                    "skills/consumer/SKILL.md",
                )

        self.assertIsNone(reference_result)
        self.assertEqual(
            [item.code for item in reference_diagnostics],
            ["REFERENCE_PATH_ESCAPE"],
        )
        self.assertIsNone(package_result)
        self.assertEqual(
            [item.code for item in package_diagnostics],
            ["PACKAGE_PATH_ESCAPE"],
        )
        self.assertIn(
            "MAPPING_SOURCE_ESCAPE",
            {item.code for item in mapping_diagnostics},
        )
        self.assertIn(
            "MEASUREMENT_INPUT_INVALID",
            {item.code for item in measurement_error.exception.diagnostics},
        )

    def test_report_output_io_failures_are_controlled(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            temp_root = Path(temporary)
            blocked_parent = temp_root / "blocked-parent"
            write_text(blocked_parent, "not a directory\n")
            cases = (
                temp_root,
                blocked_parent / "report.json",
            )
            for report in cases:
                with self.subTest(report=report):
                    result = run_validator(report=report)

                    self.assertEqual(result.returncode, 2, result.stderr)
                    self.assertIn("REPORT_WRITE_FAILED", result.stderr)
                    self.assertNotIn("Traceback", result.stderr)

    def test_package_relative_paths_require_exact_component_case(self) -> None:
        module_root = str(ROOT / "scripts")
        if module_root not in sys.path:
            sys.path.insert(0, module_root)
        import validate_codex_contract as contract

        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            temp_root = Path(temporary)
            reference_package = create_package(
                temp_root / "reference-case",
                link="references/CONTRACT.md",
            )
            reference_mapping = temp_root / "reference-case" / "rule-mapping.yaml"
            write_mapping(
                reference_mapping,
                source="plugin/ask-then-do-it/skills/consumer/SKILL.md",
                section="Consumer",
            )
            reference_result = run_validator(
                adapter_root=temp_root / "reference-case",
                source_package=reference_package,
                rule_mapping=reference_mapping,
            )

            mapping_root = temp_root / "mapping-case"
            mapping_package = create_package(mapping_root)
            mapping = mapping_root / "rule-mapping.yaml"
            write_mapping(
                mapping,
                source="plugin/ask-then-do-it/skills/CONSUMER/SKILL.md",
                section="Consumer",
            )
            mapping_result = run_validator(
                adapter_root=mapping_root,
                source_package=mapping_package,
                rule_mapping=mapping,
            )

            package_root = temp_root / "package-case"
            source_package = create_package(package_root)
            built_package = package_root / "built-package"
            shutil.copytree(source_package, built_package)
            built_reference = (
                built_package
                / "skills"
                / "consumer"
                / "references"
                / "contract.md"
            )
            intermediate_reference = built_reference.with_name("contract.tmp")
            built_reference.rename(intermediate_reference)
            intermediate_reference.rename(built_reference.with_name("CONTRACT.md"))
            package_mapping = package_root / "rule-mapping.yaml"
            write_mapping(
                package_mapping,
                source="plugin/ask-then-do-it/skills/consumer/SKILL.md",
                section="Consumer",
            )
            package_result = run_validator(
                adapter_root=package_root,
                source_package=source_package,
                package_root=built_package,
                rule_mapping=package_mapping,
            )

            with self.subTest(path_kind="reference"):
                self.assertEqual(
                    reference_result.returncode,
                    2,
                    reference_result.stderr,
                )
                self.assertIn(
                    "reference path casing differs",
                    reference_result.stderr.lower(),
                )
            with self.subTest(path_kind="mapping"):
                self.assertEqual(mapping_result.returncode, 2, mapping_result.stderr)
                self.assertIn(
                    "mapping source path casing differs",
                    mapping_result.stderr.lower(),
                )
            with self.subTest(path_kind="built-package"):
                self.assertEqual(package_result.returncode, 2, package_result.stderr)
                self.assertIn(
                    "package target path casing differs",
                    package_result.stderr.lower(),
                )
            with self.subTest(path_kind="measurement"):
                with self.assertRaises(contract.CodexContractError) as raised:
                    contract.resolve_measurement_path(
                        mapping_package,
                        "skills/CONSUMER/SKILL.md",
                    )
                self.assertIn(
                    "MEASUREMENT_INPUT_CASE_MISMATCH",
                    {item.code for item in raised.exception.diagnostics},
                )

    def test_rule_mapping_rejects_leading_syntax_and_duplicate_rules_key(self) -> None:
        cases = (
            (
                "not valid yaml [\n"
                "rules:\n"
                "  TEST-RULE-001:\n"
                "    - file: plugin/ask-then-do-it/skills/consumer/SKILL.md\n"
                "      section: Consumer\n"
                "      implementation: fixture mapping\n",
                ("unsupported rule-mapping syntax",),
            ),
            (
                "rules:\n"
                "rules:\n"
                "  TEST-RULE-001:\n"
                "    - file: plugin/ask-then-do-it/skills/consumer/SKILL.md\n"
                "      section: Consumer\n"
                "      implementation: fixture mapping\n",
                ("duplicate rules key",),
            ),
            (
                "  TEST-RULE-001:\n"
                "rules:\n"
                "  TEST-RULE-001:\n"
                "    - file: plugin/ask-then-do-it/skills/consumer/SKILL.md\n"
                "      section: Consumer\n"
                "      implementation: fixture mapping\n",
                ("unsupported rule-mapping syntax",),
            ),
            (
                "unsupported: true\n"
                "rules:\n"
                "rules:\n"
                "  TEST-RULE-001:\n"
                "    - file: plugin/ask-then-do-it/skills/consumer/SKILL.md\n"
                "      section: Consumer\n"
                "      implementation: fixture mapping\n",
                ("unsupported rule-mapping syntax", "duplicate rules key"),
            ),
        )
        for mapping_text, expected_errors in cases:
            with self.subTest(mapping=mapping_text):
                with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
                    temp_root = Path(temporary)
                    package = create_package(temp_root)
                    mapping = temp_root / "rule-mapping.yaml"
                    write_text(mapping, mapping_text)
                    result = run_validator(
                        adapter_root=temp_root,
                        source_package=package,
                        rule_mapping=mapping,
                    )

                self.assertEqual(result.returncode, 2, result.stderr)
                for expected_error in expected_errors:
                    self.assertIn(expected_error, result.stderr.lower())


if __name__ == "__main__":
    unittest.main()

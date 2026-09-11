import json
import re
import unittest
from dataclasses import dataclass
from pathlib import Path

import yaml

from tests.claude.test_public_plugin_contract import ARCHITECTURE_LENSES


ROOT = Path(__file__).resolve().parents[2]
PROFILE = (
    ROOT
    / "adapters"
    / "claude-code"
    / "plugin"
    / "ask-then-do-it"
    / "profiles"
    / "general"
)
RULES = ROOT / "core" / "rules" / "rules.yaml"
SCENARIOS = ROOT / "tests" / "claude" / "fixtures" / "general-profile" / "scenarios.json"
REVIEWED_INSTRUCTIONS = SCENARIOS.with_name("reviewed-instructions.json")

EXPECTED_MODULES = {
    "orchestration.md",
    "lite-workflow.md",
    "requirements.md",
    "documented-requirements.md",
    "specification.md",
    "ticket-planning.md",
    "tdd-implementation.md",
    "direct-implementation.md",
    "review.md",
    "architecture-improvement.md",
}
EXPECTED_SCENARIOS = {
    "CAP-CONVERSATION",
    "CAP-TOOLS",
    "CAP-MULTI-AGENT",
    "MODE-EXPLICIT",
    "MODE-CONFIG",
    "MODE-INVALID",
    "FULL-REQUIREMENTS",
    "FULL-KNOWLEDGE",
    "FULL-SPEC",
    "FULL-PLAN",
    "FULL-TDD",
    "FULL-DIRECT",
    "FULL-REVIEW",
    "FULL-ARCH",
    "LITE-QUESTIONS",
    "LITE-BRIEF",
    "LITE-RISK",
    "LITE-VALIDATION",
    "LITE-REVIEW",
    "LITE-SESSION",
    "ROUTE-AUTO",
    "ROUTE-EXPLICIT-5",
    "ROUTE-FAILURE",
    "ROUTE-SWITCH",
    "SESSION-LIFECYCLE",
    "INSTALL-STATUS",
    "INSTALL-WRITES",
    "REMOVE-ZIP",
    "DOCS-PACKAGE",
    "RELEASE-INTEGRITY",
}


@dataclass(frozen=True)
class ScenarioContract:
    module: str
    input_state: str
    expected_outcomes: tuple[str, ...]
    prohibited_actions: tuple[str, ...]


# These static coverage notes locate the instructions for each planned scenario.
# They are not model inputs or observed outputs. Whole-module reviewed text is
# checked separately; pattern presence alone must never certify changed prose.
SCENARIO_CONTRACTS = {
    "CAP-CONVERSATION": ScenarioContract(
        "orchestration.md",
        "Only conversation capability is proven.",
        ("exchange text and produce user-managed artifacts only", "give a safe handoff"),
        ("conversation may claim repository access",),
    ),
    "CAP-TOOLS": ScenarioContract(
        "orchestration.md",
        "Repository read/write and command execution are proven.",
        ("proven repository read/write access", "claim only actions and raw evidence actually observed"),
        ("claim commands that were not observed",),
    ),
    "CAP-MULTI-AGENT": ScenarioContract(
        "review.md",
        "An isolated reviewer is available, or a weaker capability must be disclosed.",
        (
            "delegate to the independent read-only reviewer",
            "wait for the reviewer to finish",
            "with `tools` but no usable reviewer/agent, perform the full review in the same context, label it `non-independent`",
            "with only `conversation` or user excerpts, label it `limited-evidence`",
        ),
        ("tools but no usable reviewer/agent, label it `limited-evidence`", "only `conversation` or user excerpts, label it `non-independent`"),
    ),
    "MODE-EXPLICIT": ScenarioContract(
        "orchestration.md",
        "The current operation supplies one or conflicting explicit modes.",
        ("valid explicit current-operation instruction", "ask one clarification and stop"),
        ("silently choose full when explicit full and lite conflict",),
    ),
    "MODE-CONFIG": ScenarioContract(
        "orchestration.md",
        "No explicit mode exists and project/user Config sources are considered in order.",
        ("<project>/.claude/ask-then-do-it.toml", "~/.claude/ask-then-do-it.toml", "full fallback"),
        ("read the user config before the project config",),
    ),
    "MODE-INVALID": ScenarioContract(
        "orchestration.md",
        "A Config is present but invalid or unreadable.",
        ("present but unreadable", "must fail closed to `full`", "must not read the user config"),
        ("repair the invalid config",),
    ),
    "FULL-REQUIREMENTS": ScenarioContract(
        "requirements.md",
        "Full mode has unresolved product decisions.",
        ("ask exactly one question per turn", "only a later direct approval changes it to `approved`"),
        ("silence approves the requirement decision record",),
    ),
    "FULL-KNOWLEDGE": ScenarioContract(
        "documented-requirements.md",
        "Existing-system work may change durable project knowledge.",
        ("maintain draft working notes", "ask one single explicit approval covering the exact displayed record and summary"),
        ("apply undisclosed knowledge changes",),
    ),
    "FULL-SPEC": ScenarioContract(
        "specification.md",
        "Confirmed requirements exist but the Specification is not approved.",
        ("implementation-independent behavioral specification", "only after approval evidence exists may status become `approved`"),
        ("draft or disputed specifications can authorize ticket planning",),
    ),
    "FULL-PLAN": ScenarioContract(
        "ticket-planning.md",
        "An Approved Specification needs vertically testable Tickets and explicit test choices.",
        ("map add tests to `tdd` and do not add tests to `direct`", "only direct approval changes it to approved"),
        ("map add tests to `direct` and do not add tests to `tdd`",),
    ),
    "FULL-TDD": ScenarioContract(
        "tdd-implementation.md",
        "The Approved Ticket mode is tdd.",
        ("observe the expected failing test", "before production", "smallest coherent production change for green"),
        ("approved mode is `direct`", "edit production before red"),
    ),
    "FULL-DIRECT": ScenarioContract(
        "direct-implementation.md",
        "The Approved Ticket mode is direct.",
        ("approved mode is `direct`", "must not create, modify, or execute behavioral tests", "tests: skipped-by-user"),
        ("approved mode is `tdd`", "add a failing behavioral test"),
    ),
    "FULL-REVIEW": ScenarioContract(
        "review.md",
        "Implementation evidence and final bytes are ready for Full Review.",
        ("review authorizes diagnosis and reporting, not fixes", "all twelve architecture and refactoring lenses"),
        ("review authorizes implementation of fixes",),
    ),
    "FULL-ARCH": ScenarioContract(
        "architecture-improvement.md",
        "A direct or proven automatic architecture trigger requests diagnosis.",
        ("diagnostic-only", "without all three, simulation is the only allowed path", "acceptance authorizes only specification work"),
        ("actual deletion requires only one guard", "acceptance authorizes direct implementation"),
    ),
    "LITE-QUESTIONS": ScenarioContract(
        "lite-workflow.md",
        "Lite reconnaissance has blocking questions.",
        ("no more than three questions", "each asks one decision and includes one concrete recommendation"),
        ("ask four blocking questions in one round",),
    ),
    "LITE-BRIEF": ScenarioContract(
        "lite-workflow.md",
        "Lite blockers are resolved and implementation has not started.",
        ("one conversation-only change brief", "lite has exactly one formal approval before implementation"),
        ("production changes start before explicit approval",),
    ),
    "LITE-RISK": ScenarioContract(
        "lite-workflow.md",
        "Material risk appears before or during Lite implementation.",
        ("pause on material risk", "ask whether to switch to full for the current operation only"),
        ("persist the lite/full choice",),
    ),
    "LITE-VALIDATION": ScenarioContract(
        "lite-workflow.md",
        "An approved Lite brief is implemented with available checks.",
        ("must not create or modify behavioral tests", "one principal success path and one important failure or boundary path"),
        ("lite may claim red/green/refactor evidence",),
    ),
    "LITE-REVIEW": ScenarioContract(
        "lite-workflow.md",
        "Lite implementation reaches same-context Review.",
        ("compact same-context review", "do not fix it until the user explicitly approves it"),
        ("the plugin reviewer upgrades lite to an independent full review",),
    ),
    "LITE-SESSION": ScenarioContract(
        "lite-workflow.md",
        "A new session follows earlier Lite conversation state.",
        ("lite conversation state is not durable across sessions", "a new session must resolve mode again"),
        ("a new session resumes unpersisted lite state",),
    ),
    "ROUTE-AUTO": ScenarioContract(
        "orchestration.md",
        "The public bootstrap supplied an automatic General ready binding.",
        ("automatic unknown-model compatibility", "this profile must not classify a model"),
        ("general profile reclassifies the active model",),
    ),
    "ROUTE-EXPLICIT-5": ScenarioContract(
        "orchestration.md",
        "An explicit Claude 5 entry produced a General binding on a supported non-Claude-5 model.",
        ("explicit claude 5 entry on a supported non-claude-5 model", "must not reroute"),
        ("override the bootstrap binding",),
    ),
    "ROUTE-FAILURE": ScenarioContract(
        "orchestration.md",
        "The public bootstrap envelope is missing or reports failure.",
        ("a missing or failure envelope must stop before profile loading",),
        ("recover inside this module after bootstrap failure",),
    ),
    "ROUTE-SWITCH": ScenarioContract(
        "orchestration.md",
        "A model-switch notice arrives during an operation-bound General run.",
        ("current operation profile remains unchanged", "next permitted public entry may reroute"),
        ("switch the current operation to the other profile",),
    ),
    "SESSION-LIFECYCLE": ScenarioContract(
        "orchestration.md",
        "Startup/resume/fork/clear/compact lifecycle evidence is evaluated.",
        ("never copy authority across sessions", "a stale last binding never authorizes another session"),
        ("startup automatically resumes the last operation",),
    ),
    "INSTALL-STATUS": ScenarioContract(
        "orchestration.md",
        "The user asks only for lifecycle status/version information.",
        ("a status/version check is completely read-only", "status must not refresh, install, update, enable, disable, remove, or write config"),
        ("status refreshes the marketplace",),
    ),
    "INSTALL-WRITES": ScenarioContract(
        "orchestration.md",
        "An explicit install/update is requested and fresh ownership state is evaluated.",
        ("immediately before every install, update, or normal remove write", "stop without writes"),
        ("write when ownership evidence changed", "perform a remove-first update"),
    ),
    "REMOVE-ZIP": ScenarioContract(
        "orchestration.md",
        "A normal remove or session-only ZIP recovery is requested.",
        ("normal remove", "add `--keep-data` only after an explicit user request", "zip recovery is session-only"),
        ("always add `--keep-data`", "unconditionally add `--keep-data`"),
    ),
    "DOCS-PACKAGE": ScenarioContract(
        "orchestration.md",
        "Documentation or package contents are prepared.",
        ("preserve three-language ownership", "exactly two supported namespaced entries"),
        ("documentation may invent a third public command",),
    ),
    "RELEASE-INTEGRITY": ScenarioContract(
        "orchestration.md",
        "A local release candidate is prepared without publication authority.",
        ("preserve all three package families", "require separate authority"),
        ("publish the local candidate automatically",),
    ),
}


CORE_RULE_OWNERS = {
    "orchestration.md": {
        "CAP-DECLARE-001",
        "CAP-CLAIM-001",
        "MODE-RESOLVE-001",
        "FULL-PRESERVE-001",
        "ADAPTER-COVERAGE-001",
        "ROUTE-USER-001",
        "ROUTE-DOCS-001",
    },
    "lite-workflow.md": {
        "LITE-QUESTIONS-001",
        "LITE-BRIEF-001",
        "LITE-RISK-001",
        "LITE-VALIDATE-001",
        "LITE-REVIEW-001",
        "LITE-SESSION-001",
    },
    "requirements.md": {"GATE-REQ-001", "GRILL-ONE-001"},
    "documented-requirements.md": {
        "KB-EVIDENCE-001",
        "KB-DRAFT-001",
        "KB-SYNC-001",
    },
    "specification.md": {"GATE-SPEC-001", "SPEC-NOCODE-001", "ART-STATE-001"},
    "ticket-planning.md": {"GATE-PLAN-001", "PLAN-VERTICAL-001"},
    "tdd-implementation.md": {"TDD-RED-001"},
    "direct-implementation.md": set(),
    "review.md": {"REVIEW-EVIDENCE-001", "REVIEW-LENSES-001"},
    "architecture-improvement.md": {
        "ARCH-DIAG-001",
        "ARCH-DELETE-001",
        "ARCH-REPORT-001",
        "ARCH-REFLOW-001",
    },
}

ARTIFACT_ENVELOPE_FIELDS = (
    "artifact_type",
    "artifact_id",
    "workflow_id",
    "core_version",
    "status",
    "inputs",
    "assumptions",
    "deferred",
    "handoff",
)
ARTIFACT_PRODUCING_STAGES = {
    "requirements.md",
    "documented-requirements.md",
    "specification.md",
    "ticket-planning.md",
    "tdd-implementation.md",
    "direct-implementation.md",
    "review.md",
    "architecture-improvement.md",
}
CONVERSATION_CONFIG_TRANSITIONS = (
    (
        "conversation",
        "none",
        "host-unavailable",
        "valid full or lite",
        "treat project as absent; select the valid user mode",
    ),
    (
        "conversation",
        "none",
        "host-unavailable",
        "host-unavailable",
        "treat both as absent; select full fallback",
    ),
    (
        "conversation",
        "none",
        "absent",
        "host-unavailable",
        "treat user as absent; select full fallback",
    ),
)
ARCHITECTURE_TRANSITIONS = (
    (
        "direct architecture request",
        "`architecture-improvement.md`",
        "explicit user route; no automatic-route announcement required",
    ),
    (
        "systemic review evidence",
        "`architecture-improvement.md`",
        "announce the evidence and reason before automatic routing",
    ),
    (
        "related ticket group completes",
        "`architecture-improvement.md`",
        "announce the evidence and reason before automatic routing",
    ),
    (
        "release milestone approaches",
        "`architecture-improvement.md`",
        "announce the evidence and reason before automatic routing",
    ),
    (
        "focused local review finding",
        "`review.md`",
        "stay in review; do not route to architecture improvement",
    ),
    (
        "accepted architecture improvement report",
        "`specification.md`",
        "return to specification; never route directly to planning or implementation",
    ),
)
FULL_ROUTE_PRECEDENCE = (
    (
        "direct architecture diagnosis",
        "any",
        "mode, capability, safety, and the architecture stage's own authorization prerequisites",
        "`architecture-improvement.md`",
        "diagnosis only; no implementation",
    ),
    (
        "automatic architecture trigger",
        "relevant full delivery gates complete and trigger proven",
        "announce the evidence and reason",
        "`architecture-improvement.md`",
        "diagnosis only; no implementation",
    ),
    (
        "accepted architecture improvement report",
        "any",
        "acceptance evidence",
        "`specification.md`",
        "no direct planning or implementation",
    ),
)
LIFECYCLE_WRITE_TRANSITIONS = (
    (
        "install or update",
        "expected source, qualified identity, exact user scope, and unambiguous current state",
        "permit only the explicitly requested bounded write",
    ),
    (
        "normal remove",
        "expected marketplace/source, qualified identity, exact user scope, and unambiguous ownership and state",
        "permit only the qualified user-scope uninstall",
    ),
    (
        "any write",
        "missing, unreadable, changed, mismatched, non-user, or multi-scope evidence",
        "stop without writes",
    ),
)
KNOWLEDGE_TRANSITIONS = (
    (
        "each approved or accepted artifact changes durable facts",
        "propose a complete knowledge base change summary tied to that artifact; display additions, modifications, and removals including none; request joint approval for the exact displayed artifact and knowledge changes before applying them",
    ),
    (
        "artifact adds no durable fact",
        "continue the unrelated gate without a knowledge update or delay",
    ),
)


def normalized(value: str) -> str:
    return " ".join(value.lower().split())


def markdown_section(source: str, heading: str) -> str:
    match = re.search(
        rf"(?ms)^## {re.escape(heading)}\r?\n(.*?)(?=^## |\Z)",
        source,
    )
    if match is None:
        raise AssertionError(f"missing section: {heading}")
    return match.group(1)


def markdown_table(source: str, heading: str) -> tuple[tuple[str, ...], ...]:
    section = markdown_section(source, heading)
    rows = []
    for line in section.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        cells = tuple(normalized(cell) for cell in stripped.strip("|").split("|"))
        if cells and all(re.fullmatch(r":?-+:?", cell.replace(" ", "")) for cell in cells):
            continue
        rows.append(cells)
    if len(rows) < 2:
        raise AssertionError(f"missing table rows: {heading}")
    return tuple(rows[1:])


def assert_core_rule_ownership(sources: dict[str, str]) -> None:
    if set(sources) != set(CORE_RULE_OWNERS):
        raise AssertionError("Core ownership inventory does not match General modules")
    for module, expected in CORE_RULE_OWNERS.items():
        lines = re.findall(r"(?m)^Core rules: ([^\r\n]+)$", sources[module])
        if len(lines) != 1:
            raise AssertionError(f"{module} must have exactly one Core rules line")
        declared = set() if lines[0] == "none" else set(lines[0].split(", "))
        if declared != expected:
            raise AssertionError(
                f"{module} declares {sorted(declared)}, expected {sorted(expected)}"
            )
        markers = set(re.findall(r"\[CORE: ([A-Z0-9-]+)\]", sources[module]))
        if markers != expected:
            raise AssertionError(
                f"{module} marks {sorted(markers)}, expected {sorted(expected)}"
            )


def assert_reviewed_instructions(sources: dict[str, str]) -> None:
    """Reject any unreviewed prompt edit, including additive contradictions.

    This is a frozen-text integrity boundary, not a natural-language evaluator.
    Never regenerate its independent fixture as part of a test run.
    """
    snapshot = json.loads(REVIEWED_INSTRUCTIONS.read_text(encoding="utf-8"))
    if set(snapshot) != {"schema_version", "profile", "modules"}:
        raise AssertionError("unexpected General reviewed-instruction schema")
    if snapshot["schema_version"] != 1 or snapshot["profile"] != "general":
        raise AssertionError("wrong General reviewed-instruction identity")
    expected = snapshot["modules"]
    if set(expected) != EXPECTED_MODULES or set(sources) != EXPECTED_MODULES:
        raise AssertionError("reviewed instruction inventory must be exactly ten modules")
    for module in sorted(EXPECTED_MODULES):
        # Preserve case, indentation, paragraphs and ordering, all of which can
        # affect Markdown instructions. Only platform line endings are equivalent.
        if sources[module].replace("\r\n", "\n") != expected[module]:
            raise AssertionError(
                f"{module}: instructions differ from the frozen review baseline; "
                "review the change and its scenario coverage before updating the fixture"
            )


def assert_scenario_contracts(sources: dict[str, str]) -> None:
    assert_reviewed_instructions(sources)
    if set(SCENARIO_CONTRACTS) != EXPECTED_SCENARIOS:
        raise AssertionError("test-owned scenario inventory is incomplete")
    for scenario_id, contract in SCENARIO_CONTRACTS.items():
        if not contract.input_state.strip():
            raise AssertionError(f"{scenario_id} has no input state")
        if not contract.expected_outcomes:
            raise AssertionError(f"{scenario_id} has no expected outcome")
        if not contract.prohibited_actions:
            raise AssertionError(f"{scenario_id} has no prohibited action")
        if contract.module not in sources:
            raise AssertionError(f"{scenario_id} has unknown owner {contract.module}")
        body = normalized(sources[contract.module])
        marker = f"[scenario: {scenario_id.lower()}]"
        if marker not in body:
            raise AssertionError(f"{scenario_id} marker is missing")
        for expected in contract.expected_outcomes:
            if normalized(expected) not in body:
                raise AssertionError(
                    f"{scenario_id} is missing expected outcome: {expected}"
                )
        for prohibited in contract.prohibited_actions:
            if normalized(prohibited) in body:
                raise AssertionError(
                    f"{scenario_id} contains prohibited action: {prohibited}"
                )


def assert_no_affirmative_cross_profile_load(sources: dict[str, str]) -> None:
    ambiguous_load = re.compile(
        r"\b(?:load|follow|obey)\b.*\b(?:other|optimized|alternate|different) profile\b"
    )
    negations = ("never", "must not", "do not", "reject", "prohibit")
    for module, source in sources.items():
        for line_number, line in enumerate(source.splitlines(), start=1):
            statement = normalized(line)
            if ambiguous_load.search(statement) and not any(
                negation in statement for negation in negations
            ):
                raise AssertionError(
                    f"{module}:{line_number} affirmatively loads an ambiguous profile"
                )


def assert_general_load_trace(module_names: tuple[str, ...]) -> None:
    profile_root = PROFILE.resolve()
    for module in module_names:
        if module not in EXPECTED_MODULES:
            raise AssertionError(f"load trace contains a non-General module: {module}")
        resolved = (PROFILE / module).resolve()
        try:
            resolved.relative_to(profile_root)
        except ValueError as error:
            raise AssertionError(f"load trace escapes the General profile: {module}") from error


def assert_lifecycle_write_transitions(source: str) -> None:
    actual = markdown_table(source, "Lifecycle write authorization transitions")
    if actual != LIFECYCLE_WRITE_TRANSITIONS:
        raise AssertionError(f"unexpected lifecycle write transitions: {actual}")
    section = normalized(
        markdown_section(source, "Lifecycle write authorization transitions")
    )
    required = (
        "immediately before every install, update, or normal remove write, perform a fresh complete read-only ownership/source/scope/state recheck"
    )
    if required not in section:
        raise AssertionError("fresh complete pre-write lifecycle recheck is missing")
    if "an earlier status result is insufficient" not in section:
        raise AssertionError("stale lifecycle state is not rejected")


def assert_full_route_precedence(source: str) -> None:
    actual = markdown_table(source, "Full route precedence")
    if actual != FULL_ROUTE_PRECEDENCE:
        raise AssertionError(f"unexpected Full route precedence: {actual}")
    section = normalized(markdown_section(source, "Full route precedence"))
    required = (
        "before the delivery first-unmet order, handle an explicit direct architecture-diagnosis request"
    )
    if required not in section:
        raise AssertionError("direct architecture precedence is missing")
    if "does not require existing requirements, specification, ticket plan, implementation, or review" not in section:
        raise AssertionError("direct architecture is still blocked by delivery gates")
    if "must not bypass the architecture stage's own safety or approval gates" not in section:
        raise AssertionError("architecture-stage safety precedence is missing")


def assert_portable_artifact_contract(sources: dict[str, str]) -> None:
    orchestration = sources["orchestration.md"]
    section = markdown_section(orchestration, "Portable artifact envelope")
    fields = tuple(re.findall(r"(?m)^\d+\. `([a-z_]+)`(?:\b|:)", section))
    if fields != ARTIFACT_ENVELOPE_FIELDS:
        raise AssertionError(f"unexpected portable artifact fields: {fields}")
    contract = normalized(section)
    if "`artifact_id` must be stable" not in contract:
        raise AssertionError("artifact_id stability is not defined")
    if "include `approval` when the artifact has an approval or acceptance gate" not in contract:
        raise AssertionError("conditional approval evidence is not defined")
    dependency = "use the `portable artifact envelope` defined in `orchestration.md`"
    for stage in ARTIFACT_PRODUCING_STAGES:
        if dependency not in normalized(sources[stage]):
            raise AssertionError(f"{stage} does not depend on the shared envelope")


def assert_conversation_config_transitions(source: str) -> None:
    actual = markdown_table(source, "Conversation-only unavailable-source transitions")
    if actual != CONVERSATION_CONFIG_TRANSITIONS:
        raise AssertionError(f"unexpected Config transitions: {actual}")
    section = normalized(
        markdown_section(source, "Conversation-only unavailable-source transitions")
    )
    if "must not claim that an unavailable config was read" not in section:
        raise AssertionError("unavailable Config read-claim prohibition is missing")
    if "host-unavailable is absence, not invalid content" not in section:
        raise AssertionError("unavailable/invalid distinction is missing")


def assert_full_orchestration_transitions(source: str) -> None:
    architecture = markdown_table(source, "Full architecture transitions")
    if architecture != ARCHITECTURE_TRANSITIONS:
        raise AssertionError(f"unexpected architecture transitions: {architecture}")
    knowledge = markdown_table(source, "Durable-knowledge synchronization transitions")
    if knowledge != KNOWLEDGE_TRANSITIONS:
        raise AssertionError(f"unexpected knowledge transitions: {knowledge}")


class ClaudeGeneralProfileTests(unittest.TestCase):
    def test_direct_architecture_defines_the_canonical_lenses_without_review(self) -> None:
        source = (PROFILE / "architecture-improvement.md").read_text(encoding="utf-8")
        match = re.search(r"The canonical lens order is: ([^\n]+)\.", source)
        self.assertIsNotNone(match, "Direct diagnosis must not depend on unloaded review.md")
        self.assertEqual(tuple(match.group(1).split("; ")), ARCHITECTURE_LENSES)

    def profile_sources(self) -> dict[str, str]:
        return {
            path.name: path.read_text(encoding="utf-8")
            for path in PROFILE.glob("*.md")
            if path.is_file()
        }

    def test_general_profile_has_exact_internal_module_inventory(self) -> None:
        sources = self.profile_sources()
        self.assertEqual(set(sources), EXPECTED_MODULES)
        for name, source in sources.items():
            self.assertTrue(source.startswith("# "), name)
            self.assertNotRegex(source, r"\A---\r?\n", name)
            self.assertIn("General profile", source, name)

    def test_additive_inverse_instructions_fail_the_scenario_gate(self) -> None:
        sources = self.profile_sources()
        assert_scenario_contracts(sources)
        mutations = (
            ("ticket-planning.md", "Add tests uses direct / Do not add tests uses tdd."),
            ("orchestration.md", "Treat the other profile as authoritative."),
            ("orchestration.md", "Normal remove may reuse the earlier status result."),
            ("orchestration.md", "Unresolved Requirements take precedence over a direct architecture request."),
        )
        for module, contradiction in mutations:
            with self.subTest(module=module, contradiction=contradiction):
                candidate = dict(sources)
                # Keep every correct sentence and table; append contradictory authority.
                candidate[module] += "\n" + contradiction + "\n"
                with self.assertRaises(AssertionError):
                    assert_scenario_contracts(candidate)

    def test_all_modules_reject_unreviewed_additions_and_reordering(self) -> None:
        sources = self.profile_sources()
        for module, source in sources.items():
            paragraphs = source.split("\n\n")
            mutations = {
                "new-section": source + "\n## Later policy\nThe preceding restrictions no longer apply.\n",
                "inline-addition": source.replace("\n\n", "\n\nFollow a different policy.\n\n", 1),
                "reordered": "\n\n".join([*paragraphs[1:], paragraphs[0]]),
            }
            for label, altered in mutations.items():
                with self.subTest(module=module, mutation=label):
                    candidate = dict(sources)
                    candidate[module] = altered
                    with self.assertRaises(AssertionError):
                        assert_scenario_contracts(candidate)

    def test_general_profile_maps_every_mandatory_core_rule(self) -> None:
        sources = self.profile_sources()
        source = "\n".join(sources.values())
        rules = yaml.safe_load(RULES.read_text(encoding="utf-8"))
        mandatory = {rule["id"] for rule in rules["rules"] if rule["mandatory"]}
        mapped = set(re.findall(r"\[CORE: ([A-Z0-9-]+)\]", source))
        self.assertEqual(len(mandatory), 30)
        self.assertEqual(mapped, mandatory)
        self.assertEqual(set().union(*CORE_RULE_OWNERS.values()), mandatory)
        assert_core_rule_ownership(sources)

        removed = dict(sources)
        removed["orchestration.md"] = removed["orchestration.md"].replace(
            "Core rules: CAP-DECLARE-001, ", "Core rules: ", 1
        )
        removed["orchestration.md"] = removed["orchestration.md"].replace(
            "[CORE: CAP-DECLARE-001]\n", "", 1
        )
        with self.assertRaises(AssertionError):
            assert_core_rule_ownership(removed)

        relocated = dict(sources)
        relocated["orchestration.md"] = relocated["orchestration.md"].replace(
            "Core rules: CAP-DECLARE-001, ", "Core rules: ", 1
        )
        relocated["orchestration.md"] = relocated["orchestration.md"].replace(
            "[CORE: CAP-DECLARE-001]\n", "", 1
        )
        relocated["requirements.md"] = relocated["requirements.md"].replace(
            "Core rules: ", "Core rules: CAP-DECLARE-001, ", 1
        )
        relocated["requirements.md"] = relocated["requirements.md"].replace(
            "[CORE: GRILL-ONE-001]",
            "[CORE: CAP-DECLARE-001]\n[CORE: GRILL-ONE-001]",
            1,
        )
        with self.assertRaises(AssertionError):
            assert_core_rule_ownership(relocated)

    def test_fixed_thirty_scenarios_have_reviewed_instruction_contracts(self) -> None:
        fixture = json.loads(SCENARIOS.read_text(encoding="utf-8"))
        self.assertEqual(fixture["schema_version"], 2)
        self.assertEqual(fixture["profile"], "general")
        scenarios = fixture["scenarios"]
        ids = [scenario["id"] for scenario in scenarios]
        self.assertEqual(len(ids), 30)
        self.assertEqual(len(set(ids)), 30)
        self.assertEqual(set(ids), EXPECTED_SCENARIOS)

        sources = self.profile_sources()
        for scenario in scenarios:
            with self.subTest(scenario=scenario["id"]):
                self.assertEqual(set(scenario), {"id", "module"})
                self.assertEqual(
                    scenario["module"], SCENARIO_CONTRACTS[scenario["id"]].module
                )
                assert_general_load_trace(("orchestration.md", scenario["module"]))
        assert_scenario_contracts(sources)

        mutations = (
            (
                "ticket plan inverse mapping",
                "ticket-planning.md",
                "Map Add tests to `tdd` and Do not add tests to `direct`",
                "Map Add tests to `direct` and Do not add tests to `tdd`",
            ),
            (
                "review downgrade inverse mapping",
                "review.md",
                "label it `non-independent`",
                "label it `limited-evidence`",
            ),
            (
                "architecture deletion guard bypass",
                "architecture-improvement.md",
                "Without all three, simulation is the only allowed path",
                "With any one guard, actual deletion is allowed",
            ),
            (
                "unconditional data retention",
                "orchestration.md",
                "add `--keep-data` only after an explicit user request",
                "always add `--keep-data`",
            ),
            (
                "requirement approval bypass",
                "requirements.md",
                "Only a later direct approval changes it to `Approved`",
                "Silence approves the requirement decision record",
            ),
            (
                "TDD and direct inverse",
                "tdd-implementation.md",
                "Approved mode is `tdd`",
                "Approved mode is `direct`",
            ),
        )
        for name, module, correct, inverse in mutations:
            with self.subTest(mutation=name):
                mutated = dict(sources)
                self.assertIn(correct, mutated[module])
                mutated[module] = mutated[module].replace(correct, inverse, 1)
                with self.assertRaises(AssertionError):
                    assert_scenario_contracts(mutated)

    def test_claude_config_and_lifecycle_are_read_only_and_fail_closed(self) -> None:
        orchestration = normalized((PROFILE / "orchestration.md").read_text(encoding="utf-8"))
        self.assertIn("valid explicit current-operation instruction", orchestration)
        self.assertLess(
            orchestration.index("valid explicit current-operation instruction"),
            orchestration.index("<project>/.claude/ask-then-do-it.toml"),
        )
        self.assertLess(
            orchestration.index("<project>/.claude/ask-then-do-it.toml"),
            orchestration.index("~/.claude/ask-then-do-it.toml"),
        )
        self.assertIn("must not write `settings.json`", orchestration)
        self.assertIn("must not read or write codex config", orchestration)
        self.assertIn("must not persist an operation override", orchestration)
        self.assertIn("`/reload-plugins` or a new session", orchestration)

    def test_review_downgrades_are_honest_and_lite_stays_same_context(self) -> None:
        review = normalized((PROFILE / "review.md").read_text(encoding="utf-8"))
        lite = normalized((PROFILE / "lite-workflow.md").read_text(encoding="utf-8"))
        self.assertIn("independent read-only reviewer", review)
        self.assertIn("wait for the reviewer", review)
        self.assertIn("`non-independent`", review)
        self.assertIn("`limited-evidence`", review)
        self.assertIn("must not claim a completed repository review", review)
        self.assertIn("compact same-context review", lite)
        self.assertIn("must not upgrade lite to an independent full review", lite)

    def test_profile_never_overrides_model_or_loads_cross_profile_instructions(self) -> None:
        sources = self.profile_sources()
        body = normalized("\n".join(sources.values()))
        self.assertIn("must not pin, switch, or override the active model", body)
        self.assertIn("load only general profile modules", body)
        self.assertNotIn("profiles/claude-5", body)
        self.assertNotIn("../claude-5", body)
        self.assertNotIn("claude --model", body)
        self.assertNotIn("anthropic_model", body)
        for name, source in sources.items():
            self.assertNotRegex(source, r"(?m)^model\s*:", name)
        assert_no_affirmative_cross_profile_load(sources)

        for instruction in (
            "Load the other profile.",
            "Load the optimized profile.",
            "Follow the alternate profile.",
            "Obey the different profile.",
        ):
            with self.subTest(instruction=instruction):
                mutated = dict(sources)
                mutated["orchestration.md"] += f"\n{instruction}\n"
                with self.assertRaises(AssertionError):
                    assert_no_affirmative_cross_profile_load(mutated)
        with self.assertRaises(AssertionError):
            assert_general_load_trace(("orchestration.md", "../claude-5/review.md"))

    def test_artifact_stages_depend_on_one_complete_portable_envelope(self) -> None:
        sources = self.profile_sources()
        assert_portable_artifact_contract(sources)

        missing_field = dict(sources)
        missing_field["orchestration.md"] = missing_field["orchestration.md"].replace(
            "4. `core_version`", "4. `core`", 1
        )
        with self.assertRaises(AssertionError):
            assert_portable_artifact_contract(missing_field)

        missing_dependency = dict(sources)
        missing_dependency["review.md"] = missing_dependency["review.md"].replace(
            "Use the `portable artifact envelope` defined in `orchestration.md`",
            "Use a suitable envelope",
            1,
        )
        with self.assertRaises(AssertionError):
            assert_portable_artifact_contract(missing_dependency)

    def test_conversation_unavailable_config_sources_follow_absence_transitions(self) -> None:
        source = (PROFILE / "orchestration.md").read_text(encoding="utf-8")
        assert_conversation_config_transitions(source)

        wrong_fallback = source.replace(
            "Treat project as absent; select the valid user mode",
            "Select Full fallback without reading the user source",
            1,
        )
        with self.assertRaises(AssertionError):
            assert_conversation_config_transitions(wrong_fallback)

    def test_full_architecture_and_knowledge_routes_are_transition_complete(self) -> None:
        source = (PROFILE / "orchestration.md").read_text(encoding="utf-8")
        assert_full_orchestration_transitions(source)

        local_review_bypass = source.replace(
            "| Focused local Review finding | `review.md` | Stay in Review; do not route to architecture improvement |",
            "| Focused local Review finding | `architecture-improvement.md` | Route automatically |",
            1,
        )
        with self.assertRaises(AssertionError):
            assert_full_orchestration_transitions(local_review_bypass)

        skipped_knowledge = source.replace(
            "request joint approval for the exact displayed artifact and knowledge changes before applying them",
            "apply the knowledge changes immediately",
            1,
        )
        with self.assertRaises(AssertionError):
            assert_full_orchestration_transitions(skipped_knowledge)

    def test_every_lifecycle_write_requires_fresh_ownership_state(self) -> None:
        source = (PROFILE / "orchestration.md").read_text(encoding="utf-8")
        assert_lifecycle_write_transitions(source)

        missing_remove = source.replace(
            "install, update, or normal remove write",
            "install or update write",
            1,
        )
        with self.assertRaises(AssertionError):
            assert_lifecycle_write_transitions(missing_remove)

        stale_write = source.replace(
            "Stop without writes",
            "Continue the requested write despite changed evidence",
            1,
        )
        with self.assertRaises(AssertionError):
            assert_lifecycle_write_transitions(stale_write)

    def test_direct_architecture_diagnosis_precedes_delivery_gates(self) -> None:
        source = (PROFILE / "orchestration.md").read_text(encoding="utf-8")
        assert_full_route_precedence(source)

        delivery_first = source.replace(
            "Before the delivery first-unmet order, handle an explicit direct architecture-diagnosis request",
            "After the delivery first-unmet order, handle an explicit direct architecture-diagnosis request",
            1,
        )
        with self.assertRaises(AssertionError):
            assert_full_route_precedence(delivery_first)

        bypass_safety = source.replace(
            "must not bypass the architecture stage's own safety or approval gates",
            "may bypass the architecture stage's own safety or approval gates",
            1,
        )
        with self.assertRaises(AssertionError):
            assert_full_route_precedence(bypass_safety)


if __name__ == "__main__":
    unittest.main()

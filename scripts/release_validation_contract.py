"""Canonical validation checks required for a stable release."""

REQUIRED_VALIDATION_CHECKS = (
    "automated-tests",
    "workflow-token-proxy",
    "codex-skill-validation",
    "codex-plugin-validation",
    "codex-conformance",
    "generic-conformance",
    "codex-package-inventory",
    "generic-package-inventory",
    "reproducible-build",
    "zip-equivalence",
    "sha256-verification",
    "removed-artifact-scan",
    "release-architecture-diagnosis",
    "claude-plugin-validation",
    "claude-conformance",
    "claude-package-inventory",
)

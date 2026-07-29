# Test-Driven Implementation

## Purpose

Implement one approved ticket at a time while preserving executable evidence that tests can detect the intended behavior.

## Capability requirement

Formal completion requires `tools`. A `conversation` host MAY provide an explicitly unexecuted proposal but MUST NOT emit completed Implementation Evidence.

## Contract

- Require approved upstream artifacts and an eligible ticket.
- Preserve unrelated user changes and stay inside the ticket boundary.
- Add or identify the smallest meaningful test for approved behavior.
- Execute it and observe failure for the expected missing-behavior reason (`TDD-RED-001`).
- If it passes immediately, investigate existing behavior or test weakness rather than manufacturing failure.
- Make the smallest coherent production change that passes.
- Execute focused verification, refactor without behavior change, and execute broader checks proportional to risk.
- Never weaken acceptance criteria or tests to fit an incorrect implementation.
- Declare a test-first exception and alternative verification before editing when automated failure is not meaningful.
- Return to the earliest affected gate when implementation evidence contradicts an approved artifact.
- Record raw commands, results, changed areas, exceptions, and residual risks in Implementation Evidence.

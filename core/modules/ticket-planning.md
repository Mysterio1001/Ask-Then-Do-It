# Ticket Planning

## Purpose

Turn an approved Specification into small, dependency-aware slices that each deliver verifiable behavior.

## Contract

- Require a relevant approved Specification.
- Return to specification when planning requires new behavior or contradicts approved intent.
- Split work vertically across all necessary layers (`PLAN-VERTICAL-001`).
- Each ticket MUST define outcome, covered acceptance criteria, scope, dependencies, likely ownership areas, test-first approach, focused and broader verification, completion criteria, and parallel-safety reasoning.
- Shared enabling work SHOULD remain minimal and name its first behavioral consumer.
- Uncertain parallel safety MUST default to sequential execution.
- Emit or persist the first plan as `Draft` (`ART-STATE-001`).
- Require explicit human approval (`GATE-PLAN-001`).
- Do not authorize implementation while the Ticket Plan remains Draft or disputed.

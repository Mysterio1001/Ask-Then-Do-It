# Architecture and Refactoring Lenses

## Core lens contract

Use these twelve core lenses in the listed order for a Full Review or Architecture diagnosis:

1. **Duplicated Code or Policy**: equivalent behavior or rules maintained in multiple places.
2. **Long Function**: a function whose size or mixed responsibilities obstruct understanding, testing, or change.
3. **Large Module or Class**: a unit that owns too many responsibilities or reasons to change.
4. **Long Parameter List**: an interface whose parameters expose unstable coordination or missing concepts.
5. **Data Clumps**: related values repeatedly passed or stored together without a coherent abstraction.
6. **Primitive Obsession**: domain meaning represented primarily through unconstrained primitive values.
7. **Feature Envy**: behavior that depends more on another unit's data or responsibilities than its own.
8. **Divergent Change**: one unit repeatedly changed for unrelated reasons.
9. **Shotgun Surgery**: one behavioral change requiring edits across many locations.
10. **Message Chains**: long navigation or call chains that expose internal structure and amplify coupling.
11. **Leaky Abstraction**: callers must understand or compensate for implementation details hidden by an abstraction.
12. **Shallow Module**: a module whose interface complexity is not justified by the functionality it hides.

For every lens, record evidence and exactly one outcome:

- `finding`: evidence demonstrates a material concern. Include trigger, impact, evidence, and location when available.
- `no-finding`: available evidence supports that no material concern was found in the declared scope.
- `not-applicable`: the lens does not apply to the declared scope. Include a scope-specific reason.
- `unverified`: available evidence is insufficient. Identify the missing evidence.

Project-specific lenses MAY follow the core set but MUST NOT remove, rename incompatibly, replace, reorder, or silently skip a core lens. This contract defines the shared list and outcomes only; each consumer owns its scope, labels, findings, simulated deletion, and handoff behavior.

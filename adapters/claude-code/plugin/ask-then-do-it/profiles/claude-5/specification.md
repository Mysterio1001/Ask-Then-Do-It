# Claude 5 Specification

Core rules: GATE-SPEC-001, SPEC-NOCODE-001, ART-STATE-001

Require an Approved Requirement Decision Record or equivalent explicit consensus. If a material decision is absent or contradicted, return to requirements rather than invent it.

Create an implementation-independent behavioral Specification with the common artifact envelope and: problem; goals/non-goals; users/scenarios; required behavior; edges/failures; data, permissions, and external contracts; compatibility, rollout/recovery; constraints/assumptions; acceptance criteria; deferred decisions. Keep production implementation code out.

The first version is Draft. Request explicit approval of the exact Specification; silence or another approval does not count. Only after approval evidence exists may it become Approved and hand off to Ticket Planning. Durable-fact changes also require the documented knowledge synchronization contract. Never implement from a Draft or disputed Specification.


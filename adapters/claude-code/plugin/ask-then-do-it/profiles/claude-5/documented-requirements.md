# Claude 5 Documented Requirements

Core rules: GATE-REQ-001, GRILL-ONE-001, ART-STATE-001, KB-EVIDENCE-001, KB-DRAFT-001, KB-SYNC-001

Compose with requirement interrogation when a Project Knowledge Base exists, an existing system changes, durable knowledge is likely, or the user chooses this mode. Read the existing knowledge base and linked evidence first. Formal knowledge may come only from approved or accepted evidence; missing/conflicting facts remain unresolved.

Maintain Draft Working Notes with the common envelope and `status: Draft`. Label each discovery `proposed`, `confirmed`, or `unresolved`; even confirmed notes are not formal knowledge before approval. Continue asking exactly one recommended requirement question per turn.

At consensus, display the complete Draft Requirement Decision Record and a complete Knowledge Base Change Summary that names upstream approved or accepted evidence and separates additions, modifications, and removals. Request one joint explicit approval for exactly both displayed items. Apply only those disclosed changes when tools capability exists; conversation capability emits complete user-managed Markdown and claims no persistence. Then record approval, mark the Requirement Decision Record Approved, synchronize the approved knowledge revision, and hand off to Specification—never implementation.


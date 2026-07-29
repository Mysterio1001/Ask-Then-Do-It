# Artifact Envelope

Every logical artifact MUST include or unambiguously convey:

- `artifact_type`: one of the defined artifact types.
- `artifact_id`: a stable identifier within the workflow.
- `workflow_id`: the feature or change identifier shared across artifacts.
- `core_version`: the core contract version used to create it.
- `status`: `Draft`, `Approved`, or a type-specific evidence state.
- `inputs`: upstream artifacts or evidence.
- `assumptions`: relevant assumptions and limitations.
- `deferred`: intentionally unresolved decisions.
- `handoff`: the intended next stage and required recipient capabilities.
- `approval`: explicit approval evidence when the artifact is Approved.

Gated artifacts MUST preserve explicit Draft and Approved states (`ART-STATE-001`). Editing a status without corresponding approval evidence does not satisfy a gate.

Adapters MAY render these fields as Markdown headings, frontmatter, structured data, or host-native records when their meaning remains unambiguous.

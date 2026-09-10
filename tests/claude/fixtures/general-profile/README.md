# General instruction regression fixtures

`reviewed-instructions.json` freezes the complete ten General modules. Its initial
baseline was the production wording examined in the Ticket 4 review after the
second correction. Subsequent changes must be reviewed with their fixture diff.
The third-correction follow-up adds the canonical twelve-lens list directly to
the architecture module so direct diagnosis does not depend on unloaded Review
instructions. The snapshot is test data, not a consumer module or runtime authority.

The scenario gate compares its supplied candidate against this independent
fixture before checking scenario coverage. Only CRLF/LF differences are ignored;
case, indentation, order, trailing content, and all instructions are preserved.
Appending a contradiction anywhere, deleting a guard, or relocating instructions
therefore fails even when every old required phrase remains.

An intentional prompt edit requires reviewing its complete diff, the affected
Core rules and scenarios, and corresponding negative tests. Update this fixture
explicitly as part of that reviewed change. Tests never write it or regenerate it
from the candidate. A matching fixture establishes reviewed-text integrity, not
semantic correctness by itself: a defective candidate and a blindly refreshed
fixture could agree. Independent review is still required for fixture changes.

`scenarios.json` and the test-owned `ScenarioContract` notes map the thirty
mandatory scenario names to their instruction coverage. Their input descriptions
and expected phrases are static coverage notes, not executed model requests or
observed Claude outputs. Passing these checks is not the Specification's live
model-behavior evidence, paired equivalence, or an authenticated host test.

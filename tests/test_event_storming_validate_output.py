from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path


def load_validate_output_module():
    repo_root = Path(__file__).resolve().parent.parent
    module_path = (
        repo_root
        / "skills"
        / "event-storming"
        / "scripts"
        / "validate_output.py"
    )
    spec = importlib.util.spec_from_file_location("event_storming_validate_output", module_path)
    module = importlib.util.module_from_spec(spec)
    assert spec is not None and spec.loader is not None
    spec.loader.exec_module(module)
    return module


validate_output = load_validate_output_module()


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


class EventStormingValidateOutputTests(unittest.TestCase):
    def test_validate_file_accepts_canonical_stable_labels(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            path = Path(tmp_dir) / "big-picture.md"
            write(
                path,
                """# Big Picture EventStorming Handoff

## Format
- Big Picture EventStorming

## Objective
- Understand the renewal experience.

## Scope
- In scope: Subscription renewal.
- Out of scope: Initial acquisition.

## Source Basis
- Stakeholders: Billing operations lead.
- Documents: Renewal SOP.
- Workshop or pre-work: Document-first synthesis.

## Confidence
- Overall confidence: Medium.
- Main confidence limit: Missing support escalation detail.

## Discovery Synthesis
### Facts
- Fact: Renewal reminders are sent three days before expiry.

### Assumptions
- Assumption: Manual retries happen after failed auto-renewals.

### Open Questions
- Open question: Which team owns grace-period overrides?

### Risks
- Risk: Third-party mail delays can hide reminder failures.

### Decisions
- Decision: Model payment retries as a separate hotspot.

## Validated Narrative
- Main storyline: Renewal reminders trigger payment review before expiry.
- Key pivot or milestone: Payment failure creates a manual recovery path.

## Narrative Diagram
```mermaid
flowchart LR
  A[Renewal reminder sent] --> B[Payment reviewed]
  B --> C[Payment failed]
  C --> D[Manual follow-up started]
```

## Main Actors And Systems
- Actor: Billing operations specialist.
- System: Payment processor.

## Hot Spots And Opportunities
- Hot Spot: Grace-period overrides are inconsistently handled.
- Opportunity: Standardize retry ownership.

## Optional Custom Steps Used
- Playing with value: None identified yet.
- Problems and Opportunities: Renewal recovery is opaque.
- Arrow Voting: None identified yet.
- Extracted User Stories: None identified yet.
- Visualised ownership: Billing owns manual follow-up.

## DDD Signals
- Candidate subdomains: Billing operations.
- Language shifts: Retry versus recovery.
- Ownership tensions: Billing and support both intervene after failure.
- Candidate bounded-context seams: Payments and customer support.

## Decisions
- Decision: Carry retry ownership into Process Modelling.

## Recommended Next Step
- Process Modelling EventStorming: Model the failed-payment branch.
- Software Design EventStorming: None identified yet.
- Context-map homework: Confirm support handoff ownership.
""",
            )

            self.assertEqual(validate_output.validate_file(path), [])

    def test_validate_file_rejects_noncanonical_stable_label_casing(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            path = Path(tmp_dir) / "bad-label.md"
            write(
                path,
                """# Big Picture EventStorming Handoff

## Format
- Big Picture EventStorming

## Objective
- Understand the renewal experience.

## Scope
- In scope: Subscription renewal.
- Out of scope: Initial acquisition.

## Source Basis
- Stakeholders: Billing operations lead.
- Documents: Renewal SOP.
- Workshop or pre-work: Document-first synthesis.

## Confidence
- Overall confidence: Medium.
- Main confidence limit: Missing support escalation detail.

## Discovery Synthesis
- Open Question: Which team owns grace-period overrides?

## Validated Narrative
- Main storyline: Renewal reminders trigger payment review before expiry.
- Key pivot or milestone: Payment failure creates a manual recovery path.

## Narrative Diagram
```mermaid
flowchart LR
  A[Renewal reminder sent] --> B[Payment reviewed]
  B --> C[Payment failed]
  C --> D[Manual follow-up started]
```

## Main Actors And Systems
- Actor: Billing operations specialist.
- System: Payment processor.

## Hot Spots And Opportunities
- Hot Spot: Grace-period overrides are inconsistently handled.
- Opportunity: Standardize retry ownership.

## Optional Custom Steps Used
- Playing with value: None identified yet.
- Problems and Opportunities: Renewal recovery is opaque.
- Arrow Voting: None identified yet.
- Extracted User Stories: None identified yet.
- Visualised ownership: Billing owns manual follow-up.

## DDD Signals
- Candidate subdomains: Billing operations.
- Language shifts: Retry versus recovery.
- Ownership tensions: Billing and support both intervene after failure.
- Candidate bounded-context seams: Payments and customer support.

## Decisions
- Decision: Carry retry ownership into Process Modelling.

## Recommended Next Step
- Process Modelling EventStorming: Model the failed-payment branch.
- Software Design EventStorming: None identified yet.
- Context-map homework: Confirm support handoff ownership.
""",
            )

            self.assertIn(
                "Stable label 'Open Question:' must be written exactly as 'Open question:'.",
                validate_output.validate_file(path),
            )

    def test_validate_file_rejects_disallowed_synonyms(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            path = Path(tmp_dir) / "bad-synonyms.md"
            write(
                path,
                """# Big Picture EventStorming Handoff

## Format
- Big Picture EventStorming

## Objective
- Understand the renewal experience.

## Scope
- In scope: Subscription renewal.
- Out of scope: Initial acquisition.

## Source Basis
- Stakeholders: Billing operations lead.
- Documents: Renewal SOP.
- Workshop or pre-work: Document-first synthesis.

## Confidence
- Overall confidence: Medium.
- Main confidence limit: Missing support escalation detail.

## Discovery Synthesis
- Issue: Billing and support disagree on override ownership.
- Decision taken: Retry failures stay in billing until payment settles.

## Validated Narrative
- Main storyline: Renewal reminders trigger payment review before expiry.
- Key pivot or milestone: Payment failure creates a manual recovery path.

## Narrative Diagram
```mermaid
flowchart LR
  A[Renewal reminder sent] --> B[Payment reviewed]
  B --> C[Payment failed]
  C --> D[Manual follow-up started]
```

## Main Actors And Systems
- Actor: Billing operations specialist.
- System: Payment processor.

## Hot Spots And Opportunities
- Hot Spot: Grace-period overrides are inconsistently handled.
- Opportunity: Standardize retry ownership.

## Optional Custom Steps Used
- Playing with value: None identified yet.
- Problems and Opportunities: Renewal recovery is opaque.
- Arrow Voting: None identified yet.
- Extracted User Stories: None identified yet.
- Visualised ownership: Billing owns manual follow-up.

## DDD Signals
- Candidate subdomains: Billing operations.
- Language shifts: Retry versus recovery.
- Ownership tensions: Billing and support both intervene after failure.
- Candidate bounded-context seams: Payments and customer support.

## Decisions
- Decision: Carry retry ownership into Process Modelling.

## Recommended Next Step
- Process Modelling EventStorming: Model the failed-payment branch.
- Software Design EventStorming: None identified yet.
- Context-map homework: Confirm support handoff ownership.
""",
            )

            errors = validate_output.validate_file(path)
            self.assertIn(
                "Disallowed label 'Issue:'; use the stable label vocabulary.",
                errors,
            )
            self.assertIn(
                "Disallowed label 'Decision taken:'; use the stable label vocabulary.",
                errors,
            )

    def test_validate_file_allows_software_design_placeholder_lifecycle(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            path = Path(tmp_dir) / "software-design.md"
            write(
                path,
                """# Software Design EventStorming Handoff

## Format
- Software Design EventStorming

## Objective
- Clarify refund handling boundaries.

## Scope
- In scope: Refund approval and execution.
- Out of scope: Chargeback disputes.

## Source Basis
- Stakeholders: Finance lead, support lead.
- Documents: Refund policy.
- Workshop or pre-work: Live workshop.

## Confidence
- Overall confidence: Medium.
- Main confidence limit: Edge cases for partial refunds need review.

## Boundaries
- Boundary: Refund operations.
- Why it exists: Approval and execution rules differ from support intake.

## Boundary Diagram
```mermaid
flowchart LR
  subgraph BC1[Support Intake]
    A1[Refund requested]
  end
  subgraph BC2[Refund Operations]
    B1[Refund approved]
    B2[Refund executed]
  end
  A1 --> B1 --> B2
```

## Commands, Events, And Policies
- Command: Approve refund.
- Event: Refund executed.
- Policy: Whenever refund approval is granted, then execution starts.

## Consistency Rules
- Component or boundary: Refund operations.
- Behaviour that must stay consistent: Approval is recorded before execution.

## Aggregate Candidates
None identified yet.

## Aggregate Lifecycle
None identified yet.

## Read Models
- Read model: Refund queue.
- Decision supported: Which approved refunds are still pending execution.

## Acceptance-Test Scenarios
- Initial state: Refund is requested and eligible.
- Trigger: Finance approves the refund.
- Expected events: Refund approved, Refund executed.
- Expected outcome: Customer balance is updated.

## Context-Map Implications
- Upstream/downstream relation: Support Intake upstream of Refund Operations.
- Pattern: Customer-supplier.

## Remaining Hot Spots
- Hot Spot: Partial refund thresholds vary by region.

## Decisions
- Decision: Keep refund execution separate from support intake.
""",
            )

            self.assertEqual(validate_output.validate_file(path), [])


if __name__ == "__main__":
    unittest.main()

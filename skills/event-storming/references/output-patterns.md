# Output Patterns

Use this file when you need to produce a final document and want the output to remain consistent across runs.

## Core contract

- Output exactly one markdown document per run.
- Pick one canonical template from `deliverables.md`.
- Preserve the section order from that template.
- Do not skip required sections.
- If a section has no credible content yet, write `None identified yet.`

## Shared top block

Every final document starts with these sections in this exact order:

```md
# <Document Title>

## Format
- Big Picture EventStorming | Process Modelling EventStorming | Software Design EventStorming | Document-First EventStorming

## Objective
- ...

## Scope
- In scope:
- Out of scope:

## Source Basis
- Stakeholders:
- Documents:
- Workshop or pre-work:

## Confidence
- Overall confidence:
- Main confidence limit:
```

## Stable labels

Use these exact labels when tagging uncertain or decision-bearing content:

- `Fact`
- `Assumption`
- `Open question`
- `Risk`
- `Decision`

Do not replace them with synonyms such as `Unknown`, `Issue`, or `Resolved item`.

## Heading rules

- Use ATX markdown headings only.
- Keep top-level sections at `##`.
- Use `###` only inside cards or subsections where the canonical template already implies nesting.
- Do not add deeper heading levels unless the template explicitly needs them.

## Allowed markdown elements

- headings
- flat bullet lists
- numbered lists
- fenced code blocks
- Mermaid fenced code blocks
- short tables only when they materially reduce ambiguity

Avoid:

- nested bullets beyond one level
- long prose paragraphs when a structured list is clearer
- HTML blocks

## Mermaid by default

Use Mermaid whenever the selected template requires it. Keep diagrams simple, business-readable, and aligned to the format.

### Big Picture

- required primary diagram: `flowchart LR`
- purpose: show the validated narrative, major actors/systems, and hotspot zones

### Process Modelling

- required primary diagram: `flowchart TD`
- purpose: show the completed path, major variations, and key policy/timer steps

### Software Design

- required primary diagram: `flowchart LR` with `subgraph` boundaries
- required lifecycle diagram when a credible aggregate exists: `stateDiagram-v2`
- purpose: show boundaries, behaviour flow, and aggregate lifecycle

### Document-First

- required primary diagram: `flowchart LR`
- purpose: show the provisional narrative and confidence-limited flow

## Diagram rules

- Prefer 6-20 nodes per primary diagram.
- Use business terms, not implementation syntax, in node labels.
- Keep one primary diagram per final document mandatory.
- Add secondary diagrams only when the canonical template explicitly allows them or the complexity demands one more view.
- Do not use diagram types that add noise over clarity.
- Keep Mermaid styling minimal. Use classes only if they materially help distinguish hotspots or boundaries.

## Unknowns and placeholders

- Unknown but important: tag with `Open question` or `Risk`.
- Missing but non-critical: write `None identified yet.`
- Provisional inference from documents: tag as `Assumption`.
- Workshop conclusion or accepted modelling choice: tag as `Decision`.

## Consistency checks before finalizing

- Does the document have the shared top block?
- Does it use the correct canonical template?
- Are section titles in the expected order?
- Is the required Mermaid diagram present?
- Are uncertainty labels using the stable vocabulary?
- Are empty required sections marked consistently?

## Validator contract

- Section names are exact.
- Section order is exact.
- The placeholder text is exact: `None identified yet.`
- Mermaid fence language must be exactly `mermaid`.
- The output validator checks generated docs, not these reference files.

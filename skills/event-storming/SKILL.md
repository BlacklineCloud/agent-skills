---
name: event-storming
description: Facilitate EventStorming for domain discovery and DDD-first software design. Use when the user wants to run, structure, or summarize Big Picture EventStorming, Process Modelling EventStorming, Software Design EventStorming, or document-first EventStorming pre-work, or to produce a canonical EventStorming handoff from stakeholder input or business documents.
---

# EventStorming

Use this skill to facilitate EventStorming for domain discovery and DDD-first software design across Big Picture, Process Modelling, Software Design, and document-first pre-work. Treat `SKILL.md` as the entrypoint: choose the format, collect minimum context, load only the references needed for the chosen run, and end with one canonical markdown handoff.

## Workflow

1. Choose the format or document-first pre-work based on the user's goal and the quality of available evidence.
2. Collect minimum context:
   - business scope and target decision
   - participants or source documents
   - major actors and systems
   - main pain points, open questions, and constraints
3. Load only the reference files needed for the chosen format.
4. Model the business flow before implementation details and keep the discussion domain-first.
5. Produce one canonical markdown handoff and run `python3 scripts/validate_output.py <path-to-output>` before treating it as final.

## Guardrails

- Discovery before design.
- Use business language first.
- Write domain events in past tense.
- Model commands as intentional business actions.
- Model policies as repeatable reactions in the form `Whenever X, then Y`.
- Surface uncertainty explicitly with `Fact`, `Assumption`, `Open question`, `Risk`, and `Decision`.
- Do not jump to APIs, schemas, or implementation structure before the business flow is coherent.

## Reference Routing

- Load [facilitation-workflow.md](./references/facilitation-workflow.md) for format choice, chaining, and per-format workshop sequence.
- Load [document-first-mode.md](./references/document-first-mode.md) for extraction from business documents and next-format selection.
- Load [notation-and-modeling.md](./references/notation-and-modeling.md) for notation, grammar, DDD heuristics, and acceptance-test extraction.
- Load [deliverables.md](./references/deliverables.md) for canonical handoff templates.
- Load [output-patterns.md](./references/output-patterns.md) for markdown structure, stable labels, and output contract details.
- Load [patterns.md](./references/patterns.md) and [anti-patterns.md](./references/anti-patterns.md) for facilitation moves and recovery patterns.

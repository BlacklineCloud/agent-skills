---
name: agent-skill-release-review
description: Review a Codex, Claude Code, or agent skill/plugin before public release. Use when the user wants to assess trigger quality, folder structure, documentation, validation gaps, GitHub readiness, or OSS release quality for an agent extension.
metadata:
  maturity: public
  owner: BlacklineCloud
---

# Agent Skill Release Review

## Overview

Use this skill to review a skill or plugin before it is published publicly.
It is intended for maintainers who want a release-quality audit rather than a casual style pass.

## Review Workflow

1. Confirm the artifact type and release target.
   - Identify whether the target is a skill, plugin, or mixed repo.
   - Confirm whether the release target is Codex-only or multi-agent.
2. Inspect trigger quality and scope.
   - Check that `name` and `description` are specific, non-overlapping, and aligned with intended user requests.
   - Flag broad language that could cause false triggering or agent confusion.
3. Inspect source structure.
   - Verify required files exist and optional resources are justified.
   - Flag dead scaffolding, redundant docs, and generated files that should not be committed.
4. Inspect release readiness.
   - Check licensing, contribution docs, security policy, changelog, tests, and CI.
   - Confirm that the public README explains what is shipped today, not just what might exist later.
5. Report findings.
   - Prioritize blocking issues first, then follow-up improvements.
   - Distinguish required release blockers from non-blocking polish.

## What to Focus On

### Trigger Quality

- Is the skill description narrow enough to trigger only in the right situations?
- Is the skill name readable, stable, and consistent with folder naming?
- Would multiple skills in the same repo conflict or overlap?

### Structure and Maintainability

- Does the artifact follow the expected folder layout?
- Are `references/`, `scripts/`, and `assets/` used only when necessary?
- Are generated or local-only files excluded from source control?

### Public OSS Readiness

- Is the repository safe and comprehensible for outside contributors?
- Are release expectations, support boundaries, and security reporting clear?
- Does CI cover the actual contract that the project exposes?

## Output Expectations

- Findings first, ordered by severity.
- Include file references when possible.
- Separate:
  - release blockers
  - correctness or maintainability issues
  - optional polish
- If the artifact is ready, say so explicitly and note any residual risk.

## References

For a detailed release checklist, read [references/release-checklist.md](references/release-checklist.md).


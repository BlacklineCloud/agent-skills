# Official Creator Workflow

This repo does not own skill or plugin scaffolding. Use OpenAI's official creator skills, then use this repo's scripts for validation and isolated activation.

## Create a skill

In Codex, ask it to use the official `skill-creator` skill and write the result directly into this repo's `skills/` directory.

Example prompt:

```text
Use the official skill creator to create a skill named `my-skill` under `<repo-root>/skills`.
Only add `scripts`, `references`, or `assets` if the skill actually needs them.
```

Then run:

```bash
make check
./scripts/validate-skill my-skill
./scripts/activate-skill my-skill
./scripts/codex-dev
```

## Create a plugin

In Codex, ask it to use the official `plugin-creator` skill and write the result directly into this repo's `plugins/` directory.

Example prompt:

```text
Use the official plugin creator to create a plugin named `my-plugin` under `<repo-root>/plugins`.
Do not create or update a source marketplace entry during normal authoring.
```

Then run:

```bash
make check
./scripts/validate-plugin my-plugin
./scripts/activate-plugin my-plugin
./scripts/codex-dev
```

## Why this split exists

- The official creator skills remain the source of truth for scaffolding.
- This repo provides validation, CI, and one-item-at-a-time runtime activation.
- The generated `.agents/plugins/marketplace.json` file is only for local development and is not source content.

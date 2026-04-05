# Contributing

Thanks for contributing to `agent-skills`.

## Before You Start

- Use Python 3.11 or newer.
- Use the official OpenAI `skill-creator` and `plugin-creator` skills to scaffold new source content.
- Create skills under `skills/` and plugins under `plugins/`.
- Do not commit generated local runtime state such as `.codex-dev-home/` or `.agents/plugins/marketplace.json`.

## Local Setup

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .[dev]
```

## Development Workflow

1. Create a short-lived branch for your change. Do not commit directly to `main`.
2. Create or update a skill/plugin in place.
3. Run the full local check suite:

```bash
make check
```

4. If you are working on a specific skill or plugin, validate and activate only that item:

```bash
./scripts/validate-skill <skill-name>
./scripts/activate-skill <skill-name>
./scripts/codex-dev
```

or

```bash
./scripts/validate-plugin <plugin-name>
./scripts/activate-plugin <plugin-name>
./scripts/codex-dev
```

## Authoring Rules

- Keep skill trigger descriptions specific and non-overlapping.
- Keep `SKILL.md` lean and move heavier supporting material into `references/`.
- Use `scripts/` only for deterministic or repetitive logic.
- Do not add extra per-skill docs such as `README.md` or `CHANGELOG.md`.
- Keep plugin directory names and `.codex-plugin/plugin.json` `name` values identical.

## Pull Requests

- Open pull requests from your feature branch into protected `main`.
- Keep PRs scoped to one logical change.
- Include tests or validation updates when behavior changes.
- Update `CHANGELOG.md` for user-visible changes.
- Use draft PRs if the change is not ready for review.

## Release Notes

Maintainers use semver tags and GitHub Releases. Do not create release tags from forks or contributor branches.

# Agent Skills

`agent-skills` is a public, Codex-first repository for building, reviewing, and releasing skills and plugins for coding agents such as Codex and Claude Code.

The repository is opinionated about two things:

- source content is created with OpenAI's official `skill-creator` and `plugin-creator` workflows
- local development stays isolated so you can work on one skill or plugin at a time without confusing your active Codex session

This repository is intended to be published as `BlacklineCloud/agent-skills`.

## What This Repo Provides

- a public source-of-truth repo for agent skills and plugins
- isolated local activation so one skill or plugin can be tested at a time
- validation and CI for release readiness
- a documented maintainer workflow for shipping public OSS releases

## Layout

```text
.
├── .github/                   CI, release, code scanning, and community templates
├── docs/                      Human-facing documentation
├── skills/                    Skill source of truth
├── plugins/                   Plugin source of truth
├── scripts/                   Activation and validation tooling
├── .agents/plugins/           Generated local plugin marketplace during dev
└── .codex-dev-home/           Repo-local runtime state for Codex development
```

The repo is the source tree. The active runtime surface lives under `.codex-dev-home/` and the generated plugin marketplace lives at `.agents/plugins/marketplace.json`. Both are ignored by git.

## Requirements

- Python 3.11 or newer
- macOS or Linux for the supported local workflow
- Codex CLI for isolated runtime testing

## Public Catalog

### Skills

- `agent-skill-release-review`: review a Codex, Claude Code, or agent skill/plugin before public release, with emphasis on trigger quality, structure, OSS readiness, and GitHub release hygiene.

### Plugins

- No public plugin has been published from this repository yet.

## Quick Start

Create a new skill with the official OpenAI creator:

Use the official `skill-creator` skill and write directly to `<repo-root>/skills`.

Example prompt:

```text
Use the official skill creator to create a skill named `my-skill` under `<repo-root>/skills`.
Include `scripts` and `references` only if needed.
```

Then run:

```bash
./scripts/validate-skill my-skill
./scripts/activate-skill my-skill
./scripts/codex-dev
```

Create a new plugin with the official OpenAI creator:

Use the official `plugin-creator` skill and write directly to `<repo-root>/plugins`.

Example prompt:

```text
Use the official plugin creator to create a plugin named `my-plugin` under `<repo-root>/plugins`.
Do not create a source marketplace entry during authoring.
```

Then run:

```bash
./scripts/validate-plugin my-plugin
./scripts/activate-plugin my-plugin
./scripts/codex-dev
```

Reset the local runtime:

```bash
./scripts/deactivate-all
```

## Local Development

Set up a development environment:

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .[dev]
```

Run the full local check suite:

```bash
make check
```

Branching model:

- create a short-lived feature branch for each change
- open pull requests into protected `main`
- do not commit directly to `main`
- do not use a long-lived `develop` branch unless the project later outgrows the simpler model

## Validation

Validate one skill or plugin:

```bash
./scripts/validate-skill my-skill
./scripts/validate-plugin my-plugin
```

Validate everything:

```bash
./scripts/validate-all
```

Validate only changed skills/plugins:

```bash
./scripts/validate-changed
```

For CI pull requests, the workflow runs changed-only validation. Pushes to `main` run a full validation pass.

## Official Authoring Workflow

1. Use the official `skill-creator` or `plugin-creator` skill in Codex.
2. Target this repo's `skills/` or `plugins/` directory directly.
3. Refine the generated files in place.
4. Run the repo validator.
5. Activate only the skill or plugin you are working on.
6. Launch Codex with `./scripts/codex-dev`.

## Release Model

- protected `main` is the integration branch
- contributors work on short-lived branches and merge through pull requests
- Releases use semantic version tags such as `v0.1.0`.
- GitHub Releases are created from tag pushes after CI passes.
- Public release notes are tracked in [CHANGELOG.md](CHANGELOG.md).

## Authoring Rules

- Keep skill `name` and `description` specific enough that unrelated prompts do not trigger them.
- Keep skill frontmatter compatible with the official skill creator conventions.
- Keep `SKILL.md` lean. Move heavy details into `references/` and deterministic logic into `scripts/`.
- Keep human-facing documentation in `docs/`, not inside individual skill directories.
- Keep plugin folder names and `.codex-plugin/plugin.json` `name` values identical.
- Do not point your personal Codex runtime directly at this repo. Use the activation scripts and `./scripts/codex-dev`.

## Contributing, Security, and Support

- Contribution guide: [CONTRIBUTING.md](CONTRIBUTING.md)
- Security reporting: [SECURITY.md](SECURITY.md)
- Support expectations: [SUPPORT.md](SUPPORT.md)
- Community conduct: [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)

See [docs/conventions.md](docs/conventions.md), [docs/official-creator-workflow.md](docs/official-creator-workflow.md), and [docs/github-maintainer-setup.md](docs/github-maintainer-setup.md) for the maintainer workflow and GitHub-side release setup.

# Conventions

## Authoring

- Use OpenAI's official `skill-creator` and `plugin-creator` skills to create new source content.
- Create new skills directly under `skills/`.
- Create new plugins directly under `plugins/`.
- Do not maintain repo-local scaffolds that compete with the official creators.
- Do not add source plugins to a tracked marketplace during authoring.
- Keep public catalog entries release-ready. Example or placeholder content should not ship as published source content.

## Skills

- Store each skill under `skills/<skill-name>/`.
- Keep the folder name in kebab-case.
- Require `SKILL.md` with YAML frontmatter containing `name` and `description`.
- Keep frontmatter aligned with the official creator conventions:
  `name`, `description`, `license`, `allowed-tools`, `metadata`.
- Keep metadata narrow and domain-specific.
- Keep long references in `references/`, reusable logic in `scripts/`, and output files in `assets/`.
- Do not add `README.md`, `CHANGELOG.md`, `INSTALLATION_GUIDE.md`, or similar files inside skill directories.

## Plugins

- Store each plugin under `plugins/<plugin-name>/`.
- Keep `.codex-plugin/plugin.json` as the plugin manifest.
- Keep the plugin folder name and manifest `name` identical.
- Keep plugin skills, assets, and optional support files inside the plugin directory.
- Do not list every source plugin in a tracked marketplace file during development.

## Local Development

- Use `./scripts/activate-skill <name>` to expose only one skill to the repo-local Codex runtime.
- Use `./scripts/activate-plugin <name>` to generate a one-plugin marketplace for the active dev session.
- Use `./scripts/codex-dev` to launch Codex against `.codex-dev-home/`.
- Use `./scripts/deactivate-all` before switching contexts if you want a clean runtime state.
- Treat `.codex-dev-home/` and `.agents/plugins/marketplace.json` as generated local runtime state.

## Validation

- Run `./scripts/validate-skill <name>` or `./scripts/validate-plugin <name>` while authoring.
- Run `./scripts/validate-changed` before opening a PR.
- Run `make check` before tagging a release.
- The validators fail on missing required structure and duplicate identifiers.
- The metadata linter warns on overly broad or highly overlapping skill descriptions.
- The skill validator also enforces the official creator frontmatter shape and hyphen-case naming.

# Release Checklist

Use this checklist when reviewing a skill, plugin, or supporting repository before public release.

## Skill Review

- `SKILL.md` has valid frontmatter with a specific `name` and `description`
- Trigger language is narrow and avoids overlap with nearby skills
- `agents/openai.yaml` is present and matches the intended public presentation
- `references/`, `scripts/`, and `assets/` exist only when justified
- No redundant per-skill docs such as `README.md` or `CHANGELOG.md`

## Plugin Review

- `.codex-plugin/plugin.json` exists and is valid JSON
- Plugin folder name matches manifest `name`
- Public metadata in `interface` is complete and coherent
- Placeholder values are removed before public release

## Repository Review

- License, contribution guide, code of conduct, support policy, and security policy are present
- README explains current public contents, not future intentions only
- Changelog and release process are clear
- CI and release automation exist and are understandable
- Issue templates and PR template guide outside contributors

## GitHub Release Review

- Default branch and merge strategy are configured
- Branch protection requires review and status checks
- Code scanning, Dependabot, and private vulnerability reporting are enabled
- Release tags and GitHub Releases follow semver


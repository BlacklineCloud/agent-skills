from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from contextlib import contextmanager
from pathlib import Path
from unittest import mock

import scripts.repo_manager as repo_manager


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


@contextmanager
def patched_repo_roots(repo_root: Path):
    dev_home = repo_root / ".codex-dev-home"
    with (
        mock.patch.object(repo_manager, "REPO_ROOT", repo_root),
        mock.patch.object(repo_manager, "SKILLS_ROOT", repo_root / "skills"),
        mock.patch.object(repo_manager, "PLUGINS_ROOT", repo_root / "plugins"),
        mock.patch.object(repo_manager, "DEFAULT_DEV_HOME", dev_home),
        mock.patch.object(repo_manager, "DEV_SKILLS_ROOT", dev_home / "skills"),
        mock.patch.object(repo_manager, "DEV_PLUGINS_ROOT", dev_home / "plugins"),
        mock.patch.object(
            repo_manager,
            "GENERATED_MARKETPLACE",
            repo_root / ".agents" / "plugins" / "marketplace.json",
        ),
    ):
        yield


class RepoManagerTests(unittest.TestCase):
    def test_validate_skill_dir_accepts_nested_metadata(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            repo_root = Path(tmp_dir)
            skill_dir = repo_root / "skills" / "valid-skill"
            write(
                skill_dir / "SKILL.md",
                """---
name: valid-skill
description: Review a release-ready skill with narrow trigger guidance and useful checks.
metadata:
  owner: BlacklineCloud
---

# Valid Skill

Real body content.
""",
            )

            result = repo_manager.validate_skill_dir(skill_dir)
            self.assertTrue(result.ok, result.errors)

    def test_validate_skill_dir_rejects_invalid_frontmatter(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            skill_dir = Path(tmp_dir) / "skills" / "BadSkill"
            write(
                skill_dir / "SKILL.md",
                """---
name: BadSkill
description: <bad>
foo: bar
---

# Broken Skill

Body.
""",
            )

            result = repo_manager.validate_skill_dir(skill_dir)
            joined = "\n".join(result.errors)
            self.assertIn("unsupported frontmatter keys", joined)
            self.assertIn("hyphen-case", joined)
            self.assertIn("angle brackets", joined)

    def test_lint_skill_metadata_reports_duplicates(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            repo_root = Path(tmp_dir)
            first = repo_root / "skills" / "first-skill"
            second = repo_root / "skills" / "second-skill"
            content = """---
name: shared-skill
description: Review release readiness for a public agent skill or plugin with specific checks.
---

# Shared Skill

Body.
"""
            write(first / "SKILL.md", content)
            write(second / "SKILL.md", content.replace("shared-skill", "shared-skill"))

            result = repo_manager.lint_skill_metadata([first, second])
            joined = "\n".join(result.errors)
            self.assertIn("Duplicate skill name", joined)
            self.assertIn("Duplicate skill description", joined)

    def test_validate_plugin_dir_rejects_missing_interface_fields(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            plugin_dir = Path(tmp_dir) / "plugins" / "demo-plugin"
            write(
                plugin_dir / ".codex-plugin" / "plugin.json",
                json.dumps(
                    {
                        "name": "demo-plugin",
                        "description": "Test plugin",
                        "interface": {"displayName": "Demo Plugin"},
                    }
                ),
            )

            result = repo_manager.validate_plugin_dir(plugin_dir)
            joined = "\n".join(result.errors)
            self.assertIn("shortDescription", joined)
            self.assertIn("longDescription", joined)
            self.assertIn("developerName", joined)

    def test_activate_skill_replaces_previous_active_skill(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            repo_root = Path(tmp_dir)
            first = repo_root / "skills" / "first-skill"
            second = repo_root / "skills" / "second-skill"
            for path, name in ((first, "first-skill"), (second, "second-skill")):
                write(
                    path / "SKILL.md",
                    f"""---
name: {name}
description: Review {name} release readiness with narrow trigger guidance for maintainers.
---

# {name}

Body.
""",
                )

            with patched_repo_roots(repo_root):
                repo_manager.activate_skill("first-skill")
                repo_manager.activate_skill("second-skill")

                active_skills = sorted((repo_root / ".codex-dev-home" / "skills").iterdir())
                self.assertEqual([path.name for path in active_skills], ["second-skill"])

    def test_activate_plugin_writes_single_plugin_marketplace(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            repo_root = Path(tmp_dir)
            plugin_dir = repo_root / "plugins" / "demo-plugin"
            write(
                plugin_dir / ".codex-plugin" / "plugin.json",
                json.dumps(
                    {
                        "name": "demo-plugin",
                        "description": "Public demo plugin",
                        "interface": {
                            "displayName": "Demo Plugin",
                            "shortDescription": "Review public plugin packaging",
                            "longDescription": "A sample plugin for repo manager tests.",
                            "developerName": "BlacklineCloud",
                            "category": "Productivity",
                        },
                    }
                ),
            )

            with patched_repo_roots(repo_root):
                repo_manager.activate_plugin("demo-plugin")

                marketplace = json.loads(
                    (repo_root / ".agents" / "plugins" / "marketplace.json").read_text(
                        encoding="utf-8"
                    )
                )
                self.assertEqual(len(marketplace["plugins"]), 1)
                self.assertEqual(marketplace["plugins"][0]["name"], "demo-plugin")

    def test_validate_changed_scopes_to_changed_items_in_git_repo(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            repo_root = Path(tmp_dir)
            valid_skill = repo_root / "skills" / "valid-skill"
            broken_plugin = repo_root / "plugins" / "broken-plugin"
            write(
                valid_skill / "SKILL.md",
                """---
name: valid-skill
description: Review a public skill release with narrow scope and repository checks.
---

# Valid Skill

Body.
""",
            )
            write(
                broken_plugin / ".codex-plugin" / "plugin.json",
                json.dumps({"name": "broken-plugin", "description": "Broken"}),
            )

            subprocess.run(["git", "init"], cwd=repo_root, check=True, capture_output=True)
            subprocess.run(
                ["git", "config", "user.email", "tests@example.com"],
                cwd=repo_root,
                check=True,
                capture_output=True,
            )
            subprocess.run(
                ["git", "config", "user.name", "Repo Manager Tests"],
                cwd=repo_root,
                check=True,
                capture_output=True,
            )
            subprocess.run(["git", "add", "."], cwd=repo_root, check=True, capture_output=True)
            subprocess.run(
                ["git", "commit", "-m", "initial"],
                cwd=repo_root,
                check=True,
                capture_output=True,
            )

            valid_skill.joinpath("SKILL.md").write_text(
                """---
name: valid-skill
description: Review a public skill release with narrow scope, repository checks, and CI expectations.
---

# Valid Skill

Updated body.
""",
                encoding="utf-8",
            )

            with patched_repo_roots(repo_root):
                changed_result = repo_manager.validate_changed(None, None)
                full_result = repo_manager.validate_all()

            self.assertTrue(changed_result.ok, changed_result.errors)
            self.assertFalse(full_result.ok)


if __name__ == "__main__":
    unittest.main()


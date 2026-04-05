#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from collections.abc import Iterable
from dataclasses import dataclass, field
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_ROOT = REPO_ROOT / "skills"
PLUGINS_ROOT = REPO_ROOT / "plugins"
GENERATED_MARKETPLACE = REPO_ROOT / ".agents" / "plugins" / "marketplace.json"
DEFAULT_DEV_HOME = Path(os.environ.get("CODEX_DEV_HOME", REPO_ROOT / ".codex-dev-home"))
DEV_SKILLS_ROOT = DEFAULT_DEV_HOME / "skills"
DEV_PLUGINS_ROOT = DEFAULT_DEV_HOME / "plugins"
MAX_SKILL_NAME_LENGTH = 64
ALLOWED_SKILL_FRONTMATTER_KEYS = {
    "name",
    "description",
    "license",
    "allowed-tools",
    "metadata",
}

BLOCKED_SKILL_DOCS = {
    "README.md",
    "CHANGELOG.md",
    "INSTALLATION_GUIDE.md",
    "QUICK_REFERENCE.md",
}
GENERIC_DESCRIPTION_MARKERS = (
    "general purpose",
    "any task",
    "any request",
    "help with anything",
    "use for anything",
)
STOPWORDS = {
    "a",
    "an",
    "and",
    "as",
    "at",
    "be",
    "by",
    "for",
    "from",
    "if",
    "in",
    "into",
    "is",
    "it",
    "of",
    "on",
    "or",
    "the",
    "to",
    "use",
    "user",
    "when",
    "with",
}


@dataclass
class ValidationResult:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def extend(self, other: ValidationResult) -> None:
        self.errors.extend(other.errors)
        self.warnings.extend(other.warnings)

    @property
    def ok(self) -> bool:
        return not self.errors


@dataclass(frozen=True)
class SkillMetadata:
    folder: str
    name: str
    description: str
    path: Path


def normalize_slug(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    slug = re.sub(r"-{2,}", "-", slug)
    if not slug:
        raise SystemExit("Name must contain at least one ASCII letter or digit.")
    return slug


def strip_quotes(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


def parse_frontmatter(path: Path) -> tuple[dict[str, str], str]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError(f"{path} must start with YAML frontmatter.")

    metadata: dict[str, str] = {}
    index = 1
    while index < len(lines):
        line = lines[index]
        if line.strip() == "---":
            body = "\n".join(lines[index + 1 :]).strip()
            return metadata, body

        if line.startswith((" ", "\t")):
            raise ValueError(f"{path} has invalid frontmatter indentation at line: {line!r}")

        match = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if not match:
            raise ValueError(f"{path} has invalid frontmatter line: {line!r}")

        key, value = match.groups()
        block_lines: list[str] = []
        next_index = index + 1
        while next_index < len(lines):
            candidate = lines[next_index]
            if candidate.strip() == "---":
                break
            if candidate.startswith((" ", "\t")):
                block_lines.append(candidate.lstrip())
                next_index += 1
                continue
            break

        if value in {"|", ">"}:
            metadata[key] = "\n".join(block_lines).strip()
        elif block_lines:
            metadata[key] = strip_quotes(value) if value else "\n".join(block_lines).strip()
        else:
            metadata[key] = strip_quotes(value)

        index = next_index

    raise ValueError(f"{path} is missing the closing frontmatter delimiter.")


def load_skill_metadata(skill_dir: Path) -> SkillMetadata:
    metadata, _ = parse_frontmatter(skill_dir / "SKILL.md")
    return SkillMetadata(
        folder=skill_dir.name,
        name=metadata.get("name", "").strip(),
        description=metadata.get("description", "").strip(),
        path=skill_dir,
    )


def list_skill_dirs() -> list[Path]:
    if not SKILLS_ROOT.exists():
        return []
    return sorted(path for path in SKILLS_ROOT.iterdir() if (path / "SKILL.md").is_file())


def list_plugin_dirs() -> list[Path]:
    if not PLUGINS_ROOT.exists():
        return []
    return sorted(
        path
        for path in PLUGINS_ROOT.iterdir()
        if (path / ".codex-plugin" / "plugin.json").is_file()
    )


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def write_json(path: Path, payload: dict) -> None:
    ensure_parent(path)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def remove_path(path: Path) -> None:
    if path.is_symlink() or path.is_file():
        path.unlink()
    elif path.is_dir():
        shutil.rmtree(path)


def clear_directory(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)
    for child in path.iterdir():
        remove_path(child)


def materialize_entry(source: Path, target: Path) -> str:
    mode = os.environ.get("CODEX_ACTIVATION_MODE", "symlink").lower()
    ensure_parent(target)
    if target.exists() or target.is_symlink():
        remove_path(target)
    if mode != "copy":
        try:
            target.symlink_to(source, target_is_directory=True)
            return "symlink"
        except OSError:
            pass
    shutil.copytree(source, target)
    return "copy"


def resolve_named_dir(root: Path, value: str, expected_file: Path) -> Path:
    candidate = Path(value)
    if not candidate.is_absolute():
        candidate = (REPO_ROOT / candidate).resolve() if candidate.parts else root / value
    if candidate.is_file():
        candidate = candidate.parent
    if (candidate / expected_file).is_file():
        return candidate

    named = root / value
    if (named / expected_file).is_file():
        return named

    raise SystemExit(f"Could not resolve {value!r} under {root}.")


def validate_skill_dir(skill_dir: Path) -> ValidationResult:
    result = ValidationResult()
    skill_file = skill_dir / "SKILL.md"
    if not skill_file.is_file():
        result.errors.append(f"{skill_dir} is missing SKILL.md.")
        return result

    try:
        metadata, body = parse_frontmatter(skill_file)
    except ValueError as exc:
        result.errors.append(str(exc))
        return result

    unexpected_keys = set(metadata) - ALLOWED_SKILL_FRONTMATTER_KEYS
    if unexpected_keys:
        allowed = ", ".join(sorted(ALLOWED_SKILL_FRONTMATTER_KEYS))
        unexpected = ", ".join(sorted(unexpected_keys))
        result.errors.append(
            f"{skill_file} has unsupported frontmatter keys: {unexpected}. Allowed keys: {allowed}."
        )

    name = metadata.get("name", "").strip()
    description = metadata.get("description", "").strip()
    if not name:
        result.errors.append(f"{skill_file} is missing frontmatter field 'name'.")
    if not description:
        result.errors.append(f"{skill_file} is missing frontmatter field 'description'.")
    if not body:
        result.errors.append(f"{skill_file} has no body content.")

    if name:
        if len(name) > MAX_SKILL_NAME_LENGTH:
            result.errors.append(
                f"{skill_file} frontmatter name is too long ({len(name)} characters). "
                f"Maximum is {MAX_SKILL_NAME_LENGTH}."
            )
        if not re.fullmatch(r"[a-z0-9-]+", name):
            result.errors.append(
                f"{skill_file} frontmatter name must be hyphen-case "
                "using lowercase letters, digits, and hyphens."
            )
        if name.startswith("-") or name.endswith("-") or "--" in name:
            result.errors.append(
                f"{skill_file} frontmatter name cannot start/end "
                "with hyphen or contain consecutive hyphens."
            )

        normalized_name = normalize_slug(name)
        if normalized_name != skill_dir.name:
            result.warnings.append(
                f"{skill_dir.name}: folder name does not match "
                f"normalized skill name {normalized_name!r}."
            )

    if description and ("<" in description or ">" in description):
        result.errors.append(f"{skill_file} description cannot contain angle brackets.")
    if description and len(description) > 1024:
        result.errors.append(
            f"{skill_file} description is too long "
            f"({len(description)} characters). Maximum is 1024."
        )

    for blocked_name in BLOCKED_SKILL_DOCS:
        if (skill_dir / blocked_name).exists():
            result.errors.append(
                f"{skill_dir.name}: remove {blocked_name} "
                "from the skill directory."
            )

    return result


def validate_plugin_dir(plugin_dir: Path) -> ValidationResult:
    result = ValidationResult()
    manifest_path = plugin_dir / ".codex-plugin" / "plugin.json"
    if not manifest_path.is_file():
        result.errors.append(f"{plugin_dir} is missing .codex-plugin/plugin.json.")
        return result

    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        result.errors.append(f"{manifest_path} is not valid JSON: {exc}")
        return result

    name = str(manifest.get("name", "")).strip()
    description = str(manifest.get("description", "")).strip()
    interface = manifest.get("interface")

    if not name:
        result.errors.append(f"{manifest_path} is missing 'name'.")
    if not description:
        result.errors.append(f"{manifest_path} is missing 'description'.")
    if name and name != plugin_dir.name:
        result.errors.append(
            f"{plugin_dir.name}: plugin folder name must match manifest name {name!r}."
        )
    if not isinstance(interface, dict):
        result.errors.append(f"{manifest_path} is missing an 'interface' object.")
    else:
        for key in (
            "displayName",
            "shortDescription",
            "longDescription",
            "developerName",
            "category",
        ):
            if not str(interface.get(key, "")).strip():
                result.errors.append(f"{manifest_path} interface is missing {key!r}.")

    return result


def significant_tokens(text: str) -> set[str]:
    tokens = set(re.findall(r"[a-z0-9]+", text.lower()))
    return {token for token in tokens if token not in STOPWORDS and len(token) > 2}


def lint_skill_metadata(skill_dirs: Iterable[Path]) -> ValidationResult:
    result = ValidationResult()
    metadata_items: list[SkillMetadata] = []
    for skill_dir in skill_dirs:
        try:
            metadata_items.append(load_skill_metadata(skill_dir))
        except ValueError as exc:
            result.errors.append(str(exc))

    names: dict[str, Path] = {}
    descriptions: dict[str, Path] = {}
    for item in metadata_items:
        if not item.name or not item.description:
            continue

        if item.name in names:
            result.errors.append(
                f"Duplicate skill name {item.name!r} in {names[item.name].name} and {item.folder}."
            )
        else:
            names[item.name] = item.path

        description_key = item.description.strip().lower()
        if description_key in descriptions:
            result.errors.append(
                "Duplicate skill description in "
                f"{descriptions[description_key].name} and {item.folder}."
            )
        else:
            descriptions[description_key] = item.path

        lowered = description_key
        if len(lowered.split()) < 8:
            result.warnings.append(
                f"{item.folder}: description is very short; make trigger conditions more specific."
            )
        if any(marker in lowered for marker in GENERIC_DESCRIPTION_MARKERS):
            result.warnings.append(
                f"{item.folder}: description looks overly broad; narrow the trigger language."
            )

    for index, left in enumerate(metadata_items):
        left_tokens = significant_tokens(left.description)
        if not left_tokens:
            continue
        for right in metadata_items[index + 1 :]:
            right_tokens = significant_tokens(right.description)
            if not right_tokens:
                continue
            overlap = left_tokens & right_tokens
            if len(overlap) < 5:
                continue
            score = len(overlap) / max(len(left_tokens), len(right_tokens))
            if score >= 0.7:
                joined = ", ".join(sorted(overlap))
                result.warnings.append(
                    f"{left.folder} and {right.folder}: descriptions overlap heavily ({joined})."
                )

    return result


def render_result(result: ValidationResult) -> int:
    for warning in result.warnings:
        print(f"WARNING: {warning}")
    for error in result.errors:
        print(f"ERROR: {error}")
    if result.ok:
        print("Validation passed.")
        return 0
    return 1


def validate_all() -> ValidationResult:
    result = ValidationResult()
    skill_dirs = list_skill_dirs()
    plugin_dirs = list_plugin_dirs()

    for skill_dir in skill_dirs:
        result.extend(validate_skill_dir(skill_dir))
    result.extend(lint_skill_metadata(skill_dirs))
    for plugin_dir in plugin_dirs:
        result.extend(validate_plugin_dir(plugin_dir))
    return result


def changed_files_from_git(base: str | None, head: str | None) -> list[Path] | None:
    git_dir = REPO_ROOT / ".git"
    if not git_dir.exists():
        return None

    if base and head:
        diff_target = f"{base}...{head}"
        command = ["git", "-C", str(REPO_ROOT), "diff", "--name-only", diff_target]
    else:
        command = ["git", "-C", str(REPO_ROOT), "status", "--porcelain"]

    try:
        completed = subprocess.run(
            command,
            capture_output=True,
            check=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return None

    paths: list[Path] = []
    for line in completed.stdout.splitlines():
        if not line:
            continue
        entry = line[3:] if not (base and head) else line
        cleaned = entry.split(" -> ", 1)[-1].strip()
        if cleaned:
            paths.append(REPO_ROOT / cleaned)
    return paths


def validate_changed(base: str | None, head: str | None) -> ValidationResult:
    changed_files = changed_files_from_git(base, head)
    if changed_files is None:
        return validate_all()

    skill_dirs: set[Path] = set()
    plugin_dirs: set[Path] = set()
    for file_path in changed_files:
        try:
            relative = file_path.relative_to(REPO_ROOT)
        except ValueError:
            continue
        parts = relative.parts
        if len(parts) >= 2 and parts[0] == "skills":
            skill_dirs.add(SKILLS_ROOT / parts[1])
        if len(parts) >= 2 and parts[0] == "plugins":
            plugin_dirs.add(PLUGINS_ROOT / parts[1])

    if not skill_dirs and not plugin_dirs:
        return validate_all()

    result = ValidationResult()
    for skill_dir in sorted(skill_dirs):
        if skill_dir.exists():
            result.extend(validate_skill_dir(skill_dir))
    result.extend(lint_skill_metadata(list_skill_dirs()))
    for plugin_dir in sorted(plugin_dirs):
        if plugin_dir.exists():
            result.extend(validate_plugin_dir(plugin_dir))
    return result


def activate_skill(name_or_path: str) -> None:
    skill_dir = resolve_named_dir(SKILLS_ROOT, name_or_path, Path("SKILL.md"))
    validation = validate_skill_dir(skill_dir)
    if not validation.ok:
        raise SystemExit(render_result(validation))

    clear_directory(DEV_SKILLS_ROOT)
    mode = materialize_entry(skill_dir, DEV_SKILLS_ROOT / skill_dir.name)
    print(f"Activated skill {skill_dir.name!r} using {mode} mode at {DEV_SKILLS_ROOT}.")


def activate_plugin(name_or_path: str) -> None:
    plugin_dir = resolve_named_dir(
        PLUGINS_ROOT,
        name_or_path,
        Path(".codex-plugin/plugin.json"),
    )
    validation = validate_plugin_dir(plugin_dir)
    if not validation.ok:
        raise SystemExit(render_result(validation))

    manifest_path = plugin_dir / ".codex-plugin" / "plugin.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    category = str(manifest.get("interface", {}).get("category", "Productivity"))

    clear_directory(DEV_PLUGINS_ROOT)
    mode = materialize_entry(plugin_dir, DEV_PLUGINS_ROOT / plugin_dir.name)
    write_json(
        GENERATED_MARKETPLACE,
        {
            "name": "agent-skills-dev",
            "interface": {"displayName": "Agent Skills Dev"},
            "plugins": [
                {
                    "name": plugin_dir.name,
                    "source": {
                        "source": "local",
                        "path": f"./.codex-dev-home/plugins/{plugin_dir.name}",
                    },
                    "policy": {
                        "installation": "AVAILABLE",
                        "authentication": "ON_INSTALL",
                    },
                    "category": category,
                }
            ],
        },
    )
    print(
        f"Activated plugin {plugin_dir.name!r} using {mode} mode and wrote {GENERATED_MARKETPLACE}."
    )


def deactivate_all() -> None:
    clear_directory(DEV_SKILLS_ROOT)
    clear_directory(DEV_PLUGINS_ROOT)
    if GENERATED_MARKETPLACE.exists():
        GENERATED_MARKETPLACE.unlink()
    print("Cleared active skills, active plugins, and generated marketplace state.")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Activation and validation harness for the agent skills monorepo."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    activate_skill_parser = subparsers.add_parser(
        "activate-skill",
        help="Expose one skill to the dev runtime.",
    )
    activate_skill_parser.add_argument("name_or_path")

    activate_plugin_parser = subparsers.add_parser(
        "activate-plugin",
        help="Expose one plugin to the dev runtime and generate a local marketplace.",
    )
    activate_plugin_parser.add_argument("name_or_path")

    subparsers.add_parser("deactivate-all", help="Clear the dev runtime state.")
    subparsers.add_parser("validate-all", help="Validate every skill and plugin.")

    validate_skill_parser = subparsers.add_parser("validate-skill", help="Validate one skill.")
    validate_skill_parser.add_argument("name_or_path")

    validate_plugin_parser = subparsers.add_parser("validate-plugin", help="Validate one plugin.")
    validate_plugin_parser.add_argument("name_or_path")

    validate_changed_parser = subparsers.add_parser(
        "validate-changed",
        help="Validate only the skills/plugins touched in git.",
    )
    validate_changed_parser.add_argument("--base")
    validate_changed_parser.add_argument("--head")

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "activate-skill":
        activate_skill(args.name_or_path)
        return 0

    if args.command == "activate-plugin":
        activate_plugin(args.name_or_path)
        return 0

    if args.command == "deactivate-all":
        deactivate_all()
        return 0

    if args.command == "validate-skill":
        target = resolve_named_dir(SKILLS_ROOT, args.name_or_path, Path("SKILL.md"))
        return render_result(validate_skill_dir(target))

    if args.command == "validate-plugin":
        target = resolve_named_dir(
            PLUGINS_ROOT,
            args.name_or_path,
            Path(".codex-plugin/plugin.json"),
        )
        return render_result(validate_plugin_dir(target))

    if args.command == "validate-changed":
        return render_result(validate_changed(args.base, args.head))

    if args.command == "validate-all":
        return render_result(validate_all())

    parser.error(f"Unsupported command: {args.command}")
    return 2


if __name__ == "__main__":
    sys.exit(main())

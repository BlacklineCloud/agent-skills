#!/usr/bin/env python3
"""
Validate generated EventStorming markdown documents against the skill's
canonical output contract.
"""

from __future__ import annotations

import re
import sys
from collections.abc import Iterable
from pathlib import Path

VALID_FORMATS = {
    "Big Picture EventStorming": {
        "required_sections": [
            "Format",
            "Objective",
            "Scope",
            "Source Basis",
            "Confidence",
            "Validated Narrative",
            "Narrative Diagram",
            "Main Actors And Systems",
            "Hot Spots And Opportunities",
            "Optional Custom Steps Used",
            "DDD Signals",
            "Decisions",
            "Recommended Next Step",
        ],
        "diagram_checks": {"flowchart LR": 1},
        "forbidden_sections": {
            "Stable End State",
            "Boundary Diagram",
            "Provisional Narrative Diagram",
        },
    },
    "Process Modelling EventStorming": {
        "required_sections": [
            "Format",
            "Objective",
            "Scope",
            "Source Basis",
            "Confidence",
            "Stable End State",
            "Completed Paths",
            "Process Diagram",
            "Commands, Events, And Policies",
            "Timers, SLAs, And Variations",
            "Stakeholder And UX Concerns",
            "Addressed Hot Spots",
            "DDD Signals",
            "Decisions",
            "Recommended Next Step",
        ],
        "diagram_checks": {"flowchart TD": 1},
        "forbidden_sections": {
            "Narrative Diagram",
            "Boundary Diagram",
            "Provisional Narrative Diagram",
        },
    },
    "Software Design EventStorming": {
        "required_sections": [
            "Format",
            "Objective",
            "Scope",
            "Source Basis",
            "Confidence",
            "Boundaries",
            "Boundary Diagram",
            "Commands, Events, And Policies",
            "Consistency Rules",
            "Aggregate Candidates",
            "Aggregate Lifecycle",
            "Read Models",
            "Acceptance-Test Scenarios",
            "Context-Map Implications",
            "Remaining Hot Spots",
            "Decisions",
        ],
        "diagram_checks": {"flowchart LR": 1, "stateDiagram-v2": 1},
        "forbidden_sections": {
            "Narrative Diagram",
            "Process Diagram",
            "Provisional Narrative Diagram",
        },
    },
    "Document-First EventStorming": {
        "required_sections": [
            "Format",
            "Objective",
            "Scope",
            "Source Basis",
            "Confidence",
            "Source Inventory",
            "Provisional Narrative",
            "Provisional Narrative Diagram",
            "Candidate Commands, Events, And Policies",
            "DDD Signals",
            "High-Risk Unknowns",
            "Questions To Validate",
            "Recommended Next Official Format",
        ],
        "diagram_checks": {"flowchart LR": 1},
        "forbidden_sections": {
            "Narrative Diagram",
            "Process Diagram",
            "Boundary Diagram",
        },
    },
}

TOP_BLOCK = ["Format", "Objective", "Scope", "Source Basis", "Confidence"]
STABLE_LABELS = {"Fact", "Assumption", "Open question", "Risk", "Decision"}
DISALLOWED_LABELS = {
    "Unknown",
    "Issue",
    "Resolved item",
    "Resolved Item",
    "Question",
    "Open Question",
    "Decision taken",
}
STABLE_LABEL_LOOKUP = {label.casefold(): label for label in STABLE_LABELS}
DISALLOWED_LABEL_LOOKUP = {label.casefold(): label for label in DISALLOWED_LABELS}
NONE_TEXT = "None identified yet."
HEADER_RE = re.compile(r"^(#{1,6})\s+(.*)$", re.MULTILINE)
MERMAID_BLOCK_RE = re.compile(r"```mermaid\s*\n(.*?)\n```", re.DOTALL)
DISALLOWED_LABEL_RE = re.compile(
    r"^\s*[-*]?\s*([A-Za-z][A-Za-z ]+):(?!/)(?:\s+.*)?$", re.MULTILINE
)


def iter_markdown_files(path: Path) -> Iterable[Path]:
    if path.is_file():
        if path.suffix.lower() != ".md":
            raise ValueError(f"Not a markdown file: {path}")
        yield path
        return

    if path.is_dir():
        for child in sorted(path.rglob("*.md")):
            if child.is_file():
                yield child
        return

    raise ValueError(f"Path does not exist: {path}")


def collect_h2_sections(text: str) -> list[tuple[str, int]]:
    sections: list[tuple[str, int]] = []
    for match in HEADER_RE.finditer(text):
        level = len(match.group(1))
        title = match.group(2).strip()
        if level == 2:
            sections.append((title, match.start()))
    return sections


def section_body(text: str, sections: list[tuple[str, int]], title: str) -> str:
    for index, (current, start) in enumerate(sections):
        if current != title:
            continue
        end = len(text)
        if index + 1 < len(sections):
            end = sections[index + 1][1]
        header_line_end = text.find("\n", start)
        if header_line_end == -1:
            return ""
        return text[header_line_end + 1 : end].strip()
    return ""


def validate_title(text: str, errors: list[str]) -> None:
    first_nonempty = next((line.strip() for line in text.splitlines() if line.strip()), "")
    if not first_nonempty.startswith("# "):
        errors.append("Missing document title as the first non-empty line.")


def parse_format(text: str, sections: list[tuple[str, int]], errors: list[str]) -> str | None:
    body = section_body(text, sections, "Format")
    if not body:
        errors.append("Missing content under '## Format'.")
        return None
    first_line = next((line.strip() for line in body.splitlines() if line.strip()), "")
    if not first_line.startswith("- "):
        errors.append("Format section must start with a bullet line.")
        return None
    value = first_line[2:].strip()
    if value not in VALID_FORMATS:
        errors.append(f"Invalid format value: '{value}'.")
        return None
    return value


def validate_section_order(
    sections: list[tuple[str, int]], expected: list[str], errors: list[str]
) -> None:
    titles = [title for title, _ in sections]
    cursor = 0
    for title in expected:
        if title not in titles:
            errors.append(f"Missing required section '## {title}'.")
            continue
        position = titles.index(title)
        if position < cursor:
            errors.append(f"Section '## {title}' is out of order.")
            continue
        cursor = position + 1


def validate_required_bodies(
    text: str, sections: list[tuple[str, int]], required: list[str], errors: list[str]
) -> None:
    titles = {title for title, _ in sections}
    for title in required:
        if title not in titles:
            continue
        body = section_body(text, sections, title)
        if not body:
            errors.append(f"Section '## {title}' is empty.")


def validate_mermaid_fences(text: str, errors: list[str]) -> list[str]:
    blocks = MERMAID_BLOCK_RE.findall(text)
    if not blocks:
        errors.append("Missing Mermaid diagram block.")
        return []
    return blocks


def software_design_lifecycle_optional(text: str, sections: list[tuple[str, int]]) -> bool:
    aggregate_body = section_body(text, sections, "Aggregate Candidates")
    lifecycle_body = section_body(text, sections, "Aggregate Lifecycle")
    return aggregate_body == NONE_TEXT and lifecycle_body == NONE_TEXT


def validate_diagrams(
    format_name: str,
    text: str,
    sections: list[tuple[str, int]],
    blocks: list[str],
    errors: list[str],
) -> None:
    expected = VALID_FORMATS[format_name]["diagram_checks"]
    contents = "\n".join(blocks)

    for diagram_type, minimum in expected.items():
        if (
            format_name == "Software Design EventStorming"
            and diagram_type == "stateDiagram-v2"
            and software_design_lifecycle_optional(text, sections)
        ):
            continue

        count = contents.count(diagram_type)
        if count < minimum:
            errors.append(
                f"Missing required Mermaid diagram type '{diagram_type}' for {format_name}."
            )


def validate_labels(text: str, errors: list[str]) -> None:
    for match in DISALLOWED_LABEL_RE.finditer(text):
        label = match.group(1).strip()
        if label in STABLE_LABELS:
            continue

        canonical = STABLE_LABEL_LOOKUP.get(label.casefold())
        if canonical is not None and label != canonical:
            errors.append(f"Stable label '{label}:' must be written exactly as '{canonical}:'.")
            continue

        if label.casefold() in DISALLOWED_LABEL_LOOKUP:
            errors.append(f"Disallowed label '{label}:'; use the stable label vocabulary.")


def validate_forbidden_sections(
    sections: list[tuple[str, int]], format_name: str, errors: list[str]
) -> None:
    titles = {title for title, _ in sections}
    for forbidden in VALID_FORMATS[format_name]["forbidden_sections"]:
        if forbidden in titles:
            errors.append(
                f"Section '## {forbidden}' conflicts with declared format '{format_name}'."
            )


def validate_none_text(text: str, errors: list[str]) -> None:
    if "None identified yet" in text and NONE_TEXT not in text:
        errors.append("Placeholder text must be exactly 'None identified yet.'")


def validate_file(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []

    validate_title(text, errors)
    sections = collect_h2_sections(text)
    validate_section_order(sections, TOP_BLOCK, errors)

    format_name = parse_format(text, sections, errors)
    if format_name is None:
        return errors

    required_sections = VALID_FORMATS[format_name]["required_sections"]
    validate_section_order(sections, required_sections, errors)
    validate_required_bodies(text, sections, required_sections, errors)
    blocks = validate_mermaid_fences(text, errors)
    validate_diagrams(format_name, text, sections, blocks, errors)
    validate_labels(text, errors)
    validate_forbidden_sections(sections, format_name, errors)
    validate_none_text(text, errors)

    return list(dict.fromkeys(errors))


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("Usage: python3 scripts/validate_output.py <path>")
        return 1

    root = Path(argv[1]).resolve()
    try:
        files = list(iter_markdown_files(root))
    except ValueError as exc:
        print(f"FAIL {exc}")
        return 1

    if not files:
        print(f"FAIL No markdown files found under {root}")
        return 1

    failures = 0
    for path in files:
        errors = validate_file(path)
        if errors:
            failures += 1
            print(f"FAIL {path}")
            for error in errors:
                print(f"  - {error}")
        else:
            print(f"PASS {path}")

    print(
        f"Checked {len(files)} file(s); {failures} failure(s)."
    )
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

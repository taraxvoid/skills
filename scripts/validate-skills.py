#!/usr/bin/env python3
"""
validate-skills.py — Local validation for the taraxvoid-claude-skills repo.

Run directly:
    python3 scripts/validate-skills.py

Or via git hook (see hooks/pre-commit):
    git config core.hooksPath hooks

Checks performed:
  1. JSON validity        — all .json files parse without error
  2. marketplace.json     — required top-level fields present
  3. plugin.json schemas  — each plugin.json has name, version, description
  4. Cross-references     — marketplace.json <-> skills/<name>/ <-> SKILL.md <-> plugin.json
  5. Frontmatter          — SKILL.md has valid frontmatter with matching name
  6. Markdown hygiene     — no trailing whitespace, files end with newline

Exit codes: 0 = pass, 1 = fail
"""

import json
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parent.parent

MARKETPLACE_PATH = REPO_ROOT / ".claude-plugin" / "marketplace.json"
SKILLS_DIR = REPO_ROOT / "skills"

MARKETPLACE_REQUIRED_FIELDS = {"name", "description", "plugins"}
PLUGIN_REQUIRED_FIELDS = {"name", "description", "version"}
FRONTMATTER_REQUIRED_KEYS = {"name", "description"}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def parse_frontmatter(content):
    """Parse simple YAML frontmatter (key: value pairs between --- markers).

    Returns a dict, or None if no valid frontmatter block is found.
    """
    if not content.startswith("---\n"):
        return None

    lines = content.split("\n")
    # lines[0] is "---"
    fm_lines = []
    for line in lines[1:]:
        if line.strip() == "---":
            break
        fm_lines.append(line)
    else:
        return None  # no closing ---

    result = {}
    for line in fm_lines:
        if ":" in line:
            key, _, value = line.partition(":")
            key = key.strip()
            value = value.strip()
            # Strip surrounding quotes
            if len(value) >= 2 and value[0] == value[-1] and value[0] in ('"', "'"):
                value = value[1:-1]
            if key:
                result[key] = value
    return result


def iter_json_files(root):
    """Yield all .json files under root, skipping .git/ and node_modules/."""
    for p in root.rglob("*.json"):
        parts = p.parts
        if ".git" in parts or "node_modules" in parts:
            continue
        yield p


def iter_markdown_files(root):
    """Yield all .md files under root, skipping .git/ and node_modules/."""
    for p in root.rglob("*.md"):
        parts = p.parts
        if ".git" in parts or "node_modules" in parts:
            continue
        yield p


# ---------------------------------------------------------------------------
# Checks — each returns a list of error strings (empty = pass)
# ---------------------------------------------------------------------------

def check_json_validity():
    """Check 1: All .json files are valid JSON."""
    errors = []
    count = 0
    for json_file in iter_json_files(REPO_ROOT):
        count += 1
        try:
            with open(json_file, encoding="utf-8") as f:
                json.load(f)
        except json.JSONDecodeError as e:
            rel = json_file.relative_to(REPO_ROOT)
            errors.append(f"{rel}: {e}")
    return errors, f"{count} files"


def check_marketplace_schema():
    """Check 2: marketplace.json has required top-level fields."""
    errors = []
    if not MARKETPLACE_PATH.exists():
        errors.append(f"{MARKETPLACE_PATH.relative_to(REPO_ROOT)}: file not found")
        return errors, "schema"

    try:
        with open(MARKETPLACE_PATH, encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        errors.append(f"marketplace.json: invalid JSON — {e}")
        return errors, "schema"

    for field in MARKETPLACE_REQUIRED_FIELDS:
        if field not in data:
            errors.append(f"marketplace.json: missing required field '{field}'")

    if "plugins" in data:
        if not isinstance(data["plugins"], list):
            errors.append("marketplace.json: 'plugins' must be an array")
        else:
            for i, plugin in enumerate(data["plugins"]):
                if not isinstance(plugin, dict):
                    errors.append(f"marketplace.json: plugins[{i}] must be an object")
                    continue
                for field in ("name", "source"):
                    if field not in plugin:
                        errors.append(
                            f"marketplace.json: plugins[{i}] missing '{field}'"
                        )

    return errors, "schema"


def check_plugin_schemas():
    """Check 3: Each plugin.json has required fields."""
    errors = []
    count = 0
    for plugin_json in REPO_ROOT.rglob(".claude-plugin/plugin.json"):
        parts = plugin_json.parts
        if ".git" in parts:
            continue
        count += 1
        try:
            with open(plugin_json, encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            rel = plugin_json.relative_to(REPO_ROOT)
            errors.append(f"{rel}: invalid JSON — {e}")
            continue
        for field in PLUGIN_REQUIRED_FIELDS:
            if field not in data:
                rel = plugin_json.relative_to(REPO_ROOT)
                errors.append(f"{rel}: missing required field '{field}'")

    return errors, f"{count} files"


def check_cross_references():
    """Check 4: marketplace.json <-> skills/ <-> SKILL.md <-> plugin.json."""
    errors = []

    if not MARKETPLACE_PATH.exists():
        errors.append("marketplace.json: file not found")
        return errors, "integrity"

    try:
        with open(MARKETPLACE_PATH, encoding="utf-8") as f:
            marketplace = json.load(f)
    except json.JSONDecodeError as e:
        errors.append(f"marketplace.json: invalid JSON — {e}")
        return errors, "integrity"

    plugins = marketplace.get("plugins", [])
    marketplace_names = set()

    for i, plugin in enumerate(plugins):
        name = plugin.get("name", f"plugins[{i}]")
        source = plugin.get("source", "")
        marketplace_names.add(name)

        # Check source path format
        expected_source = f"./skills/{name}"
        if source != expected_source:
            errors.append(
                f"marketplace.json: plugin '{name}' has source '{source}', "
                f"expected '{expected_source}'"
            )

        # Check skill directory exists
        skill_dir = SKILLS_DIR / name
        if not skill_dir.is_dir():
            errors.append(
                f"marketplace.json: plugin '{name}' — skills/{name}/ directory not found"
            )
            continue

        # Check SKILL.md exists
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            errors.append(f"skills/{name}/: SKILL.md not found")

        # Check plugin.json exists and name matches
        plugin_json = skill_dir / ".claude-plugin" / "plugin.json"
        if not plugin_json.exists():
            errors.append(f"skills/{name}/: .claude-plugin/plugin.json not found")
        else:
            try:
                with open(plugin_json, encoding="utf-8") as f:
                    plugin_data = json.load(f)
            except json.JSONDecodeError as e:
                errors.append(
                    f"skills/{name}/.claude-plugin/plugin.json: invalid JSON — {e}"
                )
                continue
            plugin_name = plugin_data.get("name", "")
            if plugin_name != name:
                errors.append(
                    f"skills/{name}/.claude-plugin/plugin.json: name '{plugin_name}' "
                    f"does not match marketplace '{name}'"
                )

    # Check for orphan skill directories (in skills/ but not in marketplace)
    if SKILLS_DIR.is_dir():
        for entry in sorted(SKILLS_DIR.iterdir()):
            if entry.is_dir() and entry.name not in marketplace_names:
                errors.append(
                    f"skills/{entry.name}/: directory not listed in marketplace.json"
                )

    return errors, "integrity"


def check_frontmatter():
    """Check 5: SKILL.md files have valid frontmatter with matching name."""
    errors = []
    count = 0

    for skill_md in iter_markdown_files(REPO_ROOT):
        if skill_md.name != "SKILL.md":
            continue
        count += 1
        rel = skill_md.relative_to(REPO_ROOT)

        content = skill_md.read_text(encoding="utf-8")
        fm = parse_frontmatter(content)

        if fm is None:
            errors.append(f"{rel}: missing or invalid YAML frontmatter")
            continue

        for key in FRONTMATTER_REQUIRED_KEYS:
            if key not in fm:
                errors.append(f"{rel}: frontmatter missing '{key}'")
            elif not fm[key]:
                errors.append(f"{rel}: frontmatter '{key}' is empty")

        # Check that frontmatter name matches directory name
        dir_name = skill_md.parent.name
        fm_name = fm.get("name", "")
        if fm_name and fm_name != dir_name:
            errors.append(
                f"{rel}: frontmatter name '{fm_name}' does not match "
                f"directory name '{dir_name}'"
            )

    return errors, f"{count} files"


def check_markdown_hygiene():
    """Check 6: No trailing whitespace, files end with newline."""
    errors = []
    count = 0

    for md_file in iter_markdown_files(REPO_ROOT):
        count += 1
        rel = md_file.relative_to(REPO_ROOT)
        content = md_file.read_text(encoding="utf-8")

        # Check final newline
        if content and not content.endswith("\n"):
            errors.append(f"{rel}: missing final newline")

        # Check trailing whitespace
        for i, line in enumerate(content.split("\n"), 1):
            if line != line.rstrip():
                errors.append(f"{rel}:{i}: trailing whitespace")

    return errors, f"{count} files"


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

CHECKS = [
    ("JSON validity", check_json_validity),
    ("marketplace.json schema", check_marketplace_schema),
    ("plugin.json schemas", check_plugin_schemas),
    ("cross-reference integrity", check_cross_references),
    ("frontmatter", check_frontmatter),
    ("markdown hygiene", check_markdown_hygiene),
]


def main():
    all_errors = []
    passed = 0
    failed = 0

    for name, check_fn in CHECKS:
        try:
            errors, detail = check_fn()
        except Exception as e:
            errors = [f"unexpected error: {e}"]
            detail = "error"

        if errors:
            failed += 1
            all_errors.extend(errors)
            print(f"✗ {name} ({detail})")
            for err in errors:
                print(f"  {err}")
        else:
            passed += 1
            print(f"✓ {name} ({detail})")

    print()
    if failed:
        print(f"{failed} check(s) failed, {passed} passed.")
        sys.exit(1)
    else:
        print(f"All {passed} checks passed.")
        sys.exit(0)


if __name__ == "__main__":
    main()

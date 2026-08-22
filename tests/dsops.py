"""Shared helpers for the design-system-ops test suite.

Stdlib only — the repo ships markdown, not code, so the tests must run
anywhere `python3` exists with nothing installed.
"""

import json
import os
import re

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SKILLS_DIR = os.path.join(REPO_ROOT, "skills")
COMMANDS_DIR = os.path.join(REPO_ROOT, "commands")
KNOWLEDGE_DIR = os.path.join(REPO_ROOT, "knowledge-notes")
PLUGIN_JSON = os.path.join(REPO_ROOT, ".claude-plugin", "plugin.json")

_FRONTMATTER = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)
_KEY = re.compile(r"^([A-Za-z_][A-Za-z0-9_-]*):\s*(.*)$")
_ITEM = re.compile(r"^\s+-\s+(.*)$")


class FrontmatterError(Exception):
    pass


def _unquote(value):
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    return value


def parse_frontmatter(text):
    """Parse the leading YAML frontmatter block.

    Supports the only two shapes this repo uses: `key: value` and a `key:`
    followed by an indented `- item` list. Anything else is an error rather
    than a silent skip, so a malformed block fails a test instead of passing
    as an empty dict.
    """
    match = _FRONTMATTER.match(text)
    if not match:
        raise FrontmatterError("no `---` frontmatter block at the top of the file")

    data = {}
    current_list = None
    for lineno, line in enumerate(match.group(1).split("\n"), start=2):
        if not line.strip() or line.lstrip().startswith("#"):
            continue

        item = _ITEM.match(line)
        if item:
            if current_list is None:
                raise FrontmatterError("line %d: list item with no preceding key" % lineno)
            current_list.append(_unquote(item.group(1)))
            continue

        key = _KEY.match(line)
        if not key:
            raise FrontmatterError("line %d: cannot parse %r" % (lineno, line))

        name, value = key.group(1), key.group(2).strip()
        if name in data:
            raise FrontmatterError("line %d: duplicate key %r" % (lineno, name))
        if value:
            data[name] = _unquote(value)
            current_list = None
        else:
            current_list = data[name] = []

    return data


def read_text(path):
    with open(path, encoding="utf-8") as handle:
        return handle.read()


def load_document(path):
    """Return (frontmatter_dict, body_text) for a markdown file."""
    text = read_text(path)
    data = parse_frontmatter(text)
    body = _FRONTMATTER.sub("", text, count=1)
    return data, body


def load_plugin_manifest():
    return json.loads(read_text(PLUGIN_JSON))


def skill_dirs():
    """Every `skills/<name>/` directory, sorted."""
    return sorted(
        os.path.join(SKILLS_DIR, entry)
        for entry in os.listdir(SKILLS_DIR)
        if os.path.isdir(os.path.join(SKILLS_DIR, entry))
    )


def skill_files():
    """Every `skills/<name>/SKILL.md`, sorted. Missing ones are surfaced by
    test_skills.test_every_skill_dir_has_a_skill_md, not hidden here."""
    return [
        os.path.join(d, "SKILL.md")
        for d in skill_dirs()
        if os.path.isfile(os.path.join(d, "SKILL.md"))
    ]


def agent_files():
    """The top-level `skills/*.md` chained-agent definitions."""
    return sorted(
        os.path.join(SKILLS_DIR, entry)
        for entry in os.listdir(SKILLS_DIR)
        if entry.endswith(".md") and os.path.isfile(os.path.join(SKILLS_DIR, entry))
    )


def command_files():
    return sorted(
        os.path.join(COMMANDS_DIR, entry)
        for entry in os.listdir(COMMANDS_DIR)
        if entry.endswith(".md")
    )


def rel(path):
    return os.path.relpath(path, REPO_ROOT)

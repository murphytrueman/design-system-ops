"""Two contracts that break silently when one side changes and the other
doesn't:

- A skill reads a `.ds-ops-config.yml` key that the annotated template never
  documents, so no user ever sets it.
- A skill tells the model to run a shell command that the slash command
  loading it doesn't pre-approve, so a headless or Cowork run stalls on a
  permission prompt or is denied outright."""

import os
import re
import unittest

import dsops

CONFIG = os.path.join(dsops.REPO_ROOT, "ds-ops-config.example.yml")
CONFIG_KEY = re.compile(r"^( *)([A-Za-z_][\w-]*):")
CONFIG_SECTION = re.compile(r"(?ms)^## Configuration[^\n]*\n(.*?)(?=^## |\Z)")
YAML_BLOCK = re.compile(r"(?ms)^[ \t]*```ya?ml\n(.*?)^[ \t]*```")
DOTTED_KEY = re.compile(r"`([a-z_]+(?:\.[\w*-]+)+)(?::[^`]*)?`")
FILE_SUFFIXES = (".md", ".yml", ".yaml", ".json", ".js", ".ts", ".css")


def config_paths():
    """Every dotted key path in the example config, from its indentation."""
    paths, stack = set(), []
    for line in dsops.read_text(CONFIG).splitlines():
        match = CONFIG_KEY.match(line.split("#", 1)[0].rstrip())
        if match:
            stack = stack[: len(match.group(1)) // 2] + [match.group(2)]
            paths.add(".".join(stack))
    return paths


def keys_read_by(text, tops):
    # Backticked keys, optionally with a value: `recurring.enabled: true`
    pattern = re.compile(r"`((?:%s)(?:\.[\w*-]+)+)(?::[^`]*)?`" % "|".join(tops))
    return set(pattern.findall(text))


class TestConfigKeys(unittest.TestCase):
    def test_config_was_parsed(self):
        paths = config_paths()
        self.assertIn("system.framework", paths)
        self.assertIn("integrations.github.repo", paths)

    def test_every_key_a_skill_reads_is_documented(self):
        paths = config_paths()
        tops = sorted(p for p in paths if "." not in p)
        config_text = dsops.read_text(CONFIG)
        for path in dsops.skill_files() + dsops.agent_files() + dsops.command_files():
            for key in keys_read_by(dsops.read_text(path), tops):
                with self.subTest(file=dsops.rel(path), key=key):
                    if key.endswith(".*"):
                        # A whole section, e.g. `recurring.*`.
                        self.assertIn(key[:-2], paths, "section not in the template")
                    elif key.endswith("*"):
                        # A prefix override such as `severity.api_*` must be
                        # named in the template's comments.
                        self.assertIn(key, config_text, "prefix key not documented")
                    else:
                        self.assertIn(
                            key,
                            paths,
                            "skill reads a key ds-ops-config.example.yml doesn't document",
                        )

    def test_configuration_sections_only_use_documented_keys(self):
        # The check above only sees keys under sections the template already
        # has, so a skill inventing a whole new section would slip past it.
        # A skill's Configuration section is where it declares what it reads:
        # every key there, in a backticked list or a YAML block, must exist.
        paths = config_paths()
        for path in dsops.skill_files():
            for section in CONFIG_SECTION.findall(dsops.read_text(path)):
                keys = set()
                for block in YAML_BLOCK.findall(section):
                    stack = []
                    for line in block.splitlines():
                        match = CONFIG_KEY.match(line.split("#", 1)[0].rstrip())
                        if match:
                            stack = stack[: len(match.group(1)) // 2] + [match.group(2)]
                            keys.add(".".join(stack))
                for key in DOTTED_KEY.findall(section):
                    if "/" not in key and not key.endswith(FILE_SUFFIXES):
                        keys.add(key)
                for key in sorted(keys):
                    with self.subTest(file=dsops.rel(path), key=key):
                        if key.endswith(".*"):
                            self.assertIn(key[:-2], paths)
                        elif key.endswith("*"):
                            self.assertIn(key, dsops.read_text(CONFIG))
                        else:
                            self.assertIn(key, paths, "document this key in ds-ops-config.example.yml")

    def test_the_section_check_sees_a_new_section(self):
        section = CONFIG_SECTION.findall("## Configuration\n\n```yaml\nmade_up:\n  key: 1\n```\n\n## Next\n")
        self.assertEqual(1, len(section))
        self.assertIn("made_up:", YAML_BLOCK.findall(section[0])[0])
        self.assertNotIn("made_up", config_paths())

    def test_the_check_catches_an_undocumented_key(self):
        tops = sorted(p for p in config_paths() if "." not in p)
        found = keys_read_by("If `system.made_up_key: true` is set", tops)
        self.assertEqual({"system.made_up_key"}, found)
        self.assertNotIn("system.made_up_key", config_paths())


PLUGIN_ROOT_PATH = re.compile(r"\$\{CLAUDE_PLUGIN_ROOT\}/([^\s)`,\"']*)")

# Shell commands a skill may tell the model to run, matched as prefixes.
SHELL = ("git log", "git blame", "git ls-files", "git diff", "git show",
         "npx", "npm view", "npm pack", "rg", "gh api", "jq")

# Left to prompt the user on purpose: `gh api` can write to GitHub with the
# user's credentials, so pre-approving it would approve writes too.
PROMPT_BY_DESIGN = ("gh api",)

# How agents name the skills they chain.
CHAINED = [
    re.compile(r"(?m)^#{3,4} Step [^\n]*\(`([a-z0-9-]+)`\)"),
    re.compile(r"(?m)^(?:- \*\*[^*]+\*\* — )?[Rr]un `([a-z0-9-]+)`"),
    re.compile(r"`([a-z0-9-]+)` runs only when"),
]

SHELL_BLOCK = re.compile(r"(?ms)^[ \t]*```(?:bash|sh|shell)\n(.*?)^[ \t]*```")


def chained_skills(agent_text):
    names = {os.path.basename(d) for d in dsops.skill_dirs()}
    found = set()
    for pattern in CHAINED:
        found |= set(pattern.findall(agent_text)) & names
    return found


def files_loaded_by(command_path):
    loaded = set()
    for rel in PLUGIN_ROOT_PATH.findall(dsops.read_text(command_path)):
        target = os.path.join(dsops.REPO_ROOT, rel.rstrip("."))
        if not os.path.isfile(target) or "/knowledge-notes/" in target:
            continue
        loaded.add(target)
        if target.endswith("-agent.md"):
            for name in chained_skills(dsops.read_text(target)):
                loaded.add(os.path.join(dsops.SKILLS_DIR, name, "SKILL.md"))
    return loaded


def shell_invocations(text):
    # The self-check block mentions `npx skills install` as a cause, not a step.
    text = text.replace(dsops.REFERENCE_CHECK_BLOCK, "")
    spans = re.findall(r"`([^`\n]+)`", text)
    for block in SHELL_BLOCK.findall(text):
        spans += block.splitlines()
    for span in spans:
        span = span.strip().lstrip("$").strip()
        for command in SHELL:
            if span == command or span.startswith(command + " "):
                yield span


def approved_prefixes(command_path):
    tools = dsops.load_document(command_path)[0]["allowed-tools"]
    return re.findall(r"Bash\(([^:)]+):\*\)", tools)


class TestCommandTools(unittest.TestCase):
    def test_agents_chain_skills_the_parser_can_see(self):
        for path in dsops.agent_files():
            with self.subTest(agent=dsops.rel(path)):
                self.assertGreaterEqual(len(chained_skills(dsops.read_text(path))), 2)

    def test_commands_approve_the_shell_commands_their_skills_run(self):
        for command in dsops.command_files():
            approved = approved_prefixes(command)
            for loaded in sorted(files_loaded_by(command)):
                for run in shell_invocations(dsops.read_text(loaded)):
                    if run.startswith(PROMPT_BY_DESIGN):
                        continue
                    with self.subTest(command=dsops.rel(command), file=dsops.rel(loaded), run=run[:60]):
                        self.assertTrue(
                            any(run == a or run.startswith(a + " ") for a in approved),
                            "add a narrow Bash(<command>:*) entry to allowed-tools",
                        )

    def test_the_check_catches_an_unapproved_command(self):
        runs = list(shell_invocations("Run `git log -1 --format=%cI -- src/Button.tsx`."))
        self.assertEqual(1, len(runs))
        self.assertFalse(any(runs[0].startswith(a + " ") for a in ("git ls-files",)))
        self.assertEqual([], list(shell_invocations(dsops.REFERENCE_CHECK_BLOCK)))


if __name__ == "__main__":
    unittest.main()

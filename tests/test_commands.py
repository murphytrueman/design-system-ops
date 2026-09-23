"""Slash commands are the user-facing entry points. Each one must have a
description (it is what `/help` lists) and every ${CLAUDE_PLUGIN_ROOT} path it
tells Claude to load must exist in the bundle."""

import os
import re
import unittest

import dsops

PLUGIN_ROOT_PATH = re.compile(r"\$\{CLAUDE_PLUGIN_ROOT\}(/[^\s)`,\"']*)")


def _resolve(plugin_relative):
    # Trailing punctuation from prose, e.g. ".../knowledge-notes/."
    cleaned = plugin_relative.rstrip(".")
    return os.path.join(dsops.REPO_ROOT, cleaned.lstrip("/"))


class TestCommandFrontmatter(unittest.TestCase):
    def test_repo_has_commands(self):
        self.assertGreater(len(dsops.command_files()), 0, "no commands found")

    def test_frontmatter_parses(self):
        for path in dsops.command_files():
            with self.subTest(command=dsops.rel(path)):
                dsops.load_document(path)

    def test_description_present(self):
        for path in dsops.command_files():
            with self.subTest(command=dsops.rel(path)):
                data, _ = dsops.load_document(path)
                self.assertIn("description", data)
                self.assertTrue(str(data["description"]).strip())

    def test_allowed_tools_present_and_non_empty(self):
        for path in dsops.command_files():
            with self.subTest(command=dsops.rel(path)):
                data, _ = dsops.load_document(path)
                self.assertIn("allowed-tools", data)
                self.assertTrue(str(data["allowed-tools"]).strip())

    def test_body_is_not_empty(self):
        for path in dsops.command_files():
            with self.subTest(command=dsops.rel(path)):
                _, body = dsops.load_document(path)
                self.assertGreater(len(body.strip()), 50, "command body is a stub")


class TestCommandTargets(unittest.TestCase):
    def test_plugin_root_paths_resolve(self):
        for path in dsops.command_files():
            _, body = dsops.load_document(path)
            for match in PLUGIN_ROOT_PATH.findall(body):
                with self.subTest(command=dsops.rel(path), target=match):
                    self.assertTrue(
                        os.path.exists(_resolve(match)),
                        "${CLAUDE_PLUGIN_ROOT}%s does not exist" % match,
                    )

    def test_every_command_loads_at_least_one_skill(self):
        for path in dsops.command_files():
            with self.subTest(command=dsops.rel(path)):
                _, body = dsops.load_document(path)
                targets = [
                    t for t in PLUGIN_ROOT_PATH.findall(body) if t.startswith("/skills/")
                ]
                self.assertTrue(targets, "command references no skill file")


if __name__ == "__main__":
    unittest.main()

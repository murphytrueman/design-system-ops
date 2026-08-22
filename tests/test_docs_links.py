"""Relative links in the shipped documentation must resolve. These docs are
read inside the plugin bundle as well as on GitHub, so a broken relative path
is a dead end in both places."""

import os
import re
import unittest

import dsops

# [text](target) — skip images, they are checked separately.
LINK = re.compile(r"(?<!!)\[[^\]]*\]\(([^)\s]+)\)")
IMAGE = re.compile(r"!\[[^\]]*\]\(([^)\s]+)\)")

SKIP_PREFIXES = ("http://", "https://", "mailto:", "#", "tel:")


def _docs():
    """Root-level markdown docs plus the knowledge notes."""
    paths = [
        os.path.join(dsops.REPO_ROOT, entry)
        for entry in sorted(os.listdir(dsops.REPO_ROOT))
        if entry.endswith(".md")
    ]
    paths += [
        os.path.join(dsops.KNOWLEDGE_DIR, entry)
        for entry in sorted(os.listdir(dsops.KNOWLEDGE_DIR))
        if entry.endswith(".md")
    ]
    return paths


def _local_targets(text, pattern):
    for target in pattern.findall(text):
        if target.startswith(SKIP_PREFIXES):
            continue
        yield target.split("#", 1)[0]


class TestDocumentationLinks(unittest.TestCase):
    def test_relative_links_resolve(self):
        for path in _docs():
            text = dsops.read_text(path)
            for target in _local_targets(text, LINK):
                if not target:
                    continue
                with self.subTest(doc=dsops.rel(path), link=target):
                    resolved = os.path.normpath(
                        os.path.join(os.path.dirname(path), target)
                    )
                    self.assertTrue(
                        os.path.exists(resolved), "broken link -> %s" % target
                    )

    def test_relative_images_resolve(self):
        for path in _docs():
            text = dsops.read_text(path)
            for target in _local_targets(text, IMAGE):
                with self.subTest(doc=dsops.rel(path), image=target):
                    resolved = os.path.normpath(
                        os.path.join(os.path.dirname(path), target)
                    )
                    self.assertTrue(
                        os.path.isfile(resolved), "broken image -> %s" % target
                    )


class TestReadme(unittest.TestCase):
    """The README is the landing page — for humans and for the registry
    linters that index this repo."""

    def setUp(self):
        self.readme = dsops.read_text(os.path.join(dsops.REPO_ROOT, "README.md"))

    def _headings(self):
        return [h.strip().lower() for h in re.findall(r"(?m)^#{1,6}\s+(.+)$", self.readme)]

    def test_has_an_installation_heading(self):
        self.assertTrue(
            any(h.startswith(("install", "getting started")) for h in self._headings()),
            "README needs an Installation heading",
        )

    def test_has_a_usage_heading(self):
        self.assertTrue(
            any(
                h.startswith(("usage", "quick start", "example", "quickstart"))
                for h in self._headings()
            ),
            "README needs a Usage / Quick start / Examples heading",
        )

    def test_has_a_license_heading(self):
        self.assertTrue(any(h.startswith("license") for h in self._headings()))

    def test_has_a_runnable_code_block(self):
        self.assertRegex(self.readme, r"```bash\n\S", "no copy-pasteable command")


if __name__ == "__main__":
    unittest.main()

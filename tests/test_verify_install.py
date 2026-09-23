"""verify-install.sh is the doctor users run when skills behave oddly. These
tests pin its contract against the canonical layout and against the flattened
layout a third-party installer (e.g. `npx skills install`) produces — the one
that silently drops knowledge-notes/."""

import os
import shutil
import subprocess
import tempfile
import unittest

import dsops

SCRIPT = os.path.join(dsops.REPO_ROOT, "verify-install.sh")
SAMPLE_SKILL = os.path.join(dsops.SKILLS_DIR, "token-audit", "SKILL.md")


def _run(root):
    result = subprocess.run(
        ["bash", SCRIPT, root],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    return result.returncode, result.stdout.decode("utf-8", "replace")


@unittest.skipUnless(shutil.which("bash"), "bash unavailable")
class TestVerifyInstall(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="dsops-verify-")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_clean_checkout_passes(self):
        code, output = _run(dsops.REPO_ROOT)
        self.assertEqual(0, code, output)
        self.assertIn("references resolve", output)
        # The known-good direction: a healthy install raises nothing at all.
        self.assertNotIn("MISSING", output)
        self.assertNotIn("UNREADABLE", output)
        self.assertNotIn("warning", output)

    def test_flattened_install_fails(self):
        # The reported bug: skills/ present, knowledge-notes/ dropped.
        target = os.path.join(self.tmp, "skills", "token-audit")
        os.makedirs(target)
        shutil.copy(SAMPLE_SKILL, target)
        code, output = _run(self.tmp)
        self.assertEqual(1, code, output)
        self.assertIn("MISSING", output)
        self.assertIn("knowledge-notes", output)

    def test_single_flattened_skill_fails(self):
        shutil.copy(SAMPLE_SKILL, os.path.join(self.tmp, "SKILL.md"))
        code, output = _run(self.tmp)
        self.assertEqual(1, code, output)
        self.assertIn("MISSING", output)

    def test_unreadable_references_fail(self):
        # A file the parser can't read must not pass as "0 references, all
        # fine". CRLF line endings are one real way to get there.
        target = os.path.join(self.tmp, "skills", "token-audit")
        os.makedirs(target)
        text = dsops.read_text(SAMPLE_SKILL).replace("\n", "\r\n")
        with open(os.path.join(target, "SKILL.md"), "w", newline="") as handle:
            handle.write(text)
        code, output = _run(self.tmp)
        self.assertEqual(1, code, output)
        self.assertIn("UNREADABLE", output)

    def test_empty_skills_dir_fails(self):
        # Zero references found means the check saw nothing, not that
        # everything is fine.
        os.makedirs(os.path.join(self.tmp, "skills"))
        code, output = _run(self.tmp)
        self.assertEqual(1, code, output)
        self.assertNotIn("references resolve", output)

    def test_not_an_install_dir_exits_2(self):
        code, output = _run(self.tmp)
        self.assertEqual(2, code, output)


if __name__ == "__main__":
    unittest.main()

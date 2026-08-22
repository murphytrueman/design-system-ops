"""The bundle in installable/ is what users actually install. These tests build
a throwaway copy in a temp dir and assert the contract build.sh promises:
identical .zip/.plugin, every skill present, no repo tooling or local scratch
leaking into the artifact."""

import os
import shutil
import subprocess
import tempfile
import unittest
import zipfile

import dsops

BUILD = os.path.join(dsops.REPO_ROOT, "build.sh")


def _build_available():
    return (
        os.path.isfile(BUILD)
        and shutil.which("git") is not None
        and shutil.which("zip") is not None
    )


@unittest.skipUnless(_build_available(), "build.sh, git or zip unavailable")
class TestBundleBuild(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.out_dir = tempfile.mkdtemp(prefix="dsops-build-")
        env = dict(os.environ, DSOPS_OUT_DIR=cls.out_dir)
        cls.result = subprocess.run(
            ["bash", BUILD],
            cwd=dsops.REPO_ROOT,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        cls.zip_path = os.path.join(cls.out_dir, "design-system-ops.zip")
        cls.plugin_path = os.path.join(cls.out_dir, "design-system-ops.plugin")

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.out_dir, ignore_errors=True)

    def _names(self):
        with zipfile.ZipFile(self.zip_path) as bundle:
            return set(bundle.namelist())

    def test_build_succeeds(self):
        self.assertEqual(
            0,
            self.result.returncode,
            "build.sh failed:\n%s" % self.result.stderr.decode("utf-8", "replace"),
        )

    def test_both_artifacts_exist(self):
        self.assertTrue(os.path.isfile(self.zip_path))
        self.assertTrue(os.path.isfile(self.plugin_path))

    def test_zip_and_plugin_are_byte_identical(self):
        with open(self.zip_path, "rb") as a, open(self.plugin_path, "rb") as b:
            self.assertEqual(a.read(), b.read())

    def test_archive_is_not_corrupt(self):
        with zipfile.ZipFile(self.zip_path) as bundle:
            self.assertIsNone(bundle.testzip())

    def test_manifest_is_bundled(self):
        self.assertIn(".claude-plugin/plugin.json", self._names())

    def test_every_skill_is_bundled(self):
        names = self._names()
        missing = [
            dsops.rel(path) for path in dsops.skill_files() if dsops.rel(path) not in names
        ]
        self.assertEqual([], missing, "skills missing from the bundle")

    def test_every_command_is_bundled(self):
        names = self._names()
        missing = [
            dsops.rel(path)
            for path in dsops.command_files()
            if dsops.rel(path) not in names
        ]
        self.assertEqual([], missing, "commands missing from the bundle")

    def test_config_template_is_bundled(self):
        # The README tells users to copy this out of the pack.
        self.assertIn("ds-ops-config.example.yml", self._names())

    def test_no_tooling_or_scratch_leaks_in(self):
        leaked = sorted(
            name
            for name in self._names()
            if name.startswith(("installable/", "tests/", ".github/", ".internal/"))
            or os.path.basename(name) in (".DS_Store", ".gitignore")
        )
        self.assertEqual([], leaked, "these should not ship inside the bundle")

    def test_build_is_reproducible(self):
        """Two consecutive builds of the same tree must be byte-identical —
        that is the whole claim behind shipping a prebuilt bundle."""
        second = tempfile.mkdtemp(prefix="dsops-build-2-")
        try:
            subprocess.run(
                ["bash", BUILD],
                cwd=dsops.REPO_ROOT,
                env=dict(os.environ, DSOPS_OUT_DIR=second),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True,
            )
            with open(self.zip_path, "rb") as a, open(
                os.path.join(second, "design-system-ops.zip"), "rb"
            ) as b:
                self.assertEqual(a.read(), b.read())
        finally:
            shutil.rmtree(second, ignore_errors=True)

    def test_committed_bundle_matches_a_fresh_build(self):
        """installable/ is committed so Cowork users can download it without
        cloning. If it drifts from the source tree, they install stale skills.

        Compared by name + CRC rather than bytes: a zip stores mtimes, and a
        fresh checkout stamps every file with the checkout time."""
        committed = os.path.join(
            dsops.REPO_ROOT, "installable", "design-system-ops.zip"
        )
        if not os.path.isfile(committed):
            self.skipTest("no committed bundle to compare against")

        def fingerprint(path):
            with zipfile.ZipFile(path) as bundle:
                return {info.filename: info.CRC for info in bundle.infolist()}

        old, new = fingerprint(committed), fingerprint(self.zip_path)
        self.assertEqual(
            sorted(old), sorted(new), "committed bundle has a different file list"
        )
        changed = sorted(name for name in new if old.get(name) != new[name])
        self.assertEqual(
            [], changed, "committed bundle is stale — re-run ./build.sh and commit"
        )


if __name__ == "__main__":
    unittest.main()

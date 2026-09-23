#!/usr/bin/env python3
"""Bring every skill's install self-check block in line with
dsops.REFERENCE_CHECK_BLOCK.

The block's wording lives in one place, dsops.py. This script copies it into
every skill: skills with `references:` get exactly one copy as their first H2
(an outdated copy is replaced), and skills without references get none.

Usage:  python3 tests/sync_selfcheck.py            (rewrite files that are out of line)
        python3 tests/sync_selfcheck.py --check    (list them and exit 1; write nothing)
"""

import re
import sys

import dsops

HEADING = dsops.REFERENCE_CHECK_BLOCK.splitlines()[0]
_FRONTMATTER = re.compile(r"\A---\n.*?\n---\n", re.DOTALL)
_H2 = re.compile(r"(?m)^## ")


def _strip_block(text):
    """Remove the self-check section, whatever its wording, up to the next H2."""
    start = text.find(HEADING + "\n")
    if start == -1:
        return text
    following = _H2.search(text, start + len(HEADING))
    end = following.start() if following else len(text)
    return text[:start] + text[end:]


def synced(text, has_references):
    """Return `text` with the canonical block in place (or absent)."""
    text = _strip_block(text)
    if not has_references:
        return text
    body_start = _FRONTMATTER.match(text).end()
    first_h2 = _H2.search(text, body_start)
    at = first_h2.start() if first_h2 else len(text)
    return text[:at] + dsops.REFERENCE_CHECK_BLOCK + "\n" + text[at:]


def sync(path, write=True):
    """Sync one skill file. Returns True if it was (or would be) changed."""
    text = dsops.read_text(path)
    data, _ = dsops.load_document(path)
    new = synced(text, "references" in data)
    if new == text:
        return False
    if write:
        with open(path, "w", encoding="utf-8") as handle:
            handle.write(new)
    return True


def main(argv):
    check = "--check" in argv
    changed = [
        dsops.rel(path)
        for path in dsops.skill_files() + dsops.agent_files()
        if sync(path, write=not check)
    ]
    for name in changed:
        print(("out of line: " if check else "synced: ") + name)
    if not changed:
        print("All self-check blocks are in line.")
    return 1 if check and changed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

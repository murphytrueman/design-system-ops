#!/usr/bin/env bash
#
# Check that a design-system-ops install is complete: every file a skill lists
# in its frontmatter `references:` must exist at that relative path.
#
# Third-party installers that flatten each skill into its own folder (for
# example `npx skills install`) drop the repo-root knowledge-notes/ directory.
# Skills then run without their reference material. This script catches that.
#
# Usage:  ./verify-install.sh                 (checks the directory it lives in)
#         ./verify-install.sh <install-dir>   (checks another install)
#
# Exit:   0  every reference resolves
#         1  references are missing, or a skill file couldn't be read
#         2  <install-dir> is not a design-system-ops install
#
set -euo pipefail

ROOT="${1:-$(cd "$(dirname "$0")" && pwd)}"
ROOT="${ROOT%/}"

total=0
missing=0
unreadable=0
is_pack=0

# Print each `references:` list item from a markdown file's frontmatter
# (the block between the first two `---` fences).
references_of() {
  awk '
    NR == 1 && $0 == "---" { in_fm = 1; next }
    in_fm && $0 == "---"   { exit }
    !in_fm                 { exit }
    /^[A-Za-z_][A-Za-z0-9_-]*:/ { in_refs = ($0 ~ /^references:[[:space:]]*$/); next }
    in_refs && /^[[:space:]]+-[[:space:]]+/ {
      sub(/^[[:space:]]+-[[:space:]]+/, "")
      gsub(/^["\047]|["\047][[:space:]]*$/, "")
      sub(/[[:space:]]+$/, "")
      print
    }
  ' "$1"
}

check_doc() {
  local doc="$1" name="$2" dir ref noun count=0 bad=0
  dir="$(dirname "$doc")"
  while IFS= read -r ref; do
    [ -n "$ref" ] || continue
    count=$((count + 1))
    if [ ! -f "$dir/$ref" ]; then
      echo "MISSING  $name -> $ref"
      bad=$((bad + 1))
    fi
  done < <(references_of "$doc")
  # A `references:` key that yields nothing means the parser couldn't read
  # this file. Reporting it as clean would be a false pass.
  if [ "$count" -eq 0 ] && grep -q '^references:' "$doc"; then
    echo "UNREADABLE  $name -> has a references: field, but none could be read"
    unreadable=$((unreadable + 1))
  fi
  total=$((total + count))
  missing=$((missing + bad))
  if [ "$count" -gt 0 ] && [ "$bad" -eq 0 ]; then
    if [ "$count" -eq 1 ]; then noun=reference; else noun=references; fi
    echo "OK       $name ($count $noun)"
  fi
}

if [ -d "$ROOT/skills" ]; then
  is_pack=1
  for required in knowledge-notes commands; do
    if [ ! -d "$ROOT/$required" ]; then
      echo "warning: $ROOT/$required/ is missing — the install looks flattened or partial"
    fi
  done
  for doc in "$ROOT"/skills/*/SKILL.md "$ROOT"/skills/*.md; do
    [ -f "$doc" ] || continue
    check_doc "$doc" "${doc#"$ROOT"/}"
  done
elif [ -f "$ROOT/SKILL.md" ]; then
  echo "note: $ROOT holds a single flattened skill, not the full pack"
  check_doc "$ROOT/SKILL.md" "SKILL.md"
else
  echo "error: $ROOT is not a design-system-ops install (no skills/ or SKILL.md)" >&2
  exit 2
fi

echo
if [ "$unreadable" -gt 0 ]; then
  echo "$unreadable skill file(s) could not be read. This check can't vouch for them."
  exit 1
fi
# Every full install has skills with references, so zero found means the
# check saw nothing — not that everything is fine.
if [ "$is_pack" -eq 1 ] && [ "$total" -eq 0 ]; then
  echo "Found skills/ but no references in it. This check can't vouch for this install."
  exit 1
fi
if [ "$missing" -gt 0 ]; then
  echo "$missing of $total references are missing. The install is incomplete."
  echo "Reinstall with git clone or the .plugin bundle — see 1-INSTALL.md."
  exit 1
fi
echo "All $total references resolve."

#!/usr/bin/env bash
#
# Build the distributable plugin bundle from the working tree.
#
# Produces two byte-identical outputs in installable/:
#   - design-system-ops.zip
#   - design-system-ops.plugin   (the file Cowork users drop into a session)
#
# The file set is derived from `git ls-files`, so anything untracked
# (.internal/, .DS_Store, local scratch) is excluded by construction.
# A few tracked files are explicitly held back below.
#
# Usage:  ./build.sh
#
set -euo pipefail
cd "$(dirname "$0")"

OUT_DIR="installable"
ZIP="$OUT_DIR/design-system-ops.zip"
PLUGIN="$OUT_DIR/design-system-ops.plugin"

# Tracked files that should NOT ship inside the bundle:
#   installable/*        the build output itself
#   .gitignore           repo tooling, not part of the plugin
# (ds-ops-config.example.yml IS shipped — it's the annotated config template
#  the README promises; users copy it to their project root as .ds-ops-config.yml.)
EXCLUDES='^installable/|^\.gitignore$'

# Refuse to build with a dirty/untracked-but-staged surprise: warn only.
if ! git diff --quiet || ! git diff --cached --quiet; then
  echo "note: working tree has uncommitted changes — the bundle reflects the"
  echo "      current files on disk, not the last commit." >&2
fi

FILES="$(git ls-files | grep -Ev "$EXCLUDES")"

rm -f "$ZIP" "$PLUGIN"
printf '%s\n' "$FILES" | zip -q -X "$ZIP" -@
cp "$ZIP" "$PLUGIN"

COUNT="$(printf '%s\n' "$FILES" | grep -c .)"
echo "Built $ZIP and $PLUGIN ($COUNT files)"

# Guard: the two outputs must be identical.
if ! cmp -s "$ZIP" "$PLUGIN"; then
  echo "error: .zip and .plugin differ after build" >&2
  exit 1
fi

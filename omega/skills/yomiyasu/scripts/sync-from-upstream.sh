#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
REPO_ROOT="$(cd "$SKILL_DIR/../../.." && pwd)"
UP="$REPO_ROOT/yomiyasu"

if [[ ! -f "$UP/SKILL.md" ]]; then
  echo "upstream not found: $UP (run: git submodule update --init yomiyasu)" >&2
  exit 1
fi

echo "Syncing from $UP -> $SKILL_DIR"

cp "$UP/references/gemini-syntax.md" "$SKILL_DIR/references/"
cp "$UP/references/slop-catalog.md" "$SKILL_DIR/references/"
cp "$UP/references/domains/"*.md "$SKILL_DIR/references/domains/"
cp "$UP/scripts/yomiyasu_lint.py" "$UP/scripts/yomiyasu_diff.py" "$SKILL_DIR/scripts/"

echo "Copied references/ and scripts/."
echo "Manual: merge upstream SKILL.md into references/writing-rules.md and omega/skills/yomiyasu/SKILL.md if needed."

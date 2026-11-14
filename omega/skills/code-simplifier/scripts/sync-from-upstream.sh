#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
REPO_ROOT="$(cd "$SKILL_DIR/../../.." && pwd)"
UP="$REPO_ROOT/claude-plugins-official/plugins/code-simplifier"
AGENT="$UP/agents/code-simplifier.md"
LICENSE="$UP/LICENSE"

if [[ ! -f "$AGENT" ]]; then
  echo "upstream not found: $AGENT (run: git submodule update --init claude-plugins-official)" >&2
  exit 1
fi

mkdir -p "$SKILL_DIR/references"
cp "$AGENT" "$SKILL_DIR/references/upstream-agent.en.md"
[[ -f "$LICENSE" ]] && cp "$LICENSE" "$SKILL_DIR/references/LICENSE.txt"

echo "上流エージェントを同期: references/upstream-agent.en.md"
echo "手動: omega/agents/code-simplifier.md へマージ（プロジェクト規約・自動起動なし）。"

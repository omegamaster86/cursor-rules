#!/usr/bin/env bash
set -euo pipefail

# Install omega into a Cloud Agent VM (or local dry-run).
# Expects OMEGA to point at the omega/ directory (commands, skills, rules).
# Writes workspace-scoped .cursor/ links plus VM-home skills for discovery.

usage() {
  echo "usage: OMEGA=/path/to/omega install-omega-cloud.sh" >&2
  echo "       (usually invoked via .cursor/install-omega.sh in each project)" >&2
}

if [[ -z "${OMEGA:-}" ]]; then
  script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
  OMEGA="$(cd "$script_dir/.." && pwd)"
fi

if [[ ! -d "$OMEGA/commands" || ! -d "$OMEGA/skills" || ! -d "$OMEGA/rules" ]]; then
  echo "omega not found: $OMEGA" >&2
  usage
  exit 1
fi

detect_workspace() {
  if [[ -n "${OMEGA_WORKSPACE:-}" ]]; then
    printf '%s\n' "$OMEGA_WORKSPACE"
    return 0
  fi
  if [[ -d /workspace ]] && { [[ -e /workspace/.git ]] || [[ -d /workspace/.cursor ]]; }; then
    printf '%s\n' /workspace
    return 0
  fi
  if git rev-parse --show-toplevel &>/dev/null; then
    git rev-parse --show-toplevel
    return 0
  fi
  pwd
}

WORKSPACE="$(detect_workspace)"
HOME_CURSOR="${HOME}/.cursor"
WS_CURSOR="$WORKSPACE/.cursor"

mkdir -p "$HOME_CURSOR/skills" "$WS_CURSOR/rules" "$WS_CURSOR/skills"

link_path() {
  local source="$1"
  local target="$2"

  if [[ -e "$target" && ! -L "$target" ]]; then
    echo "skip (exists as real path): $target" >&2
    return 0
  fi

  ln -sfn "$source" "$target"
}

link_path "$OMEGA/commands" "$WS_CURSOR/commands"
link_path "$OMEGA/agents" "$WS_CURSOR/agents"

for rule in global.mdc multi-agent-task-enforcement.mdc; do
  link_path "$OMEGA/rules/$rule" "$WS_CURSOR/rules/$rule"
done

if [[ ! -e "$WS_CURSOR/rules/forge-models.mdc" ]]; then
  cp "$OMEGA/rules/forge-models.mdc" "$WS_CURSOR/rules/forge-models.mdc"
fi

for skill in "$OMEGA/skills"/*/; do
  name="$(basename "$skill")"
  [[ "$name" == verify-* ]] && continue
  link_path "$skill" "$WS_CURSOR/skills/$name"
  link_path "$skill" "$HOME_CURSOR/skills/$name"
done

echo "omega cloud install complete"
echo "  omega:     $OMEGA"
echo "  workspace: $WORKSPACE"
echo "  workspace .cursor: $WS_CURSOR"
echo "  vm skills:         $HOME_CURSOR/skills"

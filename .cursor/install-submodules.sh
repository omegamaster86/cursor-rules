#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$root"

if [[ ! -d .git ]]; then
  echo "not a git checkout: $root" >&2
  exit 1
fi

git submodule sync --recursive

init_submodule() {
  local path="$1"
  local required="${2:-false}"
  if git submodule update --init "$path"; then
    return 0
  fi
  if [[ "$required" == true ]]; then
    echo "required submodule failed: $path" >&2
    return 1
  fi
  echo "optional submodule skipped (init failed): $path" >&2
  return 0
}

# openai/plugins is the primary reference for Codex plugin examples.
init_submodule openai-plugins true
init_submodule yomiyasu false
init_submodule supabase-skills false

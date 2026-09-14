#!/usr/bin/env bash
set -euo pipefail

# Cloud Agent install hook (commit this file + environment.json in each project).
# Clones cursor-rules, then runs omega/scripts/install-omega-cloud.sh.

OMEGA_REPO="${OMEGA_REPO:-https://github.com/omegamaster86/cursor-rules.git}"
OMEGA_REF="${OMEGA_REF:-main}"
CACHE_ROOT="${OMEGA_CACHE:-${HOME}/.cache/omega}"
REPO_DIR="${CACHE_ROOT}/cursor-rules"

clone_or_update_repo() {
  local repo_url="$1"

  if [[ -n "${GITHUB_TOKEN:-}" && "$repo_url" != *"@"* ]]; then
    repo_url="${repo_url/https:\/\//https://${GITHUB_TOKEN}@}"
  fi

  if [[ ! -d "$REPO_DIR/.git" ]]; then
    mkdir -p "$CACHE_ROOT"
    git clone --depth 1 --branch "$OMEGA_REF" "$repo_url" "$REPO_DIR"
    return 0
  fi

  git -C "$REPO_DIR" fetch --depth 1 origin "$OMEGA_REF"
  git -C "$REPO_DIR" checkout "$OMEGA_REF"
  git -C "$REPO_DIR" reset --hard "FETCH_HEAD"
}

clone_or_update_repo "$OMEGA_REPO"

export OMEGA="$REPO_DIR/omega"
exec bash "$OMEGA/scripts/install-omega-cloud.sh"

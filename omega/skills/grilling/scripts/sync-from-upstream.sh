#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
REPO_ROOT="$(cd "$SKILL_DIR/../../.." && pwd)"
UP_GRILLING="$REPO_ROOT/mattpocock-skills/productivity/grilling/SKILL.md"
UP_GRILL_ME="$REPO_ROOT/mattpocock-skills/productivity/grill-me/SKILL.md"
OMEGA_GRILL_ME="$REPO_ROOT/omega/skills/grill-me/SKILL.md"

if [[ ! -f "$UP_GRILLING" ]]; then
  echo "upstream not found: $UP_GRILLING (refresh mattpocock-skills/ first)" >&2
  exit 1
fi

echo "Upstream grilling (reference only — merge manually into $SKILL_DIR/SKILL.md):"
echo "  $UP_GRILLING"
REF="$SKILL_DIR/references/grilling-upstream.en.md"
cp "$UP_GRILLING" "$REF"
diff -u "$REF" "$UP_GRILLING" && echo "(reference copy updated)" || true

if [[ -f "$UP_GRILL_ME" ]]; then
  mkdir -p "$(dirname "$OMEGA_GRILL_ME")"
  cat > "$OMEGA_GRILL_ME" <<'EOF'
---
name: grill-me
description: 計画や設計を容赦なく研ぎ澄ますインタビュー。`/plan-interview` または grilling トリガー向けの互換入口。
disable-model-invocation: true
---

`grilling` スキルを実行する。技法の正本は `grilling/SKILL.md`。Align の推奨入口は **`/plan-interview`**（Ship への `alignment:` 手渡しは plan-interview が所有）。
EOF
  echo "Wrote $OMEGA_GRILL_ME"
fi

echo "Done. Manual: merge upstream grilling into omega/skills/grilling/SKILL.md (Japanese + forge sections)."

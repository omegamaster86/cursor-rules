#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
REPO_ROOT="$(cd "$SKILL_DIR/../../.." && pwd)"
UP="$REPO_ROOT/yomiyasu"
UP_SKILL="$UP/skills/yomiyasu/SKILL.md"

if [[ ! -f "$UP/references/gemini-syntax.md" ]] || [[ ! -f "$UP_SKILL" ]]; then
  echo "upstream not found: $UP (run: git submodule update --init yomiyasu)" >&2
  exit 1
fi

echo "Syncing from $UP -> $SKILL_DIR"

mkdir -p "$SKILL_DIR/references/domains" "$SKILL_DIR/references/doc-types" "$SKILL_DIR/references/lists"

cp "$UP/references/gemini-syntax.md" "$SKILL_DIR/references/"
cp "$UP/references/slop-catalog.md" "$SKILL_DIR/references/"
cp "$UP/references/calques.md" "$SKILL_DIR/references/"
cp "$UP/references/review-points.md" "$SKILL_DIR/references/"
cp "$UP/references/rephrase-test.md" "$SKILL_DIR/references/"
cp "$UP/references/audience.md" "$SKILL_DIR/references/"
cp "$UP/references/persona.md" "$SKILL_DIR/references/"
cp "$UP/references/fact-recovery.md" "$SKILL_DIR/references/"
cp "$UP/references/fact-recovery-details.md" "$SKILL_DIR/references/"
cp "$UP/references/domains/"*.md "$SKILL_DIR/references/domains/"
cp "$UP/references/doc-types/"*.md "$SKILL_DIR/references/doc-types/"
cp "$UP/references/lists/"*.txt "$SKILL_DIR/references/lists/"
cp "$UP/scripts/yomiyasu_lint.py" "$UP/scripts/yomiyasu_diff.py" "$SKILL_DIR/scripts/"

export SKILL_DIR
python3 - <<'PY'
import os
import re
from pathlib import Path

skill_dir = Path(os.environ["SKILL_DIR"])
repo = skill_dir.parents[2]
up_skill = repo / "yomiyasu/skills/yomiyasu/SKILL.md"
text = up_skill.read_text(encoding="utf-8")
ver = "main"
m = re.search(r'^  version:\s*"([^"]+)"', text, re.M)
if m:
    ver = m.group(1)
lines = text.splitlines()
start = next(i for i, l in enumerate(lines) if l.startswith("## 1. 基本原則"))
end = next(i for i, l in enumerate(lines) if l.startswith("## 2. 実行手順"))
body = lines[start + 1 : end]
while body and not body[0].strip():
    body = body[1:]
header = f"""# コア設計思想（yomiyasu）

上流 [nanaism/yomiyasu](https://github.com/nanaism/yomiyasu) v{ver} の `skills/yomiyasu/SKILL.md` §1 相当。omega では Cursor 向けにここへ分離している。更新は `scripts/sync-from-upstream.sh` を参照。

"""
(skill_dir / "references/writing-rules.md").write_text(header + "\n".join(body) + "\n", encoding="utf-8")
print(f"Regenerated references/writing-rules.md from upstream §1 (v{ver})")
PY

echo "Copied references/, lists/, scripts/."
echo "Upstream SKILL: $UP_SKILL"
echo "Manual: merge upstream SKILL.md §2–§3 into omega/skills/yomiyasu/SKILL.md if needed."


#!/usr/bin/env python3
"""One-shot sync from cursor/plugins pstack @ 11713c6 into omega (forge renames via port-pstack-skills)."""

from __future__ import annotations

import importlib.util
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OMEGA = ROOT / "omega"
PSTACK = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("/tmp/pstack-upstream/pstack")

spec = importlib.util.spec_from_file_location("port", ROOT / "omega/scripts/port-pstack-skills.py")
port_mod = importlib.util.module_from_spec(spec)
assert spec.loader
spec.loader.exec_module(port_mod)
port_text = port_mod.port_text


def principle_body(skill_md: str) -> str:
    if skill_md.startswith("---"):
        return skill_md.split("---", 2)[2].lstrip("\n")
    return skill_md


def write_ported(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(port_text(src.read_text(encoding="utf-8")), encoding="utf-8")


def main() -> None:
    # Scripts
    src = PSTACK / "skills/poteto-mode/scripts/orch/orch.test.ts"
    dst = OMEGA / "skills/forge-mode/scripts/orch/orch.test.ts"
    write_ported(src, dst)

    # Ketchup (new)
    ketchup_src = PSTACK / "skills/ketchup/SKILL.md"
    raw = port_text(ketchup_src.read_text(encoding="utf-8"))
    # Japanese frontmatter + body adapted from upstream
    ketchup = """---
name: ketchup
description: "このチャットでユーザー最後のメッセージ以降の出来事を平易な言葉でキャッチアップする。各 action item に判断できる executive summary を付ける。/ketchup に使用。"
disable-model-invocation: true
---

# Ketchup

ユーザーが `/ketchup` の直前に書いた最後のメッセージ以降、このチャットで起きたことをキャッチアップする。通知とサブエージェント結果はユーザーのメッセージではない。[`/bro`](../bro/SKILL.md) の平易な声で書き、その restating ステップはスキップする。ユーザーは自分の最後のメッセージだけ覚えていて、その後は何も知らないと仮定する。PR・branch・エージェントは作業中に付けたラベルではなく、ユーザーが知っている名前で呼ぶ。

## Gather what changed

このターンは read-only。自分の作業、サブエージェントの報告、このチャットの他者メッセージを集める。このチャットが触れた各 PR・CI・エージェントの現状を確認する。まだ走っているもの、確認できなかったものを述べる。

action item はユーザーだけが取れる決定またはステップ（プロダクト判断、承認、不可逆操作、アクセス不足）。ユーザー最後のメッセージより前から待っているものも含める。自分がまだできる作業は action item ではない。

## Write the reply

action item の件数を 1 文で開く。0 件ならそう言う。何も起きておらずユーザー待ちもなければそう言って終える。

次に起きたことを重要度順に述べる。各結果とユーザーへの意味を述べる。変化のないステップはスキップ。自分がまだできる残作業を 1 行で名指す。

各 action item に短い executive summary を付ける。決めること、今重要な理由、選択肢と各コスト、推奨、ユーザーが答えない場合の結果。分からない部分は推測せずそう言う。詳細があればリンクし、開かずに判断できる要約にする。
"""
    ketchup_dir = OMEGA / "skills/ketchup"
    ketchup_dir.mkdir(parents=True, exist_ok=True)
    (ketchup_dir / "SKILL.md").write_text(ketchup, encoding="utf-8")

    print("Synced orch.test.ts and ketchup/SKILL.md")


if __name__ == "__main__":
    main()

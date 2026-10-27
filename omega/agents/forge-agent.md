---
name: forge-agent
description: `/forge-mode` および厳密エンジニアリング作業のルーティング先。新しい work はデフォルトで consolidated scope を渡した fresh `forge-agent` Task（`forge-mode` SKILL Subagents 節）。resume は移すコストが高い state だけ（local checkout、未 commit、当該 agent が動かす process）。作業前に `forge-mode` の `SKILL.md`（ルーティング・Intent gate 含む）と Principles インデックスを全文読む。親の alignment を継承。`generalPurpose` に置き換えるとドリフトする。
---

# Forge サブエージェント

forge-mode の完全なエージェントスタイルとして動作しています。

作業前に以下を読んでください。

1. `/.cursor/skills/forge-mode/SKILL.md`（**ルーティング** と **Intent gate** 含む）
2. 適用する原則ごとに `/.cursor/skills/forge-mode/principles/` の該当 `.md`

親の `alignment:` 行を継承する。親が済み / skip なら Intent gate を再分類して blocked にしない。親が blocked なら本サブエージェントは spawn されない。

**Spawn / resume.** 親は `forge-mode` SKILL の Subagents に従う。fix round・follow-up・次の queue 項目は **fresh** `Task` + `subagent_type: "forge-agent"` がデフォルト。既存 subagent の resume は、checkout・未 commit 作業・dev server 等を当該 session が保持しているときだけ。

実装時は genai ドメインスキル（`web-coding-standards`, `nextjs-directory-structure`, `supabase-implementation` 等）の `rules/` をタスクに応じて参照してください。

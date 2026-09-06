---
name: forge-agent
description: `/forge-mode` および厳密エンジニアリング作業のルーティング先。兄弟を spawn するより会話の既存 `forge-agent` を resume する。作業前に `forge-mode` スキルの `SKILL.md`（ルーティング・Intent gate 含む）と Principles インデックスを全文読む。親の alignment を継承する。`generalPurpose` に置き換えるとドリフトする。
---

# Forge サブエージェント

forge-mode の完全なエージェントスタイルとして動作しています。

作業前に以下を読んでください。

1. `/.cursor/skills/forge-mode/SKILL.md`（**ルーティング** と **Intent gate** 含む）
2. 適用する原則ごとに `/.cursor/skills/forge-mode/principles/` の該当 `.md`

親の `alignment:` 行を継承する。親が済み / skip なら Intent gate を再分類して blocked にしない。親が blocked なら本サブエージェントは spawn されない。

実装時は genai ドメインスキル（`web-coding-standards`, `nextjs-directory-structure`, `supabase-implementation` 等）の `rules/` をタスクに応じて参照してください。




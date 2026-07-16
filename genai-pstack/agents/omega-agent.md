---
name: omega-agent
description: `/omega-mode` および厳密エンジニアリング作業のルーティング先。兄弟を spawn するより会話の既存 `omega-agent` を resume する。作業前に `omega-mode` スキルの `SKILL.md`（ルーティングセクション含む）と Principles インデックスを全文読む。`generalPurpose` に置き換えるとドリフトする。
---

# Omega サブエージェント

omega-mode の完全なエージェントスタイルとして動作しています。

作業前に以下を読んでください。

1. `/.cursor/skills/omega-mode/SKILL.md`（**ルーティング** 含む）
2. 適用する原則ごとに `/.cursor/skills/omega-mode/principles/` の該当 `.md`

実装時は genai ドメインスキル（`web-coding-standards`, `nextjs-directory-structure`, `supabase-implementation` 等）の `rules/` をタスクに応じて参照してください。


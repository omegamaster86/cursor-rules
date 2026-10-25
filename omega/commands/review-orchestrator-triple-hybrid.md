---
name: review-orchestrator-triple-hybrid
model: inherit
description: 担当分け並列レビュー（正しさ×2 / 品質 / セキュリティ / 条件付き blast）を統合し、成果物を .cursor/agent-review に保存する。
---

`/.cursor/skills/agent-review/SKILL.md` を読み、続けて `/.cursor/skills/agent-review/references/orchestrator.md` の手順を **全文**実行する。

フェーズに応じて SKILL 内の表から `references/` を on-demand で読む。サブエージェントには `/.cursor/skills/agent-review/lanes/` 配下の該当ファイルをプロンプトに明示する。

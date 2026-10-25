# Security レーン vs `/code-security`

| | Orchestrator D レーン | `/code-security` スキル |
|--|----------------------|-------------------------|
| 起動 | `review-orchestrator-triple-hybrid` 内で常時 | ユーザー明示依頼のみ |
| 実体 | Cursor `security-review` サブエージェント | `code-security` の jobs/ + panel |
| スコープ | ブランチ差分・PR 向け triage | codebase / repository / changes / patches |
| 成果物 | `.cursor/agent-review/<run_id>/lane-security.md` | `.cursor/CODE-SECURITY-<UTC>/` |

深い threat model・パッチ生成・広いツリースキャンは `/code-security`。PR マージ前の専任セキュリティ監査は orchestrator の D レーン。

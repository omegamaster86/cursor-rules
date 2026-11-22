# Security レーン vs `/code-security`

| | Orchestrator D レーン | `/code-security` スキル |
|--|----------------------|-------------------------|
| 起動 | `/agent-review` オーケストレーター内で常時 | ユーザー明示依頼のみ |
| 実体 | Cursor `security-review` サブエージェント | `code-security` の jobs/ + panel |
| スコープ | ブランチ差分・PR 向け triage | codebase / repository / changes / patches |
| 成果物 | チャット統合レポートの Security セクション | `.cursor/CODE-SECURITY-<UTC>/` |

深い threat model・パッチ生成・広いツリースキャンは `/code-security`（調査レンズは `code-security/references/lenses/`）。PR 上の短い表は orchestrator の D レーン。大 diff のマージ前は `/code-security` を正とし、D レーンはスモークに使う。



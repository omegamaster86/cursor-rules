---
name: codex-security
description: "omega 統合 codex-security: リポジトリ全体またはコミット済み diff のソース根拠セキュリティ監査。親スキル code-security から呼ぶ。"
---

# codex-security（omega）

OpenAI Codex Security の監査モデルを Cursor 上で再現するジョブ群。MCP / workbench は使わない。

## ジョブ

| ジョブ | ファイル |
|--------|----------|
| リポジトリ / スコープ | [scan-repository.md](scan-repository.md) |
| ブランチ・コミット diff | [scan-diff.md](scan-diff.md) |
| 監査コア | [core-audit.md](core-audit.md) |

## 共有参照

- [../references/artifacts.md](../references/artifacts.md)
- [../references/severity.md](../references/severity.md)
- [../references/threat-model.md](../references/threat-model.md)
- [../references/report-format.md](../references/report-format.md)

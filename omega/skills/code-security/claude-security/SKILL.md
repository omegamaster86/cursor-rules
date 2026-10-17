---
name: claude-security
description: "omega 統合 claude-security: codebase / changes スキャンとパッチ提案。Verifier パネル付き。親スキル code-security から呼ぶ。"
---

# claude-security（omega）

Claude Security の 3 ジョブを Cursor Task で実装する。

## ジョブ

| ジョブ | ファイル |
|--------|----------|
| Scan codebase | [scan-codebase.md](scan-codebase.md) |
| Scan changes | [scan-changes.md](scan-changes.md) |
| Suggest patches | [suggest-patches.md](suggest-patches.md) |

## 共有参照

- [../references/security-lead.md](../references/security-lead.md)
- [../references/verifier-panel.md](../references/verifier-panel.md)
- [../references/artifacts.md](../references/artifacts.md)
- [../references/report-format.md](../references/report-format.md)

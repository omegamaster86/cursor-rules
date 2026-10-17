# 統一セキュリティレポート形式

`CODE-SECURITY-<timestamp>/RESULTS.md` の形。

```markdown
## セキュリティレビュー結果

### 実行コンテキスト
| 項目 | 値 |
|------|-----|
| ジョブ | scan-codebase / scan-repository / scan-changes / scan-diff / suggest-patches / triage |
| モード | scan / changes / commit |
| スコープ | … |
| リビジョン | `<commit>` dirty: true/false |
| 検証 | verified / unverified（理由） |

### 概要
…

### 指摘事項

#### 🔴 Critical
- **F1** タイトル — `path:line`
  - CWE: …
  - 攻撃経路: …
  - 修正案: …

### カバレッジ
…

### 次のアクション
…
```

`findings.jsonl` が機械可読の正本。重大度: [severity.md](severity.md)

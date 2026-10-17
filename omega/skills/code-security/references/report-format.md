# 統一セキュリティレポート形式

`CODE-SECURITY-<timestamp>/RESULTS.md` の形。エンジンは `codex-security` または `claude-security`（本スキル配下のジョブ名）。

```markdown
## セキュリティレビュー結果

### 実行コンテキスト
| 項目 | 値 |
|------|-----|
| エンジン | codex-security / claude-security |
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

#### 🟡 Warning / 🟢 Info
（severity に応じて）

### カバレッジ
- レビューした範囲 / スキップした理由 / preExisting（changes のみ）

### 次のアクション
- [ ] 修正
- [ ] suggest-patches（claude-security）
- [ ] 再スキャン（effort / scope を指定）
```

`findings.jsonl` は機械可読の正本。チャットは要約のみ。

重大度の詳細: [severity.md](severity.md)

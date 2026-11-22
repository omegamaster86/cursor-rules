# 統一セキュリティレポート形式

`.cursor/CODE-SECURITY-<timestamp>/RESULTS.md` の形。

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

### レンズ
| レンズ | 状態 | 候補 |
|--------|------|------|
| admin-rpc | candidates / none / not_applicable | C1, C2 |

`lens_coverage.json` と一致させる。`none` は理由を表の下に 1 行。

### コントロール確認済み
[merge-gate.md](merge-gate.md)。ソースで見たものだけ。

### マージ前ゲート
[merge-gate.md](merge-gate.md) の表。無ければ「手動ゲートなし」。

### カバレッジ
…

### 次のアクション
…
```

`findings.jsonl` が機械可読の正本。重大度: [severity.md](severity.md)


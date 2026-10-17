# 統一セキュリティレポート形式（omega）

Codex / Claude / Cursor 単体のいずれでも、**ユーザー向けサマリ**はこの形に揃える。公式スキャナの生 JSON（`findings.json` / `CLAUDE-SECURITY-RESULTS.jsonl` 等）は正本として残し、チャットでは要約を出す。

```markdown
## セキュリティレビュー結果

### 実行コンテキスト
| 項目 | 値 |
|------|-----|
| エンジン | `cursor` / `codex-security` / `claude-security` / `security-guidance` |
| スコープ | リポジトリ全体 / パス / ブランチ差分 / PR / コミット |
| ベースリビジョン | （差分スキャン時） |
| 公式成果物 | （例: `CLAUDE-SECURITY-20260417-120000/`、`report.md` パス） |

### 概要
[1–3 文。何を、どの深さで見たか。カバレッジの限界があれば一言。]

### 指摘事項

#### 🔴 Critical（マージ前に修正必須）
- **[ID または ファイル:行]** タイトル
  - クラス: （例: injection / authz / secret / SSRF）
  - 根拠: [攻撃経路またはデータフロー 1–2 文]
  - 証拠: `path/to/file` のスニペットまたは公式 finding 参照
  - 修正案: [具体的な変更の方向]

#### 🟡 Warning
- （同形式）

#### 🟢 Info
- （同形式）

### カバレッジ・信頼度
- 見た範囲 / 見ていない範囲（生成コードのみ、テストのみ、サードパーティ等）
- 公式スキャンで verifier 済みの場合はその旨（Claude Security）
- 未検証の仮説は **Hypothesis** と明記

### 良い点
- [セキュリティ上妥当な実装]

### 次のアクション
- [ ] 修正 PR
- [ ] 公式パッチ適用（Claude Security `suggest-patches`）
- [ ] 再スキャン（スコープ・effort を指定）
- [ ] forge Babysit: Bugbot / agentic security コメント triage（`forge-mode/references/bugbot-triage.md`）
```

## 重大度の基準

| レベル | 基準 | 例 |
|--------|------|-----|
| 🔴 Critical | 本番で悪用可能、認可抜け、秘密漏洩、データ破壊 | IDOR、SQLi、認証バイパス、RLS なし、ハードコード鍵 |
| 🟡 Warning | 条件付きリスク、設定ミス、防御不足 | 弱い CSP、ログに PII、エラー詳細の露出 |
| 🟢 Info | ベストプラクティス、将来の負債 | コメント、監査ログの改善 |

## Finding ID のマッピング

| ソース | ID の扱い |
|--------|-----------|
| Claude Security | 公式 `F\d+` をそのまま引用 |
| Codex Security | workbench の finding identity / fingerprint を引用（レポート内表記に従う） |
| Cursor 単体 | `CUR-<連番>` または `ファイル:行` |

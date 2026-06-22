---
name: supabase-code-review
description: Supabase PRのコードレビューを規約に基づいて実施する。migrationファイル、Edge Function、DB Functionのレビュー、差分チェック、品質チェックを依頼された際に使用する。
---

# Supabase Code Review

PRの差分を規約に基づいてレビューし、問題点と改善提案をフィードバックする。
対象: migrationファイル（SQL）、Edge Function（TypeScript/Deno）、DB Function（PostgreSQL）。

## When to Apply

- Supabase関連のPRコードレビューを依頼された時
- migration / Edge Function / DB Functionの品質チェックを依頼された時
- バックエンド側の「レビューして」「チェックして」と言われた時

## Review Workflow

### Step 1: 差分を取得

```bash
# PRの差分を取得
gh pr diff <PR番号>

# または現在のブランチの差分
git diff main...HEAD
```

### Step 2: 変更ファイルを分類

変更ファイルを以下のカテゴリに分類し、優先度順にレビューする：

| 優先度 | カテゴリ | ファイルパターン |
|--------|----------|------------------|
| 1 | Migration（テーブル定義） | `migrations/*_create_*_tables.sql` |
| 2 | Migration（DB Function） | `migrations/*_create_function_*.sql` |
| 3 | Edge Function | `functions/*/index.ts` |
| 4 | 共有モジュール | `functions/_shared/*.ts` |
| 5 | 型定義 | `functions/_shared/database.types.ts` |

### Step 3: カテゴリ別レビュー

各ファイルを読み込み、[checklist.md](checklist.md) の観点に沿ってレビューする。
優先度順: A. セキュリティ（CRITICAL） → B. DB Function → C. Migration → D. Edge Function テンプレート → E. 認証 → F. ログ → G. 型定義 → H. 命名規則

### Step 4: フィードバック出力

以下のフォーマットでフィードバックを出力する：

```markdown
## PR レビュー結果

### 概要
[変更内容の要約を1-2文で]

### 指摘事項

#### 🔴 Critical（マージ前に修正必須）
- **[ファイル名:行番号]** [指摘内容]
  - 理由: [なぜ問題か]
  - 修正案: [具体的な修正コード]

#### 🟡 Warning（改善推奨）
- **[ファイル名:行番号]** [指摘内容]
  - 修正案: [具体的な修正コード]

#### 🟢 Info（任意の改善）
- **[ファイル名:行番号]** [指摘内容]

### 良い点
- [規約に沿った実装を評価するコメント]
```

**重大度の基準：**

| レベル | 基準 | 例 |
|--------|------|-----|
| 🔴 Critical | セキュリティリスク、データ損失、認証不備 | `getUser()` 未使用、RLS未設定、SECURITY DEFINER漏れ |
| 🟡 Warning | 規約違反、保守性の低下 | ログ未実装、命名規則違反、型未使用、GRANT漏れ、CORS処理の残存 |
| 🟢 Info | 軽微な改善提案 | コメント追加、コード簡略化 |

## Additional Resources

- 詳細なチェックリストは [checklist.md](checklist.md) を参照

---
name: supabase-code-review
description: Supabase PRのコードレビューを規約に基づいて実施する。schemas、migration、Edge Function、DB Functionのレビュー、差分チェック、品質チェックを依頼された際に使用する。
---

# Supabase Code Review

PRの差分を規約に基づいてレビューし、問題点と改善提案をフィードバックする。
対象: 宣言的スキーマ（`schemas/`）、migration（SQL）、Edge Function（TypeScript/Deno）、DB Function（PostgreSQL）。

## When to Apply

- Supabase関連のPRコードレビューを依頼された時
- schemas / migration / Edge Function / DB Functionの品質チェックを依頼された時
- バックエンド側の「レビューして」「チェックして」と言われた時

## Review Workflow

### Step 1: 差分を取得

```bash
gh pr diff <PR番号>
# または
git diff main...HEAD
```

### Step 2: 変更ファイルを分類

| 優先度 | カテゴリ | ファイルパターン |
|--------|----------|------------------|
| 0 | 宣言的スキーマ（正本） | `backend/supabase/schemas/**/*.sql` |
| 1 | Migration（適用履歴） | `backend/supabase/migrations/*.sql` |
| 2 | Edge Function | `backend/supabase/functions/*/index.ts` |
| 3 | 共有モジュール | `backend/supabase/functions/_shared/**` |
| 4 | config | `backend/supabase/config.toml`（`verify_jwt` 等） |
| 5 | 型定義 | `database.types.ts` |
| 6 | 統合テスト | `backend/supabase/test/**` |

migration のみの diff は `db diff` 生成物として、対応する `schemas/` 変更の有無も確認する。

### Step 3: カテゴリ別レビュー

[checklist.md](checklist.md) に沿う。優先度: A. セキュリティ → B. schemas/DB Function → C. Migration → D. Edge handler → E. ログ → F. 型 → G. 命名

### Step 4: フィードバック出力

Critical / Warning / Info の3段階。Critical 例: RLS 未設定、JWT 未検証、`verify_jwt=false` なのに代替認証なし。

## Additional Resources

- [checklist.md](checklist.md)

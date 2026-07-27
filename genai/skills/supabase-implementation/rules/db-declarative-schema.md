---
title: Declarative Schema Workflow
impact: HIGH
impactDescription: schemas/ を正本とした宣言的スキーマ管理フロー
tags: supabase, declarative-schema, migrations
---

## Declarative Schema Workflow

`backend/supabase/schemas/` にデータベースの **最終形** を定義し、`supabase db diff` で差分マイグレーションを自動生成する運用です。

### なぜ使うか

| 従来 (migrations のみ) | 宣言的スキーマ |
|------------------------|----------------|
| 変更のたびに新規 migration ファイル | `schemas/` の git diff で最終形が見える |
| 関数修正 = 全文を新 migration に | `functions/*.sql` を直接編集 |
| 複数 migration を頭の中でマージ | 1 ファイル = 1 オブジェクトの正本 |

### ディレクトリ構成

```
backend/supabase/
├── schemas/           # 正本（最終形）
│   ├── 00_extensions.sql
│   ├── 01_types.sql
│   ├── tables/
│   ├── rls/
│   ├── functions/     # 1ファイル1関数（ファイル名＝関数名）
│   └── storage/
├── migrations/        # 適用履歴（db diff で生成）
└── config.toml        # schema_paths で適用順序を定義
```

### 変更手順

1. `schemas/` 内の SQL を編集（関数は `functions/<function_name>.sql`）
2. `supabase db diff -f <change_name>` で migration 生成
3. 生成 SQL をレビューして `supabase migration up` または `npm run sb:reset`
4. `npm run sb:types:gen` で型再生成

```powershell
cd backend/supabase
supabase db diff -f add_todo_tag_column
supabase migration up
```

### schemas/ に置かないもの

schema diff が捕捉できないものは **手書き migration** または **seed.sql** に残す:

- DML（INSERT / UPDATE / DELETE）
- cron job、Storage バケット作成
- 一部の RLS ALTER POLICY

### migrations/ との共存

- 既存 migration は本番履歴として **削除しない**
- 新規変更は `schemas/` 編集 → `db diff` → 新 migration
- 履歴が肥大化したら `supabase migration squash` を検討（DML は手動で戻す）

### チェックリスト

- [ ] テーブル・関数の変更は `schemas/` を編集した
- [ ] `supabase db diff` で migration を生成した
- [ ] 生成 migration をレビューした
- [ ] DML が必要なら手書き migration または seed に追加した
- [ ] `npm run sb:types:gen` を実行した

---
title: Supabase Directory Structure
impact: MEDIUM
impactDescription: Supabase プロジェクトのディレクトリ構成
tags: supabase, directory, structure
---

## Supabase Directory Structure

Supabase プロジェクトの標準的なディレクトリ構成です。

**標準構成：**

```
backend/supabase/
├── config.toml              # Supabaseプロジェクト設定
├── schemas/                 # 宣言的スキーマ（正本・最終形）★推奨
│   ├── 00_extensions.sql
│   ├── 01_types.sql
│   ├── tables/
│   ├── rls/
│   ├── functions/
│   └── storage/
├── migrations/              # 適用履歴（db diff で自動生成 + 既存履歴）
│   ├── 20250101000000_initial_schema.sql
│   └── ...
├── db-functions/            # Database Functions開発用（非推奨・schemas/ へ移行済み）
│   ├── sel_users.sql
│   └── ...
└── functions/               # Edge Functions
    ├── _shared/             # 共通モジュール・型定義
    │   ├── database.types.ts   # Supabase型定義（自動生成）
    │   ├── handler.ts         # Edge 共通 handler / HandlerContext
    │   ├── auth.ts            # getClaims ベース認証
    │   ├── logger.ts          # createRequestLogger
    │   ├── response.ts        # errorResponse 等
    │   ├── supabase.ts        # Supabaseクライアント
    │   ├── schemas/           # Zod リクエストスキーマ
    │   └── validation.ts      # メソッド検証等
    ├── get-user-data/
    │   └── index.ts
    ├── create-order/
    │   └── index.ts
    └── webhook-handler/
        └── index.ts
```

**_shared フォルダの役割：**

| モジュール | 役割 |
|-----------|------|
| `database.types.ts` | Supabase から自動生成される型定義 |
| `handler.ts` | `handler()` / `HandlerContext`（標準エントリ） |
| `auth.ts` | `getClaims` ベースの `getAuthUser` |
| `logger.ts` | `createRequestLogger` |
| `response.ts` | `errorResponse` / JSON レスポンス |
| `supabase.ts` | 認証付き / service_role クライアント |
| `schemas/` | Zod リクエストスキーマ |
| `validation.ts` | メソッド・ヘッダー検証 |

**Database Functions の管理方法：**

### パターン A: schemas/ + migrations（推奨）

`schemas/` に最終形を定義し、`supabase db diff` で migration を自動生成します。

| メリット | デメリット |
|----------|-----------|
| ✅ git diff で関数・テーブルの変化が追いやすい | ❌ 初回セットアップが必要 |
| ✅ 関数は `CREATE OR REPLACE` でファイル内編集 | ❌ DML は手書き migration が必要 |
| ✅ Supabase 標準の宣言的スキーマ | |

```bash
# 1. schemas/functions/ で関数を編集
# 2. 差分 migration を生成
cd backend/supabase
supabase db diff -f update_sel_todos_search

# 3. 適用
supabase migration up
```

> 詳細: [db-declarative-schema](db-declarative-schema.md)

### パターン B: migrations のみ（レガシー）

すべて `migrations/` フォルダで管理します（既存履歴として保持）。

| メリット | デメリット |
|----------|-----------|
| ✅ Supabase標準の構成 | ❌ 変更のたびに新規ファイルが増える |
| ✅ バージョン管理が確実 | ❌ 最終形を追うのが困難 |

> 💡 **推奨**: 新規変更はパターン A（schemas/）を使用。既存 migrations は削除しない。

**チェックリスト：**

- [ ] `schemas/` にスキーマ正本を配置
- [ ] `migrations/` に適用履歴を保持
- [ ] `functions/_shared/` に共通モジュールを配置
- [ ] `database.types.ts` が最新の状態
- [ ] Edge Functions は各機能ごとにフォルダを分割

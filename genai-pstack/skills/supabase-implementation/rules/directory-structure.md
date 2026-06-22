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
supabase/
├── config.toml              # Supabaseプロジェクト設定
├── migrations/              # データベースマイグレーション（スキーマ、関数、RLS）
│   ├── 20250101000000_initial_schema.sql
│   ├── 20250102000000_create_function_sel_users.sql
│   ├── 20250103000000_create_function_ins_order.sql
│   └── 20250104000000_add_rls_policies.sql
├── db-functions/            # Database Functions開発用（オプション）
│   ├── sel_users.sql
│   ├── ins_order.sql
│   └── upd_user_profile.sql
└── functions/               # Edge Functions
    ├── _shared/             # 共通モジュール・型定義
    │   ├── database.types.ts   # Supabase型定義（自動生成）
    │   ├── auth.ts            # 認証ヘルパー
    │   ├── logger.ts          # ログ出力ヘルパー
    │   ├── response.ts        # レスポンスヘルパー
    │   ├── supabase.ts        # Supabaseクライアント
    │   └── validation.ts      # バリデーションヘルパー
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
| `auth.ts` | 認証処理のヘルパー関数 |
| `logger.ts` | ログ出力のヘルパー関数 |
| `response.ts` | レスポンス生成のヘルパー関数 |
| `supabase.ts` | Supabase クライアントの初期化 |
| `validation.ts` | リクエストのバリデーション |

**Database Functions の管理方法：**

### パターン A: migrations のみで管理（推奨・シンプル）

すべて `migrations/` フォルダで管理します。

| メリット | デメリット |
|----------|-----------|
| ✅ Supabase標準の構成 | ❌ ファイル名がタイムスタンプ付きで検索しづらい |
| ✅ バージョン管理が確実 | ❌ 開発中に何度も作り直すと番号が増える |
| ✅ デプロイが自動化される | |

### パターン B: db-functions + migrations で管理（開発時）

開発用に `db-functions/` フォルダを作成し、完成したら `migrations/` に移します。

| メリット | デメリット |
|----------|-----------|
| ✅ 関数ごとにファイル分割で管理しやすい | ❌ 二重管理になる可能性 |
| ✅ 開発中は自由に編集できる | ❌ db-functions の内容が古くなるリスク |
| ✅ 完成したらマイグレーションとして確定 | |

**パターン B の運用方法：**

```bash
# 1. db-functions/ で開発・SQL Editorでテスト
# 2. 完成したらマイグレーションファイル作成
supabase migration new create_function_sel_users

# 3. db-functions/sel_users.sql の内容をマイグレーションファイルにコピー
# 4. マイグレーション適用
supabase db push
```

**db-functions フォルダの構成例：**

```
db-functions/
├── README.md                # 使い方の説明
├── users/
│   ├── sel_user_by_id.sql
│   ├── sel_users_by_role.sql
│   └── upd_user_profile.sql
├── orders/
│   ├── sel_order_details.sql
│   ├── ins_order.sql
│   └── upd_order_status.sql
└── common/
    └── get_current_user.sql
```

> 💡 **推奨**: 小規模プロジェクトはパターン A、中〜大規模プロジェクトはパターン B を採用

**チェックリスト：**

- [ ] `migrations/` にマイグレーションファイルを配置
- [ ] `functions/_shared/` に共通モジュールを配置
- [ ] `database.types.ts` が最新の状態
- [ ] Edge Functions は各機能ごとにフォルダを分割

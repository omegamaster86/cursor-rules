---
title: Supabase Directory Structure
impact: HIGH
impactDescription: バックエンド機能の一元管理
tags: supabase, edge-functions, migrations, database
---

## Supabase Directory Structure

`backend/supabase/`ディレクトリにSupabase関連のファイルを管理します。

**推奨構成：**

```
backend/supabase/            # backendディレクトリ配下に配置
├── config.toml              # Supabaseプロジェクト設定
├── seed.sql                 # Seedファイル
├── migrations/              # データベースマイグレーション
│   ├── 20250101000000_initial_setup.sql
│   └── 20250102000001_create_functions_todo.sql
└── functions/               # Edge Functions
    ├── deno.json            # Deno設定ファイル
    ├── _shared/             # 共通モジュール
    │   ├── auth.ts          # 認証ヘルパー
    │   ├── database.types.ts # DB型定義
    │   ├── logger.ts        # ロギング
    │   ├── response.ts      # レスポンスヘルパー
    │   ├── supabase.ts      # Supabaseクライアント
    │   └── validation.ts    # バリデーション
    ├── health/              # ヘルスチェック
    │   └── index.ts
    ├── create-todo/         # Todo作成
    │   └── index.ts
    └── get-todos/           # Todo取得
        └── index.ts
```

**マイグレーションファイル命名規則：**

```
YYYYMMDDHHMMSS_migration_name.sql
例: 20250101000000_initial_setup.sql
```

**Edge Function構成：**

```typescript
// backend/supabase/functions/create-todo/index.ts
import { createClient } from '../_shared/supabase.ts'
import { successResponse, errorResponse } from '../_shared/response.ts'

Deno.serve(async (req) => {
  const supabase = createClient(req)
  
  // ビジネスロジック実装
  // ...
  
  return successResponse({ success: true })
})
```

**ポイント：**

1. `backend/supabase/`は`backend/`ディレクトリ配下に配置
2. マイグレーションは時系列順に実行される
3. 各Edge Functionは独立したディレクトリに配置
4. `functions/_shared/`に共通モジュールを配置し、各Functionから再利用

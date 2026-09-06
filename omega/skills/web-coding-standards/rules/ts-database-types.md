---
title: Database Types Usage
impact: HIGH
impactDescription: database.types.ts からの型再定義
tags: typescript, supabase, database, types
---

## Database Types Usage

`database.types.ts` を使用したデータベース型の活用方法です。

**基本方針：**

- データベースから取得するデータは、`database.types.ts` の型定義をベースに作成する
- これにより、データベーススキーマの変更が型定義に自動的に反映される

**型定義ファイルの生成：**

```bash
# Supabase CLI で型を生成
npx --yes supabase gen types typescript --schema public --local > supabase/functions/_shared/database.types.ts && npx @biomejs/biome check --write supabase/functions/_shared/database.types.ts
npx --yes supabase gen types typescript --schema public --local > src/types/database.types.ts && npx @biomejs/biome check --write src/types/database.types.ts
```

**型の再定義パターン：**

```typescript
// src/types/index.ts
import type { Tables, TablesInsert, TablesUpdate } from "@/types/database.types";

// database.types.ts から再定義（推奨）
export type User = Tables<"m_user">;
export type UserInsert = TablesInsert<"m_user">;
export type UserUpdate = TablesUpdate<"m_user">;

// 複数テーブルの型
export type Todo = Tables<"t_todo">;
export type TodoInsert = TablesInsert<"t_todo">;
export type TodoUpdate = TablesUpdate<"t_todo">;
```

**データベースに関係ない型：**

```typescript
// src/types/index.ts
// API レスポンスなど、DBに関係ない型は直接定義
export type ApiResponse<T> = {
  success: boolean;
  data?: T;
  error?: string;
};

export type PaginationParams = {
  page: number;
  perPage: number;
};
```

**型定義の更新タイミング：**

| タイミング | 再生成が必要 |
|----------|------------|
| テーブル定義を変更した後 | ✅ |
| Database Functions を追加・変更した後 | ✅ |
| RLS ポリシーを変更した後 | ❌ |

**チェックリスト：**

- [ ] DB から取得するデータは `database.types.ts` から再定義
- [ ] スキーマ変更後は必ず型定義を再生成
- [ ] `Tables<>`, `TablesInsert<>`, `TablesUpdate<>` を活用

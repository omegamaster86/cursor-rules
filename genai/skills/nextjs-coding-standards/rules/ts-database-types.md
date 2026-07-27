---
title: Database Types Usage
impact: HIGH
impactDescription: database.types.ts と Zod 境界型の使い分け
tags: typescript, supabase, database, types
---

## Database Types Usage

`database.types.ts` と Zod スキーマの使い分けです。

**基本方針：**

| 用途 | 手段 |
|------|------|
| DB スキーマの TypeScript 表現 | `src/types/database.types.ts`（生成物） |
| Edge / API レスポンス・リクエスト境界 | `src/types/schemas/*.ts`（Zod + `z.infer`） |
| Server クライアントのジェネリクス | `createClient<Database>()` |

**型生成（第一手段）：**

```bash
# モノレポルートから（Web + Edge の database.types.ts を同期）
npm run sb:types:gen
```

**Zod 境界型（推奨・本番パターン）：**

```typescript
// src/types/schemas/todo.ts
export const TodoSchema = z.object({
  id: z.uuidv7(),
  title: z.string().min(1),
  // ...
});
export type TodoApi = z.infer<typeof TodoSchema>;

// callEdgeFunction で data を検証
await callEdgeFunction("get-todos", z.array(TodoSchema), { method: "GET", logger });
```

**Tables<> エイリアス（必要なとき）：**

```typescript
import type { Tables, TablesInsert } from "@/types/database.types";

export type TodoRow = Tables<"t_todo">;
export type TodoInsert = TablesInsert<"t_todo">;
```

`src/types/index.ts` への集約は必須ではない。

**更新タイミング：**

| タイミング | 再生成 |
|----------|--------|
| テーブル / DB Function 変更後 | ✅ `npm run sb:types:gen` |
| RLS のみ変更 | ❌ |

**チェックリスト：**

- [ ] API 境界は Zod schemas
- [ ] スキーマ変更後は `sb:types:gen`
- [ ] クライアントは `Database` ジェネリクスを付与

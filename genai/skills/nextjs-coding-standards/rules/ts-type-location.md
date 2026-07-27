---
title: TypeScript Type Location
impact: HIGH
impactDescription: 型定義の配置場所と Zod / database.types.ts の活用
tags: typescript, types, organization
---

## TypeScript Type Location

型定義の配置場所に関するルールです。

**基本方針：**

1. **API / ドメイン境界型**: `src/types/schemas/*.ts`（Zod スキーマ + `z.infer`）
2. **DB 生成型**: `src/types/database.types.ts`（`npm run sb:types:gen`）
3. **アクション状態・フォーム**: コロケーション `_actions/types.ts` / `schema.ts`
4. **ページ内だけの一時型**: そのファイル内に定義してよい

**`src/types/index.ts` は必須ではない。** 現行 starter では schemas 分割が標準。

**schemas の例：**

```typescript
// src/types/schemas/todo.ts
import { z } from "zod";
import { TodoPrioritySchema, TodoStatusSchema } from "./common";

export const TodoSchema = z.object({
  id: z.uuidv7(),
  title: z.string().min(1),
  description: z.string().nullable(),
  status: TodoStatusSchema,
  priority: TodoPrioritySchema,
});
export type TodoApi = z.infer<typeof TodoSchema>;
```

**アクション固有型：**

```typescript
// app/(dashboard)/todos/new/_actions/types.ts
export type CreateTodoState = {
  success: boolean;
  message: string;
  payload?: FormData;
  fieldErrors?: { title?: string[]; /* ... */ };
};
```

**type vs interface：**

```typescript
// ✅ type を優先
type User = { id: string; name: string };

// interface は宣言マージが必要な場合のみ
```

**チェックリスト：**

- [ ] Edge / API 境界型は `types/schemas/` の Zod
- [ ] アクション状態は `_actions/types.ts`
- [ ] DB 生型が必要なら `database.types.ts` を参照
- [ ] `type` を優先

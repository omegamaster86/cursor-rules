---
title: Supabase Data Access Architecture
impact: CRITICAL
impactDescription: 3層アーキテクチャによるデータアクセス規約
tags: supabase, architecture, data-access
---

## Supabase Data Access Architecture

Next.js における Supabase データアクセスの3層アーキテクチャです。

**階層構造：**

```
Page Component (Server Component)
  ↓ _apis / Server Action 呼び出し
Server Action / API module
  ↓ callEdgeFunction
Edge Function (Deno)
  ↓ Database Function / service_role オーケストレーション
Database (PostgreSQL)
```

**なぜ3層か？**

1. **セキュリティ**: ビジネスロジックをサーバーサイドに閉じ込める
2. **型安全性**: 各層で Zod / DB 型を定義して検証
3. **再利用性**: Edge Function は Web/Mobile で共有可能
4. **テスタビリティ**: 各層を独立してテスト可能

**標準スタック：**

| 層 | 実装 |
|----|------|
| 読み取り | `_apis/*.server.ts` + `handler` + `callEdgeFunction` |
| 書き込み | `_actions/*.ts` + `handler` + `validate` + `callEdgeFunction` |
| Supabase クライアント | `@/services/supabase/{server,client,edge-function,middleware,admin}` |

**実装例：**

```typescript
// 1. Page Component（Server Component）
// app/(dashboard)/todos/page.tsx
import { getTodos } from "./_apis/todo.server";

export default async function TodosPage() {
  const todos = await getTodos();
  return <TodoList todos={todos} />;
}
```

```typescript
// 2. 読み取り API
// app/(dashboard)/todos/_apis/todo.server.ts
"use server";

import { z } from "zod";
import { handler } from "@/services/handler";
import { callEdgeFunction } from "@/services/supabase/edge-function";
import { TodoSchema } from "@/types/schemas/todo";

export async function getTodos() {
  return handler(
    "getTodos",
    async (logger) => {
      return callEdgeFunction("get-todos", z.array(TodoSchema), {
        method: "GET",
        logger,
      });
    },
    {
      onError: () => {
        throw new Error("ToDoの取得に失敗しました");
      },
    },
  );
}
```

```typescript
// 3. 書き込み Server Action
// app/(dashboard)/todos/new/_actions/todo.ts
"use server";

import { actionError, handler, success, validate } from "@/services/handler";
import { callEdgeFunction } from "@/services/supabase/edge-function";
import { TodoSchema } from "@/types/schemas/todo";
import { CreateTodoFormSchema } from "./schema";
import type { CreateTodoState } from "./types";

export async function createTodo(
  _prevState: CreateTodoState,
  formData: FormData,
): Promise<CreateTodoState> {
  return handler(
    "createTodo",
    async (logger): Promise<CreateTodoState> => {
      const data = validate(
        CreateTodoFormSchema,
        {
          title: formData.get("title"),
          description: formData.get("description") || null,
          priority: formData.get("priority"),
        },
        logger,
      );

      await callEdgeFunction("create-todo", TodoSchema, {
        method: "POST",
        body: { ...data, dueDate: null },
        logger,
      });

      return success("ToDoを作成しました");
    },
    {
      onError: (error): CreateTodoState => actionError(error, formData),
    },
  );
}
```

**例外：**

- **Supabase Auth SDK**（signIn / signUp / resetPassword 等）は Edge Function 経由不要
- **OAuth / コールバック Route** は Auth フロー専用
- キャッシュ更新は `revalidatePath` でも、クライアント側 `router.push` + RSC 再取得でもよい（作成フローは後者が多い）

**チェックリスト：**

- [ ] Page は `_apis` / `_actions` を呼び出す（クライアントから直接テーブルアクセス禁止）
- [ ] Edge 呼び出しは `callEdgeFunction` を使う
- [ ] 本番アクションは `handler` + `validate` を使う
- [ ] Auth SDK 直接呼び出しは認証系に限定

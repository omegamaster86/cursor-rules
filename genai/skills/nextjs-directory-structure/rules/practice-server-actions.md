---
title: Server Actions Best Practices
impact: HIGH
impactDescription: フォーム処理のセキュリティと型安全性
tags: server-actions, forms, zod, validation, useActionState
---

## Server Actions Best Practices

Server Actions の設計と実装のベストプラクティスです。

**標準パターン（handler + callEdgeFunction）：**

```typescript
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

**状態型（`fieldErrors` + 任意の `payload`）：**

```typescript
export type CreateTodoState = {
  success: boolean;
  message: string;
  payload?: FormData;
  fieldErrors?: {
    title?: string[];
    description?: string[];
    priority?: string[];
  };
};
```

**キャッシュ更新：**

- `revalidatePath` でもよい
- 作成後に `router.push` で遷移し RSC 再取得するパターンも許容

**チェックリスト：**

- [ ] `handler` + `validate` + `callEdgeFunction`
- [ ] 状態は `fieldErrors`（`errors` ではない）
- [ ] スキーマ / 型は `schema.ts` / `types.ts` に分割

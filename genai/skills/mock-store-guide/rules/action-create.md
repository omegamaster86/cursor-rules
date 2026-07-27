---
title: Create Action Implementation
impact: HIGH
impactDescription: Server Action での作成処理の実装パターン
tags: mock-store, server-action, create
---

## Create Action Implementation

Server Action での作成処理の実装パターンです（dev-starter `demo/todos/new/_actions/todo-mock.ts` 準拠）。

**配置:**

```
app/demo/todos/new/_actions/
├── todo-mock.ts
├── schema.ts
└── types.ts
```

**基本パターン：**

```typescript
"use server";

import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";
import { createLogger } from "@/services/logger";
import {
  addMockTodo,
  getNextTodoIdAndIncrement,
} from "@/services/mock-store/stores/todo";
import type { MockTodo } from "@/types/demo-types";
import { CreateTodoFormSchema } from "./schema";
import type { CreateTodoState } from "./types";

export async function createTodoMock(
  _prevState: CreateTodoState,
  formData: FormData,
): Promise<CreateTodoState> {
  const logger = createLogger("createTodoMock");
  logger.start({
    title: formData.get("title"),
    priority: formData.get("priority"),
  });

  try {
    const validationResult = CreateTodoFormSchema.safeParse({
      title: formData.get("title"),
      description: formData.get("description") || null,
      priority: formData.get("priority"),
    });

    if (!validationResult.success) {
      const fieldErrors: Record<string, string[]> = {};
      for (const issue of validationResult.error.issues) {
        const path = issue.path[0] as string;
        fieldErrors[path] ??= [];
        fieldErrors[path].push(issue.message);
      }
      logger.warn("validation_failed", { fieldErrors });
      logger.end({ success: false, errorMessage: "入力内容が不正です" });
      return {
        success: false,
        message: "入力内容が不正です",
        payload: formData,
        fieldErrors,
      };
    }

    const validatedData = validationResult.data;
    const newTodo: MockTodo = {
      id: getNextTodoIdAndIncrement(),
      title: validatedData.title.trim(),
      description: validatedData.description?.trim() || null,
      priority: validatedData.priority,
      status: "pending",
      createdAt: new Date().toISOString(),
    };

    addMockTodo(newTodo);
    logger.info("todo_created", { todoId: newTodo.id });
    logger.end({ success: true });
  } catch (error) {
    logger.error(error, { context: "createTodoMock" });
    logger.end({
      success: false,
      errorMessage: "予期しないエラーが発生しました",
    });
    return {
      success: false,
      message: "予期しないエラーが発生しました",
      payload: formData,
    };
  }

  revalidatePath("/demo/todos");
  redirect("/demo/todos");
}
```

**ポイント:**

- Zod + `createLogger` + `fieldErrors` + `payload`（本番 handler に近い）
- `console.log` より logger を優先
- ルートネストに合わせて `_actions` は `demo/todos/new/_actions/` 等に置く

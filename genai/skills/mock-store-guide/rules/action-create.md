---
title: Create Action Implementation
impact: HIGH
impactDescription: Server Action での作成処理の実装パターン
tags: mock-store, server-action, create
---

## Create Action Implementation

Server Action での作成処理の実装パターンです。

**基本パターン：**

```typescript
// src/app/demo/todos/_actions/todo-mock.ts
"use server";

import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";
import {
  addMockTodo,
  getNextTodoIdAndIncrement,
} from "@/services/mock-store/stores/todo";
import type { ActionResponse, MockTodo } from "@/types/demo-types";

export async function createTodoMock(
  _prevState: ActionResponse,
  formData: FormData,
): Promise<ActionResponse> {
  try {
    // 1. バリデーション
    const title = formData.get("title") as string;
    if (!title) {
      return {
        success: false,
        message: "タイトルは必須です",
      };
    }

    // 2. 新規データ作成
    const newTodo: MockTodo = {
      id: getNextTodoIdAndIncrement(),
      title: title.trim(),
      description: (formData.get("description") as string) || null,
      priority: (formData.get("priority") as "low" | "medium" | "high") || "medium",
      status: "pending",
      createdAt: new Date().toISOString(),
    };

    // 3. ストアに追加
    addMockTodo(newTodo);
    console.log("[MOCK] TODO作成成功:", newTodo.id);

    // 4. キャッシュ無効化 & リダイレクト
    revalidatePath("/demo/todos");
    redirect("/demo/todos");
  } catch (error) {
    // redirect は Error をスローするため、
    // NEXT_REDIRECT エラーは再スロー
    if ((error as Error).message === "NEXT_REDIRECT") {
      throw error;
    }
    
    console.error("[MOCK] TODO作成エラー:", error);
    return {
      success: false,
      message: "予期しないエラーが発生しました",
    };
  }
}
```

**useActionState との統合：**

```tsx
// _components/TodoForm/index.tsx
"use client";

import { useActionState } from "react";
import { createTodoMock } from "../../_actions/todo-mock";

const initialState: ActionResponse = {
  success: false,
  message: "",
};

export function TodoForm() {
  const [state, formAction, isPending] = useActionState(
    createTodoMock,
    initialState
  );

  return (
    <form action={formAction}>
      <input name="title" disabled={isPending} />
      {state.message && !state.success && (
        <p className="text-red-500">{state.message}</p>
      )}
      <button type="submit" disabled={isPending}>
        {isPending ? "作成中..." : "作成"}
      </button>
    </form>
  );
}
```

**チェックリスト：**

- [ ] バリデーションを実装
- [ ] `getNextIdAndIncrement()` で ID を取得
- [ ] `revalidatePath()` でキャッシュを更新
- [ ] エラーハンドリングを実装
- [ ] ログを出力

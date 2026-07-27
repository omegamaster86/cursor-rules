---
title: Update Action Implementation
impact: HIGH
impactDescription: Server Action での更新処理の実装パターン
tags: mock-store, server-action, update
---

## Update Action Implementation

Server Action での更新処理の実装パターンです。

**基本パターン：**

```typescript
// src/app/demo/todos/_actions/todo-mock.ts
"use server";

import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";
import { updateMockTodo } from "@/services/mock-store/stores/todo";
import type { ActionResponse, MockTodo } from "@/types/demo-types";

export async function updateTodoMock(
  id: number,
  _prevState: ActionResponse,
  formData: FormData,
): Promise<ActionResponse> {
  try {
    // 1. バリデーション
    const title = formData.get("title") as string;
    if (!title?.trim()) {
      return {
        success: false,
        message: "タイトルは必須です",
      };
    }

    // 2. 更新データを作成
    const updates: Partial<Omit<MockTodo, "id" | "createdAt">> = {
      title: title.trim(),
      description: (formData.get("description") as string) || null,
      priority: (formData.get("priority") as MockTodo["priority"]) || "medium",
      status: (formData.get("status") as MockTodo["status"]) || "pending",
    };

    // 3. ストアを更新
    const updated = updateMockTodo(id, updates);
    
    if (!updated) {
      return {
        success: false,
        message: "TODOが見つかりません",
      };
    }

    console.log("[MOCK] TODO更新成功:", id);

    // 4. キャッシュ無効化 & リダイレクト
    revalidatePath("/demo/todos");
    redirect("/demo/todos");
  } catch (error) {
    if ((error as Error).message === "NEXT_REDIRECT") {
      throw error;
    }
    
    console.error("[MOCK] TODO更新エラー:", error);
    return {
      success: false,
      message: "予期しないエラーが発生しました",
    };
  }
}
```

**ID をバインドする方法：**

`id` などユーザーが編集しない値は `<input type="hidden">` ではなく `bind` で渡す。

```typescript
// Server Action に ID をバインド
export async function updateTodoMock(
  id: number,  // bind で渡される
  _prevState: ActionResponse,
  formData: FormData,
): Promise<ActionResponse> {
  // ...
}
```

**useActionState との統合：**

```tsx
// _components/TodoEditForm/index.tsx
"use client";

import { useActionState, useMemo } from "react";
import { updateTodoMock } from "../../_actions/todo-mock";
import type { MockTodo, ActionResponse } from "@/types/demo-types";

const initialState: ActionResponse = {
  success: false,
  message: "",
};

type Props = {
  todo: MockTodo;
};

export function TodoEditForm({ todo }: Props) {
  const boundAction = useMemo(
    () => updateTodoMock.bind(null, todo.id),
    [todo.id],
  );

  const [state, formAction, isPending] = useActionState(
    boundAction,
    initialState,
  );

  return (
    <form action={formAction}>
      {/* ❌ <input type="hidden" name="id" value={todo.id} /> は使わない */}
      <input
        name="title"
        defaultValue={todo.title}
        disabled={isPending}
      />
      <textarea
        name="description"
        defaultValue={todo.description ?? ""}
        disabled={isPending}
      />
      <select name="priority" defaultValue={todo.priority} disabled={isPending}>
        <option value="low">低</option>
        <option value="medium">中</option>
        <option value="high">高</option>
      </select>
      <select name="status" defaultValue={todo.status} disabled={isPending}>
        <option value="pending">未着手</option>
        <option value="in_progress">進行中</option>
        <option value="completed">完了</option>
      </select>
      
      {state.message && !state.success && (
        <p className="text-red-500">{state.message}</p>
      )}
      
      <button type="submit" disabled={isPending}>
        {isPending ? "更新中..." : "更新"}
      </button>
    </form>
  );
}
```

**チェックリスト：**

- [ ] 更新対象が存在するか確認
- [ ] 存在しない場合はエラーを返す
- [ ] `id` と `createdAt` は更新対象から除外
- [ ] `bind` で ID をバインド（`<input type="hidden">` は使わない）
- [ ] `boundAction` は `useMemo` で依存値と同期する
- [ ] `revalidatePath()` でキャッシュを更新

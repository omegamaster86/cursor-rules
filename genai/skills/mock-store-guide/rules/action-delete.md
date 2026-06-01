---
title: Delete Action Implementation
impact: HIGH
impactDescription: Server Action での削除処理の実装パターン
tags: mock-store, server-action, delete
---

## Delete Action Implementation

Server Action での削除処理の実装パターンです。

**基本パターン：**

```typescript
// src/app/demo/todos/_actions/todo-mock.ts
"use server";

import { revalidatePath } from "next/cache";
import { removeMockTodo } from "@/services/mock-store/stores/todo";
import type { ActionResponse } from "@/types/demo-types";

export async function deleteTodoMock(id: number): Promise<ActionResponse> {
  try {
    // 1. 削除を実行
    const deleted = removeMockTodo(id);
    
    // 2. 存在確認
    if (!deleted) {
      return {
        success: false,
        message: "TODOが見つかりません",
      };
    }

    console.log("[MOCK] TODO削除成功:", id);

    // 3. キャッシュ無効化
    revalidatePath("/demo/todos");
    
    return {
      success: true,
      message: "TODOを削除しました",
    };
  } catch (error) {
    console.error("[MOCK] TODO削除エラー:", error);
    return {
      success: false,
      message: "予期しないエラーが発生しました",
    };
  }
}
```

**削除ボタンの実装：**

```tsx
// _components/TodoDeleteButton/index.tsx
"use client";

import { useState, useTransition } from "react";
import { deleteTodoMock } from "../../_actions/todo-mock";

type Props = {
  todoId: number;
  todoTitle: string;
};

export function TodoDeleteButton({ todoId, todoTitle }: Props) {
  const [isPending, startTransition] = useTransition();
  const [error, setError] = useState<string | null>(null);

  const handleDelete = async () => {
    // 確認ダイアログ
    const confirmed = window.confirm(
      `「${todoTitle}」を削除しますか？`
    );
    if (!confirmed) return;

    startTransition(async () => {
      setError(null);
      const result = await deleteTodoMock(todoId);
      
      if (!result.success) {
        setError(result.message);
      }
    });
  };

  return (
    <div>
      <button
        onClick={handleDelete}
        disabled={isPending}
        className="text-red-600 hover:text-red-800 disabled:opacity-50"
      >
        {isPending ? "削除中..." : "削除"}
      </button>
      {error && <p className="text-red-500 text-sm">{error}</p>}
    </div>
  );
}
```

**form action での削除：**

```tsx
// _components/TodoItem/index.tsx
import { deleteTodoMock } from "../../_actions/todo-mock";

type Props = {
  todo: MockTodo;
};

export function TodoItem({ todo }: Props) {
  // ID をバインドした関数を作成
  const deleteWithId = deleteTodoMock.bind(null, todo.id);
  
  return (
    <div>
      <span>{todo.title}</span>
      <form action={deleteWithId}>
        <button type="submit" className="text-red-600">
          削除
        </button>
      </form>
    </div>
  );
}
```

**確認ダイアログ付きの form：**

```tsx
"use client";

import { useRef } from "react";
import { deleteTodoMock } from "../../_actions/todo-mock";

type Props = {
  todo: MockTodo;
};

export function TodoItemWithConfirm({ todo }: Props) {
  const formRef = useRef<HTMLFormElement>(null);
  const deleteWithId = deleteTodoMock.bind(null, todo.id);
  
  const handleSubmit = (e: React.FormEvent) => {
    const confirmed = window.confirm(`「${todo.title}」を削除しますか？`);
    if (!confirmed) {
      e.preventDefault();
    }
  };

  return (
    <form ref={formRef} action={deleteWithId} onSubmit={handleSubmit}>
      <button type="submit" className="text-red-600">
        削除
      </button>
    </form>
  );
}
```

**チェックリスト：**

- [ ] 削除対象が存在するか確認
- [ ] 存在しない場合はエラーを返す
- [ ] 確認ダイアログを表示
- [ ] `revalidatePath()` でキャッシュを更新
- [ ] リダイレクトは不要（一覧ページで実行されるため）

---
title: Server API Implementation
impact: MEDIUM
impactDescription: サーバーサイド API の実装パターン
tags: mock-store, api, server-component
---

## Server API Implementation

Server Component から呼び出すデータ取得用 API の実装パターンです。

**配置場所：**

`src/app/demo/{entity}/_apis/{entity}.server.ts`

**基本パターン：**

```typescript
// src/app/demo/todos/_apis/todo-mock.server.ts
"use server";

import {
  getMockTodos,
  getMockTodoById,
  getMockTodosFiltered,
  queryMockTodos,
} from "@/services/mock-store/stores/todo";
import type { MockTodo } from "@/types/demo-types";

/**
 * すべての TODO を取得
 */
export async function getTodosMock(): Promise<MockTodo[]> {
  const todos = getMockTodos();
  
  // 作成日時の降順でソート
  return [...todos].sort(
    (a, b) => new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime()
  );
}

/**
 * ID で TODO を取得
 */
export async function getTodoByIdMock(id: number): Promise<MockTodo | null> {
  return getMockTodoById(id) ?? null;
}

/**
 * ステータスで TODO をフィルタリング
 */
export async function getTodosByStatusMock(
  status: MockTodo["status"]
): Promise<MockTodo[]> {
  return getMockTodosFiltered({ status });
}
```

**ページネーション対応：**

```typescript
type PaginatedTodos = {
  todos: MockTodo[];
  total: number;
  page: number;
  perPage: number;
  totalPages: number;
};

/**
 * ページネーション付きで TODO を取得
 */
export async function getTodosPaginatedMock(
  page: number = 1,
  perPage: number = 10
): Promise<PaginatedTodos> {
  const result = queryMockTodos({ page, perPage });
  
  return {
    todos: result.items,
    total: result.total,
    page: result.page,
    perPage: result.perPage,
    totalPages: result.totalPages,
  };
}
```

**Server Component での使用：**

```tsx
// src/app/demo/todos/page.tsx
import { Suspense } from "react";
import { getTodosMock } from "./_apis/todo-mock.server";
import { TodoList } from "./_components/TodoList";

export default async function DemoTodosPage() {
  const todos = await getTodosMock();

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">TODOリスト（デモ）</h1>
      
      <Suspense fallback={<p>Loading...</p>}>
        <TodoList todos={todos} />
      </Suspense>
    </div>
  );
}
```

**詳細ページでの使用：**

```tsx
// src/app/demo/todos/[id]/page.tsx
import { notFound } from "next/navigation";
import { getTodoByIdMock } from "../_apis/todo-mock.server";

type Props = {
  params: Promise<{ id: string }>;
};

export default async function TodoDetailPage({ params }: Props) {
  const { id } = await params;
  const todo = await getTodoByIdMock(Number(id));

  if (!todo) {
    notFound();
  }

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold">{todo.title}</h1>
      <p>{todo.description}</p>
      <p>ステータス: {todo.status}</p>
      <p>優先度: {todo.priority}</p>
    </div>
  );
}
```

**検索パラメータ対応：**

```tsx
// src/app/demo/todos/page.tsx
import { getTodosPaginatedMock } from "./_apis/todo-mock.server";

type Props = {
  searchParams: Promise<{
    page?: string;
    status?: string;
  }>;
};

export default async function DemoTodosPage({ searchParams }: Props) {
  const { page, status } = await searchParams;
  const currentPage = Number(page) || 1;
  
  const { todos, total, totalPages } = await getTodosPaginatedMock(
    currentPage,
    10
  );

  return (
    <div>
      <TodoList todos={todos} />
      <Pagination
        currentPage={currentPage}
        totalPages={totalPages}
        total={total}
      />
    </div>
  );
}
```

**チェックリスト：**

- [ ] ファイル名は `*.server.ts` 接尾辞
- [ ] `"use server"` ディレクティブを追加
- [ ] 戻り値の型を明示
- [ ] ソートはデフォルトで降順
- [ ] 存在しない場合は `null` を返す

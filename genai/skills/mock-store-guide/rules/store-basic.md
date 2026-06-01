---
title: Basic Store Implementation
impact: HIGH
impactDescription: モックストアの基本実装パターン
tags: mock-store, demo, nextjs
---

## Basic Store Implementation

モックストアの基本的な実装パターンです。

**コアAPI：**

| 関数 | 説明 |
|------|------|
| `createMockStore<T>(key, initialData)` | ストアを作成または取得 |
| `resetMockStore(key, initialData)` | ストアを初期状態にリセット |
| `deleteMockStore(key)` | ストアを削除 |

**基本的なストア実装：**

```typescript
// src/services/mock-store/stores/todo.ts
import { createMockStore, resetMockStore } from "../index";
import type { MockTodo } from "@/types/demo-types";

// ストアの型定義
type TodoStoreData = {
  todos: MockTodo[];
  nextId: number;
};

// 初期データ
const initialTodoData: TodoStoreData = {
  todos: [
    {
      id: 1,
      title: "サンプルTODO",
      description: "説明文",
      priority: "medium",
      status: "pending",
      createdAt: new Date().toISOString(),
    },
  ],
  nextId: 2,
};

// ストア取得
function getTodoStore(): TodoStoreData {
  return createMockStore<TodoStoreData>("demo:todos", initialTodoData);
}

// CRUD操作
export function getMockTodos(): MockTodo[] {
  return getTodoStore().todos;
}

export function addMockTodo(todo: MockTodo): void {
  getTodoStore().todos.push(todo);
}

export function removeMockTodo(id: number): MockTodo | null {
  const store = getTodoStore();
  const index = store.todos.findIndex((t) => t.id === id);
  if (index === -1) return null;
  return store.todos.splice(index, 1)[0];
}

export function getNextTodoIdAndIncrement(): number {
  return getTodoStore().nextId++;
}

export function resetTodoStore(): void {
  resetMockStore("demo:todos", initialTodoData);
}
```

**ストアキーの命名規則：**

```typescript
// ✅ Good: 名前空間を使用
createMockStore("demo:todos", initialData);
createMockStore("demo:users", initialData);

// ❌ Bad: 衝突の可能性
createMockStore("todos", initialData);
```

**チェックリスト：**

- [ ] 型を明示的に定義
- [ ] 初期データを定数として定義
- [ ] ストアキーに名前空間を使用
- [ ] リセット関数を用意

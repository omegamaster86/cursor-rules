---
title: CRUD Operations
impact: HIGH
impactDescription: モックストアの CRUD 操作の実装
tags: mock-store, crud, demo
---

## CRUD Operations

モックストアの CRUD 操作の実装パターンです。

**全件取得（Read All）：**

```typescript
export function getMockTodos(): MockTodo[] {
  return getTodoStore().todos;
}
```

**ID で取得（Read One）：**

```typescript
export function getMockTodoById(id: number): MockTodo | undefined {
  return getTodoStore().todos.find((todo) => todo.id === id);
}
```

**作成（Create）：**

```typescript
export function addMockTodo(todo: MockTodo): void {
  getTodoStore().todos.push(todo);
  console.log("[MOCK TODO] 追加成功:", getTodoStore().todos.length, "件");
}

export function getNextTodoIdAndIncrement(): number {
  return getTodoStore().nextId++;
}
```

**更新（Update）：**

```typescript
export function updateMockTodo(
  id: number,
  updates: Partial<Omit<MockTodo, "id" | "createdAt">>,
): MockTodo | null {
  const store = getTodoStore();
  const index = store.todos.findIndex((todo) => todo.id === id);
  
  // 見つからない場合は null を返す
  if (index === -1) return null;
  
  // スプレッド演算子でマージ
  store.todos[index] = { ...store.todos[index], ...updates };
  return store.todos[index];
}
```

**削除（Delete）：**

```typescript
export function removeMockTodo(id: number): MockTodo | null {
  const store = getTodoStore();
  const index = store.todos.findIndex((todo) => todo.id === id);
  
  // 見つからない場合は null を返す
  if (index === -1) return null;
  
  // splice で削除して削除したアイテムを返す
  return store.todos.splice(index, 1)[0];
}
```

**完全な CRUD ストアの例：**

```typescript
// src/services/mock-store/stores/todo.ts
import { createMockStore, resetMockStore } from "../index";
import type { MockTodo } from "@/types/demo-types";

type TodoStoreData = {
  todos: MockTodo[];
  nextId: number;
};

const initialTodoData: TodoStoreData = {
  todos: [...],
  nextId: 2,
};

function getTodoStore(): TodoStoreData {
  return createMockStore<TodoStoreData>("demo:todos", initialTodoData);
}

// Read All
export function getMockTodos(): MockTodo[] {
  return getTodoStore().todos;
}

// Read One
export function getMockTodoById(id: number): MockTodo | undefined {
  return getTodoStore().todos.find((t) => t.id === id);
}

// Create
export function addMockTodo(todo: MockTodo): void {
  getTodoStore().todos.push(todo);
}

// Update
export function updateMockTodo(id: number, updates: Partial<MockTodo>): MockTodo | null {
  const store = getTodoStore();
  const index = store.todos.findIndex((t) => t.id === id);
  if (index === -1) return null;
  store.todos[index] = { ...store.todos[index], ...updates };
  return store.todos[index];
}

// Delete
export function removeMockTodo(id: number): MockTodo | null {
  const store = getTodoStore();
  const index = store.todos.findIndex((t) => t.id === id);
  if (index === -1) return null;
  return store.todos.splice(index, 1)[0];
}

// ID発番
export function getNextTodoIdAndIncrement(): number {
  return getTodoStore().nextId++;
}

// リセット
export function resetTodoStore(): void {
  resetMockStore("demo:todos", initialTodoData);
}
```

**チェックリスト：**

- [ ] 見つからない場合は `null` を返す
- [ ] 更新では `id` や `createdAt` を除外
- [ ] 削除では `splice` を使用
- [ ] 各操作でログを出力

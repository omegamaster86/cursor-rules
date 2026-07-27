---
title: Type Definitions
impact: HIGH
impactDescription: 型定義の明示
tags: mock-store, typescript, types
---

## Type Definitions

モックストアにおける型定義のベストプラクティスです。

**基本ルール：**

ストアの型を明示的に定義します。

**エンティティ型の定義：**

```typescript
// src/types/demo-types.ts

/**
 * モック TODO の型定義
 */
export type MockTodo = {
  id: number;
  title: string;
  description: string | null;
  priority: "low" | "medium" | "high";
  status: "pending" | "in_progress" | "completed" | "cancelled";
  createdAt: string;
};

/**
 * Server Actions の汎用レスポンス型
 */
export type ActionResponse<T = unknown> = {
  success: boolean;
  message: string;
  data?: T;
  error?: string;
};
```

**ストアデータ型の定義：**

```typescript
// src/services/mock-store/stores/todo.ts

/**
 * TODO ストアの内部データ型
 */
type TodoStoreData = {
  todos: MockTodo[];
  nextId: number;
};
```

**良い例：**

```typescript
// ✅ Good: ストアの型を明示的に定義
type TodoStoreData = {
  todos: MockTodo[];
  nextId: number;
};

const initialData: TodoStoreData = {
  todos: [],
  nextId: 1,
};

function getTodoStore(): TodoStoreData {
  return createMockStore<TodoStoreData>("demo:todos", initialData);
}
```

**悪い例：**

```typescript
// ❌ Bad: 型推論に頼る（変更時に問題が発生しやすい）
const store = createMockStore("demo:todos", {
  todos: [],
  nextId: 1,
});

// ❌ Bad: any を使用
const store = createMockStore<any>("demo:todos", initialData);
```

**関数の戻り値型：**

```typescript
// ✅ Good: 戻り値型を明示
export function getMockTodos(): MockTodo[] {
  return getTodoStore().todos;
}

export function getMockTodoById(id: number): MockTodo | undefined {
  return getTodoStore().todos.find((t) => t.id === id);
}

export function updateMockTodo(
  id: number,
  updates: Partial<Omit<MockTodo, "id" | "createdAt">>
): MockTodo | null {
  // ...
}

export function removeMockTodo(id: number): MockTodo | null {
  // ...
}
```

**Partial と Omit の活用：**

```typescript
// 更新時は id と createdAt を除外
type TodoUpdates = Partial<Omit<MockTodo, "id" | "createdAt">>;

export function updateMockTodo(id: number, updates: TodoUpdates): MockTodo | null {
  // ...
}

// 作成時は id を省略（自動採番）
type NewTodoInput = Omit<MockTodo, "id">;

export function createMockTodo(input: NewTodoInput): MockTodo {
  return {
    id: getNextTodoIdAndIncrement(),
    ...input,
  };
}
```

**型のエクスポート：**

```typescript
// src/types/index.ts
export type { ActionResponse, MockTodo } from "./demo-types";

// 使用時
import type { MockTodo, ActionResponse } from "@/types";
```

**チェックリスト：**

- [ ] エンティティ型を `types/demo-types.ts` に定義
- [ ] ストアデータ型を明示的に定義
- [ ] 関数の戻り値型を明示
- [ ] `Partial`, `Omit` を適切に活用
- [ ] 型を `types/index.ts` から再エクスポート

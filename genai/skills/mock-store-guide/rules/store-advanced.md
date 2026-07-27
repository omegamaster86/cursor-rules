---
title: Advanced Store Operations
impact: MEDIUM
impactDescription: 検索・フィルタリング・ページネーションの実装
tags: mock-store, search, filter, pagination
---

## Advanced Store Operations

検索、フィルタリング、ページネーションを含むストア操作の実装パターンです。

**フィルタリング：**

```typescript
/**
 * ステータスでフィルタリング
 */
export function getMockTodosByStatus(status: MockTodo["status"]): MockTodo[] {
  return getTodoStore().todos.filter((todo) => todo.status === status);
}

/**
 * 優先度でフィルタリング
 */
export function getMockTodosByPriority(priority: MockTodo["priority"]): MockTodo[] {
  return getTodoStore().todos.filter((todo) => todo.priority === priority);
}

/**
 * 複数条件でフィルタリング
 */
export function getMockTodosFiltered(filters: {
  status?: MockTodo["status"];
  priority?: MockTodo["priority"];
}): MockTodo[] {
  let todos = getTodoStore().todos;
  
  if (filters.status) {
    todos = todos.filter((t) => t.status === filters.status);
  }
  if (filters.priority) {
    todos = todos.filter((t) => t.priority === filters.priority);
  }
  
  return todos;
}
```

**検索：**

```typescript
/**
 * タイトルと説明で検索
 */
export function searchMockTodos(query: string): MockTodo[] {
  if (!query.trim()) return getTodoStore().todos;
  
  const lowerQuery = query.toLowerCase();
  return getTodoStore().todos.filter((todo) =>
    todo.title.toLowerCase().includes(lowerQuery) ||
    todo.description?.toLowerCase().includes(lowerQuery)
  );
}
```

**ソート：**

```typescript
/**
 * 作成日時でソート
 */
export function getMockTodosSorted(order: "asc" | "desc" = "desc"): MockTodo[] {
  const todos = [...getTodoStore().todos];
  
  return todos.sort((a, b) => {
    const diff = new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime();
    return order === "desc" ? diff : -diff;
  });
}

/**
 * 優先度でソート
 */
export function getMockTodosSortedByPriority(): MockTodo[] {
  const priorityOrder = { high: 0, medium: 1, low: 2 };
  const todos = [...getTodoStore().todos];
  
  return todos.sort((a, b) => priorityOrder[a.priority] - priorityOrder[b.priority]);
}
```

**ページネーション：**

```typescript
type PaginatedResult<T> = {
  items: T[];
  total: number;
  page: number;
  perPage: number;
  totalPages: number;
};

/**
 * ページネーション付きで取得
 */
export function getMockTodosPaginated(
  page: number = 1,
  perPage: number = 10
): PaginatedResult<MockTodo> {
  const all = getTodoStore().todos;
  const total = all.length;
  const totalPages = Math.ceil(total / perPage);
  
  const start = (page - 1) * perPage;
  const end = start + perPage;
  const items = all.slice(start, end);
  
  return {
    items,
    total,
    page,
    perPage,
    totalPages,
  };
}
```

**複合クエリ：**

```typescript
type TodoQuery = {
  status?: MockTodo["status"];
  priority?: MockTodo["priority"];
  search?: string;
  sortBy?: "createdAt" | "priority";
  sortOrder?: "asc" | "desc";
  page?: number;
  perPage?: number;
};

/**
 * 複合条件でクエリ
 */
export function queryMockTodos(query: TodoQuery): PaginatedResult<MockTodo> {
  let todos = getTodoStore().todos;
  
  // フィルタリング
  if (query.status) {
    todos = todos.filter((t) => t.status === query.status);
  }
  if (query.priority) {
    todos = todos.filter((t) => t.priority === query.priority);
  }
  
  // 検索
  if (query.search) {
    const lowerSearch = query.search.toLowerCase();
    todos = todos.filter((t) =>
      t.title.toLowerCase().includes(lowerSearch)
    );
  }
  
  // ソート
  todos = [...todos];
  if (query.sortBy === "priority") {
    const order = { high: 0, medium: 1, low: 2 };
    todos.sort((a, b) => order[a.priority] - order[b.priority]);
  } else {
    todos.sort((a, b) => 
      new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime()
    );
  }
  if (query.sortOrder === "asc") todos.reverse();
  
  // ページネーション
  const page = query.page ?? 1;
  const perPage = query.perPage ?? 10;
  const total = todos.length;
  const start = (page - 1) * perPage;
  
  return {
    items: todos.slice(start, start + perPage),
    total,
    page,
    perPage,
    totalPages: Math.ceil(total / perPage),
  };
}
```

**チェックリスト：**

- [ ] フィルタリングは元の配列を変更しない
- [ ] ソートでは配列のコピーを作成
- [ ] ページネーションでは `totalPages` を計算
- [ ] 複合クエリはオプショナルなパラメータ

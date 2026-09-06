---
title: Server/Client Component Separation
impact: CRITICAL
impactDescription: パフォーマンスとバンドルサイズの最適化
tags: server-components, client-components, use-client, separation
---

## Server/Client Component Separation

Server ComponentsとClient Componentsの適切な分離方法です。

**基本原則：**

1. **デフォルトはServer Components** - 可能な限りServer Componentsを使用
2. **Client Componentsは最小化** - インタラクティブな部分のみ
3. **明確な分離** - ページ（Server）とフォーム（Client）を分ける

**Incorrect（全体がClient Component）:**

```tsx
// ❌ page.tsx全体がClient Component
'use client'

export default function TodosPage() {
  const [todos, setTodos] = useState([])
  
  useEffect(() => {
    fetchTodos().then(setTodos)
  }, [])
  
  return (
    <div>
      <h1>Todos</h1>
      <TodoList todos={todos} />
      <AddTodoForm />
    </div>
  )
}
```

**Correct（必要な部分のみClient）:**

```tsx
// page.tsx - Server Component
export default async function TodosPage() {
  // サーバーサイドでデータフェッチ
  const todos = await getTodos()
  
  return (
    <div>
      <h1>Todos</h1>
      {/* インタラクティブな部分のみClient Component */}
      <TodoList todos={todos} />
      <AddTodoButton />
    </div>
  )
}

// _components/TodoList/index.tsx - Client Component
'use client'

export function TodoList({ todos }: { todos: Todo[] }) {
  const [filter, setFilter] = useState('all')
  
  // フィルタリングなどのインタラクティブなロジック
  const filteredTodos = todos.filter(/* ... */)
  
  return (
    <div>
      <FilterButtons value={filter} onChange={setFilter} />
      {filteredTodos.map(todo => <TodoItem key={todo.id} todo={todo} />)}
    </div>
  )
}
```

**Server Componentに適したもの：**

| 用途 | 理由 |
|------|------|
| データフェッチ | サーバーサイドで直接DB/APIアクセス |
| 静的コンテンツ | バンドルサイズ削減 |
| SEO重要なコンテンツ | 初期HTMLに含まれる |
| レイアウト | 状態を持たない |

**Client Componentに適したもの：**

| 用途 | 理由 |
|------|------|
| フォーム入力 | ユーザーインタラクション |
| ドロップダウン/モーダル | UIの状態管理 |
| クリックハンドラ | イベント処理 |
| useStateが必要な場合 | React Hooks |
| ブラウザAPIを使用 | window/document |

**'use client'の配置：**

```tsx
// ✅ ファイルの最上部に配置
'use client'

import { useState } from 'react'

export function InteractiveComponent() {
  // ...
}
```

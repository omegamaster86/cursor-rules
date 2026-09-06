---
title: Server/Client Component Separation
impact: HIGH
impactDescription: Server Component と Client Component の分離
tags: react, next.js, server-components, client-components
---

## Server/Client Component Separation

Server Component と Client Component の明確な分離ルールです。

### 基本原則

| Component | 用途 |
|-----------|-----|
| Server Component | ページレイアウト、静的コンテンツ、データフェッチ |
| Client Component | フォーム、ユーザーインタラクション、状態管理 |

### 良い例：Server と Client の分離

```typescript
// ✅ 良い例：Server ComponentとClient Componentを分離
// page.tsx (Server Component)
import { NewTodoForm } from "./_components/NewTodoForm";
import { getTodos } from "./_apis/todo.server";

export default async function TodoPage() {
  const todos = await getTodos(); // サーバーでデータ取得

  return (
    <div>
      <h1>ToDo一覧</h1>
      <NewTodoForm />        {/* Client Component */}
      <TodoList todos={todos} />
    </div>
  );
}
```

```typescript
// _components/NewTodoForm/index.tsx (Client Component)
"use client";

export function NewTodoForm() {
  // フォームのロジック（状態管理、イベントハンドラ）
}
```

### 悪い例：ページ全体を Client Component にする

```typescript
// ❌ 悪い例：ページ全体をClient Componentにする
"use client";

export default function TodoPage() {
  // すべてのコンテンツがClient Componentになってしまう
  // サーバーサイドレンダリングの利点が失われる
}
```

### Client Component が必要なケース

以下の機能を使用する場合は Client Component が必要です：

| 機能 | 例 |
|-----|-----|
| useState | フォーム入力、UI状態 |
| useEffect | 外部APIとの同期 |
| useActionState | Server Action との統合 |
| イベントハンドラ | onClick, onChange |
| ブラウザ API | localStorage, window |

### Server Component のままでいいケース

```typescript
// ✅ Server Component のまま
// - データの表示のみ
// - 静的なコンテンツ
// - async/await でのデータ取得

export default async function UserPage({ params }: { params: { id: string } }) {
  const user = await getUser(params.id);

  return (
    <div>
      <h1>{user.name}</h1>
      <p>{user.email}</p>
    </div>
  );
}
```

### データフェッチコロケーション

データは必要なコンポーネントで直接フェッチします。

```typescript
// ✅ 良い例：データが必要なコンポーネントで直接フェッチ
async function UserProfile({ userId }: { userId: number }) {
  const userData = await getUserData(userId);

  return (
    <div>
      <h1>{userData.name}</h1>
      <UserStats userId={userId} />
    </div>
  );
}

async function UserStats({ userId }: { userId: number }) {
  // Request Memoization により重複リクエストは自動的に排除
  const userData = await getUserData(userId);

  return <p>投稿数: {userData.postCount}</p>;
}
```

```typescript
// ❌ 悪い例：Props Drilling
async function UserProfile({ userId }: { userId: number }) {
  const userData = await getUserData(userId);

  return (
    <div>
      <h1>{userData.name}</h1>
      <UserStats userData={userData} /> {/* propsで渡す */}
    </div>
  );
}
```

**チェックリスト：**

- [ ] ページレイアウトは Server Component
- [ ] フォームは Client Component
- [ ] `"use client"` は必要なコンポーネントのみに記載
- [ ] データフェッチは必要なコンポーネントで直接実行

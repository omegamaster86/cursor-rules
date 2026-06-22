---
title: Supabase Data Access Architecture
impact: CRITICAL
impactDescription: 3層アーキテクチャによるデータアクセス規約
tags: supabase, architecture, data-access
---

## Supabase Data Access Architecture

Next.js における Supabase データアクセスの3層アーキテクチャです。

**階層構造：**

```
Page Component (Server Component)
  ↓ Server Action 呼び出し
Server Action
  ↓ Edge Function 呼び出し
Edge Function (Deno)
  ↓ Database Function 呼び出し
Database Function (PostgreSQL)
```

**なぜ3層か？**

1. **セキュリティ**: ビジネスロジックをサーバーサイドに閉じ込める
2. **型安全性**: 各層で型を定義して検証
3. **再利用性**: Edge Function は Web/Mobile で共有可能
4. **テスタビリティ**: 各層を独立してテスト可能

**実装例：**

```typescript
// 1. Page Component（Server Component）
// app/todos/page.tsx
import { getTodos } from "./_apis/todo.server";

export default async function TodosPage() {
  const todos = await getTodos();
  return <TodoList todos={todos} />;
}
```

```typescript
// 2. API（Server Action 相当）
// app/todos/_apis/todo.server.ts
"use server";

import { createClient } from "@/services/supabase-service/server";

export async function getTodos() {
  const supabase = await createClient();
  
  // 認証検証
  const { data: { user }, error: authError } = await supabase.auth.getUser();
  if (authError || !user) throw new Error("認証が必要です");
  
  // Edge Function 呼び出し
  const { data, error } = await supabase.functions.invoke("get-todos");
  if (error) throw new Error(error.message);
  
  return data.data;
}
```

```typescript
// 3. Server Action（データ変更）
// app/todos/_actions/todo.ts
"use server";

import { createClient } from "@/services/supabase-service/server";
import { revalidatePath } from "next/cache";

export async function createTodo(formData: FormData) {
  const supabase = await createClient();
  
  const { data: { user } } = await supabase.auth.getUser();
  if (!user) return { success: false, error: "認証が必要です" };
  
  const { error } = await supabase.functions.invoke("create-todo", {
    body: { title: formData.get("title") },
  });
  
  if (error) return { success: false, error: error.message };
  
  revalidatePath("/todos");
  return { success: true };
}
```

**チェックリスト：**

- [ ] Page Component は Server Action / API を呼び出す
- [ ] Server Action は Edge Function を呼び出す
- [ ] データ変更後は `revalidatePath` でキャッシュ更新
- [ ] 各層で認証・バリデーションを実施

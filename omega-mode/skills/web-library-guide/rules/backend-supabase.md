---
title: Supabase SDK Integration
impact: HIGH
impactDescription: Supabase クライアントの設定と認証・データアクセス
tags: supabase, backend, authentication, database
---

## Supabase SDK Integration

Supabase SDK を使用したバックエンド連携のベストプラクティスです。

**インストール：**

```bash
npm install @supabase/supabase-js @supabase/ssr
```

**サーバーサイドクライアント（Server Components / Server Actions）：**

```typescript
// services/supabase-service/server.ts
import { createServerClient } from '@supabase/ssr'
import { cookies } from 'next/headers'

export async function createClient() {
  const cookieStore = await cookies()

  return createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        getAll() {
          return cookieStore.getAll()
        },
        setAll(cookiesToSet) {
          try {
            cookiesToSet.forEach(({ name, value, options }) =>
              cookieStore.set(name, value, options)
            )
          } catch {
            // Server Component では無視
          }
        },
      },
    }
  )
}
```

**クライアントサイドクライアント：**

```typescript
// services/supabase-service/client.ts
import { createBrowserClient } from '@supabase/ssr'

export function createClient() {
  return createBrowserClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
  )
}
```

**Server Component でのデータ取得：**

```tsx
// app/todos/page.tsx
import { createClient } from '@/services/supabase-service/server'

export default async function TodosPage() {
  const supabase = await createClient()
  
  const { data: todos, error } = await supabase
    .from('todos')
    .select('*')
    .order('created_at', { ascending: false })

  if (error) {
    throw new Error('Todoの取得に失敗しました')
  }

  return (
    <ul>
      {todos.map((todo) => (
        <li key={todo.id}>{todo.title}</li>
      ))}
    </ul>
  )
}
```

**Edge Functions の呼び出し：**

```typescript
// app/todos/_actions/todo.ts
'use server'

import { createClient } from '@/services/supabase-service/server'
import { revalidatePath } from 'next/cache'

export async function createTodo(formData: FormData) {
  const supabase = await createClient()
  
  const { data, error } = await supabase.functions.invoke('create-todo', {
    body: {
      title: formData.get('title'),
      description: formData.get('description'),
    },
  })

  if (error) {
    return { success: false, message: error.message }
  }

  revalidatePath('/todos')
  return { success: true, data }
}
```

**認証状態の取得：**

```typescript
// Server Component
import { createClient } from '@/services/supabase-service/server'

export async function getCurrentUser() {
  const supabase = await createClient()
  const { data: { user } } = await supabase.auth.getUser()
  return user
}

// Client Component
'use client'
import { createClient } from '@/services/supabase-service/client'
import { useEffect, useState } from 'react'
import type { User } from '@supabase/supabase-js'

export function useUser() {
  const [user, setUser] = useState<User | null>(null)
  const supabase = createClient()

  useEffect(() => {
    const { data: { subscription } } = supabase.auth.onAuthStateChange(
      (_, session) => setUser(session?.user ?? null)
    )
    return () => subscription.unsubscribe()
  }, [supabase])

  return user
}
```

**チェックリスト：**

- [ ] サーバー/クライアントで適切なクライアントを使用
- [ ] 環境変数は `NEXT_PUBLIC_` プレフィックスを確認
- [ ] Server Component でデータ取得、Server Action でデータ変更
- [ ] Edge Functions でビジネスロジックを処理
- [ ] `revalidatePath` でキャッシュを適切に更新

---
title: API Clients Colocation
impact: HIGH
impactDescription: API呼び出しの一貫性とセキュリティ
tags: api-clients, colocation, server, client
---

## API Clients Colocation

APIクライアントはコロケーション原則に従い、ページ固有は`_apis/`、共通は`apis/`に配置します。

**Incorrect（すべて共通に配置）:**

```
apis/
├── auth.ts        # loginページでしか使わない
├── users.ts
├── todos.ts
└── orders.ts
# 使用場所が不明確
```

**Correct（コロケーション原則に従う）:**

```
src/
├── apis/                      # 複数ページで使用
│   ├── users.server.ts
│   └── users.client.ts
└── app/
    └── login/
        ├── _apis/             # ページ固有
        │   ├── auth.server.ts
        │   └── auth.client.ts
        └── page.tsx
```

**サーバー/クライアント分離：**

```typescript
// app/login/_apis/auth.server.ts (サーバーサイド用)
'use server'

import { createClient } from '@/services/supabase-service/server'

export async function loginUser(email: string, password: string) {
  const supabase = await createClient()
  return await supabase.functions.invoke('auth-login', {
    body: { email, password }
  })
}

export async function logoutUser() {
  const supabase = await createClient()
  return await supabase.auth.signOut()
}
```

```typescript
// app/login/_apis/auth.client.ts (クライアントサイド用 - GETのみ)
'use client'

import { createClient } from '@/services/supabase-service/client'

export async function getLoginStatus() {
  const supabase = createClient()
  const { data } = await supabase.auth.getSession()
  return data.session
}
```

**命名規則：**

| ファイル名 | 用途 |
|-----------|------|
| `[resource].server.ts` | サーバー用（全HTTPメソッド） |
| `[resource].client.ts` | クライアント用（**GETのみ**） |

**セキュリティルール：**
- クライアント側ではGETメソッドのみ使用
- データ変更（POST/PUT/DELETE）はServer Actionsで実行

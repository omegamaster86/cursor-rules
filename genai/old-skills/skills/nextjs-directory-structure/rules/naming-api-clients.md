---
title: API Client Naming Convention
impact: HIGH
impactDescription: サーバー/クライアント分離の明確化
tags: naming, api-clients, server, client, convention
---

## API Client Naming Convention

APIクライアントファイルの命名規則です。サーバー用とクライアント用を明確に分離します。

**命名パターン：**

```
[resource].server.ts    # サーバー用APIクライアント
[resource].client.ts    # クライアント用APIクライアント
```

**Incorrect（曖昧な命名）:**

```
_apis/
├── auth.ts           # ❌ サーバー用？クライアント用？
├── authApi.ts        # ❌ サーバー用？クライアント用？
└── AuthService.ts    # ❌ サーバー用？クライアント用？
```

**Correct（明確な分離）:**

```
_apis/
├── auth.server.ts    # ✅ サーバー用
└── auth.client.ts    # ✅ クライアント用
```

**ファイルの内容：**

```typescript
// auth.server.ts - サーバーサイド専用
'use server'

import { createClient } from '@/services/supabase-service/server'

// 全HTTPメソッドが使用可能
export async function loginUser(email: string, password: string) { }
export async function logoutUser() { }
export async function updateProfile(data: ProfileData) { }  // ✅ OK
```

```typescript
// auth.client.ts - クライアントサイド専用
'use client'

import { createClient } from '@/services/supabase-service/client'

// GETメソッドのみ使用可能
export async function getLoginStatus() { }
export async function getCurrentUser() { }
// export async function updateProfile() { }  // ❌ NG - Server Actionsを使用
```

**共通APIクライアント（apis/）：**

```
apis/
├── users.server.ts       # ユーザー関連（サーバー）
├── users.client.ts       # ユーザー関連（クライアント）
├── orders.server.ts      # 注文関連（サーバー）
└── orders.client.ts      # 注文関連（クライアント）
```

**リソース名の付け方：**

| リソース | ファイル名 |
|---------|-----------|
| 認証 | `auth.server.ts` / `auth.client.ts` |
| ユーザー | `users.server.ts` / `users.client.ts` |
| Todo | `todos.server.ts` / `todos.client.ts` |
| 注文 | `orders.server.ts` / `orders.client.ts` |

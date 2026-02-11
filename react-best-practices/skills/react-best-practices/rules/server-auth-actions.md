---
title: Server Actions も API ルート同様に認証する
impact: CRITICAL
impactDescription: prevents unauthorized access to server mutations
tags: server, server-actions, authentication, security, authorization
---

## Server Actions も API ルート同様に認証する

このルールの目的はパフォーマンスと保守性の向上です。以下に非推奨例と推奨例を示します。

**影響: CRITICAL（サーバー更新処理への不正アクセスを防ぐ）**

Server Actions（`"use server"` を持つ関数）は API ルートと同様に公開エンドポイントです。各 Server Action **内部**で必ず認証・認可を検証してください。middleware / layout ガード / ページレベル検査だけに依存すると、直接呼び出しを防げません。

Next.js 公式にも、Server Actions は公開 API エンドポイントと同等のセキュリティ前提で扱い、ユーザーがその更新を実行可能か検証すべきだと明記されています。

**Incorrect（no authentication check):**

```typescript
'use server'

export async function deleteUser(userId: string) {
  // Anyone can call this! No auth check
  await db.user.delete({ where: { id: userId } })
  return { success: true }
}
```

**Correct（authentication inside the action):**

```typescript
'use server'

import { verifySession } from '@/lib/auth'
import { unauthorized } from '@/lib/errors'

export async function deleteUser(userId: string) {
  // Always check auth inside the action
  const session = await verifySession()
  
  if (!session) {
    throw unauthorized('Must be logged in')
  }
  
  // Check authorization too
  if (session.user.role !== 'admin' && session.user.id !== userId) {
    throw unauthorized('Cannot delete other users')
  }
  
  await db.user.delete({ where: { id: userId } })
  return { success: true }
}
```

**入力検証を組み合わせる場合:**

```typescript
'use server'

import { verifySession } from '@/lib/auth'
import { z } from 'zod'

const updateProfileSchema = z.object({
  userId: z.string().uuid(),
  name: z.string().min(1).max(100),
  email: z.string().email()
})

export async function updateProfile(data: unknown) {
  // Validate input first
  const validated = updateProfileSchema.parse(data)
  
  // Then authenticate
  const session = await verifySession()
  if (!session) {
    throw new Error('Unauthorized')
  }
  
  // Then authorize
  if (session.user.id !== validated.userId) {
    throw new Error('Can only update own profile')
  }
  
  // Finally perform the mutation
  await db.user.update({
    where: { id: validated.userId },
    data: {
      name: validated.name,
      email: validated.email
    }
  })
  
  return { success: true }
}
```

参考: [https://nextjs.org/docs/app/guides/authentication](https://nextjs.org/docs/app/guides/authentication)

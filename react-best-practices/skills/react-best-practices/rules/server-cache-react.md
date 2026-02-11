---
title: React.cache() でリクエスト内重複を排除する
impact: MEDIUM
impactDescription: deduplicates within request
tags: server, cache, react-cache, deduplication
---

## React.cache() でリクエスト内重複を排除する

このルールの目的はパフォーマンスと保守性の向上です。以下に非推奨例と推奨例を示します。

サーバー側のリクエスト内重複排除には `React.cache()` を使います。特に認証処理や DB クエリで効果が高いです。

**使用例：**

```typescript
import { cache } from 'react'

export const getCurrentUser = cache(async () => {
  const session = await auth()
  if (!session?.user?.id) return null
  return await db.user.findUnique({
    where: { id: session.user.id }
  })
})
```

単一リクエスト内では `getCurrentUser()` を複数回呼んでもクエリ実行は 1 回だけです。

**引数にインラインオブジェクトを使わない:**

`React.cache()` は浅い等価比較（`Object.is`）でキャッシュヒットを判定します。インラインオブジェクトは毎回新しい参照になるためヒットしません。

**Incorrect（always cache miss):**

```typescript
const getUser = cache(async (params: { uid: number }) => {
  return await db.user.findUnique({ where: { id: params.uid } })
})

// Each call creates new object, never hits cache
getUser({ uid: 1 })
getUser({ uid: 1 })  // Cache miss, runs query again
```

**Correct（cache hit):**

```typescript
const getUser = cache(async (uid: number) => {
  return await db.user.findUnique({ where: { id: uid } })
})

// Primitive args use value equality
getUser(1)
getUser(1)  // Cache hit, returns cached result
```

オブジェクトを渡す必要がある場合は、同じ参照を渡してください:

```typescript
const params = { uid: 1 }
getUser(params)  // Query runs
getUser(params)  // Cache hit (same reference)
```

**Next.js 固有の注記：**

Next.js では `fetch` API にリクエストメモ化が組み込まれており、同じ URL とオプションのリクエストは単一リクエスト内で自動的に重複排除されます。そのため `fetch` に `React.cache()` は不要です。ただし、次のような他の非同期処理では `React.cache()` が依然重要です:

- データベースクエリ（Prisma, Drizzle など）
- 重い計算処理
- 認証チェック
- ファイルシステム操作
- fetch 以外の非同期処理全般

これらの処理をコンポーネントツリー全体で重複排除するために `React.cache()` を使います。

参考: [React.cache documentation](https://react.dev/reference/react/cache)

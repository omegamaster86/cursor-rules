---
title: リクエスト間は LRU キャッシュを使う
impact: HIGH
impactDescription: caches across requests
tags: server, cache, lru, cross-request
---

## リクエスト間は LRU キャッシュを使う

このルールの目的はパフォーマンスと保守性の向上です。以下に非推奨例と推奨例を示します。

`React.cache()` は 1 リクエスト内でのみ有効です。連続する複数リクエスト（例: ユーザーが A ボタンの後に B ボタンを押す）で共有したいデータには LRU キャッシュを使います。

**実装例:**

```typescript
import { LRUCache } from 'lru-cache'

const cache = new LRUCache<string, any>({
  max: 1000,
  ttl: 5 * 60 * 1000  // 5 minutes
})

export async function getUser(id: string) {
  const cached = cache.get(id)
  if (cached) return cached

  const user = await db.user.findUnique({ where: { id } })
  cache.set(id, user)
  return user
}

// Request 1: DB query, result cached
// Request 2: cache hit, no DB query
```

ユーザーの連続操作が短時間に同じデータを必要とする複数エンドポイントへ到達する場合に有効です。

**Vercel の [Fluid Compute](https://vercel.com/docs/fluid-compute) 利用時:** 複数の同時リクエストが同じ関数インスタンスとキャッシュを共有できるため、LRU キャッシュは特に効果的です。Redis などの外部ストレージを使わなくても、リクエストをまたいでキャッシュを維持できます。

**従来型 serverless の場合:** 各呼び出しは分離されるため、プロセス間キャッシュには Redis などを検討してください。

参考: [https://github.com/isaacs/node-lru-cache](https://github.com/isaacs/node-lru-cache)

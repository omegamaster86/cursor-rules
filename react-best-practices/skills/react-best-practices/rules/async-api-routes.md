---
title: API ルートのウォーターフォール連鎖を防ぐ
impact: CRITICAL
impactDescription: 2-10× improvement
tags: api-routes, server-actions, waterfalls, parallelization
---

## API ルートのウォーターフォール連鎖を防ぐ

このルールの目的はパフォーマンスと保守性の向上です。以下に非推奨例と推奨例を示します。

API ルートや Server Actions では、まだ await しない処理でも、独立しているものはすぐ開始してください。

**Incorrect（config waits for auth, data waits for both):**

```typescript
export async function GET(request: Request) {
  const session = await auth()
  const config = await fetchConfig()
  const data = await fetchData(session.user.id)
  return Response.json({ data, config })
}
```

**Correct（auth and config start immediately):**

```typescript
export async function GET(request: Request) {
  const sessionPromise = auth()
  const configPromise = fetchConfig()
  const session = await sessionPromise
  const [config, data] = await Promise.all([
    configPromise,
    fetchData(session.user.id)
  ])
  return Response.json({ data, config })
}
```

依存関係がより複雑な処理では、`better-all` を使うと並列性を自動で最大化できます（依存関係ベース並列化を参照）。

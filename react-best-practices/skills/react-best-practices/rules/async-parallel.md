---
title: 独立処理は Promise.all() で並列実行する
impact: CRITICAL
impactDescription: 2-10× improvement
tags: async, parallelization, promises, waterfalls
---

## 独立処理は Promise.all() で並列実行する

このルールの目的はパフォーマンスと保守性の向上です。以下に非推奨例と推奨例を示します。

非同期処理に依存関係がない場合は、`Promise.all()` で同時実行します。

**Incorrect（sequential execution, 3 round trips):**

```typescript
const user = await fetchUser()
const posts = await fetchPosts()
const comments = await fetchComments()
```

**Correct（parallel execution, 1 round trip):**

```typescript
const [user, posts, comments] = await Promise.all([
  fetchUser(),
  fetchPosts(),
  fetchComments()
])
```

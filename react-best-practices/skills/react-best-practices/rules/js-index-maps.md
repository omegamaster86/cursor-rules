---
title: 繰り返し検索にはインデックス Map を作る
impact: LOW-MEDIUM
impactDescription: 1M ops to 2K ops
tags: javascript, map, indexing, optimization, performance
---

## 繰り返し検索にはインデックス Map を作る

このルールの目的はパフォーマンスと保守性の向上です。以下に非推奨例と推奨例を示します。

同じキーで `.find()` を繰り返す場合は Map を使います。

**Incorrect（O(n) per lookup):**

```typescript
function processOrders(orders: Order[], users: User[]) {
  return orders.map(order => ({
    ...order,
    user: users.find(u => u.id === order.userId)
  }))
}
```

**Correct（O(1) per lookup):**

```typescript
function processOrders(orders: Order[], users: User[]) {
  const userById = new Map(users.map(u => [u.id, u]))

  return orders.map(order => ({
    ...order,
    user: userById.get(order.userId)
  }))
}
```

Map を 1 回だけ構築（O(n)）すれば、その後の検索はすべて O(1) です。
1000 件の注文 × 1000 人のユーザーでは、100 万操作が約 2000 操作まで減ります。

---
title: Min/Max 探索に Sort ではなくループを使う
impact: LOW
impactDescription: O(n) instead of O(n log n)
tags: javascript, arrays, performance, sorting, algorithms
---

## Min/Max 探索に Sort ではなくループを使う

このルールの目的はパフォーマンスと保守性の向上です。以下に非推奨例と推奨例を示します。

最小値・最大値の探索は配列を 1 回走査すれば十分です。ソートは無駄で遅くなります。

**Incorrect（O(n log n) - sort to find latest):**

```typescript
interface Project {
  id: string
  name: string
  updatedAt: number
}

function getLatestProject(projects: Project[]) {
  const sorted = [...projects].sort((a, b) => b.updatedAt - a.updatedAt)
  return sorted[0]
}
```

最大値を求めるためだけに配列全体をソートしています。

**Incorrect（O(n log n) - sort for oldest and newest):**

```typescript
function getOldestAndNewest(projects: Project[]) {
  const sorted = [...projects].sort((a, b) => a.updatedAt - b.updatedAt)
  return { oldest: sorted[0], newest: sorted[sorted.length - 1] }
}
```

min/max だけが必要なのに不要なソートを行っています。

**Correct（O(n) - single loop):**

```typescript
function getLatestProject(projects: Project[]) {
  if (projects.length === 0) return null
  
  let latest = projects[0]
  
  for (let i = 1; i < projects.length; i++) {
    if (projects[i].updatedAt > latest.updatedAt) {
      latest = projects[i]
    }
  }
  
  return latest
}

function getOldestAndNewest(projects: Project[]) {
  if (projects.length === 0) return { oldest: null, newest: null }
  
  let oldest = projects[0]
  let newest = projects[0]
  
  for (let i = 1; i < projects.length; i++) {
    if (projects[i].updatedAt < oldest.updatedAt) oldest = projects[i]
    if (projects[i].updatedAt > newest.updatedAt) newest = projects[i]
  }
  
  return { oldest, newest }
}
```

配列を 1 回走査するだけで、コピーもソートも不要です。

**代替案（Math.min/Math.max for small arrays):**

```typescript
const numbers = [5, 2, 8, 1, 9]
const min = Math.min(...numbers)
const max = Math.max(...numbers)
```

この方法は小さな配列には有効ですが、スプレッド演算子の制限により、非常に大きい配列では遅くなったりエラーになったりします。最大配列長は Chrome 143 で約 124000、Safari 18 で約 638000 程度です（環境により変動。詳細は [the fiddle](https://jsfiddle.net/qw1jabsx/4/) 参照）。信頼性を重視するならループ方式を使ってください。

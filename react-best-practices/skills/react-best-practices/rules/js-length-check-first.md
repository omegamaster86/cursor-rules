---
title: 配列比較は先に Length を確認する
impact: MEDIUM-HIGH
impactDescription: avoids expensive operations when lengths differ
tags: javascript, arrays, performance, optimization, comparison
---

## 配列比較は先に Length を確認する

このルールの目的はパフォーマンスと保守性の向上です。以下に非推奨例と推奨例を示します。

配列を高コスト処理（ソート・深い比較・シリアライズ）で比較する場合は、先に length を確認します。length が異なれば等価ではありません。

実運用では、比較処理がホットパス（event handler / render ループ）で実行される場合に特に有効です。

**Incorrect（always runs expensive comparison):**

```typescript
function hasChanges(current: string[], original: string[]) {
  // Always sorts and joins, even when lengths differ
  return current.sort().join() !== original.sort().join()
}
```

`current.length` が 5、`original.length` が 100 のように明らかに違う場合でも、O(n log n) のソートが 2 回走ってしまいます。さらに join と文字列比較のオーバーヘッドも発生します。

**Correct（O(1) length check first):**

```typescript
function hasChanges(current: string[], original: string[]) {
  // Early return if lengths differ
  if (current.length !== original.length) {
    return true
  }
  // Only sort when lengths match
  const currentSorted = current.toSorted()
  const originalSorted = original.toSorted()
  for (let i = 0; i < currentSorted.length; i++) {
    if (currentSorted[i] !== originalSorted[i]) {
      return true
    }
  }
  return false
}
```

この方法が効率的な理由:
- 長さが異なる時点で、ソートや join のオーバーヘッドを回避できる
- join した文字列のメモリ消費を避けられる（大きな配列で特に重要）
- 元の配列を破壊しない
- 差分を見つけた時点で早期 return できる

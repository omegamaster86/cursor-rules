---
title: 静的 JSX をホイストする
impact: LOW
impactDescription: avoids re-creation
tags: rendering, jsx, static, optimization
---

## 静的 JSX をホイストする

このルールの目的はパフォーマンスと保守性の向上です。以下に非推奨例と推奨例を示します。

静的 JSX はコンポーネント外へ切り出し、再生成を避けます。

**Incorrect（recreates element every render):**

```tsx
function LoadingSkeleton() {
  return <div className="animate-pulse h-20 bg-gray-200" />
}

function Container() {
  return (
    <div>
      {loading && <LoadingSkeleton />}
    </div>
  )
}
```

**Correct（reuses same element):**

```tsx
const loadingSkeleton = (
  <div className="animate-pulse h-20 bg-gray-200" />
)

function Container() {
  return (
    <div>
      {loading && loadingSkeleton}
    </div>
  )
}
```

これは大きく静的な SVG ノードで特に有効です。毎レンダー再生成すると高コストになります。

**注記:** プロジェクトで [React Compiler](https://react.dev/learn/react-compiler) を有効化している場合、静的 JSX 要素の hoist と再レンダー最適化は自動で行われるため、手動 hoist は不要です。

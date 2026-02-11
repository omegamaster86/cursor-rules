---
title: 条件レンダリングは明示的に書く
impact: LOW
impactDescription: prevents rendering 0 or NaN
tags: rendering, conditional, jsx, falsy-values
---

## 条件レンダリングは明示的に書く

このルールの目的はパフォーマンスと保守性の向上です。以下に非推奨例と推奨例を示します。

条件が `0` / `NaN` など描画されうる falsy 値を取り得る場合、条件レンダリングは `&&` ではなく明示的な三項演算子（`? :`）を使います。

**Incorrect（renders "0" when count is 0):**

```tsx
function Badge({ count }: { count: number }) {
  return (
    <div>
      {count && <span className="badge">{count}</span>}
    </div>
  )
}

// When count = 0, renders: <div>0</div>
// When count = 5, renders: <div><span class="badge">5</span></div>
```

**Correct（renders nothing when count is 0):**

```tsx
function Badge({ count }: { count: number }) {
  return (
    <div>
      {count > 0 ? <span className="badge">{count}</span> : null}
    </div>
  )
}

// When count = 0, renders: <div></div>
// When count = 5, renders: <div><span class="badge">5</span></div>
```

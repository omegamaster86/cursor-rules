---
title: Effect 依存を狭める
impact: LOW
impactDescription: minimizes effect re-runs
tags: rerender, useEffect, dependencies, optimization
---

## Effect 依存を狭める

このルールの目的はパフォーマンスと保守性の向上です。以下に非推奨例と推奨例を示します。

Effect の再実行を減らすため、オブジェクトではなくプリミティブを依存に指定します。

**Incorrect（re-runs on any user field change):**

```tsx
useEffect(() => {
  console.log(user.id)
}, [user])
```

**Correct（re-runs only when id changes):**

```tsx
useEffect(() => {
  console.log(user.id)
}, [user.id])
```

**導出 state は Effect 外で計算:**

```tsx
// Incorrect: runs on width=767, 766, 765...
useEffect(() => {
  if (width < 768) {
    enableMobileMode()
  }
}, [width])

// Correct: runs only on boolean transition
const isMobile = width < 768
useEffect(() => {
  if (isMobile) {
    enableMobileMode()
  }
}, [isMobile])
```

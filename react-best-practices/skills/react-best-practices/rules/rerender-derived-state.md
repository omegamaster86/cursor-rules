---
title: 導出 State を購読する
impact: MEDIUM
impactDescription: reduces re-render frequency
tags: rerender, derived-state, media-query, optimization
---

## 導出 State を購読する

このルールの目的はパフォーマンスと保守性の向上です。以下に非推奨例と推奨例を示します。

連続値ではなく導出した boolean state を購読して、再レンダー頻度を下げます。

**Incorrect（re-renders on every pixel change):**

```tsx
function Sidebar() {
  const width = useWindowWidth()  // updates continuously
  const isMobile = width < 768
  return <nav className={isMobile ? 'mobile' : 'desktop'} />
}
```

**Correct（re-renders only when boolean changes):**

```tsx
function Sidebar() {
  const isMobile = useMediaQuery('(max-width: 767px)')
  return <nav className={isMobile ? 'mobile' : 'desktop'} />
}
```

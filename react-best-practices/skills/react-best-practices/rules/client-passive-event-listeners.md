---
title: スクロール性能のため Passive Event Listener を使う
impact: MEDIUM
impactDescription: eliminates scroll delay caused by event listeners
tags: client, event-listeners, scrolling, performance, touch, wheel
---

## スクロール性能のため Passive Event Listener を使う

このルールの目的はパフォーマンスと保守性の向上です。以下に非推奨例と推奨例を示します。

touch / wheel イベントリスナーに `{ passive: true }` を付けるとスクロールを即時化できます。通常ブラウザは `preventDefault()` の有無確認のためリスナー完了まで待機するため、遅延が発生します。

**Incorrect：**

```typescript
useEffect(() => {
  const handleTouch = (e: TouchEvent) => console.log(e.touches[0].clientX)
  const handleWheel = (e: WheelEvent) => console.log(e.deltaY)
  
  document.addEventListener('touchstart', handleTouch)
  document.addEventListener('wheel', handleWheel)
  
  return () => {
    document.removeEventListener('touchstart', handleTouch)
    document.removeEventListener('wheel', handleWheel)
  }
}, [])
```

**Correct：**

```typescript
useEffect(() => {
  const handleTouch = (e: TouchEvent) => console.log(e.touches[0].clientX)
  const handleWheel = (e: WheelEvent) => console.log(e.deltaY)
  
  document.addEventListener('touchstart', handleTouch, { passive: true })
  document.addEventListener('wheel', handleWheel, { passive: true })
  
  return () => {
    document.removeEventListener('touchstart', handleTouch)
    document.removeEventListener('wheel', handleWheel)
  }
}, [])
```

**passive を使う場面:** トラッキング/分析、ログ、`preventDefault()` を呼ばないリスナー。

**passive を使わない場面:** カスタムスワイプ、カスタムズーム制御、`preventDefault()` が必要なリスナー。

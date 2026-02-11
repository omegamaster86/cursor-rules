---
title: イベントハンドラを Ref に保持する
impact: LOW
impactDescription: 購読を安定化
tags: advanced, hooks, refs, event-handlers, optimization
---

## イベントハンドラを Ref に保持する

このルールの目的はパフォーマンスと保守性の向上です。以下に非推奨例と推奨例を示します。

コールバック変更のたびに再購読させたくない Effect では、コールバックを `ref` に保持します。

**Incorrect（毎レンダーで再購読される）:**

```tsx
function useWindowEvent(event: string, handler: (e) => void) {
  useEffect(() => {
    window.addEventListener(event, handler)
    return () => window.removeEventListener(event, handler)
  }, [event, handler])
}
```

**Correct（購読が安定する）:**

```tsx
function useWindowEvent(event: string, handler: (e) => void) {
  const handlerRef = useRef(handler)
  useEffect(() => {
    handlerRef.current = handler
  }, [handler])

  useEffect(() => {
    const listener = (e) => handlerRef.current(e)
    window.addEventListener(event, listener)
    return () => window.removeEventListener(event, listener)
  }, [event])
}
```

**代替案（最新 React を使っている場合は `useEffectEvent` を使う）:**

```tsx
import { useEffectEvent } from 'react'

function useWindowEvent(event: string, handler: (e) => void) {
  const onEvent = useEffectEvent(handler)

  useEffect(() => {
    window.addEventListener(event, onEvent)
    return () => window.removeEventListener(event, onEvent)
  }, [event])
}
```

`useEffectEvent` は同じパターンをより簡潔に書ける API です。常に最新のハンドラを呼び出す、安定した関数参照を作成できます。

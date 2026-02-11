---
title: レイアウトスラッシングを避ける
impact: MEDIUM
impactDescription: prevents forced synchronous layouts and reduces performance bottlenecks
tags: javascript, dom, css, performance, reflow, layout-thrashing
---

## レイアウトスラッシングを避ける

このルールの目的はパフォーマンスと保守性の向上です。以下に非推奨例と推奨例を示します。

style 書き込みと layout 読み取りを交互に行わないでください。style 変更の間に `offsetWidth` / `getBoundingClientRect()` / `getComputedStyle()` などを読むと、ブラウザに同期 reflow が強制されます。

**これは問題ありません（ブラウザが style 変更をバッチ化する）:**
```typescript
function updateElementStyles(element: HTMLElement) {
  // Each line invalidates style, but browser batches the recalculation
  element.style.width = '100px'
  element.style.height = '200px'
  element.style.backgroundColor = 'blue'
  element.style.border = '1px solid black'
}
```

**Incorrect（interleaved reads and writes force reflows):**
```typescript
function layoutThrashing(element: HTMLElement) {
  element.style.width = '100px'
  const width = element.offsetWidth  // Forces reflow
  element.style.height = '200px'
  const height = element.offsetHeight  // Forces another reflow
}
```

**Correct（batch writes, then read once):**
```typescript
function updateElementStyles(element: HTMLElement) {
  // Batch all writes together
  element.style.width = '100px'
  element.style.height = '200px'
  element.style.backgroundColor = 'blue'
  element.style.border = '1px solid black'
  
  // Read after all writes are done (single reflow)
  const { width, height } = element.getBoundingClientRect()
}
```

**Correct（batch reads, then writes):**
```typescript
function avoidThrashing(element: HTMLElement) {
  // Read phase - all layout queries first
  const rect1 = element.getBoundingClientRect()
  const offsetWidth = element.offsetWidth
  const offsetHeight = element.offsetHeight
  
  // Write phase - all style changes after
  element.style.width = '100px'
  element.style.height = '200px'
}
```

**より良い方法: CSS クラスを使う**
```css
.highlighted-box {
  width: 100px;
  height: 200px;
  background-color: blue;
  border: 1px solid black;
}
```
```typescript
function updateElementStyles(element: HTMLElement) {
  element.classList.add('highlighted-box')
  
  const { width, height } = element.getBoundingClientRect()
}
```

**React の例:**
```tsx
// Incorrect: interleaving style changes with layout queries
function Box({ isHighlighted }: { isHighlighted: boolean }) {
  const ref = useRef<HTMLDivElement>(null)
  
  useEffect(() => {
    if (ref.current && isHighlighted) {
      ref.current.style.width = '100px'
      const width = ref.current.offsetWidth // Forces layout
      ref.current.style.height = '200px'
    }
  }, [isHighlighted])
  
  return <div ref={ref}>Content</div>
}

// Correct: toggle class
function Box({ isHighlighted }: { isHighlighted: boolean }) {
  return (
    <div className={isHighlighted ? 'highlighted-box' : ''}>
      Content
    </div>
  )
}
```

可能な限り inline style より CSS クラスを優先してください。CSS ファイルはブラウザにキャッシュされ、関心の分離と保守性の面でも有利です。

レイアウト強制を引き起こす操作の詳細は、[this gist](https://gist.github.com/paulirish/5d52fb081b3570c81e3a) と [CSS Triggers](https://csstriggers.com/) を参照してください。

---
title: SVG 要素ではなくラッパーをアニメーションする
impact: LOW
impactDescription: enables hardware acceleration
tags: rendering, svg, css, animation, performance
---

## SVG 要素ではなくラッパーをアニメーションする

このルールの目的はパフォーマンスと保守性の向上です。以下に非推奨例と推奨例を示します。

多くのブラウザでは SVG 要素上の CSS3 アニメーションがハードウェア加速されません。SVG を `<div>` で包み、ラッパー側をアニメーションさせます。

**Incorrect（animating SVG directly - no hardware acceleration):**

```tsx
function LoadingSpinner() {
  return (
    <svg 
      className="animate-spin"
      width="24" 
      height="24" 
      viewBox="0 0 24 24"
    >
      <circle cx="12" cy="12" r="10" stroke="currentColor" />
    </svg>
  )
}
```

**Correct（animating wrapper div - hardware accelerated):**

```tsx
function LoadingSpinner() {
  return (
    <div className="animate-spin">
      <svg 
        width="24" 
        height="24" 
        viewBox="0 0 24 24"
      >
        <circle cx="12" cy="12" r="10" stroke="currentColor" />
      </svg>
    </div>
  )
}
```

これは `transform` / `opacity` / `translate` / `scale` / `rotate` などの CSS 変形・遷移全般に当てはまります。ラッパー div を使うことで GPU 加速が効き、より滑らかなアニメーションになります。

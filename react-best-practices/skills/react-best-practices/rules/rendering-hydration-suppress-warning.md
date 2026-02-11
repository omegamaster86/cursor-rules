---
title: 想定内の Hydration 不一致警告を抑制する
impact: LOW-MEDIUM
impactDescription: avoids noisy hydration warnings for known differences
tags: rendering, hydration, ssr, nextjs
---

## 想定内の Hydration 不一致警告を抑制する

このルールの目的はパフォーマンスと保守性の向上です。以下に非推奨例と推奨例を示します。

SSR フレームワーク（例: Next.js）では、サーバーとクライアントで意図的に値が異なる場合があります（ランダム ID、日付、ロケール/タイムゾーン整形など）。このような**想定内**の不一致には、動的テキストを `suppressHydrationWarning` 付き要素で包み、不要な警告を抑制します。実バグの隠蔽には使わず、過剰利用もしないでください。

**Incorrect（known mismatch warnings):**

```tsx
function Timestamp() {
  return <span>{new Date().toLocaleString()}</span>
}
```

**Correct（suppress expected mismatch only):**

```tsx
function Timestamp() {
  return (
    <span suppressHydrationWarning>
      {new Date().toLocaleString()}
    </span>
  )
}
```

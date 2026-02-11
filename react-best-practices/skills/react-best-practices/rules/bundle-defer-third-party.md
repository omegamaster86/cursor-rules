---
title: 非クリティカルなサードパーティライブラリを遅延する
impact: MEDIUM
impactDescription: loads after hydration
tags: bundle, third-party, analytics, defer
---

## 非クリティカルなサードパーティライブラリを遅延する

このルールの目的はパフォーマンスと保守性の向上です。以下に非推奨例と推奨例を示します。

分析・ログ・エラートラッキングはユーザー操作をブロックしないため、hydration 後に読み込みます。

**Incorrect（blocks initial bundle):**

```tsx
import { Analytics } from '@vercel/analytics/react'

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        {children}
        <Analytics />
      </body>
    </html>
  )
}
```

**Correct（loads after hydration):**

```tsx
import dynamic from 'next/dynamic'

const Analytics = dynamic(
  () => import('@vercel/analytics/react').then(m => m.Analytics),
  { ssr: false }
)

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        {children}
        <Analytics />
      </body>
    </html>
  )
}
```

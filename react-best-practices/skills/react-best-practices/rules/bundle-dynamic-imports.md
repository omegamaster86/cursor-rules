---
title: 重いコンポーネントは Dynamic Import する
impact: CRITICAL
impactDescription: directly affects TTI and LCP
tags: bundle, dynamic-import, code-splitting, next-dynamic
---

## 重いコンポーネントは Dynamic Import する

このルールの目的はパフォーマンスと保守性の向上です。以下に非推奨例と推奨例を示します。

初期描画で不要な大きいコンポーネントは `next/dynamic` で遅延読み込みします。

**Incorrect（Monaco bundles with main chunk ~300KB):**

```tsx
import { MonacoEditor } from './monaco-editor'

function CodePanel({ code }: { code: string }) {
  return <MonacoEditor value={code} />
}
```

**Correct（Monaco loads on demand):**

```tsx
import dynamic from 'next/dynamic'

const MonacoEditor = dynamic(
  () => import('./monaco-editor').then(m => m.MonacoEditor),
  { ssr: false }
)

function CodePanel({ code }: { code: string }) {
  return <MonacoEditor value={code} />
}
```

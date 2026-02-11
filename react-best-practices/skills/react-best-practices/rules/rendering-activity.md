---
title: 表示切替には Activity コンポーネントを使う
impact: MEDIUM
impactDescription: preserves state/DOM
tags: rendering, activity, visibility, state-preservation
---

## 表示切替には Activity コンポーネントを使う

このルールの目的はパフォーマンスと保守性の向上です。以下に非推奨例と推奨例を示します。

表示/非表示を頻繁に切り替える高コストコンポーネントでは、React の `<Activity>` を使って state/DOM を保持します。

**使用例：**

```tsx
import { Activity } from 'react'

function Dropdown({ isOpen }: Props) {
  return (
    <Activity mode={isOpen ? 'visible' : 'hidden'}>
      <ExpensiveMenu />
    </Activity>
  )
}
```

高コストな再レンダーと state の消失を防げます。

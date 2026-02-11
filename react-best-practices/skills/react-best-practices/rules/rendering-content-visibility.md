---
title: 長いリストに CSS content-visibility を使う
impact: HIGH
impactDescription: faster initial render
tags: rendering, css, content-visibility, long-lists
---

## 長いリストに CSS content-visibility を使う

このルールの目的はパフォーマンスと保守性の向上です。以下に非推奨例と推奨例を示します。

`content-visibility: auto` を適用して、画面外要素の描画を遅延します。

**CSS 例:**

```css
.message-item {
  content-visibility: auto;
  contain-intrinsic-size: 0 80px;
}
```

**例:**

```tsx
function MessageList({ messages }: { messages: Message[] }) {
  return (
    <div className="overflow-y-auto h-screen">
      {messages.map(msg => (
        <div key={msg.id} className="message-item">
          <Avatar user={msg.author} />
          <div>{msg.content}</div>
        </div>
      ))}
    </div>
  )
}
```

1000 件のメッセージでは、約 990 件の画面外要素の layout/paint をスキップでき、初期描画が約 10 倍高速化します。

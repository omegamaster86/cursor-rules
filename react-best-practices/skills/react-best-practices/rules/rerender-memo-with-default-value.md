---

title: Memo コンポーネントの非プリミティブ既定値を定数に切り出す
impact: MEDIUM
impactDescription: restores memoization by using a constant for default value
tags: rerender, memo, optimization

---

## Memo コンポーネントの非プリミティブ既定値を定数に切り出す

このルールの目的はパフォーマンスと保守性の向上です。以下に非推奨例と推奨例を示します。

memo 化コンポーネントで、配列・関数・オブジェクトなど非プリミティブな任意引数にデフォルト値を直接書くと、その引数を省略した呼び出しで memo 化が破綻します。毎レンダー新しいインスタンスが作られ、`memo()` の厳密等価比較を通らないためです。

この問題を避けるには、デフォルト値を定数へ切り出します。

**Incorrect（`onClick` has different values on every rerender):**

```tsx
const UserAvatar = memo(function UserAvatar({ onClick = () => {} }: { onClick?: () => void }) {
  // ...
})

// Used without optional onClick
<UserAvatar />
```

**Correct（stable default value):**

```tsx
const NOOP = () => {};

const UserAvatar = memo(function UserAvatar({ onClick = NOOP }: { onClick?: () => void }) {
  // ...
})

// Used without optional onClick
<UserAvatar />
```

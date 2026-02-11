---
title: 不変性のため sort() ではなく toSorted() を使う
impact: MEDIUM-HIGH
impactDescription: prevents mutation bugs in React state
tags: javascript, arrays, immutability, react, state, mutation
---

## 不変性のため sort() ではなく toSorted() を使う

このルールの目的はパフォーマンスと保守性の向上です。以下に非推奨例と推奨例を示します。

`.sort()` は配列を破壊的に変更するため、React の state/props で不具合の原因になります。非破壊で新しい配列を返す `.toSorted()` を使ってください。

**Incorrect（mutates original array):**

```typescript
function UserList({ users }: { users: User[] }) {
  // Mutates the users prop array!
  const sorted = useMemo(
    () => users.sort((a, b) => a.name.localeCompare(b.name)),
    [users]
  )
  return <div>{sorted.map(renderUser)}</div>
}
```

**Correct（creates new array):**

```typescript
function UserList({ users }: { users: User[] }) {
  // Creates new sorted array, original unchanged
  const sorted = useMemo(
    () => users.toSorted((a, b) => a.name.localeCompare(b.name)),
    [users]
  )
  return <div>{sorted.map(renderUser)}</div>
}
```

**React で重要な理由:**

1. Props/state の破壊的変更は React の不変性モデルを壊す - React は props と state を読み取り専用として扱う前提
2. stale closure バグを誘発する - クロージャ（callback/effect）内で配列を破壊的変更すると予期しない挙動につながる

**ブラウザサポート（古い環境向け代替）:**

`.toSorted()` は主要モダン環境（Chrome 110+ / Safari 16+ / Firefox 115+ / Node.js 20+）で利用できます。古い環境ではスプレッド演算子を使ってください:

```typescript
// Fallback for older browsers
const sorted = [...items].sort((a, b) => a.value - b.value)
```

**その他の非破壊配列メソッド:**

- `.toSorted()` - 非破壊ソート
- `.toReversed()` - 非破壊 reverse
- `.toSpliced()` - 非破壊 splice
- `.with()` - 非破壊要素置換

---
title: RegExp 生成をホイストする
impact: LOW-MEDIUM
impactDescription: avoids recreation
tags: javascript, regexp, optimization, memoization
---

## RegExp 生成をホイストする

このルールの目的はパフォーマンスと保守性の向上です。以下に非推奨例と推奨例を示します。

RegExp を render 内で毎回生成しないでください。モジュールスコープへ hoist するか `useMemo()` でメモ化します。

**Incorrect（new RegExp every render):**

```tsx
function Highlighter({ text, query }: Props) {
  const regex = new RegExp(`(${query})`, 'gi')
  const parts = text.split(regex)
  return <>{parts.map((part, i) => ...)}</>
}
```

**Correct（memoize or hoist):**

```tsx
const EMAIL_REGEX = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

function Highlighter({ text, query }: Props) {
  const regex = useMemo(
    () => new RegExp(`(${escapeRegex(query)})`, 'gi'),
    [query]
  )
  const parts = text.split(regex)
  return <>{parts.map((part, i) => ...)}</>
}
```

**注意（グローバル regex は可変 state を持つ）:**

グローバル regex（`/g`）は `lastIndex` という可変 state を持ちます:

```typescript
const regex = /foo/g
regex.test('foo')  // true, lastIndex = 3
regex.test('foo')  // false, lastIndex = 0
```

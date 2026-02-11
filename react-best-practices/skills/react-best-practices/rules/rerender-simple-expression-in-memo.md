---
title: 単純なプリミティブ式を useMemo で包まない
impact: LOW-MEDIUM
impactDescription: wasted computation on every render
tags: rerender, useMemo, optimization
---

## 単純なプリミティブ式を useMemo で包まない

このルールの目的はパフォーマンスと保守性の向上です。以下に非推奨例と推奨例を示します。

式が単純（論理/算術演算子が少ない）で結果がプリミティブ（boolean/number/string）の場合、`useMemo` で包まないでください。
`useMemo` 呼び出しと依存比較のコストが、式そのものより高くなる場合があります。

**Incorrect：**

```tsx
function Header({ user, notifications }: Props) {
  const isLoading = useMemo(() => {
    return user.isLoading || notifications.isLoading
  }, [user.isLoading, notifications.isLoading])

  if (isLoading) return <Skeleton />
  // return some markup
}
```

**Correct：**

```tsx
function Header({ user, notifications }: Props) {
  const isLoading = user.isLoading || notifications.isLoading

  if (isLoading) return <Skeleton />
  // return some markup
}
```

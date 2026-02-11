---
title: Memo 化コンポーネントへ分離する
impact: MEDIUM
impactDescription: enables early returns
tags: rerender, memo, useMemo, optimization
---

## Memo 化コンポーネントへ分離する

このルールの目的はパフォーマンスと保守性の向上です。以下に非推奨例と推奨例を示します。

高コスト処理を memo 化コンポーネントへ分離し、計算前の早期 return を可能にします。

**Incorrect（computes avatar even when loading):**

```tsx
function Profile({ user, loading }: Props) {
  const avatar = useMemo(() => {
    const id = computeAvatarId(user)
    return <Avatar id={id} />
  }, [user])

  if (loading) return <Skeleton />
  return <div>{avatar}</div>
}
```

**Correct（skips computation when loading):**

```tsx
const UserAvatar = memo(function UserAvatar({ user }: { user: User }) {
  const id = useMemo(() => computeAvatarId(user), [user])
  return <Avatar id={id} />
})

function Profile({ user, loading }: Props) {
  if (loading) return <Skeleton />
  return (
    <div>
      <UserAvatar user={user} />
    </div>
  )
}
```

**注記:** プロジェクトで [React Compiler](https://react.dev/learn/react-compiler) を有効化している場合、`memo()` や `useMemo()` による手動メモ化は不要です。再レンダー最適化はコンパイラが自動で行います。

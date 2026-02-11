---
title: RSC 境界のシリアライズを最小化する
impact: HIGH
impactDescription: reduces data transfer size
tags: server, rsc, serialization, props
---

## RSC 境界のシリアライズを最小化する

このルールの目的はパフォーマンスと保守性の向上です。以下に非推奨例と推奨例を示します。

React の Server/Client 境界では、オブジェクトの全プロパティが文字列としてシリアライズされ、HTML レスポンスや後続 RSC リクエストに埋め込まれます。このデータ量はページ重量と読み込み時間へ直結するため、**サイズは非常に重要**です。client が実際に使うフィールドだけを渡してください。

**Incorrect（serializes all 50 fields):**

```tsx
async function Page() {
  const user = await fetchUser()  // 50 fields
  return <Profile user={user} />
}

'use client'
function Profile({ user }: { user: User }) {
  return <div>{user.name}</div>  // uses 1 field
}
```

**Correct（serializes only 1 field):**

```tsx
async function Page() {
  const user = await fetchUser()
  return <Profile name={user.name} />
}

'use client'
function Profile({ name }: { name: string }) {
  return <div>{name}</div>
}
```

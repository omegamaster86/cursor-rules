---
title: RSC Props の重複シリアライズを避ける
impact: LOW
impactDescription: reduces network payload by avoiding duplicate serialization
tags: server, rsc, serialization, props, client-components
---

## RSC Props の重複シリアライズを避ける

このルールの目的はパフォーマンスと保守性の向上です。以下に非推奨例と推奨例を示します。

**影響: LOW（重複シリアライズ回避によりネットワーク転送量を削減）**

RSC→client のシリアライズは値ではなくオブジェクト参照で重複排除されます。同じ参照は 1 回だけ、新しい参照は再シリアライズされます。変換（`.toSorted()` / `.filter()` / `.map()`）は server ではなく client 側で行ってください。

**Incorrect（duplicates array):**

```tsx
// RSC: sends 6 strings (2 arrays × 3 items)
<ClientList usernames={usernames} usernamesOrdered={usernames.toSorted()} />
```

**Correct（sends 3 strings):**

```tsx
// RSC: send once
<ClientList usernames={usernames} />

// Client: transform there
'use client'
const sorted = useMemo(() => [...usernames].sort(), [usernames])
```

**ネスト時の重複排除挙動:**

重複排除は再帰的に働きます。効果はデータ型で変わります:

- `string[]` / `number[]` / `boolean[]`: **影響 HIGH** - 配列とすべてのプリミティブが完全重複
- `object[]`: **影響 LOW** - 配列は重複するが、ネストオブジェクトは参照で重複排除される

```tsx
// string[] - duplicates everything
usernames={['a','b']} sorted={usernames.toSorted()} // sends 4 strings

// object[] - duplicates array structure only
users={[{id:1},{id:2}]} sorted={users.toSorted()} // sends 2 arrays + 2 unique objects (not 4)
```

**重複排除を壊す操作（新しい参照を作る）:**

- 配列: `.toSorted()` / `.filter()` / `.map()` / `.slice()` / `[...arr]`
- オブジェクト: `{...obj}` / `Object.assign()` / `structuredClone()` / `JSON.parse(JSON.stringify())`

**追加例:**

```tsx
// ❌ Bad
<C users={users} active={users.filter(u => u.active)} />
<C product={product} productName={product.name} />

// ✅ Good
<C users={users} />
<C product={product} />
// Do filtering/destructuring in client
```

**例外:** 変換が高コストな場合や client 側で元データが不要な場合は、導出データを渡して構いません。

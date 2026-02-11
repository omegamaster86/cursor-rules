---
title: 依存関係ベースで並列化する
impact: CRITICAL
impactDescription: 2-10× improvement
tags: async, parallelization, dependencies, better-all
---

## 依存関係ベースで並列化する

このルールの目的はパフォーマンスと保守性の向上です。以下に非推奨例と推奨例を示します。

部分的な依存関係がある処理では、`better-all` を使って並列性を最大化します。各タスクを可能な最速タイミングで自動開始します。

**Incorrect（profile waits for config unnecessarily):**

```typescript
const [user, config] = await Promise.all([
  fetchUser(),
  fetchConfig()
])
const profile = await fetchProfile(user.id)
```

**Correct（config and profile run in parallel):**

```typescript
import { all } from 'better-all'

const { user, config, profile } = await all({
  async user() { return fetchUser() },
  async config() { return fetchConfig() },
  async profile() {
    return fetchProfile((await this.$.user).id)
  }
})
```

**追加依存なしの代替案:**

先にすべての Promise を作成し、最後に `Promise.all()` でまとめて待つ方法もあります。

```typescript
const userPromise = fetchUser()
const profilePromise = userPromise.then(user => fetchProfile(user.id))

const [user, config, profile] = await Promise.all([
  userPromise,
  fetchConfig(),
  profilePromise
])
```

参考: [https://github.com/shuding/better-all](https://github.com/shuding/better-all)

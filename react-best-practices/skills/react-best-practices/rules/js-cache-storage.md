---
title: Storage API の読み取りをキャッシュする
impact: LOW-MEDIUM
impactDescription: reduces expensive I/O
tags: javascript, localStorage, storage, caching, performance
---

## Storage API の読み取りをキャッシュする

このルールの目的はパフォーマンスと保守性の向上です。以下に非推奨例と推奨例を示します。

`localStorage` / `sessionStorage` / `document.cookie` は同期かつ高コストです。読み取り結果をメモリキャッシュします。

**Incorrect（reads storage on every call):**

```typescript
function getTheme() {
  return localStorage.getItem('theme') ?? 'light'
}
// Called 10 times = 10 storage reads
```

**Correct（Map cache):**

```typescript
const storageCache = new Map<string, string | null>()

function getLocalStorage(key: string) {
  if (!storageCache.has(key)) {
    storageCache.set(key, localStorage.getItem(key))
  }
  return storageCache.get(key)
}

function setLocalStorage(key: string, value: string) {
  localStorage.setItem(key, value)
  storageCache.set(key, value)  // keep cache in sync
}
```

Map（hook ではなく）を使うことで、React コンポーネントだけでなく utility や event handler でも使えます。

**Cookie キャッシュ:**

```typescript
let cookieCache: Record<string, string> | null = null

function getCookie(name: string) {
  if (!cookieCache) {
    cookieCache = Object.fromEntries(
      document.cookie.split('; ').map(c => c.split('='))
    )
  }
  return cookieCache[name]
}
```

**重要（外部変更時に無効化）:**

ストレージが外部で変更される可能性がある場合（別タブ、サーバー設定 Cookie など）はキャッシュを無効化します:

```typescript
window.addEventListener('storage', (e) => {
  if (e.key) storageCache.delete(e.key)
})

document.addEventListener('visibilitychange', () => {
  if (document.visibilityState === 'visible') {
    storageCache.clear()
  }
})
```

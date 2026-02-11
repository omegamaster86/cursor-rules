---
title: localStorage のデータをバージョン管理し最小化する
impact: MEDIUM
impactDescription: prevents schema conflicts, reduces storage size
tags: client, localStorage, storage, versioning, data-minimization
---

## localStorage のデータをバージョン管理し最小化する

このルールの目的はパフォーマンスと保守性の向上です。以下に非推奨例と推奨例を示します。

キーにバージョンプレフィックスを付け、必要なフィールドだけ保存します。スキーマ衝突や機微データの誤保存を防げます。

**Incorrect：**

```typescript
// No version, stores everything, no error handling
localStorage.setItem('userConfig', JSON.stringify(fullUserObject))
const data = localStorage.getItem('userConfig')
```

**Correct：**

```typescript
const VERSION = 'v2'

function saveConfig(config: { theme: string; language: string }) {
  try {
    localStorage.setItem(`userConfig:${VERSION}`, JSON.stringify(config))
  } catch {
    // Throws in incognito/private browsing, quota exceeded, or disabled
  }
}

function loadConfig() {
  try {
    const data = localStorage.getItem(`userConfig:${VERSION}`)
    return data ? JSON.parse(data) : null
  } catch {
    return null
  }
}

// Migration from v1 to v2
function migrate() {
  try {
    const v1 = localStorage.getItem('userConfig:v1')
    if (v1) {
      const old = JSON.parse(v1)
      saveConfig({ theme: old.darkMode ? 'dark' : 'light', language: old.lang })
      localStorage.removeItem('userConfig:v1')
    }
  } catch {}
}
```

**サーバーレスポンスからは最小限のフィールドのみ保存:**

```typescript
// User object has 20+ fields, only store what UI needs
function cachePrefs(user: FullUser) {
  try {
    localStorage.setItem('prefs:v1', JSON.stringify({
      theme: user.preferences.theme,
      notifications: user.preferences.notifications
    }))
  } catch {}
}
```

**必ず try-catch で囲む:** `getItem()` / `setItem()` は、シークレット/プライベートブラウズ（Safari/Firefox）、容量超過、無効化時に例外を投げます。

**利点:** バージョニングによるスキーマ進化、保存サイズ削減、トークン/PII/内部フラグの保存防止。

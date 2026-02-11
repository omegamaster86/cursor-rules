---
title: ループ内のプロパティ参照をキャッシュする
impact: LOW-MEDIUM
impactDescription: reduces lookups
tags: javascript, loops, optimization, caching
---

## ループ内のプロパティ参照をキャッシュする

このルールの目的はパフォーマンスと保守性の向上です。以下に非推奨例と推奨例を示します。

ホットパスではオブジェクトのプロパティ参照をキャッシュします。

**Incorrect（3 lookups × N iterations):**

```typescript
for (let i = 0; i < arr.length; i++) {
  process(obj.config.settings.value)
}
```

**Correct（1 lookup total):**

```typescript
const value = obj.config.settings.value
const len = arr.length
for (let i = 0; i < len; i++) {
  process(value)
}
```

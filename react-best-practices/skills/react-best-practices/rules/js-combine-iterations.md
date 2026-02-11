---
title: 配列反復をまとめる
impact: LOW-MEDIUM
impactDescription: reduces iterations
tags: javascript, arrays, loops, performance
---

## 配列反復をまとめる

このルールの目的はパフォーマンスと保守性の向上です。以下に非推奨例と推奨例を示します。

`.filter()` や `.map()` を複数回呼ぶと配列を何度も走査します。1 回のループに統合してください。

**Incorrect（3 iterations):**

```typescript
const admins = users.filter(u => u.isAdmin)
const testers = users.filter(u => u.isTester)
const inactive = users.filter(u => !u.isActive)
```

**Correct（1 iteration):**

```typescript
const admins: User[] = []
const testers: User[] = []
const inactive: User[] = []

for (const user of users) {
  if (user.isAdmin) admins.push(user)
  if (user.isTester) testers.push(user)
  if (!user.isActive) inactive.push(user)
}
```

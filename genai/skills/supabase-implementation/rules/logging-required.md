---
title: Required Logging
impact: HIGH
impactDescription: Edge Function の必須ログ（handler 内包）
tags: supabase, logging, edge-functions
---

## Required Logging

標準 Edge Function では `handler()` が開始・終了・例外ログを担う。

**必須（handler が自動）：**

- リクエスト開始（`loggingStart`）
- 成功 / 失敗終了（`loggingEnd`）
- 未処理例外（`loggingError`）

**ビジネスロジック側：**

```typescript
ctx.log("todo_created", { todoId });
```

自前で `Deno.serve` を書く例外系では `createRequestLogger(req)` を使い、同等の start / end / error を手動で呼ぶ。

**旧 API（使わない）：** `createLogger` / `start()` / `end()` / `action` フィールド中心の記述。

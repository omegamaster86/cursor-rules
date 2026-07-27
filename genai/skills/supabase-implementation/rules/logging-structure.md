---
title: Structured Logging (createRequestLogger)
impact: HIGH
impactDescription: Edge Functions の構造化ログ API
tags: supabase, logging, createRequestLogger
---

## Structured Logging (createRequestLogger)

**API（`_shared/logger.ts`）：**

```typescript
import { createRequestLogger } from "./logger.ts";

const logger = createRequestLogger(req);
logger.loggingStart({ function: "create-todo" });
logger.loggingInfo("message", { meta: true });
logger.loggingWarn("message", { meta: true });
logger.loggingError(err, { context: "..." });
logger.loggingEnd({ errorMessage?: string });
```

メソッド名は **camelCase**（`LoggingStart` ではない）。

センシティブキー（password / token / email 等）は自動マスク。`MASK_TARGETS` 環境変数で上書き可。

標準 CRUD では `handler()` 経由で十分なため、この API を直接触るのは例外系が中心。

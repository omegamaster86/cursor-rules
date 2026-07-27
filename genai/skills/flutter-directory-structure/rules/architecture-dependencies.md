---
title: Architecture Dependencies
impact: HIGH
impactDescription: 依存の方向
tags: architecture, dependencies, flutter
---

## Architecture Dependencies

```
presentation → providers / controllers → data/repository → Supabase
```

- presentation が repository を `@riverpod` 経由で使うのは許容
- domain インターフェース必須ではない（具象 Repository でよい）
- UI から直接 `Supabase.instance` を触らず、Repository / Manager 経由

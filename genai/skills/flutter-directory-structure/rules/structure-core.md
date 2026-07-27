---
title: Core Directory
impact: HIGH
impactDescription: 横断関心の配置
tags: structure, core, flutter
---

## Core Directory

```
lib/core/
├── constants.dart           # AppConstants（String.fromEnvironment）
├── exceptions.dart          # AppException / EdgeFunctionException
├── supabase_client.dart     # SupabaseClientManager
├── enums/                   # TodoStatus 等
├── notifications/           # FCM / local notifications
└── widgets/                 # logout_button, loading_screen, main_shell 等（フラット）
```

**必須ではない（starter 未使用）:** `core/errors/`, `core/network/`, `core/theme/`, `core/providers/`, `core/types/`

テーマは現状 `app.dart` で `ThemeData` 直書きでもよい。抽出は規模に応じて。

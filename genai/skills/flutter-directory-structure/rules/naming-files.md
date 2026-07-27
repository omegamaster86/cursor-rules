---
title: File Naming
impact: MEDIUM
impactDescription: snake_case ファイル名
tags: naming, files, flutter
---

## File Naming

```
auth_repository.dart       # impl 分離なしで可
login_screen.dart
login_controller.dart
todo.dart                  # Freezed model
```

`*_repository_impl.dart` / `*_notifier.dart` は必須ではない（`*Controller` が標準）。

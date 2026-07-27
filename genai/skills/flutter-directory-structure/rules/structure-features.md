---
title: Features Directory
impact: HIGH
impactDescription: 機能単位のディレクトリ構成
tags: structure, features, flutter
---

## Features Directory

**標準（簡略 Feature-First）：**

```
features/todos/
├── data/
│   ├── todo_repository.dart      # @riverpod 可
│   └── models/
│       └── todo.dart             # Freezed（*Model / entity 分離なし）
├── providers/
│   └── todo_provider.dart
└── presentation/
    ├── todos_screen.dart
    └── widgets/
```

```
features/auth/
├── data/
│   └── auth_repository.dart
├── providers/
│   └── auth_provider.dart
└── presentation/
    └── login/
        ├── login_screen.dart
        ├── login_controller.dart
        └── widgets/
            └── login_form.dart
```

- `domain/` は置かない（オプション）
- `presentation/screens/` サブフォルダは必須ではない（画面名ディレクトリでよい）
- settings のように presentation のみの薄い feature も可

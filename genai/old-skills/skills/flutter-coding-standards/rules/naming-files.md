---
title: File Naming
impact: MEDIUM
impactDescription: ファイル・ディレクトリの命名規則
tags: dart, naming, files, directories
---

## File Naming

ファイル・ディレクトリの命名規則です。

**Dart ファイル（snake_case）：**

```
✅ 良い例
user_profile.dart
auth_repository.dart
login_use_case.dart
primary_button.dart
login_screen.dart

❌ 悪い例
UserProfile.dart // PascalCase
userProfile.dart // camelCase
user-profile.dart // kebab-case
```

**クラス名との対応：**

| クラス名 | ファイル名 |
|----------|------------|
| `UserProfile` | `user_profile.dart` |
| `AuthRepository` | `auth_repository.dart` |
| `LoginUseCase` | `login_use_case.dart` |
| `PrimaryButton` | `primary_button.dart` |

**生成ファイル：**

```
user_model.dart
user_model.freezed.dart   // Freezed
user_model.g.dart         // json_serializable

auth_provider.dart
auth_provider.g.dart      // Riverpod Generator
```

**ディレクトリ（snake_case + 複数形）：**

```
✅ 良い例
features/
  auth/
    data/
      datasources/
      models/
      repositories/
    domain/
      entities/
      repositories/
      usecases/
    presentation/
      providers/
      screens/
      widgets/

❌ 悪い例
Features/ // PascalCase
user-profile/ // kebab-case
```

**Feature ディレクトリ構成：**

```
features/
├── auth/
│   ├── data/
│   │   ├── datasources/
│   │   │   └── auth_remote_data_source.dart
│   │   ├── models/
│   │   │   └── user_model.dart
│   │   └── repositories/
│   │       └── auth_repository_impl.dart
│   ├── domain/
│   │   ├── entities/
│   │   │   └── user.dart
│   │   ├── repositories/
│   │   │   └── auth_repository.dart
│   │   └── usecases/
│   │       ├── get_current_user.dart
│   │       └── login.dart
│   └── presentation/
│       ├── providers/
│       │   └── auth_notifier.dart
│       ├── screens/
│       │   └── login_screen.dart
│       └── widgets/
│           └── login_form.dart
└── home/
    └── ...
```

**共通ファイルの配置：**

```
lib/
├── core/
│   ├── constants/
│   │   └── app_constants.dart
│   ├── errors/
│   │   ├── exceptions.dart
│   │   └── failures.dart
│   ├── providers/
│   │   └── auth_state_provider.dart
│   ├── theme/
│   │   ├── app_theme.dart
│   │   └── colors.dart
│   ├── types/
│   │   └── api_response.dart
│   └── widgets/
│       └── buttons/
│           └── primary_button.dart
└── features/
    └── ...
```

**チェックリスト：**

- [ ] ファイル名は snake_case
- [ ] ディレクトリ名は snake_case + 複数形
- [ ] クラス名を snake_case に変換した名前
- [ ] 生成ファイルの拡張子（`.freezed.dart`, `.g.dart`）
- [ ] Feature-First 構成に従っている

---
title: File Naming Conventions
impact: MEDIUM
impactDescription: ファイル命名規則（snake_case）
tags: flutter, naming, files, snake-case
---

## File Naming Conventions

Dart/Flutter プロジェクトにおけるファイル命名規則です。

**基本ルール：**

- **スネークケース（snake_case）** を使用
- 小文字とアンダースコアのみ

**接尾辞による分類：**

| 接尾辞 | 用途 | 例 |
|--------|------|-----|
| `_screen.dart` | 画面ウィジェット | `login_screen.dart` |
| `_widget.dart` | 再利用可能なウィジェット（オプション） | `custom_button_widget.dart` |
| `_provider.dart` | Riverpod プロバイダー定義 | `auth_provider.dart` |
| `_provider.g.dart` | Riverpod 生成ファイル（自動生成） | `auth_provider.g.dart` |
| `_notifier.dart` | 状態管理 Notifier クラス | `auth_notifier.dart` |
| `_model.dart` | データモデル | `user_model.dart` |
| `_repository.dart` | リポジトリ | `auth_repository.dart` |
| `_repository_impl.dart` | リポジトリ実装 | `auth_repository_impl.dart` |
| `_data_source.dart` | データソース | `auth_remote_data_source.dart` |
| `_usecase.dart` | ユースケース | `login_usecase.dart` |

**例：**

```
features/auth/
├── data/
│   ├── datasources/
│   │   ├── auth_local_data_source.dart
│   │   └── auth_remote_data_source.dart
│   ├── models/
│   │   └── user_model.dart
│   └── repositories/
│       └── auth_repository_impl.dart
├── domain/
│   ├── entities/
│   │   └── user.dart                    # エンティティは接尾辞なし
│   ├── repositories/
│   │   └── auth_repository.dart
│   └── usecases/
│       ├── login.dart                   # シンプルなユースケースは接尾辞なし
│       └── logout.dart
└── presentation/
    ├── providers/
    │   ├── auth_provider.dart
    │   ├── auth_provider.g.dart         # 自動生成
    │   └── auth_notifier.dart
    └── screens/
        ├── login_screen.dart
        └── register_screen.dart
```

**NG 例：**

```dart
// ❌ キャメルケース
loginScreen.dart
userModel.dart

// ❌ パスカルケース
LoginScreen.dart
UserModel.dart

// ❌ ハイフン
login-screen.dart
user-model.dart
```

**チェックリスト：**

- [ ] すべてのファイル名はスネークケース
- [ ] 適切な接尾辞を使用
- [ ] 生成ファイル（`.g.dart`）は自動生成に任せる
- [ ] エンティティは接尾辞なし（または `_entity.dart`）

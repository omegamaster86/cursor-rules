---
title: Class Naming Conventions
impact: MEDIUM
impactDescription: クラス命名規則（PascalCase）
tags: flutter, naming, classes, pascal-case
---

## Class Naming Conventions

Dart/Flutter プロジェクトにおけるクラス命名規則です。

**基本ルール：**

- **パスカルケース（PascalCase）** を使用
- 各単語の先頭を大文字に

**接尾辞による分類：**

| 接尾辞 | 用途 | 例 |
|--------|------|-----|
| `Screen` | 画面ウィジェット | `LoginScreen` |
| `Notifier` | Riverpod Notifier クラス | `AuthNotifier` |
| `Model` | データモデル（JSON対応） | `UserModel` |
| `Repository` | リポジトリインターフェース | `AuthRepository` |
| `RepositoryImpl` | リポジトリ実装 | `AuthRepositoryImpl` |
| `DataSource` | データソース | `AuthRemoteDataSource` |
| `UseCase` | ユースケース | `LoginUseCase` |
| `Failure` | エラークラス | `ServerFailure` |
| `Exception` | 例外クラス | `NetworkException` |

**Riverpod プロバイダーの命名：**

| 種別 | 命名規則 | 例 |
|------|----------|-----|
| プロバイダー変数 | `camelCase` + `Provider` | `authNotifierProvider` |
| Notifier クラス | `PascalCase` + `Notifier` | `AuthNotifier` |
| State クラス | `PascalCase` + `State` | `AuthState` |

**クラス定義例：**

```dart
// 画面ウィジェット
class LoginScreen extends ConsumerWidget { ... }
class RegisterScreen extends StatelessWidget { ... }

// Notifier
@riverpod
class AuthNotifier extends _$AuthNotifier { ... }

// リポジトリ
abstract class AuthRepository { ... }
class AuthRepositoryImpl implements AuthRepository { ... }

// データソース
class AuthRemoteDataSource { ... }
class AuthLocalDataSource { ... }

// モデル
@freezed
class UserModel with _$UserModel { ... }

// エンティティ
class User { ... }

// ユースケース
class LoginUseCase { ... }
class LogoutUseCase { ... }

// エラー
class ServerFailure extends Failure { ... }
class NetworkException implements Exception { ... }
```

**ファイル名とクラス名の対応：**

| ファイル名 | クラス名 |
|------------|----------|
| `login_screen.dart` | `LoginScreen` |
| `user_model.dart` | `UserModel` |
| `auth_repository.dart` | `AuthRepository` |
| `auth_repository_impl.dart` | `AuthRepositoryImpl` |
| `auth_notifier.dart` | `AuthNotifier` |

**チェックリスト：**

- [ ] すべてのクラス名はパスカルケース
- [ ] 適切な接尾辞を使用
- [ ] ファイル名とクラス名が対応している
- [ ] Riverpod プロバイダー変数はキャメルケース + Provider

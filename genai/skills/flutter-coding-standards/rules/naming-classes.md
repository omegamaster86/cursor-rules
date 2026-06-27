---
title: Class Naming
impact: MEDIUM
impactDescription: クラスの命名規則
tags: dart, naming, classes
---

## Class Naming

クラスの命名規則です。

**基本規則（PascalCase）：**

```dart
// ✅ 良い例
class UserProfile { /* ... */ }
class AuthRepository { /* ... */ }
class LoginUseCase { /* ... */ }
class ProductListNotifier { /* ... */ }

// ❌ 悪い例
class userProfile { /* ... */ } // camelCase
class User { /* ... */ } // 役割が不明確
class Data { /* ... */ } // 意味が不明確
```

**接尾辞規則：**

| 種別 | 接尾辞 | 例 |
|------|--------|-----|
| Entity | なし | `User`, `Product` |
| Model | `Model` | `UserModel`, `ProductModel` |
| Repository | `Repository` | `AuthRepository` |
| UseCase | `UseCase` | `LoginUseCase` |
| DataSource | `DataSource` | `AuthRemoteDataSource` |
| Notifier | `Notifier` | `AuthNotifier` |
| Screen/Page | `Screen`/`Page` | `LoginScreen`, `HomePage` |
| Widget | 内容による | `PrimaryButton`, `UserCard` |
| Exception | `Exception` | `ServerException` |
| Failure | `Failure` | `ServerFailure` |

**Clean Architecture での命名：**

```dart
// Entity（ドメイン層）
class User { /* ... */ }

// Model（データ層、JSON対応）
class UserModel { /* ... */ }

// Repository インターフェース（ドメイン層）
abstract class UserRepository { /* ... */ }

// Repository 実装（データ層）
class UserRepositoryImpl implements UserRepository { /* ... */ }

// DataSource（データ層）
abstract class UserRemoteDataSource { /* ... */ }
class UserRemoteDataSourceImpl implements UserRemoteDataSource { /* ... */ }

// UseCase（ドメイン層）
class GetUserById { /* ... */ }
class CreateUser { /* ... */ }

// Notifier（プレゼンテーション層）
class UserNotifier extends _$UserNotifier { /* ... */ }
```

**Widget の命名：**

```dart
// 画面全体
class LoginScreen extends ConsumerWidget { /* ... */ }
class HomeScreen extends StatelessWidget { /* ... */ }

// 再利用可能なウィジェット
class PrimaryButton extends StatelessWidget { /* ... */ }
class UserCard extends StatelessWidget { /* ... */ }
class LoadingIndicator extends StatelessWidget { /* ... */ }

// 画面固有のウィジェット（private）
class _LoginForm extends StatefulWidget { /* ... */ }
class _UserListItem extends StatelessWidget { /* ... */ }
```

**Riverpod Provider（自動生成）：**

```dart
@riverpod
class AuthNotifier extends _$AuthNotifier { /* ... */ }
// → authNotifierProvider

@riverpod
User? currentUser(CurrentUserRef ref) { /* ... */ }
// → currentUserProvider
```

**チェックリスト：**

- [ ] クラス名は PascalCase
- [ ] 役割に応じた接尾辞を使用
- [ ] 実装クラスは `Impl` 接尾辞
- [ ] Screen/Page は画面を表すクラスに使用
- [ ] 意味が明確な名前

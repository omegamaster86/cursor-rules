---
title: Architecture Dependencies
impact: HIGH
impactDescription: 依存関係の方向と依存性逆転の原則
tags: flutter, clean-architecture, dependencies, dip
---

## Architecture Dependencies

Clean Architecture における依存関係の方向と依存性逆転の原則（DIP）です。

**依存の方向：**

```
presentation → domain ← data
```

- `presentation` は `domain` に依存
- `data` は `domain` に依存
- `domain` は他の層に依存しない（純粋なビジネスロジック）

**依存性逆転の原則（DIP）：**

`domain` 層でインターフェース（抽象クラス）を定義し、`data` 層で実装します：

```dart
// domain/repositories/auth_repository.dart（インターフェース）
abstract class AuthRepository {
  Future<Either<Failure, User>> login(String email, String password);
  Future<Either<Failure, void>> logout();
  Future<Either<Failure, User?>> getCurrentUser();
}
```

```dart
// data/repositories/auth_repository_impl.dart（実装）
class AuthRepositoryImpl implements AuthRepository {
  final AuthRemoteDataSource remoteDataSource;
  final AuthLocalDataSource localDataSource;

  AuthRepositoryImpl({
    required this.remoteDataSource,
    required this.localDataSource,
  });

  @override
  Future<Either<Failure, User>> login(String email, String password) async {
    try {
      final userModel = await remoteDataSource.login(email, password);
      await localDataSource.cacheUser(userModel);
      return Right(userModel.toEntity());
    } catch (e) {
      return Left(ServerFailure());
    }
  }
}
```

**Riverpod での依存性注入：**

```dart
// プロバイダーで依存性を注入
@riverpod
AuthRepository authRepository(AuthRepositoryRef ref) {
  return AuthRepositoryImpl(
    remoteDataSource: ref.watch(authRemoteDataSourceProvider),
    localDataSource: ref.watch(authLocalDataSourceProvider),
  );
}
```

**依存関係のルール：**

| 層 | 依存先 | 禁止事項 |
|----|--------|----------|
| `presentation` | `domain` のみ | `data` への直接依存禁止 |
| `domain` | なし | 外部ライブラリ・他の層への依存禁止 |
| `data` | `domain` のみ | `presentation` への依存禁止 |

**チェックリスト：**

- [ ] `domain` 層は他の層に依存しない
- [ ] リポジトリは `domain` でインターフェース、`data` で実装
- [ ] `presentation` から `data` への直接依存がない
- [ ] 依存性注入は Riverpod で行う

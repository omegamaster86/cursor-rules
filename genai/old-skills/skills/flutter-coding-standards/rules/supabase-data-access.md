---
title: Supabase Data Access
impact: CRITICAL
impactDescription: データアクセスの階層構造（Clean Architecture）
tags: flutter, supabase, clean-architecture, data-access
---

## Supabase Data Access

データベースアクセスは Clean Architecture に基づいた階層構造で実装します。

**階層構造：**

```
Widget (UI)
  ↓ ref.watch/ref.read
Provider (Riverpod)
  ↓ 依存性注入
UseCase (Domain)
  ↓ リポジトリ呼び出し
Repository (Domain Interface → Data Implementation)
  ↓ データソース呼び出し
DataSource (API通信)
  ↓ HTTP/RPC
Supabase Edge Function / Database
```

**DataSource（データソース層）：**

```dart
// features/auth/data/datasources/auth_remote_data_source.dart
abstract class AuthRemoteDataSource {
  Future<UserModel> getUserById(String userId);
  Future<UserModel> getCurrentUser();
}

class AuthRemoteDataSourceImpl implements AuthRemoteDataSource {
  final SupabaseClient _supabase;

  AuthRemoteDataSourceImpl(this._supabase);

  @override
  Future<UserModel> getUserById(String userId) async {
    final response = await _supabase.functions.invoke(
      'get-user-data',
      queryParameters: {'userId': userId},
    );

    if (response.status != 200) {
      throw Exception('ユーザー情報の取得に失敗しました');
    }

    final data = response.data as Map<String, dynamic>;
    if (data['success'] != true) {
      throw Exception(data['error'] ?? 'Unknown error');
    }

    return UserModel.fromJson(data['data']);
  }
}
```

**Repository（リポジトリ層）：**

```dart
// Domain インターフェース
abstract class AuthRepository {
  Future<Either<Failure, User>> getUserById(String userId);
  Future<Either<Failure, User>> getCurrentUser();
}

// Data 実装
class AuthRepositoryImpl implements AuthRepository {
  final AuthRemoteDataSource _remoteDataSource;

  AuthRepositoryImpl(this._remoteDataSource);

  @override
  Future<Either<Failure, User>> getUserById(String userId) async {
    try {
      final userModel = await _remoteDataSource.getUserById(userId);
      return Right(userModel.toEntity());
    } catch (e) {
      return Left(ServerFailure(e.toString()));
    }
  }
}
```

**UseCase（ユースケース層）：**

```dart
class GetCurrentUser {
  final AuthRepository _repository;

  GetCurrentUser(this._repository);

  Future<Either<Failure, User>> call() {
    return _repository.getCurrentUser();
  }
}
```

**Provider（プロバイダー層）：**

```dart
@riverpod
AuthRemoteDataSource authRemoteDataSource(AuthRemoteDataSourceRef ref) {
  final supabase = ref.watch(supabaseClientProvider);
  return AuthRemoteDataSourceImpl(supabase);
}

@riverpod
AuthRepository authRepository(AuthRepositoryRef ref) {
  final dataSource = ref.watch(authRemoteDataSourceProvider);
  return AuthRepositoryImpl(dataSource);
}

@riverpod
GetCurrentUser getCurrentUser(GetCurrentUserRef ref) {
  final repository = ref.watch(authRepositoryProvider);
  return GetCurrentUser(repository);
}
```

**ファイル配置：**

| 層 | 配置場所 |
|----|----------|
| DataSource | `features/[機能]/data/datasources/` |
| Model | `features/[機能]/data/models/` |
| Repository 実装 | `features/[機能]/data/repositories/` |
| Entity | `features/[機能]/domain/entities/` |
| Repository インターフェース | `features/[機能]/domain/repositories/` |
| UseCase | `features/[機能]/domain/usecases/` |
| Provider | `features/[機能]/presentation/providers/` |

**チェックリスト：**

- [ ] Clean Architecture の階層構造に従っている
- [ ] DataSource で API 通信を実装
- [ ] Repository で Either 型を返す
- [ ] UseCase でビジネスロジックを実装
- [ ] Provider で依存性注入

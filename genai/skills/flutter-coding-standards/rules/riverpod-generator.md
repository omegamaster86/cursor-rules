---
title: Riverpod Generator
impact: HIGH
impactDescription: riverpod_generator を使用したプロバイダー定義
tags: flutter, riverpod, generator, code-generation
---

## Riverpod Generator

基本的に `riverpod_generator` を使用してプロバイダーを生成します。

**基本的な使い方：**

```dart
import 'package:riverpod_annotation/riverpod_annotation.dart';

part 'user_provider.g.dart';

// 単純な値を提供
@riverpod
String greeting(GreetingRef ref) => 'Hello';

// 非同期でデータを取得
@riverpod
Future<User> currentUser(CurrentUserRef ref) async {
  final repository = ref.watch(userRepositoryProvider);
  return repository.getCurrentUser();
}

// Stream を提供
@riverpod
Stream<AuthState> authState(AuthStateRef ref) {
  final supabase = ref.watch(supabaseClientProvider);
  return supabase.auth.onAuthStateChange;
}
```

**Notifier（複雑な状態管理）：**

```dart
@riverpod
class UserListNotifier extends _$UserListNotifier {
  @override
  Future<List<User>> build() async {
    return ref.watch(userRepositoryProvider).getUsers();
  }

  Future<void> refresh() async {
    state = const AsyncValue.loading();
    state = await AsyncValue.guard(() => 
      ref.read(userRepositoryProvider).getUsers()
    );
  }

  Future<void> addUser(User user) async {
    final currentUsers = state.valueOrNull ?? [];
    state = AsyncValue.data([...currentUsers, user]);
  }
}
```

**keepAlive オプション：**

```dart
// アプリ起動中は破棄されない（認証状態など）
@Riverpod(keepAlive: true)
SupabaseClient supabaseClient(SupabaseClientRef ref) {
  return Supabase.instance.client;
}

// デフォルト：参照がなくなると破棄される
@riverpod
Future<User> userProfile(UserProfileRef ref) async {
  // ...
}
```

**依存性注入パターン：**

```dart
// DataSource
@riverpod
AuthRemoteDataSource authRemoteDataSource(AuthRemoteDataSourceRef ref) {
  final supabase = ref.watch(supabaseClientProvider);
  return AuthRemoteDataSourceImpl(supabase);
}

// Repository（DataSource に依存）
@riverpod
AuthRepository authRepository(AuthRepositoryRef ref) {
  final dataSource = ref.watch(authRemoteDataSourceProvider);
  return AuthRepositoryImpl(dataSource);
}

// UseCase（Repository に依存）
@riverpod
LoginUseCase loginUseCase(LoginUseCaseRef ref) {
  final repository = ref.watch(authRepositoryProvider);
  return LoginUseCase(repository);
}
```

**コード生成：**

```bash
flutter pub run build_runner build --delete-conflicting-outputs
```

**生成されるプロバイダー名：**

| アノテーション | 生成されるプロバイダー |
|---------------|----------------------|
| `@riverpod` 関数 | `関数名Provider` |
| `@riverpod` Notifier | `クラス名Provider` |
| `@Riverpod(keepAlive: true)` | keepAlive 付きプロバイダー |

**チェックリスト：**

- [ ] `part 'xxx.g.dart'` を追加
- [ ] `@riverpod` アノテーションを使用
- [ ] 永続化が必要な場合は `@Riverpod(keepAlive: true)`
- [ ] Notifier は `_$クラス名` を継承
- [ ] コード生成を実行

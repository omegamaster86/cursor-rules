---
title: Riverpod Generator
impact: HIGH
impactDescription: riverpod_generator を使用したプロバイダー定義
tags: flutter, riverpod, generator, code-generation
---

## Riverpod Generator

基本的に `riverpod_generator` を使用してプロバイダーを生成します。

**Repository（data 層に同居可）：**

```dart
@riverpod
TodoRepository todoRepository(Ref ref) => TodoRepository();
```

**機能横断 Auth：**

```dart
@Riverpod(keepAlive: true)
class Auth extends _$Auth {
  @override
  Stream<User?> build() {
    return ref.watch(authRepositoryProvider).onAuthStateChange;
  }
}
```

**画面 Controller：**

```dart
@riverpod
class LoginController extends _$LoginController {
  @override
  FutureOr<void> build() {}

  Future<void> submit(String email, String password) async {
    // ...
  }
}
```

グローバルな `supabaseClientProvider` は必須ではない。クライアントは `SupabaseClientManager` 経由。

```bash
dart run build_runner build --delete-conflicting-outputs
```

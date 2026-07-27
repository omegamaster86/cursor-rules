---
title: Supabase Auth
impact: CRITICAL
impactDescription: Auth 状態管理
tags: supabase, auth, flutter, riverpod
---

## Supabase Auth

**標準（dev-starter）:**

- `features/auth/providers/auth_provider.dart` — `@Riverpod(keepAlive: true) class Auth`
- `features/auth/data/auth_repository.dart` — `onAuthStateChange` 等
- DI: `SupabaseClientManager`（`core/supabase_client.dart`）

```dart
@Riverpod(keepAlive: true)
class Auth extends _$Auth {
  @override
  Stream<User?> build() {
    return ref.watch(authRepositoryProvider).onAuthStateChange;
  }
}
```

旧例の `core/providers/auth_state_provider.dart` + グローバル `supabaseClientProvider` は使わない。

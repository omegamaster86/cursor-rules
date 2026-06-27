---
title: Supabase Authentication
impact: CRITICAL
impactDescription: Supabase 認証状態の管理
tags: flutter, supabase, authentication, riverpod
---

## Supabase Authentication

Supabase の認証機能を Flutter で使用する際の規約です。

**認証状態の管理（Riverpod）：**

```dart
// lib/core/providers/auth_state_provider.dart
import 'package:riverpod_annotation/riverpod_annotation.dart';
import 'package:supabase_flutter/supabase_flutter.dart';

part 'auth_state_provider.g.dart';

@Riverpod(keepAlive: true)
SupabaseClient supabaseClient(SupabaseClientRef ref) {
  return Supabase.instance.client;
}

@riverpod
Stream<AuthState> authStateChanges(AuthStateChangesRef ref) {
  final client = ref.watch(supabaseClientProvider);
  return client.auth.onAuthStateChange;
}

@riverpod
User? currentUser(CurrentUserRef ref) {
  final authState = ref.watch(authStateChangesProvider);
  return authState.whenData((state) => state.session?.user).valueOrNull;
}
```

**認証ガードの実装：**

```dart
class AuthGuard extends ConsumerWidget {
  final Widget child;

  const AuthGuard({super.key, required this.child});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final authState = ref.watch(authStateChangesProvider);

    return authState.when(
      data: (state) {
        if (state.session == null) {
          WidgetsBinding.instance.addPostFrameCallback((_) {
            context.go('/login');
          });
          return const SizedBox.shrink();
        }
        return child;
      },
      loading: () => const Center(child: CircularProgressIndicator()),
      error: (error, stack) => Center(child: Text('Error: $error')),
    );
  }
}
```

**ログイン処理：**

```dart
@riverpod
class AuthNotifier extends _$AuthNotifier {
  @override
  FutureOr<void> build() {}

  Future<void> signInWithEmail(String email, String password) async {
    state = const AsyncValue.loading();

    state = await AsyncValue.guard(() async {
      final supabase = ref.read(supabaseClientProvider);
      await supabase.auth.signInWithPassword(
        email: email,
        password: password,
      );
    });
  }

  Future<void> signOut() async {
    state = const AsyncValue.loading();

    state = await AsyncValue.guard(() async {
      final supabase = ref.read(supabaseClientProvider);
      await supabase.auth.signOut();
    });
  }
}
```

**セッショントークンの取得：**

```dart
Future<void> callEdgeFunction() async {
  final supabase = Supabase.instance.client;
  final session = supabase.auth.currentSession;

  if (session == null) {
    throw Exception('認証が必要です');
  }

  final accessToken = session.accessToken;

  // Edge Function 呼び出しに使用
  final response = await supabase.functions.invoke(
    'function-name',
    headers: {
      'Authorization': 'Bearer $accessToken',
    },
  );
}
```

**認証規約まとめ：**

| 用途 | 方法 |
|------|------|
| 認証状態の監視 | `StreamProvider` + `onAuthStateChange` |
| 現在のユーザー取得 | `supabase.auth.currentUser` |
| アクセストークン取得 | `session.accessToken` |
| ログイン | `signInWithPassword` |
| ログアウト | `signOut` |

**チェックリスト：**

- [ ] `@Riverpod(keepAlive: true)` で Supabase クライアントを永続化
- [ ] `StreamProvider` で認証状態を監視
- [ ] 認証ガードを実装
- [ ] エラーハンドリングを実装

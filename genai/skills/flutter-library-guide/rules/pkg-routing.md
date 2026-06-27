---
title: Go Router Routing
impact: HIGH
impactDescription: go_router によるルーティング
tags: flutter, routing, go-router, navigation
---

## Go Router Routing

go_router を使用した宣言的ルーティングのパターンです。

**インストール：**

```yaml
dependencies:
  go_router: ^13.0.0
```

**基本設定：**

```dart
// config/routes/app_router.dart
import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:riverpod_annotation/riverpod_annotation.dart';

part 'app_router.g.dart';

@riverpod
GoRouter appRouter(AppRouterRef ref) {
  return GoRouter(
    initialLocation: '/',
    routes: [
      GoRoute(
        path: '/',
        name: 'home',
        builder: (context, state) => const HomeScreen(),
      ),
      GoRoute(
        path: '/login',
        name: 'login',
        builder: (context, state) => const LoginScreen(),
      ),
      GoRoute(
        path: '/profile/:userId',
        name: 'profile',
        builder: (context, state) {
          final userId = state.pathParameters['userId']!;
          return ProfileScreen(userId: userId);
        },
      ),
    ],
    errorBuilder: (context, state) => ErrorScreen(error: state.error),
  );
}
```

**MaterialApp.router での使用：**

```dart
class MyApp extends ConsumerWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final router = ref.watch(appRouterProvider);
    
    return MaterialApp.router(
      routerConfig: router,
      title: 'My App',
      theme: ThemeData.light(),
    );
  }
}
```

**ナビゲーション：**

```dart
// 名前付きルート
context.goNamed('profile', pathParameters: {'userId': '123'});

// パスで直接
context.go('/profile/123');

// プッシュ（戻れる）
context.pushNamed('profile', pathParameters: {'userId': '123'});

// 戻る
context.pop();
```

**リダイレクト（認証ガード）：**

```dart
GoRouter(
  redirect: (context, state) {
    final isLoggedIn = ref.read(authStateProvider).value != null;
    final isLoginRoute = state.matchedLocation == '/login';
    
    if (!isLoggedIn && !isLoginRoute) {
      return '/login';
    }
    if (isLoggedIn && isLoginRoute) {
      return '/';
    }
    return null;
  },
  // ...
);
```

**チェックリスト：**

- [ ] `GoRouter` を Riverpod プロバイダーで管理
- [ ] `MaterialApp.router` を使用
- [ ] パスパラメータは `pathParameters` で取得
- [ ] 認証ガードは `redirect` で実装

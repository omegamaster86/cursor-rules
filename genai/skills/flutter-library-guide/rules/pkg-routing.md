---
title: go_router
impact: HIGH
impactDescription: ルーティング
tags: go_router, routing, flutter
---

## go_router

**標準（dev-starter）:** 手書き `Provider<GoRouter>` + `refreshListenable`（`@riverpod` codegen 必須ではない）。

```dart
// config/routes/router.dart
final routerProvider = Provider<GoRouter>((ref) {
  final refresh = _RouterNotifier(ref);
  return GoRouter(
    refreshListenable: refresh,
    // StatefulShellRoute 等
  );
});
```

参考版: `go_router: ^14.6.2`

旧例の `app_router.g.dart` / `@riverpod GoRouter` は任意パターン。

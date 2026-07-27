---
title: Riverpod Best Practices
impact: HIGH
impactDescription: Riverpod のベストプラクティス
tags: flutter, riverpod, best-practices
---

## Riverpod Best Practices

Riverpod を使用する際のベストプラクティスです。

**AsyncValue の使用：**

```dart
class ProductListScreen extends ConsumerWidget {
  const ProductListScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final productsAsync = ref.watch(productListProvider);

    return productsAsync.when(
      data: (products) => ListView.builder(
        itemCount: products.length,
        itemBuilder: (context, index) => ProductCard(product: products[index]),
      ),
      loading: () => const Center(child: CircularProgressIndicator()),
      error: (error, stack) => Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text('エラー: $error'),
            ElevatedButton(
              onPressed: () => ref.invalidate(productListProvider),
              child: const Text('再試行'),
            ),
          ],
        ),
      ),
    );
  }
}
```

**ref.watch vs ref.read：**

```dart
// ✅ 良い例
@override
Widget build(BuildContext context, WidgetRef ref) {
  // UI の再構築が必要な場合は watch
  final user = ref.watch(currentUserProvider);
  
  return ElevatedButton(
    onPressed: () {
      // イベントハンドラ内では read
      ref.read(authNotifierProvider.notifier).signOut();
    },
    child: Text('ログアウト'),
  );
}

// ❌ 悪い例
@override
Widget build(BuildContext context, WidgetRef ref) {
  // build 内で read を使うと再構築されない
  final user = ref.read(currentUserProvider); // ❌
  
  return ElevatedButton(
    onPressed: () {
      // イベントハンドラ内で watch は不要
      ref.watch(authNotifierProvider.notifier).signOut(); // ❌
    },
    child: Text('ログアウト'),
  );
}
```

**ConsumerWidget vs ConsumerStatefulWidget：**

```dart
// ステートレスな場合は ConsumerWidget
class UserProfileWidget extends ConsumerWidget {
  const UserProfileWidget({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final user = ref.watch(currentUserProvider);
    return Text(user?.name ?? 'Guest');
  }
}

// ローカル状態が必要な場合は ConsumerStatefulWidget
class LoginForm extends ConsumerStatefulWidget {
  const LoginForm({super.key});

  @override
  ConsumerState<LoginForm> createState() => _LoginFormState();
}

class _LoginFormState extends ConsumerState<LoginForm> {
  final _emailController = TextEditingController();

  @override
  void dispose() {
    _emailController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    // ref は widget から取得
    final authState = ref.watch(authNotifierProvider);
    // ...
  }
}
```

**アンチパターン：**

```dart
// ❌ 悪い例1：build 内での副作用
@override
Widget build(BuildContext context, WidgetRef ref) {
  ref.read(analyticsProvider).logEvent('screen_view'); // ❌
  return Container();
}

// ✅ 良い例：initState で副作用
@override
void initState() {
  super.initState();
  WidgetsBinding.instance.addPostFrameCallback((_) {
    ref.read(analyticsProvider).logEvent('screen_view');
  });
}

// ❌ 悪い例2：大きすぎるプロバイダー
@riverpod
class AppState extends _$AppState {
  // すべての状態を1つで管理しない
}

// ✅ 良い例：関心事ごとに分割
@riverpod
class UserNotifier extends _$UserNotifier { /* ... */ }

@riverpod
class CartNotifier extends _$CartNotifier { /* ... */ }
```

**プロバイダーのスコープ：**

```dart
// 特定の画面でのみプロバイダーをオーバーライド
MaterialApp(
  home: ProviderScope(
    overrides: [
      authRepositoryProvider.overrideWithValue(MockAuthRepository()),
    ],
    child: const LoginScreen(),
  ),
)
```

**チェックリスト：**

- [ ] build 内では `ref.watch`、イベント内では `ref.read`
- [ ] `AsyncValue.when` でローディング・エラー・データを処理
- [ ] build 内で副作用を起こさない
- [ ] プロバイダーは関心事ごとに分割
- [ ] ローカル状態が必要な場合のみ `ConsumerStatefulWidget`

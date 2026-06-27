---
title: Flutter Riverpod Usage
impact: HIGH
impactDescription: flutter_riverpod の使用方法とベストプラクティス
tags: flutter, riverpod, state-management
---

## Flutter Riverpod Usage

flutter_riverpod を使用した状態管理のベストプラクティスです。

**インストール：**

```yaml
dependencies:
  flutter_riverpod: ^2.4.0
  riverpod_annotation: ^2.3.0

dev_dependencies:
  riverpod_generator: ^2.3.0
  build_runner: ^2.4.0
```

**セットアップ（main.dart）：**

```dart
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  
  runApp(
    const ProviderScope(
      child: MyApp(),
    ),
  );
}
```

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

**ConsumerWidget vs ConsumerStatefulWidget：**

```dart
// ステートレスな場合
class UserProfileWidget extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final user = ref.watch(currentUserProvider);
    return Text(user?.name ?? 'Guest');
  }
}

// ローカル状態が必要な場合
class LoginForm extends ConsumerStatefulWidget {
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
    // ref は widget.ref ではなく this.ref で取得
    final authState = ref.watch(authNotifierProvider);
    // ...
  }
}
```

**チェックリスト：**

- [ ] `ProviderScope` でアプリをラップ
- [ ] `AsyncValue.when()` で状態を処理
- [ ] ローカル状態が不要なら `ConsumerWidget`
- [ ] `ref.invalidate()` でプロバイダーをリフレッシュ

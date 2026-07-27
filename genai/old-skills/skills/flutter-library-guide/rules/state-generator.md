---
title: Riverpod Generator
impact: HIGH
impactDescription: riverpod_generator によるコード生成
tags: flutter, riverpod, code-generation
---

## Riverpod Generator

riverpod_generator を使用したプロバイダー生成のパターンです。

**インストール：**

```yaml
dependencies:
  flutter_riverpod: ^2.4.0
  riverpod_annotation: ^2.3.0

dev_dependencies:
  riverpod_generator: ^2.3.0
  build_runner: ^2.4.0
```

**基本的なプロバイダー：**

```dart
import 'package:riverpod_annotation/riverpod_annotation.dart';

part 'my_provider.g.dart';

// シンプルなプロバイダー（Provider を生成）
@riverpod
String greeting(GreetingRef ref) {
  return 'Hello, World!';
}

// 非同期プロバイダー（FutureProvider を生成）
@riverpod
Future<List<Product>> productList(ProductListRef ref) async {
  final repository = ref.watch(productRepositoryProvider);
  return repository.getProducts();
}

// ストリームプロバイダー（StreamProvider を生成）
@riverpod
Stream<AuthState> authState(AuthStateRef ref) {
  final client = ref.watch(supabaseClientProvider);
  return client.auth.onAuthStateChange;
}
```

**Notifier プロバイダー：**

```dart
@riverpod
class Counter extends _$Counter {
  @override
  int build() => 0;

  void increment() => state++;
  void decrement() => state--;
}

// AsyncNotifier
@riverpod
class ProductNotifier extends _$ProductNotifier {
  @override
  FutureOr<List<Product>> build() async {
    return _fetchProducts();
  }

  Future<List<Product>> _fetchProducts() async {
    final repository = ref.read(productRepositoryProvider);
    return repository.getProducts();
  }

  Future<void> addProduct(Product product) async {
    state = const AsyncValue.loading();
    state = await AsyncValue.guard(() async {
      final repository = ref.read(productRepositoryProvider);
      await repository.addProduct(product);
      return _fetchProducts();
    });
  }
}
```

**keepAlive オプション：**

```dart
// アプリ全体で保持するプロバイダー
@Riverpod(keepAlive: true)
SupabaseClient supabaseClient(SupabaseClientRef ref) {
  return Supabase.instance.client;
}
```

**コード生成コマンド：**

```bash
# 一度だけ生成
flutter pub run build_runner build --delete-conflicting-outputs

# ウォッチモード（開発中に自動生成）
flutter pub run build_runner watch --delete-conflicting-outputs
```

**チェックリスト：**

- [ ] `part 'xxx.g.dart';` を忘れずに追加
- [ ] 関数名がプロバイダー名になる（`greeting` → `greetingProvider`）
- [ ] グローバルプロバイダーは `@Riverpod(keepAlive: true)`
- [ ] コード生成後に `.g.dart` ファイルを確認

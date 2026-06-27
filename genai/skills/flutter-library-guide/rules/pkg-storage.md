---
title: Local Storage
impact: MEDIUM
impactDescription: ローカルストレージ（isar, shared_preferences, flutter_secure_storage）
tags: flutter, storage, isar, shared-preferences
---

## Local Storage

ローカルストレージの使い分けと実装パターンです。

**パッケージの選択：**

| パッケージ | 用途 | 特徴 |
|-----------|------|------|
| `isar` | 大量データ、複雑なクエリ | NoSQL、高速、型安全 |
| `shared_preferences` | 簡単なキーバリュー | 軽量、設定保存向け |
| `flutter_secure_storage` | 機密情報 | 暗号化ストレージ |

**インストール：**

```yaml
dependencies:
  isar: ^3.1.0
  isar_flutter_libs: ^3.1.0
  shared_preferences: ^2.2.0
  flutter_secure_storage: ^9.0.0

dev_dependencies:
  isar_generator: ^3.1.0
```

**Isar（大量データ）：**

```dart
// モデル定義
import 'package:isar/isar.dart';

part 'product_cache.g.dart';

@collection
class ProductCache {
  Id id = Isar.autoIncrement;
  
  @Index()
  late String productId;
  late String name;
  late double price;
  late DateTime cachedAt;
}

// 初期化
final isar = await Isar.open([ProductCacheSchema]);

// CRUD
await isar.writeTxn(() async {
  await isar.productCaches.put(productCache);
});

final products = await isar.productCaches.where().findAll();
```

**SharedPreferences（設定）：**

```dart
// core/providers/preferences_provider.dart
@Riverpod(keepAlive: true)
Future<SharedPreferences> sharedPreferences(SharedPreferencesRef ref) async {
  return await SharedPreferences.getInstance();
}

// 使用例
final prefs = ref.read(sharedPreferencesProvider).value!;
await prefs.setBool('darkMode', true);
final isDarkMode = prefs.getBool('darkMode') ?? false;
```

**SecureStorage（機密情報）：**

```dart
// core/providers/secure_storage_provider.dart
@Riverpod(keepAlive: true)
FlutterSecureStorage secureStorage(SecureStorageRef ref) {
  return const FlutterSecureStorage();
}

// トークン保存
final storage = ref.read(secureStorageProvider);
await storage.write(key: 'auth_token', value: token);
final token = await storage.read(key: 'auth_token');
await storage.delete(key: 'auth_token');
```

**チェックリスト：**

- [ ] 大量データは `isar`、設定は `shared_preferences`
- [ ] トークンなど機密情報は `flutter_secure_storage`
- [ ] ストレージプロバイダーは `keepAlive: true`
- [ ] Isar は `build_runner` でコード生成が必要

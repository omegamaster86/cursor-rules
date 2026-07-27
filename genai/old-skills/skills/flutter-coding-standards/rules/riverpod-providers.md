---
title: Riverpod Provider Types
impact: HIGH
impactDescription: プロバイダーの種類と適切な使い分け
tags: flutter, riverpod, providers
---

## Riverpod Provider Types

Riverpod のプロバイダー種類と使い分けです。

**プロバイダーの種類：**

| 種別 | 用途 | 使用例 |
|------|------|--------|
| `Provider` | 変更されない値、DI | Repository、Service |
| `FutureProvider` | 非同期で取得する値 | API からのデータ取得 |
| `StreamProvider` | ストリームデータ | リアルタイム、認証状態 |
| `StateProvider` | シンプルな状態 | フィルター、ソート条件 |
| `NotifierProvider` | 複雑な状態管理 | フォーム、ビジネスロジック |
| `AsyncNotifierProvider` | 非同期な状態管理 | CRUD 操作 |

**riverpod_generator の使用：**

```dart
import 'package:riverpod_annotation/riverpod_annotation.dart';

part 'user_provider.g.dart';

// 単純な値
@riverpod
String greeting(GreetingRef ref) => 'Hello';

// 非同期取得
@riverpod
Future<User> currentUser(CurrentUserRef ref) async {
  final repository = ref.watch(userRepositoryProvider);
  return repository.getCurrentUser();
}

// 複雑な状態管理
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
}
```

**ref.watch vs ref.read：**

```dart
// build 内では watch（再構築が必要）
final user = ref.watch(currentUserProvider);

// イベントハンドラ内では read
onPressed: () {
  ref.read(authNotifierProvider.notifier).signOut();
}
```

**チェックリスト：**

- [ ] 用途に応じたプロバイダーを選択
- [ ] `riverpod_generator` を使用
- [ ] build 内は `watch`、イベント内は `read`
- [ ] `@Riverpod(keepAlive: true)` で永続化

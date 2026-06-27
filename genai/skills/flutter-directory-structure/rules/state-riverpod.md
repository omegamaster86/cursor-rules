---
title: Riverpod State Management
impact: HIGH
impactDescription: Riverpod プロバイダーの配置と使用方法
tags: flutter, riverpod, state-management
---

## Riverpod State Management

Riverpod を使用した状態管理の実装パターンです。

**プロバイダーの配置：**

```
lib/
├── core/providers/              # グローバルプロバイダー
│   ├── providers.dart           # エクスポートファイル
│   ├── supabase_provider.dart   # Supabase クライアント
│   └── dio_provider.dart        # HTTP クライアント
└── features/[機能]/presentation/providers/  # 機能別プロバイダー
    ├── [機能]_provider.dart     # プロバイダー定義
    ├── [機能]_provider.g.dart   # 生成ファイル
    └── [機能]_notifier.dart     # Notifier クラス
```

**プロバイダーの種類：**

| 種別 | 用途 | 使用例 |
|------|------|--------|
| `Provider` | 変更されない値、DI | リポジトリ、サービス |
| `FutureProvider` | 非同期取得 | API からのデータ取得 |
| `StreamProvider` | ストリーム | リアルタイムデータ |
| `NotifierProvider` | 複雑な状態 | フォーム、ビジネスロジック |
| `AsyncNotifierProvider` | 非同期状態 | CRUD 操作 |

**riverpod_generator の使用：**

```dart
import 'package:riverpod_annotation/riverpod_annotation.dart';

part 'auth_provider.g.dart';

@riverpod
class AuthNotifier extends _$AuthNotifier {
  @override
  FutureOr<User?> build() async {
    final repository = ref.watch(authRepositoryProvider);
    return repository.getCurrentUser();
  }

  Future<void> login(String email, String password) async {
    state = const AsyncValue.loading();
    state = await AsyncValue.guard(() async {
      final repository = ref.read(authRepositoryProvider);
      return repository.login(email, password);
    });
  }
}
```

**ref.watch vs ref.read：**

```dart
@override
Widget build(BuildContext context, WidgetRef ref) {
  // ✅ build 内では watch（再構築が必要）
  final user = ref.watch(currentUserProvider);
  
  return ElevatedButton(
    onPressed: () {
      // ✅ イベントハンドラ内では read
      ref.read(authNotifierProvider.notifier).signOut();
    },
    child: Text('ログアウト'),
  );
}
```

**チェックリスト：**

- [ ] グローバルプロバイダーは `core/providers/` に配置
- [ ] 機能別プロバイダーは `features/[機能]/presentation/providers/` に配置
- [ ] `riverpod_generator` を使用
- [ ] build 内は `watch`、イベントハンドラ内は `read`

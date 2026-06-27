---
title: Supabase Flutter SDK
impact: HIGH
impactDescription: supabase_flutter の使用方法
tags: flutter, supabase, backend, sdk
---

## Supabase Flutter SDK

supabase_flutter を使用したバックエンド連携のパターンです。

**インストール：**

```yaml
dependencies:
  supabase_flutter: ^2.0.0
```

**初期化（main.dart）：**

```dart
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:supabase_flutter/supabase_flutter.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  
  await Supabase.initialize(
    url: const String.fromEnvironment('SUPABASE_URL'),
    anonKey: const String.fromEnvironment('SUPABASE_ANON_KEY'),
  );

  runApp(
    const ProviderScope(
      child: MyApp(),
    ),
  );
}
```

**Riverpod プロバイダー：**

```dart
// core/providers/supabase_provider.dart
import 'package:riverpod_annotation/riverpod_annotation.dart';
import 'package:supabase_flutter/supabase_flutter.dart';

part 'supabase_provider.g.dart';

@Riverpod(keepAlive: true)
SupabaseClient supabaseClient(SupabaseClientRef ref) {
  return Supabase.instance.client;
}

@riverpod
Stream<AuthState> authState(AuthStateRef ref) {
  final client = ref.watch(supabaseClientProvider);
  return client.auth.onAuthStateChange;
}
```

**Database Function 呼び出し：**

```dart
// Edge Function 経由ではなく、RPC で直接呼び出す場合
final response = await supabase.rpc('sel_user_by_id', params: {'p_user_id': userId});
```

**環境変数の設定：**

```bash
# 実行時に環境変数を渡す
flutter run --dart-define=SUPABASE_URL=https://xxx.supabase.co --dart-define=SUPABASE_ANON_KEY=xxx
```

**チェックリスト：**

- [ ] `main.dart` で `Supabase.initialize()` を呼び出す
- [ ] 環境変数は `--dart-define` で渡す
- [ ] `supabaseClient` プロバイダーは `keepAlive: true`
- [ ] 認証状態は `authState` プロバイダーで監視

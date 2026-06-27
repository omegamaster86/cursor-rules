---
title: Core Directory Structure
impact: HIGH
impactDescription: core/ ディレクトリの役割と構成
tags: flutter, directory, core
---

## Core Directory Structure

`core/` ディレクトリは、アプリケーション全体で共有される機能・コンポーネントを配置します。

**構成：**

```
lib/core/
├── constants/               # 定数
│   ├── app_constants.dart
│   └── api_constants.dart
├── errors/                  # エラーハンドリング
│   ├── exceptions.dart
│   └── failures.dart
├── network/                 # ネットワーク関連
│   └── network_info.dart
├── providers/               # グローバルプロバイダー（Riverpod）
│   ├── providers.dart       # エクスポートファイル
│   ├── supabase_provider.dart
│   └── dio_provider.dart
├── theme/                   # テーマ設定
│   ├── app_theme.dart
│   └── colors.dart
├── utils/                   # ユーティリティ
│   ├── validators.dart
│   └── formatters.dart
└── widgets/                 # 共通ウィジェット（複数機能で使用）
    ├── buttons/
    │   ├── primary_button.dart
    │   └── secondary_button.dart
    ├── inputs/
    │   └── custom_text_field.dart
    └── loading/
        └── loading_indicator.dart
```

**各ディレクトリの役割：**

| ディレクトリ | 役割 |
|-------------|------|
| `constants/` | アプリ全体で使用する定数、APIエンドポイント、設定値 |
| `errors/` | ネットワークエラー、サーバーエラー、ビジネスロジックのエラー表現 |
| `network/` | ネットワーク接続の確認、HTTPクライアントの設定 |
| `providers/` | グローバルプロバイダー（Supabaseクライアント、Dioなど） |
| `theme/` | カラーパレット、テキストスタイル、テーマ設定 |
| `utils/` | バリデーター、フォーマッターなどユーティリティ関数 |
| `widgets/` | 複数機能で共有される共通ウィジェット |

**グローバルプロバイダー例：**

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

**チェックリスト：**

- [ ] 複数機能で使用するコンポーネントは `core/` に配置
- [ ] グローバルプロバイダーは `core/providers/` に配置
- [ ] 共通ウィジェットは `core/widgets/` に配置
- [ ] エラーハンドリングは `core/errors/` で統一管理

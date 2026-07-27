---
title: supabase_flutter
impact: HIGH
impactDescription: Supabase クライアント初期化
tags: supabase, flutter
---

## supabase_flutter

**キー名:** `SUPABASE_PUBLISHABLE_KEY`（`SUPABASE_ANON_KEY` ではない）

```dart
// core/constants.dart
static const String supabasePublishableKey = String.fromEnvironment(
  'SUPABASE_PUBLISHABLE_KEY',
  defaultValue: '',
);
```

初期化は `SupabaseClientManager.initialize()`（`core/supabase_client.dart`）。main で直 `Supabase.initialize` してもよいが、starter は Manager 経由。

env ファイル運用は `mobile-env` instruction（`env.local.json` + `--dart-define-from-file`）を参照。

参考版: `supabase_flutter: ^2.8.2`

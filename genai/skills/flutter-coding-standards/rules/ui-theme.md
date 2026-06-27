---
title: Theme Configuration
impact: MEDIUM
impactDescription: アプリケーションテーマの設定
tags: flutter, theme, ui
---

## Theme Configuration

`lib/core/theme/` にアプリケーション全体のテーマを定義します。

**テーマ設定（app_theme.dart）：**

```dart
// lib/core/theme/app_theme.dart
import 'package:flutter/material.dart';
import 'colors.dart';

class AppTheme {
  // ライトテーマ
  static ThemeData get lightTheme {
    return ThemeData(
      useMaterial3: true,
      colorScheme: ColorScheme.fromSeed(
        seedColor: AppColors.primary,
        brightness: Brightness.light,
      ),
      appBarTheme: const AppBarTheme(
        centerTitle: true,
        elevation: 0,
      ),
      elevatedButtonTheme: ElevatedButtonThemeData(
        style: ElevatedButton.styleFrom(
          padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 12),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(8),
          ),
        ),
      ),
      inputDecorationTheme: InputDecorationTheme(
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(8),
        ),
        contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
      ),
    );
  }

  // ダークテーマ
  static ThemeData get darkTheme {
    return ThemeData(
      useMaterial3: true,
      colorScheme: ColorScheme.fromSeed(
        seedColor: AppColors.primary,
        brightness: Brightness.dark,
      ),
      // ... その他の設定
    );
  }
}
```

**カラー定義（colors.dart）：**

```dart
// lib/core/theme/colors.dart
import 'package:flutter/material.dart';

class AppColors {
  // プライマリカラー
  static const Color primary = Color(0xFF2196F3);
  static const Color primaryLight = Color(0xFF64B5F6);
  static const Color primaryDark = Color(0xFF1976D2);

  // セマンティックカラー
  static const Color success = Color(0xFF4CAF50);
  static const Color warning = Color(0xFFFFC107);
  static const Color error = Color(0xFFF44336);
  static const Color info = Color(0xFF2196F3);

  // グレースケール
  static const Color grey100 = Color(0xFFF5F5F5);
  static const Color grey300 = Color(0xFFE0E0E0);
  static const Color grey500 = Color(0xFF9E9E9E);
  static const Color grey700 = Color(0xFF616161);
  static const Color grey900 = Color(0xFF212121);
}
```

**テーマの使用方法：**

```dart
// ✅ 良い例：テーマから値を取得
Widget build(BuildContext context) {
  final theme = Theme.of(context);
  final colorScheme = theme.colorScheme;

  return Container(
    color: colorScheme.primary,
    child: Text(
      'Hello',
      style: theme.textTheme.titleLarge,
    ),
  );
}

// ❌ 悪い例：ハードコーディング
Widget build(BuildContext context) {
  return Container(
    color: Colors.blue, // ハードコーディング
    child: Text(
      'Hello',
      style: TextStyle(fontSize: 20), // ハードコーディング
    ),
  );
}
```

**チェックリスト：**

- [ ] `Theme.of(context)` を使用してテーマ値にアクセス
- [ ] 色は `AppColors` または `colorScheme` から取得
- [ ] フォントスタイルは `theme.textTheme` から取得
- [ ] ハードコーディングを避ける

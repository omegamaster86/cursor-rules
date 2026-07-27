---
title: UI Theme
impact: MEDIUM
impactDescription: テーマ設定
tags: ui, theme, flutter
---

## UI Theme

starter では `app.dart` で `ThemeData(colorScheme: ColorScheme.fromSeed(...))` を直書きしてよい。

`lib/core/theme/app_theme.dart` / `AppColors` への抽出は規模に応じたガイドライン（必須ではない）。

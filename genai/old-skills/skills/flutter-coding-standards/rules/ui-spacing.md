---
title: Spacing Constants
impact: LOW
impactDescription: 間隔（Spacing）の定義と使用
tags: flutter, spacing, ui, constants
---

## Spacing Constants

一貫した間隔を使用するため、定数を定義します。

**Spacing の定義：**

```dart
// lib/core/constants/app_constants.dart
class AppSpacing {
  static const double xs = 4.0;
  static const double sm = 8.0;
  static const double md = 16.0;
  static const double lg = 24.0;
  static const double xl = 32.0;
  static const double xxl = 48.0;
}
```

**使用例：**

```dart
// ✅ 良い例：定数を使用
Padding(
  padding: const EdgeInsets.all(AppSpacing.md),
  child: Column(
    children: [
      const Text('Title'),
      const SizedBox(height: AppSpacing.sm),
      const Text('Description'),
    ],
  ),
)

// ❌ 悪い例：マジックナンバー
Padding(
  padding: const EdgeInsets.all(16), // マジックナンバー
  child: Column(
    children: [
      const Text('Title'),
      const SizedBox(height: 8), // マジックナンバー
      const Text('Description'),
    ],
  ),
)
```

**SizedBox ヘルパー（オプション）：**

```dart
// lib/core/constants/app_constants.dart
class AppGap {
  static const SizedBox xs = SizedBox(height: AppSpacing.xs, width: AppSpacing.xs);
  static const SizedBox sm = SizedBox(height: AppSpacing.sm, width: AppSpacing.sm);
  static const SizedBox md = SizedBox(height: AppSpacing.md, width: AppSpacing.md);
  static const SizedBox lg = SizedBox(height: AppSpacing.lg, width: AppSpacing.lg);
  
  // 垂直方向のみ
  static const SizedBox vXs = SizedBox(height: AppSpacing.xs);
  static const SizedBox vSm = SizedBox(height: AppSpacing.sm);
  static const SizedBox vMd = SizedBox(height: AppSpacing.md);
  static const SizedBox vLg = SizedBox(height: AppSpacing.lg);
  
  // 水平方向のみ
  static const SizedBox hXs = SizedBox(width: AppSpacing.xs);
  static const SizedBox hSm = SizedBox(width: AppSpacing.sm);
  static const SizedBox hMd = SizedBox(width: AppSpacing.md);
  static const SizedBox hLg = SizedBox(width: AppSpacing.lg);
}

// 使用例
Column(
  children: [
    const Text('Title'),
    AppGap.vSm,
    const Text('Description'),
  ],
)
```

**Spacing の目安：**

| サイズ | 値 | 用途 |
|--------|-----|------|
| xs | 4.0 | アイコンとテキストの間 |
| sm | 8.0 | 小さな要素間 |
| md | 16.0 | 標準的な要素間、パディング |
| lg | 24.0 | セクション間 |
| xl | 32.0 | 大きなセクション間 |
| xxl | 48.0 | ページレベルの余白 |

**チェックリスト：**

- [ ] マジックナンバーを使用していない
- [ ] `AppSpacing` 定数を使用している
- [ ] 一貫した間隔を維持している

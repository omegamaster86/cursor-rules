---
title: Intl for Internationalization
impact: MEDIUM
impactDescription: intl による国際化と日付フォーマット
tags: flutter, intl, i18n, date-format
---

## Intl for Internationalization

intl を使用した国際化と日付フォーマットのパターンです。

**インストール：**

```yaml
dependencies:
  intl: ^0.19.0
```

**日付フォーマット：**

```dart
import 'package:intl/intl.dart';

// 基本的なフォーマット
final now = DateTime.now();

// 日付のみ
DateFormat('yyyy/MM/dd').format(now);  // 2024/01/15
DateFormat('yyyy年MM月dd日').format(now);  // 2024年01月15日

// 日時
DateFormat('yyyy/MM/dd HH:mm').format(now);  // 2024/01/15 14:30
DateFormat('yyyy年MM月dd日 HH時mm分').format(now);  // 2024年01月15日 14時30分

// ロケール指定
DateFormat.yMMMd('ja').format(now);  // 2024年1月15日
DateFormat.yMMMEd('ja').format(now);  // 2024年1月15日(月)
```

**数値フォーマット：**

```dart
import 'package:intl/intl.dart';

// 通貨
NumberFormat.currency(locale: 'ja', symbol: '¥').format(1234567);
// ¥1,234,567

// パーセント
NumberFormat.percentPattern('ja').format(0.75);
// 75%

// カンマ区切り
NumberFormat('#,###').format(1234567);
// 1,234,567
```

**ユーティリティクラス：**

```dart
// core/utils/formatters.dart
import 'package:intl/intl.dart';

class AppFormatters {
  // 日付フォーマット
  static String formatDate(DateTime date) {
    return DateFormat('yyyy/MM/dd').format(date);
  }

  static String formatDateTime(DateTime date) {
    return DateFormat('yyyy/MM/dd HH:mm').format(date);
  }

  static String formatRelativeTime(DateTime date) {
    final now = DateTime.now();
    final diff = now.difference(date);

    if (diff.inDays > 0) {
      return '${diff.inDays}日前';
    } else if (diff.inHours > 0) {
      return '${diff.inHours}時間前';
    } else if (diff.inMinutes > 0) {
      return '${diff.inMinutes}分前';
    } else {
      return 'たった今';
    }
  }

  // 通貨フォーマット
  static String formatCurrency(int amount) {
    return NumberFormat.currency(locale: 'ja', symbol: '¥', decimalDigits: 0)
        .format(amount);
  }
}
```

**使用例：**

```dart
Text(AppFormatters.formatDate(product.createdAt));
Text(AppFormatters.formatCurrency(product.price));
Text(AppFormatters.formatRelativeTime(notification.createdAt));
```

**チェックリスト：**

- [ ] 日付フォーマットは `DateFormat` を使用
- [ ] 数値フォーマットは `NumberFormat` を使用
- [ ] よく使うフォーマットはユーティリティクラスに集約
- [ ] ロケールを明示的に指定（`'ja'`）

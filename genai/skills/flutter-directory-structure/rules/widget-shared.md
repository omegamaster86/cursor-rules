---
title: Shared Widgets
impact: MEDIUM
impactDescription: 共通ウィジェットの配置
tags: flutter, widget, shared, core
---

## Shared Widgets

複数の場所で使用される共通ウィジェットの配置方法です。

**配置場所の種類：**

| 配置場所 | スコープ | 用途 |
|----------|----------|------|
| `features/[機能]/presentation/widgets/` | 機能内 | 同一機能内の複数画面で共有 |
| `core/widgets/` | アプリ全体 | 複数機能で共有するデザインシステム |

**機能内共有ウィジェット：**

```
features/auth/presentation/widgets/
└── auth_text_field.dart    # auth機能専用のテキストフィールド
```

```dart
// features/auth/presentation/widgets/auth_text_field.dart
class AuthTextField extends StatelessWidget {
  final String label;
  final TextEditingController controller;
  final bool obscureText;

  const AuthTextField({
    required this.label,
    required this.controller,
    this.obscureText = false,
  });

  @override
  Widget build(BuildContext context) {
    return TextField(
      controller: controller,
      obscureText: obscureText,
      decoration: InputDecoration(
        labelText: label,
        // auth機能固有のスタイル
      ),
    );
  }
}
```

**全体共有ウィジェット：**

```
core/widgets/
├── buttons/
│   ├── primary_button.dart
│   └── secondary_button.dart
├── inputs/
│   └── custom_text_field.dart
├── loading/
│   └── loading_indicator.dart
└── dialogs/
    └── confirm_dialog.dart
```

```dart
// core/widgets/buttons/primary_button.dart
class PrimaryButton extends StatelessWidget {
  final String text;
  final VoidCallback? onPressed;
  final bool isLoading;

  const PrimaryButton({
    required this.text,
    this.onPressed,
    this.isLoading = false,
  });

  @override
  Widget build(BuildContext context) {
    return ElevatedButton(
      onPressed: isLoading ? null : onPressed,
      child: isLoading
        ? const CircularProgressIndicator()
        : Text(text),
    );
  }
}
```

**共通化の判断基準：**

| 条件 | 判断 |
|------|------|
| 2つ以上の機能で使用 | `core/widgets/` に配置 |
| デザインシステムの一部 | `core/widgets/` に配置 |
| 1つの機能内でのみ使用 | `features/[機能]/presentation/widgets/` に配置 |

**チェックリスト：**

- [ ] 複数機能で使う共通ウィジェットは `core/widgets/` に配置
- [ ] 機能内で複数画面で使うウィジェットは `features/[機能]/presentation/widgets/` に配置
- [ ] `core/widgets/` は用途別にサブディレクトリで整理（buttons, inputs, loading など）
- [ ] 共通ウィジェットはアプリ全体で統一されたデザインを維持

---
title: Common Widgets
impact: MEDIUM
impactDescription: 共通ウィジェットの実装規約
tags: flutter, widgets, ui
---

## Common Widgets

`lib/core/widgets/` に共通ウィジェットを配置します。

**PrimaryButton の例：**

```dart
// lib/core/widgets/buttons/primary_button.dart
import 'package:flutter/material.dart';

class PrimaryButton extends StatelessWidget {
  final String text;
  final VoidCallback? onPressed;
  final bool isLoading;
  final bool isDisabled;
  final double? width;

  const PrimaryButton({
    super.key,
    required this.text,
    this.onPressed,
    this.isLoading = false,
    this.isDisabled = false,
    this.width,
  });

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      width: width,
      child: ElevatedButton(
        onPressed: isLoading || isDisabled ? null : onPressed,
        child: isLoading
            ? const SizedBox(
                height: 20,
                width: 20,
                child: CircularProgressIndicator(strokeWidth: 2),
              )
            : Text(text),
      ),
    );
  }
}
```

**共通ウィジェットのディレクトリ構成：**

```
lib/core/widgets/
├── buttons/
│   ├── primary_button.dart
│   └── secondary_button.dart
├── cards/
│   └── info_card.dart
├── dialogs/
│   └── confirm_dialog.dart
├── forms/
│   └── custom_text_field.dart
└── loading/
    └── loading_indicator.dart
```

**ウィジェット設計のルール：**

| ルール | 説明 |
|--------|------|
| const コンストラクタ | 可能な限り `const` を使用 |
| required パラメータ | 必須のパラメータは `required` を付ける |
| デフォルト値 | オプションには適切なデフォルト値を設定 |
| super.key | キーを受け取れるようにする |

**使用例：**

```dart
// 使用側
PrimaryButton(
  text: 'ログイン',
  isLoading: authState.isLoading,
  onPressed: _handleLogin,
)
```

**チェックリスト：**

- [ ] 共通ウィジェットは `lib/core/widgets/` に配置
- [ ] `const` コンストラクタを使用
- [ ] `super.key` を受け取る
- [ ] ローディング状態を考慮
- [ ] 適切なデフォルト値を設定

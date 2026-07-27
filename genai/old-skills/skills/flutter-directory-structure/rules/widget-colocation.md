---
title: Widget Colocation
impact: MEDIUM
impactDescription: ウィジェット配置のコロケーション原則
tags: flutter, widget, colocation
---

## Widget Colocation

コロケーション原則に基づいたウィジェットの配置方法です。

**基本原則：**

ウィジェットは「使用する場所の近く」に配置します。

**配置の優先順位：**

1. **画面固有** → `features/[機能]/presentation/screens/[画面]/widgets/`
2. **機能内共有** → `features/[機能]/presentation/widgets/`
3. **全体共有** → `core/widgets/`

**画面固有のウィジェット：**

```
features/auth/presentation/screens/
├── login_screen.dart
│   └── widgets/              # login画面でのみ使用
│       ├── login_form.dart
│       └── social_login_buttons.dart
└── register_screen.dart
    └── widgets/              # register画面でのみ使用
        ├── register_form.dart
        └── terms_checkbox.dart
```

**配置例：**

```dart
// features/auth/presentation/screens/login_screen.dart
import 'widgets/login_form.dart';
import 'widgets/social_login_buttons.dart';

class LoginScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Column(
        children: [
          LoginForm(),           // 同じディレクトリの widgets/ から
          SocialLoginButtons(),  // 同じディレクトリの widgets/ から
        ],
      ),
    );
  }
}
```

**昇格のタイミング：**

ウィジェットを上位に移動するタイミング：

| 状況 | 移動先 |
|------|--------|
| 同じ機能内の別の画面で使う | `features/[機能]/presentation/widgets/` |
| 別の機能で使う | `core/widgets/` |

**チェックリスト：**

- [ ] その画面でのみ使うウィジェットは `screens/[画面]/widgets/` に配置
- [ ] 複数画面で使う前に、まず画面固有として作成
- [ ] 昇格が必要になったときにのみ上位に移動
- [ ] ウィジェットは使用場所の近くに配置

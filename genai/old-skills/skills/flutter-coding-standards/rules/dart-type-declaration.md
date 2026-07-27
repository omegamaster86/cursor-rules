---
title: Dart Type Declaration
impact: HIGH
impactDescription: 明示的な型宣言のルール
tags: dart, types, declaration
---

## Dart Type Declaration

Dart を使用する際の型宣言に関するルールです。

**基本方針：**

- 型推論に頼らず、**明示的に型を宣言する**
- 特に関数の引数、戻り値、クラスのフィールドは必ず型を明記
- `dynamic` の使用は極力避ける

**良い例：**

```dart
// ✅ 明示的な型宣言
String userName = "太郎";
int totalPrice = 10000;
bool isLoggedIn = true;
List<User> userList = [];
Map<String, dynamic> jsonData = {};

// 関数の戻り値と引数に型を明記
Future<User> fetchUser(String userId) async {
  // ...
}
```

**悪い例：**

```dart
// ❌ 型推論に頼る（可読性が低下）
var userName = "太郎";
var userList = [];

// ❌ 型が不明確
dynamic data = fetchData();
```

**型定義の配置場所：**

| 種類 | 配置場所 |
|------|----------|
| Entity（ドメイン層） | `features/[機能]/domain/entities/` |
| Model（データ層） | `features/[機能]/data/models/` |
| 共通型 | `lib/core/types/` |

**画面固有の型：**

そのファイルでのみ使用する型は、同じファイル内に定義します。

```dart
// features/dashboard/presentation/screens/dashboard_screen.dart
class DashboardStats {
  final int totalUsers;
  final int activeUsers;

  const DashboardStats({
    required this.totalUsers,
    required this.activeUsers,
  });
}
```

**チェックリスト：**

- [ ] 変数に明示的な型を宣言している
- [ ] 関数の引数と戻り値に型を明記している
- [ ] `dynamic` を使用していない
- [ ] 型定義を適切な場所に配置している

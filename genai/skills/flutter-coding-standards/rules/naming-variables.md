---
title: Variable Naming
impact: MEDIUM
impactDescription: 変数・関数の命名規則
tags: dart, naming, variables, functions
---

## Variable Naming

変数・関数の命名規則です。

**変数名（camelCase）：**

```dart
// ✅ 良い例
String userName = "太郎";
int totalPrice = 10000;
bool isLoggedIn = true;
List<User> userList = [];

// ❌ 悪い例
String un = "太郎"; // 略語
int TotalPrice = 10000; // PascalCase
bool is_logged_in = true; // snake_case
var data = []; // 意味が不明確
```

**定数（camelCase）：**

```dart
// ✅ Dart の慣例に従う
const int maxRetryCount = 3;
const String apiBaseUrl = "https://api.example.com";
const Duration defaultTimeout = Duration(seconds: 30);

// クラス内の定数
class ApiConstants {
  static const String baseUrl = 'https://api.example.com';
  static const int timeout = 30;
}
```

**真偽値（Boolean）：**

```dart
// ✅ 良い例：接頭辞を使用
bool isLoggedIn = true;
bool hasPermission = false;
bool shouldShowModal = true;
bool canEdit = false;

// ❌ 悪い例
bool loggedIn = true; // 接頭辞なし
bool notLoggedIn = false; // 否定形
bool permission = false; // 真偽値であることが不明確
```

**関数名（camelCase + 動詞）：**

```dart
// ✅ 良い例
void fetchUserData() { /* ... */ }
int calculateTotalPrice() { /* ... */ }
bool validateEmail(String email) { /* ... */ }
Future<User> createUser(UserInput data) async { /* ... */ }

// ❌ 悪い例
void user() { /* ... */ } // 動詞がない
void FetchUserData() { /* ... */ } // PascalCase
void get() { /* ... */ } // 何を取得するか不明確
```

**非同期関数の命名：**

```dart
// ✅ 取得系は fetch, load, get
Future<User> fetchUser(String id) async { /* ... */ }
Future<List<Product>> loadProducts() async { /* ... */ }

// ✅ 保存系は save, create, update, delete
Future<void> saveUserProfile(UserProfile profile) async { /* ... */ }
Future<void> createOrder(OrderInput input) async { /* ... */ }
```

**命名の目安：**

| 接頭辞 | 用途 | 例 |
|--------|------|-----|
| `is` | 状態を表す真偽値 | `isLoading`, `isActive` |
| `has` | 所有を表す真偽値 | `hasError`, `hasPermission` |
| `should` | 条件を表す真偽値 | `shouldRefresh` |
| `can` | 能力を表す真偽値 | `canEdit`, `canDelete` |
| `fetch` | APIからの取得 | `fetchUser` |
| `load` | データの読み込み | `loadProducts` |
| `save` | データの保存 | `saveProfile` |
| `create` | 新規作成 | `createUser` |
| `update` | 更新 | `updateOrder` |
| `delete` | 削除 | `deleteItem` |

**チェックリスト：**

- [ ] 変数名は camelCase
- [ ] 意味のある名前（略語を避ける）
- [ ] 真偽値は `is`, `has`, `should`, `can` などの接頭辞
- [ ] 関数名は動詞で始まる

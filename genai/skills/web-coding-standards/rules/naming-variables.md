---
title: Variable Naming Convention
impact: MEDIUM
impactDescription: 変数・関数の命名規則
tags: typescript, naming, conventions, variables
---

## Variable Naming Convention

変数と関数の命名規則です。

### 変数名（camelCase）

```typescript
// ✅ 良い例
const userName = "太郎";
const totalPrice = 10000;
const isLoggedIn = true;
const userList = [];

// ❌ 悪い例
const un = "太郎"; // 略語
const TotalPrice = 10000; // PascalCase
const is_logged_in = true; // snake_case
const data = []; // 意味が不明確
```

### 定数（UPPER_SNAKE_CASE）

グローバル定数、設定値は `UPPER_SNAKE_CASE` を使用します。

```typescript
// ✅ 良い例
const MAX_RETRY_COUNT = 3;
const API_BASE_URL = "https://api.example.com";
const DEFAULT_PAGE_SIZE = 20;

// ❌ 悪い例
const maxRetryCount = 3; // camelCase
const apiBaseUrl = "https://api.example.com";
```

### 真偽値（Boolean）の命名

`is`, `has`, `should`, `can` などの接頭辞を使用します。

```typescript
// ✅ 良い例
const isLoggedIn = true;
const hasPermission = false;
const shouldShowModal = true;
const canEdit = false;

// ❌ 悪い例
const loggedIn = true; // 接頭辞なし
const notLoggedIn = false; // 否定形
const permission = false; // 真偽値であることが不明確
```

### 関数名（camelCase）

動詞または動詞句で命名します。

```typescript
// ✅ 良い例
function fetchUserData() { /* ... */ }
function calculateTotalPrice() { /* ... */ }
function validateEmail(email: string) { /* ... */ }
async function createUser(data: UserInsert) { /* ... */ }

// ❌ 悪い例
function user() { /* ... */ } // 動詞がない
function FetchUserData() { /* ... */ } // PascalCase
function get() { /* ... */ } // 何を取得するか不明確
```

### イベントハンドラの命名

`handle` + イベント名の形式を使用します。

```typescript
// ✅ 良い例
function handleClick() { /* ... */ }
function handleSubmit() { /* ... */ }
function handleChange() { /* ... */ }
function handleUserDelete() { /* ... */ }

// ❌ 悪い例
function onClick() { /* ... */ } // handleを使う
function submit() { /* ... */ } // handleを付ける
function doSomething() { /* ... */ } // 何をするか不明確
```

### 一般的なルール

| ルール | 説明 |
|-------|------|
| 意味のある名前 | コードを読んだだけで何をしているかわかる |
| 略語は避ける | `usr` → `user`、`btn` → `button` |
| 一貫性を保つ | プロジェクト全体で同じ命名パターン |
| 長すぎる名前は避ける | 目安: 2〜4単語 |

```typescript
// ✅ 良い例：一貫性のある命名
function fetchUserData() { /* ... */ }
function fetchProductData() { /* ... */ }
function fetchOrderData() { /* ... */ }

// ❌ 悪い例：一貫性がない
function getUserData() { /* ... */ }
function loadProductData() { /* ... */ }
function retrieveOrderData() { /* ... */ }
```

**チェックリスト：**

- [ ] 変数は camelCase
- [ ] 定数は UPPER_SNAKE_CASE
- [ ] 真偽値は is/has/should/can で始める
- [ ] 関数は動詞で始める
- [ ] イベントハンドラは handle で始める

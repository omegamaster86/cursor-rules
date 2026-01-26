## 6. 命名規約

コードの可読性と保守性を高めるための命名規則を定義します。

### 6.1 変数名の命名規則

#### 6.1.1 通常の変数（camelCase）

- 基本的に `camelCase` を使用する
- 名詞または名詞句で命名する
- 意味のある名前を付ける（略語は避ける）

```typescript
// ✅ 良い例
const userName = "太郎";
const totalPrice = 10000;
const isLoggedIn = true;
const userList = [];

// ❌ 悪い例
const un = "太郎"; // 略語
const TotalPrice = 10000; // PascalCase（変数には使わない）
const is_logged_in = true; // snake_case（TypeScriptでは使わない）
const data = []; // 意味が不明確
```

#### 6.1.2 定数（UPPER_SNAKE_CASE）

- グローバル定数、設定値は `UPPER_SNAKE_CASE` を使用する
- アプリケーション全体で共有する値に使用

```typescript
// ✅ 良い例
const MAX_RETRY_COUNT = 3;
const API_BASE_URL = "https://api.example.com";
const DEFAULT_PAGE_SIZE = 20;

// ❌ 悪い例
const maxRetryCount = 3; // camelCase（定数には使わない）
const apiBaseUrl = "https://api.example.com"; // camelCase
```

#### 6.1.3 真偽値（Boolean）の命名

- `is`, `has`, `should`, `can` などの接頭辞を使用する
- 肯定形で命名する（否定形は避ける）

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

### 6.2 関数・メソッドの命名規則

#### 6.2.1 関数名（camelCase）

- `camelCase` を使用する
- 動詞または動詞句で命名する
- 何をする関数かが明確にわかる名前にする

```typescript
// ✅ 良い例
function fetchUserData() { /* ... */ }
function calculateTotalPrice() { /* ... */ }
function validateEmail(email: string) { /* ... */ }
async function createUser(data: UserInsert) { /* ... */ }

// ❌ 悪い例
function user() { /* ... */ } // 動詞がない
function FetchUserData() { /* ... */ } // PascalCase（関数には使わない）
function get() { /* ... */ } // 何を取得するか不明確
```

#### 6.2.2 イベントハンドラの命名

- `handle` + イベント名の形式を使用する
- イベントの種類が明確にわかる名前にする

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

### 6.3 コンポーネントの命名規則

#### 6.3.1 Reactコンポーネント（PascalCase）

- `PascalCase` を使用する
- 名詞で命名する
- 単一責任の原則に従い、コンポーネントの役割が明確にわかる名前にする

```typescript
// ✅ 良い例
export function UserProfile() { /* ... */ }
export function LoginForm() { /* ... */ }
export function HeaderNavigation() { /* ... */ }
export function ProductCard() { /* ... */ }

// ❌ 悪い例
export function userProfile() { /* ... */ } // camelCase（コンポーネントには使わない）
export function User() { /* ... */ } // 役割が不明確
export function Component1() { /* ... */ } // 意味のない名前
```

#### 6.3.2 カスタムフックの命名

- `use` + 機能名の形式を使用する
- `camelCase` で記述する

```typescript
// ✅ 良い例
function useAuth() { /* ... */ }
function useUserData() { /* ... */ }
function useLocalStorage(key: string) { /* ... */ }

// ❌ 悪い例
function auth() { /* ... */ } // useを付ける
function UseAuth() { /* ... */ } // PascalCase（フックには使わない）
function getUserData() { /* ... */ } // useで始める
```

### 6.4 ファイル名の命名規則

#### 6.4.1 コンポーネントファイル（PascalCase.tsx）

- コンポーネント名と同じ `PascalCase` を使用する
- 拡張子は `.tsx` を使用

```
// ✅ 良い例
UserProfile.tsx
LoginForm.tsx
HeaderNavigation.tsx

// ❌ 悪い例
userProfile.tsx // camelCase（コンポーネントファイルには使わない）
user-profile.tsx // kebab-case
user_profile.tsx // snake_case
```

#### 6.4.2 ユーティリティ・ヘルパーファイル（camelCase.ts）

- `camelCase` を使用する
- 機能が明確にわかる名前にする

```
// ✅ 良い例
formatDate.ts
validateEmail.ts
apiClient.ts
utils.ts

// ❌ 悪い例
FormatDate.ts // PascalCase（ユーティリティには使わない）
format-date.ts // kebab-case
format_date.ts // snake_case
```

#### 6.4.3 Next.js特有のファイル

- Next.js の規約に従う
- `page.tsx`, `layout.tsx`, `route.ts` などは固定名を使用

```
// ✅ Next.jsの規約に従ったファイル名
page.tsx          // ページコンポーネント
layout.tsx        // レイアウトコンポーネント
loading.tsx       // ローディング画面
error.tsx         // エラー画面
route.ts          // API Route
```

### 6.5 型・インターフェースの命名規則

#### 6.5.1 型定義（PascalCase）

- `PascalCase` を使用する
- `type` キーワードを使用（基本方針）

```typescript
// ✅ 良い例
type User = {
  id: string;
  name: string;
};

type ApiResponse<T> = {
  data: T;
  message: string;
};

// ❌ 悪い例
type user = { /* ... */ }; // camelCase
type user_type = { /* ... */ }; // snake_case
```

#### 6.5.2 Props型の命名

- コンポーネント名 + `Props` の形式を使用する

```typescript
// ✅ 良い例
type UserProfileProps = {
  userId: string;
  showAvatar?: boolean;
};

export function UserProfile({ userId, showAvatar }: UserProfileProps) {
  // ...
}

// ❌ 悪い例
type Props = { /* ... */ }; // 汎用的すぎる
type UserProfileProperties = { /* ... */ }; // 冗長
```

### 6.6 ディレクトリの命名規則

#### 6.6.1 基本的なディレクトリ（kebab-case）

- `kebab-case` を使用する（Next.js App Routerの規約）
- 複数形を使用する（コレクションを表す場合）

```
// ✅ 良い例
components/
hooks/
lib/
types/
app/user-profile/
app/admin-dashboard/

// ❌ 悪い例
Components/ // PascalCase
user_profile/ // snake_case（Next.jsでは推奨されない）
userProfile/ // camelCase
```

#### 6.6.2 動的ルートのディレクトリ

- Next.js の規約に従う
- `[id]`, `[slug]` などの形式を使用

```
// ✅ Next.jsの規約に従ったディレクトリ名
app/posts/[id]/
app/users/[userId]/
app/products/[slug]/
```

### 6.7 命名のベストプラクティス

#### 6.7.1 一般的なルール

- **意味のある名前を付ける**: コードを読んだだけで何をしているかわかるようにする
- **略語は避ける**: `usr` ではなく `user`、`btn` ではなく `button`
- **一貫性を保つ**: プロジェクト全体で同じ命名パターンを使用する
- **長すぎる名前は避ける**: 適度な長さに抑える（目安: 2〜4単語）

#### 6.7.2 良い例と悪い例

```typescript
// ✅ 良い例：意味が明確
const activeUsers = users.filter(user => user.isActive);
const totalPrice = items.reduce((sum, item) => sum + item.price, 0);

// ❌ 悪い例：意味が不明確
const au = users.filter(user => user.isActive);
const tp = items.reduce((sum, item) => sum + item.price, 0);
```

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

---

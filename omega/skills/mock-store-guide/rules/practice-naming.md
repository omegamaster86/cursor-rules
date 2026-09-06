---
title: Store Key Naming Conventions
impact: MEDIUM
impactDescription: ストアキーの命名規則
tags: mock-store, naming, convention
---

## Store Key Naming Conventions

ストアキーの命名規則です。

**基本ルール：**

名前空間を使用してストアキーを定義します。

```typescript
// 形式: {namespace}:{entity}
createMockStore("demo:todos", initialData);
createMockStore("demo:users", initialData);
createMockStore("test:fixtures", initialData);
```

**名前空間の種類：**

| 名前空間 | 用途 |
|---------|------|
| `demo:` | デモアプリケーション用 |
| `test:` | テスト用フィクスチャ |
| `dev:` | 開発時の一時データ |

**良い例：**

```typescript
// ✅ Good: 名前空間を使用
createMockStore("demo:todos", initialData);
createMockStore("demo:users", initialData);
createMockStore("demo:products", initialData);

// ✅ Good: 複数単語はキャメルケース
createMockStore("demo:orderItems", initialData);
createMockStore("demo:userProfiles", initialData);

// ✅ Good: テスト用は別の名前空間
createMockStore("test:todos", testFixtures);
```

**悪い例：**

```typescript
// ❌ Bad: 名前空間なし（衝突の可能性）
createMockStore("todos", initialData);
createMockStore("users", initialData);

// ❌ Bad: スネークケース（統一性のため避ける）
createMockStore("demo:order_items", initialData);

// ❌ Bad: 冗長なプレフィックス
createMockStore("demo:demo_todos", initialData);
createMockStore("mock:mock_users", initialData);
```

**関連するエンティティのグループ化：**

```typescript
// 同じドメインのエンティティは同じ名前空間
createMockStore("demo:orders", orderData);
createMockStore("demo:orderItems", orderItemData);
createMockStore("demo:orderHistory", historyData);

// 別のドメインは分ける
createMockStore("demo:users", userData);
createMockStore("demo:userSettings", settingsData);
```

**デバッグ用 API：**

```typescript
import { getMockStoreKeys, clearAllMockStores } from "@/services/mock-store";

// すべてのストアキーを取得
const keys = getMockStoreKeys();
// => ["demo:todos", "demo:users", "demo:products"]

// すべてのストアをクリア（デバッグ用）
clearAllMockStores();
```

**チェックリスト：**

- [ ] ストアキーに名前空間を使用
- [ ] 複数単語はキャメルケース
- [ ] 関連エンティティは同じ名前空間でグループ化
- [ ] テスト用は `test:` 名前空間を使用

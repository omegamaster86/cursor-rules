---
title: Custom Hooks Rules
impact: MEDIUM
impactDescription: カスタムフック作成のルール
tags: react, hooks, custom-hooks
---

## Custom Hooks Rules

カスタムフックの作成ルールです。

**命名規則：**

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

**ファイル配置：**

```
src/
  hooks/
    useAuth.ts
    useUserData.ts
    useLocalStorage.ts
```

**カスタムフックの実装例：**

```typescript
// hooks/useAuth.ts
import { useState, useEffect } from "react";
import { createClient } from "@/services/supabase/client";
import type { User } from "@supabase/supabase-js";

export function useAuth() {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  // Supabase Auth の状態変更を監視
  useEffect(() => {
    const supabase = createClient();

    // 初期状態を取得
    supabase.auth.getSession().then(({ data: { session } }) => {
      setUser(session?.user ?? null);
      setLoading(false);
    });

    // 状態変更を監視
    const { data: { subscription } } = supabase.auth.onAuthStateChange(
      (_event, session) => {
        setUser(session?.user ?? null);
      }
    );

    return () => subscription.unsubscribe();
  }, []);

  return { user, loading };
}
```

```typescript
// hooks/useLocalStorage.ts
import { useState, useEffect } from "react";

export function useLocalStorage<T>(key: string, initialValue: T) {
  const [storedValue, setStoredValue] = useState<T>(() => {
    if (typeof window === "undefined") {
      return initialValue;
    }
    try {
      const item = window.localStorage.getItem(key);
      return item ? JSON.parse(item) : initialValue;
    } catch (error) {
      console.error(error);
      return initialValue;
    }
  });

  // localStorage への同期
  useEffect(() => {
    if (typeof window !== "undefined") {
      window.localStorage.setItem(key, JSON.stringify(storedValue));
    }
  }, [key, storedValue]);

  return [storedValue, setStoredValue] as const;
}
```

**カスタムフック作成の判断基準：**

| 作成すべき場合 | 作成不要な場合 |
|--------------|--------------|
| 複数コンポーネントで再利用するロジック | 1つのコンポーネントでのみ使用 |
| 複雑な状態管理ロジック | シンプルな useState のみ |
| 外部サービスとの連携 | 単純なイベントハンドラ |

**チェックリスト：**

- [ ] `use` で始まる命名
- [ ] `hooks/` ディレクトリに配置
- [ ] 再利用可能なロジックを抽出
- [ ] 依存関係を正しく設定

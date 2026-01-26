# Supabase 実装ガイド（分割）: Edge Functions

## 2. Edge Functions

### 2.1 ひな形ファイル

`[project]/supabase/functions/` 配下に作成します。

```typescript
import "jsr:@supabase/functions-js/edge-runtime.d.ts";
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";
import type { Database } from "../_shared/database.types.ts";

// FIXME: Database Function の戻り値の型を定義
type ResponseData = Database["public"]["Functions"]["XXXXXX"]["Returns"][0];

const supabase = createClient(
  Deno.env.get("SUPABASE_URL"),
  Deno.env.get("SUPABASE_ANON_KEY")
);

Deno.serve(async (req) => {
  // FIXME: XXXXXX（実際のDatabase Function名に置き換える）
  const { data, error } = await supabase.rpc("XXXXXX");

  if (error) {
    return new Response(JSON.stringify({ error: error.message }), {
      headers: { "Content-Type": "application/json" },
      status: 500,
    });
  }

  // 型安全なデータの使用
  const responseData: ResponseData = data[0];

  return new Response(JSON.stringify(responseData), {
    headers: { "Content-Type": "application/json" },
    status: 200,
  });
});
```

> 💡 **注意**: ローカル環境で実行はしないので、importとDenoで構文エラーが発生していても無視してください（赤い波線部分）。

> 💡 **型定義**: `XXXXXX` 部分は実際のDatabase Function名に置き換え、型定義も合わせて更新してください。

### 2.2 Database Functions の呼び出し

```typescript
// 引数なし
const { data, error } = await supabase.rpc("function_name");

// 引数あり
const { data, error } = await supabase.rpc("function_name", {
  param1: value1,
  param2: value2
});
```

`XXXXXX` 部分は利用したいDatabase Functionsの名称を指定してください。

### 2.3 型定義（database.types.ts の参照）

**重要な原則**:
- Database Function の戻り値は `database.types.ts` から型を参照する
- 型安全性を確保し、データベーススキーマ変更時に自動的に型エラーを検知できる
- `Database["public"]["Functions"]` を使用してDatabase Functionの型を参照する

#### 基本的な型定義パターン

```typescript
import "jsr:@supabase/functions-js/edge-runtime.d.ts";
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";
import type { Database } from "../_shared/database.types.ts";

// Database Function の戻り値の型を定義
type UserData = Database["public"]["Functions"]["sel_user_by_auth_id"]["Returns"][0];

Deno.serve(async (req) => {
  const supabase = createClient(
    Deno.env.get("SUPABASE_URL"),
    Deno.env.get("SUPABASE_ANON_KEY")
  );

  // Database Function を呼び出し
  const { data, error } = await supabase.rpc("sel_user_by_auth_id", {
    target_auth_user_id: "xxx",
  });

  if (error) {
    return new Response(JSON.stringify({ error: error.message }), {
      headers: { "Content-Type": "application/json" },
      status: 500,
    });
  }

  // database.types.ts で定義された型を使用
  const userData: UserData = data[0];

  return new Response(JSON.stringify(userData), {
    headers: { "Content-Type": "application/json" },
    status: 200,
  });
});
```

#### Tables 型を使用する場合

テーブルの型を参照する場合は、`Tables` 型を使用することでより簡潔に書けます。

```typescript
import type { Database, Tables } from "../_shared/database.types.ts";

// Database Function の戻り値の型
type UserData = Database["public"]["Functions"]["sel_user_by_auth_id"]["Returns"][0];

// テーブルの型を直接参照する場合（簡潔な書き方）
type Customer = Tables["m_customer"];

// 複数のテーブル型を使用する例
type Office = Tables["m_office"];
type Department = Tables["m_department"];
```

#### Database 型を使用する場合

より詳細な型定義が必要な場合は、`Database` 型も使用できます。

```typescript
import type { Database } from "../_shared/database.types.ts";

// フルパスで指定する場合
type Customer = Database["public"]["Tables"]["m_customer"]["Row"];
type CustomerInsert = Database["public"]["Tables"]["m_customer"]["Insert"];
type CustomerUpdate = Database["public"]["Tables"]["m_customer"]["Update"];
```

> 💡 **推奨**: 通常は `Tables` 型とともに `Database["public"]["Functions"]` を使用します。

#### 型定義のメリット

✅ **型安全性の向上**: データベースの型定義と完全に同期  
✅ **補完機能**: IDEでプロパティが正確に補完される  
✅ **メンテナンス性**: スキーマ変更時に自動的に型エラーで検知できる  
✅ **可読性**: `Database["public"]["Functions"]["function_name"]["Returns"]` の形式で意図が明確

### 2.4 CORS 対応（Web API の場合）

Web で利用する想定の API を実装する場合、CORS 対応として以下を対応してください。

#### HTTPメソッドの制限（セキュリティのベストプラクティス）

**重要な原則**:
- 必要最小限のHTTPメソッドのみを許可する
- 読み取り専用のAPIは **GETメソッドのみ** を許可する
- 不要なメソッドを許可しない（セキュリティリスクを低減）

#### GETメソッドのみを許可する場合（推奨）

データ取得系のAPIでは、GETメソッドのみを許可します。

```typescript
Deno.serve(async (req) => {
  const allowedOrigin = Deno.env.get("EDGE_FUNCTION_ALLOWED_ORIGIN");
  
  // CORS対応: OPTIONSリクエストへの応答
  if (req.method === "OPTIONS") {
    return new Response(null, {
      headers: {
        "Access-Control-Allow-Origin": allowedOrigin || "*",
        "Access-Control-Allow-Methods": "GET, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type, Authorization",
      },
      status: 204,
    });
  }

  try {
    // GETメソッドのみ許可
    if (req.method !== "GET") {
      console.warn("[WARN] Invalid method", { method: req.method });
      return new Response(
        JSON.stringify({ success: false, error: "Method not allowed" }),
        {
          headers: {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": allowedOrigin || "*",
          },
          status: 405,
        }
      );
    }

    // 以降、通常の処理
    const { data, error } = await supabase.rpc("XXXXXX");

    // レスポンスにもCORSヘッダーを追加
    const headers = {
      "Content-Type": "application/json",
      "Access-Control-Allow-Origin": allowedOrigin || "*",
    };

    if (error) {
      return new Response(JSON.stringify({ success: false, error: error.message }), {
        headers,
        status: 500,
      });
    }

    return new Response(JSON.stringify({ success: true, data }), {
      headers,
      status: 200,
    });
  } catch (err) {
    console.error("[EXCEPTION] Unexpected error", { error: err.message });
    return new Response(
      JSON.stringify({ success: false, error: "Internal server error" }),
      {
        headers: {
          "Content-Type": "application/json",
          "Access-Control-Allow-Origin": allowedOrigin || "*",
        },
        status: 500,
      }
    );
  }
});
```

#### 複数のメソッドを許可する場合

データ登録・更新・削除が必要なAPIでは、必要なメソッドのみを許可します。

```typescript
Deno.serve(async (req) => {
  const allowedOrigin = Deno.env.get("EDGE_FUNCTION_ALLOWED_ORIGIN");
  
  // CORS対応: OPTIONSリクエストへの応答
  if (req.method === "OPTIONS") {
    return new Response(null, {
      headers: {
        "Access-Control-Allow-Origin": allowedOrigin || "*",
        "Access-Control-Allow-Methods": "POST, PUT, DELETE, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type, Authorization",
      },
      status: 204,
    });
  }

  try {
    // 許可されたメソッドのみ受け付ける
    if (!["POST", "PUT", "DELETE"].includes(req.method)) {
      console.warn("[WARN] Invalid method", { method: req.method });
      return new Response(
        JSON.stringify({ success: false, error: "Method not allowed" }),
        {
          headers: {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": allowedOrigin || "*",
          },
          status: 405,
        }
      );
    }

    // メソッドに応じた処理
    // ...
  } catch (err) {
    // エラーハンドリング
  }
});
```

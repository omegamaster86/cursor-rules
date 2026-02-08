# Supabase 実装ガイド（分割）: サンプルコード集

## 5. サンプルコード集

### 5.1 Database Function: ユーザー情報取得

```sql
create or replace function sel_user_by_id(target_user_id bigint)
returns TABLE(
  id bigint,
  email text,
  display_name text,
  created_at timestamptz
)
language plpgsql
as $$
begin
  return query
  select
    u.id,
    u.email,
    u.display_name,
    u.created_at
  from
    users u
  where
    u.id = target_user_id
    and u.deleted_at is null
  ;
end;
$$;
```

### 5.2 Edge Function: ユーザー情報取得 API

```typescript
import "jsr:@supabase/functions-js/edge-runtime.d.ts";
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";
import type { Database } from "../_shared/database.types.ts";

// Database Function の戻り値の型を定義
type UserData = Database["public"]["Functions"]["sel_user_by_id"]["Returns"][0];

Deno.serve(async (req) => {
  console.log("[START] get-user-data called", {
    method: req.method,
    url: req.url,
    timestamp: new Date().toISOString(),
  });

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

    // 認証トークンを取得
    const authHeader = req.headers.get("Authorization");
    if (!authHeader) {
      console.warn("[WARN] Missing Authorization header");
      return new Response(
        JSON.stringify({ success: false, error: "認証トークンがありません" }),
        {
          headers: {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": allowedOrigin || "*",
          },
          status: 401,
        }
      );
    }

    // Supabaseクライアントに認証トークンを設定
    const supabaseWithAuth = createClient(
      Deno.env.get("SUPABASE_URL") ?? "",
      Deno.env.get("SUPABASE_ANON_KEY") ?? "",
      {
        global: {
          headers: { Authorization: authHeader },
        },
      }
    );

    // 認証ユーザー情報を取得
    const {
      data: { user },
      error: authError,
    } = await supabaseWithAuth.auth.getUser();

    if (authError || !user) {
      console.error("[ERROR] Authentication failed", {
        error: authError?.message,
        timestamp: new Date().toISOString(),
      });
      return new Response(
        JSON.stringify({ success: false, error: "ユーザー認証に失敗しました" }),
        {
          headers: {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": allowedOrigin || "*",
          },
          status: 401,
        }
      );
    }

    // URLクエリパラメータからuserIdを取得
    const url = new URL(req.url);
    const userId = url.searchParams.get("userId");

    if (!userId) {
      console.warn("[WARN] Missing userId parameter");
      return new Response(
        JSON.stringify({ success: false, error: "userId is required" }),
        {
          headers: {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": allowedOrigin || "*",
          },
          status: 400,
        }
      );
    }

    // Database Function 呼び出し
    const { data, error } = await supabaseWithAuth.rpc("sel_user_by_id", {
      target_user_id: parseInt(userId, 10),
    });

    if (error) {
      console.error("[ERROR] Database function failed", {
        function: "sel_user_by_id",
        userId,
        error: error.message,
        timestamp: new Date().toISOString(),
      });
      return new Response(
        JSON.stringify({ success: false, error: error.message }),
        {
          headers: {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": allowedOrigin || "*",
          },
          status: 500,
        }
      );
    }

    console.log("[SUCCESS] User data retrieved", {
      userId,
      found: data?.length > 0,
      timestamp: new Date().toISOString(),
    });

    // database.types.ts で定義された型を使用
    const userData: UserData | null = data?.[0] || null;

    return new Response(
      JSON.stringify({ success: true, data: userData }),
      {
        headers: {
          "Content-Type": "application/json",
          "Access-Control-Allow-Origin": allowedOrigin || "*",
        },
        status: 200,
      }
    );
  } catch (err) {
    console.error("[EXCEPTION] Unexpected error", {
      error: err.message,
      stack: err.stack,
      timestamp: new Date().toISOString(),
    });
    return new Response(
      JSON.stringify({ success: false, error: "サーバーエラーが発生しました" }),
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

### 5.3 Database Function: UPSERT（設定の登録・更新）

```sql
create or replace function upsert_user_settings(
  p_user_id bigint,
  p_key text,
  p_value text
)
returns TABLE(
  user_id bigint,
  key text,
  value text,
  updated_at timestamptz
)
language plpgsql
as $$
begin
  return query
  insert into user_settings (user_id, key, value, updated_at)
  values (p_user_id, p_key, p_value, now())
  on conflict (user_id, key)
  do update set
    value = excluded.value,
    updated_at = now()
  returning
    user_settings.user_id,
    user_settings.key,
    user_settings.value,
    user_settings.updated_at;
end;
$$;
```

### 5.4 Database Function: カーソルベースのページネーション

```sql
create or replace function sel_orders_paged(
  p_customer_id bigint,
  p_last_id bigint default 0,
  p_limit int default 20
)
returns TABLE(
  id bigint,
  customer_id bigint,
  total numeric,
  status text,
  created_at timestamptz
)
language plpgsql
as $$
begin
  return query
  select
    o.id,
    o.customer_id,
    o.total,
    o.status,
    o.created_at
  from
    orders o
  where
    o.customer_id = p_customer_id
    and o.id > p_last_id
  order by
    o.id
  limit
    p_limit;
end;
$$;

-- 使用例:
-- 1ページ目: select * from sel_orders_paged(123, 0, 20);
-- 2ページ目: select * from sel_orders_paged(123, last_id, 20);
-- ※ last_id = 前ページの最後のレコードの id
```

### 5.5 テーブル定義 + RLS のセット例

新しいテーブルを作成する際の推奨パターンです。

```sql
-- テーブル定義（推奨されるデータ型を使用）
create table orders (
  id bigint generated always as identity primary key,
  customer_id bigint not null references customers(id) on delete cascade,
  total numeric(10,2) not null default 0,
  status text not null default 'pending',
  notes text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  deleted_at timestamptz  -- 論理削除
);

-- RLS を有効化
alter table orders enable row level security;
alter table orders force row level security;

-- RLS ポリシー（SELECT でラップしてパフォーマンス最適化）
create policy orders_select_policy on orders
  for select
  to authenticated
  using (customer_id in (
    select c.id from customers c
    where c.auth_user_id = (select auth.uid())
  ));

create policy orders_insert_policy on orders
  for insert
  to authenticated
  with check (customer_id in (
    select c.id from customers c
    where c.auth_user_id = (select auth.uid())
  ));
```

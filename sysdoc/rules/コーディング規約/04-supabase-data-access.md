## 4. Supabaseデータアクセス規約

Supabase を使用してデータベースにアクセスする際の実装方法を定義します。

### 4.1 データアクセスの階層構造

データベースアクセスは、以下の3層構造で実装することを原則とします：

```
Page Component (page.tsx)
  ↓ 呼び出し
Server Action (_apis/*.server.ts)
  ↓ fetch()
Edge Function (supabase/functions/*/index.ts)
  ↓ rpc()
Database Function (supabase/migrations/*.sql)
  ↓ クエリ実行
PostgreSQL Database
```

**この階層構造を採用する理由**：

1. **セキュリティ**: データベースロジックをサーバーサイドに集約し、クライアントから直接アクセスさせない
2. **保守性**: ビジネスロジックを DB Function に集約することで、変更箇所を最小化
3. **再利用性**: Edge Function を API として他のクライアントからも利用可能
4. **テスト容易性**: 各層を独立してテスト可能

### 4.2 データアクセスの実装方針

#### 4.2.1 直接アクセスの禁止

Server Component や Server Action から、Supabase クライアントを使って **直接データベーステーブルにアクセスすることは禁止** します。

```typescript
// ❌ 悪い例：Supabase クライアントで直接テーブルにアクセス
const { data } = await supabase
  .from("t_schedule")
  .select("*")
  .eq("user_id", userId);
```

#### 4.2.2 3層構造での実装（推奨）

必ず以下の手順で実装します：

1. **DB Function（SQL）を作成**
2. **Edge Function を作成**（DB Function を `rpc()` で呼び出す）
3. **Server Action を作成**（Edge Function を `fetch()` で呼び出す）
4. **Page Component から呼び出し**

### 4.3 DB Function（SQL）の実装規則

#### 4.3.1 ファイル配置

- `supabase/migrations/` ディレクトリに配置
- ファイル名: `YYYYMMDDHHMMSS_create_function_<関数名>.sql`
- 例: `20251108000000_create_function_sel_today_schedules.sql`

#### 4.3.2 関数の命名規則

| 操作タイプ | プレフィックス | 例                      |
| ---------- | -------------- | ----------------------- |
| SELECT     | `sel_`         | `sel_user_by_id`        |
| INSERT     | `ins_`         | `ins_new_user`          |
| UPDATE     | `upd_`         | `upd_user_status`       |
| DELETE     | `del_`         | `del_user_by_id`        |
| 複合処理   | 動詞_          | `register_new_customer` |

#### 4.3.3 実装例

DB Function の詳細な実装例については、以下のドキュメントを参照してください。

> 📖 **詳細**: [03\_Supabase実装ガイド\_Web.md](03_Supabase実装ガイド_Web.md) の「1. Database Functions（SQL）」および「5.1 Database Function: ユーザー情報取得」を参照

### 4.4 Edge Function の実装規則

#### 4.4.1 ファイル配置

- `supabase/functions/<関数名>/index.ts`
- 関数名は kebab-case を使用
- 例: `supabase/functions/get-today-schedules/index.ts`

#### 4.4.2 命名規則

| 操作タイプ | プレフィックス | 例                      |
| ---------- | -------------- | ----------------------- |
| GET（取得）| `get-`         | `get-today-schedules`   |
| POST（作成）| `create-`     | `create-user`           |
| PUT（更新） | `update-`      | `update-user-status`    |
| DELETE（削除）| `delete-`   | `delete-user`           |

#### 4.4.3 HTTPメソッドの使い分け

| 操作     | HTTPメソッド | パラメータ渡し方      | 用途                     |
| -------- | ------------ | --------------------- | ------------------------ |
| 参照     | GET          | URLクエリパラメータ   | データの取得             |
| 作成     | POST         | リクエストボディ      | 新規データの作成         |
| 更新     | POST/PUT     | リクエストボディ      | 既存データの更新         |
| 削除     | POST/DELETE  | リクエストボディ      | データの削除             |

**注意**: データの参照（SELECT）は必ず **GET メソッド** を使用してください。

#### 4.4.4 実装例

Edge Function の詳細な実装例については、以下のドキュメントを参照してください。

> 📖 **詳細**: [03\_Supabase実装ガイド\_Web.md](03_Supabase実装ガイド_Web.md) の「2. Edge Functions」および「5.2 Edge Function: ユーザー情報取得 API」を参照

**GETメソッドでのパラメータ取得例**:

```typescript
// URLクエリパラメータから取得
const url = new URL(req.url);
const userId = url.searchParams.get("userId");
const startDate = url.searchParams.get("startDate");

// 数値変換が必要な場合
const userIdNum = parseInt(userId, 10);
if (isNaN(userIdNum)) {
  // エラーハンドリング
}
```

### 4.5 Server Action（_apis）の実装規則

#### 4.5.1 ファイル配置（コロケーション）

Server Action は、使用する Page Component と同じディレクトリ配下の `_apis/` ディレクトリに配置します。

```
app/
  (app)/
    dashboard/
      _apis/
        schedule.server.ts  ← Server Action
      page.tsx              ← Page Component
```

**コロケーションの利点**：

- 関連するファイルが近くに配置され、保守性が向上
- 相対パスでのインポートが可能（`"./_apis/schedule.server"`）
- ページ固有のロジックであることが明確

#### 4.5.2 命名規則

- ファイル名: `<機能名>.server.ts`（例: `schedule.server.ts`）
- 関数名: `get` + 機能名（camelCase）（例: `getTodaySchedules`）
- ファイルの先頭に `"use server";` ディレクティブを記載

#### 4.5.3 実装例

```typescript
"use server";

import { createClient } from "@/lib/supabase/server";

/**
 * 今日のスケジュールを取得
 * サーバーサイドでEdge Functionを呼び出して今日のスケジュールを取得する
 *
 * @param userId ユーザーID
 * @param todayStart 今日の開始時刻（ISO文字列）
 * @param tomorrowStart 明日の開始時刻（ISO文字列）
 * @returns スケジュール配列またはnull
 */
export async function getTodaySchedules(
  userId: number,
  todayStart: string,
  tomorrowStart: string
) {
  const supabase = await createClient();

  try {
    // 1. 認証検証（必須）
    const {
      data: { user },
      error: userError,
    } = await supabase.auth.getUser();

    if (userError || !user) {
      return null;
    }

    // 2. トークン取得（Edge Function呼び出し用）
    const {
      data: { session },
    } = await supabase.auth.getSession();

    if (!session) {
      return null;
    }

    // 3. Supabase URL取得
    const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL;
    if (!supabaseUrl) {
      console.error("NEXT_PUBLIC_SUPABASE_URL が設定されていません");
      return null;
    }

    // 4. fetchメソッドでEdge Functionを呼び出し（GETメソッド）
    const queryParams = new URLSearchParams({
      userId: userId.toString(),
      todayStart,
      tomorrowStart,
    });
    const response = await fetch(
      `${supabaseUrl}/functions/v1/get-today-schedules?${queryParams.toString()}`,
      {
        method: "GET",
        headers: {
          Authorization: `Bearer ${session.access_token}`,
        },
      }
    );

    // 5. HTTPステータスチェック
    if (!response.ok) {
      console.error("Edge Function呼び出しエラー:", {
        status: response.status,
        statusText: response.statusText,
      });
      return null;
    }

    // 6. レスポンスをJSON形式でパース
    const data = await response.json();

    // 7. レスポンスの成功チェック
    if (!data?.success) {
      console.error("スケジュール情報取得エラー:", data?.error);
      return null;
    }

    return data.data;
  } catch (error) {
    console.error("スケジュール取得エラー:", error);
    return null;
  }
}
```

### 4.6 Page Component からの呼び出し

#### 4.6.1 実装例

```typescript
import { getTodaySchedules } from "./_apis/schedule.server";

export default async function DashboardPage() {
  // 現在のユーザーIDを取得（省略）
  const currentUserId = 123;

  // 日付範囲を計算（省略）
  const todayStr = "2025-11-08T00:00:00.000Z";
  const tomorrowStr = "2025-11-09T00:00:00.000Z";

  // Server Actionを呼び出してスケジュールを取得
  const todaySchedules = currentUserId
    ? await getTodaySchedules(currentUserId, todayStr, tomorrowStr)
    : null;

  return (
    <div>
      {todaySchedules && todaySchedules.length > 0 ? (
        <div>
          {todaySchedules.map((schedule) => (
            <div key={schedule.id}>{schedule.title}</div>
          ))}
        </div>
      ) : (
        <div>今日の予定はありません</div>
      )}
    </div>
  );
}
```

### 4.7 クライアントサイドからの外部API呼び出し規約

#### 4.7.1 基本原則（セキュリティ重要）

クライアントサイド（`_apis/*.client.ts`）から外部APIを呼び出す場合、**APIキーなどの機密情報を露出しないために、必ずNext.jsのRoute Handlers（API Routes）を経由してAPI実行すること**。

**禁止事項**：
- クライアントサイドから直接外部APIを呼び出すこと
- APIキー、シークレットキーなどの機密情報をクライアントサイドに含めること
- 環境変数（`NEXT_PUBLIC_*`以外）をクライアントサイドで使用すること

**理由**：
- クライアントサイドのコードはブラウザで実行されるため、すべてのコードが公開される
- APIキーをクライアントサイドに含めると、DevToolsやソースコードから簡単に抽出される
- 悪意のあるユーザーがAPIキーを取得し、不正利用する可能性がある

#### 4.7.2 実装パターン

外部API呼び出しは、以下の2層構造で実装します：

```
Client Component (_apis/*.client.ts)
  ↓ fetch()
Route Handler (app/api/*/route.ts)
  ↓ 外部API呼び出し（APIキーを使用）
External API（例：OpenAI API、Stripe API、SendGrid API など）
```

#### 4.7.3 Route Handler の実装例

```typescript
// app/api/openai/chat/route.ts（Route Handler）
import { NextRequest, NextResponse } from "next/server";
import { createClient } from "@/lib/supabase/server";

/**
 * OpenAI ChatGPT APIを呼び出すRoute Handler
 * APIキーはサーバーサイドで管理し、クライアントに露出しない
 */
export async function POST(request: NextRequest) {
  try {
    // 1. 認証検証（必須）
    const supabase = await createClient();
    const {
      data: { user },
      error: userError,
    } = await supabase.auth.getUser();

    if (userError || !user) {
      return NextResponse.json(
        { error: "認証が必要です" },
        { status: 401 }
      );
    }

    // 2. リクエストボディを取得
    const { message } = await request.json();

    if (!message) {
      return NextResponse.json(
        { error: "メッセージが必要です" },
        { status: 400 }
      );
    }

    // 3. APIキーを環境変数から取得（サーバーサイドのみ）
    const apiKey = process.env.OPENAI_API_KEY;

    if (!apiKey) {
      console.error("OPENAI_API_KEY が設定されていません");
      return NextResponse.json(
        { error: "サーバー設定エラー" },
        { status: 500 }
      );
    }

    // 4. 外部API（OpenAI）を呼び出し
    const response = await fetch("https://api.openai.com/v1/chat/completions", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${apiKey}`, // APIキーはサーバーサイドで使用
      },
      body: JSON.stringify({
        model: "gpt-4",
        messages: [{ role: "user", content: message }],
      }),
    });

    if (!response.ok) {
      console.error("OpenAI API呼び出しエラー:", response.statusText);
      return NextResponse.json(
        { error: "AI API呼び出しエラー" },
        { status: response.status }
      );
    }

    const data = await response.json();

    // 5. クライアントにレスポンスを返す
    return NextResponse.json({
      success: true,
      data: data.choices[0].message.content,
    });
  } catch (error) {
    console.error("Route Handlerエラー:", error);
    return NextResponse.json(
      { error: "サーバーエラー" },
      { status: 500 }
    );
  }
}
```

#### 4.7.4 Client APIの実装例

```typescript
// app/(app)/chat/_apis/openai.client.ts（クライアントサイド）
"use client";

/**
 * OpenAI ChatGPT APIを呼び出すクライアント関数
 * Route Handlerを経由して呼び出すため、APIキーは露出しない
 *
 * @param message ユーザーのメッセージ
 * @returns AI応答またはnull
 */
export async function sendChatMessage(message: string) {
  try {
    // Route Handlerを経由してAPIを呼び出し
    const response = await fetch("/api/openai/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ message }),
    });

    if (!response.ok) {
      console.error("Chat API呼び出しエラー:", {
        status: response.status,
        statusText: response.statusText,
      });
      return null;
    }

    const data = await response.json();

    if (!data?.success) {
      console.error("Chat API応答エラー:", data?.error);
      return null;
    }

    return data.data;
  } catch (error) {
    console.error("Chat API通信エラー:", error);
    return null;
  }
}
```

#### 4.7.5 Client Componentからの呼び出し

```typescript
// app/(app)/chat/page.tsx
"use client";

import { useState } from "react";
import { sendChatMessage } from "./_apis/openai.client";

export default function ChatPage() {
  const [message, setMessage] = useState("");
  const [response, setResponse] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();

    if (!message.trim()) {
      return;
    }

    setLoading(true);

    // クライアントAPI関数を呼び出し
    const aiResponse = await sendChatMessage(message);

    if (aiResponse) {
      setResponse(aiResponse);
    } else {
      setResponse("エラーが発生しました");
    }

    setLoading(false);
  }

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="メッセージを入力"
          disabled={loading}
        />
        <button type="submit" disabled={loading}>
          {loading ? "送信中..." : "送信"}
        </button>
      </form>

      {response && (
        <div>
          <h3>AI応答:</h3>
          <p>{response}</p>
        </div>
      )}
    </div>
  );
}
```

#### 4.7.6 環境変数の管理

外部APIのキーは、必ず環境変数として管理し、サーバーサイドでのみ使用します。

```bash
# .env.local（サーバーサイドでのみ使用可能）
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
STRIPE_SECRET_KEY=sk_test_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
SENDGRID_API_KEY=SG.xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# クライアントサイドで必要な環境変数（NEXT_PUBLIC_プレフィックス）
NEXT_PUBLIC_APP_URL=https://example.com
NEXT_PUBLIC_SUPABASE_URL=https://xxxxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**重要な注意点**：
- `NEXT_PUBLIC_*` プレフィックスが付いた環境変数は、クライアントサイドに公開される
- APIキーやシークレットキーには `NEXT_PUBLIC_*` プレフィックスを**絶対に付けない**
- クライアントサイドで使用する環境変数は、公開されても問題ない値のみにする

#### 4.7.7 良い例と悪い例

```typescript
// ❌ 悪い例：クライアントサイドから直接外部APIを呼び出し（APIキーが露出する）
"use client";

export async function sendChatMessage(message: string) {
  // APIキーがクライアントサイドに露出する（危険）
  const apiKey = process.env.NEXT_PUBLIC_OPENAI_API_KEY;

  const response = await fetch("https://api.openai.com/v1/chat/completions", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${apiKey}`, // APIキーがブラウザで見える
    },
    body: JSON.stringify({
      model: "gpt-4",
      messages: [{ role: "user", content: message }],
    }),
  });

  return await response.json();
}
```

```typescript
// ✅ 良い例：Route Handlerを経由してAPIを呼び出し（APIキーは露出しない）
"use client";

export async function sendChatMessage(message: string) {
  // Route Handlerを経由（APIキーはサーバーサイドで管理）
  const response = await fetch("/api/openai/chat", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ message }),
  });

  return await response.json();
}
```

### 4.8 データアクセス規約まとめ

| 層                | ファイル配置                          | 命名規則                    | 責務                           |
| ----------------- | ------------------------------------- | --------------------------- | ------------------------------ |
| DB Function       | `supabase/migrations/*.sql`           | `sel_`, `ins_`, `upd_`, `del_` | データベースクエリの実行       |
| Edge Function     | `supabase/functions/*/index.ts`       | `get-`, `create-`, `update-`, `delete-` | DB Functionの呼び出し（rpc）   |
| Server Action     | `app/(app)/<page>/_apis/*.server.ts`  | `get*`, `create*`, `update*`, `delete*` | Edge Functionの呼び出し（fetch） |
| Client API        | `app/(app)/<page>/_apis/*.client.ts`  | `send*`, `call*`, `fetch*` | Route Handlerの呼び出し（fetch） |
| Route Handler     | `app/api/*/route.ts`                  | HTTPメソッド（GET, POST, etc.） | 外部APIの呼び出し（APIキー管理） |
| Page Component    | `app/(app)/<page>/page.tsx`           | -                           | Server Actionの呼び出し        |

### 4.9 データフェッチコロケーション

#### 4.9.1 基本原則

データは **必要なコンポーネントで直接フェッチする** ことを原則とします。

```typescript
// ✅ 良い例：データが必要なコンポーネントで直接フェッチ
async function UserProfile({ userId }: { userId: number }) {
  // このコンポーネントで必要なデータを直接取得
  const userData = await getUserData(userId);

  return (
    <div>
      <h1>{userData.name}</h1>
      <UserStats userId={userId} />
    </div>
  );
}

async function UserStats({ userId }: { userId: number }) {
  // このコンポーネントで必要なデータを直接取得（Request Memoizationにより重複リクエストは自動的に排除される）
  const userData = await getUserData(userId);

  return (
    <div>
      <p>投稿数: {userData.postCount}</p>
    </div>
  );
}
```

```typescript
// ❌ 悪い例：親コンポーネントでデータを取得してpropsで渡す（Props Drilling）
async function UserProfile({ userId }: { userId: number }) {
  // 親で一度だけ取得
  const userData = await getUserData(userId);

  return (
    <div>
      <h1>{userData.name}</h1>
      {/* propsでデータを子孫コンポーネントへ渡す（Props Drilling） */}
      <UserStats userData={userData} />
    </div>
  );
}

function UserStats({ userData }: { userData: User }) {
  return (
    <div>
      <p>投稿数: {userData.postCount}</p>
    </div>
  );
}
```

#### 4.9.2 コロケーションのメリット

データフェッチコロケーションを実践することで、以下のメリットが得られます：

1. **コンポーネントの独立性向上**
   - 各コンポーネントが自身に必要なデータを自分で管理する
   - 他のコンポーネントへの依存が減り、単独でのテストや再利用が容易になる

2. **Props Drillingの解消**
   - 親から子、孫へとpropsを何階層も渡す必要がなくなる
   - 中間コンポーネントが不要なpropsを持たずに済む

3. **保守性の向上**
   - データの取得場所と使用場所が近いため、変更が容易
   - データ構造の変更時に影響範囲が限定される

4. **コンポーネントの再利用性向上**
   - コンポーネントが自己完結しているため、別の画面やプロジェクトでも再利用しやすい

#### 4.9.3 Request Memoization による重複排除

Next.js 15 では、**Request Memoization** というキャッシュ機能が同一レンダー内の重複取得を自動的に排除します。

**仕組み**：
- 同じレンダーツリー内で同じ URL とオプションの `fetch` リクエストは、1回だけ実行される
- 複数のコンポーネントで同じデータを取得しても、実際のネットワークリクエストは1回のみ
- Server Actions や Server Components でも同様に動作する

```typescript
// 以下の例では、getUserData(123) が複数回呼ばれても
// 実際のリクエストは1回だけ実行される

async function ParentComponent() {
  const userData = await getUserData(123); // ← 1回目：実際にリクエスト実行

  return (
    <div>
      <h1>{userData.name}</h1>
      <ChildComponent userId={123} />
    </div>
  );
}

async function ChildComponent({ userId }: { userId: number }) {
  const userData = await getUserData(123); // ← 2回目：キャッシュから取得（リクエストなし）

  return <div>{userData.email}</div>;
}
```

**注意点**：
- Request Memoization は **同一レンダー内でのみ有効**
- 異なるページやリクエスト間では共有されない
- Server Actions の場合も同様に、同じレンダー内であれば重複排除される

#### 4.9.4 実装のポイント

```typescript
// ✅ 良い例：コンポーネントが自己完結している
async function ProductCard({ productId }: { productId: number }) {
  // 必要なデータを自分で取得
  const product = await getProduct(productId);

  if (!product) {
    return <div>商品が見つかりません</div>;
  }

  return (
    <div>
      <h2>{product.name}</h2>
      <p>¥{product.price.toLocaleString()}</p>
      {/* このコンポーネント内でさらに子コンポーネントを使う場合も同様 */}
      <ProductReviews productId={productId} />
    </div>
  );
}

async function ProductReviews({ productId }: { productId: number }) {
  // このコンポーネントでも必要なデータを直接取得（Request Memoizationにより重複リクエストは排除される）
  const reviews = await getProductReviews(productId);

  return (
    <div>
      {reviews.map((review) => (
        <div key={review.id}>{review.comment}</div>
      ))}
    </div>
  );
}
```

```typescript
// ❌ 悪い例：親コンポーネントで全てのデータを取得してpropsで配る
async function ProductPage({ productId }: { productId: number }) {
  // 親で全てのデータを取得
  const product = await getProduct(productId);
  const reviews = await getProductReviews(productId);

  return (
    <div>
      {/* propsでデータを渡す（コンポーネントの独立性が低下） */}
      <ProductCard product={product} />
      <ProductReviews reviews={reviews} />
    </div>
  );
}

function ProductCard({ product }: { product: Product }) {
  // propsに依存している（再利用性が低い）
  return (
    <div>
      <h2>{product.name}</h2>
      <p>¥{product.price.toLocaleString()}</p>
    </div>
  );
}
```

---

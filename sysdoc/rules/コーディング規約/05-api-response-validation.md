## 5. APIレスポンスバリデーション規約

APIからのレスポンスを安全に処理するため、Zodを使用したバリデーション規約を定義します。

### 5.1 基本原則：信頼境界でのバリデーション

**信頼境界（Trust Boundary）でのみZodバリデーションを実施する**

```
外部API → [zodバリデーション] → 内部処理
```

**理由**:
- ランタイムでのデータ型チェックにより、予期しないレスポンス形式を早期に検出
- TypeScriptの型チェックとランタイムバリデーションの両方を実現
- 不正なデータによる実行時エラーを防止
- APIレスポンスの仕様変更を検出可能

### 5.2 バリデーションを実施する場所

#### 5.2.1 バリデーションが必要な場所（✅ 必須）

以下のケースでは**必ずZodバリデーションを実施**してください：

| 場所 | 対象API | 理由 |
|------|---------|------|
| **Route Handler** | Supabase Edge Functions、FastAPIなど外部API | 信頼境界（外部→内部） |
| **Client API** | FastAPIへの直接呼び出し | 信頼境界（外部→内部） |
| **Server Action** | 外部APIを直接呼び出す場合 | 信頼境界（外部→内部） |

### 5.3 Zodスキーマの定義

#### 5.3.1 スキーマの配置場所

すべてのZodスキーマは `src/types/schemas.ts` に集約して定義します。

```typescript
// src/types/schemas.ts
import { z } from 'zod';

// ユーザー情報のスキーマ
export const UserSchema = z.object({
    id: z.string().uuid(),
    email: z.string().email(),
    name: z.string().min(1),
    age: z.number().int().positive().optional(),
    role: z.enum(['admin', 'user', 'guest']),
    created_at: z.string().datetime(),
    updated_at: z.string().datetime(),
});

// TypeScriptの型を自動生成
export type User = z.infer<typeof UserSchema>;

// 商品情報のスキーマ
export const ProductSchema = z.object({
    id: z.number().int().positive(),
    name: z.string().min(1),
    description: z.string().nullable(),
    price: z.number().positive(),
    stock: z.number().int().nonnegative(),
    category: z.string(),
    is_available: z.boolean(),
    created_at: z.string().datetime(),
});

export type Product = z.infer<typeof ProductSchema>;
```

#### 5.3.2 スキーマの命名規則

| 対象 | 命名規則 | 例 |
|------|---------|-----|
| スキーマ | 型名 + `Schema` | `UserDataSchema`, `ApiResponseSchema` |
| 成功レスポンス | 型名 + `SuccessResponseSchema` | `SearchSuccessResponseSchema` |
| エラーレスポンス | 型名 + `ErrorResponseSchema` | `SearchErrorResponseSchema` |
| 統合スキーマ | 型名 + `ResponseSchema` | `SearchResponseSchema` |

#### 5.3.3 Union型を使った成功/失敗の表現

APIレスポンスは、成功時と失敗時で異なる構造を持つため、Union型を使用します。

```typescript
// ユーザー取得の成功レスポンス
export const GetUserSuccessResponseSchema = z.object({
    success: z.literal(true),
    data: UserSchema,
});

// エラーレスポンス
export const ErrorResponseSchema = z.object({
    success: z.literal(false),
    error: z.string(),
});

// 統合（Union型）
export const GetUserResponseSchema = z.union([
    GetUserSuccessResponseSchema,
    ErrorResponseSchema,
]);

export type GetUserResponse = z.infer<typeof GetUserResponseSchema>;

// 商品一覧取得のレスポンス（配列の場合）
export const GetProductsSuccessResponseSchema = z.object({
    success: z.literal(true),
    data: z.object({
        products: z.array(ProductSchema),
        total: z.number().int().nonnegative(),
        page: z.number().int().positive(),
        per_page: z.number().int().positive(),
    }),
});

export const GetProductsResponseSchema = z.union([
    GetProductsSuccessResponseSchema,
    ErrorResponseSchema,
]);

export type GetProductsResponse = z.infer<typeof GetProductsResponseSchema>;
```

### 5.4 Route Handlerでのバリデーション実装

Route Handlerでは、外部APIからのレスポンスを**必ずZodでバリデーション**します。

#### 5.4.1 実装パターン（GET: 単一リソース取得）

```typescript
// app/api/users/[id]/route.ts
import { NextRequest, NextResponse } from "next/server";
import { GetUserResponseSchema } from "@/types/schemas";
import type { GetUserResponse } from "@/types";

export async function GET(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  try {
    const userId = params.id;

    // 1. 認証チェック（必要に応じて）
    const authHeader = request.headers.get('authorization');
    if (!authHeader) {
      return NextResponse.json(
        { success: false, error: "認証が必要です" },
        { status: 401 }
      );
    }

    // 2. 外部API（例：バックエンドAPI）を呼び出し
    const apiUrl = process.env.BACKEND_API_URL;
    const response = await fetch(`${apiUrl}/users/${userId}`, {
      method: "GET",
      headers: {
        Authorization: authHeader,
        "Content-Type": "application/json",
      },
    });

    if (!response.ok) {
      return NextResponse.json(
        { success: false, error: `ユーザー取得に失敗しました (${response.status})` },
        { status: response.status }
      );
    }

    // 3. レスポンスをJSON形式でパース
    const jsonData = await response.json();

    // 4. ✅ zodでレスポンスをバリデーション（信頼境界）
    const validationResult = GetUserResponseSchema.safeParse(jsonData);

    if (!validationResult.success) {
      console.error("[API] レスポンスのバリデーションエラー:", {
        error: validationResult.error,
        receivedData: jsonData,
      });
      return NextResponse.json(
        {
          success: false,
          error: `レスポンスの形式が不正です: ${validationResult.error.message}`,
        },
        { status: 500 }
      );
    }

    // 5. バリデーション済みデータを使用（型安全）
    const data = validationResult.data;

    if (!data.success) {
      return NextResponse.json(
        { success: false, error: data.error },
        { status: 400 }
      );
    }

    // 6. 成功レスポンスを返す
    return NextResponse.json({
      success: true,
      data: data.data,
    } as GetUserResponse);

  } catch (error) {
    console.error("[EXCEPTION] ユーザー取得エラー:", error);
    return NextResponse.json(
      { success: false, error: "予期しないエラーが発生しました" },
      { status: 500 }
    );
  }
}
```

#### 5.4.2 実装パターン（GET: リスト取得）

```typescript
// app/api/products/route.ts
import { NextRequest, NextResponse } from "next/server";
import { GetProductsResponseSchema } from "@/types/schemas";
import type { GetProductsResponse } from "@/types";

export async function GET(request: NextRequest) {
  try {
    // 1. クエリパラメータの取得
    const searchParams = request.nextUrl.searchParams;
    const page = parseInt(searchParams.get('page') || '1');
    const perPage = parseInt(searchParams.get('per_page') || '20');
    const category = searchParams.get('category');

    // 2. 外部APIを呼び出し
    const apiUrl = process.env.BACKEND_API_URL;
    const params = new URLSearchParams({
      page: page.toString(),
      per_page: perPage.toString(),
      ...(category && { category }),
    });

    const response = await fetch(`${apiUrl}/products?${params.toString()}`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    });

    if (!response.ok) {
      return NextResponse.json(
        { success: false, error: `商品一覧取得に失敗しました (${response.status})` },
        { status: response.status }
      );
    }

    // 3. レスポンスをJSON形式でパース
    const jsonData = await response.json();

    // 4. ✅ zodでレスポンスをバリデーション（信頼境界）
    const validationResult = GetProductsResponseSchema.safeParse(jsonData);

    if (!validationResult.success) {
      console.error("[API] レスポンスのバリデーションエラー:", {
        error: validationResult.error,
        receivedData: jsonData,
      });
      return NextResponse.json(
        {
          success: false,
          error: `レスポンスの形式が不正です: ${validationResult.error.message}`,
        },
        { status: 500 }
      );
    }

    // 5. バリデーション済みデータを使用（型安全）
    const data = validationResult.data;

    if (!data.success) {
      return NextResponse.json(
        { success: false, error: data.error },
        { status: 400 }
      );
    }

    // 6. 成功レスポンスを返す
    return NextResponse.json({
      success: true,
      data: data.data,
    } as GetProductsResponse);

  } catch (error) {
    console.error("[EXCEPTION] 商品一覧取得エラー:", error);
    return NextResponse.json(
      { success: false, error: "予期しないエラーが発生しました" },
      { status: 500 }
    );
  }
}
```

#### 5.4.3 実装パターン（POST: リソース作成）

```typescript
// app/api/orders/route.ts
import { NextRequest, NextResponse } from "next/server";
import { CreateOrderRequestSchema, CreateOrderResponseSchema } from "@/types/schemas";

export async function POST(request: NextRequest) {
  try {
    // 1. リクエストボディの取得とバリデーション
    const body = await request.json();
    const requestValidation = CreateOrderRequestSchema.safeParse(body);

    if (!requestValidation.success) {
      return NextResponse.json(
        {
          success: false,
          error: `リクエストデータが不正です: ${requestValidation.error.message}`,
        },
        { status: 400 }
      );
    }

    const orderData = requestValidation.data;

    // 2. 外部APIを呼び出し
    const apiUrl = process.env.BACKEND_API_URL;
    const response = await fetch(`${apiUrl}/orders`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(orderData),
    });

    if (!response.ok) {
      return NextResponse.json(
        { success: false, error: `注文作成に失敗しました (${response.status})` },
        { status: response.status }
      );
    }

    // 3. レスポンスをJSON形式でパース
    const jsonData = await response.json();

    // 4. ✅ zodでレスポンスをバリデーション（信頼境界）
    const validationResult = CreateOrderResponseSchema.safeParse(jsonData);

    if (!validationResult.success) {
      console.error("[API] レスポンスのバリデーションエラー:", {
        error: validationResult.error,
        receivedData: jsonData,
      });
      return NextResponse.json(
        {
          success: false,
          error: `レスポンスの形式が不正です: ${validationResult.error.message}`,
        },
        { status: 500 }
      );
    }

    // 5. バリデーション済みデータを使用（型安全）
    const data = validationResult.data;

    if (!data.success) {
      return NextResponse.json(
        { success: false, error: data.error },
        { status: 400 }
      );
    }

    // 6. 成功レスポンスを返す
    return NextResponse.json(data, { status: 201 });

  } catch (error) {
    console.error("[EXCEPTION] 注文作成エラー:", error);
    return NextResponse.json(
      { success: false, error: "予期しないエラーが発生しました" },
      { status: 500 }
    );
  }
}
```

#### 5.4.4 エラーレスポンスのバリデーション

バックエンドAPIのエラーレスポンスも型安全に処理するため、専用のスキーマを定義します。

```typescript
// 一般的なエラーレスポンススキーマ
export const ApiErrorResponseSchema = z.object({
    message: z.string(),
    code: z.string().optional(),
    details: z.record(z.any()).optional(),
});

// RESTful APIの標準的なエラーレスポンス
export const StandardErrorResponseSchema = z.object({
    error: z.object({
        message: z.string(),
        status: z.number(),
        code: z.string().optional(),
    }),
});

// 使用例
if (!response.ok) {
    const errorJson = await response.json();
    const errorResult = ApiErrorResponseSchema.safeParse(errorJson);
    
    let errorMessage = 'API呼び出しに失敗しました';
    if (errorResult.success) {
        errorMessage = errorResult.data.message;
        if (errorResult.data.details) {
            console.error('エラー詳細:', errorResult.data.details);
        }
    }
    
    return NextResponse.json(
        { success: false, error: errorMessage },
        { status: response.status }
    );
}
```

### 5.5 Client APIでのバリデーション実装

Client APIでは、呼び出し先に応じてバリデーション方法を選択します。

#### 5.5.1 実装パターン（Route Handler経由の場合）

Route Handlerで既にバリデーションが行われているため、通常は型アサーションで問題ありませんが、
より安全性を高めたい場合はZodバリデーションを追加することも検討してください。

```typescript
// app/(app)/users/_apis/users.client.ts
import type { GetUserResponse } from "@/types";

/**
 * ユーザー情報を取得
 */
export async function getUser(userId: string): Promise<GetUserResponse> {
  try {
    // Route Handlerを呼び出す
    const response = await fetch(`/api/users/${userId}`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    });

    // ✅ 型アサーションのみ（Route Handlerで既にバリデーション済み）
    const data = await response.json() as GetUserResponse;

    if (!response.ok || !data?.success) {
      return {
        success: false,
        error: data?.error || `ユーザー取得に失敗しました (${response.status})`,
      };
    }

    return data;
  } catch (error) {
    console.error("[EXCEPTION] ユーザー取得エラー:", error);
    return {
      success: false,
      error: "予期しないエラーが発生しました",
    };
  }
}

/**
 * 商品一覧を取得
 */
export async function getProducts(params?: {
  page?: number;
  perPage?: number;
  category?: string;
}): Promise<GetProductsResponse> {
  try {
    const searchParams = new URLSearchParams();
    if (params?.page) searchParams.set('page', params.page.toString());
    if (params?.perPage) searchParams.set('per_page', params.perPage.toString());
    if (params?.category) searchParams.set('category', params.category);

    const response = await fetch(`/api/products?${searchParams.toString()}`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    });

    const data = await response.json() as GetProductsResponse;

    if (!response.ok || !data?.success) {
      return {
        success: false,
        error: data?.error || `商品一覧取得に失敗しました (${response.status})`,
      };
    }

    return data;
  } catch (error) {
    console.error("[EXCEPTION] 商品一覧取得エラー:", error);
    return {
      success: false,
      error: "予期しないエラーが発生しました",
    };
  }
}
```

#### 5.5.2 実装パターン（外部APIを直接呼び出す場合）

外部APIを直接呼び出す場合は、**Zodバリデーション必須**です。

```typescript
// src/apis/external-api.ts
import { GetUserResponseSchema, ApiErrorResponseSchema } from '@/types/schemas';
import type { GetUserResponse } from '@/types/schemas';

/**
 * 外部APIから直接ユーザー情報を取得
 * （Route Handlerを経由しない場合）
 */
export async function fetchUserFromExternalApi(userId: string): Promise<GetUserResponse> {
    const apiUrl = process.env.NEXT_PUBLIC_EXTERNAL_API_URL;
    const apiKey = process.env.NEXT_PUBLIC_API_KEY;

    const response = await fetch(`${apiUrl}/v1/users/${userId}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'X-API-Key': apiKey || '',
        },
    });

    if (!response.ok) {
        const errorJson = await response.json();
        
        // ✅ エラーレスポンスをzodでバリデーション
        const errorResult = ApiErrorResponseSchema.safeParse(errorJson);
        
        let errorMessage = 'ユーザー取得に失敗しました';
        if (errorResult.success) {
            errorMessage = errorResult.data.message;
        }
        
        return {
            success: false,
            error: errorMessage,
        };
    }

    const jsonData = await response.json();
    
    // ✅ 成功レスポンスをzodでバリデーション（信頼境界）
    const result = GetUserResponseSchema.safeParse(jsonData);
    
    if (!result.success) {
        console.error('ユーザー情報レスポンスのバリデーションエラー:', result.error);
        return {
            success: false,
            error: `レスポンスの形式が不正です: ${result.error.message}`,
        };
    }
    
    return result.data; // 型安全なデータ
}

/**
 * 外部APIで注文を作成
 */
export async function createOrderInExternalApi(orderData: CreateOrderRequest): Promise<CreateOrderResponse> {
    const apiUrl = process.env.NEXT_PUBLIC_EXTERNAL_API_URL;
    const apiKey = process.env.NEXT_PUBLIC_API_KEY;

    const response = await fetch(`${apiUrl}/v1/orders`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-API-Key': apiKey || '',
        },
        body: JSON.stringify(orderData),
    });

    if (!response.ok) {
        const errorJson = await response.json();
        const errorResult = ApiErrorResponseSchema.safeParse(errorJson);
        
        let errorMessage = '注文作成に失敗しました';
        if (errorResult.success) {
            errorMessage = errorResult.data.message;
        }
        
        return {
            success: false,
            error: errorMessage,
        };
    }

    const jsonData = await response.json();
    
    // ✅ zodでレスポンスをバリデーション
    const result = CreateOrderResponseSchema.safeParse(jsonData);
    
    if (!result.success) {
        console.error('注文作成レスポンスのバリデーションエラー:', result.error);
        return {
            success: false,
            error: `レスポンスの形式が不正です: ${result.error.message}`,
        };
    }
    
    return result.data;
}
```

### 5.6 safeParse() vs parse()

Zodでバリデーションを実行する際は、**必ず `safeParse()` を使用**してください。

#### 5.6.1 safeParse()（✅ 推奨）

```typescript
// ✅ 良い例：safeParse()を使用
const result = Schema.safeParse(jsonData);

if (!result.success) {
    // エラーハンドリング
    console.error('バリデーションエラー:', result.error);
    return { success: false, error: result.error.message };
}

// 成功時のデータ
const data = result.data;
```

**メリット**:
- 例外を投げない（エラーハンドリングが容易）
- `result.success` でバリデーションの成功/失敗を判定
- `result.data` でバリデーション済みのデータにアクセス
- `result.error` で詳細なエラー情報にアクセス

#### 5.6.2 parse()（❌ 非推奨）

```typescript
// ❌ 悪い例：parse()を使用（例外が投げられる）
try {
    const data = Schema.parse(jsonData);
    // 成功時の処理
} catch (error) {
    // エラーハンドリングが複雑になる
    console.error('バリデーションエラー:', error);
}
```

**デメリット**:
- バリデーションエラー時に例外を投げる
- try-catchが必須
- エラーハンドリングが複雑になる

### 5.7 アーキテクチャ図

```
┌─────────────────────────────────────────┐
│ 外部API (Supabase / FastAPI)           │
└───────────────┬─────────────────────────┘
                │
                │ fetch
                ↓
┌─────────────────────────────────────────┐
│ Route Handler                           │
│  ✅ zodバリデーション（safeParse）     │
│  (信頼境界)                             │
└───────────────┬─────────────────────────┘
                │
                │ 内部通信
                ↓
┌─────────────────────────────────────────┐
│ Client API                              │
│  ✅ 型アサーション (as Type)           │
│  または zodバリデーション               │
└───────────────┬─────────────────────────┘
                │
                ↓
┌─────────────────────────────────────────┐
│ Component                               │
└─────────────────────────────────────────┘
```

### 5.8 良い例と悪い例

#### 5.8.1 Route Handlerでの実装

```typescript
// ❌ 悪い例：zodバリデーションを省略（危険）
export async function GET(request: NextRequest) {
    const response = await fetch(externalApiUrl);
    const data = await response.json(); // バリデーションなし
    
    // 不正なデータ構造でもそのまま処理される危険性
    return NextResponse.json(data);
}

// ✅ 良い例：zodバリデーションを実施
export async function GET(request: NextRequest) {
    const response = await fetch(externalApiUrl);
    const jsonData = await response.json();
    
    // zodでバリデーション
    const result = ApiResponseSchema.safeParse(jsonData);
    
    if (!result.success) {
        return NextResponse.json(
            { success: false, error: `レスポンスの形式が不正です: ${result.error.message}` },
            { status: 500 }
        );
    }
    
    return NextResponse.json(result.data);
}
```

#### 5.8.2 Client APIでの実装

```typescript
// ❌ 悪い例：バリデーションなしで型アサーションのみ（脆弱）
export async function callApi() {
    const response = await fetch('/api/external-api');
    
    // バリデーションなしで型アサーション（危険）
    const data = await response.json() as ApiResponse;
    
    return data;
}

// ✅ 良い例：Route Handler経由の場合は型アサーションで十分（Route Handlerでバリデーション済み）
export async function callApi() {
    const response = await fetch('/api/route-handler');
    
    // Route Handlerで既にバリデーション済み
    const data = await response.json() as ApiResponse;
    
    if (!data?.success) {
        return { success: false, error: data?.error || "エラーが発生しました" };
    }
    
    return data;
}

// ✅ より良い例：Route Handler経由でも二重チェックで安全性を高める
export async function callApi() {
    const response = await fetch('/api/route-handler');
    const jsonData = await response.json();
    
    // Route Handlerでバリデーション済みだが、二重チェックでより安全に
    const result = ApiResponseSchema.safeParse(jsonData);
    
    if (!result.success) {
        console.error('予期しないレスポンス形式:', result.error);
        return { success: false, error: 'レスポンスの形式が不正です' };
    }
    
    return result.data;
}
```

### 5.9 バリデーション規約まとめ

| 場所 | 通信先 | バリデーション方法 | 理由 |
|------|--------|-------------------|------|
| **Route Handler** | 外部API | zodバリデーション（safeParse） ✅ | 信頼境界 |
| **Client API** | 外部API | zodバリデーション（safeParse） ✅ | 信頼境界 |
| **Client API** | Route Handler | 型アサーション（as Type） または zodバリデーション | 通常は型アサーションで十分だが、より安全性を高めたい場合はzodも検討 |
| **Server Action** | Edge Function | zodバリデーション（safeParse） ✅ | 信頼境界 |
| **Component** | Server Action | zodバリデーション推奨 | 型安全性をより確実にするため |

### 5.10 メリット

1. **型安全性**: TypeScriptの型チェックとランタイムバリデーションの両方を実現
2. **エラー検出**: 予期しないレスポンス形式を早期に検出
3. **ドキュメント化**: スキーマ定義がAPIレスポンスの仕様書として機能
4. **開発者体験**: IDEの補完が効き、バグを未然に防げる
5. **保守性**: スキーマ定義が一元化され、変更時の影響範囲が明確
6. **安全性**: 基本的にバリデーションを実施することで、予期しない不具合を防止

---

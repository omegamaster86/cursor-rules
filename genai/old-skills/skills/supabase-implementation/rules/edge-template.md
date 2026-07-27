---
title: Edge Functions Template
impact: HIGH
impactDescription: Edge Functions の基本ひな形
tags: supabase, edge-functions, deno
---

## Edge Functions Template

Edge Functions の基本的なひな形です。共有モジュール（`_shared/`）を活用して、統一されたレスポンス・認証・ロギングを実現します。

**基本ひな形：**

```typescript
import { getAuthUser } from "@shared/auth.ts";
import { createLogger } from "@shared/logger.ts";
import {
  createAuthErrorResponse,
  createErrorResponse,
  createMethodNotAllowedResponse,
  createSuccessResponse,
} from "@shared/response.ts";
import { createAuthenticatedClient } from "@shared/supabase.ts";
import { getAuthHeader, validateMethod } from "@shared/validation.ts";

/**
 * Edge Function の説明
 * 何をするFunctionかを記載
 */

Deno.serve(async (req) => {
  // 構造化ロガーを作成（関数名を指定）
  const logger = createLogger("function-name");

  // 処理開始ログ
  logger.start({ method: req.method, url: req.url });

  try {
    // HTTPメソッドを制限（許可するメソッドを指定）
    if (!validateMethod(req, ["GET"])) {
      logger.warn("無効なHTTPメソッド", { method: req.method });
      logger.end({ success: false, errorMessage: "Method not allowed" });
      return createMethodNotAllowedResponse();
    }

    // 認証トークンを取得
    const authHeader = getAuthHeader(req);
    if (!authHeader) {
      logger.warn("Authorizationヘッダーが見つかりません");
      logger.end({ success: false, errorMessage: "Missing auth header" });
      return createAuthErrorResponse();
    }

    // Supabaseクライアントに認証トークンを設定
    const supabaseWithAuth = createAuthenticatedClient(authHeader);

    // 認証ユーザー情報を取得
    const authResult = await getAuthUser(supabaseWithAuth);
    if (!authResult.success || !authResult.user) {
      logger.warn("認証エラー", { error: authResult.error });
      logger.end({ success: false, errorMessage: authResult.error });
      return createAuthErrorResponse(authResult.error);
    }

    // 認証ユーザーのUUIDを使用
    const authUserId = authResult.user.id;

    // Database Function 呼び出し
    const { data, error } = await supabaseWithAuth.rpc("sel_xxx", {
      target_auth_user_id: authUserId,
    });

    if (error) {
      logger.error(error, {
        function: "sel_xxx",
        authUserId,
      });
      logger.end({ success: false, errorMessage: error.message });
      return createErrorResponse(error.message, 500);
    }

    logger.info("処理成功", {
      authUserId,
      count: data?.length || 0,
    });
    logger.end({ success: true });

    // 成功レスポンス
    return createSuccessResponse(data || []);
  } catch (err) {
    logger.error(err, { context: "Unexpected error" });
    logger.end({ success: false, errorMessage: "サーバーエラー" });
    return createErrorResponse("サーバーエラーが発生しました");
  }
});
```

**共有モジュールの役割：**

| モジュール | 役割 |
|-----------|------|
| `@shared/auth.ts` | 認証ユーザー情報の取得 |
| `@shared/logger.ts` | 構造化ロギング |
| `@shared/response.ts` | 統一されたレスポンス生成 |
| `@shared/supabase.ts` | Supabase クライアント生成 |
| `@shared/validation.ts` | リクエストバリデーション |

**チェックリスト：**

- [ ] 共有モジュールからインポート
- [ ] `createLogger` でロガーを初期化（関数名を指定）
- [ ] `validateMethod` で HTTP メソッドを制限
- [ ] `getAuthHeader` + `createAuthenticatedClient` で認証
- [ ] `getAuthUser` でユーザー情報取得
- [ ] `createSuccessResponse` / `createErrorResponse` でレスポンス生成
- [ ] `logger.start()` / `logger.end()` で処理時間を記録

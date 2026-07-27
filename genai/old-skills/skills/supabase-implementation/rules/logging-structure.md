---
title: Structured Logger
impact: HIGH
impactDescription: 構造化ログ（logger.ts）の詳細
tags: supabase, edge-functions, logging
---

## Structured Logger

`logger.ts` は Supabase Edge Functions（Deno）向けの軽量な構造化ロガーです。

**主な機能：**

- リクエストごとの一意な `requestId` 生成
- 構造化 JSON ログ出力
- センシティブデータの自動マスキング
- JWT からのユーザー ID 抽出
- 処理時間の自動計測

**ログに含まれる情報：**

| 情報 | 必須 | 説明 |
|------|------|------|
| `requestId` | ✅ | リクエスト全体を追跡するための一意ID |
| `ts` | ✅ | ログ出力時刻（ISO 8601形式） |
| `level` | ✅ | ログレベル（info/warn/error） |
| `message` | ✅ | 何が起きたかの簡潔な説明 |
| `userId` | 推奨 | 認証済みユーザーのID |
| `method` / `path` | 推奨 | HTTPメソッドとパス |
| `durationMs` | 推奨 | 処理時間（終了ログ） |
| `status` | 推奨 | HTTPステータスコード |
| `recordCount` | 推奨 | レスポンスのレコード件数 |
| `affectedCount` | 推奨 | INSERT/UPDATE/DELETEで影響を受けた件数 |

**使用例：**

```typescript
import { createRequestLogger } from "../_shared/logger.ts";

Deno.serve(async (req) => {
  const logger = await createRequestLogger(req);

  // リクエスト開始ログ
  logger.LoggingStart({ function: "get-user-data" });

  try {
    // 処理中のログ
    logger.LoggingInfo("処理中", { step: "validation" });

    // Database Function 呼び出し
    const { data, error } = await supabase.rpc("sel_xxx");

    if (error) {
      logger.LoggingError(error, { function: "sel_xxx" });
      logger.LoggingEnd(500, { errorMessage: error.message });
      return new Response(JSON.stringify({ error: error.message }), { status: 500 });
    }

    // 成功時
    logger.LoggingInfo("処理完了", { recordCount: data?.length || 0 });
    logger.LoggingEnd(200);
    return new Response(JSON.stringify({ success: true, data }), { status: 200 });
  } catch (err) {
    // エラーログ
    logger.LoggingError(err, { context: "main process" });
    logger.LoggingEnd(500, { errorMessage: err.message });
    return new Response(JSON.stringify({ error: "Internal error" }), { status: 500 });
  }
});
```

**センシティブデータの自動マスキング：**

以下のキーは自動的にマスキングされます（`***` に置換）：

- `password`, `pass`, `pwd`
- `email`, `lastName`, `firstName`
- `postalCode1`, `postalCode2`, `prefecture`, `city`, `address`, `building`
- `phone`, `tel`
- `token`, `access_token`, `refresh_token`, `authorization`, `auth`, `jwt`

**環境変数でマスキング対象を追加：**

```bash
MASK_TARGETS='["custom_field", "secret_key"]'
```

**logger メソッド一覧：**

| メソッド | 用途 |
|----------|------|
| `LoggingStart(meta?)` | 処理開始 |
| `LoggingEnd(status, meta?)` | 処理終了 |
| `LoggingInfo(message, meta?)` | 情報ログ |
| `LoggingWarn(message, meta?)` | 警告ログ |
| `LoggingError(err, meta?)` | エラーログ |

> ⚠️ **レスポンス内容のログ出力について**: Supabase Edge Functions ではレスポンスボディは**自動的にはログ出力されません**。障害調査のためにレスポンス内容を確認したい場合は、明示的に `LoggingInfo` で出力する必要があります。

**チェックリスト：**

- [ ] `createRequestLogger` でロガーを初期化
- [ ] `LoggingStart()` でリクエスト開始を記録
- [ ] `LoggingEnd()` でステータスコードと処理終了を記録
- [ ] エラー時は `LoggingError()` でスタックトレースを含めて記録
- [ ] センシティブデータがログに含まれていないか確認

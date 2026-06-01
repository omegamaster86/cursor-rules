---
title: Required Logging
impact: HIGH
impactDescription: Edge Functions での必須ログ出力
tags: supabase, logging, debugging
---

## Required Logging

Edge Functions でのログ出力は**必須**です。`@shared/logger.ts` の `createLogger` を使用して構造化ログを出力します。

**ログをつけるべき箇所：**

| 箇所 | メソッド | 目的 |
|------|----------|------|
| リクエスト開始時 | `logger.start()` | リクエストの追跡開始 |
| リクエスト終了時 | `logger.end()` | 処理時間、成否の記録 |
| Database Function 呼び出し後 | `logger.info()` / `logger.error()` | DB処理の成否 |
| 外部API呼び出し後 | `logger.info()` / `logger.error()` | 外部連携の成否 |
| 認証・認可処理 | `logger.info()` / `logger.warn()` | 認証成功/失敗 |
| バリデーションエラー | `logger.warn()` | 不正な入力の検知 |
| 例外発生時 | `logger.error()` | エラー原因の特定 |

**ログに自動で含まれる情報：**

| 情報 | 説明 |
|------|------|
| `requestId` | リクエスト追跡用の一意ID（自動生成） |
| `ts` | ログ出力時刻（ISO 8601） |
| `level` | ログレベル |
| `action` | 関数名（createLogger の引数） |
| `durationMs` | 処理時間（end() で自動計算） |

**基本的なログ出力例：**

```typescript
import { createLogger } from "@shared/logger.ts";

Deno.serve(async (req) => {
  // 構造化ロガーを作成（関数名を指定）
  const logger = createLogger("function-name");

  // 処理開始ログ
  logger.start({ method: req.method, url: req.url });

  try {
    // Database Function 呼び出し
    const { data, error } = await supabase.rpc("sel_xxx");

    if (error) {
      // エラーログ（エラーオブジェクトとメタデータを渡す）
      logger.error(error, {
        function: "sel_xxx",
      });
      logger.end({ success: false, errorMessage: error.message });
      // ...
    }

    // 成功ログ
    logger.info("処理成功", {
      function: "sel_xxx",
      recordCount: data?.length || 0,
    });
    logger.end({ success: true });
    // ...
  } catch (err) {
    // 例外ログ（スタックトレースは自動で含まれる）
    logger.error(err, { context: "Unexpected error" });
    logger.end({ success: false, errorMessage: "サーバーエラー" });
    // ...
  }
});
```

**logger メソッド一覧：**

| メソッド | 用途 | 引数 |
|----------|------|------|
| `start(meta?)` | 処理開始 | オプションでメタデータ |
| `end(meta?)` | 処理終了 | `{ success: boolean, errorMessage?: string }` |
| `info(message, meta?)` | 情報ログ | メッセージとメタデータ |
| `warn(message, meta?)` | 警告ログ | メッセージとメタデータ |
| `error(err, meta?)` | エラーログ | エラーオブジェクトとメタデータ |

**⚠️ センシティブデータの自動マスキング：**

`createLogger` はセンシティブなキー（password, token, email など）を自動でマスキングします。追加のマスキングが必要な場合は、ログ出力前に手動でデータを加工してください。

**チェックリスト：**

- [ ] `createLogger` で関数名を指定してロガーを初期化
- [ ] `logger.start()` でリクエスト開始を記録
- [ ] `logger.end()` で処理終了を記録（success フラグ必須）
- [ ] Database Function 呼び出し結果を `logger.info()` / `logger.error()` で記録
- [ ] 例外発生時は `logger.error(err)` でスタックトレースを含めて記録

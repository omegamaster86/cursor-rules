# Supabase 実装ガイド（分割）: ログ出力

### 2.5 ログ出力（必須）

**重要な原則**:
- 障害時の原因調査のためにログ出力は**必ず実装**する
- どんなに簡単な機能でもバックエンドでログが出ないアーキテクチャーにしない

#### ログをつけるべき箇所

| 箇所 | ログレベル | 目的 |
|------|-----------|------|
| リクエスト開始時 | INFO | リクエストの追跡開始、パラメータの記録 |
| リクエスト終了時 | INFO | 処理時間、ステータスコードの記録 |
| レスポンス送信時 | INFO | レスポンス内容の記録（※自動出力されないため明示的に出力） |
| Database Function 呼び出し前後 | INFO/ERROR | DB処理の成否、実行時間の把握 |
| DB更新操作（INSERT/UPDATE/DELETE）後 | INFO | 影響を受けた件数の記録（データ整合性の確認） |
| 外部API呼び出し前後 | INFO/ERROR | 外部連携の成否、レスポンス時間の把握 |
| 認証・認可処理 | INFO/WARN | 認証成功/失敗、権限チェック結果 |
| 重要なビジネスロジックの分岐点 | INFO | 処理フローの追跡 |
| バリデーションエラー | WARN | 不正な入力の検知 |
| 業務エラー（想定済みの例外） | WARN | 在庫不足、重複登録、権限不足など想定されたエラー |
| 例外発生時（想定外のエラー） | ERROR | エラー原因の特定（スタックトレース含む） |
| リトライ処理 | WARN | リトライ回数、失敗理由 |

#### ログに含めるべき情報

| 情報 | 必須 | 説明 |
|------|------|------|
| `requestId` | ✅ | リクエスト全体を追跡するための一意ID |
| `timestamp` | ✅ | ログ出力時刻（ISO 8601形式） |
| `level` | ✅ | ログレベル（info/warn/error） |
| `message` | ✅ | 何が起きたかの簡潔な説明 |
| `userId` | 推奨 | 認証済みユーザーのID |
| `method` / `path` | 推奨 | HTTPメソッドとパス |
| `durationMs` | 推奨 | 処理時間（終了ログ） |
| `status` | 推奨 | HTTPステータスコード（終了ログ） |
| `recordCount` | 推奨 | レスポンスのレコード件数（一覧取得時） |
| `affectedCount` | 推奨 | INSERT/UPDATE/DELETEで影響を受けた件数 |
| `responseSize` | 任意 | レスポンスサイズ（バイト数、大きなデータの場合） |
| `error` | 条件 | エラー時のエラー情報 |

> ⚠️ **レスポンス内容のログ出力について**: Supabase Edge Functions ではレスポンスボディは**自動的にはログ出力されません**。障害調査のためにレスポンス内容を確認したい場合は、明示的に `console.log` で出力する必要があります。ただし、センシティブデータが含まれる場合はマスキングするか、レコード件数などの要約情報のみを出力してください。

> 💡 **注意**: センシティブデータ（パスワード、トークン、個人情報など）はログに出力しないか、マスキングすること。`logger.ts` を使用すると自動的にマスキングされます。

#### サンプルコード（基本形）

```typescript
Deno.serve(async (req) => {
  // リクエスト情報をログ出力
  console.log("[START] Function called", {
    method: req.method,
    url: req.url,
    timestamp: new Date().toISOString(),
  });

  try {
    const { data, error } = await supabase.rpc("function_name");

    if (error) {
      console.error("[ERROR] Database function failed", {
        function: "function_name",
        error: error.message,
        timestamp: new Date().toISOString(),
      });
      return new Response(JSON.stringify({ error: error.message }), {
        headers: { "Content-Type": "application/json" },
        status: 500,
      });
    }

    console.log("[SUCCESS] Function completed", {
      function: "function_name",
      recordCount: data?.length || 0,
      timestamp: new Date().toISOString(),
    });

    return new Response(JSON.stringify(data), {
      headers: { "Content-Type": "application/json" },
      status: 200,
    });
  } catch (err) {
    console.error("[EXCEPTION] Unexpected error", {
      error: err.message,
      stack: err.stack,
      timestamp: new Date().toISOString(),
    });
    return new Response(JSON.stringify({ error: "Internal server error" }), {
      headers: { "Content-Type": "application/json" },
      status: 500,
    });
  }
});
```

---
title: Edge Function Calls
impact: CRITICAL
impactDescription: Edge Function 呼び出しとレスポンス検証
tags: supabase, edge-functions, flutter
---

## Edge Function Calls

Repository から `functions.invoke` を呼ぶ。

**検証（実装準拠）:**

- HTTP status >= 400 で失敗（`EdgeFunctionException.fromResponse`）
- JSON body の `success == true` 文字列チェックは **必須ではない**（lib 全体で未使用の例あり）
- 成功時は body を Freezed / json_serializable でパース

Web 側の `{ success, data }` 契約と揃える場合はパース時に確認してよいが、mobile starter の正例は status ベース。

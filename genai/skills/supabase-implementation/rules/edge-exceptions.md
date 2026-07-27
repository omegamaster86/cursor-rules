---
title: Edge Function Exceptions
impact: HIGH
impactDescription: handler を使わない特殊 Edge（webhook / cron / health）
tags: supabase, edge-functions, webhook, cron
---

## Edge Function Exceptions

次のケースは `handler()` を使わず、独自エントリにしてよい。

| 種類 | 例 | 認証 | config.toml |
|------|-----|------|-------------|
| Stripe Webhook | `stripe-webhook` | Stripe 署名検証 | `verify_jwt = false` |
| Cron / バッチ | `create-amazon-giftcard-for-admin` | `x-cron-key` + `CRON_KEY` | `verify_jwt = false` |
| Health | `health` | なし | 公開 200 |

**注意：**

- `verify_jwt = false` は最小限。代替の署名 / 共有鍵検証を必ず実装する
- CORS 用 secret（`EDGE_FUNCTION_ALLOWED_ORIGIN`）は現行 Edge 実装では未使用。Server からの呼び出しが前提なら CORS 処理は不要
- 例外系でも構造化ログ（`createRequestLogger`）と統一エラー形状を可能な範囲で合わせる

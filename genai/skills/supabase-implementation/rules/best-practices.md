---
title: Supabase Best Practices
impact: HIGH
impactDescription: Supabase 実装のベストプラクティス
tags: supabase, best-practices
---

## Supabase Best Practices

### Database Functions

| 推奨 | 説明 |
|------|------|
| ✅ | CRUD・複雑 SQL は Database Functions（`schemas/functions/`） |
| ✅ | 命名は `sel_` / `ins_` / `upd_` / `del_` |
| ✅ | 機密・RLS バイパスが必要な関数は `SECURITY DEFINER` + `search_path` |
| ℹ️ | 全関数必須の DEFINER / GRANT EXECUTE ではない（ToDo RPC 等は非 DEFINER の例あり） |
| ℹ️ | GRANT は `04_grants.sql` + 関数単位の例外 |

### Edge Functions — 二段ルール

| パターン | 方針 |
|----------|------|
| 標準 CRUD | `handler` + `ctx.callRpc`（RPC 優先） |
| オーケストレーション（Stripe / FCM 等） | `createServiceRoleClient().from(...)` 可。所有権・認可・ログ必須 |

### Edge 共通

| 推奨 | 説明 |
|------|------|
| ✅ | `handler()` + Zod（`_shared/schemas`） |
| ✅ | ログは handler / `createRequestLogger` |
| ✅ | `npm run sb:types:gen` で型同期 |
| ✅ | 日付は可能な限りクライアントから渡す（`new Date()` サーバー生成は避ける） |
| ❌ | 機密のハードコード |
| ❌ | 旧 API（`getUser` 必須 / `createSuccessResponse` 等） |

### データアクセス階層

```
Client → Edge（handler） → DB Function または service_role オーケストレーション → DB
```

### 認証

| ルール | 説明 |
|--------|------|
| 標準 | `handler` → `getClaims` |
| 管理者 | `requireAdmin: true` |

### チェックリスト

- [ ] 新規変更は `schemas/` + `db diff`
- [ ] 標準 API は `handler()`
- [ ] service_role `.from()` には認可根拠がある
- [ ] 型を再生成した

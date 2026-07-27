---
title: RLS Policies
impact: CRITICAL
impactDescription: Row Level Security ポリシーの設定
tags: supabase, security, rls, postgresql
---

## RLS Policies

**基本原則：**

- すべてのテーブルで RLS を有効化
- 正本は `backend/supabase/schemas/rls/`（例: `policies.sql`）
- GRANT は `schemas/04_grants.sql` で anon / authenticated / service_role に明示
- 最小権限。`service_role` の使用はオーケストレーションに限定

**ヘルパー（実装準拠）：**

```sql
-- schemas/03_auth_helpers.sql 等
-- get_current_user_id()
-- is_admin()
```

ポリシー例では単純な `auth.uid() = id` より、プロジェクトのヘルパーを使う。

**service_role：**

- JWT クレーム / 専用ポリシーがある場合は `schemas/rls` を参照
- service_role クライアントは RLS をバイパスしうる → Edge 側で所有権チェックを徹底

**チェックリスト：**

- [ ] 新テーブルに RLS 有効化
- [ ] `schemas/rls` と `04_grants.sql` を更新
- [ ] admin / ユーザー分離に `is_admin()` 等を使っている

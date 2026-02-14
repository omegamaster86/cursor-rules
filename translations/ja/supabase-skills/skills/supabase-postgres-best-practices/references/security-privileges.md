---
title: 最小権限の原則を適用する
impact: MEDIUM
impactDescription: 攻撃面を縮小し、監査性を向上
tags: privileges, security, roles, permissions
---

## 最小権限の原則を適用する

必要最小限の権限だけを付与します。アプリケーションクエリに superuser を使ってはいけません。

**誤り（過剰な権限付与）:**

```sql
-- Application uses superuser connection
-- Or grants ALL to application role
grant all privileges on all tables in schema public to app_user;
grant all privileges on all sequences in schema public to app_user;

-- Any SQL injection becomes catastrophic
-- drop table users; cascades to everything
```

**正しい例（最小かつ限定的な権限）:**

```sql
-- Create role with no default privileges
create role app_readonly nologin;

-- Grant only SELECT on specific tables
grant usage on schema public to app_readonly;
grant select on public.products, public.categories to app_readonly;

-- Create role for writes with limited scope
create role app_writer nologin;
grant usage on schema public to app_writer;
grant select, insert, update on public.orders to app_writer;
grant usage on sequence orders_id_seq to app_writer;
-- No DELETE permission

-- Login role inherits from these
create role app_user login password 'xxx';
grant app_writer to app_user;
```

public への既定権限を取り消す:

```sql
-- Revoke default public access
revoke all on schema public from public;
revoke all on all tables in schema public from public;
```

Reference: [Roles and Privileges](https://supabase.com/blog/postgres-roles-and-privileges)

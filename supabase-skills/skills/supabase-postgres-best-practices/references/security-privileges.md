---
title: 最小権限の原則を適用する
impact: MEDIUM
impactDescription: 攻撃面を縮小し監査性を向上
tags: privileges, security, roles, permissions
---

## 最小権限の原則を適用する

必要最小限の権限だけを付与してください。アプリのクエリにスーパーユーザーは絶対に使わないでください。

**Incorrect (過剰な権限):**

```sql
-- アプリがスーパーユーザー接続
-- あるいはアプリロールに ALL を付与
grant all privileges on all tables in schema public to app_user;
grant all privileges on all sequences in schema public to app_user;

-- SQL インジェクションが致命的になる
-- drop table users; が全体に波及
```

**Correct (最小限で具体的な権限):**

```sql
-- デフォルト権限なしのロールを作成
create role app_readonly nologin;

-- 特定テーブルに SELECT のみ付与
grant usage on schema public to app_readonly;
grant select on public.products, public.categories to app_readonly;

-- 書き込み用ロールは範囲を限定
create role app_writer nologin;
grant usage on schema public to app_writer;
grant select, insert, update on public.orders to app_writer;
grant usage on sequence orders_id_seq to app_writer;
-- DELETE 権限は付与しない

-- ログインロールがこれらを継承
create role app_user login password 'xxx';
grant app_writer to app_user;
```

public のデフォルト権限を撤回:

```sql
-- public のデフォルトアクセスを無効化
revoke all on schema public from public;
revoke all on all tables in schema public from public;
```

Reference: [Roles and Privileges](https://supabase.com/blog/postgres-roles-and-privileges)

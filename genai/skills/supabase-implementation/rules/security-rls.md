---
title: RLS Policies
impact: CRITICAL
impactDescription: Row Level Security ポリシーの設定
tags: supabase, security, rls, postgresql
---

## RLS Policies

Row Level Security（RLS）は Supabase でデータアクセスを制御するための重要な機能です。

**基本原則：**

- ✅ すべてのテーブルで RLS を有効化
- ✅ Edge Functions 用のポリシーを設定
- ✅ 最小権限の原則に従う
- ❌ `service_role` キーを不用意に使用しない

**RLS の有効化：**

```sql
-- テーブルに RLS を有効化
alter table public.users enable row level security;
```

**基本的なポリシーの例：**

```sql
-- 自分のデータのみ SELECT 可能
create policy "Users can view own data"
on public.users
for select
using (auth.uid() = id);

-- 自分のデータのみ UPDATE 可能
create policy "Users can update own data"
on public.users
for update
using (auth.uid() = id);

-- 認証済みユーザーのみ INSERT 可能
create policy "Authenticated users can insert"
on public.users
for insert
with check (auth.uid() = id);
```

**Edge Functions 用のポリシー：**

Edge Functions が `anon` キーを使用する場合：

```sql
-- anon キーでアクセス可能なポリシー
create policy "Public read access"
on public.public_data
for select
using (true);
```

Edge Functions が `service_role` キーを使用する場合：

```sql
-- service_role は RLS をバイパスするため、ポリシー不要
-- ただし、service_role の使用は最小限に
```

**ポリシーの確認項目：**

| 確認項目 | 説明 |
|----------|------|
| RLS 有効化 | テーブルに RLS が有効化されているか |
| SELECT ポリシー | 読み取り権限が適切か |
| INSERT ポリシー | 登録権限が適切か |
| UPDATE ポリシー | 更新権限が適切か |
| DELETE ポリシー | 削除権限が適切か |

**よくある問題：**

> 💡 **Edge Functions が正常に動作しない場合**:
>
> Supabase 側でテーブルの policy を確認してください。対応する policy がない場合、Edge Functions が正常に動作しません。

**チェックリスト：**

- [ ] すべてのテーブルで RLS が有効化されている
- [ ] 必要な操作（SELECT/INSERT/UPDATE/DELETE）にポリシーが設定されている
- [ ] 最小権限の原則に従っている
- [ ] `service_role` キーの使用は必要最小限
- [ ] ポリシーの条件が適切（`auth.uid()` の使用など）

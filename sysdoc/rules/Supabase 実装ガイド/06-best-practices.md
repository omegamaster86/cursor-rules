# Supabase 実装ガイド（分割）: ベストプラクティス

## 4. ベストプラクティス

### 4.1 Database Functions

- ✅ 複雑なクエリは Database Functions にまとめる
- ✅ トランザクションが必要な処理は Functions で実装
- ✅ 関数名は用途が分かりやすい名前にする
- ✅ 引数と戻り値の型を明確に定義する
- ❌ 単純な SELECT は直接 Supabase Client から実行する方が効率的

### 4.2 Edge Functions

- ✅ 必ずログ出力を実装する
- ✅ エラーハンドリングを適切に行う
- ✅ CORS 設定を適切に行う
- ✅ 環境変数を使用して設定を管理
- ✅ `database.types.ts` から型定義をインポートして型安全性を確保する
- ✅ `Database` 型と `Tables` 型を使用して型を定義する
- ✅ データベーススキーマ変更後は必ず `database.types.ts` を再生成する
- ✅ 日付を使用する場合は、クライアントから引数として受け取る（`new Date()` をサーバー内部で生成しない）
- ❌ 機密情報をコードにハードコーディングしない
- ❌ 型定義なしで `any` 型を使用しない
- ❌ サーバー内部で現在日時を生成しない（テスト容易性・再現性のため）

### 4.3 RLS ポリシー

- ✅ すべてのテーブルで RLS を有効化
- ✅ Edge Functions 用のポリシーを設定
- ✅ 最小権限の原則に従う
- ✅ RLS ポリシー内の関数呼び出しは `(SELECT ...)` でラップする（パフォーマンス最適化）
- ❌ `service_role` キーを不用意に使用しない

#### RLS パフォーマンス最適化

RLS ポリシーの書き方次第で性能が大きく変わります。

```sql
-- ❌ 悪い例: auth.uid() が各行で呼ばれる（100万行なら100万回実行）
create policy orders_policy on orders
  using (auth.uid() = user_id);

-- ✅ 良い例: SELECT でラップすると1回呼ばれてキャッシュされる（100x+ 高速）
create policy orders_policy on orders
  using ((select auth.uid()) = user_id);
```

複雑な権限チェックには `SECURITY DEFINER` 関数を使う:

```sql
-- ヘルパー関数（RLS をバイパスして内部で権限確認）
create or replace function is_team_member(p_team_id bigint)
returns boolean
language sql
security definer
set search_path = ''
as $$
  select exists (
    select 1 from public.team_members
    where team_id = p_team_id and user_id = (select auth.uid())
  );
$$;

-- ポリシーで使用
create policy team_orders_policy on orders
  using ((select is_team_member(team_id)));
```

### 4.4 スキーマ設計

#### データ型の選択

| 用途 | ❌ 避ける | ✅ 推奨 | 理由 |
|------|----------|---------|------|
| ID | `int` / `serial` | `bigint generated always as identity` | 21億制限回避、SQL標準 |
| 文字列 | `varchar(255)` | `text` | 不要な長さ制限なし、性能は同等 |
| 日時 | `timestamp` | `timestamptz` | タイムゾーン情報を保持 |
| フラグ | `varchar(5)` | `boolean` | 1バイトで型安全 |
| 金額 | `float` | `numeric(10,2)` | 正確な小数演算 |

```sql
-- ✅ 推奨されるテーブル定義
create table users (
  id bigint generated always as identity primary key,
  email text not null,
  display_name text,
  is_active boolean default true,
  created_at timestamptz default now()
);
```

#### 主キー戦略

- **単一DB**: `bigint generated always as identity`（連番、8バイト、SQL標準）
- **分散/公開ID**: UUIDv7（`pg_uuidv7` 拡張が必要、時間順で断片化しにくい）
- ❌ 大規模テーブルの主キーにランダム UUID (v4) を使わない（インデックス断片化の原因）

#### 識別子の命名

- ✅ テーブル名・カラム名は **小文字の snake_case** で統一する
- ❌ `"CamelCase"` のような引用符付き識別子を使わない（ツール/ORM/AI との互換性問題）

### 4.5 トランザクション管理

#### トランザクションを短く保つ

長時間のトランザクションはロックを保持し、他のクエリをブロックします。外部 API 呼び出しなどはトランザクション外で行ってください。

```sql
-- ❌ 悪い例: 外部呼び出しを含む長いトランザクション
begin;
select * from orders where id = 1 for update;  -- ロック取得
-- ここで支払い API に HTTP 呼び出し（2-5秒）→ 他のクエリがブロック
update orders set status = 'paid' where id = 1;
commit;

-- ✅ 良い例: API 呼び出しはトランザクション外、更新だけをロック下で実行
-- アプリ側: response = await paymentAPI.charge(...)
begin;
update orders set status = 'paid', payment_id = $1
where id = $2 and status = 'pending'
returning *;
commit;  -- ロックはミリ秒単位
```

#### デッドロック防止

複数行を更新する場合は、常に一貫した順序（例: ID昇順）でロックを取得してください。

```sql
-- ✅ ID 順で明示的にロック取得
begin;
select * from accounts where id in (1, 2) order by id for update;
update accounts set balance = balance - 100 where id = 1;
update accounts set balance = balance + 100 where id = 2;
commit;
```

### 4.6 データアクセスの階層構造

Next.js における Supabase のデータアクセスは、3層アーキテクチャ（Page Component → Server Action → Edge Function → DB Function）で実装することが推奨されます。詳細は以下のドキュメントを参照してください。

> 📖 **詳細**: [04\_コーディング規約\_Web.md](04_コーディング規約_Web.md) の「4. Supabaseデータアクセス規約」を参照

### 4.7 認証処理

Next.js における Supabase の認証処理（`getUser()`/`getSession()` の使い分け、Edge Function 呼び出し時の認証など）については、以下のドキュメントを参照してください。

> 📖 **詳細**: [04\_コーディング規約\_Web.md](04_コーディング規約_Web.md) の「3. Supabase 認証規約」を参照

---

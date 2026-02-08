# Supabase 実装ガイド（分割）: デプロイ/トラブルシューティング

### 2.6 デプロイ

開発が完了したらデプロイします。

```bash
# 基本コマンド
supabase functions deploy [開発したファンクション名] --project-ref [デプロイ先のプロジェクトID]

# 例
supabase functions deploy get-user-data --project-ref abcdefghijklmnop
```

### 2.7 トラブルシューティング

> 💡 **デプロイしたEdge Functionsが正常に動作しないとき**:
> 
> Supabase側でテーブルのpolicyを確認してください。対応するpolicyがない場合、Edge Functionsが正常に動作しません。

**確認項目**:
1. RLS（Row Level Security）が有効になっているか
2. `service_role` または `anon` キーに対するポリシーが設定されているか
3. Edge Functions が実行するクエリに必要な権限があるか

### 2.8 クエリパフォーマンスの診断（EXPLAIN ANALYZE）

Database Function やクエリが遅い場合、`EXPLAIN ANALYZE` で実行計画と実測時間を確認できます。

```sql
explain (analyze, buffers, format text)
select * from orders where customer_id = 123 and status = 'pending';
```

**出力の読み方（注目ポイント）**:

| シグナル | 意味 | 対処 |
|---------|------|------|
| `Seq Scan` on 大規模テーブル | テーブル全体を走査している | フィルタ条件や取得列の見直し |
| `Rows Removed by Filter` が多い | 絞り込みが弱い | WHERE 条件をより絞る |
| `Buffers: read >> hit` | キャッシュミスが多い | メモリ設定の見直し |
| `Nested Loop` の loops が多い | JOIN 戦略が非効率 | クエリの書き換えや JOIN 条件の見直し |

```sql
-- 出力例:
-- Seq Scan on orders (actual time=0.015..450.123 rows=50 loops=1)
--   Filter: ((customer_id = 123) AND (status = 'pending'))
--   Rows Removed by Filter: 999950        ← 大量の行を読み捨てている
--   Buffers: shared hit=5000 read=15000

-- → WHERE 条件の見直しや取得列の削減を検討
```

> 💡 **ヒント**: SQL Editor で `EXPLAIN ANALYZE` を実行し、`Seq Scan` が大規模テーブルに出ていないか確認する習慣をつけましょう。

---

---
title: 適切な接続上限を設定する
impact: CRITICAL
impactDescription: DB クラッシュやメモリ枯渇を防止
tags: connections, max-connections, limits, stability
---

## 適切な接続上限を設定する

接続数が多すぎるとメモリを消費し、性能が低下します。利用可能なリソースに応じた上限を設定してください。

**Incorrect (無制限/過剰な接続):**

```sql
-- デフォルト max_connections = 100 だが、よく根拠なく増やされる
show max_connections;  -- 500 (4GB RAM では多すぎ)

-- 1 接続あたり 1-3MB RAM を消費
-- 500 接続 * 2MB = 接続だけで 1GB
-- 負荷時にメモリ不足
```

**Correct (リソースに基づいて算出):**

```sql
-- 目安: max_connections = (RAM(MB) / 5MB/接続) - 予約分
-- 4GB RAM: (4096 / 5) - 10 = 理論上 ~800
-- ただし実運用では 100-200 程度がクエリ性能に有利

-- 4GB RAM の推奨設定例
alter system set max_connections = 100;

-- work_mem も適切に設定
-- work_mem * max_connections が RAM の 25% を超えないように
alter system set work_mem = '8MB';  -- 8MB * 100 = 最大 800MB
```

接続使用状況の監視:

```sql
select count(*), state from pg_stat_activity group by state;
```

Reference: [Database Connections](https://supabase.com/docs/guides/platform/performance#connection-management)

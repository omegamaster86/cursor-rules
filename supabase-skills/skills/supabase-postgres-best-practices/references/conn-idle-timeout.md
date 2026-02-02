---
title: アイドル接続のタイムアウトを設定する
impact: HIGH
impactDescription: アイドルクライアントの接続スロットを 30-50% 回収
tags: connections, timeout, idle, resource-management
---

## アイドル接続のタイムアウトを設定する

アイドル接続はリソースを浪費します。タイムアウトを設定して自動的に回収してください。

**Incorrect (接続が無期限に保持される):**

```sql
-- タイムアウト未設定
show idle_in_transaction_session_timeout;  -- 0 (無効)

-- アイドルでも接続がずっと残る
select pid, state, state_change, query
from pg_stat_activity
where state = 'idle in transaction';
-- 何時間もアイドルのトランザクションがロックを保持
```

**Correct (アイドル接続の自動クリーンアップ):**

```sql
-- トランザクション内アイドルを 30 秒で終了
alter system set idle_in_transaction_session_timeout = '30s';

-- 完全にアイドルな接続を 10 分で終了
alter system set idle_session_timeout = '10min';

-- 設定の再読み込み
select pg_reload_conf();
```

プール接続の場合は、プーラ側で設定します:

```ini
# pgbouncer.ini
server_idle_timeout = 60
client_idle_timeout = 300
```

Reference: [Connection Timeouts](https://www.postgresql.org/docs/current/runtime-config-client.html#GUC-IDLE-IN-TRANSACTION-SESSION-TIMEOUT)

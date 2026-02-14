---
title: アイドル接続タイムアウトを設定する
impact: HIGH
impactDescription: アイドルクライアントから接続枠を 30-50% 回収
tags: connections, timeout, idle, resource-management
---

## アイドル接続タイムアウトを設定する

アイドル接続はリソースを浪費します。タイムアウトを設定して自動回収します。

**誤り（接続を無期限に保持）:**

```sql
-- No timeout configured
show idle_in_transaction_session_timeout;  -- 0 (disabled)

-- Connections stay open forever, even when idle
select pid, state, state_change, query
from pg_stat_activity
where state = 'idle in transaction';
-- Shows transactions idle for hours, holding locks
```

**正しい例（アイドル接続の自動クリーンアップ）:**

```sql
-- Terminate connections idle in transaction after 30 seconds
alter system set idle_in_transaction_session_timeout = '30s';

-- Terminate completely idle connections after 10 minutes
alter system set idle_session_timeout = '10min';

-- Reload configuration
select pg_reload_conf();
```

プール接続では、プーラー側でも設定します:

```ini
# pgbouncer.ini
server_idle_timeout = 60
client_idle_timeout = 300
```

Reference: [Connection Timeouts](https://www.postgresql.org/docs/current/runtime-config-client.html#GUC-IDLE-IN-TRANSACTION-SESSION-TIMEOUT)

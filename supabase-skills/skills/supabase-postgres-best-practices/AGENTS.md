# supabase-postgres-best-practices

> **Note:** `CLAUDE.md` はこのファイルへのシンボリックリンクです。

## 概要

Supabase による Postgres のパフォーマンス最適化とベストプラクティス。Postgres のクエリ作成・レビュー・最適化、スキーマ設計、またはデータベース設定に取り組むときにこのスキルを使います。

## 構成

```
supabase-postgres-best-practices/
  SKILL.md       # メインのスキルファイル - まず読む
  AGENTS.md      # このナビゲーションガイド
  CLAUDE.md      # AGENTS.md へのシンボリックリンク
  references/    # 詳細な reference ファイル
```

## 使い方

1. `SKILL.md` を読んでメインの指示を把握
2. `references/` で特定トピックの詳細を参照
3. reference はオンデマンドで読む（必要なものだけ）

## Reference カテゴリ

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Query Performance | CRITICAL | `query-` |
| 2 | Connection Management | CRITICAL | `conn-` |
| 3 | Security & RLS | CRITICAL | `security-` |
| 4 | Schema Design | HIGH | `schema-` |
| 5 | Concurrency & Locking | MEDIUM-HIGH | `lock-` |
| 6 | Data Access Patterns | MEDIUM | `data-` |
| 7 | Monitoring & Diagnostics | LOW-MEDIUM | `monitor-` |
| 8 | Advanced Features | LOW | `advanced-` |

Reference ファイルは `{prefix}-{topic}.md` という命名（例: `query-missing-indexes.md`）。

## 利用可能な Reference

**Advanced Features** (`advanced-`):
- `references/advanced-full-text-search.md`
- `references/advanced-jsonb-indexing.md`

**Connection Management** (`conn-`):
- `references/conn-idle-timeout.md`
- `references/conn-limits.md`
- `references/conn-pooling.md`
- `references/conn-prepared-statements.md`

**Data Access Patterns** (`data-`):
- `references/data-batch-inserts.md`
- `references/data-n-plus-one.md`
- `references/data-pagination.md`
- `references/data-upsert.md`

**Concurrency & Locking** (`lock-`):
- `references/lock-advisory.md`
- `references/lock-deadlock-prevention.md`
- `references/lock-short-transactions.md`
- `references/lock-skip-locked.md`

**Monitoring & Diagnostics** (`monitor-`):
- `references/monitor-explain-analyze.md`
- `references/monitor-pg-stat-statements.md`
- `references/monitor-vacuum-analyze.md`

**Query Performance** (`query-`):
- `references/query-composite-indexes.md`
- `references/query-covering-indexes.md`
- `references/query-index-types.md`
- `references/query-missing-indexes.md`
- `references/query-partial-indexes.md`

**Schema Design** (`schema-`):
- `references/schema-data-types.md`
- `references/schema-foreign-key-indexes.md`
- `references/schema-lowercase-identifiers.md`
- `references/schema-partitioning.md`
- `references/schema-primary-keys.md`

**Security & RLS** (`security-`):
- `references/security-privileges.md`
- `references/security-rls-basics.md`
- `references/security-rls-performance.md`

---

*8 カテゴリに合計 30 件の reference ファイル*

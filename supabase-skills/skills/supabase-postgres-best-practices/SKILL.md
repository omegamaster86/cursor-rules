---
name: supabase-postgres-best-practices
description: Supabase による Postgres のパフォーマンス最適化とベストプラクティス。Postgres のクエリ作成・レビュー・最適化、スキーマ設計、またはデータベース設定に取り組むときにこのスキルを使用する。
license: MIT
metadata:
  author: supabase
  version: "1.1.0"
  organization: Supabase
  date: January 2026
  abstract: Supabase と Postgres を使う開発者向けの包括的な Postgres パフォーマンス最適化ガイド。8 つのカテゴリにわたるパフォーマンスルールを、重要度（重大: クエリ性能、接続管理）から段階的（高度な機能）まで影響度順に整理。各ルールには詳細な解説、誤/正の SQL 例、クエリプラン分析、具体的な性能指標が含まれ、自動最適化やコード生成のガイドとなる。
---

# Supabase Postgres Best Practices

Supabase が保守する Postgres の包括的なパフォーマンス最適化ガイド。8 つのカテゴリにわたるルールを、影響度順に整理し、クエリ最適化やスキーマ設計を支援します。

## 適用する場面

次のときにこれらのガイドラインを参照してください:
- SQL クエリ作成やスキーマ設計
- インデックスの実装やクエリ最適化
- データベースのパフォーマンス問題のレビュー
- コネクションプーリングやスケーリングの設定
- Postgres 固有機能の最適化
- 行レベルセキュリティ（RLS）の作業

## 優先度別のルールカテゴリ

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

## 使い方

詳細な解説と SQL 例は、個別のルールファイルを参照してください:

```
references/query-missing-indexes.md
references/schema-partial-indexes.md
references/_sections.md
```

各ルールファイルには次を含みます:
- なぜ重要かの簡潔な説明
- 誤った SQL 例と解説
- 正しい SQL 例と解説
- 任意の EXPLAIN 出力やメトリクス
- 追加の文脈や参考リンク
- Supabase 固有の注意点（該当する場合）

## References

- https://www.postgresql.org/docs/current/
- https://supabase.com/docs
- https://wiki.postgresql.org/wiki/Performance_Optimization
- https://supabase.com/docs/guides/database/overview
- https://supabase.com/docs/guides/auth/row-level-security

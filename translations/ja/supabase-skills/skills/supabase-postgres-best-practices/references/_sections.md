# セクション定義

このファイルは Postgres ベストプラクティスのルールカテゴリを定義します。ルールはファイル名のプレフィックスに基づいて、自動的にセクションへ割り当てられます。

以下の例は説明用です。各セクションは、Postgres ベストプラクティスの実際のルールカテゴリに置き換えてください。

---

## 1. クエリ性能 (query)
**Impact:** CRITICAL
**Description:** 遅いクエリ、インデックス不足、非効率なクエリプラン。Postgres の性能問題で最も一般的な原因。

## 2. 接続管理 (conn)
**Impact:** CRITICAL
**Description:** コネクションプーリング、接続上限、サーバーレス向け戦略。高並行またはサーバーレス環境で特に重要。

## 3. セキュリティと RLS (security)
**Impact:** CRITICAL
**Description:** 行レベルセキュリティ（RLS）ポリシー、権限管理、認証パターン。

## 4. スキーマ設計 (schema)
**Impact:** HIGH
**Description:** テーブル設計、インデックス戦略、パーティショニング、データ型選定。長期的な性能の土台。

## 5. 並行性とロック (lock)
**Impact:** MEDIUM-HIGH
**Description:** トランザクション管理、分離レベル、デッドロック防止、ロック競合パターン。

## 6. データアクセスパターン (data)
**Impact:** MEDIUM
**Description:** N+1 クエリ解消、バッチ処理、カーソルベースページネーション、効率的なデータ取得。

## 7. 監視と診断 (monitor)
**Impact:** LOW-MEDIUM
**Description:** pg_stat_statements、EXPLAIN ANALYZE、メトリクス収集、性能診断の活用。

## 8. 高度な機能 (advanced)
**Impact:** LOW
**Description:** 全文検索、JSONB 最適化、PostGIS、拡張機能などの高度な Postgres 機能。

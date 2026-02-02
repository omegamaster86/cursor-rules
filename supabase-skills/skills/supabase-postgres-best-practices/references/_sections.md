# セクション定義

このファイルは Postgres ベストプラクティスのルールカテゴリを定義します。ルールはファイル名の prefix に基づいて自動的にセクションへ割り当てられます。

以下の例は説明用です。Postgres ベストプラクティスの実際のカテゴリに置き換えてください。

---

## 1. Query Performance (query)
**Impact:** CRITICAL
**Description:** 遅いクエリ、インデックス不足、非効率なクエリプラン。Postgres の性能問題で最も一般的な原因。

## 2. Connection Management (conn)
**Impact:** CRITICAL
**Description:** 接続プーリング、制限、サーバーレス戦略。高い同時実行性やサーバーレス環境のアプリに不可欠。

## 3. Security & RLS (security)
**Impact:** CRITICAL
**Description:** 行レベルセキュリティ（RLS）ポリシー、権限管理、認証パターン。

## 4. Schema Design (schema)
**Impact:** HIGH
**Description:** テーブル設計、インデックス戦略、パーティショニング、データ型選定。長期的な性能の土台。

## 5. Concurrency & Locking (lock)
**Impact:** MEDIUM-HIGH
**Description:** トランザクション管理、分離レベル、デッドロック防止、ロック競合パターン。

## 6. Data Access Patterns (data)
**Impact:** MEDIUM
**Description:** N+1 クエリの解消、バッチ処理、カーソルベースのページング、効率的なデータ取得。

## 7. Monitoring & Diagnostics (monitor)
**Impact:** LOW-MEDIUM
**Description:** pg_stat_statements、EXPLAIN ANALYZE、メトリクス収集、性能診断。

## 8. Advanced Features (advanced)
**Impact:** LOW
**Description:** 全文検索、JSONB 最適化、PostGIS、拡張、Postgres の高度な機能。

# Databricks 分析とシステムテーブル

## このソースに含まれるもの

Databricks はプロダクト分析・データパイプライン・ウェアハウステレメトリ層。Datadog を補完する。Datadog は*インフラ/ランタイム*、Databricks は*プロダクト/データ*（ユーザーが何をしたか、どの実験が走ったか、機能利用の推移、閾値定数の出所）。

- **プロダクト分析イベント.** `your_warehouse.events.analytics_track_event`（生）と `<your_analytics_db>.<schema>.<table>` の型付き・重複排除 dbt モデル。機能呼び出し、クリック、accept/reject、送信、クライアント報告エラーなど。
- **利用・請求イベント.** `your_warehouse.events.usage_event` / `stg_usage_events`、`raw_model_event` / `stg_raw_model_events`。コスト・ボリューム駆動の決定向け。
- **実験 / フィーチャーフラグデータ.** 露出とアウトカムテーブル。**スキーマは会社依存。** 名前を仮定する前に `SHOW TABLES`。
- **システムテーブル.** `system.query.history`、`system.compute.warehouses`、`system.billing.*`、`system.access.audit`。「このクエリは高コスト？」「誰がどれくらい実行？」「ウェアハウス負荷はいつスパイク？」
- **dbt lineage.** `<your_analytics_db>.<schema>` のモデルはテーブル/フィールド依存のパイプラインを示す。上流変更がコンシューマコード変更の動機になることが多い。
- **Databricks ノートブック.** コード変更前の探索分析。**SQL MCP では照会不可。** rationale がノートブックにある疑いならギャップとして名指し。

## 検索方法

Databricks SQL MCP。主ツール: `execute_sql_read_only`。`statement_id` が返るなら `poll_sql_result` でポーリングし、再実行しない。

**クエリ前にオリエント。** スキーマは会社依存。テーブル名を信じる前にプローブ:

```sql
SHOW TABLES IN <your_analytics_db>.<schema> LIKE '*<keyword>*';
DESCRIBE TABLE <your_analytics_db>.<schema>.stg_<event>;
```

**すべてのクエリに時間境界。** テーブルは巨大、無制限スキャンはタイムアウト。出荷日を挟む窓（通常前後約30日、強い理由があるときだけ広げる）で `_timestamp`（イベント）または `start_time`（`system.query.history`）をフィルタ。

**生テーブルより型付き dbt モデルを優先。** `<your_analytics_db>.<schema>.<table>` は重複排除・型付き・liquid cluster。`analytics_track_event` は重複と未型 `properties_json`。モデル名パターン: `stg_<source>_<event_name_with_underscores>`、`<source>` は `app`、`backend`、`website`、`cli`。パターンだけでは解決しないときは `SHOW TABLES` で exact 名を確認。dbt モデルがまだない、または dbt 更新ラグ内のイベントだけ生テーブル。

**型付き dbt モデルの列規約**（`DESCRIBE` 往復を避ける）:

- `_timestamp`、`_id`、`_auth_id`、`_request_id`、`event_name` — 全モデル標準
- `properties_<name>` — 型付きイベントプロパティ（`properties_entrypoint`、`properties_size_bytes` など）
- `context_team_id`、`context_client_version`、`context_country`、`context_client_os` — 抽出済みクライアント文脈

### よく効く調査パターン

対象に合うテーブル+列の組みを選ぶ:

1. **イベント利用推移.** 関連 `stg_*` で PR マージ前後 ±30 日の日次カウント。マージから1〜2日でゼロから定常量への段差は機能ローンチの強い状況証拠。ゼロへの減衰は非推奨/削除の示唆。
2. **ガードレール/防御チェックの起源.** PR 前14日間の関連 `properties_<name>` の分布（median / p99 / max）。p99 が対象の閾値定数と一致すればデータ由来の数字の可能性。
3. **実験/フラグ.** `SHOW TABLES ... LIKE '*experiment*'` で露出テーブル、PR 日付前後のフラグキー別露出数。
4. **マイグレーション・バックフィル・パフォーマンス書き換えの query history.** `system.query.history` で `statement_text ILIKE '%<table_or_symbol>%'` と狭い `start_time`。変更の動機となった高コストクエリ（`total_duration_ms` または `SUM(read_bytes)`、`COUNT(*)` でソート/集計）。
5. **dbt lineage.** 対象が `<your_analytics_db>.<schema>` モデルを読む/書くなら、モデル自身の git 履歴（このリポジトリ）に rationale があることが多い。そのリードは git investigator に返し、自分では追わない。

## 良い証拠

上記パターンに加え:

- エラー分類イベントのカウントが防御コード PR の数日後にほぼゼロ — そのエラークラスを PR が解いた示唆
- 露出テーブル行が対象のフィーチャーフラグキーを名指し、PR 出荷前後に shipped/concluded 決定

## よくある落とし穴

- **instrumented ≠ caused.** イベント存在はログした人がいた証拠。対象コードが**そのため**存在する証拠ではない。git investigator の PR/コミット引用と組み合わせてから因果を主張。
- **サイレントな計装変更.** イベント量の段差は新規ログ開始の可能性。同窓の計装 PR を確認してからローンチ信号として読む。
- **スキーマドリフト.** プロパティは evolve。今日の型付き列は書かれたときは無かったかも。古いデータは生 `properties_json` 内のみ。
- **dbt 更新ラグ.** `<schema>.*` はスケジュール再ビルド（時間/日単位）。直近数時間は `your_warehouse.events.*` にフォールバックし `_id` で重複排除。
- **会社固有テーブル.** 実験・フラグ・請求・利用テーブルは様々。存在未確認のテーブル結果を報告するのは典型失敗。先に `SHOW TABLES` / `DESCRIBE TABLE`。
- **保持 cliff.** 関連窓がテーブル保持または dbt モデル作成より前なら*ギャップ*であり null ではない。「結果なし」を「活動なし」と synthesizer が読まないよう明示。
- **ノートブックは照会不可。** rationale がノートブックにある疑いならギャップを返す。

## 返すもの

関連 finding ごとに:

- 種別（product event / experiment exposure / usage or billing / system-table row / dbt model）
- 完全修飾テーブル名と実行した exact クエリ
- 照会した時間窓
- コンパクトな数値要約（カウント、パーセンタイル、first/last-seen）。**生行はダンプしない。**
- 対象出荷日との時間相関（例:「初行 2024-08-15、PR #49074 は 2024-08-14 マージ」）
- 関連性と強度: direct / circumstantial / weak

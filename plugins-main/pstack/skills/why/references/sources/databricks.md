# Databricks 分析とシステムテーブル

## このソースが含むもの

Databricks はプロダクト分析、データパイプライン、ウェアハウステレメトリ層。Datadog を補完: Datadog は*インフラ/ランタイム*視点、Databricks は*プロダクト/データ*視点（ユーザーが何をしたか、どの実験が走ったか、機能利用の進化、閾値定数の出所）。

- **Product analytics events.** `your_warehouse.events.analytics_track_event`（raw）と `<your_analytics_db>.<schema>.<table>` の typed、dedup 済み per-event dbt モデル。ユーザー行動: 機能呼び出し、クリック、accept/reject、submit、クライアント報告エラー。
- **Usage & billing events.** `your_warehouse.events.usage_event` / `<your_analytics_db>.<schema>.stg_usage_events`; `your_warehouse.events.raw_model_event` / `<your_analytics_db>.<schema>.stg_raw_model_events`。コスト/ボリューム駆動決定向け。
- **Experiment / feature-flag data.** 露出と outcome テーブル。**スキーマは会社固有。** 名前を仮定する前に `SHOW TABLES` で probe。
- **System tables.** `system.query.history`、`system.compute.warehouses`、`system.billing.*`、`system.access.audit`。「このクエリは高コスト？」「誰がどれだけ実行？」「ウェアハウス負荷はいつスパイク？」
- **dbt lineage.** `<your_analytics_db>.<schema>` モデルは table/field に依存するパイプラインを示す。上流変更が consumer コード変更を often 動機づける。
- **Databricks notebooks.** コード変更前にエンジニアが書いた探索分析。**SQL MCP では query 不可。** 根拠が notebook にありそうならギャップとして名指す。

## 検索方法

Databricks SQL MCP を使用。主要ツール: `execute_sql_read_only`。`statement_id` 返却なら再実行せず `poll_sql_result` で poll。

**query 前に向き合い。** スキーマは会社固有。テーブル名を信じる前に probe:

```sql
SHOW TABLES IN <your_analytics_db>.<schema> LIKE '*<keyword>*';
DESCRIBE TABLE <your_analytics_db>.<schema>.stg_<event>;
```

**すべての query に時間境界。** テーブルは巨大。無制約 scan はタイムアウト。出荷日を挟むウィンドウで `_timestamp`（events）または `start_time`（`system.query.history`）を filter。通常 ±30 日。強い理由があるときのみ広げる。

**raw テーブルより typed dbt モデルを優先。** `<your_analytics_db>.<schema>.<table>` は dedup、typed、liquid-clustered。`your_warehouse.events.analytics_track_event` は duplicate と untyped `properties_json`。モデル名パターン: `stg_<source>_<event_name_with_underscores>`、`<source>` は `app`、`backend`、`website`、`cli`。完全 mapping は `databricks-use-dbt-models` スキル。dbt モデルがまだない、または dbt refresh lag 内イベントが要るときだけ raw に落とす。

**typed dbt モデルの列慣習**（`DESCRIBE` 往復を避ける）:

- `_timestamp`、`_id`、`_auth_id`、`_request_id`、`event_name`。全モデル標準
- `properties_<name>`。typed、アンダースコア event プロパティ
- `context_team_id`、`context_client_version`、`context_country`、`context_client_os`。抽出済みクライアントコンテキスト

### 報われやすい調査パターン

対象に合う table + column 組み合わせを選ぶ:

1. **Event usage trajectory.** PR マージ ±30d で relevant `stg_*` モデルの日次カウント。マージ 1〜2 日以内のゼロから定常への step function は PR が機能を launch した強い circumstantial 証拠。ゼロへの decay は deprecation/deletion 示唆。
2. **Guard-rail / defensive-check origin.** PR *前* 14 日の relevant `properties_<name>` 分布（median / p99 / max）。p99 が対象閾値定数と一致すれば数値がデータから選ばれた示唆。
3. **Experiment / feature-flag lookup.** `SHOW TABLES ... LIKE '*experiment*'` で exposure テーブル見つけ、PR 日付近の relevant flag key で variant 別 exposure count。
4. **Migration、backfill、perf rewrite の query-history 証拠。** `statement_text ILIKE '%<table_or_symbol>%'` と tight `start_time` で filter した `system.query.history` が変更を動機づけた高コスト query を surface（`total_duration_ms` で sort または `SUM(read_bytes)`、`COUNT(*)` 集約）。
5. **dbt lineage.** 対象が `<your_analytics_db>.<schema>` モデルを読む/書くなら、モデル自身の git 履歴（この repo）に often 根拠。git 調査員へ lead を返し自分では追わない。

## 良い証拠

上記パターン形状を超えて:

- 防御コード PR の数日後に error 分類 event count が near zero に。PR がその error class を解決した示唆
- 対象 feature-flag key を名指し、PR 出荷日付近に "shipped" / "concluded" 決定の exposure テーブル行

## 一般的落とし穴

- **計装 != 原因。** event 存在は誰かが log する価値があった証拠であり、対象コードが*そのため*存在する証明ではない。git 調査員の PR/commit 引用と pair してから causation を主張。
- **Silent instrumentation changes.** event volume の step function はユーザー行動変化ではなく新 event が log 始めただけかも。同ウィンドウの instrumentation PR を確認してから ramp を feature-launch シグナルとして読む。
- **Schema drift.** event プロパティは進化。typed dbt モデルの列は対象書かれた時存在しなかったかも。古いデータは raw `properties_json` のみ。
- **dbt refresh lag.** `<your_analytics_db>.<schema>.*` はスケジュール rebuild（often hourly/daily）。直近数時間 event は `your_warehouse.events.*` にフォールバックし `_id` で dedup。
- **Company-specific tables.** experiment、feature-flag、billing、usage テーブルは異なる。存在未確認テーブルの結果報告は典型失敗モード。先に `SHOW TABLES` / `DESCRIBE TABLE`。
- **Retention cliff.** 関連ウィンドウがテーブル保持または dbt モデル作成日より前なら*ギャップ*であり null 結果ではない。統合者が「no results」を「no activity」と読まないよう明示。
- **Notebooks は query 不可。** SQL MCP は Databricks notebook を見えない。根拠が notebook にありそうならギャップを返す。

## 返すもの

各関連所見について:
- タイプ（product event / experiment exposure / usage or billing event / system-table row / dbt model）
- 完全修飾テーブル名と実行した正確 query
- query した時間ウィンドウ
- コンパクト数値要約（counts、percentiles、first/last-seen）。**生行をダンプしない。**
- 対象出荷日との時間相関（例「first row 2024-08-15; PR #49074 merged 2024-08-14」）
- 関連性 + 強さ: direct / circumstantial / weak

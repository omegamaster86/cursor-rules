# Datadog テレメトリ

## このソースが含むもの

Datadog はランタイム記録: 計画や議論ではなく本番で実際に起きたこと。

- **Metrics.** チームが計装したカウンター、ゲージ、ヒストグラム。メトリクスの*存在*自体が証拠: 誰かがこの数値を監視する価値があった。
- **Monitors & alerts.** 誰かを起こす価値があると判断した条件。`rate_limit_hit > 10/min` で鳴るモニターはその閾値をチームが心配した直接証拠。
- **Dashboards.** キュレーションされたビュー。チャートはサブシステムで重要と見なすものを示す。
- **APM traces & spans.** リクエストレベルランタイムデータ。「なぜ遅い/タイムアウト」質問に有用。
- **Logs.** 大量イベント記録。防御的コードを動機づけたエラー条件を often 含む。
- **Incidents.** タイムラインとリンクポストモーテム付き正式インシデント記録。
- **Notebooks.** 探索調査。仮説と分析を often 含む。

Datadog は「このコードが書かれた頃の本番現実は何だったか？」に答え、コード形状を often 説明する。

## 検索方法

Datadog MCP を使用。広く始め絞る。

1. **所有サービスを特定。**

   ```
   search_datadog_services (filter by name or team)
   search_datadog_service_dependencies (see upstream/downstream)
   ```

2. **ダッシュボードとモニターを先に。** チームが care するものを示す。

   ```
   search_datadog_dashboards (query: feature name, service name, symbol)
   search_datadog_monitors   (same queries)
   ```

   ダッシュボード/モニターが対象をカバーするとき、クエリと監視閾値を記す。閾値が often「なぜ N にクランプ？」の答え。

3. **対象周辺のメトリクス。**

   ```
   search_datadog_metrics (by name pattern, e.g., the feature or symbol)
   get_datadog_metric_context (metadata: description, units, tags)
   get_datadog_metric (timeseries; "was there a spike around the PR date?")
   ```

   メトリクス軌道と対象追加/変更日の相関は強い supporting 証拠:「`payment_timeout` が 2023-11-03 にスパイク、リトライロジックが 2023-11-06 マージ」。

4. **Logs。絞る。ダンプしない。**

   ```
   search_datadog_logs (raw log patterns near the target, set use_log_patterns=true)
   analyze_datadog_logs (SQL-style aggregations, only when you need counts)
   ```

   シンボル、エラー文字列、機能名で検索。**時間境界クエリを強く優先**（例 変更前後 30 日）。ログ量は巨大。無制約検索は時間浪費・タイムアウト。

5. **APM spans と traces。**

   ```
   aggregate_spans    (stats: "how often does this endpoint fail?")
   search_datadog_spans (inspect individual spans)
   get_datadog_trace  (a specific trace ID)
   ```

   タイムアウト、リトライ、遅い経路、クロスサービス振る舞いに有用。

6. **Incidents。**

   ```
   search_datadog_incidents (by title, team, date range)
   get_datadog_incident     (full detail for a specific incident)
   ```

   対象が防御的に見えるなら追加時期周辺のインシデント検索。「X の防御チェック追加」を含むタイムラインは near-direct 証拠。

## 良い証拠

- コードが強制する制約と一致するクエリと閾値のモニター（コードが 100 にクランプ、モニターが 100/min 超でアラート）
- 対象著者が作り、コードが測定/防御することに対応するウィジェットを持つダッシュボード
- コードマージ直前の本番スパイクと、その後の安定値を示すメトリクス
- 対象コード、同シンボル、同エラー文字列を参照するインシデント記録
- 変更前ウィンドウの、防御コードが防ぐであろう特定エラーパターンを示すログ

## 一般的落とし穴

- **相関は causation ではない。** マージ前スパイクと後安定は示唆的。同ウィンドウに他変更が land しうる。近傍 PR を確認。
- **見つけたチャートへの過適合。** Datadog 可視化は*人間が作る*。その人の枠組みを反映。「retry success rate」チャートはリトライ成功を care した証拠であり、特定行が存在する理由の証明ではない。
- **消えたテレメトリ。** メトリクス改名・削除・短い保持。関連ウィンドウのデータがなければギャップであり null 結果ではない。
- **スケールでのノイズ。** 共通文字列検索は数千マッチ。サービス、タグ、時間で aggressively 絞る。生ログダンプより `analyze_datadog_logs` で集約。
- **計装 != 原因。** メトリクス存在は誰かが何かを測った証拠であり、コードが*そのため*追加された証明ではない。commit/PR 日付と突合。

## 返すもの

各関連項目について:
- タイプ（dashboard / monitor / metric / log pattern / trace / incident / notebook）
- タイトルまたは名前
- リンクまたは識別子（dashboard ID、monitor ID、metric 名、incident ID）
- 所有者/著者と作成/変更日
- 質問に関係する具体条件、クエリ、引用（可能なら逐語）
- 関連性: 対象コードについて何を示唆し、接続の強さ

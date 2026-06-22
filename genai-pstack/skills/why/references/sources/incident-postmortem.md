# インシデントとポストモーテムコンテキスト

別ソースではなく**横断角度**。インシデントは防御的コードを often 動機づける（「X 障害後にこのチェック追加」）。対象が防御的（null チェック、リトライ、タイムアウト、レート制限、feature flag）なら、利用可能なすべてのソースでインシデント履歴を specifically hunt:

- **Notion**: 対象ファイル、機能、エラー文字列を言及するポストモーテム検索
- **Linear**: `incident`、`sev-*`、`postmortem-action-item`、`reliability` ラベルチケット
- **Slack**: 対象コード追加日付前後の `#sev-*` と `#incident-*` 検索
- **Git**: 「fix for incident」「add defensive check」、「revert」の後「re-apply with...」メッセージは強シグナル
- **Datadog**: タイムライン付き正式インシデント `search_datadog_incidents`、ポストモーテムアクションとして作られたダッシュボード/モニター
- **Sentry**: first-seen/last-seen ウィンドウが対象 PR 出荷日と一致する issue、対象を通るスタックトレース
- **Databricks**: エラー条件を分類するプロダクト分析 event（クライアント報告失敗、ユーザー可視リトライ event など）はインシデントウィンドウで often スパイク。対象 PR 出荷後その event count 低下は、Datadog/Sentry シグナルがノイズでもユーザー可視症状を対象コードが解決した circumstantial 支持。

インシデントリンクを見つけたらフルポストモーテム取得。ポストモーテムは typically「Action Items」節がありコード変更に直接結びつく。複数ソースが裏付けるとき（Datadog incident ID が Linear チケットに現れ、Notion ポストモーテムに現れ、Slack スレッドが対象 PR をリンクし、fix 後 Databricks error-event count が落ちる）証拠は特に強い。

コードの防御的性格からインシデント駆動起源がもっともらしいとき時間をかける価値あり。防御的に見えないコードではスキップ。

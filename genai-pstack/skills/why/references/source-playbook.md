# ソースプレイブック

why スキルは利用可能証拠カテゴリごとに調査員を 1 人起動し、各は下記の単一ソース固有プレイブックを読む。プレイブックは一般的 MCP の具体例。同カテゴリの別 MCP に適応。

| カテゴリ | プレイブック | 記述例 MCP |
|---|---|---|
| ソース管理履歴 | [`code-archaeology.md`](./sources/code-archaeology.md) | git, `gh` |
| 課題 / チケットトラッカー | [`linear.md`](./sources/linear.md) | Linear（Jira、GitHub Issues、Plane、Shortcut に適応） |
| 長文ドキュメント | [`notion.md`](./sources/notion.md) | Notion（Confluence、Google Docs、Coda に適応） |
| リアルタイムチームチャット | [`slack.md`](./sources/slack.md) | Slack（Discord、Microsoft Teams、Mattermost に適応） |
| インフラ可観測性 | [`datadog.md`](./sources/datadog.md) | Datadog（New Relic、Honeycomb、Grafana、Splunk に適応） |
| エラー / 例外トラッキング | [`sentry.md`](./sources/sentry.md) | Sentry（Rollbar、Bugsnag、Airbrake に適応） |
| プロダクト分析ウェアハウス | [`databricks.md`](./sources/databricks.md) | Databricks SQL（Snowflake、BigQuery、ClickHouse、dbt に適応） |

横断:

- [`incident-postmortem.md`](./sources/incident-postmortem.md)。対象コードが防御的に見えるとき追加（null チェック、リトライ、タイムアウト、レート制限、feature flag、egress ガード、OOM ハンドラ）。

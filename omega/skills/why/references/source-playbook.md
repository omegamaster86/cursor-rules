# ソースプレイブック

why スキルは、利用可能な証拠カテゴリごとに1人の investigator を起動し、各 investigator は下記のカテゴリ別プレイブックを1つだけ読む。プレイブックは一般的な MCP の具体例。同カテゴリの別 MCP には適宜読み替える。

| カテゴリ | プレイブック | 記載例の MCP |
|---|---|---|
| ソース管理履歴 | [`code-archaeology.md`](./sources/code-archaeology.md) | git、`gh` |
| Issue / チケットトラッカー | [`linear.md`](./sources/linear.md) | Linear（Jira、GitHub Issues、Plane、Shortcut などに読み替え） |
| 長文ドキュメント | [`notion.md`](./sources/notion.md) | Notion（Confluence、Google Docs、Coda などに読み替え） |
| リアルタイムチームチャット | [`slack.md`](./sources/slack.md) | Slack（Discord、Microsoft Teams、Mattermost などに読み替え） |
| インフラ可観測性 | [`datadog.md`](./sources/datadog.md) | Datadog（New Relic、Honeycomb、Grafana、Splunk などに読み替え） |
| エラー / 例外トラッキング | [`sentry.md`](./sources/sentry.md) | Sentry（Rollbar、Bugsnag、Airbrake などに読み替え） |
| プロダクト分析ウェアハウス | [`databricks.md`](./sources/databricks.md) | Databricks SQL（Snowflake、BigQuery、ClickHouse、dbt などに読み替え） |

横断:

- [`incident-postmortem.md`](./sources/incident-postmortem.md)。対象コードが防御的に見える場合（null チェック、リトライ、タイムアウト、レート制限、フィーチャーフラグ、egress ガード、OOM ハンドラ）に追加する。

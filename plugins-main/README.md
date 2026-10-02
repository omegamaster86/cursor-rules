# Cursor プラグイン

人気の開発者向けツール、フレームワーク、SaaS 製品向けの公式 Cursor プラグイン集。各プラグインはリポジトリルート直下の独立ディレクトリとして配置され、各々に `.cursor-plugin/plugin.json` マニフェストがあります。

## プラグイン一覧

| `name` | プラグイン | 作成者 | カテゴリ | `description`（マーケットプレイス掲載文） |
|:-------|:-------|:-------|:---------|:-------------------------------------|
| `teaching` | [Teaching](teaching/) | Cursor | Utilities | スキルマッピング、実践プラン、学習レトロスペクティブ。 |
| `continual-learning` | [Continual Learning](continual-learning/) | Eric Zakariasson | Developer Tools | 重要度の高い要点だけを使い、AGENTS.md の対話履歴ベースの段階的メモリ更新を実現します。 |
| `cursor-team-kit` | [Cursor Team Kit](cursor-team-kit/) | Eric Zakariasson | Developer Tools | Cursor 開発者が CI、コードレビュー、出荷、ローカル自動化、検証に用いる社内のチームワークフロー。 |
| `thermos` | [Thermos](thermos/) | Cursor | Developer Tools | Thermo-nuclear branch review: 深いセキュリティ / 正確性監査、厳格なコード品質ルーブリック、並列サブエージェント、thermos オーケストレーション、必要に応じたマージ準備済み PR フローを提供。 |
| `create-plugin` | [Create Plugin](create-plugin/) | Cursor | Developer Tools | 新規エージェントプラグインのスキャフォールドと検証。 |
| `ralph-loop` | [Ralph Loop](ralph-loop/) | Cursor | Developer Tools | Ralph Wiggum 技法による反復的な自己参照型 AI ループ。 |
| `agent-compatibility` | [Agent Compatibility](agent-compatibility/) | Cursor | Developer Tools | CLI 駆動のリポジトリ互換性スキャンに加え、起動、検証、ドキュメントを実態に即して監査するエージェントを提供。 |
| `cli-for-agent` | [CLI for Agents](cli-for-agent/) | Eric Zakariasson | Developer Tools | コーディングエージェントが確実に実行できる CLI を設計するためのパターン：フラグ、サンプル付きヘルプ、パイプライン、エラー、冪等性、dry-run。 |
| `pr-review-canvas` | [PR Review Canvas](pr-review-canvas/) | Cursor | Developer Tools | PR の差分を重要度順にグループ化したレビュー用 Canvas としてレンダリング。 |
| `docs-canvas` | [Docs Canvas](docs-canvas/) | Cursor | Developer Tools | ドキュメントをナビゲーション可能な Canvas としてレンダリング。 |
| `cursor-sdk` | [Cursor SDK](cursor-sdk/) | Cursor | Developer Tools | TypeScript SDK でアプリ、スクリプト、オートメーションを構築。 |
| `orchestrate` | [Orchestrate](orchestrate/) | Cursor | Developer Tools | プランナー、ワーカー、検証担当と構造化ハンドオフで、大規模タスクを並列クラウドエージェントに分散。 |
| `pstack` | [pstack](pstack/) | Lauren Tan | Developer Tools | 「早く進めたいなら、まず深く掘る」。pstack は少なく質の高いコードを書く支援と、信頼して並列化できる厳密なエージェントワークフローを提供。 |
| `dyl-stack` | [dyl-stack](dyl-stack/) | Dylan Gattey | Developer Tools | pstack 上の Dylan 流エージェントスタイル：症状パッチより根本原因、設計前の The Algorithm、簡潔な検証済みデリバリー、ペースト向き PR レビュー、ビジュアル判定付き Figma→UI。 |
| `advisor` | [Advisor](advisor/) | Cursor | Developer Tools | 重要な判断前、行き詰まり時、完了宣言前に、より強いモデルへ相談。 |
| `grok-voice` | [Grok Voice](grok-voice/) | Eric Zakariasson | Developer Tools | アプリに Grok 音声を追加：リアルタイム音声対話、音声入力、読み上げ TTS、音声セッション向けログ駆動の修正ループ。 |
| `gmail` | [Gmail](third_party/gmail/) | Cursor | Productivity | メールの検索、閲覧、下書き、管理。 |
| `google-drive` | [Google Drive](third_party/google-drive/) | Cursor | Productivity | ファイルの検索、閲覧、作成、共有。 |
| `google-calendar` | [Google Calendar](third_party/google-calendar/) | Cursor | Productivity | イベント検索とミーティング予約。 |
| `google-docs` | [Google Docs](third_party/google-docs/) | Cursor | Productivity | ドキュメントの閲覧、作成、編集。 |
| `google-sheets` | [Google Sheets](third_party/google-sheets/) | Cursor | Productivity | スプレッドシートの読み取り、書き込み、追記。 |
| `google-slides` | [Google Slides](third_party/google-slides/) | Cursor | Productivity | プレゼンの作成、編集、レンダリング。 |
| `gong` | [Gong](third_party/gong/) | Cursor | Integrations | アカウントサマリー、ディールインサイト、コールブリーフの取得。 |
| `salesforce` | [Salesforce](third_party/salesforce/) | Cursor | Integrations | 組織内レコードのクエリ、作成、更新。 |
| `playwright` | [Playwright](third_party/playwright/) | Cursor | Integrations | 実ブラウザでのナビゲーション、クリック、スクリーンショット、テスト。 |
| `github` | [GitHub](third_party/github/) | Cursor | Integrations | リポジトリ、Issue、PR、Actions の管理。 |
| `ashby` | [Ashby](third_party/ashby/) | Cursor | Integrations | 候補者検索、面接準備、パイプラインタスク管理。 |
| `hubspot` | [HubSpot](third_party/hubspot/) | Cursor | Integrations | コンタクト、会社、ディール、チケットの検索と更新。 |
| `intercom` | [Intercom](third_party/intercom/) | Cursor | Integrations | 会話、コンタクト、ヘルプセンター記事の検索。 |
| `zoom` | [Zoom](third_party/zoom/) | Cursor | Integrations | ミーティング検索、トランスクリプト取得、Zoom Docs の操作。 |
| `x` | [X](third_party/x/) | Cursor | Integrations | 投稿検索、タイムライン閲覧、トレンド、ブックマーク管理。 |
| `clay` | [Clay](third_party/clay/) | Cursor | Integrations | 人物・企業のエンリッチ、AI リサーチエージェントの実行。 |
| `circleback` | [Circleback](third_party/circleback/) | Cursor | Integrations | ミーティング、トランスクリプト、アクション項目、メールの検索。 |
| `docusign` | [Docusign](third_party/docusign/) | Cursor | Integrations | エンベロープ、テンプレート、ワークフロー、契約の管理。 |
| `navan` | [Navan](third_party/navan/) | Cursor | Integrations | 経費、旅行予約、ポリシー、カードのクエリ。 |
| `profound` | [Profound](third_party/profound/) | Cursor | Integrations | AI 可視性、センチメント、引用の追跡。 |
| `juicebox` | [Juicebox](third_party/juicebox/) | Cursor | Integrations | 採用アナリティクス、ショートリスト、ソーシングエージェントのクエリ。 |
| `outreach` | [Outreach](third_party/outreach/) | Cursor | Integrations | シーケンス、見込み客、Kaia ミーティングの検索。 |
| `amplemarket` | [Amplemarket](third_party/amplemarket/) | Cursor | Integrations | 人物・企業の検索、リードエンリッチ、シーケンス実行。 |
| `klaviyo` | [Klaviyo](third_party/klaviyo/) | Cursor | Integrations | プロファイル、セグメント、キャンペーン、フローの管理。 |
| `customer-io` | [Customer.io](third_party/customer-io/) | Cursor | Integrations | キャンペーン構築、セグメント管理、人物のクエリ。 |
| `mailerlite` | [MailerLite](third_party/mailerlite/) | Cursor | Integrations | 購読者、グループ、キャンペーン、自動化の管理。 |
| `brevo` | [Brevo](third_party/brevo/) | Cursor | Integrations | コンタクト、メール/SMS キャンペーン、CRM ディールの管理。 |
| `typeform` | [Typeform](third_party/typeform/) | Cursor | Integrations | フォーム作成、回答分析、コンタクト管理。 |
| `jotform` | [Jotform](third_party/jotform/) | Cursor | Integrations | フォームの作成・編集と送信内容の閲覧。 |
| `semrush` | [Semrush](third_party/semrush/) | Cursor | Integrations | キーワード、被リンク、トラフィック、競合のリサーチ。 |
| `ahrefs` | [Ahrefs](third_party/ahrefs/) | Cursor | Integrations | キーワード、被リンク、ランキング、サイトヘルスのリサーチ。 |
| `godaddy` | [GoDaddy](third_party/godaddy/) | Cursor | Integrations | ドメイン名のブレインストーミングと空き確認。 |
| `upwork` | [Upwork](third_party/upwork/) | Cursor | Integrations | タレント検索、求人投稿、契約管理。 |
| `workable` | [Workable](third_party/workable/) | Cursor | Integrations | 候補者検索、パイプライン移動、HR レコード管理。 |
| `brex` | [Brex](third_party/brex/) | Cursor | Integrations | 経費、領収書、請求、カード、旅行のクエリ。 |
| `mercury` | [Mercury](third_party/mercury/) | Cursor | Integrations | 残高、取引、明細、カードの閲覧。 |
| `todoist` | [Todoist](third_party/todoist/) | Cursor | Integrations | タスクとプロジェクトの作成、検索、完了。 |
| `calendly` | [Calendly](third_party/calendly/) | Cursor | Integrations | 空き確認と予約・キャンセル・再予約。 |
| `smartsheet` | [Smartsheet](third_party/smartsheet/) | Cursor | Integrations | シート、行、ワークスペースのクエリと更新。 |
| `wrike` | [Wrike](third_party/wrike/) | Cursor | Integrations | プロジェクト検索、タスク作成、コメント投稿。 |
| `coda` | [Coda](third_party/coda/) | Cursor | Integrations | ドキュメント検索、ページ閲覧、テーブル更新。 |
| `guru` | [Guru](third_party/guru/) | Cursor | Integrations | 社内ナレッジの検索と検証済み回答の下書き。 |
| `fireflies` | [Fireflies](third_party/fireflies/) | Cursor | Integrations | ミーティングトランスクリプト、サマリー、アクション項目の検索。 |
| `otter` | [Otter.ai](third_party/otter/) | Cursor | Integrations | ミーティング履歴の検索と全文トランスクリプトの取得。 |
| `fathom` | [Fathom](third_party/fathom/) | Cursor | Integrations | ミーティング検索とトランスクリプト・サマリーの取得。 |
| `craft` | [Craft](third_party/craft/) | Cursor | Integrations | ドキュメントとデイリーノートの検索、作成、更新。 |
| `mem` | [Mem](third_party/mem/) | Cursor | Integrations | ノートとコレクションのキャプチャ、検索、整理。 |
| `readwise` | [Readwise](third_party/readwise/) | Cursor | Integrations | ハイライトと Reader ドキュメントの検索、記事の保存。 |
| `similarweb` | [Similarweb](third_party/similarweb/) | Cursor | Integrations | ウェブトラフィック、オーディエンス、競合の分析。 |
| `xero` | [Xero](third_party/xero/) | Cursor | Integrations | 請求書、コンタクト、レポート、給与の読み書き。 |
| `x-ads` | [X Ads](third_party/x-ads/) | Cursor | Integrations | 広告キャンペーン管理、広告作成、コンバージョン追跡、パフォーマンス統計の取得。 |
| `attio` | [Attio](third_party/attio/) | Cursor | Integrations | CRM レコード、リスト、ノート、タスクの検索と更新。 |
| `hunter` | [Hunter](third_party/hunter/) | Cursor | Integrations | メールの検索・検証、企業発見、リード保存。 |
| `gamma` | [Gamma](third_party/gamma/) | Cursor | Integrations | プレゼン、ドキュメント、ウェブページの生成。 |
| `teams` | [Teams](third_party/teams/) | Cursor | Productivity | Microsoft Teams のチャットとチャンネルメッセージの検索、閲覧、送信。 |
| `sharepoint` | [SharePoint](third_party/sharepoint/) | Cursor | Productivity | SharePoint サイト、ドキュメントライブラリ、ファイル、リストの検索と閲覧。 |
| `finance` | [Finance](third_party/finance/) | Cursor | Integrations | 口座を安全に接続し、支出、サブスク、残高、投資について Grok が支援。 |
| `webull` | [Webull](third_party/webull/) | Cursor | Integrations | 口座、ポジション、注文、ウォッチリスト、マーケットデータの閲覧。 |
| `sp-global` | [S&P Global](third_party/sp-global/) | Cursor | Integrations | S&P Capital IQ の財務、価格、トランスクリプトのクエリ。 |
| `interactive-brokers` | [Interactive Brokers](third_party/interactive-brokers/) | Cursor | Integrations | ポジション、残高、P&L の確認と取引指示の下書き。 |
| `meltwater` | [Meltwater](third_party/meltwater/) | Cursor | Integrations | メディア・ソーシャル言及の検索とアナリティクス取得。 |
| `daloopa` | [Daloopa](third_party/daloopa/) | Cursor | Integrations | ソースリンク付きファンダメンタルズ、KPI、開示、価格の取得。 |
| `excalidraw` | [Excalidraw](third_party/excalidraw/) | Cursor | Integrations | チャットから手描き風図の作成とエクスポート。 |
| `google-cloud-bigquery` | [Google Cloud BigQuery](third_party/google-cloud-bigquery/) | Cursor | Integrations | データセットとテーブルの探索、SQL クエリの実行。 |
| `statsig` | [Statsig](third_party/statsig/) | Cursor | Integrations | フィーチャーゲート、実験、ダイナミック設定、メトリクスの確認と管理。 |
| `robinhood` | [Robinhood](third_party/robinhood/) | Cursor | Integrations | ポートフォリオ、ポジション、注文、ウォッチリスト、マーケットデータの閲覧と Robinhood Agentic 口座での取引。 |
| `coinbase` | [Coinbase](third_party/coinbase/) | Cursor | Integrations | 残高確認、見積り取得、取引のプレビューまたは実行。 |
| `etoro-trading` | [eToro Trading](third_party/etoro-trading/) | Cursor | Integrations | eToro ポートフォリオ、残高、ポジション、ウォッチリストの閲覧、銘柄・トレーダーの調査、取引の準備と実行。 |
| `x-money` | [X Money](third_party/x-money/) | Cursor | Integrations | X Money カードの利用、X ユーザーへの送金、財務管理、残高と取引履歴の閲覧。 |
| `shopify-store` | [Shopify](third_party/shopify-store/) | Cursor | Integrations | Shopify ストアを接続し、商品、注文、顧客、在庫、売上について Grok が回答。 |

作成者情報は各プラグインの `plugin.json` の `author.name` に一致します（Cursor はマニフェストで `plugins@cursor.com` を記載）。

## リポジトリ構成

このリポジトリは複数プラグインのマーケットプレイス形式です。ルートの `.cursor-plugin/marketplace.json` がすべてのプラグインを一覧化し、各プラグインは個別にマニフェストを持ちます。

```
plugins/
├── .cursor-plugin/
│   └── marketplace.json       # マーケットプレイスマニフェスト（全プラグインの一覧）
├── plugin-name/
│   ├── .cursor-plugin/
│   │   └── plugin.json        # プラグイン個別マニフェスト
│   ├── skills/                # エージェントスキル（frontmatter を持つ SKILL.md）
│   ├── rules/                 # Cursor ルール（.mdc）
│   ├── mcp.json               # MCP サーバ定義
│   ├── README.md
│   ├── CHANGELOG.md
│   └── LICENSE
└── ...
```

## 同期元

このディレクトリは [cursor/plugins](https://github.com/cursor/plugins) の `main` ブランチと同期しています（最終同期: 2026-10-02）。

## ライセンス

MIT

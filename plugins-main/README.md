# Cursor プラグイン

人気の開発者向けツール、フレームワーク、SaaS 製品向けの公式 Cursor プラグイン集。各プラグインはリポジトリルート直下の独立ディレクトリとして配置され、各々に `\.cursor-plugin/plugin.json` マニフェストがあります。

## プラグイン一覧

| `name` | プラグイン | 作成者 | カテゴリ | `description`（マーケットプレイス掲載文） |
|:-------|:-------|:-------|:---------|:-------------------------------------|
| `continual-learning` | [Continual Learning](continual-learning/) | Cursor | Developer Tools | 重要度の高い要点だけを使い、AGENTS.md の対話履歴ベースの段階的メモリ更新を実現します。 |
| `cursor-team-kit` | [Cursor Team Kit](cursor-team-kit/) | Cursor | Developer Tools | Cursor 開発者が CI、コードレビュー、出荷、ローカル自動化、検証に用いる社内のチームワークフロー。 |
| `thermos` | [Thermos](thermos/) | Cursor | Developer Tools | Thermo-nuclear branch review: 深いセキュリティ / 正確性監査、厳格なコード品質ルーブリック、並列サブエージェント、thermos オーケストレーション、必要に応じたマージ準備済み PR フローを提供。 |
| `create-plugin` | [Create Plugin](create-plugin/) | Cursor | Developer Tools | 新規 Cursor プラグインの作成と検証。 |
| `agent-compatibility` | [Agent Compatibility](agent-compatibility/) | Cursor | Developer Tools | CLI 駆動のリポジトリ互換性スキャンに加え、起動、検証、ドキュメントを実態に即して監査する Cursor エージェントを提供。 |
| `cli-for-agent` | [CLI for Agents](cli-for-agent/) | Cursor | Developer Tools | コーディングエージェントが確実に実行できる CLI を設計するためのパターン：フラグ、サンプル付きヘルプ、パイプライン、エラー、冪等性、dry-run。 |
| `pr-review-canvas` | [PR Review Canvas](pr-review-canvas/) | Cursor | Developer Tools | PR の差分をレビュアー理解しやすい形で Cursor Canvas 上にレンダリング。重要度順に変更をグループ化し、定型処理と中核ロジックを分離し、複雑／予期しづらいコードを強調表示。 |
| `docs-canvas` | [Docs Canvas](docs-canvas/) | Cursor | Developer Tools | ドキュメント（アーキテクチャノート、API リファレンス、ランブック、コードベースウォークスルー）を、セクション、目次、図表、相互参照付きのナビゲーション可能な Cursor Canvas としてレンダリング。 |
| `cursor-sdk` | [Cursor SDK](cursor-sdk/) | Cursor | Developer Tools | Cursor TypeScript SDK（`@cursor/sdk`）上で、アプリ、スクリプト、CI パイプライン、オートメーションを構築するための基盤を提供。実行環境選択、認証、ストリーミング、MCP、エラーハンドリング、拡張可能な統合パターン。 |
| `orchestrate` | [Orchestrate](orchestrate/) | Cursor | Developer Tools | 計画担当、作業担当、検証担当を使って、複数の Cursor クラウドエージェントに大規模タスクを並列分散。 |
| `pstack` | [pstack](pstack/) | Lauren Tan | Developer Tools | 「早く進めたいなら、まず深く掘る」。pstack は、少なくて質の高いコードを書くための支援を行い、信頼して並列化できる厳密なエージェントワークフローを提供。 |

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

## ライセンス

MIT

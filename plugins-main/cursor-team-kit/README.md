# Cursor Team Kit プラグイン

CI、コードレビュー、出荷、テスト信頼性向上のための社内向けワークフロー。プラグインは、サードパーティのサービス連携なしでそのまま利用できるように、プラグイン&プレイ方式で設計されています。

## インストール

```bash
/add-plugin cursor-team-kit
```

## 構成

### Skills

| Skill | 説明 |
|:------|:------------|
| `loop-on-ci` | CI 実行を監視し、失敗を解消するまで再試行を繰り返す |
| `review-and-ship` | 体系的なレビューを実行し、変更をコミットして PR を作成 |
| `pr-review-canvas` | 注釈付き・カテゴリ分けされた差分を表示する対話型 HTML PR ウォークスルーを生成 |
| `verify-this` | ベースライン/比較対象の成果物を使って主張を検証し、明確な結論を返す |
| `control-cli` | 対話型 CLI や TUI を駆動し、プロファイル取得するためのローカルハーネスを構築・適応 |
| `control-ui` | Web や Electron UI 向けにローカルブラウザ/CDP ハーネスを構築・適応 |
| `make-pr-easy-to-review` | ノイズの多い PR 履歴を整理し、説明を改善し、レビュアー向けガイダンスを追加 |
| `run-smoke-tests` | Playwright スモークテストを実行し、失敗をトリアージ |
| `fix-ci` | 失敗した CI ジョブを特定し、ログを調査し、絞った修正を適用 |
| `new-branch-and-pr` | 新規ブランチを作成し、作業を完了して Pull Request を作成 |
| `get-pr-comments` | 対象 PR のレビュアーコメントを取得・要約 |
| `check-compiler-errors` | コンパイルと型チェックを実行し、失敗を報告 |
| `what-did-i-get-done` | 指定期間の作業コミットを要約し、簡潔なステータス更新を作成 |
| `weekly-review` | バグ修正/技術的負債/新規対応の観点で毎週の作業要約を生成 |
| `fix-merge-conflicts` | マージ競合を解消し、ビルド/テストを検証、決定内容を要約 |
| `deslop` | AI 由来の冗長実装を取り除き、コードスタイルを整える |
| `workflow-from-chats` | チャット内容から継続的に使える作業方針を抽出し、スキル・ルール・ドキュメントに反映 |
| `thermo-nuclear-code-quality-review` | 例外的に厳密な保守性レビューを実施（code-judo、1k 行ルール、スパゲッティ、境界チェック） |

### Agents

| Agent | 説明 |
|:------|:------------|
| `ci-watcher` | GitHub Actions の実行を監視し、簡潔な成功/失敗サマリを返す |
| `thermo-nuclear-code-quality-review` | 差分に対して thermo-nuclear コード品質ルーブリックを適用する Task サブエージェント |

### Rules

| Rule | 説明 |
|:-----|:------------|
| `typescript-exhaustive-switch` | union/enum に対して網羅的な switch を要求 |
| `no-inline-imports` | 可読性と一貫性のため、インポートはモジュール先頭に配置 |

## ライセンス

MIT

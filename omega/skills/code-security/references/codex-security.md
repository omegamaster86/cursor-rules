# Codex Security への委譲

正本: [openai/plugins — codex-security](https://github.com/openai/plugins/tree/main/plugins/codex-security)（cursor-rules では `openai-plugins/` submodule）。

## いつ使う

| 依頼 | Codex 側の入口 |
|------|----------------|
| リポジトリ全体・スコープ付きディレクトリ（diff なし） | プラグイン `security-scan` スキル（Standard） |
| PR / ブランチ / コミット / 作業ツリー diff | diff 向けスキル（プラグイン内。`security-scan` の description で除外されている種別） |
| より深い多パススキャン | Deep スキャン（プラグイン設定・`CODEX_SECURITY_*`） |

Cursor の omega スキルからは **Codex CLI が動いているセッション**でのみ委譲する。Cursor 単体では [checklist.md](checklist.md) を実行する。

## セットアップ（ユーザー環境）

1. Codex CLI にプラグインをインストール（OpenAI 公式手順に従う）
2. MCP `codex-security` が起動できること（`plugins/codex-security/scripts/launch_codex_security_mcp`）
3. 任意: `CODEX_SECURITY_KNOWLEDGE_BASE`、リポジトリの `SECURITY.md`

## エージェントがやること

1. スコープと diff の有無を確認し、**Standard vs diff vs Deep** を選ぶ（公式 SKILL の description に従う）
2. ホストが SDK スキャン ID / ディレクトリを渡したら **それを正**とし、別スキャンを開始しない
3. 完了後、生成された `report.md` と canonical JSON を正本として [report-format.md](report-format.md) で要約する
4. `report.md` を手書きしない（公式 finalize 経路の成果物のみ）

## 環境変数（よく使う）

| 変数 | 意味 |
|------|------|
| `CODEX_SECURITY_SCAN_ID` / `CODEX_SECURITY_SCAN_DIR` | SDK 所有スキャン（上書き禁止） |
| `CODEX_SECURITY_TARGET_PATHS_FILE` | 許可されたパス一覧（スコープ拡大禁止） |
| `CODEX_SECURITY_STATE_DIR` | 永続スキャン成果物のルート |

詳細: プラグイン `references/scan-contract.md`, `artifact-storage.md`。

## Cursor との関係

- omega の `code-security` は **手順とレポート形式**を共有するラッパー
- 実行エンジンは Codex 側に残す（[UPSTREAM.md](UPSTREAM.md)）

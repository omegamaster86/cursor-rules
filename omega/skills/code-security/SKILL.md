---
name: code-security
description: "コードベース・差分・PRのセキュリティスキャンとレビュー。Codex の codex-security、Claude Code の claude-security に委譲するか、Cursor 単体でチェックリストレビュー。スキャン、監査、脆弱性チェック、セキュリティレビューの依頼時に使用。"
disable-model-invocation: true
argument-hint: "スコープ（全体 / 差分 / PR）と深さ（軽量レビュー / 公式スキャン）"
---

# Code Security（codex-security × claude-security）

Anthropic **Claude Security** と OpenAI **Codex Security** を **1 つの入口**にまとめる omega スキル。スキャンエンジン本体は各公式プラグインに残し、ここでは **ルーティング・手順・レポート形式**を統一する。

## ルーティング

| ユーザーの依頼 | 推奨エンジン | 参照 |
|----------------|--------------|------|
| リポジトリ全体・パッケージ単位（diff なし） | **codex-security** `security-scan`（Standard） | [codex-security.md](references/codex-security.md) |
| PR / ブランチ / コミット / 未コミット差分の監査 | **claude-security** Scan changes、または Codex の diff スキャン | [claude-security.md](references/claude-security.md) |
| 既存 Claude Security レポートの修正パッチ | **claude-security** Suggest patches | [claude-security.md](references/claude-security.md) |
| Cursor のみ・軽量・コスト抑えめ | **cursor** チェックリスト | [checklist.md](references/checklist.md) |
| 編集中の即時リマインド + コミット時 LLM レビュー | **security-guidance**（Claude Code プラグイン） | 公式 README（omega 非同梱） |
| PR 上の Bugbot / agentic security コメント | **forge** triage | `forge-mode/references/bugbot-triage.md` |

**判定の順序**

1. ホストを確認: Codex CLI / Claude Code / Cursor のみ
2. diff の有無とスコープ（全体 vs 変更のみ）
3. 深さ: 軽量（checklist） vs 公式スキャン（時間・トークンコストあり）
4. 迷ったらユーザーに 1 問（スコープとエンジン）。セキュリティ・認可・課金・データに触れる変更は **深いスキャンまたは checklist の Critical 重点**をデフォルトにする

## ワークフロー A — Cursor 単体（デフォルト）

公式プラグインが使えない、またはユーザーが軽量レビューを指定した場合。

1. スコープ固定（`git diff` / `gh pr diff`、対象ブランチ名を記録）
2. [checklist.md](references/checklist.md) を上から適用（変更に auth/billing/data/migration タグがあれば 1–2 を必ず）
3. ドメイン特化は既存 omega へ委譲（Supabase → `supabase-code-review`、Next → `nextjs-code-review`）
4. [report-format.md](references/report-format.md) で出力（`エンジン: cursor`）

**禁止**: 公式スキャナの JSON / SARIF を手書きで捏造する。未実行のスキャンを「実行済み」と言わない。

## ワークフロー B — Claude Security

Claude Code が利用可能なとき。

1. プラグイン未インストールなら [claude-security.md](references/claude-security.md) のセットアップを案内
2. ジョブ選択: codebase / changes / suggest-patches（ユーザーが明示していればスキップ）
3. 公式 `claude-security` スキル・ジョブレシピに従い **Workflow を自分で代替しない**
4. 成果物ディレクトリ `CLAUDE-SECURITY-*` を正本に、[report-format.md](references/report-format.md) で要約（Finding ID `F\d+` を保持）

## ワークフロー C — Codex Security

Codex CLI + プラグインが利用可能なとき。

1. [codex-security.md](references/codex-security.md) のセットアップ確認
2. diff の有無で Standard / diff / Deep を選ぶ（`security-scan` SKILL の description に従う）
3. SDK 所有の `CODEX_SECURITY_SCAN_*` がある場合はそれに従い、二重スキャンしない
4. 完了後 `report.md` を正本に要約（手書きレポート禁止）

## 統一レポート

すべての経路の最終ユーザー向けサマリは [report-format.md](references/report-format.md) に揃える。チャットでは Critical を先に、根拠と修正案を 1 finding あたり短く。

## 限界・免責

補助ツールであり、SAST/DAST・依存スキャン・ペンテスト・人間レビューの代替ではない。false positive / false negative あり。本番前は組み込み CI と人間のレビューを維持する。

## 上流・同期

プラグイン本体の更新追従: [references/UPSTREAM.md](references/UPSTREAM.md)

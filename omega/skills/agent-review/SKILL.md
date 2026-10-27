---
name: agent-review
description: "担当分け並列 PR レビュー（正しさ×2 / 品質 / セキュリティ / 条件付き blast）。争点あるブランチ・PR で `/agent-review` を明示起動。成果物は `.cursor/agent-review/yyyy-mm-dd-<branch>/`。"
disable-model-invocation: true
---

# Agent review

**起動:** ユーザーが `/agent-review` で明示依頼したときのみ（omega `commands/` には載せない）。手順は [references/](references/) と [lanes/](lanes/) に分割する。

## 親（オーケストレーター）

1. 本ファイルを読む。
2. [references/orchestrator.md](references/orchestrator.md) を **全文**実行する。
3. フェーズごとに必要な reference だけ追加で読む（下表）。

| フェーズ | reference |
|----------|-----------|
| 0 成果物 | [artifacts.md](references/artifacts.md) |
| 1 base・差分 | [base-resolution.md](references/base-resolution.md) |
| 0.3 Router | [dimension-router.md](references/dimension-router.md) |
| 0.5 構造 | [structural-audit.md](references/structural-audit.md) |
| 1.9 モデル | [resolve-lane-models.md](references/resolve-lane-models.md) + `scripts/resolve-lane-models.mjs` — **Task 起動前必須** |
| 2.6 正しさ A×B | [lane-correctness-ab-format.md](references/lane-correctness-ab-format.md) |
| 2 統合 | [consolidation.md](references/consolidation.md)、[consolidated-output-format.md](references/consolidated-output-format.md) |

## サブエージェント（レーン）

プロンプトには **lane ファイルの絶対パス**（`/.cursor/skills/agent-review/lanes/...`）を埋め込む。

| レーン | ファイル |
|--------|----------|
| A Correctness（Codex） | [correctness-codex.md](lanes/correctness-codex.md) |
| B Correctness（Sonnet） | [correctness-sonnet.md](lanes/correctness-sonnet.md) |
| C Quality | [quality.md](lanes/quality.md) |
| D Security | [security.md](lanes/security.md) |
| E Blast radius | [blast-radius.md](lanes/blast-radius.md) + `blast-radius` スキル |

ドメイン準拠の参照先: [lane-map.md](references/lane-map.md)。

## Security レーンと code-security

オーケストレーター内の D レーンは Cursor の `security-review` サブエージェント。広い監査・パッチ提案は `/code-security`（別スキル）。→ [security-vs-code-security.md](references/security-vs-code-security.md)

## 限界

補助レビュー。CI・人間レビュー・ペンテストの代替ではない。

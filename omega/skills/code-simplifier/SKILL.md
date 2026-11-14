---
name: code-simplifier
description: "挙動を変えず直近 diff のコードを読みやすく整える。/code-simplifier、simplify、仕上げ、読みやすく、refine、ブラッシュアップ（コード）に使用。削減調査は /refactor-check、コメント査読は /no-comments（削除しない）。"
disable-model-invocation: true
---

# コード仕上げ

**最近触ったコード**を、機能・挙動を変えずに構造と表現だけ整える。編集は **code-simplifier** サブエージェントが行う。

**使う:** 本スキル（`/code-simplifier`）、実装直後の仕上げ、PR 前の cosmetic 整理（挙動 pin 済みまたは変更が小さいとき）。

**使わない:** 削減・層・追跡ホップの調査（編集しない）→ **`/refactor-check`**。コメント査読 → **`/no-comments`**（削除しない）。構造移行・契約変更 → **Refactoring プレイブック** + **`forge-agent`**。

## 境界

| ツール | 役割 |
|--------|------|
| 本スキル | スコープ内の **実装編集**（ネスト、命名、冗長なローカル抽象の整理） |
| `refactor-check` | レポートのみ。Must/Should 候補と commit 順 |
| `no-comments` | コメント査読のみ（削除しない） |
| `agent-review` | レビュー（readonly）。仕上げ編集は本スキル |

## Scope

1. ユーザー指定のパスがあればそれだけ。
2. なければベースブランチ（未指定時 `main` / `master`）に対する `git diff <base>...HEAD` の変更ファイル。
3. スコープ外ファイルは触らない。新 API・新機能・仕様変更は禁止。

## Steps

1. リポジトリルート（git root）とスコープ内ファイル一覧を確定する。
2. `Task` を `subagent_type: "code-simplifier"` で起動。`readonly: false`、`run_in_background: false`。`model` は [task-models.md](./references/task-models.md)（`forge-models.mdc` の `code-simplifier` 行）。プロンプトに **絶対パス・許可パス・禁止事項** を渡す。サブエージェントの Subagents / speed は **forge-mode** スキルに従う。
3. サブエージェントの diff をレビューする。スコープ逸脱・挙動変更・過剰抽象削除は reject し、最大 **1 回** だけ scope を絞って再実行。
4. 親が **`/verify-done`** または少なくとも TS なら `tsc --noEmit` と、触った領域の関連テストを実行する（**principle-prove-it-works**）。
5. 報告: 変更ファイル、reader-load の変化（1〜2 文）、検証結果。コミットはユーザーが依頼したときだけ。

## 上流

[claude-plugins-official/plugins/code-simplifier](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/code-simplifier)（Apache-2.0）。エージェント正本は `omega/agents/code-simplifier.md`。更新: [references/UPSTREAM.md](./references/UPSTREAM.md)、`scripts/sync-from-upstream.sh`。
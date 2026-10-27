# レーン model 解決（フェーズ 1.9・必須）

親は **Task を 1 体も起動する前**に、必ず本手順で `model` と `subagent_type` を決める。正本は **スクリプト出力の JSON のみ**（`forge-models.mdc` をスクリプトが読む）。注入ルール・記憶・手動の Default 指定は禁止。

一般ルールは [task-model-resolution.md](../../forge-mode/references/task-model-resolution.md) と同じ: **ロール行が無い・`inherit`・許可リスト外 slug → Task の `model` 省略（親チャットモデル）**。

## 1. スクリプト実行（正本）

対象 PJ の git ルートで:

```bash
node .cursor/skills/agent-review/scripts/resolve-lane-models.mjs
```

（別ルートから実行する場合は第 1 引数に PJ ルートを渡す。）

## 2. 出力の使い方

JSON の `lanes.A` … `lanes.E` それぞれ:

| フィールド | Task への反映 |
|------------|----------------|
| `subagent_type` | 必ず設定 |
| `model` | `omit_task_model: false` のとき **必ず** Task の `model` に設定 |
| `omit_task_model: true` | Task の `model` を省略（親チャットモデル） |

`warnings` が空でないときは、チャットと `consolidated.md` の Inputs に **Resolved lane models** と併記する。

## 3. 記録

`consolidated.md` の **Inputs** に次を載せる:

- `Resolved lane models:` — スクリプト出力の `lanes`（lane ID → `model` / `resolved_from`）

## 4. レーン定義（スクリプト内 `LANES` と同期）

| レーン | `forge-models.mdc` ロール行 | `subagent_type` |
|--------|-----------------------------|-----------------|
| A | `review orchestrator grok` | `generalPurpose` |
| B | `review orchestrator sonnet correctness` | `generalPurpose` |
| C | `review orchestrator sonnet quality` | `generalPurpose` |
| D | `review orchestrator security` | `security-review` |
| E | `review orchestrator blast radius` | `generalPurpose` |

## 5. Task 起動の共通オプション

- `readonly: true`
- オーケストレーター並列時: `run_in_background: true`
- レーン D: JSON の `omit_task_model` に従う。`security-review` が slug を拒否したときだけ `model` を省略し、チャットに記録する。

## 6. 検証

起動ログ・`consolidated.md` の model と、直前のスクリプト出力が一致していること。不一致なら **起動をやり直す**（再レビューはユーザー指示または `/agent-review` 再実行）。

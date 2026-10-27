# Task models

Security Lead（親）は `/code-security` コマンドの `model: inherit`。以下は **Task** の `model` のみ。

`model` の解決は [task-model-resolution.md](../../forge-mode/references/task-model-resolution.md) が正。各 spawn は `subagent_type: generalPurpose`、`run_in_background: true`（ジョブが別指定する場合はそちら）。

| 用途 | Role line（`forge-models.mdc`） |
|------|----------------------------------|
| inventory、baseline、investigator、researcher、patch-generator、adversarial researcher | `code security workers` |
| finding ごとの verifier 3 体（順に 1 slug ずつ） | `code security verifier panel` |
| suggest-patches の patch-verifier（単体） | 同上 **`verifier panel` の 2 番目の slug**（1 件だけならその slug） |

**Verifier panel（finding）:** slug を左から verifier 1 / 2 / 3 に割り当て。1 件だけなら 3 体とも同じ。2 件なら 1→2→1→2… でローテーション。slug が足りない verifier は `model` 省略（親チャットモデル）。

# Task models

Security Lead（親）は `/code-security` コマンドの `model: inherit`。以下は **Task** の `model` のみ。

各 spawn は `subagent_type: generalPurpose`、`run_in_background: true`（ジョブが別指定する場合はそちら）。`forge-models.mdc` の role 行と default を名指す。`model` はその行の値、ルールや行が無ければ default。値が `inherit` なら `model` は未設定。Task ツールが slug を拒否したら default を使い、その旨を述べる。default も拒否されたらエラーメッセージから同族の最も近い有効 slug を使う。

| 用途 | Role line | Default `model` |
|------|-----------|-----------------|
| inventory、baseline、investigator、researcher、patch-generator、adversarial researcher | `code security workers` | `grok-4.7-medium` |
| finding ごとの verifier 3 体（順に 1 slug ずつ） | `code security verifier panel` | `grok-4.7-medium`, `claude-sonnet-5-5-high`, `gemini-4-argon-medium` |
| suggest-patches の patch-verifier（単体） | 同上 **`verifier panel` の 2 番目の slug**（1 件だけならその slug） | `claude-sonnet-5-5-high` |

**Verifier panel（finding）:** slug を左から verifier 1 / 2 / 3 に割り当て。1 件だけなら 3 体とも同じ。2 件なら 1→2→1→2… でローテーション。

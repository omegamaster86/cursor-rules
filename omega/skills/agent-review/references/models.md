# Task models（agent-review レーン）

親オーケストレーターはフェーズ1の **Task 起動前**に `.cursor/rules/forge-models.mdc` を読む。各 spawn は `subagent_type` と下表の `model` を設定する（`code-security` の [task-models.md](../../code-security/references/task-models.md) と同様）。

- Role 行が無い、または値が `inherit` のとき: Default `model` を使う。`inherit` なら Task の `model` は省略可（親モデル継承）。
- slug が拒否されたら Default にフォールバックし、その旨を述べる。

| レーン | Role line（`forge-models.mdc`） | Default `model` | `subagent_type` |
|--------|----------------------------------|-----------------|-----------------|
| A Correctness（1本目） | `review orchestrator grok` | `gpt-5.3-codex` | `generalPurpose` |
| B Correctness | `review orchestrator sonnet correctness` | `claude-4.6-sonnet-medium-thinking` | `generalPurpose` |
| C Quality | `review orchestrator sonnet quality` | `claude-4.6-sonnet-medium-thinking` | `generalPurpose` |
| D Security | `review orchestrator security` | （行なしなら `model` 省略 — `security-review` 既定） | `security-review` |
| E Blast radius | `review orchestrator blast radius` | `claude-4.6-sonnet-medium-thinking` | `generalPurpose` |

すべて `readonly: true`。orchestrator 並列時は `run_in_background: true`。

**D:** `subagent_type: security-review` が `model` を無視する環境では、forge 行は記録用。Task が受け付けるときだけ `model` を渡す。

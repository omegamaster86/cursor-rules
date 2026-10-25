# レーン別モデル（既定）

`.cursor/rules/forge-models.mdc` に `review orchestrator` 行がある場合はそちらを優先する。

| レーン | 既定 model | subagent_type |
|--------|------------|---------------|
| A Correctness（Codex） | `gpt-5.3-codex` | `generalPurpose` |
| B Correctness（Sonnet） | `claude-4.6-sonnet-medium-thinking` | `generalPurpose` |
| C Quality | `claude-4.6-sonnet-medium-thinking` | `generalPurpose` |
| D Security | （サブエージェント既定） | `security-review` |
| E Blast radius | `claude-4.6-sonnet-medium-thinking` | `generalPurpose` |

すべて `readonly: true`。並列起動時は `run_in_background: true`。

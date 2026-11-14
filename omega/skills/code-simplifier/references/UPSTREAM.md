# UPSTREAM — code-simplifier

| 項目 | 値 |
|------|-----|
| 正本 | `claude-plugins-official/plugins/code-simplifier/`（repo 直下 submodule） |
| エージェント | `plugins/code-simplifier/agents/code-simplifier.md` |
| ライセンス | Apache-2.0（`references/LICENSE.txt`） |
| omega 配置 | `omega/agents/code-simplifier.md`（genai 規約・明示起動に適応） |
| オーケストレーション | `omega/skills/code-simplifier/SKILL.md`（omega 独自） |

## 同期

```bash
/path/to/cursor-rules/omega/skills/code-simplifier/scripts/sync-from-upstream.sh
```

1. 上流エージェントを `references/upstream-agent.en.md` にコピー
2. `references/LICENSE.txt` を更新
3. `omega/agents/code-simplifier.md` は **手マージ**（CLAUDE.md 節削除、genai rules 参照、自律起動削除）

submodule bump:

```bash
git submodule update --remote claude-plugins-official
```
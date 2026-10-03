# 自分用にする

## forge-models.mdc

ロール別 Task モデル。`/setup-forge` または `.cursor/rules/forge-models.mdc` を編集。

## PJ 固有

| 置き場 | 内容 |
|--------|------|
| `.cursor/skills/verify-*/` | 動作確認レシピ（omega 本体に含めない） |
| `.cursor/rules/` の追加 mdc | PJ だけの常時ルール |

## スキル追加

omega 正本に skill を足したら、各 PJ で `omega-link` を再実行（symlink 更新）。

**yomiyasu**（日本語推敲）は repo 直下 submodule + `omega/skills/yomiyasu/` 抜粋。上流 bump 後は `omega/skills/yomiyasu/scripts/sync-from-upstream.sh` と [README.md](../../../README.md)。`SKILL.md` / `writing-rules.md` は必要時手マージ。

**product-design** は Cursor 専用（browser MCP・`.cursor/product-design/`）。Codex CLI 用スキル同期には含めない。詳細は `omega/skills/product-design/SKILL.md`。

スキル authoring: forge-mode **authoring-a-skill** プレイブック、Cursor **create-skill**。

## 振り返り

- `engineer-retrospective` + `daily-chat-digest`
- `reflect` — 長タスク後にスキル edits へルーティング
- `study-log` — 学習を `.cursor/study-log/` に

次: [レシピと落とし穴](./10-recipes.md)

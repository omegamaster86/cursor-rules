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

スキル authoring: forge-mode **authoring-a-skill** プレイブック、Cursor **create-skill**。

## 振り返り

- `engineer-retrospective` + `daily-chat-digest`
- `reflect` — 長タスク後にスキル edits へルーティング
- `study-log` — 学習を `.cursor/study-log/` に

次: [レシピと落とし穴](./10-recipes.md)

# 離席・夜間

## decision-log

長時間 run・離席後のレビュー用の決定証跡は **decision-log**（Notion 正本）。「寝る」「戻ったら信頼したい」「/loop until X」とセットで使う。

## Autonomous run

単一タスクを止めず完走: **autonomous-run** プレイブック。

## Autopilot

| プレイブック | いつ |
|-------------|------|
| **autopilot-stack** | 検証済み linear stack を渡し、人が land |
| **autopilot-full** | PR ごと owner、swarm 検証後 merge（権限があるとき） |

## Orchestrate

多日・数十 PR・コーディネーター 1 チャット: **orchestrate** プレイブック。

- 状態: `bun .cursor/skills/forge-mode/scripts/orch/orch.ts`
- コーディネーターはコードを書かない。brief と drain が仕事

## Pause / Session pickup

中断: **pause-safely**。再開: **session-pickup**、**session-log**。

次: [原則で舵を取る](./08-principles.md)

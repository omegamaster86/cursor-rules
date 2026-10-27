---
name: reflect
description: "アクティブ transcript 上で 3 つの parallel review サブエージェントを spawn し、学びを surface し、各件を既存スキルへの具体 edit にルーティング。ユーザーが reflect と言ったときに使用。"
disable-model-invocation: true
---

# Reflect

現在の会話から durable な学びを mining し、skill edit にルーティングする。

ユーザーが「reflect」または `/reflect` と言ったとき起動。会話が trivial、off-topic、親が既存スキルを正しく踏んでいる場合はスキップ。一回限りは学びではない。

## 1. Locate the active transcript

fan-out 前に、system prompt が名指す `agent-transcripts/` でこの会話の transcript を見つける。`~/.cursor/projects/*/` を glob しない。workspace 境界を越え、無関係 project の private チャットを読む。

```bash
ls -t <agent-transcripts>/*.jsonl <agent-transcripts>/*/*.jsonl <agent-transcripts>/*/subagents/*.jsonl 2>/dev/null | head -10
```

legacy flat（`<id>.jsonl`）、current nested（`<id>/<id>.jsonl`）、subagent（`<parent>/subagents/<child>.jsonl`）をカバーする。各候補で JSONL 先頭行を読み、`message.content[0].text` に会話の opening user prompt が含まれるファイルを採用。どれもマッチしなければセッションの tight digest を渡す。

## 2. Spawn three reviewers in parallel

1 メッセージ、3 `Task` 呼び出し、`subagent_type: generalPurpose`、agent mode（`readonly: false`）。reviewer は transcript が参照する ticket、チャット thread、observability trace を MCP で調べる必要がある。readonly は MCP を剥がす。

各 reviewer と synthesizer の `model` は下表の Role 行で解決する（[task-model-resolution.md](../forge-mode/references/task-model-resolution.md)）。

| Lens | Role line（`forge-models.mdc`） | Prompt template |
|---|---|---|
| Judgment | `reflect judgment, divergent, synthesizer` | `references/judgment-reviewer.md` |
| Tooling | `reflect tooling` | `references/tooling-reviewer.md` |
| Divergent | `reflect judgment, divergent, synthesizer` | `references/divergent-reviewer.md` |

各 template をそのまま渡し、マーク箇所を transcript path または digest に置換。reviewer は `Task` 応答本文で findings を返す。

## 3. Synthesize

1 `Task` 呼び出し、`subagent_type: generalPurpose`、`model` は `reflect judgment, divergent, synthesizer` ロール行で解決、agent mode（`readonly: false`）。citation を MCP で spot 検証する。readonly は MCP を剥がす。`references/synthesizer.md` をそのまま使い、マーク箇所に各 reviewer の full output をインライン。Accepted / Rejected / Backlog リストを返す。

## 4. Structural enforcement check

lint rule、script、metadata flag、runtime check でより確実に強制できる Accepted 項目は Backlog に移す。**encode-lessons-in-structure** principle スキルを参照。

## 5. Apply

Accepted edit を適用する前に、synthesizer の full Accepted/Rejected/Backlog 出力をユーザーに提示し、明示承認を待つ。ユーザーが適用 subset を選び、routing を差し替え可能。skill 変更は org の将来の全 agent に効く。auto-apply しない。

Backlog 項目はチームの devex / backlog tracker に filing。承認待ちは Accepted リストだけ。

承認された各行の Routing を厳守：

- Trivial 既存スキル edit（1 行 bullet、文の tighten、古い fact 修正）：親が直接。
- Substantive 既存スキル edit（新 section、新 pattern 表、~10 行超）：Cursor 組み込み `create-skill` に渡し draft / test / iterate loop。
- `tune description: <skill path>`（スキルはあるが trigger すべきとき踏まなかった）：`create-skill` の description 最適化 loop。
- `new skill via create-skill: <kebab-name>`：作成は `create-skill`。形を ad hoc で発明しない。

環境に SKILL.md validator があれば、触った skill ごとに完了宣言前に実行。

## 6. Summarize for the user

短いリスト、前置きなし：

- Edits applied: `<skill path>`. 各 1 行で何が変わった。
- New skills created: `<skill path>`. 各 1 行（稀）。
- Backlog filed to the devex tracker: `<issue title>` (`<tags>`). 各 1 行。
- Dropped: synthesizer の rejected 理由を 1 行ずつ。

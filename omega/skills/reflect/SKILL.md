---
name: reflect
description: "アクティブ transcript 上で 3 つの parallel review サブエージェントを spawn し、学びを surface し、各件を既存スキルへの具体 edit にルーティング。ユーザーが reflect と言ったときに使用。"
disable-model-invocation: true
---

# Reflect

現在の会話から durable な学びを mining し、skill edit にルーティングする。

## When to invoke

ユーザーが「reflect」または `/reflect` と言ったとき起動。会話が trivial、off-topic、親が既存スキルを正しく踏んでいる場合はスキップ。一回限りは学びではない。

## Process

### 1. Locate the active transcript

fan-out 前に親が自分の transcript file を特定。system prompt がアクティブ workspace の `agent-transcripts/` を名指す。その path を使う。`~/.cursor/projects/*/` を glob しない。workspace 境界を越え、無関係 project の private チャットを読む。

```bash
ls -t <agent-transcripts>/*.jsonl <agent-transcripts>/*/*.jsonl <agent-transcripts>/*/subagents/*.jsonl 2>/dev/null | head -10
```

3 つの transcript レイアウト：legacy flat（`<id>.jsonl`）、current nested（`<id>/<id>.jsonl`）、subagent（`<parent>/subagents/<child>.jsonl`）。

各候補で JSONL 先頭行を読み、`message.content[0].text` に会話の opening user prompt が含まれるか確認。マッチする path を採用。path が解決しなければセッションの tight digest を書きそれを渡す。

### 2. Spawn three reviewers in parallel

1 メッセージ、3 `Task` 呼び出し、`subagent_type: generalPurpose`、`model` は下記、agent mode（`readonly: false`）。reviewer は transcript で参照された ticket、チャット thread、observability trace の context lookup に MCP が要る。readonly は MCP を剥がす。

各 reviewer と synthesizer は `forge-models.mdc` ルールの role 行と default を名指す。`model` はその行の値、ルールや行が無ければ default。値が `inherit` なら `model` は未設定。Task ツールが slug を拒否したら default を使い、その旨を述べる。default も拒否されたらエラーメッセージから同族の最も近い有効 slug を使う。

| Lens | Role line | Default `model` | Prompt template |
|---|---|---|---|
| Judgment | `reflect judgment, divergent, synthesizer` | `claude-opus-5.5-thinking-medium` | `references/judgment-reviewer.md` |
| Tooling | `reflect tooling` | `cursor-grok-4.6-medium` | `references/tooling-reviewer.md` |
| Divergent | `reflect judgment, divergent, synthesizer` | `claude-opus-5.5-thinking-medium` | `references/divergent-reviewer.md` |

各 template をそのまま渡し、マーク箇所を transcript path または digest に置換。reviewer は `Task` 応答本文で findings を返す。

### 3. Synthesize

1 `Task` 呼び出し、`subagent_type: generalPurpose`、`model` は `reflect judgment, divergent, synthesizer` 行（default `claude-opus-5.5-thinking-medium`）、agent mode（`readonly: false`）。synthesizer の quality check は citation spot 検証で MCP が要る場合がある。readonly は MCP を剥がす。`references/synthesizer.md` をそのまま使い、マーク箇所に各 reviewer の full output をインライン。synthesizer は構造化 Accepted / Rejected / Backlog リストを返す。

### 4. Structural enforcement check

synthesizer の Accepted リストを sanity-check。lint rule、script、metadata flag、runtime check でより確実に強制できる項目は Accepted から Backlog に移す。**encode-lessons-in-structure** principle スキルを参照。

### 5. Apply

Accepted edit を適用する前に、synthesizer の full Accepted/Rejected/Backlog 出力をユーザーに提示し、明示承認を待つ。ユーザーが適用 subset を選び、routing を差し替え可能。skill 変更は org の将来の全 agent に効く。auto-apply しない。

Backlog 項目はチームの devex / backlog tracker に自動 filing。承認待ちは Accepted リストだけ。

承認された Accepted 項目ごとに Routing field を厳守：

- Trivial 既存スキル edit（1 行 bullet、文の tighten、古い fact 修正）：親が直接。
- Substantive 既存スキル edit（新 section、新 pattern 表、~10 行超）：Cursor 組み込み `create-skill` に渡し draft / test / iterate loop。
- `tune description: <skill path>`（スキルはあるが trigger すべきとき踏まなかった）：`create-skill` の description 最適化 loop。
- `new skill via create-skill: <kebab-name>`：作成は `create-skill`。形を ad hoc で発明しない。

環境に SKILL.md validator があれば、触った skill ごとに完了宣言前に実行。なければスキップ。

### 6. Summarize for the user

短いリスト、前置きなし：

- Edits applied: `<skill path>`. 各 1 行で何が変わった。
- New skills created: `<skill path>`. 各 1 行（稀）。
- Backlog filed to the devex tracker: `<issue title>`（`<tags>`）。各 1 行。
- Dropped: synthesizer の rejected finding ごとに 1 行 + 理由。

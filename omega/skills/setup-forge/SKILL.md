---
name: setup-forge
description: forge-mode のロール別モデルと reasoning budget を設定する。利用可能 slug を検出し always-applied ルールを書く。/setup-forge、「forge のモデル設定」「forge budget」に使用。
disable-model-invocation: true
---

# Setup forge

`~/.cursor/rules/forge-models.mdc` を書き、forge-mode のロールごとのモデルを上書きする。PJ に omega を `omega-link` 済みなら、テンプレは `.cursor/rules/forge-models.mdc`（PJ コピー）を編集してもよい。

## Steps

### 1. 利用可能モデルを検出

このセッションで `Task` サブエージェントに渡せる model slug を列挙する。検出できないときはユーザーに slug 一覧を貼るよう依頼する。未確認の slug は書かない。`inherit` は常に有効。

### 2. 現状を読む

デフォルトの形は下記 step 5。`~/.cursor/rules/forge-models.mdc` または PJ の `.cursor/rules/forge-models.mdc` があれば `# budget` 行と各ロール値を現状として読む。step 5 に無いロール行（例: 廃止された `how critics`）は落とす。

### 3. Budget、マップ、確認

**(a) budget を聞く。** AskQuestion を優先。次の 4 択（ラベルはそのまま）。既存 budget があれば名指す。ルールが無いときは `large` がスキルデフォルトと同じと伝える。

- `unlimited — max reasoning`
- `large — xhigh reasoning`
- `medium — high reasoning`
- `small — medium reasoning`

**(b) 適用。** スキルデフォルトから作業表を構築。再実行時はユーザーが変えたロールはファミリ・リスト・`inherit` を保持。`unlimited` / `large` / `medium` / `small` は実 slug の effort を `max` / `xhigh` / `high` / `medium` に下げる（`max` > `xhigh` > `high` > `medium` > `low`、末尾 `fast` の前のトークンが effort）。結果が検出集合に無ければ同ファミリで target 以下の最高 effort、なければ要選択。`inherit` は変えない。Grok 系は effort の上限が `xhigh` のことが多い。

**(c) ロール一覧を見せて確認。** 検出外 slug は要選択とマーク。step 2 で落とした行も列挙。そのままかロール単位で変更かを聞く。リスト型ロール（`multi-agent-candidates runners`、`architect runners`、`review orchestrator *`）はエントリ数＝fan-out 数。`swarm workers` は各ワーカーのデフォルト（レース arm は brief で別指定可）。

### 4. 検証

書く実 slug はすべて検出集合に含める。`inherit` は常に OK。

### 5. ルールを書く

`alwaysApply: true`、idempotent にファイル全体を上書き。`# budget` 行を含める。形:

```
---
description: forge-mode ロールごとのモデル選択（スキルデフォルトの上書き）
alwaysApply: true
---
# forge-mode model configuration
# `inherit` のロールは親チャットモデルで走る（Task の `model` を省略）
# budget: large (xhigh)
feature, refactoring: cursor-grok-4.6-medium
bug-fix: cursor-grok-4.6-medium
perf-issue: cursor-grok-4.6-medium
hillclimb: cursor-grok-4.6-medium
judgment and prose: claude-opus-5.5-thinking-medium
hardest tasks: claude-opus-5.5-thinking-medium
how explorer: cursor-grok-4.6-medium
how explainer: claude-opus-5.5-thinking-medium
why investigators: cursor-grok-4.6-medium
why synthesizer: claude-opus-5.5-thinking-medium
reflect tooling: cursor-grok-4.6-medium
reflect judgment, divergent, synthesizer: claude-opus-5.5-thinking-medium
multi-agent-candidates runners: claude-opus-5.5-thinking-medium, cursor-grok-4.6-medium
swarm workers: cursor-grok-4.6-medium
architect runners: claude-opus-5.5-thinking-medium, cursor-grok-4.6-medium
review orchestrator grok: cursor-grok-4.6-medium
review orchestrator sonnet correctness: claude-sonnet-5-thinking-medium
review orchestrator sonnet quality: claude-sonnet-5-thinking-medium
```

### 6. 確認

ルールを書いた旨と、新セッションから適用される旨を伝える。再実行で更新できる。

### 7. verify スキル（任意）

PJ に `verify-*` や実アプリ drive 手段が無ければ一度だけ提案: `/create-verification-skill` でユーザー操作の証明レシピを生成できる。yes なら実行。no なら押し付けない。

---
name: setup-pstack
description: pstack がロールごとに使用するモデルを設定する。利用可能なモデルを検出し、スキルのデフォルトを上書きする常時適用ルールを書き込む。/setup-pstack、「pstack のモデルを設定」、pstack のモデル選択を変更するときに使用。
---

# Setup pstack

`~/.cursor/rules/pstack-models.mdc` を書き込む。これは常時適用ルールで、pstack のロールごとのモデルを設定する。スキルはこれを読み、行が欠けている場合はインラインのデフォルトにフォールバックする。つまりこれは上書きレイヤーであり、必須ではない。

## 手順

### 1. 利用可能なモデルを検出する

このセッションで `Task` サブエージェントに渡せるモデル slug を列挙する。これが信頼できる情報源。Cursor がユーザーの利用権限のあるモデルを一覧する API や CLI も公開していれば、完全性のためにそちらを優先する。何も検出できない場合は、ユーザーにアクセスできる slug を貼り付けてもらう。利用可能であることを確認していない slug は書き込まない。

### 2. 現在の状態を読み込む

デフォルトのロールとモデルの対応は、下記ステップ 5 のルール形式に示されている。`~/.cursor/rules/pstack-models.mdc` が既に存在する場合は読み込み、その値を現在の選択として扱う。なければそのデフォルトから始める。

### 3. マッピングして確認する

検出セットにないモデルを使っているロールには選択が必要である旨を示しつつ、全ロールと現在のモデルを表示する。現状のまま受け入れるか、特定のロールを変更するかを尋ね、検出したモデルを選択肢として提示する。自由入力より `AskQuestion` を優先する。パネルロール（how の critic、arena の runner、architect の runner、interrogate の reviewer）の値はリストであり、モデルごとにサブエージェントが 1 つ起動する。リストの長さが数を決める。

### 4. 検証する

書き込む slug はすべて検出セットに含まれていること。選択した slug が利用できない場合は停止して再確認する。ユーザーが使えないモデルを指すルールは、それを読むすべての委譲を壊す。

### 5. ルールを書き込む

`alwaysApply: true` とロールごとに 1 行で `~/.cursor/rules/pstack-models.mdc` を書き込む。poteto-mode と同じラベルを使う。再実行時も冪等にするため、ファイル全体を上書きする。形式:

```
---
description: pstack per-role model choices (overrides skill defaults)
alwaysApply: true
---
# pstack model configuration. One line per role. Delete a line to fall back to the skill default.
feature, refactoring: composer-2.5-fast
bug-fix: gpt-5.5-high-fast
perf-issue: gpt-5.5-high-fast
hillclimb: gpt-5.5-high-fast
judgment and prose: claude-opus-4-8-thinking-xhigh
how explorer: composer-2.5-fast
how explainer: claude-opus-4-8-thinking-xhigh
how critics: claude-opus-4-8-thinking-xhigh, gpt-5.5-high-fast, composer-2.5-fast
why investigators: composer-2.5-fast
why synthesizer: claude-opus-4-8-thinking-xhigh
reflect tooling: composer-2.5-fast
reflect judgment, divergent, synthesizer: claude-opus-4-8-thinking-xhigh
arena runners: claude-opus-4-8-thinking-xhigh, gpt-5.5-high-fast, composer-2.5-fast
architect runners: claude-opus-4-8-thinking-xhigh, gpt-5.5-high-fast, composer-2.5-fast
interrogate reviewers: claude-opus-4-8-thinking-xhigh, gpt-5.5-high-fast, composer-2.5-fast
```

### 6. 確認する

ルールが書き込まれたこと、新しいセッションに適用されることを伝える。このスキルを再実行すると更新される。

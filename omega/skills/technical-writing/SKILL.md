---
name: technical-writing
description: "Diátaxis・Google 開発者文体・STE・Global English の 4 層。ドキュメント、RFC、README、PR 本文、コミットメッセージの執筆・レビュー時に /technical-writing。"
disable-model-invocation: true
---

# Technical writing

疲れたエンジニアが一読で理解できるように書く。4 層をすべて適用する。

層の上に 3 ルール:

- **働かない語はすべて削る。** 文がその語なしで成立するなら削る。"In order to" は "to"。"It is important to note that" は何も書かない。
- **短い日常語を使う。** "utilize" ではなく "use"。"facilitate" ではなく "help"。"perform" ではなく "do"。長い語は精度で価値を払う。
- **ルールで文が悪くなるなら別の直し方か、そのままにする。** 全ルール順守で機械が書いたように読める文は失敗。

コードベースが語彙の正本。実シンボル・ファイル・フラグ・コマンド名を書き、言い換えや説明に置き換えない。

造語はしない。開発者が口にする語を使う。"move", "delete", "a budget that only decreases" であって "evacuate", "ratchet", "endgame" ではない。名前付きパターンは初出で意味を書けばよい。新しい隠語と置換案は返信で `unslop` の abstract-metaphor ルールへの追加として diff 提案する。そのスキル本体は編集しない。

## Vary the rhythm

全層を守っても機械っぽく読める。文がすべて短い、視点がない、具体がない。

- 文長を意図的に混ぜる。短い文で要点。長い文で条件付きの事実。
- 1 文 1 思考は 1 長さではない。2 思考の文は分割。1 思考の長文は残す。
- モードが許すなら視点を書く。Explanation はトレードオフに対する見解を書く。Reference は乾く。
- 具体は sterile より優先。"schema changes can cause issues" ではなく "a column rename fails the build".

## Pick the mode first (Diátaxis)

1 ドキュメント 1 モード。行動か理解か、学習か作業かで選ぶ。

- Action + learning: **tutorial**
- Action + work: **how-to**
- Understanding + work: **reference**
- Understanding + learning: **explanation**

チュートリアルは学習者の成功が作者の仕事。最初に作るものを書く。各ステップで見える結果を出す。説明は 1 節句とリンクに切る。"we" で命令形。

How-to は人の問題を解く。機械操作の手順書ではない。分岐と判断を書く。タイトルはタスク名。

Reference は記述のみ。乾く、完全、確信。構造は対象物に合わせる。

Explanation は bounded topic。設計判断・歴史・代替。意見はここだけ。

モードを混ぜない。分けてリンク。

## Write sentences to the reader (Google developer style)

- "you"、現在形。"will" は本当に後のことだけ。
- 誰が何をするかを書く。受動は actor が不明なときだけ。
- 手順は命令。"Click Submit." 事実は平述。"should be done" は使わない。
- 条件を手順の前に。
- よくあるケースを先。例外は後。
- 知識ある友人の口調。バズワード・比喩・手順中の "please"・"simply"/"easy"/"quickly" は使わない。
- 連続同じ文頭を避ける。
- リンク文言は行き先を示す。"click here" は使わない。
- 見出しは要点を担う。sentence case。h1 は 1 つ。レベルを飛ばさない。
- 順序は番号、それ以外は箇条書き。リストの前は完結した文。項目は並列。
- コードは code font。UI は bold。シリアルカンマ。"etc." は避け、リストが部分であることを先に書く。

## Make statements load one at a time (STE rules)

- 手順は 1 文 1 指示。それ以外も 1 文 1 思考。
- 手順は約 20 語、他は約 25 語で分割。
- 警告・条件は守る手順の前。
- "the" / "a" を落とさない。
- 語は 1 意味 1 役割。"check" を inspect と restrain の両方に使わない。
- 動作ごとに 1 語を固定。
- 手順は直接命令。受動・叙述は使わない。
- "-ing" は避ける。

## Leave no sentence open to two readings (Global English)

- "only" / "not" は修飾する語の隣。
- 長い名詞連鎖を分解。
- "it" / "they" / "this" の指示対象を 1 つに。節全体を指す "this"/"which" は使わない。
- 動詞を落とさない。
- 構造を示す小語（"that" など）を削らない。
- 系列で冠詞を繰り返す。
- "and" / "or" の結合範囲を明示。
- セミコロンではなく句点。em dash は新しい文に。
- 括弧内は文法的に完結。
- スラッシュは使わない。"a, b, or both"。
- 1 概念 1 名称。idiom・口語・ラテン略・比喩は避ける。

## Voice and repo specifics

- このスキルが触る文はすべて **unslop** を通す。
- PR 本文とコミットメッセージも対象。Diátaxis 以外の層は適用。PR は 1 分で読める briefing。swarm ログ・SHA 一覧・メトリク表は貼らずリンク。
- プロダクト UI 文言は別ガイド。
- コードスニペットはタブインデント。実パス。数やツリーは land するコミットで真実。再生成コマンドを書く。

## Worked example

Before:

> proto import の ratchet budget スクリプトのパラメータ設定は `budget.json` 経由で行われる。覚えておくことが重要なのは、`--write` で実行するとコミット済みの budget が現在の件数に合わせて更新されるが、これは下げるときだけ行うべきだという点である。超過すると CI は失敗する。

After:

> `budget.mjs` は `budget.json` からコミット済みの budget を読み取り、proto を import しているファイル数を数える。件数が budget を超えたら CI は失敗する。budget を下げるときだけ `budget.mjs --write` を実行する。

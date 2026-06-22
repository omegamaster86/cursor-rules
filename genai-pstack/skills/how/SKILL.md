---
name: how
description: "「how does X work」、変更前のコードウォークスルー、配置/所有/レイヤリングの質問（「where should this live」「which package owns this」「is this the right layer」）に使用。サブシステムアーキテクチャ、ランタイムフロー、オンボーディングのメンタルモデルを説明。アーキテクチャ批判可。"
---

# How

コードベースを探索し「how does X work?」に答える。シニアエンジニアがサブシステムにオンボードするレベルの明確なアーキテクチャ説明。注釈付きソースコードではなく、動くメンタルモデルに十分。

2 モード:

1. **Explain**（デフォルト）。コードベースを探索し明確な説明を産出
2. **Critique。** まず説明し、複数モデルを起動して独立にアーキテクチャ問題を特定

## Explain モード

### ステップ 1. 質問を理解し複雑さを評価

ユーザーが聞いていることを解析:

- "How does the rate limiter work?" → サブシステム
- "How do we handle billing for on-demand usage?" → 機能フロー
- "How is the auth service structured?" → アーキテクチャ概要
- "Walk me through what happens when a user submits a form" → ランタイムトレース

スコープを特定。曖昧なら最善の解釈を述べてから探索。聞かない。ずれていればユーザーがリダイレクト。

**複雑さを評価しアプローチを決める:**

- **Simple**（単一モジュール、小ユーティリティ、「function X はどう動くか」など狭い質問）: explorer をスキップ。explainer が 1 パスで探索・説明。ステップ 2b へ。
- **Complex**（複数ファイル/サービスにまたがるサブシステム、横断機能、フルアーキテクチャ概要）: 先に並列 explorer を起動し explainer に渡す。ステップ 2a へ。

迷ったら simple に寄せる。explainer が壁に当たったら explorer を起動できる。

### ステップ 2a. 探索（複雑な質問のみ）

質問を 2〜4 の並列探索角度に分解。各角度はサブシステムの異なるスライスで explorer の重複を防ぐ。「how does the rate limiter work?」の例:

- Explorer 1: データモデルと状態管理
- Explorer 2: リクエストパスとエンフォースメント
- Explorer 3: 設定とメトリクス基盤

分解は質問次第。判断を使う。狭い質問は 2 explorer で可。広いサブシステムは最大 4。

1 メッセージですべての explorer を起動:

- `subagent_type`: `generalPurpose`
- `model`: 設定済み how-explorer モデル（デフォルト `composer-2.5-fast`）
- `readonly`: `true`

各 explorer は `references/explorer-prompt.md` のベースプロンプトに、そのスライスを名指す探索角度を加える。各 explorer は:
- 広く始める: 関連ディレクトリを Glob、主要型/interface/クラス名を Grep
- 糸を辿る: エントリポイントから呼び出しチェーン（呼び出し元、被呼び出し、データフロー、型定義）
- 実コードを読む。ファイル名から推測しない
- 入力から出力（またはトリガーから効果）まで手を振らず説明できるまで続ける
- 驚くこと、非自明、新参が誤解しそうなことを記す

各 explorer は構造化所見を返す: 見つけたコンポーネント、トレースしたフロー、読んだファイル、非自明なもの。explorer 間の重複は可。explainer が調整。

ステップ 3 へ。

### ステップ 2b. 直接説明（単純な質問）

1 つの Task サブエージェントで 1 パス探索・説明:

- `subagent_type`: `generalPurpose`
- `model`: 設定済み how-explainer モデル（デフォルト `claude-opus-4-8-thinking-xhigh`）
- `readonly`: `true`

エージェントが自分で探索（Glob、Grep、Read）し直接説明を書く。`references/explainer-prompt.md` でコミュニケーションスタイルと出力形式。同じ構造、explorer 所見入力なし。

ステップ 4 へ。

### ステップ 3. 統合（複雑な質問のみ）

全 explorer が戻ったら、1 つの Task サブエージェントで所見を 1 つの一貫説明に統合:

- `subagent_type`: `generalPurpose`
- `model`: 設定済み how-explainer モデル（デフォルト `claude-opus-4-8-thinking-xhigh`）
- `readonly`: `true`

explainer は全 explorer 所見を受け、人向け説明を書く（下記出力形式）。`references/explainer-prompt.md` でフルテンプレート。重複を調整、矛盾を解決、スライスを統一像に織る。

### ステップ 4. 提示

explainer の出力をユーザーに提示。明瞭化の軽い編集や会話からのコンテキスト追加は可。大幅な書き換えはしない。explainer のコミュニケーションが成果物。

### 出力形式

質問に合わせてこの構造。すべての質問にすべての節は不要。

**Overview.** 1〜2 段落。何か、何をするか、なぜ存在するか。読み続けるか判断するのに十分。

**Key Concepts.** 重要な型、サービス、抽象。各に短い定義。網羅ではなく、残りを理解するのに要るもの。

**How It Works.** 説明の核。フローを歩く: 何がトリガーか、段階的に何が起きるか、データの行き先、判断点。散文。疑似コードではない。読者が見に行けるよう特定ファイルと関数を参照。本当に必要なとき以外コードブロックをダンプしない。

**Where Things Live.** 関連ファイル/ディレクトリの短いマップ。すべてではなく、この領域で作業を始めるのに要るもの。

**Gotchas.** 非自明、驚く振る舞い、変に見える理由の歴史、既知の鋭い角。

## Critique モード

ユーザーが理解だけでなくアーキテクチャ問題、改善を求めたときにトリガー。

### ステップ 1. まず説明

上記 explain フロー（ステップ 1〜4）をフル実行。批判の前にアーキテクチャを理解しなければならない。

### ステップ 2. Critic を起動

説明完了後、設定済み how-critics リストのモデルごとにアーキテクチャ critic を 1 人、1 メッセージで起動（デフォルト `claude-opus-4-8-thinking-xhigh`、`gpt-5.5-high-fast`、`composer-2.5-fast`）。

各 critic:
- `subagent_type`: `generalPurpose`
- `model`: how-critics リストの 1 モデル。最低推論レベル。アーキテクチャがより深い分析を要すればリードがエスカレート。
- `readonly`: `true`

`references/critic-prompt.md` でテンプレート。各 critic は受け取る:
1. ステップ 1 の説明（再探索不要）
2. 関連ファイルパス（実コードを読むため）
3. `references/critique-rubric.md` のアーキテクチャ批判ルーブリック

### ステップ 3. リード判断

interrogate スキルと同じフレームワーク。実務的リードであり集約器ではない。

所見を分類:
- **Act on.** 今直す価値のあるアーキテクチャ問題
- **Consider.** 実在する懸念だがコスト/便益が不明
- **Noted.** 正当な観察、優先度低
- **Dismissed.** 誤り、コンテキスト欠如、スタイル好み

まずステップ 1 の説明を提示し、その下に批判判定。説明は単体で立つ。理解だけしたい人が批判に溺れないように。

---
name: architect
description: "実装前に型・シグネチャ・モジュール構造をスケッチし、実装が埋まる間もループに留まる。/architect、「architect this」「design this」、いきなりコードに飛ぶと間違った形にロックインする非自明な作業に使用。"
disable-model-invocation: true
---

# Architect

実装前に設計する。`not implemented` 本体と疑似コードで型、関数シグネチャ、クラス形状、モジュール境界をスケッチする。複数モデル視点を統合し、選ばれたスケッチに対してコードを埋める。実装がスケッチの誤りを証明したら捨てて再設計する。

## 開始

開始前にフェーズごとに 1 項目の todolist を開く。チェックポイントなしの自律モードでは、リストがフェーズ位置を示し、フェーズが静かに消えるのを防ぐ。

1. Ground
2. Sketch
3. Agree
4. Implement
5. Scrap

## フェーズ A: 問題を土台固めする

新コードが触れるすべてのシステムの実際のメンタルモデルを構築する。関連サブシステムに **how** スキルを実行する。既存構造が制約、または設計がそれに押し返す必要があるときは critique モード。

ファイル名を挙げるだけは土台固めではない。`how` が規定するトレース済みモデルを出す。設計が所有権やレイヤリングを再定義するなら、`git log` / `gh pr view` で既存形の経緯を確認し、根拠を推測ではなく制約にする。

周囲に統合するシステムが本当にない純粋なグリーンフィールド作業だけフェーズ A をスキップ。

## フェーズ B: スケッチ

設計スケッチタスクとフェーズ A の土台固め成果物で **multi-agent-candidates** スキルを実行する。各 runner に `references/runner-prompt.md` を渡す。各候補は `references/rationale-template.md` の形の設計パッケージを出す。

**`.cursor/rules/multi-agent-task-enforcement.mdc` を厳守。** 親が単一応答で 3 案を書くのは禁止 — **同一メッセージで Task を 3 回** `run_in_background: true` で起動する。

**扇状展開ターンでは統合設計を出さない。** Task 起動 → Runners 下書き（`in_progress`）→ ターン終了。subagent 完了後の収集ターンで各 runner の `<model-slug>.md` を読み、**チャット統合出力**（multi-agent-candidates スキル参照）と **Synthesis decision** を出す。

### multi-agent-candidates のモード選択（Frame で必須）

| 状況 | モード | 親の仕事 |
|------|--------|----------|
| 単一判断（フィールド要否、命名、1 契約の詰め） | **`compare-models`** | フェーズ A で **採用立場を 1 つ確定** → [`compare-models-brief-template.md`](../multi-agent-candidates/references/compare-models-brief-template.md) を埋める → 3 **異なるモデル**に **同一 brief** |
| 根本的に異なる形の比較（配列 vs Map 等） | **`explore-shapes`** | 候補 1/2/3 に **異なる Assigned shape** を書く → **同一モデル** を 3 回 |

**ルーティング例:**

- 「`source_key` は要るか？」→ `compare-models`
- 「API レスポンスをどう簡略化するか（形の選択肢）」→ まず Ground で候補形を列挙 → `explore-shapes`

**禁止:** `compare-models` で runner にバラバラの立場を割り当てる（立場×モデルの交絡）。

**`explore-shapes` のみ:** 1 つの形の中の点修正ではなく、形全体の代替案を探索する。

multi-agent-candidates は 1 つの統合設計パッケージを返す。統合メモの **Runners** 表と **Dropout** 節も必須。**Runners の Status が確定する前に Synthesis decision を書かない。**

## フェーズ C: 合意（オプトイン）

デフォルト: 統合設計のまま実装へ直行。人のチェックポイントなし。

呼び出し側が明示的に求めたときだけチェックポイント: 「/architect with checkpoint」「実装前に止めて見せて」など。統合設計を提示し、承認待ち。

どちらでも統合は単独コミットとして出荷できる。**foundational-thinking**（`forge-mode/principles/foundational-thinking.md`）の「scaffold first」モード。以降のコミットは安定契約に対する本体の充填として読める。充填は計画・スコープ内で進め、完了前に **`/verify-done`** で検証する。実装前に設計へ敵対的圧力をかけるなら、統合スケッチに **`review-orchestrator-triple-hybrid` コマンド**を実行。

人が形に押し返したら（チェックポイント中または事後）、フェーズ A の証拠として扱う。さらにコードを書く前に再土台固めしフェーズ B を再実行。

## フェーズ D: スケッチに沿って実装する

`not implemented` 本体をコードに、疑似コードをロジックに置き換える。統合スケッチが契約。

スケッチからの逸脱は、黙って吸収する摩擦ではなく、表面に出す価値のあるシグナル。スケッチにないパラメータが要るなら、スケッチが間違いか、要件の見落としか、実装の過剰かを問う。表面に出す。ねじ込まない。

## フェーズ E: アーキテクチャが間違っているときは捨てる

実装がスケッチが吸収できない摩擦を繰り返し出すなら、スケッチを捨てる。間違った設計に修正をねじ込まない。

シグナルは*パターン*であり単発ではない。兆候:

- 無関係なコード横断で同じ形の回避策が繰り返し現れる。
- 無関係なエッジケースがすべて特別分岐を要する。
- コンパイルのため `any`、キャスト、実際は常に設定される optional が要る型。
- スケッチが状態は共有されないと言ったのに「ロックが要る」反射。
- 呼び出し側が抽象の内部ルールを知らないと使えない。
- 実装横断で同じ形のフェーズ D 逸脱が 2 つ以上独立して起きる。

判断を使う。書き直しシグナルは同形の繰り返し摩擦であり、単発の難ケースではない。

捨てるとき:

1. 構築済みに **how** スキルを再実行。
2. 新制約が初日からあったかのように再設計する。
3. 追加の前に削る（**refactor-check**）。
4. フェーズ B に戻り multi-agent-candidates を再実行（モードを見直す）。

## 成果物

呼び出し側の使い方を先に書き、型スケッチはそこから導く。根拠は `references/rationale-template.md` の形で併せて出荷。収集ターンでは **チャット統合出力**（multi-agent-candidates 必須節）を含む。

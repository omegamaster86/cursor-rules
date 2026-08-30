# 根拠テンプレート

型スケッチと併せて出荷する文章。1 ページ。見出しは sentence case、定型文なし。イタリックの注記を実内容に置き換える。

## Chat summary（runner が必ず埋める・親がチャットに転記しやすい形式）

*収集ターンで親が統合するため、runner 出力ファイル（`<model-slug>.md` 等）の冒頭近くに置く。5 項目すべて埋める。*

- **Answer:** *質問への 1 文回答*
- **Mode:** *`compare-models` または `explore-shapes`*
- **Recommended wire shape:** *JSON または swagger 抜粋を 1 コードブロック（省略しない）*
- **Key risk:** *1 行*
- **Unique vs other runners:** *同一 brief 下での差分、または explore-shapes での立場の核心を 1 行*

## Problem

*1 段落。何をしようとしているか、既存システムや制約の何が形を自明でなくしているか。[フェーズ A](../SKILL.md#phase-a-ground-the-problem) で表面化した制約があればここに名指しする。*

## Usage (caller's view)

*型スケッチの前に書く。呼び出しサイト 2〜3 個。何を import し、何を呼び、何が返るか。[Shape](#shape) はここから導く。*

## Shape

*データ構造 → シグネチャ → モジュールマップ。型にエンコードした不変条件、検証の所在。*

## Synthesis decision

*[multi-agent-candidates](../../multi-agent-candidates/SKILL.md) の **親オーケストレータ** が、全 runner 完了後の収集ターンでのみ埋める。runner 起動ターンでは「pending — awaiting orchestrator」。*

### Runners

*モードに応じた表（multi-agent-candidates スキル参照）。Status 確定前に Synthesis 本文を書かない。*

### Dropout

*なしなら `none`。*

## Tradeoffs accepted

*「X を引き換えに Y を受け入れる」形式で 1 項目ずつ。*

## Alternatives considered

*設計上の代替 ≥1（他 runner との差別化ではない）。負けた理由を 1 行。*

## Open questions and risks

*人が判断すべきこと。質問形式で。*

## Next implementation step

*1 文。*


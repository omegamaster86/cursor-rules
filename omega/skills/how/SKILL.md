---
name: how
description: "「X はどう動くか」、変更前のコード walkthrough、配置・所有・レイヤの質問（「どこに置くか」「どの package が持つか」「このレイヤで正しいか」）に使用。サブシステムの architecture、runtime 流れ、オンボーディングの mental model。動機は why を使用。"
disable-model-invocation: true
---

# How

コードベースを探索し「X はどう動くか」に答える。サブシステムにオンボーディングするシニア相当の architectural 説明。動く mental model が作れる程度に。annotated ソースのように読ませない。

各 spawn は `subagent_type: generalPurpose` かつ `readonly: true` の Task サブエージェント。explorer は `forge-models.mdc` の `how explorer` 行（default `cursor-grok-4.6-medium`）、explainer は `how explainer` 行（default `claude-opus-5.5-thinking-medium`）。`model` はその行の値、ルールや行が無ければ default。値が `inherit` なら `model` は未設定。Task ツールが slug を拒否したら default を使い、その旨を述べる。default も拒否されたらエラーメッセージから同族の最も近い有効 slug を使う。

## 1. Assess complexity

スコープが曖昧なら解釈を述べて探索する。ユーザーは差し替えできる。

- **Simple**（単一 module、小さな utility、「function X はどう動くか」など狭い質問）：explorer なし。`references/explainer-prompt.md` から explorer-findings セクションなしで組んだ 1 explainer が 1 パスで探索・説明。step 4 へ。
- **Complex**（複数 file/service にまたがるサブシステム、横断 feature、architecture 全体像）：step 2 へ。

迷ったら simple 経路。

## 2. Explore（complex のみ）

質問を 2〜4 の角度に分解。各角度はサブシステムの distinct な slice。1 メッセージで全 explorer を spawn。各 explorer に `references/explorer-prompt.md` と埋めた角度を渡す。

## 3. Synthesize（complex のみ）

全 explorer が戻ったら、1 explainer を spawn。`references/explainer-prompt.md` に各 explorer の findings をすべて埋める。

## 4. Present

explainer の出力を提示。会話文脈からの軽い編集は可。大幅な書き換えはしない。

## Output format

説明は `references/explainer-prompt.md` で定義されたセクションを使い、当てはまらないものは落とす：Overview、Key Concepts、How It Works、Where Things Live、Gotchas。

---
name: how
description: "「X はどう動くか」、変更前のコード walkthrough、配置・所有・レイヤの質問（「どこに置くか」「どの package が持つか」「このレイヤで正しいか」）に使用。サブシステムの architecture、runtime 流れ、オンボーディングの mental model。動機は why を使用。"
disable-model-invocation: true
---

# How

コードベースを探索し「X はどう動くか」に答える。サブシステムにオンボーディングするシニア相当の architectural 説明。動く mental model が作れる程度に。annotated ソースのように読ませない。

各 spawn は `forge-models.mdc` ルールの role 行と default を名指す。`model` はその行の値、ルールや行が無ければ default。値が `inherit` なら `model` は未設定。Task ツールが slug を拒否したら default を使い、その旨を述べる。default も拒否されたらエラーメッセージから同族の最も近い有効 slug を使う。

## Step 1. Assess Complexity

スコープが曖昧なら解釈を述べて探索する。ユーザーは差し替えできる。

- **Simple**（単一 module、小さな utility、「function X はどう動くか」など狭い質問）：explorer なし。1 explainer が 1 パスで探索・説明。Step 2b。
- **Complex**（複数 file/service にまたがるサブシステム、横断 feature、architecture 全体像）：先に parallel explorer、その後 explainer に渡す。Step 2a。

迷ったら simple 経路。

## Step 2a. Explore（complex のみ）

質問を 2〜4 の探索角度に分解。各角度はサブシステムの distinct な slice。1 メッセージで全 explorer を spawn：

- `subagent_type`: `generalPurpose`
- `model`: `how explorer` 行、default `cursor-grok-4.6-medium`
- `readonly`: `true`

各 explorer は `references/explorer-prompt.md` のプロンプトに角度を埋める。Step 3。

## Step 2b. Direct Explain（simple）

1 Task サブエージェントが 1 パスで探索・説明：

- `subagent_type`: `generalPurpose`
- `model`: `how explainer` 行、default `claude-opus-5.5-thinking-medium`
- `readonly`: `true`

`references/explainer-prompt.md` から explorer-findings セクションなしでプロンプトを組む。Step 4。

## Step 3. Synthesize（complex のみ）

全 explorer が戻ったら、1 Task で findings を 1 本の説明に合成：

- `subagent_type`: `generalPurpose`
- `model`: `how explainer` 行、default `claude-opus-5.5-thinking-medium`
- `readonly`: `true`

`references/explainer-prompt.md` に各 explorer の findings をすべて埋めてプロンプトを組む。

## Step 4. Present

explainer の出力をユーザーに提示。会話文脈からの軽い編集は可。大幅な書き換えはしない。

## Output Format

説明は `references/explainer-prompt.md` で定義されたセクションを使い、当てはまらないものは落とす：Overview、Key Concepts、How It Works、Where Things Live、Gotchas。
